"""
Downloads every year and every month from the Maldives Police Service crime statistics page
https://www.police.gov.mv/crime-statistics
and saves them to police_crime_stats.csv in the same folder as this script.

HOW TO RUN (Windows, Mac or Linux)
  1. Install Python 3 from python.org if you don't have it (tick "Add Python to PATH" on Windows).
  2. Open a terminal (Command Prompt on Windows) in the folder where this file is, then run:
         pip install playwright
         python -m playwright install chromium
         python police_crime_stats.py
  3. Wait until it says "Finished". It takes about 10 to 20 minutes.
  4. Send me police_crime_stats.csv (and police_debug.txt if anything went wrong).

Options
  python police_crime_stats.py --show          watch the browser while it works
  python police_crime_stats.py --years 2025    just one year (or several: --years 2024 2025)
  python police_crime_stats.py --redo          fetch everything again (normally it keeps what is already saved)

Output columns
  year, month (0 = whole year, 1-12 = January to December), category, cases, total_shown, retrieved
"""
import argparse
import asyncio
import csv
import json
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

URL = "https://www.police.gov.mv/crime-statistics"
HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "police_crime_stats.csv"
DEBUG_PATH = HERE / "police_debug.txt"
API_PATH = HERE / "police_api_log.json"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
COLS = ["year", "month", "category", "cases", "total_shown", "retrieved"]

debug_lines = []


def log(msg):
    print(msg, flush=True)
    debug_lines.append(msg)


def to_int(text):
    d = re.sub(r"[^\d]", "", text or "")
    return int(d) if d else 0


async def state(page):
    """What the page is showing right now: the period label, the total and the table rows."""
    return await page.evaluate(r"""() => {
        const text = document.body.innerText;
        const label = (text.match(/Period overview\s*\n\s*([^\n]+)/i) || [])[1] || "";
        const total = (text.match(/TOTAL CASES\s*\n\s*([\d,]+)/i) || [])[1] || "";
        const rows = [];
        document.querySelectorAll("table tbody tr").forEach(tr => {
            const td = [...tr.querySelectorAll("td")].map(x => x.innerText.trim());
            if (td.length >= 2) rows.push([td[0].split("\n")[0].trim(), td[td.length - 1]]);
        });
        if (!rows.length) {   // if the table isn't a real <table>, read the "Theft / 2,649 cases" cards instead
            const re = /\n([A-Za-z][A-Za-z ]+)\n\s*([\d,]+) cases/g; let m;
            while ((m = re.exec(text))) rows.push([m[1].trim(), m[2]]);
        }
        return { label: label.trim(), total, rows };
    }""")


async def click(page, text):
    btn = page.get_by_role("button", name=re.compile(rf"^\s*{re.escape(text)}\s*$", re.I))
    if await btn.count() == 0:
        return False
    b = btn.first
    try:
        if await b.is_disabled():
            return False
        await b.scroll_into_view_if_needed()
        await b.click(timeout=10000)
        return True
    except Exception:
        return False


async def wait_for(page, expected, before=None, seconds=30):
    """Wait until the page says it shows `expected` (like "Feb 2022" or "2022"), the figures have
    actually arrived (the page shows 0 for a moment while it fetches them), and they stop changing."""
    try:
        await page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    loop = asyncio.get_event_loop()
    end = loop.time() + seconds
    last, same = None, 0
    st = await state(page)
    while loop.time() < end:
        st = await state(page)
        loaded = to_int(st["total"]) > 0 and st["rows"]
        fresh = before is None or (st["total"], tuple(map(tuple, st["rows"]))) != before
        if st["label"].lower() == expected.lower() and loaded and fresh:
            key = (st["total"], tuple(map(tuple, st["rows"])))
            same = same + 1 if key == last else 0
            last = key
            if same >= 2:          # the same figures three reads in a row
                return st, True
        await page.wait_for_timeout(600)
    # still nothing after the wait: the period really is empty, or the page is stuck
    return st, st["label"].lower() == expected.lower() and to_int(st["total"]) == 0


