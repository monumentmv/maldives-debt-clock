"""
Ministry of Finance lists of active external loans and active sovereign guarantees.

Every new version of each file is kept in inputs/mof/, named by its "as of" date, so the history builds up
over time (the Ministry replaces the files on its website). Every version is read into
data/lenders/raw.json, with the IMF exchange rates on each version's "as of" date in data/lenders/fx.json
(the IMF tables used are kept in inputs/imf/).
build_lenders.py then turns that into lenders.json for the home page.

Runs every morning in GitHub Actions. To run it yourself:
    pip install requests openpyxl
    python fetch_lenders.py
"""
import io
import json
import re
from datetime import date, datetime, timedelta
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


IMF = "https://www.imf.org/external/np/fin/data/rms_mth.aspx?SelectDate={d}&reportType={r}&tsvflag=Y"
IMF_SAVE = HERE / "inputs" / "imf"
# IMF currency names -> ISO codes
IMF_NAMES = [("chinese yuan", "CNY"), ("renminbi", "CNY"), ("euro", "EUR"), ("indian rupee", "INR"), ("japanese yen", "JPY"),
             ("kuwaiti dinar", "KWD"), ("saudi arabian riyal", "SAR"), ("saudi riyal", "SAR"), ("u.a.e. dirham", "AED"),
             ("emirati dirham", "AED"), ("u.k. pound", "GBP"), ("pound sterling", "GBP"), ("swiss franc", "CHF"),
             ("korean won", "KRW"), ("singapore dollar", "SGD"), ("australian dollar", "AUD"), ("u.s. dollar", "USD")]


def _imf_day(t):
    t = t.strip()
    for f in ("%B %d, %Y", "%d-%b-%Y", "%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(t, f).date().isoformat()
        except ValueError:
            pass
    return None


def imf_table(d, report):
    """{ISO: (mode, {day: value})} from the IMF's monthly table that contains day d.
    mode says which way round the numbers are: per_usd, usd_per or per_sdr."""
    r = requests.get(IMF.format(d=d, r=report), headers=H, timeout=60)
    r.raise_for_status()
    IMF_SAVE.mkdir(parents=True, exist_ok=True)
    (IMF_SAVE / f"{report}_{d[:7]}.tsv").write_text(r.text)   # kept, so every rate used can be checked later
    out, mode, cols = {}, "per_usd" if report == "REP" else "per_sdr", []
    for line in r.text.splitlines():
        cells = [c.strip() for c in line.split("\t")]
        low = line.lower()
        if "dollars per currency unit" in low or "u.s.$ per" in low:
            mode = "usd_per"
        elif "units per u.s. dollar" in low or "per u.s.$" in low or "currency units per us dollar" in low:
            mode = "per_usd"
        elif "per sdr" in low:
            mode = "per_sdr"
        days = [_imf_day(c) for c in cells[1:]]
        if cells and cells[0].lower().startswith("currency") and any(days):
            cols = days
            continue
        name = cells[0].lower() if cells else ""
        code = next((c for n, c in IMF_NAMES if n in name), None)
        if not code or not cols:
            continue
        vals = {}
        for day_, v in zip(cols, cells[1:]):
            try:
                vals[day_] = float(v.replace(",", ""))
            except ValueError:
                pass
        if vals:
            out.setdefault(code, (mode, vals))
    return out


def imf_rates(d):
    """Units of each currency per US dollar on day d (or the last day before it the IMF has a rate), from the IMF."""
    prev = (date.fromisoformat(d[:8] + "01") - timedelta(days=1)).isoformat()
    rates, used = {}, {}
    for report in ("REP", "CVSDR"):
        tables = []
        for when in (d, prev):
            try:
                tables.append(imf_table(when, report))
            except Exception as e:
                print(f"  IMF {report} table for {when[:7]} not available ({e})")
        for t in tables:
            for code, (mode, vals) in t.items():
                ok = sorted(k for k in vals if k and k <= d)
                if not ok or (code in used and used[code] >= ok[-1]):
                    continue
                v = vals[ok[-1]]
                if report == "CVSDR":
                    if code != "USD":
                        continue
                    code, v = "XDR", 1 / v   # SDRs per US dollar
                elif mode == "usd_per":
                    v = 1 / v
                rates[code], used[code] = v, ok[-1]
    return rates, used


def fx_on(d, currencies, usd_mvr, before=None):
    """Units of each currency per US dollar on day d, from the IMF. MVR uses the MMA rate."""
    need = sorted(c for c in currencies if c not in ("USD", "MVR"))
    rates, notes = {"USD": 1.0} if "USD" in currencies else {}, {}
    imf, used = imf_rates(d) if need else ({}, {})
    for c in need:
        if c in imf:
            v = imf[c]
            old = (before or {}).get(c)
            if old and abs(v / old - 1) > .2 and abs((1 / v) / old - 1) < .05:   # a table read the other way round
                v = 1 / v
            rates[c] = v
            if used[c] != d:
                notes[c] = f"IMF rate on {date.fromisoformat(used[c]):%-d %B %Y}, the last day before with a rate"
    missing = [c for c in need if c not in rates]
    for c in missing:   # not in the IMF's tables: fixed pegs, else the open currency-api dataset
        if c in PEGS:
            rates[c], notes[c] = PEGS[c], f"fixed to the US dollar at {PEGS[c]}"
            continue
        for url in (f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{d}/v1/currencies/usd.json",
                    f"https://{d}.currency-api.pages.dev/v1/currencies/usd.json"):
            try:
                rates[c] = float(requests.get(url, timeout=60).json()["usd"][c.lower()])
                notes[c] = "not in the IMF's tables; open currency-api dataset"
                break
            except Exception:
                pass
    if "MVR" in currencies and usd_mvr:
        rates["MVR"], notes["MVR"] = usd_mvr, "MMA reference rate"
    from_imf = any(c in imf for c in need)
    return {"date": d, "per_usd": rates, "notes": notes, "imf": from_imf,
            "source": "Representative exchange rates published by the International Monetary Fund (IMF) for that day" if from_imf else None}


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
        if not fx.get(asof, {}).get("imf") or not cur <= set(fx[asof].get("per_usd", {})):
            fx[asof] = fx_on(asof, cur, mma_rate(asof), fx.get(asof, {}).get("per_usd"))
            print(f"  exchange rates for {asof}: " + ", ".join(f"{c} {v:.4f}" for c, v in sorted(fx[asof]['per_usd'].items())))
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
