"""
Builds priorities.json for the priorities page. It sets what the government pays in interest
against what it spends on policing, justice, protection and rights, and on other big services,
with cases reported to the Maldives Police Service.

Runs every morning in GitHub Actions, after fetch_wfd.py and fetch_police.py. Reads:
  data/wfd/wfd_long.csv           every row of every Weekly Fiscal Developments table
  data/police/crime_monthly.csv   case counts by year, month and category (may not exist yet)

Every weekly report from 2019 is included, so visitors can look at any earlier week.

To run it yourself:
    python build_priorities.py
"""
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LONG = HERE / "data" / "wfd" / "wfd_long.csv"
POLICE = HERE / "data" / "police" / "crime_monthly.csv"
OUT = HERE / "priorities.json"

# key, name on the site, pattern for lines in the "budget by office" table, group, icon, related case categories and wording, add up every match
OFFICES = [
    ("police", "Maldives Police Service", r"^maldives police serv", "safety", "police", None, False),
    ("corr", "Maldives Correctional Services", r"^maldives correctional", "safety", "prison", None, False),
    ("pg", "Prosecutor General\u2019s Office", r"^prosecutor general", "safety", "gavel", None, False),
    ("acc", "Anti-Corruption Commission", r"^anti.corruption", "safety", "search", None, False),
    ("fpa", "Family Protection Authority", r"^family protection", "rights", "family", (["Domestic violence"], "domestic violence"), False),
    ("coo", "Children\u2019s Ombudsperson\u2019s Office", r"^children.s ombudsperson", "rights", "child", (["Sexual Offences"], "sexual offence"), False),
    ("hrc", "Human Rights Commission", r"^human rights commission", "rights", "scales", None, False),
    ("nda", "National Drug Agency", r"^national drug agency", "rights", "pill", (["Drugs"], "drug"), False),
    ("edu", "Ministry of Education", r"^ministry of education", "context", "school", None, False),
    ("health", "Health ministry and public hospitals", r"^ministry of health|hospital", "context", "hospital", None, True),
    ("mndf", "Maldives National Defence Force", r"national defen[cs]e force", "context", "shield", None, False),
]
FIRST_YEAR = 2019


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
        if int(r["as_at"][:4]) >= FIRST_YEAR:
            by_date.setdefault(r["as_at"], []).append(r)

    def pick(d):
        interest, found = None, {}
        for r in by_date[d]:
            lab = clean(r["label"])
            if r["table"] == "summary" and re.search(r"financing and interest costs", lab, re.I):
                interest = [num(r["approved"]), num(r["last_year"]), num(r["this_year"])]
            if r["table"] != "agencies":
                continue
            for key, _, pat, _, _, _, add_up in OFFICES:
                if re.search(pat, lab, re.I):
                    v = [num(r["approved"]), num(r["last_year"]), num(r["this_year"])]
                    if key in found and add_up:
                        found[key] = [round((a or 0) + (b or 0), 1) if (a is not None or b is not None) else None for a, b in zip(found[key], v)]
                    elif key not in found:
                        found[key] = v
        return interest, found

    reports = []
    for d in sorted(by_date):
        interest, found = pick(d)
        if interest is None or interest[2] is None or not found:
            continue
        dd = date.fromisoformat(d)
        reports.append({"d": d, "days": (dd - date(dd.year, 1, 1)).days + 1, "i": interest, "a": found})

    # police case counts
    crime = None
    if POLICE.exists():
        pr = list(csv.DictReader(open(POLICE, encoding="utf-8")))
        if pr:
            months, years = {}, {}
            for r in pr:
                y, m, c, n = int(r["year"]), int(r["month"]), r["category"], int(r["cases"])
                if m == 0:
                    years.setdefault(y, {})[c] = n
                else:
                    months.setdefault(y, {}).setdefault(m, {})[c] = n
            crime = {"retrieved": max(r["retrieved"] for r in pr),
                     "monthly": {str(y): {str(m): c for m, c in sorted(v.items())} for y, v in sorted(months.items())},
                     "yearly": {str(y): v for y, v in sorted(years.items())}}

    # longer history from the Statistical Yearbook, kept in the repo, so it never has to be fetched again
    BOOK_T, BOOK_M = HERE / "data" / "police" / "yearbook_by_type.csv", HERE / "data" / "police" / "yearbook_by_month.csv"
    if BOOK_T.exists():
        yearly, others, monthly = {}, {}, {}
        for r in csv.DictReader(open(BOOK_T, encoding="utf-8")):
            if r["category"] == "Others":
                others[r["year"]] = int(r["cases"])
            else:
                yearly.setdefault(r["year"], {})[r["category"]] = int(r["cases"])
        if BOOK_M.exists():
            for r in csv.DictReader(open(BOOK_M, encoding="utf-8")):
                monthly.setdefault(r["year"], {})[r["month"]] = int(r["cases"])
        crime = crime or {"retrieved": None, "monthly": {}, "yearly": {}}
        # the police website comes first: the yearbook only fills years the website hasn't given yet
        site_years = set(crime["yearly"]) | set(crime["monthly"])
        yearly = {y: v for y, v in yearly.items() if y not in site_years}
        others = {y: v for y, v in others.items() if y not in site_years}
        monthly = {y: v for y, v in monthly.items() if y not in site_years}
        if yearly or monthly:
            crime["book"] = {"yearly": yearly, "others": others, "monthly": monthly}

    data = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "latest": {"d": reports[-1]["d"], "days": reports[-1]["days"], "interest": reports[-1]["i"]},
        "offices": [{"key": k, "name": n, "group": g, "icon": ic, "cases": c[0] if c else [], "case_noun": c[1] if c else None}
                    for k, n, _, g, ic, c, _ in OFFICES],
        "reports": reports,
        "crime": crime,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    L = reports[-1]
    missing = [k for k, *_ in OFFICES if k not in L["a"]]
    print(f"Wrote {OUT.name}: {len(reports)} weekly reports, latest {L['d']}" + (f", not found in the latest: {', '.join(missing)}" if missing else "") +
          (", with police case counts." if crime else ", no police case counts yet."))


if __name__ == "__main__":
    main()
