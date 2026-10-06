"""
Builds protection.json for the protection page: spending by the police and the agencies that
protect families, children, human rights and people affected by drugs, set against government
interest costs, with reported case counts from the Maldives Police Service.

Runs every morning in GitHub Actions, after fetch_wfd.py and fetch_police.py. Reads:
  data/wfd/wfd_long.csv           every row of every Weekly Fiscal Developments table
  data/police/crime_monthly.csv   case counts by year, month and category (may not exist yet)

To run it yourself:
    python build_protection.py
"""
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LONG = HERE / "data" / "wfd" / "wfd_long.csv"
POLICE = HERE / "data" / "police" / "crime_monthly.csv"
OUT = HERE / "protection.json"

# key, name on the site, pattern for the line in the "budget by office" table, group, related case categories
AGENCIES = [
    ("police", "Maldives Police Service", r"^maldives police serv", "police", None),
    ("fpa", "Family Protection Authority", r"^family protection", "protection", (["Domestic violence"], "domestic violence")),
    ("coo", "Children\u2019s Ombudsperson\u2019s Office", r"^children.s ombudsperson", "protection", (["Sexual Offences"], "sexual offence")),
    ("hrc", "Human Rights Commission", r"^human rights commission", "protection", None),
    ("nda", "National Drug Agency", r"^national drug agency", "protection", (["Drugs"], "drug")),
    ("corr", "Maldives Correctional Services", r"^maldives correctional", "justice", None),
    ("pg", "Prosecutor General\u2019s Office", r"^prosecutor general", "justice", None),
    ("acc", "Anti-Corruption Commission", r"^anti.corruption", "justice", None),
]


def num(v):
    try:
        return round(float(v), 1) if v not in (None, "") else None
    except ValueError:
        return None


def clean(label):
    return re.sub(r"^\d+\s+", "", label.strip())


def main():
    rows = list(csv.DictReader(open(LONG, encoding="utf-8")))
    by_date = {}
    for r in rows:
        by_date.setdefault(r["as_at"], []).append(r)

    def pick(d):
        out = {"interest": None, "agencies": {}}
        for r in by_date[d]:
            lab = clean(r["label"])
            if r["table"] == "summary" and re.search(r"financing and interest costs", lab, re.I):
                out["interest"] = [num(r["approved"]), num(r["last_year"]), num(r["this_year"])]
            if r["table"] == "agencies":
                for key, _, pat, _, _ in AGENCIES:
                    if key not in out["agencies"] and re.search(pat, lab, re.I):
                        out["agencies"][key] = [num(r["approved"]), num(r["last_year"]), num(r["this_year"])]
        return out

    dates = sorted(by_date)
    latest = dates[-1]
    L = pick(latest)
    d0 = date.fromisoformat(latest)
    days = (d0 - date(d0.year, 1, 1)).days + 1

    # last report of each year: the year-by-year history
    last_of_year = {}
    for d in dates:
        last_of_year[d[:4]] = d
    history = []
    for y, d in sorted(last_of_year.items()):
        p = pick(d)
        if p["interest"] is None:
            continue
        dd = date.fromisoformat(d)
        history.append({"year": int(y), "d": d, "full": dd.month == 12 and dd.day >= 24,
                        "interest": p["interest"][2], "agencies": {k: v[2] for k, v in p["agencies"].items()}})

    # police case counts
    crime = None
    if POLICE.exists():
        pr = list(csv.DictReader(open(POLICE, encoding="utf-8")))
        if pr:
            months, years = {}, {}
            for r in pr:
                y, m, c, n = int(r["year"]), int(r["month"]), r["category"], int(r["cases"])
                (years if m == 0 else months).setdefault(y, {}).setdefault(m if m else 0, {})[c] = n
            monthly = {str(y): {str(m): cats for m, cats in sorted(v.items())} for y, v in sorted(months.items())}
            yearly = {str(y): v[0] for y, v in sorted(years.items())}
            retrieved = max(r["retrieved"] for r in pr)
            # cases in the same months as the latest weekly report, 1 January to the report's month
            same = {}
            for m in range(1, d0.month + 1):
                for c, n in months.get(d0.year, {}).get(m, {}).items():
                    same[c] = same.get(c, 0) + n
            crime = {"retrieved": retrieved, "monthly": monthly, "yearly": yearly,
                     "aligned": {"year": d0.year, "to_month": d0.month, "cases": same} if same else None}

    data = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "latest": {"d": latest, "days": days, "interest": L["interest"],
                   "agencies": {k: v for k, v in L["agencies"].items()}},
        "agencies": [{"key": k, "name": n, "group": g, "cases": c[0] if c else [], "case_noun": c[1] if c else None} for k, n, _, g, c in AGENCIES],
        "history": history,
        "crime": crime,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    missing = [k for k, *_ in AGENCIES if k not in L["agencies"]]
    print(f"Wrote {OUT.name}: report of {latest}, {len(history)} years" + (f", not found this week: {', '.join(missing)}" if missing else "")
          + (", with police case counts." if crime else ", no police case counts yet."))


if __name__ == "__main__":
    main()
