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
            "points": points,
        }

    missing = [k for k in SERIES.values() if k not in series or not series[k]["points"]]
    if "total" in missing:
        sys.exit(f"Core series missing from API response: {missing}")
    if missing:
        print(f"Warning: no data for {missing}")

    with open("data.json", "w") as f:
        json.dump(
            {"fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "series": series},
            f,
            indent=1,
        )
    t = series["total"]["points"][-1]
    print(f"OK. Latest total debt: MVR {t['value']:,.0f} at {t['date']}")


if __name__ == "__main__":
    main()
