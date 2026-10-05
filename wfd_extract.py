"""
Downloads every Weekly Fiscal Developments (WFD) report from the Ministry of Finance website
and turns the tables into spreadsheets.

Setup (once):
    pip install requests pdfplumber

Run:
    python wfd_extract.py              download anything new, then extract everything
    python wfd_extract.py download     only download
    python wfd_extract.py extract      only extract from PDFs already downloaded

Output (folder wfd/):
    pdfs/                     one PDF per report, named by its "as at" date, e.g. 2026-09-24.pdf
    reports.csv               every report found on the website, with its link and date
    wfd_headline.csv          one row per report: revenue, spending, deficit, interest and other key totals
    wfd_long.csv              every row of every table in every report (approved, last year, this year)
    wfd_checks.csv            reports where the tables don't add up, or a figure couldn't be read
"""
import csv
import html
import re
import sys
import time
from datetime import date
from pathlib import Path

try:
    import requests
    import pdfplumber
except ImportError:
    sys.exit("Please run:  pip install requests pdfplumber")

PAGE = "https://www.finance.gov.mv/publications/statistical-releases/weekly-fiscal-developments"
OUT = Path(__file__).resolve().parent / "wfd"
PDFS = OUT / "pdfs"
MONTHS = {m: i + 1 for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july",
                                          "august", "september", "october", "november", "december"])}
HEADERS = {"User-Agent": "Mozilla/5.0 (research download of Weekly Fiscal Developments)"}


# ---------------------------------------------------------------- download
def list_reports():
    r = requests.get(PAGE, headers=HEADERS, timeout=60)
    r.raise_for_status()
    found, seen, last_year = [], set(), None
    for href, text in re.findall(r'<a[^>]+href="([^"]+?\.pdf)"[^>]*>(.*?)</a>', r.text, flags=re.S | re.I):
        text = html.unescape(re.sub(r"<[^>]+>", "", text)).strip()
        if "weekly fiscal" not in text.lower() or href in seen:
            continue
        seen.add(href)
        m = re.search(r"as at\s+(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)(?:\s+(\d{4}))?", text, flags=re.I)
        if not m or m.group(2).lower() not in MONTHS:
            print(f"  can't read a date from: {text}")
            continue
        year = int(m.group(3)) if m.group(3) else last_year   # a few 2024 links leave out the year
        if year is None:
            print(f"  can't read a year from: {text}")
            continue
        last_year = year
        d = date(year, MONTHS[m.group(2).lower()], int(m.group(1)))
        url = href if href.startswith("http") else "https://www.finance.gov.mv" + href
        found.append({"as_at": d.isoformat(), "revised": "revised" in text.lower(), "title": text, "url": url})
    return found


