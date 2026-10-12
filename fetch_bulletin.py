"""
The Ministry of Finance's Quarterly Debt Bulletins: what is still owed to each lender, repayments and interest
each quarter, money agreed but not yet paid out, and loans passed on to state companies.

Each run it:
  1. reads the list of bulletins on the Ministry of Finance website,
  2. downloads only bulletins it hasn't read yet (on the first run, every quarterly bulletin since 2023 Q1),
  3. reads every table, checks that each one adds up to its own total,
  4. saves the tables in data/bulletin/<year>-Q<n>.json.
build_lenders.py then puts them together (a newer bulletin's figures replace an older one's for the same
quarter, as the Ministry revises them) for the home page.

Each bulletin covers the last 12 quarters, so together they go back to mid-2020. The older half-yearly
bulletins (2018 to 2023) only give broad groups of lenders, so they are not read.

Runs every morning in GitHub Actions. To run it yourself:
    pip install requests pdfplumber
    python fetch_bulletin.py               (or: python fetch_bulletin.py some/folder/of/pdfs)
"""
import io
import json
import re
import sys
import time
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import pdfplumber
import requests

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "bulletin"
PAGE = "https://www.finance.gov.mv/publications/reports-and-analyses/quarterly-debt-bulletin"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
QEND = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}

# table title (as the bulletin words it, without its number) -> short name. Longer titles first, as
# "by Creditor" is the start of "by Creditor Category".
TABLES = [
    ("disbursed outstanding debt of public and publicly guaranteed", "ppg"),
    ("debt service cost of public and publicly guaranteed debt", "service"),
    ("debt outstanding of bcg external debt by creditor category", "gov_ext_cat"),
    ("debt outstanding of bcg external debt by creditor", "gov_ext"),
    ("debt outstanding of bcg external debt by currency", "gov_ext_cur"),
    ("principal repayments of bcg external debt by creditor category", "gov_ext_principal"),
    ("interest & other payments of bcg external debt by creditor category", "gov_ext_interest"),
    ("disbursements of bcg external debt by creditor category", "gov_disb_cat"),
    ("disbursements of bcg external debt by creditor", "gov_disb"),
    ("committed undisbursed balance", "cub"),
    ("outstanding of bcg domestic debt by creditor category", "gov_dom_cat"),
    ("outstanding of bcg domestic debt by currency", "gov_dom_cur"),
    ("outstanding of bcg domestic debt by type of instrument", "gov_dom_type"),
    ("outstanding of sg external debt by beneficiary", "sg_ext_ben"),
    ("outstanding of sg external debt by creditor category", "sg_ext_cat"),
    ("outstanding of sg external debt by creditor", "sg_ext"),
    ("outstanding of sg domestic debt by beneficiary", "sg_dom_ben"),
    ("outstanding of sg domestic debt by creditor", "sg_dom"),
    ("outstanding under subsidiary loans", "subsidiary"),
]
QTOK = re.compile(r"Q([1-4])[ ,]+(\d{4})")
SECTION = re.compile(r"^\d+(\.\d+)*\.?\s+[A-Z][a-z]")   # "8. Risks to Debt Portfolio", "5.1. BCG External Debt"
NUM = re.compile(r"^\(?-?[\d,]*\.?\d+\)?%?$|^-$")


def qdate(q, y):
    return f"{y}-{QEND[int(q)]}"


def number(t):
    if t == "-":
        return 0.0
    neg = t.startswith("(") or t.startswith("-")
    v = float(t.strip("()%-").replace(",", ""))
    return -v if neg else v


def table_key(line):
    t = re.sub(r"^[\d.\s]+", "", line).strip().lower()
    t = re.sub(r"\s+", " ", t)
    for title, key in TABLES:
        if t.startswith(title):
            return key
    return None


def parse(pdf_bytes):
    """{"quarter": "2026-06-30", "tables": {key: {row: {date: value}}}} from one bulletin."""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        lines = [ln.strip() for p in pdf.pages for ln in (p.extract_text() or "").splitlines()]
    # the bulletin's own quarter: the latest quarter in its tables (the title is worded differently over the years)
    heads = [qdate(q, y) for ln in lines if len(QTOK.findall(ln)) >= 3 for q, y in QTOK.findall(ln)]
    for a, b in zip(lines, lines[1:] + [""]):
        m = re.search(r"(Q[1-4]\s*){3,}$", a)
        if m and not re.search(r"\d[,.]\d", b):
            heads += [qdate(q, y) for q, y in zip(re.findall(r"Q([1-4])", m.group(0)), re.findall(r"\b(20\d\d)\b", b))]
    if not heads:
        raise RuntimeError("no quarterly tables: not a quarterly bulletin")
    quarter = max(heads)
    tables, key, cols, group, pending, qonly = {}, None, [], None, None, None
    for ln in lines:
        if "...." in ln or not ln:
            continue
        k = table_key(ln)
        if k or SECTION.match(ln):   # a new table, or a section we don't read
            key, cols, group, pending = k, [], None, None
            continue
        if key is None:
            continue
        qs = QTOK.findall(ln)
        if len(qs) >= 3:   # a header row of quarters
            cols, pending = [qdate(q, y) for q, y in qs], None
            continue
        m = re.search(r"(Q[1-4]\s*){3,}$", ln)
        if m:   # some bulletins split the header: "Q1 Q2 ..." then "2022 2022 ..."
            qonly = re.findall(r"Q([1-4])", m.group(0))
            continue
        ys = re.findall(r"\b(20\d\d)\b", ln)
        if qonly and len(ys) == len(qonly) and not re.search(r"\d[,.]\d", ln):
            cols, pending, qonly = [qdate(q, y) for q, y in zip(qonly, ys)], None, None
            continue
        if key == "subsidiary" and "outstanding as of" in ln.lower() and qs:
            cols = [qdate(*qs[0])]
            continue
        if not cols:
            continue
        toks = ln.split()
        vals = []
        while toks and NUM.match(toks[-1]) and len(vals) < len(cols):
            vals.insert(0, toks.pop())
        while toks and NUM.match(toks[-1]):   # a row with more figures than the header has quarters: the extra, oldest ones are dropped
            toks.pop()
        name = " ".join(toks).strip()
        if not vals:   # words only: may be a row name, with its figures on the next line
            pending = name if re.search(r"[A-Za-z]", name) and len(name) < 90 else None
            continue
        if len(vals) != len(cols):
            pending = None
            continue
        if not re.search(r"[A-Za-z]", name):
            if not pending:
                continue
            name = pending
        pending = None
        if "%" in "".join(vals):
            continue   # shares of GDP and of the total: worked out again from the amounts
        if name.isupper() and key in ("ppg", "service"):
            group = name
        elif group and key in ("ppg", "service"):
            name = f"{group} | {name}"
        row = tables.setdefault(key, {}).setdefault(name, {})
        for c, v in zip(cols, vals):
            row.setdefault(c, number(v))
        if name.upper() == "TOTAL" and key not in ("ppg", "service"):
            key = None   # the table ends at its total; what follows is a chart
    return {"quarter": quarter, "tables": tables}


