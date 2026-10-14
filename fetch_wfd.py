"""
Keeps the Weekly Fiscal Developments (WFD) dataset up to date, and builds budget.json for the budget page.

Runs every morning in GitHub Actions, straight after fetch_data.py. Each run it:
  1. reads the list of reports on Ministry of Finance website,
  2. downloads only reports it hasn't read yet (on the first run, the whole history from 2018),
  3. reads the tables (using wfd_extract.py) and checks the totals add up,
  4. adds them to the dataset in data/wfd/ and rebuilds budget.json.

A report whose totals can't be read or don't add up is not published. The previous figures stay,
the problem is written to data/wfd/processed.csv, and if it is the newest report the run is marked
as failed so GitHub sends an email.

To run it yourself:
    pip install requests pdfplumber
    python fetch_wfd.py
"""
import csv
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

import wfd_extract as W

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "wfd"
CACHE = HERE / ".wfd_cache"          # downloaded PDFs, not kept in the repo
OUT_JSON = HERE / "budget.json"
NEWEST = HERE / "wfd-latest.json"   # a few lines on the newest report, for the site-wide "new figures" ribbon
DETAIL_DIR = HERE / "budget-detail"
PROCESSED = DATA / "processed.csv"
REVISIONS = DATA / "revisions.json"   # every time the Ministry replaced a report it had already published, and what changed
HEADLINE = DATA / "wfd_headline.csv"
LONG = DATA / "wfd_long.csv"
PROC_COLS = ["as_at", "url", "title", "status", "problems", "checked_at"]


def read_csv(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f) if rows and isinstance(rows[0], list) else csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if isinstance(w, csv.DictWriter):
            w.writeheader()
        else:
            w.writerow(cols)
        w.writerows(rows)


def choose(listing):
    """One report per date: a revised version wins over the original."""
    best = {}
    for r in listing:
        d = r["as_at"]
        if d not in best or (r["revised"] and not best[d]["revised"]):
            best[d] = r
    return best


def download(url, path):
    for attempt in range(4):
        try:
            resp = requests.get(url, headers=W.HEADERS, timeout=120)
            resp.raise_for_status()
            if not resp.content.startswith(b"%PDF"):
                raise RuntimeError("not a PDF")
            path.write_bytes(resp.content)
            return True
        except Exception as e:
            print(f"    problem downloading ({e}), retrying")
            time.sleep(5 * (attempt + 1))
    return False


def num(v):
    if v in (None, ""):
        return None
    try:
        return round(float(v), 1)
    except ValueError:
        return None


HEAD_LABELS = {"revenue_and_grants": "Revenue and grants", "tax_revenue": "Tax revenue", "non_tax_revenue": "Non-tax revenue", "grants": "Grants",
               "total_expenditure": "Total spending", "recurrent_expenditure": "Recurrent spending", "capital_expenditure": "Capital spending",
               "salaries_wages_pensions": "Salaries, wages and pensions", "primary_balance": "Primary balance", "overall_balance": "Overall balance",
               "interest_costs": "Interest and financing costs", "loan_repayment": "Loan repayments", "transfers_to_sdf": "Transfers to Sovereign Development Fund",
               "psip": "Public Sector Investment Programme"}
FIELDS = (("this_year", "so far this year"), ("approved", "approved budget"), ("last_year", "same date last year"))


def compare(old_h, new_h, old_long, new_long):
    """the figures that differ between the version already published and the replacement (in MVR million)"""
    changes = []
    def add(where, label, field, a, b):
        a, b = num(a), num(b)
        if a != b and not (a is not None and b is not None and abs(a - b) < 0.05):
            changes.append({"t": where, "l": label, "f": field, "a": a, "b": b})
    for col, label in HEAD_LABELS.items():
        for suffix, field in (("", "so far this year"), ("_approved", "approved budget"), ("_last_year", "same date last year")):
            add("summary", label, field, old_h.get(col + suffix), new_h.get(col + suffix))
    key = lambda r: (r["table"], r["label"].strip())
    old_rows, new_rows = {key(r): r for r in old_long}, {key(r): r for r in new_long}
    for k in sorted(set(old_rows) | set(new_rows)):
        if k[0] not in ("revenue", "expenditure", "agencies", "psip") or k[0] == "summary":
            continue
        o, n = old_rows.get(k, {}), new_rows.get(k, {})
        for col, field in FIELDS:
            add(k[0], k[1], field, o.get(col), n.get(col))
    big = [c for c in changes if c["t"] == "summary"]
    lines = sorted((c for c in changes if c["t"] != "summary"), key=lambda c: -abs((c["b"] or 0) - (c["a"] or 0)))
    return big + lines[:40], len(lines)


def read_revisions():
    try:
        return json.loads(REVISIONS.read_text(encoding="utf-8"))
    except Exception:
        return []