def download():
    PDFS.mkdir(parents=True, exist_ok=True)
    print("Reading the list of reports from the Ministry of Finance website...")
    reports = list_reports()
    if not reports:
        sys.exit("No report links found. The Ministry may have changed its website. Send the error to Claude.")
    print(f"Found {len(reports)} reports, from {min(r['as_at'] for r in reports)} to {max(r['as_at'] for r in reports)}.")
    with open(OUT / "reports.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["as_at", "revised", "title", "url", "file"])
        w.writeheader()
        new = 0
        for rep in sorted(reports, key=lambda r: r["as_at"]):
            name = rep["as_at"] + ("_revised" if rep["revised"] else "") + ".pdf"
            path = PDFS / name
            if path.exists() and path.stat().st_size > 1000:
                rep["file"] = name
                w.writerow(rep)
                continue
            for attempt in range(4):
                try:
                    resp = requests.get(rep["url"], headers=HEADERS, timeout=120)
                    resp.raise_for_status()
                    if not resp.content.startswith(b"%PDF"):
                        raise RuntimeError("not a PDF")
                    path.write_bytes(resp.content)
                    new += 1
                    print(f"  downloaded {name}")
                    break
                except Exception as e:
                    print(f"  problem with {name} ({e}), retrying")
                    time.sleep(5 * (attempt + 1))
            else:
                print(f"  gave up on {name}")
            rep["file"] = name if path.exists() else ""
            w.writerow(rep)
            time.sleep(1)
    print(f"{new} new PDFs downloaded into {PDFS}")


# ---------------------------------------------------------------- reading numbers
TOKEN_NUM = re.compile(r"^\(?-?\d{1,3}(?:,\d{3})*\.\d+\)?$|^-$")
TOKEN_INT = re.compile(r"^\(?-?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?$|^-$")   # securities tables in older reports use whole numbers
CONCAT_NUM = re.compile(r"\(?\d{1,3}(?:,\d{3})*\.\d\)?|-")
NUMISH = re.compile(r"^[\d,.()\-]+$")


def to_float(s):
    if s == "-":
        return 0.0
    neg = s.startswith("(")
    v = float(s.strip("()").replace(",", ""))
    return -v if neg else v


def split_row(line, allow_int=False):
    """Split 'Label 1,234.5 6 ,789.0 (12.3)' into ('Label', [1234.5, 6789.0, -12.3]).
    The PDFs sometimes put stray spaces inside numbers, so when the plain split fails the numbers
    are joined up and re-split, using the fact that every figure has exactly one decimal place."""
    toks = line.split()
    i = len(toks)
    while i > 0 and NUMISH.match(toks[i - 1]):
        i -= 1
    label, tail = " ".join(toks[:i]).strip(), toks[i:]
    if not tail:
        return None
    if allow_int:
        # securities tables: whole numbers, sometimes with stray spaces ("7 ,703", "2 5,800").
        # Try the plain split and a version with the broken pieces joined, and keep whichever
        # has its maturity columns adding up to the TOTAL column.
        cands = []
        if all(TOKEN_INT.match(t) for t in tail):
            cands.append([to_float(t) for t in tail])
        merged, i2 = [], 0
        while i2 < len(tail):
            t = tail[i2]
            while i2 + 1 < len(tail) and (tail[i2 + 1].startswith(",") or (re.fullmatch(r"\d", t) and re.fullmatch(r"\d{1,2}(?:,\d{3})*(?:\.\d+)?", tail[i2 + 1]))):
                t += tail[i2 + 1]; i2 += 1
            merged.append(t); i2 += 1
        if all(TOKEN_INT.match(t) for t in merged):
            cands.append([to_float(t) for t in merged])
        for c in cands:
            if len(c) > 2 and abs(sum(c[:-1]) - c[-1]) <= max(2.0, abs(c[-1]) * 0.001):
                return label, c
        if cands and not all(TOKEN_NUM.match(t) for t in tail):
            joined = "".join(tail)
            parts = CONCAT_NUM.findall(joined)
            if "".join(parts) == joined:
                return label, [to_float(p) for p in parts]
            return label, cands[-1]
    if all(TOKEN_NUM.match(t) for t in tail):
        return label, [to_float(t) for t in tail]
    joined = "".join(tail)
    parts = CONCAT_NUM.findall(joined)
    if "".join(parts) != joined:
        return None
    return label, [to_float(p) for p in parts]


TABLES = [  # (key, words that start the table heading)
    ("summary", ("summary of government finances",)),
    ("revenue", ("revenue details",)),
    ("expenditure", ("expenditure details",)),
    ("psip", ("public sector investment",)),
    ("agencies", ("budget utilization of accountable", "budget utilisation of accountable")),
    ("securities", ("government securities",)),   # also "TABLE 5: Government Securities" in older reports
]


def table_of(line, current):
    low = line.lower()
    if low.startswith("table") or low.startswith("government securities"):
        for key, words in TABLES:
            if any(w in low for w in words):
                return key
    if low.startswith("definitions"):
        return None
    return current


def norm(label):
    s = re.sub(r"\d+/", "", label)                  # footnote marks like 1/ or 2/
    s = re.sub(r"^[A-G]\s+(?=[A-Z])", "", s)         # row letters A to G in table 1
    s = re.sub(r"^\d+\.?\s+", "", s)                 # numbering in the agency and PSIP tables
    return re.sub(r"\s+", " ", s).strip().lower()


def read_pdf(path):
    with pdfplumber.open(path) as pdf:
        return [(p.extract_text() or "") for p in pdf.pages]


def parse_report(pages):
    meta, rows, table, pending = {}, [], None, None
    text = "\n".join(pages)
    m = re.search(r"as at\s+(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text)
    if m and m.group(2).lower() in MONTHS:
        meta["pdf_as_at"] = date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
    m = re.search(r"WFD/(\d+)/(\d{4})", text)
    if m:
        meta["week"], meta["series_year"] = int(m.group(1)), int(m.group(2))
    m = re.search(r"Government Securities Outstanding as of\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})", text)
    if m:
        meta["securities_as_of"] = m.group(1)
    order, header_years, in_header, memo = 0, [], False, False
    for page_no, page in enumerate(pages, 1):
        for raw in page.splitlines():
            line = raw.strip()
            if not line or line.lower().startswith("weekly fiscal developments |"):
                continue
            before = table
            table = table_of(line, table)
            if table is None:
                continue  # the dashboard on page 1 of newer reports comes before any table heading
            if table == "summary" and before != "summary" and not header_years:
                in_header = True
            if before != table:
                memo = False
            if line.lower().startswith("memorandum"):
                memo = True
                continue
            got = split_row(line, allow_int=(table == "securities"))
            if in_header:
                if got is None or not re.search(r"[A-Za-z]{3}", got[0]):
                    # column headings of table 1: note the order of the years, e.g. "2025 2026" or "2020 ... 2019*"
                    header_years += [int(y) for y in re.findall(r"\b(20\d\d)\b", line)]
                    continue
                in_header = False
                meta["header_years"] = header_years
            if got is None:
                # a label on its own line, with its numbers on the next line
                pending = line if re.search(r"[A-Za-z]", line) and not re.search(r"\d{3}", line) else None
                continue
            label, vals = got
            if pending and not re.search(r"[A-Za-z]{3}", label):
                label = pending
            pending = None
            if not re.search(r"[A-Za-z]{3}", label):
                continue
            order += 1
            rows.append({"table": table, "page": page_no, "row": order, "label": label, "key": norm(label), "values": vals, "memo": memo})
    return meta, rows


# ---------------------------------------------------------------- headline figures
HEADLINE = [  # (column, table, key starts with)
    ("revenue_and_grants", "summary", ("total revenues and grants", "total revenue and grants")),
    ("tax_revenue", "summary", ("tax revenues",)),
    ("non_tax_revenue", "summary", ("non-tax revenues",)),
    ("grants", "summary", ("grants",)),
    ("total_expenditure", "summary", ("total expenditure",)),
    ("recurrent_expenditure", "summary", ("recurrent expenditure",)),
    ("capital_expenditure", "summary", ("capital expenditure",)),
    ("salaries_wages_pensions", "summary", ("salaries, wages and pensions", "salaries and wages and pensions")),
    ("primary_balance", "summary", ("primary balance",)),
    ("overall_balance", "summary", ("overall balance",)),
    ("interest_costs", "summary", ("financing and interest costs",)),
    ("loan_repayment", "summary", ("loan repayment",)),
    ("transfers_to_sdf", "summary", ("transfers to sovereign development fund",)),
    ("psip", "summary", ("public sector investment program",)),
    ("tourism_gst", "revenue", ("tourism goods and services tax",)),
    ("general_gst", "revenue", ("general goods and services tax",)),
    ("import_duties", "revenue", ("import duties",)),
    ("green_tax", "revenue", ("green tax",)),
    ("rent_from_resorts", "revenue", ("rent from resorts",)),
    ("soe_dividends", "revenue", ("soe dividends",)),
    ("subsidies", "expenditure", ("subsidies",)),
    ("aasandha", "expenditure", ("aasandha",)),
]
SECURITIES = [("securities_total", "total securities outstanding"), ("securities_domestic", "domestic instruments"),
              ("securities_external", "external instruments")]


def columns_for(vals, ncols, this_year_first=False):
    """Tables have either 2 columns (approved, this year) or 3. With 3, most years run
    approved, same day last year, this year; reports from 2020 put this year before last year."""
    if len(vals) == ncols == 3:
        return (vals[0], vals[2], vals[1]) if this_year_first else (vals[0], vals[1], vals[2])
    if len(vals) == ncols == 2:
        return vals[0], None, vals[1]
    return None, None, None


HEAD_COLS = ["as_at", "week", "pdf_as_at", "file", "columns", "column_order"] + \
            [x for c, _, _ in HEADLINE for x in (c, c + "_approved", c + "_last_year")] + \
            ["securities_as_of"] + [c for c, _ in SECURITIES]
LONG_COLS = ["as_at", "table", "page", "row", "label", "approved", "last_year", "this_year", "memo", "all_values", "file"]
ESSENTIAL = ("revenue_and_grants", "total_expenditure", "overall_balance", "interest_costs")


def summarise(d, fname, meta, rows):
    """Turn one parsed report into (headline row, table rows, problems)."""
    problems, long_rows = [], []
    # "contains" rather than "starts with": in a few reports a watermark is printed over this label
    tot = next((r for r in rows if r["table"] == "summary" and re.search(r"revenues? and grants", r["key"])), None)
    ncols = len(tot["values"]) if tot else None
    yrs = [y for y in meta.get("header_years", []) if 2000 < y < 2100]
    flip = len(yrs) >= 2 and yrs[0] > yrs[-1]   # e.g. "2020 ... 2019*": this year comes first
    if ncols not in (2, 3):
        problems.append("couldn't find table 1 (summary of government finances)")
    for r in rows:
        if r["table"] == "securities":
            a, b, c = None, None, r["values"][-1]
        else:
            a, b, c = columns_for(r["values"], ncols, flip)
        long_rows.append([d, r["table"], r["page"], r["row"], r["label"], a, b, c, int(r.get("memo", False)),
                          " ".join(str(v) for v in r["values"]), fname])
    h = {"as_at": d, "week": meta.get("week"), "pdf_as_at": meta.get("pdf_as_at"), "file": fname, "columns": ncols,
         "column_order": ("approved, this year, last year" if flip else "approved, last year, this year") if ncols == 3 else ("approved, this year" if ncols == 2 else ""),
         "securities_as_of": meta.get("securities_as_of")}
    for col, table, starts in HEADLINE:
        if col == "revenue_and_grants":
            r = tot
        else:
            r = next((r for r in rows if r["table"] == table and r["key"].startswith(starts)), None)
        if r:
            a, b, c = columns_for(r["values"], ncols, flip)
            h[col], h[col + "_approved"], h[col + "_last_year"] = c, a, b
        elif table == "summary" and col not in ("psip", "salaries_wages_pensions", "transfers_to_sdf", "grants"):
            problems.append(f"no '{starts[0]}' row in table 1")
    for col, start in SECURITIES:
        r = next((r for r in rows if r["table"] == "securities" and r["key"].startswith(start)), None)
        if r:
            h[col] = r["values"][-1]
    if h.get("securities_total") is None:
        # reports before 2022 used a different securities table, ending in a TOTAL row
        r = next((r for r in rows if r["table"] == "securities" and r["key"] == "total"), None)
        if r and len(r["values"]) in (3, 7):
            v = r["values"][-1] if len(r["values"]) == 3 else r["values"][5]   # closing balance
            h["securities_total"] = round(v / 1e6, 1) if v > 1e7 else v      # some years are in rufiyaa, not millions

    def close(a, b, tol=1.0):
        return a is not None and b is not None and abs(a - b) <= tol
    if all(h.get(k) is not None for k in ("total_expenditure", "recurrent_expenditure", "capital_expenditure")):
        if not close(h["total_expenditure"], h["recurrent_expenditure"] + h["capital_expenditure"]):
            problems.append(f"total spending {h['total_expenditure']} isn't recurrent + capital ({h['recurrent_expenditure'] + h['capital_expenditure']:.1f})")
    if all(h.get(k) is not None for k in ("revenue_and_grants", "total_expenditure", "overall_balance")):
        if not close(h["overall_balance"], h["revenue_and_grants"] - h["total_expenditure"]):
            problems.append(f"overall balance {h['overall_balance']} isn't revenue minus spending ({h['revenue_and_grants'] - h['total_expenditure']:.1f})")
    if meta.get("pdf_as_at") and meta["pdf_as_at"] != d:
        problems.append(f"note: the report itself says 'as at {meta['pdf_as_at']}'")
    return h, long_rows, problems


def usable(h, problems):
    """Good enough to publish: the main totals were read and add up."""
    return all(h.get(k) is not None for k in ESSENTIAL) and not any(p.startswith(("total spending", "overall balance", "couldn't")) for p in problems)


def extract():
    files = sorted(PDFS.glob("*.pdf"))
    if not files:
        sys.exit(f"No PDFs in {PDFS}. Run:  python wfd_extract.py download")
    # where a revised report exists, use it instead of the original for that date
    best = {}
    for f in files:
        d = f.stem.split("_")[0]
        if d not in best or "revised" in f.stem:
            best[d] = f
    fl = open(OUT / "wfd_long.csv", "w", newline="", encoding="utf-8")
    fh = open(OUT / "wfd_headline.csv", "w", newline="", encoding="utf-8")
    fc = open(OUT / "wfd_checks.csv", "w", newline="", encoding="utf-8")
    wl, wh, wc = csv.writer(fl), csv.DictWriter(fh, fieldnames=HEAD_COLS), csv.writer(fc)
    wl.writerow(LONG_COLS)
    wh.writeheader()
    wc.writerow(["as_at", "file", "problem"])
    n_ok = 0
    for d, f in sorted(best.items()):
        try:
            meta, rows = parse_report(read_pdf(f))
        except Exception as e:
            wc.writerow([d, f.name, f"couldn't open the PDF: {e}"])
            print(f"  {f.name}: couldn't open ({e})")
            continue
        h, long_rows, problems = summarise(d, f.name, meta, rows)
        wl.writerows(long_rows)
        wh.writerow(h)
        for p in problems:
            wc.writerow([d, f.name, p])
        n_ok += 1
        print(f"  {f.name}: {len(rows)} rows, revenue {h.get('revenue_and_grants')}, spending {h.get('total_expenditure')}")
    fl.close(); fh.close(); fc.close()
    print(f"\nDone. {n_ok} reports extracted into {OUT}. Check wfd_checks.csv for anything that didn't add up.")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    OUT.mkdir(exist_ok=True)
    if what in ("all", "download"):
        download()
    if what in ("all", "extract"):
        extract()
