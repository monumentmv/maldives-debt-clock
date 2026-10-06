"""
Collects every year and every month from the Maldives Police Service crime statistics page
(https://www.police.gov.mv/crime-statistics) and saves it to data/police/crime_monthly.csv.

The page shows one period at a time: a year (2017 onwards) and either the whole year or a month.
This script clicks every combination, waits until the page says it is showing that period,
reads the "Detailed breakdown" table, and checks the categories add up to the total shown.

First time (collects everything, about 10 to 20 minutes):
    pip install playwright
    python -m playwright install chromium
    python fetch_police.py --all

Every day after that (GitHub Actions runs this): only the current and previous year are read
again, and everything else already saved is kept.
    python fetch_police.py

Other options:
    --years 2022 2023   read just these years
    --show              open a visible browser window, to watch what it does

Output columns: year, month (0 = the whole year), category, cases, retrieved
Anything it couldn't read is listed in data/police/fetch_log.json, and the old figures are kept.
"""
import argparse
import asyncio
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

URL = os.environ.get("POLICE_URL", "https://www.police.gov.mv/crime-statistics")
HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "police"
CSV_PATH = OUT / "crime_monthly.csv"
LOG_PATH = OUT / "fetch_log.json"
COLS = ["year", "month", "category", "cases", "retrieved"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TIMEOUT_MS = 20000


def to_int(text):
    d = re.sub(r"[^\d]", "", text or "")
    return int(d) if d else 0


def load_existing():
    if not CSV_PATH.exists():
        return []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(rows):
    OUT.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: (int(r["year"]), int(r["month"]), -int(r["cases"]), r["category"]))
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)


async def page_state(page):
    """What the page says it is showing, the total, and the rows of the breakdown table."""
    return await page.evaluate("""() => {
        const text = document.body.innerText;
        const label = (text.match(/Period overview\\s*\\n\\s*([^\\n]+)/i) || [])[1] || "";
        const total = (text.match(/TOTAL CASES\\s*\\n\\s*([\\d,]+)/i) || [])[1] || "";
        const rows = [];
        document.querySelectorAll("table tbody tr").forEach(tr => {
            const td = [...tr.querySelectorAll("td")].map(x => x.innerText.trim());
            if (td.length >= 2) rows.push([td[0].split("\\n")[0].trim(), td[td.length - 1]]);
        });
        return { label: label.trim(), total, rows };
    }""")


async def click_button(page, text):
    btn = page.get_by_role("button", name=re.compile(rf"^\s*{re.escape(text)}\s*$", re.I))
    if await btn.count() == 0:
        return False
    first = btn.first
    if await first.is_disabled():
        return False
    await first.click()
    return True


async def wait_for_period(page, expected_label, before=None):
    """Wait until the page shows the period asked for, the figures have actually arrived
    (the page shows 0 for a moment while it fetches them), and they have stopped changing."""
    try:
        await page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    deadline = asyncio.get_event_loop().time() + 30
    last, same = None, 0
    st = await page_state(page)
    while asyncio.get_event_loop().time() < deadline:
        st = await page_state(page)
        key = (st["total"], tuple(map(tuple, st["rows"])))
        if st["label"].lower() == expected_label.lower() and to_int(st["total"]) > 0 and st["rows"] and (before is None or key != before):
            same = same + 1 if key == last else 0
            last = key
            if same >= 2:
                return st
        await page.wait_for_timeout(600)
    return st


async def read_period(page, year, month_index):
    """month_index 0 = the whole year, 1..12 = a month"""
    expected = str(year) if month_index == 0 else f"{MONTHS[month_index - 1]} {year}"
    b4 = await page_state(page)
    before = (b4["total"], tuple(map(tuple, b4["rows"]))) if b4["label"].lower() != expected.lower() else None
    if not await click_button(page, "All" if month_index == 0 else MONTHS[month_index - 1]):
        return None, f"{expected}: no button"
    st = await wait_for_period(page, expected, before)
    if to_int(st["total"]) == 0:
        return None, f"{expected}: page showed no cases"
    if st["label"].lower() != expected.lower():
        return None, f"{expected}: page showed '{st['label']}'"
    rows = [(c, to_int(n)) for c, n in st["rows"] if c]
    total = to_int(st["total"])
    if rows and total and sum(n for _, n in rows) != total:
        # one more try, the table sometimes redraws a moment after the total
        await page.wait_for_timeout(1500)
        st = await page_state(page)
        rows = [(c, to_int(n)) for c, n in st["rows"] if c]
        total = to_int(st["total"])
        if sum(n for _, n in rows) != total:
            return None, f"{expected}: categories add to {sum(n for _, n in rows)} but total is {total}"
    return rows, None


async def run(years_wanted, show):
    from playwright.async_api import async_playwright
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    existing = load_existing()
    found, problems = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not show)
        page = await browser.new_page(user_agent="Mozilla/5.0 (compatible; mvdebtclock.org data update)")
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.get_by_text("Detailed breakdown").first.wait_for(timeout=60000)
        year_btns = page.get_by_role("button", name=re.compile(r"^\s*20\d\d\s*$"))
        years = sorted({int(t.strip()) for t in await year_btns.all_inner_texts()}, reverse=True)
        if years_wanted:
            years = [y for y in years if y in years_wanted]
        print(f"Years to read: {years}")
        for year in years:
            if not await click_button(page, str(year)):
                problems.append(f"{year}: no year button")
                continue
            await wait_for_period(page, str(year))
            year_rows = []
            for mi in range(0, 13):
                rows, err = await read_period(page, year, mi)
                label = "whole year" if mi == 0 else MONTHS[mi - 1]
                if err:
                    if "no button" not in err:
                        problems.append(err)
                    print(f"  {year} {label:>10}: skipped ({err})")
                    continue
                for c, n in rows:
                    year_rows.append({"year": year, "month": mi, "category": c, "cases": n, "retrieved": stamp})
                print(f"  {year} {label:>10}: {sum(n for _, n in rows):>6,} cases in {len(rows)} categories")
            found += year_rows
            # save after every year, so a stopped run keeps what it already read
            done = {(int(r["year"]), int(r["month"])) for r in found}
            keep = [r for r in existing if (int(r["year"]), int(r["month"])) not in done]
            save(keep + found)
        await browser.close()
    return found, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="read every year the page offers")
    ap.add_argument("--years", nargs="*", type=int, help="read only these years")
    ap.add_argument("--show", action="store_true", help="show the browser window")
    a = ap.parse_args()
    existing = load_existing()
    now_year = datetime.now(timezone.utc).year
    have = {int(r["year"]) for r in existing}
    if a.years:
        wanted = set(a.years)
    elif a.all or not have or min(have) >= now_year - 1:
        wanted = None                       # everything
    else:
        wanted = {now_year, now_year - 1}   # daily: just the latest two years
    try:
        found, problems = asyncio.run(run(wanted, a.show))
    except Exception as e:
        print(f"Couldn't read the police statistics page ({e}). The saved figures are unchanged.")
        OUT.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(json.dumps({"checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": False, "error": str(e)}, indent=1))
        return
    LOG_PATH.write_text(json.dumps({"checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": True,
                                    "periods_read": len({(r['year'], r['month']) for r in found}), "problems": problems}, indent=1))
    total_rows = len(load_existing())
    print(f"\nDone. {len({(r['year'], r['month']) for r in found})} periods read, {total_rows} rows in {CSV_PATH.relative_to(HERE)}."
          + (f" {len(problems)} periods couldn't be read, see {LOG_PATH.relative_to(HERE)}." if problems else ""))


if __name__ == "__main__":
    main()
