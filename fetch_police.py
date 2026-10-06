"""
Keeps the Maldives Police Service case counts up to date, for the priorities page.

Runs every morning in GitHub Actions. It opens https://www.police.gov.mv/crime-statistics
in a headless browser, clicks each year and month, and reads the "Detailed breakdown" table.
On the first run it reads every year the page offers. After that it reads only the current
and previous year, because older figures don't change.

Writes:
  data/police/crime_monthly.csv   year, month (0 = the whole year as shown), category, cases
  data/police/fetch_log.json      when it last ran, what it found, and any background
                                  requests the page made (useful if a JSON API appears)

If the page can't be read, the existing data is kept and the run carries on.

To run it yourself:
    pip install playwright
    playwright install chromium
    python fetch_police.py            # current and previous year
    python fetch_police.py --all      # every year
"""
import asyncio
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

URL = "https://www.police.gov.mv/crime-statistics"
HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "police"
CSV = OUT / "crime_monthly.csv"
LOG = OUT / "fetch_log.json"
COLS = ["year", "month", "category", "cases", "retrieved"]
MONTHS = ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PAUSE_MS = 1500


def to_int(text):
    d = re.sub(r"[^\d]", "", text or "")
    return int(d) if d else 0


def read_existing():
    if not CSV.exists():
        return []
    with open(CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


async def read_breakdown(page):
    rows = []
    for tr in await page.locator("table tbody tr").all():
        cells = await tr.locator("td").all_inner_texts()
        if len(cells) >= 2:
            cat = cells[0].strip().split("\n")[0].strip()
            if cat:
                rows.append((cat, to_int(cells[-1])))
    if rows:
        return rows
    text = await page.inner_text("body")
    for m in re.finditer(r"\n([A-Za-z][A-Za-z ]+)\n\s*([\d,]+) cases", text):
        rows.append((m.group(1).strip(), to_int(m.group(2))))
    return rows


async def total_shown(page):
    text = await page.inner_text("body")
    m = re.search(r"TOTAL CASES\s*\n\s*([\d,]+)", text, re.I)
    return to_int(m.group(1)) if m else None


async def click(page, label):
    btn = page.get_by_role("button", name=re.compile(rf"^\s*{label}\s*$", re.I))
    if await btn.count() == 0:
        return False
    await btn.first.click()
    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    await page.wait_for_timeout(PAUSE_MS)
    return True


async def scrape(years_wanted):
    from playwright.async_api import async_playwright
    found, requests_seen, problems = [], [], []
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (compatible; mvdebtclock.org data update)")

        async def on_response(resp):
            if resp.request.resource_type in ("fetch", "xhr"):
                requests_seen.append({"url": resp.url, "status": resp.status, "type": resp.headers.get("content-type", "")})
        page.on("response", on_response)

        await page.goto(URL, wait_until="networkidle", timeout=60000)
        years = [y.strip() for y in await page.get_by_role("button", name=re.compile(r"^\s*20\d\d\s*$")).all_inner_texts()]
        if years_wanted:
            years = [y for y in years if int(y) in years_wanted]
        for y in years:
            await click(page, y)
            for i, m in enumerate(MONTHS):
                if not await click(page, m):
                    continue
                rows = await read_breakdown(page)
                shown = await total_shown(page)
                if shown is not None and rows and sum(n for _, n in rows) != shown:
                    problems.append(f"{y} {m}: categories add to {sum(n for _, n in rows)}, page total {shown}")
                for cat, n in rows:
                    found.append({"year": int(y), "month": i, "category": cat, "cases": n, "retrieved": stamp})
                print(f"  {y} {m:>3}: {len(rows)} categories, {sum(n for _, n in rows):,} cases")
        await browser.close()
    return found, requests_seen, problems


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    existing = read_existing()
    now_year = datetime.now(timezone.utc).year
    have_years = {int(r["year"]) for r in existing}
    full = "--all" in sys.argv or not have_years or min(have_years) >= now_year - 1   # older years not read yet
    wanted = None if full else {now_year, now_year - 1}
    try:
        found, seen, problems = asyncio.run(scrape(wanted))
    except Exception as e:
        print(f"Couldn't read the police statistics page ({e}). Keeping the existing data.")
        LOG.write_text(json.dumps({"checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": False, "error": str(e)}, indent=1))
        return
    if not found:
        print("The police statistics page returned no figures. Keeping the existing data.")
        return
    redone = {(r["year"], r["month"]) for r in found}
    keep = [r for r in existing if (int(r["year"]), int(r["month"])) not in redone]
    rows = sorted(keep + found, key=lambda r: (int(r["year"]), int(r["month"]), -int(r["cases"])))
    with open(CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    LOG.write_text(json.dumps({"checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": True,
                               "rows": len(rows), "problems": problems, "background_requests": seen[:200]}, indent=1))
    print(f"Wrote {CSV.relative_to(HERE)}: {len(rows)} rows." + (f" {len(problems)} totals didn't match, see fetch_log.json." if problems else ""))


if __name__ == "__main__":
    main()