async def read_period(page, year, mi):
    expected = str(year) if mi == 0 else f"{MONTHS[mi - 1]} {year}"
    for attempt in range(3):
        b4 = await state(page)
        before = (b4["total"], tuple(map(tuple, b4["rows"])))
        if not await click(page, "All" if mi == 0 else MONTHS[mi - 1]):
            return None, "no button"
        st, ok = await wait_for(page, expected, before=before if b4["label"].lower() != expected.lower() else None)
        if not ok:
            log(f"    {expected}: page showed '{st['label']}', trying again")
            continue
        rows = [(re.sub(r"\s*[\d.]+%\s*of total.*$", "", c, flags=re.I).strip(), to_int(n)) for c, n in st["rows"] if c]
        total = to_int(st["total"])
        if rows and total and sum(n for _, n in rows) != total:
            log(f"    {expected}: categories add to {sum(n for _, n in rows)}, total {total}, trying again")
            await page.wait_for_timeout(1500)
            continue
        return (rows, total), None
    return None, "didn't settle after 3 tries"


def save(rows):
    rows = sorted(rows, key=lambda r: (int(r["year"]), int(r["month"]), -int(r["cases"]), r["category"]))
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)


def load_saved():
    if not CSV_PATH.exists():
        return []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if int(r.get("cases") or 0) >= 0]


async def main(years_wanted, show, redo):
    from playwright.async_api import async_playwright
    stamp = datetime.now().strftime("%Y-%m-%d")
    saved = [] if redo else load_saved()
    have = {(int(r["year"]), int(r["month"])) for r in saved if int(r.get("total_shown") or 0) > 0}
    out, problems, api = list(saved), [], []
    if have:
        log(f"Keeping {len(have)} periods already saved. Add --redo to fetch everything again.")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not show)
        page = await browser.new_page(viewport={"width": 1400, "height": 1000})

        # keep a note of any data the page loads in the background, in case it has a simpler data feed
        async def on_response(resp):
            if resp.request.resource_type in ("fetch", "xhr"):
                entry = {"url": resp.url, "status": resp.status, "type": resp.headers.get("content-type", "")}
                if "json" in entry["type"] and len(api) < 300:
                    try:
                        entry["body"] = await resp.json()
                    except Exception:
                        pass
                api.append(entry)
        page.on("response", on_response)

        log(f"Opening {URL}")
        await page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        await page.get_by_text("Detailed breakdown").first.wait_for(timeout=90000)
        await page.wait_for_timeout(2000)

        years = sorted({int(t.strip()) for t in await page.get_by_role("button", name=re.compile(r"^\s*20\d\d\s*$")).all_inner_texts()}, reverse=True)
        if years_wanted:
            years = [y for y in years if y in years_wanted]
        log(f"Years on the page: {years}")

        for year in years:
            if not await click(page, str(year)):
                problems.append(f"{year}: couldn't click the year")
                log(f"{year}: couldn't click the year button")
                continue
            await wait_for(page, str(year))
            log(f"{year}")
            for mi in range(13):
                name = "whole year" if mi == 0 else MONTHS[mi - 1]
                if (year, mi) in have:
                    log(f"    {name:>10}: already saved")
                    continue
                res, err = await read_period(page, year, mi)
                if err:
                    if err != "no button":
                        problems.append(f"{year} {name}: {err}")
                    log(f"    {name:>10}: skipped ({err})")
                    continue
                rows, total = res
                if not total:
                    problems.append(f"{year} {name}: page showed no cases")
                    log(f"    {name:>10}: no cases shown, skipped")
                    continue
                for c, n in rows:
                    out.append({"year": year, "month": mi, "category": c, "cases": n, "total_shown": total, "retrieved": stamp})
                log(f"    {name:>10}: {total:>6,} cases, {len(rows)} types")
            save(out)   # saved after every year, so nothing is lost if it stops
        await browser.close()

    API_PATH.write_text(json.dumps(api, indent=1, default=str), encoding="utf-8")
    periods = len({(r["year"], r["month"]) for r in out})
    log(f"\nFinished. {periods} periods saved to {CSV_PATH.name}.")
    if problems:
        log(f"{len(problems)} periods couldn't be read:")
        for x in problems:
            log("  " + x)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="show the browser window")
    ap.add_argument("--years", nargs="*", type=int, help="only these years")
    ap.add_argument("--redo", action="store_true", help="fetch everything again, ignoring what is already saved")
    a = ap.parse_args()
    try:
        asyncio.run(main(set(a.years) if a.years else None, a.show, a.redo))
    except ModuleNotFoundError:
        print("Playwright isn't installed. Run:  pip install playwright  then  python -m playwright install chromium")
        sys.exit(1)
    except Exception:
        log("Something went wrong:\n" + traceback.format_exc())
        print(f"\nPlease send me {DEBUG_PATH.name} (and {CSV_PATH.name} if it exists).")
    finally:
        DEBUG_PATH.write_text("\n".join(debug_lines), encoding="utf-8")
