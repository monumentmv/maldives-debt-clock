"""
Builds lenders.json for the home page from Ministry of Finance lists saved by fetch_lenders.py:
every active external loan and sovereign guarantee, with the lender's country or type and the amount in
US dollars at the exchange rates on the list's "as of" date.

The amounts in those lists are what was originally borrowed or guaranteed, not what is still owed: many
have been partly repaid. What is still owed to each lender, quarter by quarter, comes from the Ministry's
Quarterly Debt Bulletins, read by fetch_bulletin.py into data/bulletin/.

To run it yourself:
    python build_lenders.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "lenders" / "raw.json"
FX = HERE / "data" / "lenders" / "fx.json"
BULLETINS = HERE / "data" / "bulletin"
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
    "Hungary": {"lon": 19.04, "lat": 47.5, "label": "Hungary", "kind": "country", "map": ["Hungary"]},
    "Denmark": {"lon": 12.57, "lat": 55.68, "label": "Denmark", "kind": "country", "map": ["Denmark"]},
    "Switzerland": {"lon": 8.54, "lat": 47.37, "label": "Switzerland", "kind": "country", "map": ["Switzerland"]},
    "Sri Lanka": {"lon": 79.86, "lat": 6.93, "label": "Sri Lanka", "kind": "country", "map": ["Sri Lanka"]},
    "United States": {"lon": -77.0, "lat": 38.9, "label": "United States", "kind": "country", "map": ["United States of America"]},
    "World Bank (IDA)": {"lon": -77.04, "lat": 38.9, "label": "World Bank", "kind": "institution", "city": "Washington DC"},
    "Asian Development Bank": {"lon": 121.0, "lat": 14.6, "label": "ADB", "kind": "institution", "city": "Manila"},
    "Asian Infrastructure Investment Bank": {"lon": 116.4, "lat": 39.9, "label": "AIIB", "kind": "institution", "city": "Beijing"},
    "Islamic Development Bank": {"lon": 39.2, "lat": 21.5, "label": "IsDB", "kind": "institution", "city": "Jeddah"},
    "International Islamic Trade Finance Corporation": {"lon": 39.2, "lat": 21.5, "label": "ITFC", "kind": "institution", "city": "Jeddah"},
    "Islamic Corporation for the Development of the Private Sector": {"lon": 39.2, "lat": 21.5, "label": "ICD", "kind": "institution", "city": "Jeddah"},
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
    "Islamic Corporation for the Development of the Private Sector": "Islamic Corporation for the Development of the Private Sector",
}

# lender names in the Debt Bulletins (written a little differently from bulletin to bulletin) -> (short name, country or group, type).
# Matched on the start of the name, lower case, letters only.
BULLETIN_LENDERS = [
    ("abnamro", "AKA, ABN AMRO and ING (bank group)", "Germany and the Netherlands", C),
    ("ingbank", "AKA, ABN AMRO and ING (bank group)", "Germany and the Netherlands", C),
    ("rabobank", "Rabobank", "Germany and the Netherlands", C),
    ("abudhabifund", "Abu Dhabi Fund for Development", "United Arab Emirates", B),
    ("agencefrancaise", "French Development Agency (AFD)", "France", B),
    ("asiandevelopmentbank", "Asian Development Bank", "Multilateral institutions", M),
    ("asianinfrastructure", "Asian Infrastructure Investment Bank", "Multilateral institutions", M),
    ("bondholders", "International bond holders", "Bond holders", X),
    ("cfsit", "CFSIT Inc.", "Not published", C),
    ("europeaninvestmentbank", "European Investment Bank", "Multilateral institutions", M),
    ("exportimportbankofindia", "Export-Import Bank of India", "India", B),
    ("exportimportbankofchina", "Export-Import Bank of China", "China", B),
    ("governmentofbelgium", "Government of Belgium", "Belgium", B),
    ("governmentofindia", "Government of India", "India", B),
    ("hungarianexportimport", "Hungarian Export-Import Bank", "Hungary", B),
    ("internationaldevelopmentassociation", "World Bank (IDA)", "Multilateral institutions", M),
    ("intrfundforagricultural", "International Fund for Agricultural Development", "Multilateral institutions", M),
    ("internationalfundforagricultural", "International Fund for Agricultural Development", "Multilateral institutions", M),
    ("islamicdevelopmentbank", "Islamic Development Bank", "Multilateral institutions", M),
    ("internationalislamictrade", "International Islamic Trade Finance Corporation", "Multilateral institutions", M),
    ("islamiccorp", "Islamic Corporation for the Development of the Private Sector", "Multilateral institutions", M),
    ("japaninternational", "Japan International Cooperation Agency", "Japan", B),
    ("kuwaitfund", "Kuwait Fund for Arab Economic Development", "Kuwait", B),
    ("nordeabank", "Nordea Bank", "Denmark", C),
    ("nordicdevelopmentfund", "Nordic Development Fund", "Multilateral institutions", M),
    ("saudifund", "Saudi Fund for Development", "Saudi Arabia", B),
    ("opecfund", "OPEC Fund for International Development", "Multilateral institutions", M),
    ("usagency", "US Agency for International Development", "United States", B),
    ("bankofceylon", "Bank of Ceylon", "Sri Lanka", C),
    ("seylanbank", "Seylan Bank", "Sri Lanka", C),
    ("bankofchina", "Bank of China (London branch)", "China", C),
    ("browns", "Browns and China Machinery Engineering Corporation", "China", C),
    ("chinadevelopmentbank", "China Development Bank", "China", B),
    ("creditsuisse", "Credit Suisse (Singapore branch)", "Switzerland", C),
    ("dongfang", "Dongfang Electric Corporation", "China", C),
    ("industrialandcommercialbank", "Industrial and Commercial Bank of China", "China", C),
    ("reservebankofindia", "Reserve Bank of India", "India", B),
    ("others", "Others, not named in the bulletin", "Not published", X),
    # banks in Maldives (guaranteed debt owed at home)
    ("bankofmaldives", "Bank of Maldives", "Maldives", C),
    ("maldivesislamicbank", "Maldives Islamic Bank", "Maldives", C),
    ("habibbank", "Habib Bank (Malé branch)", "Pakistan", C),
    ("statebankofindia", "State Bank of India (Malé branch)", "India", C),
    ("hongkongandshanghai", "HSBC (Malé branch)", "United Kingdom", C),
]


def bulletin_name(n):
    """(short name, country or group, type) for a lender as a Debt Bulletin writes it."""
    key = re.sub(r"[^a-z]", "", re.sub(r"(?<=[A-Za-z.])\d+$", "", n).lower())
    key = key[3:] if key.startswith("the") else key
    for start, short, country, typ in BULLETIN_LENDERS:
        if key.startswith(start):
            return short, country, typ
    return None


def tidy(n):
    """A beneficiary's name, without footnote numbers and with spelling slips fixed."""
    n = re.sub(r"(?<=[A-Za-z.])\d+$", "", n).strip()
    return {"Fenaka Corperation Limited": "Fenaka Corporation Limited", "Bank of Maldive PLC": "Bank of Maldives PLC"}.get(n, n)


