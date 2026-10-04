"""
Pulls Maldives public debt series from the MMA Statistics Database
and writes data.json for the debt clock page.

Runs in GitHub Actions. The API token comes from the MMA_TOKEN secret,
so it never appears in the public repo or the website.
"""
import json
import os
import sys
from datetime import datetime, timezone

import requests
import urllib3

urllib3.disable_warnings()  # MMA's own sample code uses verify=False

TOKEN = os.environ.get("MMA_TOKEN")
if not TOKEN:
    sys.exit("MMA_TOKEN is not set. Add it as a repository secret.")

SERIES = {
    4514: "total",            # Public & publicly guaranteed debt, MVR
    4515: "domestic",
    4516: "domestic_cg",
    4517: "domestic_guaranteed",
    4518: "external",
    4519: "external_cg",
    4520: "external_guaranteed",
    4522: "debt_to_gdp",      # percent
    79:   "population",
    4039: "usd_rate",         # MVR per USD
    5226: "ext_interest_q",   # quarterly external interest paid, USD
    4523: "domestic_to_gdp",  # ratio
    4526: "external_to_gdp",  # ratio
    38:   "gdp",              # nominal GDP, MVR, annual
    # monthly government finances, MVR
    1999: "revenue",          # total revenue and grants
    2000: "tax_revenue",
    2034: "expenditure",      # recurrent + capital
    2035: "recurrent_exp",
    2057: "capital_exp",
    2036: "salaries_pensions",
    2049: "interest_costs",   # financing and interest costs
    2050: "subsidies",        # grants, contributions and subsidies
    # prices, for inflation adjustment
    280:  "cpi",              # national consumer price index, monthly
    # fuel imports, US dollars, monthly (Maldives Customs Service)
    3486: "imports_goods",    # all goods imports
    3503: "fuel_imports",     # petroleum products
    3504: "fuel_petrol",
    3505: "fuel_diesel",      # diesel (marine gas oil)
    3507: "fuel_other",
    3787: "crude_price",      # World Bank average of Brent, Dubai and WTI, US$ per barrel
}

# Extra series for comparing presidencies (first three years of each term).
# Saved separately in compare.json so the debt clock pages stay light.
COMPARE = {
    # annual government finance statistics, MVR
    2080: "gfs_revenue_grants",
    2081: "gfs_revenue",
    2082: "gfs_current_revenue",
    2083: "gfs_tax_revenue",       # name checked against the API response
    2138: "gfs_grants",
    2141: "gfs_expenditure_net_lending",
    2142: "gfs_expenditure",
    2143: "gfs_current_expenditure",
    2155: "gfs_interest",
    2156: "gfs_subsidies_transfers",
    2159: "gfs_capital_expenditure",
    2167: "gfs_overall_balance",
    2168: "gfs_primary_balance",
    2171: "gfs_financing",
    2176: "gfs_balance_pct_gdp",
    # economy
    72:   "real_gdp_growth",
    38:   "gdp_mvr",
    76:   "gdp_usd",
    104:  "tourist_arrivals",          # monthly
    3382: "reserves_usd",              # official reserve assets, monthly
    3450: "current_account_pct_gdp",
    2299: "broad_money",
    # debt before 2015
    4505: "external_debt_total_usd",   # quarterly
    4020: "external_debt_cg_usd",      # quarterly
    2185: "claims_on_government",      # monthly, domestic lending to government
}

URL = "https://database.mma.gov.mv/api/series"


def fetch(ids):
    out, page = [], 1
    while True:
        r = requests.get(
            URL,
            params={"ids": ",".join(map(str, ids)), "page": page},
            headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"},
            verify=False,
            timeout=60,
        )
        r.raise_for_status()
        body = r.json()
        out.extend(body.get("data", []))
        meta = body.get("meta", {})
        if meta.get("current_page", 1) >= meta.get("last_page", 1):
            return out
        page += 1


def pack(raw, mapping):
    out = {}
    for s in raw:
        key = mapping.get(s["id"])
        if not key:
            continue
        points = sorted(
            [{"date": p["date"], "value": p["amount"]} for p in s.get("data", []) if p.get("amount") is not None],
            key=lambda p: p["date"],
        )
        out[key] = {"id": s["id"], "name": s.get("name"), "unit": s.get("unit"),
                    "frequency": s.get("frequency"), "points": points}
    return out


def write_compare():
    """Fetch the comparison series. Failures here never stop the debt clock update."""
    try:
        new = pack(fetch(list(COMPARE)), COMPARE)
    except Exception as e:  # noqa: BLE001
        print(f"Warning: comparison series not updated ({e})")
        return
    old = {}
    if os.path.exists("compare.json"):
        try:
            with open("compare.json") as f:
                old = json.load(f).get("series", {})
        except (OSError, ValueError):
            old = {}
    carried = [k for k in COMPARE.values() if (k not in new or not new[k]["points"]) and old.get(k, {}).get("points")]
    for k in carried:
        new[k] = old[k]
    with open("compare.json", "w") as f:
        json.dump({"fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "carried_over": carried, "series": new}, f, indent=1)
    cover = {k: (v["points"][0]["date"], v["points"][-1]["date"]) for k, v in new.items() if v["points"]}
    print("compare.json coverage:")
    for k in sorted(cover, key=lambda k: cover[k][0]):
        print(f"  {k:30} {cover[k][0]} to {cover[k][1]}")


def main():
    raw = fetch(list(SERIES))
    series = {}
    for s in raw:
        key = SERIES.get(s["id"])
        if not key:
            continue
        points = sorted(
            [{"date": p["date"], "value": p["amount"]} for p in s.get("data", []) if p.get("amount") is not None],
            key=lambda p: p["date"],
        )
        series[key] = {
            "id": s["id"],
            "name": s.get("name"),
            "unit": s.get("unit"),
            "frequency": s.get("frequency"),
            "last_updated_at": s.get("last_updated_at"),
            "notes": s.get("description") or s.get("definition"),
            "points": points,
        }

    # If the API leaves a series out (or returns it empty), keep the values from the
    # previous run rather than losing that part of the site.
    previous = {}
    if os.path.exists("data.json"):
        try:
            with open("data.json") as f:
                previous = json.load(f).get("series", {})
        except (OSError, ValueError):
            previous = {}
    carried = []
    for key in SERIES.values():
        if (key not in series or not series[key]["points"]) and previous.get(key, {}).get("points"):
            series[key] = previous[key]
            carried.append(key)
    missing = [k for k in SERIES.values() if k not in series or not series[k]["points"]]
    if "total" in missing:
        sys.exit(f"Core series missing and no previous copy: {missing}")
    if carried:
        print(f"Warning: kept previous values for {carried}")
    if missing:
        print(f"Warning: no data at all for {missing}")

    with open("data.json", "w") as f:
        json.dump(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "carried_over": carried,
                "series": series,
            },
            f,
            indent=1,
        )
    t = series["total"]["points"][-1]
    print(f"OK. Latest total debt: MVR {t['value']:,.0f} at {t['date']}")
    write_compare()


if __name__ == "__main__":
    main()