def build_json(headline, long_rows):
    # "Grants, Contributions and Subsidies" for every report, used by the budget page's spending picture
    gcs = {}
    for row in long_rows:
        if row["table"] == "expenditure" and row["label"].strip().lower().startswith("grants, contributions and subsidies"):
            gcs.setdefault(row["as_at"], [num(row["this_year"]), num(row["approved"]), num(row["last_year"])])
    reports = []
    for h in sorted(headline, key=lambda r: r["as_at"]):
        v = {}
        for col, _, _ in W.HEADLINE:
            trip = [num(h.get(col)), num(h.get(col + "_approved")), num(h.get(col + "_last_year"))]
            if any(x is not None for x in trip):
                v[col] = trip
        if h["as_at"] in gcs:
            v["grants_subsidies"] = gcs[h["as_at"]]
        reports.append({"d": h["as_at"], "w": int(float(h["week"])) if h.get("week") else None, "v": v,
                        "sec": [num(h.get("securities_total")), num(h.get("securities_domestic")), num(h.get("securities_external"))],
                        "sec_d": h.get("securities_as_of") or None})
    latest = reports[-1]["d"] if reports else None
    detail = {}
    for row in long_rows:
        if row["as_at"] != latest or row["table"] not in ("revenue", "expenditure", "agencies", "psip"):
            continue
        detail.setdefault(row["table"], []).append({"label": row["label"], "approved": num(row["approved"]),
                                                    "last": num(row["last_year"]), "now": num(row["this_year"]),
                                                    "memo": row.get("memo") == "1"})
    revisions = {}
    for r in read_revisions():
        revisions.setdefault(r["as_at"], []).append(r)
    data = {"built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": W.PAGE, "latest": latest, "reports": reports, "detail": detail, "revisions": revisions}
    OUT_JSON.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUT_JSON.name}: {len(reports)} reports, latest {latest}.")
    # when the newest report first went on the site, so pages can point readers to it for a couple of days
    if reports:
        log = {r["as_at"]: r for r in read_csv(PROCESSED)}
        newest = {"d": latest, "w": reports[-1]["w"], "added": log.get(latest, {}).get("checked_at") or data["built_at"]}
        NEWEST.write_text(json.dumps(newest), encoding="utf-8")

    # every line of every report, one file per year, so the budget page can show any earlier week line by line
    by_year = {}
    for row in long_rows:
        if row["table"] not in ("revenue", "expenditure", "agencies", "psip"):
            continue
        t = by_year.setdefault(row["as_at"][:4], {}).setdefault(row["as_at"], {}).setdefault(row["table"], [])
        t.append([row["label"], num(row["approved"]), num(row["last_year"]), num(row["this_year"]), 1 if row.get("memo") == "1" else 0])
    DETAIL_DIR.mkdir(exist_ok=True)
    for y, reps in by_year.items():
        (DETAIL_DIR / f"{y}.json").write_text(json.dumps(reps, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(by_year)} yearly files of line-by-line figures to {DETAIL_DIR.name}/.")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    processed = {r["as_at"]: r for r in read_csv(PROCESSED)}
    headline = {r["as_at"]: r for r in read_csv(HEADLINE)}
    long_rows = read_csv(LONG)

    try:
        listing = W.list_reports()
    except Exception as e:
        print(f"Couldn't read Ministry of Finance website ({e}). Keeping the existing data.")
        listing = []
    best = choose(listing)
    todo = [d for d in sorted(best) if processed.get(d, {}).get("url") != best[d]["url"]]
    print(f"{len(best)} reports listed, {len(todo)} new or changed.")

    newest_failed = False
    revisions = read_revisions()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for d in todo:
        rep = best[d]
        old_url = processed.get(d, {}).get("url") if processed.get(d, {}).get("status") == "published" else None
        pdf = CACHE / (d + ".pdf")
        print(f"  {d}: {rep['title']}")
        if not download(rep["url"], pdf):
            processed[d] = {"as_at": d, "url": "", "title": rep["title"], "status": "download failed", "problems": "", "checked_at": now}
            continue
        try:
            meta, rows = W.parse_report(W.read_pdf(pdf))
            h, lrows, problems = W.summarise(d, rep["url"], meta, rows)
        except Exception as e:
            h, lrows, problems = {}, [], [f"couldn't read the PDF: {e}"]
        ok = W.usable(h, problems)
        processed[d] = {"as_at": d, "url": rep["url"], "title": rep["title"], "status": "published" if ok else "not published",
                        "problems": "; ".join(problems), "checked_at": now}
        if ok:
            new_long = [dict(zip(W.LONG_COLS, lr)) for lr in lrows]
            if d in headline and old_url:   # a report already on the site was replaced: record what changed
                changes, n_lines = compare(headline[d], h, [r for r in long_rows if r["as_at"] == d], new_long)
                revisions.append({"as_at": d, "found": datetime.now(timezone(timedelta(hours=5))).date().isoformat(), "title": rep["title"],
                                  "url": rep["url"], "prev_url": old_url, "revised": rep["revised"], "changes": changes, "lines_changed": n_lines})
                print(f"    replaces the version published before: {len(changes)} figures changed" if changes else "    replaces the version published before: no figures changed")
            headline[d] = h
            long_rows = [r for r in long_rows if r["as_at"] != d] + new_long
        else:
            print(f"    not published: {'; '.join(problems)}")
            if d == max(best):
                newest_failed = True
        time.sleep(1)

    long_rows.sort(key=lambda r: (r["as_at"], int(float(r["row"]))))
    write_csv(PROCESSED, PROC_COLS, [processed[d] for d in sorted(processed)])
    REVISIONS.write_text(json.dumps(revisions, ensure_ascii=False, indent=1), encoding="utf-8")
    write_csv(HEADLINE, W.HEAD_COLS, [headline[d] for d in sorted(headline)])
    write_csv(LONG, W.LONG_COLS, long_rows)
    build_json(list(headline.values()), long_rows)
    if newest_failed:
        sys.exit(f"The newest report ({max(best)}) couldn't be read properly, so it hasn't been published. See data/wfd/processed.csv.")


if __name__ == "__main__":
    main()