def merged(bulletins, table, name=lambda n: n):
    """{row: {quarter: value}} and {quarter: total} for one table across every bulletin. For each quarter the
    newest bulletin whose rows add up to its total is used (bulletins revise earlier quarters); if none adds up,
    the newest is used, with rows it leaves out taken from older bulletins, and anything still missing shown
    as not itemised."""
    rows, totals, unknown = {}, {}, set()
    quarters = sorted({q for b in bulletins for r in b["tables"].get(table, {}).values() for q in r})
    for q in quarters:
        cands = []
        for b in sorted(bulletins, key=lambda b: b["quarter"], reverse=True):
            t = b["tables"].get(table, {})
            if not any(q in r for r in t.values()):
                continue
            tot = next((r.get(q) for n, r in t.items() if n.upper() == "TOTAL"), None)
            vals = {}
            for n, r in t.items():
                if n.upper() == "TOTAL" or q not in r:
                    continue
                k = name(n)
                if k is None:
                    unknown.add(n)
                    k = n
                vals[k] = vals.get(k, 0) + r[q]
            cands.append((tot, vals))
        if not cands:
            continue
        ok = [c for c in cands if c[0] is None or abs(sum(c[1].values()) - c[0]) <= max(1.0, abs(c[0]) * .002)]
        if len(ok) >= 3:   # a bulletin whose figures for this quarter disagree with all the others is a misprint: skip it
            med = lambda k: sorted(c[1].get(k, 0) for c in ok)[len(ok) // 2]
            big = [k for k in {k for c in ok for k in c[1]} if med(k) > .02 * max(1, sum(med(x) for x in {x for c in ok for x in c[1]}))]
            off = lambda c: max((abs(c[1].get(k, 0) - med(k)) / med(k) for k in big), default=0)
            agree = [c for c in ok if off(c) <= .3]
            if agree:
                ok = agree
        tot, vals = ok[0] if ok else cands[0]
        if not ok:
            vals = dict(vals)
            for _, other in cands[1:]:
                for k, v in other.items():
                    if k not in vals and abs(sum(vals.values()) + v - tot) < abs(sum(vals.values()) - tot):
                        vals[k] = v
            gap = tot - sum(vals.values())
            if gap > 1:
                vals["Not itemised in the bulletin"] = gap
        totals[q] = tot if tot is not None else sum(vals.values())
        for k, v in vals.items():
            rows.setdefault(k, {})[q] = round(v, 1)
    return rows, totals, unknown


def bulletin_data():
    files = sorted(BULLETINS.glob("*.json")) if BULLETINS.exists() else []
    bulletins = [json.load(open(f)) for f in files]
    if not bulletins:
        return None
    unknown = set()
    who = {}
    def lender(n):
        hit = bulletin_name(n)
        if not hit:
            return None
        short, country, typ = hit
        who[short] = {"c": country, "t": typ, "pl": INSTITUTION.get(short) or (country if country in PLACES else None)}
        return short
    loans, lt, u1 = merged(bulletins, "gov_ext", lender)
    guar, gt, u2 = merged(bulletins, "sg_ext", lender)
    def home_lender(n):   # bonds in this table were bought by banks in Maldives
        if n.lower().startswith("bondholder"):
            who["Bondholders (banks in Maldives)"] = {"c": "Maldives", "t": C, "pl": None}
            return "Bondholders (banks in Maldives)"
        return lender(n)
    home, ht, u3 = merged(bulletins, "sg_dom", home_lender)   # guaranteed debt owed to banks in Maldives
    unknown |= u1 | u2 | u3
    for k in list(loans) + list(guar) + list(home):
        who.setdefault(k, {"c": "Not published", "t": X, "pl": None})
    # exchange rate the bulletin applied each quarter (MVR per US dollar)
    rate = {}
    for b in sorted(bulletins, key=lambda b: b["quarter"]):
        for n, r in b["tables"].get("ppg", {}).items():
            if n.lower().endswith("applied exchange rate"):
                rate.update({q: v for q, v in r.items() if v})
    # repayments and interest each quarter, government and guaranteed debt
    svc = {}
    for b in sorted(bulletins, key=lambda b: b["quarter"]):
        for n, r in b["tables"].get("service", {}).items():
            n = n.upper().replace("SG DEBT", "GUARANTEED DEBT")
            part = "p" if "PRINCIPAL" in n else "i" if "INTEREST" in n else None
            who_ = "g" if n.startswith("TOTAL DEBT SERVICE COST OF BCG DEBT") else "s" if n.startswith("TOTAL DEBT SERVICE COST OF GUARANTEED DEBT") else None
            if part and who_:
                for q, v in r.items():
                    svc.setdefault(q, {})[who_ + part] = v
    latest = max(bulletins, key=lambda b: b["quarter"])
    lq = latest["quarter"]
    # owed at home: who holds the government's domestic debt, in what form and currency, every quarter
    home_debt = {}
    HOLDER = [("central", "Maldives Monetary Authority"), ("commercial", "Banks"), ("other financial", "Pension fund and other financial firms"),
              ("public", "State companies"), ("private", "Individuals and private companies"),
              ("bond", "Bonds"), ("loan", "Loans"), ("t-bill", "Treasury bills"), ("t bill", "Treasury bills")]
    plain = lambda n: next((v for k, v in HOLDER if tidy(n).lower().startswith(k)), tidy(n))
    for t in ("gov_dom_cat", "gov_dom_type", "gov_dom_cur"):
        rows, tots, _ = merged(bulletins, t, plain)
        home_debt[t.replace("gov_dom_", "")] = rows
        home_debt.setdefault("total", tots)
    # money agreed but not yet paid out, by lender, every quarter
    cub, _, _ = merged(bulletins, "cub", lambda n: (bulletin_name(n) or (tidy(n),))[0])
    # loans passed on to state companies: each bulletin gives only its own quarter
    sub = {}
    for b in bulletins:
        for n, r in b["tables"].get("subsidiary", {}).items():
            if n.upper() != "TOTAL" and r.get(b["quarter"]):
                sub.setdefault(tidy(n), {})[b["quarter"]] = r[b["quarter"]]
    # who borrowed with a government guarantee, abroad and at home, every quarter
    ben = {}
    for t, part in (("sg_ext_ben", "ext"), ("sg_dom_ben", "dom")):
        rows, _, _ = merged(bulletins, t, tidy)
        for n, v in rows.items():
            for q, x in v.items():
                if x:
                    ben.setdefault(n, {}).setdefault(q, {})[part] = x
    if unknown:
        print("Lenders in the Debt Bulletins not yet given a country:\n  " + "\n  ".join(sorted(unknown)))
    return {
        "latest": lq, "quarters": sorted(set(lt) | set(gt)), "rate": rate,
        "loans": loans, "guarantees": guar, "guarantees_home": home, "total": {"loans": lt, "guarantees": gt, "guarantees_home": ht}, "who": who,
        "service": dict(sorted(svc.items())), "home": home_debt, "cub": cub, "subsidiary": sub, "guaranteed_for": ben,
        "sources": [{"q": b["quarter"], "url": b.get("url"), "title": b.get("title")} for b in sorted(bulletins, key=lambda b: b["quarter"])],
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
    owed = bulletin_data()
    if owed:
        out["owed"] = owed
        q = owed["latest"]
        print(f"Debt Bulletins: {len(owed['sources'])}, {owed['quarters'][0]} to {q}. Still owed at {q}: "
              f"loans MVR {owed['total']['loans'][q]:,.1f} m, guarantees MVR {owed['total']['guarantees'][q]:,.1f} m")
    json.dump(out, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    for kind, v in out["lists"].items():
        a = versions[-1] if versions[-1] in v else max(v)
        tot = sum(r["usd"] or 0 for r in v[a])
        print(f"{kind}, as of {a}: {len(v[a])} items, US$ {tot / 1e9:.2f} bn originally borrowed or guaranteed")
    if unknown:
        print("Lenders not yet given a country (shown as 'Not published'):\n  " + "\n  ".join(sorted(unknown)))


if __name__ == "__main__":
    main()
