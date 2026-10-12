"""
Ministry of Finance lists of active external loans and active sovereign guarantees.

Every new version of each file is kept in inputs/mof/, named by its "as of" date, so the history builds up
over time (the Ministry replaces the files on its website). Every version is read into
data/lenders/raw.json, with the exchange rates on each version's "as of" date in data/lenders/fx.json.
build_lenders.py then turns that into lenders.json for the home page.

Runs every morning in GitHub Actions. To run it yourself:
    pip install requests openpyxl
    python fetch_lenders.py
"""
import io
import json
import re
from datetime import date, datetime
from pathlib import Path

import openpyxl
import requests

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs" / "mof"
OUT = HERE / "data" / "lenders"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
# the files' current addresses on finance.gov.mv (the Ministry replaces the file behind each address)
FILES = {
    "guarantees": "https://www.finance.gov.mv/public/attachments/TNxIzceEndB8ZaPZbzjn9aMXG5wY4HFgJG473Rwy.xlsx",
    "loans": "https://www.finance.gov.mv/public/attachments/uhclBk3Vdbveshqh4b9u5jsUIqEfSOBch5ewr32p.xlsx",
}
MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
PEGS = {"USD": 1.0, "SAR": 3.75, "AED": 3.6725}   # currencies fixed to the US dollar


def as_of(wb):
    for ws in wb.worksheets:
        for row in ws.iter_rows(max_row=6, values_only=True):
            for c in row:
                m = re.search(r"as of\s+(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})", str(c or ""), re.I)
                if m:
                    return date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()
    return None


def day(v):
    if isinstance(v, datetime):
        return v.date().isoformat()
    m = re.match(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", str(v or ""))
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat() if m else None


def rows_of(ws):
    """The table under the header row that starts with '#', as dicts keyed by simplified header names."""
    rows = list(ws.iter_rows(values_only=True))
    for i, r in enumerate(rows):
        if r and str(r[0] or "").strip() == "#" or (len(r) > 1 and str(r[0] or "").strip() == "" and str(r[1] or "").strip() == "#"):
            hdr = [re.sub(r"[^a-z%#]+", " ", str(h or "").lower()).strip() for h in r]
            out = []
            for r2 in rows[i + 1:]:
                if not any(c not in (None, "") for c in r2):
                    break
                d = {hdr[j]: r2[j] for j in range(len(hdr)) if hdr[j]}
                if not isinstance(d.get("#"), (int, float)):
                    break
                out.append(d)
            return out
    return []


def pick(d, *names):
    for n in names:
        for k, v in d.items():
            if k.startswith(n):
                return v
    return None


def parse(kind, content):
    wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
    asof = as_of(wb)
    items = []
    for ws in wb.worksheets:
        group = "private" if "private" in ws.title.lower() else ("soe" if kind == "guarantees" else "loan")
        for d in rows_of(ws):
            amt = pick(d, "guaranteed amount", "amount")
            items.append({
                "group": group, "date": day(pick(d, "loan date", "date")),
                "creditor": str(pick(d, "creditor") or "").strip().replace("Male'", "Malé").rstrip("'").strip(),
                "beneficiary": str(pick(d, "beneficiary") or "").strip() or None,
                "purpose": re.sub(r"\s+", " ", str(pick(d, "purpose", "project") or "")).strip(),
                "currency": str(pick(d, "curren") or "").strip().upper(),
                "amount": float(amt) if isinstance(amt, (int, float)) else None,
                "status": str(pick(d, "project implementation", "implementation status", "implementation") or "").strip() or None,
            })
    return asof, items


def fx_on(d, currencies, usd_mvr):
    """Units of each currency per US dollar on day d. Pegged currencies use their peg, MVR the MMA rate."""
    rates, source = {}, None
    need = sorted(c for c in currencies if c not in PEGS and c != "MVR")
    if need:
        for url in (f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{d}/v1/currencies/usd.json",
                    f"https://{d}.currency-api.pages.dev/v1/currencies/usd.json"):
            try:
                j = requests.get(url, timeout=60).json()["usd"]
                rates = {c: float(j[c.lower()]) for c in need if c.lower() in j}
                source = "Exchange rates on that day from the open currency-api dataset (fawazahmed0), which compiles central bank and market rates"
                break
            except Exception as e:
                print(f"  exchange rates for {d} not available from {url.split('/')[2]} ({e})")
    rates.update({c: v for c, v in PEGS.items() if c in currencies})
    if "MVR" in currencies and usd_mvr:
        rates["MVR"] = usd_mvr
    return {"date": d, "per_usd": rates, "source": source,
            "notes": {"SAR": "fixed to the US dollar at 3.75", "AED": "fixed to the US dollar at 3.6725", "MVR": "MMA reference rate"}}


def mma_rate(d):
    try:
        pts = json.load(open(HERE / "data.json"))["series"]["usd_rate"]["points"]
        before = [p for p in pts if p["date"] <= d] or pts
        return before[-1]["value"]
    except Exception:
        return None


def main():
    INPUTS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for kind, url in FILES.items():
        try:
            r = requests.get(url, headers=H, timeout=90)
            r.raise_for_status()
            if not r.content.startswith(b"PK"):
                raise RuntimeError("not an Excel file")
            asof, items = parse(kind, r.content)
            if not asof or not items:
                raise RuntimeError("couldn't find the 'As of' date or the table")
        except Exception as e:
            print(f"{kind}: couldn't use the Ministry's file ({e}). Keeping the saved versions.")
            continue
        path = INPUTS / f"{kind}_{asof}.xlsx"
        if path.exists() and path.read_bytes() == r.content:
            print(f"{kind}: as of {asof}, no change.")
        else:
            path.write_bytes(r.content)
            print(f"{kind}: as of {asof}, {len(items)} rows, saved as {path.relative_to(HERE)}.")

    raw, fx = {"loans": {}, "guarantees": {}}, {}
    try:
        fx = json.load(open(OUT / "fx.json"))
    except Exception:
        pass
    for f in sorted(INPUTS.glob("*.xlsx")):
        kind = f.name.split("_")[0]
        asof, items = parse(kind, f.read_bytes())
        raw[kind][asof] = items
    # exchange rates on each "as of" day, for every currency used that day (looked up once, then kept)
    for asof in sorted({a for k in raw for a in raw[k]}):
        cur = {i["currency"] for k in raw for i in raw[k].get(asof, []) if i["currency"]}
        if not cur <= set(fx.get(asof, {}).get("per_usd", {})):
            fx[asof] = fx_on(asof, cur, mma_rate(asof))
            missing = sorted(cur - set(fx[asof]["per_usd"]))
            if missing:
                print(f"  no exchange rate for {', '.join(missing)} on {asof}")
    json.dump(raw, open(OUT / "raw.json", "w"), ensure_ascii=False, indent=0)
    json.dump(fx, open(OUT / "fx.json", "w"), indent=1)
    creditors = sorted({i["creditor"] for k in raw for v in raw[k].values() for i in v})
    print(f"Versions saved: {', '.join(f'{k} {sorted(v)}' for k, v in raw.items())}")
    print(f"{len(creditors)} creditors:\n  " + "\n  ".join(creditors))


if __name__ == "__main__":
    main()
