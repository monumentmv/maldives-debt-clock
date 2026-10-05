"""
Turns MIRA's monthly revenue spreadsheets into revenue.json for the revenue page.

Reads every .xlsx file in inputs/mira/ and recognises the two MIRA files by their title:
  "REVENUE SERIES (MONTHLY) - TOTAL REVENUE COLLECTION"  all collections, in rufiyaa
  "REVENUE SERIES (MONTHLY) - USD REVENUE COLLECTION"    the part paid in US dollars

Runs in GitHub Actions whenever a file in inputs/mira/ changes. To run it yourself:
    pip install openpyxl
    python build_revenue.py
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("Please run:  pip install openpyxl")

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs" / "mira"
OUT = HERE / "revenue.json"
MON = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

GROUPS = [
    ("tourism_gst", "Tourism GST"),
    ("gst_other", "GST outside tourism"),
    ("green", "Green tax"),
    ("airport", "Airport taxes and fees"),
    ("resort_land", "Resort land and leases"),
    ("business", "Business profit taxes"),
    ("personal", "Personal income taxes"),
    ("tourism_tax", "Tourism tax (ended 2014)"),
    ("other", "Other taxes and fees"),
]
GROUP_OF = {
    "gst (tourism sector)": "tourism_gst",
    "gst (non-tourism sector)": "gst_other",
    "green tax": "green",
    "airport service charge": "airport",
    "airport development fee": "airport",
    "departure tax": "airport",
    "tourism land rent": "resort_land",
    "lease period extension fee": "resort_land",
    "land acquisition and conversion fee": "resort_land",
    "construction period extension fee": "resort_land",
    "corporate income tax": "business",
    "business profit tax": "business",
    "bank profit tax": "business",
    "withholding tax": "business",
    "non-resident withholding tax": "business",
    "personal income tax": "personal",
    "employee withholding tax": "personal",
    "tourism tax": "tourism_tax",
}
# lines shown on their own inside a group
DETAIL = {"tourism land rent": "Tourism land rent", "lease period extension fee": "Lease period extensions",
          "land acquisition and conversion fee": "Land acquisition and conversion",
          "construction period extension fee": "Construction period extensions"}


def norm(name):
    n = re.sub(r"\s+", " ", str(name)).strip().lower()
    return n.replace("goods and services tax", "gst")


def read_sheet(path):
    ws = openpyxl.load_workbook(path, data_only=True, read_only=True).worksheets[0]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    title = str(rows[0][0] or "").upper()
    kind = "usd" if "USD REVENUE" in title else "all" if "TOTAL REVENUE" in title else None
    if not kind:
        return None
    years, months = rows[1], rows[2]
    cols, y = {}, None
    for j in range(1, len(months)):
        if years[j] not in (None, ""):
            y = int(years[j])
        m = str(months[j] or "").strip().lower()[:3]
        if y and m in MON:
            cols[j] = f"{y}-{MON.index(m) + 1:02d}"
    items, total, note = {}, None, ""
    for r in rows[3:]:
        label = r[0]
        if label is None:
            continue
        if str(label).lower().startswith("updated on"):
            note = str(label).strip()
            continue
        vals = {cols[j]: (float(r[j]) if isinstance(r[j], (int, float)) else None) for j in cols}
        if total is not None:
            continue  # zakat and donations sit below TOTAL and are not part of it
        if norm(label) == "total":
            total = vals
            continue
        items[str(label).strip()] = vals
    if total is None:
        sys.exit(f"{path.name}: no TOTAL row found")
    return {"kind": kind, "items": items, "total": total, "note": note, "file": path.name}


def main():
    files = sorted(INPUTS.glob("*.xlsx"))
    if not files:
        print("No MIRA files in inputs/mira/, nothing to do.")
        return
    found = {}
    for f in files:
        s = read_sheet(f)
        if s:
            if s["kind"] in found:
                sys.exit(f"Two {s['kind']} files in inputs/mira/ ({found[s['kind']]['file']}, {f.name}). Delete the older one.")
            found[s["kind"]] = s
        else:
            print(f"Skipping {f.name}, not a recognised MIRA monthly revenue file.")
    if "all" not in found:
        sys.exit("The total revenue collection file is missing from inputs/mira/.")
    A, U = found["all"], found.get("usd")

    # months run from the first to the last month with a total above zero
    months = sorted(m for m, v in A["total"].items() if v)
    first, last = months[0], months[-1]
    months = sorted(m for m in A["total"] if first <= m <= last)
    usd_months = sorted(m for m, v in (U["total"] if U else {}).items() if v and m <= last)
    usd_from = usd_months[0] if usd_months else None

    problems = []
    for name, S in (("all", A), ("usd", U)):
        if not S:
            continue
        for m in months:
            t = S["total"].get(m)
            if t is None or (name == "usd" and (not usd_from or m < usd_from)):
                continue
            s = sum(v[m] or 0 for v in S["items"].values())
            if abs(s - t) > max(1.0, abs(t) * 1e-6):
                problems.append(f"{name} file, {m}: lines add up to {s:,.0f} but TOTAL says {t:,.0f}")
    if problems:
        print("Warning, totals don't match:\n  " + "\n  ".join(problems[:20]))

    def by_group(S, start):
        out = {k: [0.0] * len(months) for k, _ in GROUPS}
        detail = {label: [0.0] * len(months) for label in DETAIL.values()}
        unknown = set()
        for name, vals in S["items"].items():
            n = norm(name)
            g = GROUP_OF.get(n, "other")
            if g == "other" and n not in ("others",):
                unknown.add(name)
            for i, m in enumerate(months):
                v = vals.get(m) or 0.0
                out[g][i] += v
                if n in DETAIL:
                    detail[DETAIL[n]][i] += v
        for arr in list(out.values()) + list(detail.values()):
            for i, m in enumerate(months):
                arr[i] = None if (start and m < start) else round(arr[i], 2)
        return out, detail, unknown

    mvr, mvr_detail, other_all = by_group(A, None)
    usd, usd_detail, other_usd = (by_group(U, usd_from) if U else (None, None, set()))
    total_mvr = [round(A["total"].get(m) or 0.0, 2) for m in months]
    total_usd = [None if (not U or not usd_from or m < usd_from) else round(U["total"].get(m) or 0.0, 2) for m in months]

    data = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Maldives Inland Revenue Authority, monthly revenue collection",
        "source_note": A["note"],
        "files": [A["file"]] + ([U["file"]] if U else []),
        "start": months[0],
        "end": months[-1],
        "usd_start": usd_from,
        "months": months,
        "groups": [{"key": k, "label": l} for k, l in GROUPS],
        "total": {"mvr": total_mvr, "usd": total_usd},
        "mvr": mvr,
        "usd": usd,
        "detail": {"mvr": mvr_detail, "usd": usd_detail},
        "other_lines": {"all": sorted(other_all), "usd": sorted(other_usd)},
        "warnings": problems,
    }
    OUT.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    yr = months[-1][:4]
    ytd = sum(v for m, v in zip(months, total_mvr) if m.startswith(yr))
    print(f"OK. {months[0]} to {months[-1]} ({len(months)} months), dollar figures from {usd_from}. "
          f"{yr} so far MVR {ytd / 1e9:,.2f} bn. Wrote {OUT.name}.")


if __name__ == "__main__":
    main()