def check(b):
    """Each table with a TOTAL row should add up to it. Returns a list of problems."""
    problems = []
    for key, rows in b["tables"].items():
        tot = next((r for n, r in rows.items() if n.upper() == "TOTAL"), None)
        if not tot or key in ("ppg", "service", "gov_dom_type"):
            continue
        for d, v in tot.items():
            s = sum(r.get(d, 0) for n, r in rows.items() if n.upper() != "TOTAL")
            if abs(s - v) > max(1.0, abs(v) * .002):
                problems.append(f"{key} {d}: rows add up to {s:,.1f}, total says {v:,.1f}")
    for need in ("gov_ext", "sg_ext", "service"):
        if need not in b["tables"]:
            problems.append(f"table {need} not found")
    return problems


def listing():
    r = requests.get(PAGE, headers=H, timeout=60)
    r.raise_for_status()
    found = {}
    for href, text in re.findall(r'<a[^>]+href="([^"]+?\.pdf)"[^>]*>(.*?)</a>', r.text, flags=re.S | re.I):
        text = " ".join(unescape(re.sub(r"<[^>]+>", " ", text)).split())
        m = re.search(r"quarterly debt bulletin\D*(\d{4})\s*Q([1-4])", text, flags=re.I) or re.search(r"quarterly debt bulletin\D*Q([1-4])\D*(\d{4})", text, flags=re.I)
        if not m:
            continue
        y, q = (m.group(1), m.group(2)) if len(m.group(1)) == 4 else (m.group(2), m.group(1))
        url = href if href.startswith("http") else "https://www.finance.gov.mv" + href
        found[f"{y}-Q{q}"] = {"url": url, "title": text}
    return found


def save(name, b, url, title, problems):
    b.update({"name": name, "url": url, "title": title, "checks": problems or "every table adds up",
              "read_at": datetime.now(timezone.utc).strftime("%Y-%m-%d")})
    (OUT / f"{name}.json").write_text(json.dumps(b, ensure_ascii=False, indent=0))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1:   # read PDFs from a folder instead of the website
        for f in sorted(Path(sys.argv[1]).glob("*.pdf")):
            try:
                b = parse(f.read_bytes())
            except Exception as e:
                print(f"{f.name}: skipped ({e})")
                continue
            y, q = b["quarter"][:4], {"03": 1, "06": 2, "09": 3, "12": 4}[b["quarter"][5:7]]
            problems = check(b)
            save(f"{y}-Q{q}", b, None, f.name, problems)
            print(f"{f.name}: {y} Q{q}, {len(b['tables'])} tables" + (f"; problems: {problems}" if problems else ""))
        return
    try:
        found = listing()
    except Exception as e:
        print(f"Couldn't read the list of bulletins ({e}). Keeping what we have.")
        return
    if not found:
        print("No bulletins found on the Ministry's page. The website may have changed.")
        return
    print(f"{len(found)} quarterly bulletins listed, {min(found)} to {max(found)}.")
    for name, it in sorted(found.items()):
        path = OUT / f"{name}.json"
        if path.exists() and json.loads(path.read_text()).get("url") == it["url"]:
            continue
        for attempt in range(3):
            try:
                r = requests.get(it["url"], headers=H, timeout=120)
                r.raise_for_status()
                if not r.content.startswith(b"%PDF"):
                    raise RuntimeError("not a PDF")
                b = parse(r.content)
                break
            except Exception as e:
                print(f"  {name}: problem ({e})")
                b = None
                time.sleep(5 * (attempt + 1))
        if not b:
            continue
        problems = check(b)
        save(name, b, it["url"], it["title"], problems)
        print(f"  {name}: read {len(b['tables'])} tables" + (f"; check these: {problems}" if problems else ", every table adds up"))


if __name__ == "__main__":
    main()
