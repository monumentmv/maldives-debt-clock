"""
Downloads MIRA's two monthly revenue spreadsheets into inputs/mira/ when MIRA publishes a new version.

Runs every morning in GitHub Actions, before build_revenue.py. MIRA gives each new upload a new link,
so the script reads the Revenue Series page to find the current links, downloads both files, and
replaces the copies in inputs/mira/ only if they have changed and look like the right files.
If anything goes wrong, the files already in inputs/mira/ are kept.

To run it yourself:
    pip install requests openpyxl
    python fetch_mira.py
"""
import hashlib
import io
import re
import sys
from pathlib import Path

import requests

try:
    import openpyxl
except ImportError:
    sys.exit("Please run:  pip install openpyxl")

PAGE = "https://www.mira.gov.mv/Publications/Categories/310"
HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs" / "mira"
# MIRA's site turns away requests that don't look like a browser, so ask like one
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-GB,en;q=0.9"}
FILES = {  # kind: (heading on MIRA's page, title inside the spreadsheet, file name we keep)
    "all": ("Total Revenue Collection", "TOTAL REVENUE COLLECTION", "mira_total_revenue_collection.xlsx"),
    "usd": ("USD Revenue Collection", "USD REVENUE COLLECTION", "mira_usd_revenue_collection.xlsx"),
}


def find_links(html):
    links = {}
    for kind, (heading, _, _) in FILES.items():
        m = re.search(re.escape(heading) + r"\s*\(\s*\d{4}\s*-\s*\d{4}\s*\).*?href=\"([^\"]*Files/GetFile/[^\"]+)\"", html, flags=re.S | re.I)
        if m:
            url = m.group(1)
            links[kind] = url if url.startswith("http") else "https://www.mira.gov.mv" + url
    return links


def title_of(content):
    ws = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True).worksheets[0]
    first = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), (None,))
    return str(first[0] or "").upper()


def existing(kind):
    """The spreadsheet of this kind already in inputs/mira/, whatever it is called."""
    for f in sorted(INPUTS.glob("*.xlsx")):
        try:
            if FILES[kind][1] in title_of(f.read_bytes()):
                return f
        except Exception:
            continue
    return None


class Plain:
    """Plain requests, with a browser's headers."""
    def page(self):
        r = requests.get(PAGE, headers=HEADERS, timeout=60)
        r.raise_for_status()
        return r.text

    def file(self, url):
        r = requests.get(url, headers=HEADERS, timeout=120)
        r.raise_for_status()
        return r.content

    def close(self):
        pass


class Browser:
    """A headless browser, for when MIRA's site refuses plain requests (GitHub Actions installs it for fetch_police.py)."""
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch()
        self.ctx = self.browser.new_context(user_agent=HEADERS["User-Agent"], locale="en-GB")

    def page(self):
        pg = self.ctx.new_page()
        resp = pg.goto(PAGE, wait_until="networkidle", timeout=90000)
        if resp and resp.status >= 400:
            raise RuntimeError(f"{resp.status} from MIRA's page in a browser too")
        return pg.content()

    def file(self, url):
        r = self.ctx.request.get(url, timeout=120000)   # shares the page's cookies
        if not r.ok:
            raise RuntimeError(f"{r.status} for the download")
        return r.body()

    def close(self):
        self.browser.close()
        self.pw.stop()


def main():
    INPUTS.mkdir(parents=True, exist_ok=True)
    web = Plain()
    try:
        html = web.page()
    except Exception as e:
        print(f"MIRA's page refused a plain request ({e}). Trying a browser.")
        try:
            web = Browser()
            html = web.page()
        except Exception as e2:
            print(f"Couldn't read MIRA's Revenue Series page ({e2}). Keeping the existing files.")
            if isinstance(web, Browser):
                web.close()
            return
    try:
        update(web, html)
    finally:
        web.close()


def update(web, html):
    links = find_links(html)
    if len(links) < 2:
        print(f"Found {len(links)} of 2 download links on MIRA's page. The page may have changed. Keeping the existing files.")
        return
    changed = 0
    for kind, url in links.items():
        heading, title, name = FILES[kind]
        try:
            content = web.file(url)
            if not content.startswith(b"PK"):
                raise RuntimeError("not an Excel file")
            if title not in title_of(content):
                raise RuntimeError(f"the spreadsheet's title doesn't mention '{title}'")
        except Exception as e:
            print(f"  {heading}: couldn't use the download ({e}). Keeping the existing file.")
            continue
        old = existing(kind)
        if old and hashlib.sha256(old.read_bytes()).digest() == hashlib.sha256(content).digest():
            print(f"  {heading}: no change.")
            continue
        if old and old.name != name:
            old.unlink()
        (INPUTS / name).write_bytes(content)
        changed += 1
        print(f"  {heading}: new version saved as inputs/mira/{name}.")
    print(f"{changed} MIRA file(s) updated.")


if __name__ == "__main__":
    main()
