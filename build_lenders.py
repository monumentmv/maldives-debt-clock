"""
Builds lenders.json for the home page from the Ministry of Finance lists saved by fetch_lenders.py:
every active external loan and sovereign guarantee, with the lender's country or type and the amount in
US dollars at the exchange rates on the list's "as of" date.

The amounts are what was originally borrowed or guaranteed, as the Ministry lists them, not what is
still owed: many have been partly repaid.

To run it yourself:
    python build_lenders.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "lenders" / "raw.json"
FX = HERE / "data" / "lenders" / "fx.json"
OUT = HERE / "lenders.json"

# lender name as the Ministry writes it -> (short name, country or group, type)
M, B, C, X = "Multilateral institution", "Government or state lender", "Bank or company", "Other"
LENDERS = {
    "International Development Association": ("World Bank (IDA)", "Multilateral institutions", M),
    "International Development Association / Clean Technology Fund": ("World Bank (IDA) / Clean Technology Fund", "Multilateral institutions", M),
    "Asian Development Bank": ("Asian Development Bank", "Multilateral institutions", M),
    "Asian Development Bank / Clean Technology Fund": ("Asian Development Bank / Clean Technology Fund", "Multilateral institutions", M),
    "Asian Infrastructure Investment Bank": ("Asian Infrastructure Investment Bank", "Multilateral institutions", M),
    "Islamic Development Bank": ("Islamic Development Bank", "Multilateral institutions", M),
    "International Islamic Trade Finance Corporation": ("International Islamic Trade Finance Corporation", "Multilateral institutions", M),
    "International Fund for Agricultural Development": ("International Fund for Agricultural Development", "Multilateral institutions", M),
    "European Investment Bank": ("European Investment Bank", "Multilateral institutions", M),
    "Nordic Development Fund": ("Nordic Development Fund", "Multilateral institutions", M),
    "The OPEC Fund for International Development": ("OPEC Fund for International Development", "Multilateral institutions", M),
    "Export Import Bank of China": ("Export-Import Bank of China", "China", B),
    "The Export Import Bank of China": ("Export-Import Bank of China", "China", B),
    "China Development Bank": ("China Development Bank", "China", B),
    "Industrial and Commercial Bank of China": ("Industrial and Commercial Bank of China", "China", C),
    "Dongfang Electric Corporation": ("Dongfang Electric Corporation", "China", C),
    "Browns - China Machinery Engineering Corporation": ("Browns and China Machinery Engineering Corporation", "China", C),
    "The Export Import Bank of India": ("Export-Import Bank of India", "India", B),
    "Reserve Bank of India": ("Reserve Bank of India", "India", B),
    "State Bank of India, Malé": ("State Bank of India (Malé branch)", "India", C),
    "Saudi Fund for Development": ("Saudi Fund for Development", "Saudi Arabia", B),
    "Kuwait Fund for Arab Economic Development": ("Kuwait Fund for Arab Economic Development", "Kuwait", B),
    "Abu Dhabi Fund for Development": ("Abu Dhabi Fund for Development", "United Arab Emirates", B),
    "Japan International Cooperation Agency": ("Japan International Cooperation Agency", "Japan", B),
    "Agence Française de Développement": ("French Development Agency (AFD)", "France", B),
    "Government of Belgium": ("Government of Belgium", "Belgium", B),
    "U.S. Agency for International Development": ("US Agency for International Development", "United States", B),
    "AKA Ausfuhrkedit-Gesellschaft mbH, ABN AMRO Bank N.V. and ING Bank N.V.": ("AKA, ABN AMRO and ING (bank group)", "Germany and the Netherlands", C),
    "OQ Trading Limited": ("OQ Trading", "Oman", C),
    "Habib Bank Limited, Malé": ("Habib Bank (Malé branch)", "Pakistan", C),
    "Bank of Maldives": ("Bank of Maldives", "Maldives", C),
    "Maldives Islamic Bank": ("Maldives Islamic Bank", "Maldives", C),
    "Bond Holders": ("International bond holders", "Bond holders", X),
    "Private Creditor": ("A private lender (name not published)", "Not published", X),
    "CFSIT Inc.": ("CFSIT Inc.", "Not published", C),
}


# where each lender sits on the map: countries at their capital (or where the lender is based), development banks
# and funds at their headquarters. "map" names the country shaded on the map.
PLACES = {
    "China": {"lon": 116.4, "lat": 39.9, "label": "China", "kind": "country", "map": ["China"]},
    "India": {"lon": 77.2, "lat": 28.6, "label": "India", "kind": "country", "map": ["India"]},
    "Saudi Arabia": {"lon": 46.7, "lat": 24.7, "label": "Saudi Arabia", "kind": "country", "map": ["Saudi Arabia"]},
    "United Arab Emirates": {"lon": 54.4, "lat": 24.5, "label": "UAE", "kind": "country", "map": ["United Arab Emirates"]},
    "Kuwait": {"lon": 48.0, "lat": 29.4, "label": "Kuwait", "kind": "country", "map": ["Kuwait"]},
    "Oman": {"lon": 58.4, "lat": 23.6, "label": "Oman", "kind": "country", "map": ["Oman"]},
    "Pakistan": {"lon": 67.0, "lat": 24.9, "label": "Pakistan", "kind": "country", "map": ["Pakistan"]},
    "Japan": {"lon": 139.7, "lat": 35.7, "label": "Japan", "kind": "country", "map": ["Japan"]},
    "France": {"lon": 2.35, "lat": 48.9, "label": "France", "kind": "country", "map": ["France"]},
    "Belgium": {"lon": 4.35, "lat": 50.85, "label": "Belgium", "kind": "country", "map": ["Belgium"]},
    "Germany and the Netherlands": {"lon": 8.7, "lat": 51.5, "label": "Germany, Netherlands", "kind": "country", "map": ["Germany", "Netherlands"]},
    "United States": {"lon": -77.0, "lat": 38.9, "label": "United States", "kind": "country", "map": ["United States of America"]},
    "World Bank (IDA)": {"lon": -77.04, "lat": 38.9, "label": "World Bank", "kind": "institution", "city": "Washington DC"},
    "Asian Development Bank": {"lon": 121.0, "lat": 14.6, "label": "ADB", "kind": "institution", "city": "Manila"},
    "Asian Infrastructure Investment Bank": {"lon": 116.4, "lat": 39.9, "label": "AIIB", "kind": "institution", "city": "Beijing"},
    "Islamic Development Bank": {"lon": 39.2, "lat": 21.5, "label": "IsDB", "kind": "institution", "city": "Jeddah"},
    "International Islamic Trade Finance Corporation": {"lon": 39.2, "lat": 21.5, "label": "ITFC", "kind": "institution", "city": "Jeddah"},
    "International Fund for Agricultural Development": {"lon": 12.5, "lat": 41.9, "label": "IFAD", "kind": "institution", "city": "Rome"},
    "European Investment Bank": {"lon": 6.1, "lat": 49.6, "label": "EIB", "kind": "institution", "city": "Luxembourg"},
    "Nordic Development Fund": {"lon": 24.9, "lat": 60.2, "label": "Nordic Fund", "kind": "institution", "city": "Helsinki"},
    "OPEC Fund for International Development": {"lon": 16.4, "lat": 48.2, "label": "OPEC Fund", "kind": "institution", "city": "Vienna"},
}
INSTITUTION = {  # lender short name -> its place, for the development banks and funds
    "World Bank (IDA)": "World Bank (IDA)", "World Bank (IDA) / Clean Technology Fund": "World Bank (IDA)",
    "Asian Development Bank": "Asian Development Bank", "Asian Development Bank / Clean Technology Fund": "Asian Development Bank",
    "Asian Infrastructure Investment Bank": "Asian Infrastructure Investment Bank", "Islamic Development Bank": "Islamic Development Bank",
    "International Islamic Trade Finance Corporation": "International Islamic Trade Finance Corporation",
    "International Fund for Agricultural Development": "International Fund for Agricultural Development",
    "European Investment Bank": "European Investment Bank", "Nordic Development Fund": "Nordic Development Fund",
    "OPEC Fund for International Development": "OPEC Fund for International Development",
}


def main():
    raw, fx = json.load(open(RAW)), json.load(open(FX))
    versions = sorted({a for k in raw for a in raw[k]})
    unknown = set()
    out = {"versions": versions, "fx": fx, "places": PLACES, "lists": {}}
    for kind in ("loans", "guarantees"):
        out["lists"][kind] = {}
        for asof, items in sorted(raw[kind].items()):
            rate = fx.get(asof, {}).get("per_usd", {})
            rows = []
            for i in items:
                name, country, typ = LENDERS.get(i["creditor"], (i["creditor"], "Not published", X))
                if i["creditor"] not in LENDERS:
                    unknown.add(i["creditor"])
                r = rate.get(i["currency"])
                place = INSTITUTION.get(name) or (country if country in PLACES else None)
                rows.append({"g": i["group"], "d": i["date"], "l": name, "c": country, "t": typ, "pl": place, "p": i["purpose"], "b": i["beneficiary"],
                             "cur": i["currency"], "a": i["amount"], "usd": round(i["amount"] / r) if r and i["amount"] is not None else None, "s": i["status"]})
            out["lists"][kind][asof] = rows
    json.dump(out, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    for kind, v in out["lists"].items():
        a = versions[-1] if versions[-1] in v else max(v)
        tot = sum(r["usd"] or 0 for r in v[a])
        print(f"{kind}, as of {a}: {len(v[a])} items, US$ {tot / 1e9:.2f} bn originally borrowed or guaranteed")
    if unknown:
        print("Lenders not yet given a country (shown as 'Not published'):\n  " + "\n  ".join(sorted(unknown)))


if __name__ == "__main__":
    main()
