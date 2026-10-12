"""One-off look at the Ministry of Finance's debt files: what's in them, and whether older versions are listed.
Prints to the log only; changes nothing."""
import io, re, html, requests, openpyxl
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
FILES = {"guarantees": "https://www.finance.gov.mv/public/attachments/TNxIzceEndB8ZaPZbzjn9aMXG5wY4HFgJG473Rwy.xlsx",
         "loans": "https://www.finance.gov.mv/public/attachments/uhclBk3Vdbveshqh4b9u5jsUIqEfSOBch5ewr32p.xlsx"}
for name, url in FILES.items():
    print(f"\n===== {name}: {url}")
    try:
        r = requests.get(url, headers=H, timeout=60); print("status", r.status_code, len(r.content), "bytes")
        wb = openpyxl.load_workbook(io.BytesIO(r.content), data_only=True)
        for ws in wb.worksheets:
            print(f"--- sheet '{ws.title}': {ws.max_row} rows x {ws.max_column} cols")
            rows = list(ws.iter_rows(values_only=True))
            for i, row in enumerate(rows):
                if i < 9 or i >= len(rows) - 6:
                    print(i + 1, [c for c in row if c is not None][:10])
            cur = {}
            for row in rows:
                for c in row:
                    if isinstance(c, str) and re.fullmatch(r"[A-Z]{3}", c.strip()): cur[c.strip()] = cur.get(c.strip(), 0) + 1
            print("currencies:", cur)
    except Exception as e:
        print("ERROR", e)

print("\n===== looking for the pages that list these files, and older versions")
seen, queue, hits = set(), ["https://www.finance.gov.mv/", "https://www.finance.gov.mv/publications"], []
KEY = re.compile(r"guarant|borrow|external loan|debt|loan", re.I)
while queue and len(seen) < 60:
    u = queue.pop(0)
    if u in seen: continue
    seen.add(u)
    try:
        t = requests.get(u, headers=H, timeout=40).text
    except Exception as e:
        print("  can't open", u, e); continue
    for href, text in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', t, flags=re.S | re.I):
        text = html.unescape(re.sub(r"<[^>]+>", " ", text)).strip()
        full = href if href.startswith("http") else "https://www.finance.gov.mv" + href
        if "finance.gov.mv" not in full: continue
        if KEY.search(text) or KEY.search(href):
            if re.search(r"\.(xlsx?|pdf|csv)(\?|$)", full, re.I):
                hits.append((u, text[:120], full))
            elif full not in seen and len(queue) < 200 and "/publications" in full:
                queue.append(full)
print(f"pages read: {len(seen)}")
for p in sorted(seen): print("  page", p)
print(f"\nfiles found with debt / guarantee / loan in the name or link: {len(hits)}")
for u, t, f in hits: print(f"  [{t}] {f}   (on {u})")
