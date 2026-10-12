/* Maldives National Debt Clock: every active external loan and sovereign guarantee (home page, "Who is the money owed to?").
   Reads lenders.json, built by build_lenders.py from Ministry of Finance lists. Also the "What's in this number?" pop-up. */
(() => {
  const $ = id => document.getElementById(id);
  const { fmt } = MV;
  const usd = v => v == null ? "–" : "US$ " + MV.short(v);
  const day = d => d ? MV.dayLabel(d) : "–";
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const colour = () => KC[kind];   // every bar in the colour of what is shown: loans or guarantees
  let L = null, kind = "loans", group = "all", asof = null, only = null, q = "", sortBy = "d", desc = true, all = false, status = "all";
  let W = null, mshow = "both", minst = true, mpick = null, mzoom = innerWidth < 700 ? "region" : "world";   // map: what to show, and the place picked
  let mbasis = "owed", mq = 0, playing = null;   // map: still owed (Debt Bulletins) or originally borrowed (Ministry lists), and which quarter
  const O = () => L?.owed, QS = () => O()?.quarters || [], qNow = () => QS()[mq];
  const qLabel = d => "End of " + MV.mLabel(d);
  const mvr = (v, d) => MV.moneyNow(v * 1e6, d);
  // what is still owed to each lender at a quarter, in the same shape as a list row
  function owedRows(k, d, home) {   // home: also guaranteed debt owed to banks in Maldives (not on the map)
    const o = O(); if (!o) return [];
    const rate = o.rate[d] || 15.42, row = ([l, v]) => { const w = o.who[l] || {}; return { l, c: w.c, pl: w.pl, m: v[d], usd: v[d] * 1e6 / rate }; };
    const ext = Object.entries(o[k] || {}).filter(([, v]) => v[d] > 0).map(row);
    return home && k === "guarantees" ? ext.concat(Object.entries(o.guarantees_home || {}).filter(([, v]) => v[d] > 0).map(row)) : ext;
  }
  const KC = { loans: "#3fb8b0", guarantees: "#b39ddb" }, KW = { loans: "loan", guarantees: "guarantee" };
  // flags (stored with the site, so every phone shows the same)
  const FLAG = { China: ["cn"], India: ["in"], "Saudi Arabia": ["sa"], "United Arab Emirates": ["ae"], Kuwait: ["kw"], Oman: ["om"], Pakistan: ["pk"], Japan: ["jp"],
    France: ["fr"], Belgium: ["be"], "Germany and the Netherlands": ["de", "nl"], "United States": ["us"], Hungary: ["hu"], Denmark: ["dk"], Switzerland: ["ch"],
    "Sri Lanka": ["lk"], Maldives: ["mv"], "United Kingdom": ["gb"] };
  const WORLD = `<svg class="flag-world" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M2.5 12h19M12 2.5c3 3 3 16 0 19M12 2.5c-3 3-3 16 0 19" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>`;
  const isInst = k => L?.places?.[k]?.kind === "institution";
  const flag = (c, pl) => isInst(pl) ? `<i class="flag-inst" aria-hidden="true"></i>` : c === "Multilateral institutions" ? WORLD
    : (FLAG[c] || []).map(x => `<img class="flag" src="assets/flag-${x}.svg" alt="" width="20" height="15">`).join("");
  // who a page is about: a development bank or fund (by its place), or a country or group (by name)
  const whoOf = r => isInst(r.pl) ? r.pl : r.c;
  const matches = key => isInst(key) ? r => r.pl === key : r => r.c === key;
  const nameOf = key => key === "Germany and the Netherlands" ? "Germany and Netherlands" : key;

  // ---------- the map: every lender, with a line to Malé ----------
  function rowsAll(k) { if (mbasis === "owed" && O()) return owedRows(k, qNow()); const v = L.lists[k], a = v[asof] ? asof : Object.keys(v).sort().pop(); return v[a] || []; }
  function curMix(rows) {   // amounts in their own currencies, largest first
    const m = {}; rows.forEach(r => { if (r.a != null) m[r.cur] = (m[r.cur] || 0) + r.a; });
    return Object.entries(m).sort((a, b) => b[1] - a[1]).map(([c, v]) => `${c} ${MV.short(v)}`).join(" + ");
  }
  function drawMap() {
    if (!L || !W) return;
    const box = $("lendMap"), P = L.places, rad = d => d * Math.PI / 180;
    const xy = (lon, lat) => { let d = lon - W.lon0; d = ((d + 540) % 360) - 180; return [W.tx + W.s * rad(d), W.ty - W.s * rad(lat)]; };
    const kinds = mshow === "both" ? ["loans", "guarantees"] : [mshow];
    const nodes = {};
    kinds.forEach(k => rowsAll(k).forEach(r => {
      if (!r.pl || !P[r.pl] || (!minst && P[r.pl].kind === "institution")) return;
      const n = nodes[r.pl] = nodes[r.pl] || { key: r.pl, ...P[r.pl], loans: [], guarantees: [] };
      n[k].push(r);
    }));
    const list = Object.values(nodes).map(n => ({ ...n, lu: n.loans.reduce((s, r) => s + (r.usd || 0), 0), gu: n.guarantees.reduce((s, r) => s + (r.usd || 0), 0) }));
    let maxT = Math.max(1, ...list.map(n => n.lu + n.gu));
    if (mbasis === "owed" && O()) {   // the same scale for every quarter, so the dots grow and shrink as the years play
      maxT = Math.max(1, ...QS().map(d => { const t = {}; kinds.forEach(k => owedRows(k, d).forEach(r => { if (r.pl) t[r.pl] = (t[r.pl] || 0) + r.usd; })); return Math.max(0, ...Object.values(t)); }));
    }
    // whole world, or a closer view from the Gulf to China (the default on phones)
    const [ax, ay] = xy(26, 50), [bx, by] = xy(128, -9), vb = mzoom === "region" ? [ax, ay, bx - ax, by - ay] : [0, 0, W.w, W.h];
    const [mx, my] = xy(73.5, 4.2), px = vb[2] / Math.max(300, box.clientWidth || W.w);   // px: map units per screen pixel
    // places in the same city (the World Bank and the United States, AIIB and China) are nudged apart
    list.forEach(n => { [n.x, n.y] = xy(n.lon, n.lat); });
    list.forEach((n, i) => list.slice(0, i).forEach(m => { if (Math.hypot(n.x - m.x, n.y - m.y) < 14 * px) { n.x += 13 * px; n.y += 11 * px; } }));
    const shade = {}; list.forEach(n => (n.map || []).forEach(c => { shade[c] = n.lu ? "loans" : "guarantees"; }));
    let g = `<path d="${W.land}" class="land"/>` + Object.entries(W.countries).filter(([c]) => shade[c]).map(([c, d]) => `<path d="${d}" class="lc ${shade[c]}"/>`).join("");
    const arc = (n, k) => {
      const v = k === "loans" ? n.lu : n.gu; if (!v) return "";
      const dx = mx - n.x, dy = my - n.y, len = Math.hypot(dx, dy) || 1;
      let nx = -dy / len, ny = dx / len; if (ny > 0) { nx = -nx; ny = -ny; }        // bow towards the north
      const bend = (k === "guarantees" && n.lu ? -1 : 1) * Math.min(120, len * .22);  // two lines bow apart when a place has both
      const cx = (n.x + mx) / 2 + nx * bend, cy = (n.y + my) / 2 + ny * bend, w = 2 * px;
      return `<path class="arc ${k}${mpick && mpick !== n.key ? " dim" : ""}" data-pl="${esc(n.key)}" d="M${n.x.toFixed(1)} ${n.y.toFixed(1)} Q${cx.toFixed(1)} ${cy.toFixed(1)} ${mx.toFixed(1)} ${my.toFixed(1)}" style="stroke-width:${w.toFixed(2)};stroke-dasharray:${(6 * px).toFixed(1)} ${(5 * px).toFixed(1)}"><title>${esc(n.label)}: ${usd(v)} ${mbasis === "owed" && O() ? "still owed in" : "in"} ${KW[k]}s</title></path>`;
    };
    list.sort((a, b) => (b.lu + b.gu) - (a.lu + a.gu));
    g += list.map(n => arc(n, "loans") + arc(n, "guarantees")).join("");
    const fs = 12 * px, placed = [[mx, my, mx + 70 * px, my + 22 * px]];   // label boxes already drawn, so labels never overlap
    const labels = [], free = (x0, y0, x1, y1) => !placed.some(([a, b, c, d]) => x0 < c && x1 > a && y0 < d && y1 > b);
    g += list.map((n, i) => {
      const r = Math.max(3 + 7 * Math.sqrt((n.lu + n.gu) / maxT), n.kind === "institution" || !FLAG[n.key] ? 0 : 7) * px, col = n.lu && n.gu ? "#fff" : n.lu ? KC.loans : KC.guarantees;
      const fl = FLAG[n.key], rf = r, cid = "cf" + i;
      const mark = n.kind === "institution"
        ? `<rect x="${(n.x - r).toFixed(1)}" y="${(n.y - r).toFixed(1)}" width="${(2 * r).toFixed(1)}" height="${(2 * r).toFixed(1)}" rx="${(r * .3).toFixed(1)}" transform="rotate(45 ${n.x.toFixed(1)} ${n.y.toFixed(1)})" fill="${col}"/>`
        : fl ? `<clipPath id="${cid}"><circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${rf.toFixed(1)}"/></clipPath><image href="assets/flag-${fl[0]}.svg" x="${(n.x - rf * 1.34).toFixed(1)}" y="${(n.y - rf).toFixed(1)}" width="${(rf * 2.68).toFixed(1)}" height="${(rf * 2).toFixed(1)}" clip-path="url(#${cid})" preserveAspectRatio="xMidYMid slice"/><circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${rf.toFixed(1)}" fill="none" stroke="${col}" stroke-width="${(2 * px).toFixed(2)}"/>`
        : `<circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${r.toFixed(1)}" fill="${col}"/>`;
      let lab = "";
      const tw = n.label.length * fs * .58, inView = n.x > vb[0] && n.x < vb[0] + vb[2] && n.y > vb[1] && n.y < vb[1] + vb[3];
      for (const [lx, anchor] of [[n.x + r + 4 * px, "start"], [n.x - r - 4 * px, "end"]]) {   // right of the mark, else left
        const x0 = anchor === "start" ? lx : lx - tw, b = [x0, n.y - fs * .8, x0 + tw, n.y + fs * .4];
        if (inView && b[0] > vb[0] && b[2] < vb[0] + vb[2] && free(...b)) { placed.push(b); lab = `<text x="${lx.toFixed(1)}" y="${(n.y + 4 * px).toFixed(1)}" text-anchor="${anchor}" style="font-size:${fs.toFixed(1)}px">${esc(n.label)}</text>`; break; }
      }
      labels.push(lab.replace("<text ", `<text data-pl="${esc(n.key)}" `));
      return `<g class="node${mpick === n.key ? " on" : ""}" data-pl="${esc(n.key)}" tabindex="0" role="button" aria-label="${esc(n.label)}">${mark}</g>`;
    }).join("") + `<g class="labels">${labels.join("")}</g>`;   // labels on top of every mark
    g += `<circle cx="${mx}" cy="${my}" r="${6 * px}" class="male"/><text x="${mx + 9 * px}" y="${my + 18 * px}" class="male-t" style="font-size:${(fs * 1.05).toFixed(1)}px">Maldives</text>`;
    box.innerHTML = `<svg viewBox="${vb.map(v => v.toFixed(1)).join(" ")}" role="img" aria-label="Map of where Maldives' foreign loans and guaranteed loans come from">${g}</svg>`;
    // the quarter, and the totals at that quarter
    const owed = mbasis === "owed" && O();
    $("qNav").hidden = !O(); $("mapBasis").hidden = !O();
    if (O()) { const d = qNow(), sm = k => Object.values(O()[k] || {}).reduce((t, v) => t + (v[d] || 0), 0);
      $("foreignNote").innerHTML = `<span class="why-fx big"><b>Why foreign debt matters more than its size.</b> It has to be repaid in foreign currency, mostly US dollars, and Maldives cannot issue (print) foreign currency. Neither the government nor Maldives Monetary Authority can create it. It has to be earned, mostly from tourism, or borrowed again from abroad. <button type="button" class="linkish" data-term="foreign">Read more</button></span>`
        + `Foreign debt is money owed to lenders abroad, such as other governments, development banks and international bond holders. At the end of ${MV.mLabel(d)} the government owed <b>${mvr(sm("loans"), d)}</b> abroad, and state companies and others owed <b>${mvr(sm("guarantees"), d)}</b> abroad with a government guarantee.`; }
    if (O()) {
      const d = qNow(), src = pdfOf(d);
      $("mapQ").max = QS().length - 1; $("mapQ").value = mq; $("mapQl").textContent = qLabel(d);
      document.querySelectorAll("[data-qs]").forEach(b => { b.disabled = b.dataset.qs < 0 ? mq <= 0 : mq >= QS().length - 1; });
      $("qSrc").innerHTML = src ? `Figures for this quarter come from Ministry of Finance's <a href="${esc(src.url)}" target="_blank" rel="noopener">Quarterly Debt Bulletin, ${MV.mLabel(d)} (PDF)</a>.`
        : `Figures for this quarter come from later Quarterly Debt Bulletins, which go back to ${MV.mLabel(QS()[0])}. <a href="https://www.finance.gov.mv/publications/reports-and-analyses/quarterly-debt-bulletin" target="_blank" rel="noopener">All bulletins</a>.`;
    }
    if (owed) {
      const d = qNow(), sum = k => owedRows(k, d).reduce((s, r) => s + r.m, 0);
      $("mapTot").className = "map-tot";
      $("mapTot").innerHTML = `The map shows who it is owed to at the end of ${MV.mLabel(d)}. Press ▶ to watch it change since ${MV.mLabel(QS()[0])}.`;
    } else {
      $("mapTot").className = "map-tot map-warn";
      $("mapTot").innerHTML = `<b>This is not what is owed today.</b> It shows what was agreed for every loan and guarantee on Ministry of Finance's lists as of ${day(asof)}, including loans for finished projects that are still being repaid, and a few repaid since.${O() ? ` <button type="button" class="linkish" data-mb="owed">Show what is still owed</button>` : ""}`;
    }
    // not on the map
    const off = {};
    kinds.forEach(k => rowsAll(k).forEach(r => { if (!r.pl || !P[r.pl] || (!minst && P[r.pl].kind === "institution")) { const key = r.pl && P[r.pl] ? "Development banks and funds (hidden)" : (r.c === "Maldives" ? "Maldivian banks" : r.l); (off[key] = off[key] || { loans: [], guarantees: [] })[k].push(r); } }));
    $("mapOff").innerHTML = Object.keys(off).length ? "<b>Not on the map:</b> " + Object.entries(off).map(([k, v]) => `${esc(k)}, ` + ["loans", "guarantees"].filter(x => v[x].length).map(x => owed ? `${mvr(v[x].reduce((s, r) => s + r.m, 0), qNow())} still owed in ${KW[x]}s` : `${usd(v[x].reduce((s, r) => s + (r.usd || 0), 0))} in ${KW[x]}s (${curMix(v[x])})`).join(" and ")).join("; ") + "." : "";
    drawCard();
  }
  function drawCard() {
    $("mapCard").innerHTML = `<p class="hint">Tap a country or a development bank to see everything about it, including what is still owed, how that has changed, and every loan and guarantee.</p>`;
  }

  // ---------- a full page for one lender or year, with a way back to exactly where you were ----------
  let sheetEl = null, sheetFrom = null, sheetDepth = 0;
  function showSheet(title, html) {
    if (!sheetEl) {
      sheetFrom = document.activeElement;
      sheetEl = document.createElement("div"); sheetEl.className = "sheet"; sheetEl.setAttribute("role", "dialog"); sheetEl.setAttribute("aria-modal", "true");
      document.body.appendChild(sheetEl); document.body.classList.add("sheet-open");
    }
    sheetEl.innerHTML = `<div class="sheet-bar"><button type="button" class="sheet-back">← Back</button><div class="sheet-ttl" id="sheetT">${title}</div></div><div class="sheet-body">${html}</div>`;
    sheetEl.setAttribute("aria-labelledby", "sheetT"); sheetEl.scrollTop = 0;
    sheetEl.querySelector(".sheet-back").focus({ preventScroll: true });
  }
  function closeSheet() {
    if (!sheetEl) return;
    sheetEl.remove(); sheetEl = null; document.body.classList.remove("sheet-open");
    sheetFrom?.focus?.({ preventScroll: true });
  }
  // every page opened is a step in the browser's history, so the phone's back gesture works too
  function go(hash) { window.history.pushState({ lend: hash }, "", "#" + hash); sheetDepth++; render(hash); }
  function back() { if (sheetDepth > 0) window.history.back(); else { closeSheet(); window.history.replaceState(null, "", location.pathname + location.search); } }
  addEventListener("popstate", () => { sheetDepth = Math.max(0, sheetDepth - 1); const h = location.hash.slice(1); if (/^(lender|signed|borrower)=/.test(h) && L) render(h); else closeSheet(); });
  addEventListener("keydown", e => { if (e.key === "Escape" && sheetEl) back(); });
  function render(hash) {
    const [k, v] = hash.split("="), val = decodeURIComponent(v || "");
    if (k === "lender") placePage(val);
    else if (k === "signed") { const [y, kd] = val.split("-"); yearPage(y, kd || "loans"); }
    else if (k === "borrower") borrowerPage(val);
  }
  const pdfOf = d => O()?.sources.find(x => x.q === d);
  // a borrower's name, as both the Ministry's list and the bulletin write it ("Ltd", "Limited", "Co." and so on dropped)
  const bkey = n => (n || "").toLowerCase().replace(/[^a-z ]/g, " ").replace(/\b(ltd|limited|plc|private|pvt|company|co|corporation|corp|the)\b/g, " ").split(/\s+/).filter(Boolean).slice(0, 3).join(" ");
  const short = n => (n || "").replace(/ (Limited|Ltd|PLC|Private Limited|Pvt Ltd)$/, "");
  function copy(btn, text) {
    const done = () => { btn.classList.add("done"); const t = btn.textContent; btn.textContent = "Copied"; setTimeout(() => { btn.classList.remove("done"); btn.textContent = t; }, 1800); };
    (navigator.clipboard?.writeText(text) || Promise.reject()).then(done).catch(() => { const a = document.createElement("textarea"); a.value = text; document.body.appendChild(a); a.select(); try { document.execCommand("copy"); done(); } catch (e) {} a.remove(); });
  }
  const itemHTML = (r, k) => `<div class="sh-item"><div><div class="w">${esc(r.l)}${paid(r.l) ? `<span class="lend-flag">nothing owed now</span>` : ""}</div>
      <div class="m">Signed ${r.d ? MV.dayLabel(r.d) : "date not given"}${r.s && r.s !== "NA" ? `<span class="tag${r.s === "Ongoing" ? " on" : ""}">Project ${r.s === "Ongoing" ? "under way" : r.s === "Completed" ? "finished" : esc(r.s)}</span>` : ""}</div></div>
      <div class="a">${usd(r.usd)}<small>${esc(r.cur)} ${r.a == null ? "–" : MV.short(r.a)}</small></div>
      <div class="p">${k === "guarantees" && r.b ? `<b>For ${esc(r.b)}:</b> ` : ""}${esc(r.p || "")}</div></div>`;
  function placePage(key) {
    const m = matches(key), o = O(), d = o ? qNow() : null, P = L.places[key];
    const title = `${flag(isInst(key) ? null : key, isInst(key) ? key : null)}${esc(nameOf(key))}`;
    let h = "";
    if (o) {
      const lo = owedRows("loans", d).filter(m), gu = owedRows("guarantees", d, true).filter(m), sum = a => a.reduce((s, r) => s + r.m, 0);
      const box = (k, rs, t) => `<div style="--kc:${KC[k]}"><span>${t}</span><b>${rs.length ? mvr(sum(rs), d) : "Nothing"}</b>${rs.length ? `<span>about ${usd(rs.reduce((s, r) => s + r.usd, 0))}</span>` : ""}${rs.length > 1 ? rs.sort((a, b) => b.m - a.m).map(r => `<div class="mc-row"><span>${esc(r.l)}</span><b>${mvr(r.m, d)}</b></div>`).join("") : rs.length ? `<div class="mc-row"><span>${esc(rs[0].l)}</span></div>` : ""}</div>`;
      h += `<p class="hint">Still owed at the end of ${MV.mLabel(d)}${pdfOf(d) ? `, from <a href="${esc(pdfOf(d).url)}" target="_blank" rel="noopener">Ministry of Finance's Quarterly Debt Bulletin</a>` : ", from Ministry of Finance's Quarterly Debt Bulletins"}. Change the quarter with ‹ › on the main page.</p>
        <div class="sh-tot">${box("loans", lo, "Owed by the government")}${box("guarantees", gu, "Owed by others, guaranteed by the government")}</div>`;
      // history, quarter by quarter
      const qs = QS(), ser = qs.map(q => [owedRows("loans", q).filter(m).reduce((s, r) => s + r.m, 0), owedRows("guarantees", q, true).filter(m).reduce((s, r) => s + r.m, 0)]);
      if (ser.some(([a, b]) => a + b > 0)) {
        const W = 640, H = 150, bw = (W - 20) / qs.length, top = Math.max(1, ...ser.map(([a, b]) => a + b));
        h += `<h3>Still owed, every quarter since ${MV.mLabel(qs[0])}</h3><div class="sh-chart"><svg viewBox="0 0 ${W} ${H + 20}" role="img" aria-label="Still owed each quarter">`
          + qs.map((q, i) => { const [a, b] = ser[i], ha = a / top * H, hb = b / top * H, x = 10 + i * bw + 1, w = Math.max(1, bw - 2), sel = q === d;
            return `<g${sel ? ' opacity="1"' : ' opacity=".75"'}><rect x="${x.toFixed(1)}" y="${(H - ha).toFixed(1)}" width="${w.toFixed(1)}" height="${ha.toFixed(1)}" fill="${KC.loans}"><title>${MV.mLabel(q)}: ${mvr(a, q)} owed by the government</title></rect><rect x="${x.toFixed(1)}" y="${(H - ha - hb).toFixed(1)}" width="${w.toFixed(1)}" height="${hb.toFixed(1)}" fill="${KC.guarantees}"><title>${MV.mLabel(q)}: ${mvr(b, q)} guaranteed</title></rect>${sel ? `<rect x="${x.toFixed(1)}" y="0" width="${w.toFixed(1)}" height="${H}" fill="none" stroke="#fff" stroke-width="1.5"/>` : ""}</g>`; }).join("")
          + qs.map((q, i) => q.endsWith("03-31") ? `<text x="${(10 + i * bw).toFixed(1)}" y="${H + 15}">${q.slice(0, 4)}</text>` : "").join("")
          + `</svg></div><p class="hint">Teal is what the government owes. Lavender is what others owe with a government guarantee. Tap or hover a bar for its figures.</p>`;
      }
    }
    // every loan and guarantee signed
    ["loans", "guarantees"].forEach(k => {
      const v = L.lists[k], a = v[asof] ? asof : Object.keys(v).sort().pop(), rs = (v[a] || []).filter(m).sort((x, y) => (y.d || "").localeCompare(x.d || ""));
      if (!rs.length) return;
      h += `<h3>${rs.length} ${k === "loans" ? `loan${rs.length > 1 ? "s" : ""} to the government` : `loan${rs.length > 1 ? "s" : ""} guaranteed by the government`}, ${usd(rs.reduce((s, r) => s + (r.usd || 0), 0))} originally</h3>
        <p class="hint">From Ministry of Finance's list as of ${day(a)}. Amounts are what was agreed, converted at IMF rates for that date.</p><div class="sh-list">${rs.map(r => itemHTML(r, k)).join("")}</div>`;
    });
    if (!h) h = `<p>Nothing is listed for ${esc(nameOf(key))}.</p>`;
    const cite = () => { const lo = o ? owedRows("loans", d).filter(m).reduce((s, r) => s + r.m, 0) : 0, gu = o ? owedRows("guarantees", d, true).filter(m).reduce((s, r) => s + r.m, 0) : 0;
      return `At the end of ${MV.mLabel(d)}, Maldives government owed ${mvr(lo, d)} to ${nameOf(key)}${gu ? `, and ${mvr(gu, d)} more was owed to ${nameOf(key)} by state companies and others under government guarantees` : ""}. Source: Ministry of Finance, Quarterly Debt Bulletin${pdfOf(d) ? ` (${pdfOf(d).url})` : ""}. Via Maldives National Debt Clock, ${location.origin}${location.pathname}#lender=${encodeURIComponent(key)}`; };
    showSheet(title, `${h}<div class="sheet-acts"><button type="button" data-copy="cite">Copy these figures, with source</button><button type="button" data-copy="link">Copy a link to this page</button></div>`);
    sheetEl._cite = cite; sheetEl._link = `${location.origin}${location.pathname}#lender=${encodeURIComponent(key)}`;
  }
  function yearPage(y, k) {
    const v = L.lists[k], a = v[asof] ? asof : Object.keys(v).sort().pop(), rs = (v[a] || []).filter(r => r.d && r.d.slice(0, 4) === y).sort((x, z) => (z.usd || 0) - (x.usd || 0));
    const word = k === "loans" ? "loan" : "guarantee";
    showSheet(`${rs.length} ${word}${rs.length === 1 ? "" : "s"} signed in ${esc(y)}`,
      `<div class="sh-tot"><div style="--kc:${KC[k]}"><span>${k === "loans" ? "Borrowed" : "Guaranteed"} in ${esc(y)}, as agreed</span><b>${usd(rs.reduce((s, r) => s + (r.usd || 0), 0))}</b><span>${rs.length} ${word}${rs.length === 1 ? "" : "s"} still on Ministry of Finance's list as of ${day(a)}</span></div></div>
       <h3>Largest first</h3><div class="sh-list">${rs.map(r => itemHTML(r, k).replace('<div class="w">', `<div class="w"><button type="button" class="cty" data-who="${esc(whoOf(r))}">${flag(r.c, r.pl)}</button>`)).join("")}</div>
       <p class="hint">Only ${word}s still on the Ministry's list are counted. Ones fully repaid before the list was made are not included.</p>
       <div class="sheet-acts"><button type="button" data-copy="link">Copy a link to this page</button></div>`);
    sheetEl._link = `${location.origin}${location.pathname}#signed=${y}-${k}`;
  }

  function borrowerPage(name) {
    const o = O(), d = qNow(), qs = QS(), ser = o.guaranteed_for[name] || {}, rate = o.rate[d] || 15.42;
    const gl = L.lists.guarantees, ga = gl[asof] ? asof : Object.keys(gl).sort().pop(), rows = (gl[ga] || []).filter(r => bkey(r.b) === bkey(name)).sort((x, y) => (y.d || "").localeCompare(x.d || ""));
    const now = ser[d] || {}, owed = (now.ext || 0) + (now.dom || 0), agreedUSD = rows.reduce((t, r) => t + (r.usd || 0), 0), agreed = agreedUSD * rate / 1e6, showA = d >= ga && agreed > 0;
    const swap = /Monetary Authority/.test(name);
    // what the bulletins show: owed now, against the first quarter they cover (and, for the swaps, the most ever owed)
    const tq = q => { const x = ser[q] || {}; return (x.ext || 0) + (x.dom || 0); }, known = qs.filter(q => q <= d && tq(q) > 0);
    const first = known[0], peakQ = known.reduce((p, q) => tq(q) > tq(p) ? q : p, first);
    let h = `<p class="lead-in">${swap ? `${esc(short(name))}, the central bank, has currency swaps with Reserve Bank of India, India's central bank. Ministry of Finance lists them among its sovereign guarantees and counts what has been drawn as government-guaranteed debt.`
        : `${esc(short(name))} borrowed with a government guarantee. If it can't repay, the government has promised to.`}`
      + (showA ? ` ${swap ? "The swaps on its list were agreed for" : "The guarantees on Ministry of Finance's list cover loans of"} <b>${usd(agreedUSD)}</b>, about ${mvr(agreed, d)}.` : "")
      + ` At the end of ${MV.mLabel(d)} it owed <b>${mvr(owed, d)}</b>${swap ? " on them" : ""}.`
      + (swap && peakQ && peakQ !== d && tq(peakQ) > owed ? ` The most it has owed was ${mvr(tq(peakQ), peakQ)}, at the end of ${MV.mLabel(peakQ)}.`
        : !swap && first && first !== d && Math.abs(tq(first) - owed) > 1 ? ` That is ${tq(first) > owed ? "down" : "up"} from ${mvr(tq(first), first)} at the end of ${MV.mLabel(first)}${tq(first) > owed ? ", as it has been repaying" : ""}.` : "")
      + `</p>`;
    h += `<div class="sh-tot"><div style="--kc:${KC.guarantees}"><span>Still owed, end of ${MV.mLabel(d)}</span><b>${mvr(owed, d)}</b>${now.dom ? `<span>${now.ext ? `${mvr(now.dom, d)} of it to banks in Maldives` : "all to banks in Maldives"}</span>` : ""}</div>`
      + (showA ? `<div style="--kc:#7f9aa5"><span>Agreed, on the Ministry's list</span><b>${mvr(agreed, d)}</b><span>${usd(agreedUSD)}, ${rows.length} loan${rows.length === 1 ? "" : "s"}</span></div>` : "") + `</div>`;
    // what it owed, quarter by quarter
    const vals = qs.map(q => { const x = ser[q] || {}; return (x.ext || 0) + (x.dom || 0); });
    if (vals.some(v => v > 0)) {
      const W = 640, H = 160, bw = (W - 20) / qs.length, top = Math.max(1, ...vals, showA ? agreed : 0), y = v => H - v / top * H;
      h += `<h3>Still owed, every quarter</h3><div class="sh-chart"><svg viewBox="0 0 ${W} ${H + 20}" role="img" aria-label="Still owed each quarter">`
        + qs.map((q, i) => { const x = 10 + i * bw + 1, w = Math.max(1, bw - 2), e = (ser[q] || {}).ext || 0, m = (ser[q] || {}).dom || 0;
            return `<g opacity="${q === d ? 1 : .75}"><rect x="${x.toFixed(1)}" y="${y(e).toFixed(1)}" width="${w.toFixed(1)}" height="${(H - y(e)).toFixed(1)}" fill="${KC.guarantees}"><title>${MV.mLabel(q)}: ${mvr(e, q)} owed abroad</title></rect>`
              + (m ? `<rect x="${x.toFixed(1)}" y="${y(e + m).toFixed(1)}" width="${w.toFixed(1)}" height="${(y(e) - y(e + m)).toFixed(1)}" fill="#ddd2f2"><title>${MV.mLabel(q)}: ${mvr(m, q)} owed to banks in Maldives</title></rect>` : "") + `</g>`; }).join("")
        + (showA ? `<line x1="10" x2="${W - 10}" y1="${y(agreed).toFixed(1)}" y2="${y(agreed).toFixed(1)}" stroke="#f4c95d" stroke-width="1.5" stroke-dasharray="5 4"/><text x="${W - 12}" y="${(y(agreed) - 5).toFixed(1)}" text-anchor="end" style="fill:#f4c95d">agreed ${mvr(agreed, d)}</text>` : "")
        + qs.map((q, i) => q.endsWith("03-31") ? `<text x="${(10 + i * bw).toFixed(1)}" y="${H + 15}">${q.slice(0, 4)}</text>` : "").join("")
        + `</svg></div><p class="hint">From Ministry of Finance's Quarterly Debt Bulletins. ${qs.some(q => (ser[q] || {}).dom) ? "Darker: owed to lenders abroad. Lighter: owed to banks in Maldives. " : ""}${showA ? "Yellow line: the total agreed, for the guarantees on today's list. " : ""}A falling bar means it is being repaid.`
        + (showA && vals.some(v => v > agreed + 1) ? ` Where a bar is above the line, ${esc(short(name))} also owed on other guaranteed loans that have since been repaid, so they are no longer on the list.` : "") + ` Tap or hover a bar for its figure.</p>`;
    }
    if (rows.length) h += `<h3>${swap ? "The swaps, as listed" : "The loans the government guaranteed"}</h3><p class="hint">From Ministry of Finance's list of active sovereign guarantees as of ${day(ga)}. Amounts are what was agreed.</p>`
      + `<div class="sh-list">${rows.map(r => itemHTML(r, "loans").replace('<div class="w">', `<div class="w"><button type="button" class="cty" data-who="${esc(whoOf(r))}" aria-label="${esc(nameOf(r.c))}">${flag(r.c, r.pl)}</button>`).replace("</small></div>", ` = ${mvr((r.usd || 0) * rate / 1e6, d)}</small></div>`)).join("")}</div>`;
    const link = `${location.origin}${location.pathname}#borrower=${encodeURIComponent(name)}`;
    showSheet(esc(short(name)), `${h}<div class="sheet-acts"><button type="button" data-copy="cite">Copy these figures, with source</button><button type="button" data-copy="link">Copy a link to this page</button></div>`);
    sheetEl._link = link;
    sheetEl._cite = () => `At the end of ${MV.mLabel(d)}, ${short(name)} owed ${mvr(owed, d)} on debt counted as guaranteed by Maldives government${showA ? `. The guarantees on Ministry of Finance's list total ${usd(agreedUSD)}, about ${mvr(agreed, d)}` : ""}. Sources: Ministry of Finance, Quarterly Debt Bulletin${pdfOf(d) ? ` (${pdfOf(d).url})` : ""}, and list of active sovereign guarantees. Via Maldives National Debt Clock, ${link}`;
  }

  // ---------- the two parts of the debt: domestic and foreign ----------
  function drawParts() {
    const o = O(); if (!o) { $("parts").innerHTML = ""; return; }
    const d = qNow(), sum = k => Object.values(o[k] || {}).reduce((t, v) => t + (v[d] || 0), 0);
    const hg = o.home?.total?.[d] || 0, hgu = sum("guarantees_home"), fg = sum("loans"), fgu = sum("guarantees"), all = hg + hgu + fg + fgu;
    if (!all) { $("parts").innerHTML = ""; return; }
    const card = (id, kc, name, total, gov, gu, who, why) => `<div class="part" style="--kc:${kc}"><span class="k">${name}</span><b class="num">${mvr(total, d)}</b>
      <span class="s">${mvr(gov, d)} owed by the government, and ${mvr(gu, d)} owed by state companies and others with a government guarantee.</span><span class="s">${who}</span>${why || ""}<button type="button" class="go" data-part="${id}">See the details ↓</button></div>`;
    $("parts").innerHTML = `<p class="parts-lead">All public debt, <b>${mvr(all, d)}</b> at the end of ${MV.mLabel(d)}, is in two parts. Domestic debt is owed to lenders in Maldives. Foreign debt is owed to lenders abroad.</p>`
      + card("partHome", "#f4c95d", "1. Domestic debt", hg + hgu, hg, hgu, "Mostly owed to banks, the pension fund and Maldives Monetary Authority.")
      + card("partForeign", "#3fb8b0", "2. Foreign debt", fg + fgu, fg, fgu, "Owed to other countries, development banks and international bond holders.",
        `<span class="why-fx">Smaller, but harder to repay. It must be paid in US dollars or other foreign currencies, which Maldives cannot issue (print). <button type="button" class="linkish" data-term="foreign">Why it matters</button></span>`);
  }

  // ---------- owed at home: who holds the government's domestic debt ----------
  const HC = { "Banks": "#3fb8b0", "Pension fund and other financial firms": "#f4c95d", "Maldives Monetary Authority": "#9fe0d6", "State companies": "#b39ddb", "Individuals and private companies": "#7f9aa5" };
  function drawHome() {
    const o = O(), H = o?.home; $("lendHome").hidden = !H; if (!H) return;
    const d = qNow(), tot = H.total[d], abroad = Object.values(o.loans).reduce((t, v) => t + (v[d] || 0), 0);

    if (!tot) { $("homeNote").textContent = "The bulletins don't give this for this quarter."; ["homeBars", "homeKey", "homeChart"].forEach(i => { $(i).innerHTML = ""; }); return; }
    const ty = H.type, cu = H.cur, v = (t, k) => (t[k] || {})[d] || 0, ratio = abroad ? tot / abroad : 0;
    $("homeNote").innerHTML = `Domestic debt is money the government owes to lenders in Maldives. At the end of ${MV.mLabel(d)} it was <b>${mvr(tot, d)}</b>${abroad ? `, ${ratio >= 1.5 ? `${fmt(ratio, 1)} times` : "more than"} the ${mvr(abroad, d)} the government owed abroad` : ""}.`
      + ` Of it, ${mvr(v(ty, "Treasury bills"), d)} is in treasury bills, which fall due within a year, and ${mvr(v(ty, "Bonds"), d)} is in bonds.`
      + (v(cu, "USD") ? ` ${mvr(v(cu, "USD"), d)} of it is in US dollars, even though it is owed at home.` : "") + ` Here is who it is owed to.`;
    const rows = Object.entries(H.cat).map(([n, x]) => [n, x[d] || 0]).filter(([, x]) => x > 0).sort((a, b) => b[1] - a[1]), top = rows[0]?.[1] || 1;
    $("homeBars").innerHTML = rows.map(([n, x]) => `<div class="lb" role="img" aria-label="${esc(n)}: ${mvr(x, d)}"><span class="n">${esc(n)}</span><span class="t"><i style="width:${x / top * 100}%;background:${HC[n] || "#7f9aa5"}"></i></span><span class="v num">${mvr(x, d)}<small>${x / tot < .005 ? "under 1%" : fmt(x / tot * 100, 0) + "%"}</small></span></div>`).join("");
    // who has held it, quarter by quarter
    const qs = Object.keys(H.total).sort(), names = Object.keys(HC).filter(n => H.cat[n]), Wd = Math.max(300, $("homeChart").clientWidth || 640), Hh = 150, bw = (Wd - 30) / qs.length, mx = Math.max(...qs.map(q => H.total[q] || 0), 1);
    $("homeKey").innerHTML = names.map(n => `<span><i style="background:${HC[n]}"></i>${esc(n)}</span>`).join("");
    $("homeChart").innerHTML = `<svg viewBox="0 0 ${Wd} ${Hh + 22}" role="img" aria-label="Owed at home, by who holds it, every quarter">`
      + qs.map((q, j) => { let y = Hh; const x = 15 + j * bw + 1, w = Math.max(1, bw - 2);
          return `<g data-q="${q}" opacity="${q === d ? 1 : .6}" style="cursor:pointer">` + names.map(n => { const h = ((H.cat[n] || {})[q] || 0) / mx * Hh; y -= h;
            return `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" fill="${HC[n]}"><title>${MV.mLabel(q)}, ${n}: ${mvr((H.cat[n] || {})[q] || 0, q)}</title></rect>`; }).join("")
            + (q === d ? `<rect x="${x.toFixed(1)}" y="0" width="${w.toFixed(1)}" height="${Hh}" fill="none" stroke="#fff" stroke-width="1.5"/>` : "") + `</g>`; }).join("")
      + qs.map((q, j) => q.endsWith("03-31") && (bw > 14 || q.slice(0, 4) % 2 === 0) ? `<text x="${(15 + j * bw).toFixed(1)}" y="${Hh + 16}">${q.slice(0, 4)}</text>` : "").join("")
      + `<line x1="15" x2="${Wd - 15}" y1="${Hh}" y2="${Hh}" stroke="rgba(169,205,214,.3)"/></svg>`;
    $("homeSrc").innerHTML = `Each bar is one quarter. Tap a bar to move to that quarter. Source: Ministry of Finance's Quarterly Debt Bulletins, tables of domestic debt by creditor, by instrument and by currency. The bulletin calls these groups central bank, commercial banks, other financial corporations, public non-financial corporations and private. This is the government's own debt at home. Debt it has guaranteed for others at home is shown under who owes the guaranteed debt.`;
  }

  // ---------- from the Debt Bulletins: repayments, money still to come, loans passed on ----------
  // "April to June 2026" for the quarter ending 30 June 2026
  const qSpan = d => { const e = new Date(d + "T00:00:00Z"), st = new Date(Date.UTC(e.getUTCFullYear(), e.getUTCMonth() - 2, 1)), mo = x => x.toLocaleString("en-GB", { month: "long", timeZone: "UTC" });
    return `${mo(st)} to ${mo(e)} ${e.getUTCFullYear()}`; };
  function drawBul() {
    drawParts(); drawHome();
    const o = O(); $("lendBul").hidden = !o; if (!o) return;
    const d = qNow(), S = o.service, qs = Object.keys(S).sort(), tot = q => ["gp", "gi", "sp", "si"].reduce((a, k) => a + (S[q][k] || 0), 0);
    // repayments: the four quarters to the one chosen
    const upto = qs.filter(q => q <= d), yr = upto.slice(-4), sum = k => yr.reduce((a, q) => a + (S[q][k] || 0), 0);
    const i = o.quarters.indexOf(d), prev = o.quarters[i - 1], drops = [];
    if (prev) ["loans", "guarantees"].forEach(k => Object.entries(o[k]).forEach(([l, v]) => { const dlt = (v[prev] || 0) - (v[d] || 0); if (dlt > 300) drops.push([l, dlt]); }));
    drops.sort((x, y) => y[1] - x[1]);
    $("svcNote").innerHTML = !yr.length ? `The bulletins give repayments and interest from ${MV.mLabel(qs[0])}. Move the quarter forward to see them.`
      : `The government repays its loans and pays interest at different times through the year. Ministry of Finance reports the payments for each quarter, shown here as one bar per quarter. In the ${yr.length === 4 ? "year" : `${yr.length} quarter${yr.length > 1 ? "s" : ""}`} to the end of ${MV.mLabel(yr[yr.length - 1])} it paid <b>${mvr(sum("gp"), d)}</b> in repayments and <b>${mvr(sum("gi"), d)}</b> in interest. `
      + `State companies and others paid <b>${mvr(sum("sp") + sum("si"), d)}</b> on debt the government guaranteed for them, <b>${mvr(sum("si"), d)}</b> of it interest. That interest is not in the clock's <i>interest accrued</i>, as the government doesn't pay it.`
      + (S[d] ? ` Payments in ${qSpan(d)} alone came to ${mvr(tot(d), d)}.` : "")
      + (drops.length ? ` What was owed abroad fell most for ${drops.slice(0, 2).map(([l, v]) => `${esc(l)} (down ${mvr(v, d)})`).join(" and ")}.` : "");
    const Wd = Math.max(300, $("lendSvc").clientWidth || 640), Hh = 150, bw = (Wd - 30) / qs.length, top = Math.max(...qs.map(tot), 1);
    const COLS = { gp: "#3fb8b0", gi: "#9fe0d6", sp: "#b39ddb", si: "#ddd2f2" }, NAMES = { gp: "government repayments", gi: "government interest", sp: "guaranteed repayments", si: "guaranteed interest" };
    $("lendSvc").innerHTML = `<svg viewBox="0 0 ${Wd} ${Hh + 22}" role="img" aria-label="Repayments and interest each quarter">`
      + qs.map((q, j) => { let y = Hh; const x = 15 + j * bw + 1, w = Math.max(1, bw - 2);
          return `<g data-q="${q}" opacity="${q === d ? 1 : .55}" style="cursor:pointer">` + ["gp", "gi", "sp", "si"].map(k => { const h = (S[q][k] || 0) / top * Hh; y -= h;
            return `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" fill="${COLS[k]}"><title>${MV.mLabel(q)}: ${NAMES[k]} ${mvr(S[q][k] || 0, q)}</title></rect>`; }).join("")
            + (q === d ? `<rect x="${x.toFixed(1)}" y="0" width="${w.toFixed(1)}" height="${Hh}" fill="none" stroke="#fff" stroke-width="1.5"/>` : "") + `</g>`; }).join("")
      + qs.map((q, j) => q.endsWith("03-31") && (bw > 14 || q.slice(0, 4) % 2 === 0) ? `<text x="${(15 + j * bw).toFixed(1)}" y="${Hh + 16}">${q.slice(0, 4)}</text>` : "").join("")
      + `<line x1="15" x2="${Wd - 15}" y1="${Hh}" y2="${Hh}" stroke="rgba(169,205,214,.3)"/></svg><p class="hint">Each bar is one quarter (three months). Tap a bar to move to that quarter.</p>`;
    // still to come, and passed on, at the chosen quarter
    const at = tbl => Object.entries(tbl).map(([n, v]) => [n, v[d]]).filter(([, v]) => v > 0).sort((x, y) => y[1] - x[1]);
    const cub = at(o.cub), sub = at(o.subsidiary), t = a => a.reduce((s, [, v]) => s + v, 0);
    const list = a => a.slice(0, 3).map(([n, v]) => `${esc(n.replace(/ (Limited|Ltd|PLC|Private Limited)$/, ""))} ${mvr(v, d)}`).join(", ");
    $("lendExtra").innerHTML = (cub.length ? `<div><b class="num">${mvr(t(cub), d)}</b><span>in loans the government has signed with lenders abroad but not yet received, at the end of ${MV.mLabel(d)}. It becomes debt as the money is drawn.</span><small>Largest: ${list(cub)}</small><small>Source: Debt Bulletin table "Committed Undisbursed Balance (CUB) of BCG External Loans".</small></div>`
        : `<div><b>–</b><span>Money agreed but not yet paid out is in the bulletins from ${MV.mLabel(Object.values(o.cub).flatMap(Object.keys).sort()[0])}.</span></div>`)
      + (sub.length ? `<div><b class="num">${mvr(t(sub), d)}</b><span>in "subsidiary loans": in Ministry of Finance's words, "loans borrowed by the Government and on-lent to an institution", mostly state companies. The government is the borrower, so this is already part of its debt, not extra.</span><small>Largest: ${list(sub)}</small><small>Source: Debt Bulletin table "Outstanding under Subsidiary Loans", and its definitions page.</small></div>`
        : `<div><b>–</b><span>Loans passed on to state companies are in the bulletins from ${MV.mLabel(Object.values(o.subsidiary).flatMap(Object.keys).sort()[0])}.</span></div>`);
    // guaranteed for whom: still owed (Debt Bulletin) against what was agreed (Ministry's list of guarantees)
    const gl = L.lists.guarantees, ga = gl[asof] ? asof : Object.keys(gl).sort().pop(), agreed = {}, rate = o.rate[d] || 15.42;
    (gl[ga] || []).forEach(r => { if (r.usd) (agreed[bkey(r.b)] = agreed[bkey(r.b)] || []).push(r); });
    const ben = Object.entries(o.guaranteed_for).map(([n, v]) => [n, v[d]]).filter(([, v]) => v).map(([n, v]) => [n, (v.ext || 0) + (v.dom || 0), v]).sort((x, y) => y[1] - x[1]);
    const showA = d >= ga;   // the list is from one date: for earlier quarters it would include guarantees not yet signed
    const agr = n => showA ? (agreed[bkey(n)] || []).reduce((s, r) => s + r.usd, 0) * rate / 1e6 : 0, bm = Math.max(1, ...ben.map(([n, v]) => Math.max(v, agr(n))));
    $("lendFor").innerHTML = ben.map(([n, v, p]) => { const a = agr(n);
      return `<button type="button" class="lb" data-ben="${esc(n)}" aria-label="${esc(n)}: ${mvr(v, d)} still owed${a ? `, ${mvr(a, d)} agreed` : ""}. See its loans"><span class="n">${esc(n.replace(/ (Limited|Ltd|PLC|Private Limited|Pvt Ltd)$/, ""))}</span><span class="t">${a ? `<i class="f" style="width:${a / bm * 100}%;background:${KC.guarantees}"></i>` : ""}<i style="width:${v / bm * 100}%;background:${KC.guarantees}"></i></span><span class="v num">${mvr(v, d)}${a ? `<small>of ${mvr(a, d)} agreed</small>` : ""}${p.dom ? `<small>${p.ext ? `${mvr(p.dom, d)} of it` : "all"} at home</small>` : ""}</span></button>`; }).join("")
      + (!showA ? `<p class="hint">Still owed at the end of ${MV.mLabel(d)}, from the Debt Bulletin.</p>` : "")
      + (!showA ? "" : `<p class="hint">The solid bar is what was still owed at the end of ${MV.mLabel(d)}, from the Debt Bulletin. The faint bar is the total of the guarantees on Ministry of Finance's list as of ${day(ga)}, at the bulletin's exchange rate. Tap a name for its loans and repayments.</p>`)
      + (ben.length ? "" : `<p class="hint">Not given for this quarter.</p>`);
    $("forHead").textContent = `Who owes the guaranteed debt, at the end of ${MV.mLabel(d)}`;
    $("forNote").innerHTML = `These are the state companies and others that borrowed with a government guarantee, and how much each still owed on that date. It is not what they borrowed during the quarter. It is everything still owed, from loans taken over many years. If they can't repay, the government has promised to.`
      + (() => { const m = ben.find(([n]) => /Monetary Authority/.test(n)); if (!m) return ""; const sw = agreed[bkey(m[0])] || [];
          return ` <b>Maldives Monetary Authority</b>, the central bank, is here because of its currency swaps with Reserve Bank of India, India's central bank. They are usually described simply as currency swaps between the two central banks. Ministry of Finance lists them among its sovereign guarantees and counts what MMA has drawn as government-guaranteed debt, so they are shown here the same way.`
            + (sw.length && showA ? ` The swaps were agreed for ${sw.map(r => `${esc(r.cur)} ${MV.short(r.a)}`).join(" and ")}, about ${mvr(agr(m[0]), d)} together. At the end of ${MV.mLabel(d)}, ${mvr(m[1], d)} was owed on them.` : ""); })();
    $("bulSrc").innerHTML = `Source: Ministry of Finance's Quarterly Debt Bulletins, ${MV.mLabel(o.sources[0].q)} to ${MV.mLabel(o.latest)}. Where a later bulletin revised a quarter, the later figure is used.`;
  }

  // ---------- "What's in this number?" ----------
  function whatIn() {
    const S = window.MV_DATA?.series; if (!S) return;
    const last = k => (S[k]?.points || []).slice(-1)[0];
    const tot = last("total"), dcg = last("domestic_cg"), ecg = last("external_cg"), dg = last("domestic_guaranteed"), eg = last("external_guaranteed");
    if (!tot || !dcg || !ecg || !dg || !eg) return;
    const bn = v => "MVR " + fmt(v / 1e9, 1) + " bn", gov = dcg.value + ecg.value, gu = dg.value + eg.value;
    const box = document.createElement("div"); box.className = "explain"; box.setAttribute("role", "presentation");
    box.innerHTML = `<div class="explain-box what-in" role="dialog" aria-modal="true" aria-labelledby="wiT"><button type="button" class="x" aria-label="Close">×</button>
      <h3 id="wiT">What's in this number</h3>
      <p>The clock counts all public debt, the standard measure. That is what the government owes itself, plus what it has guaranteed for others. Official figures at the end of ${MV.mLabel(tot.date)}:</p>
      <table class="wi"><tr><th></th><th>At home</th><th>Abroad</th><th>Total</th></tr>
        <tr><td>Owed by the government</td><td>${bn(dcg.value)}</td><td>${bn(ecg.value)}</td><td><b>${bn(gov)}</b></td></tr>
        <tr><td>Guaranteed by the government</td><td>${bn(dg.value)}</td><td>${bn(eg.value)}</td><td><b>${bn(gu)}</b></td></tr>
        <tr class="t"><td>All public debt</td><td></td><td></td><td><b>${bn(tot.value)}</b></td></tr></table>
      <p>Guaranteed debt is borrowed by state-owned companies and a few others, with the government promising to repay if they can't. They pay its interest themselves, so <b>interest accrued</b> counts only the interest in the government's own budget.</p>
      <a class="more" href="#ch-owed" id="wiGo">See every loan and guarantee</a></div>`;
    const close = () => box.remove();
    box.addEventListener("click", e => { if (e.target === box || e.target.closest(".x")) close(); });
    addEventListener("keydown", function k(e) { if (e.key === "Escape") { close(); removeEventListener("keydown", k); } });
    box.querySelector("#wiGo").addEventListener("click", e => { e.preventDefault(); close(); openPanel(true); });
    document.body.appendChild(box); box.querySelector(".x").focus();
  }

  // ---------- the panel ----------
  function openPanel(scroll) {
    const head = document.querySelector("#ch-owed .chap-head");
    if (head && head.getAttribute("aria-expanded") !== "true") head.click();
    if ($("lendPanel").hidden) toggle();
    if (scroll) setTimeout(() => $("lendBtn").scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  }
  function toggle() {
    const open = $("lendPanel").hidden;
    $("lendPanel").hidden = !open; $("lendBtn").setAttribute("aria-expanded", open);
    $("lendBtn").querySelector(".t").textContent = open ? "Hide the details" : "See who it is owed to, at home and abroad";
    if (open && !L) Promise.all([MV.getJSON("lenders.json"), MV.getJSON("assets/worldmap.json").catch(() => null)]).then(([j, w]) => { L = j; W = w; asof = j.versions[j.versions.length - 1]; mbasis = j.owed ? "owed" : "signed"; mq = Math.max(0, QS().length - 1); draw(); drawBul();
      const h = location.hash.slice(1); if (/^(lender|signed|borrower)=/.test(h)) render(h); })
      .catch(() => { $("lendNote").textContent = "The lists couldn't be loaded. Please try again later."; });
  }
  const rowsNow = () => {
    const v = L.lists[kind], a = v[asof] ? asof : Object.keys(v).sort().pop();
    return (v[a] || []).filter(r => group === "all" || r.g === group);
  };
  function draw() {
    if (!L) return;
    const rows = rowsNow(), word = kind === "loans" ? "loan" : "guarantee";
    $("lendG").hidden = kind !== "guarantees";
    $("lendAsof").innerHTML = L.versions.slice().reverse().map(v => `<option value="${v}"${v === asof ? " selected" : ""}>${day(v)}</option>`).join("");
    const tot = rows.reduce((s, r) => s + (r.usd || 0), 0), open = rows.filter(r => /ongoing/i.test(r.s || "")).length;
    $("lendNote").innerHTML = kind === "loans"
      ? `Every foreign loan the government still has on its books, as Ministry of Finance lists them, as of <b>${day(asof)}</b>. Amounts are <b>what was originally borrowed</b>, not what is still owed. Many have been partly repaid.`
      : `Every loan the government has guaranteed for others, as Ministry of Finance lists them, as of <b>${day(asof)}</b>. If the borrower can't repay, the government has promised to. Amounts are <b>what was originally guaranteed</b>, not what is still owed.`;
    listHistory(rows, word);
    // the list's country filter: countries, then each development bank
    const opts = {}; rowsNow().forEach(r => { const k = whoOf(r); opts[k] = (opts[k] || 0) + 1; });
    if (only && !opts[only]) only = null;
    $("lendC").innerHTML = `<option value="">Every country and lender</option>` + Object.keys(opts).sort((a, b) => (isInst(a) - isInst(b)) || a.localeCompare(b))
      .map(k => `<option value="${esc(k)}"${k === only ? " selected" : ""}>${esc(nameOf(k))}${isInst(k) ? "" : ""} (${opts[k]})</option>`).join("");
    // summary
    const by = {}; rows.forEach(r => { by[r.c] = (by[r.c] || 0) + (r.usd || 0); });
    let groups = Object.entries(by).sort((a, b) => b[1] - a[1]);
    $("lendSum").innerHTML = `<div><b class="num">${fmt(rows.length)}</b><span>${word}s${open ? `, ${fmt(open)} still being carried out` : ""}</span></div>`
      + `<div><b class="num">${usd(tot)}</b><span>${kind === "loans" ? "borrowed" : "guaranteed"} in all, in US dollars</span></div>`
      + (O() && group === "all" ? `<div><b class="num">${usd(owedRows(kind, O().latest, true).reduce((s, r) => s + r.usd, 0))}</b><span>still owed at the end of ${MV.mLabel(O().latest)}, from the Debt Bulletin</span></div>` : "")
      + (groups[0] ? `<div><b>${esc(groups[0][0])}</b><span>the largest source, ${fmt(groups[0][1] / tot * 100, 0)}%</span></div>` : "");
    // by lender: what was borrowed (faint) and, from the latest Debt Bulletin, what is still owed (solid)
    const o = O(), oq = o?.latest, ow = {};
    if (o && group === "all") owedRows(kind, oq, true).forEach(r => { ow[r.c] = (ow[r.c] || 0) + r.usd; });
    const none = v => v > 0 ? usd(v) : "none";
    if (o && group === "all") Object.keys(ow).forEach(c => { if (!(c in by) && !only) groups.push([c, 0]); });   // owed to a lender not on the Ministry's list
    const hasOw = o && group === "all", max = Math.max(groups[0]?.[1] || 1, ...Object.values(ow));
    $("lendBars").innerHTML = groups.map(([c, v]) => `<button type="button" class="lb" data-c="${esc(c)}">
      <span class="n">${flag(c)}${esc(nameOf(c))}</span><span class="t">${hasOw ? `<i class="f" style="width:${v / max * 100}%;background:${colour(c)}"></i><i style="width:${(ow[c] || 0) / max * 100}%;background:${colour(c)}"></i>` : `<i style="width:${v / max * 100}%;background:${colour(c)}"></i>`}</span>
      <span class="v num">${hasOw ? `${none(ow[c] || 0)}<small>of ${none(v)}</small>` : usd(v)}</span></button>`).join("")
      + `<p class="hint">${hasOw ? `The solid bar is what was still owed at the end of ${MV.mLabel(oq)}, from the Debt Bulletin. The faint bar is what was originally ${kind === "loans" ? "borrowed" : "guaranteed"}, from the Ministry's list. ` : ""}Tap one for everything about it.</p>`;
    // signed each year
    const yrs = {}; rows.forEach(r => { if (r.d) { const y = r.d.slice(0, 4); yrs[y] = (yrs[y] || 0) + (r.usd || 0); } });
    const ys = Object.keys(yrs).sort(), y0 = +ys[0], y1 = +ys[ys.length - 1], ym = Math.max(...Object.values(yrs), 1);
    const W = Math.max(300, $("lendYears").clientWidth || 640), Hh = 140, bw = (W - 40) / (y1 - y0 + 1), step = W < 500 ? 10 : 5;
    $("lendYears").innerHTML = ys.length ? `<svg viewBox="0 0 ${W} ${Hh + 22}" role="img" aria-label="${word}s signed each year, in US dollars">`
      + ys.map(y => { const h = yrs[y] / ym * Hh; return `<rect data-yr="${y}" tabindex="0" role="button" aria-label="${y}: ${usd(yrs[y])}, see the ${word}s" x="${20 + (y - y0) * bw + 1}" y="${Math.min(Hh - h, Hh - 3)}" width="${Math.max(1, bw - 2)}" height="${Math.max(h, 3)}" fill="${KC[kind]}"><title>${y}: ${usd(yrs[y])}. Tap to see them.</title></rect>`; }).join("")
      + Array.from({ length: y1 - y0 + 1 }, (_, i) => y0 + i).filter(y => y % step === 0).map(y => `<text x="${20 + (y - y0 + .5) * bw}" y="${Hh + 16}" text-anchor="middle">${y}</text>`).join("")
      + `<line x1="20" x2="${W - 20}" y1="${Hh}" y2="${Hh}" stroke="rgba(169,205,214,.3)"/></svg><p class="hint">The highest year was ${Object.entries(yrs).sort((a, b) => b[1] - a[1])[0][0]}, with ${usd(ym)}. Tap a bar to see that year's ${word}s.</p>` : "";
    drawTable(); drawMap();
    // exchange rates
    const fx = L.fx[asof] || {}, cur = [...new Set(rowsNow().map(r => r.cur))].sort();
    $("lendFx").innerHTML = `<p>Each amount is converted to US dollars at the rate on <b>${day(fx.rate_date || fx.date)}</b>${(fx.rate_date || fx.date) === fx.date ? ", the date of the Ministry's list" : `, the last month-end before the Ministry's list of ${day(fx.date)}`}, so all ${word}s are compared at the same rates.</p><ul>`
      + cur.map(c => `<li><b>${c}</b> ${c === "USD" ? "US dollar" : `${fmt(fx.per_usd?.[c], fx.per_usd?.[c] < 10 ? 4 : 2)} per US dollar${fx.notes?.[c] ? `, ${fx.notes[c]}` : ""}`}${c === "XDR" ? " (the IMF's Special Drawing Right, used by IDA, IFAD and others)" : ""}</li>`).join("")
      + `</ul><p class="hint">${esc(fx.source || "")}.</p>`;
  }
  // each list the Ministry publishes is kept: an older one stays here as history when a new one comes in
  function listHistory(rows, word) {
    const ks = Object.keys(L.lists[kind]).sort(), i = ks.indexOf(asof), latest = ks[ks.length - 1], el = $("lendHist");
    if (!el) return;
    if (ks.length < 2) { el.innerHTML = `This is the first ${word} list saved here. When Ministry of Finance publishes a new one, this list will be kept as history, and you can pick its date under <b>As of</b> to see it again.`; return; }
    const key = r => [r.l, r.d, r.cur, r.a, r.b].join("|"), sum = a => a.reduce((s, r) => s + (r.usd || 0), 0);
    let t = asof !== latest ? `This is an older list. <a href="#" data-asof="${latest}">See the latest, ${day(latest)}</a>. ` : "";
    if (i > 0) {
      const prev = (L.lists[kind][ks[i - 1]] || []).filter(r => group === "all" || r.g === group), was = new Set(prev.map(key)), now = new Set(rows.map(key));
      const added = rows.filter(r => !was.has(key(r))), gone = prev.filter(r => !now.has(key(r)));
      t += `Since the list of ${day(ks[i - 1])}, <b>${fmt(added.length)}</b> added${added.length ? ` (${esc([...new Set(added.map(r => r.l))].slice(0, 3).join(", "))}${added.length > 3 ? "…" : ""})` : ""}, <b>${fmt(gone.length)}</b> no longer listed. Total ${usd(sum(prev))} then, ${usd(sum(rows))} now.`;
    } else t += `This is the oldest list saved here.`;
    el.innerHTML = t;
  }
  // a lender the latest Debt Bulletin lists with nothing owed (and no other amount owed to it)
  function paid(l) {
    const o = O(); if (!o) return false;
    const vs = ["loans", "guarantees", "guarantees_home"].map(k => (o[k] || {})[l]).filter(Boolean);
    return vs.length > 0 && vs.every(v => v[o.latest] === 0);   // listed, with nothing owed (a lender simply missing from it isn't counted)
  }
  function drawTable() {
    let rows = rowsNow().filter(r => (!only || matches(only)(r)) && (status === "all" || (status === "paid" ? paid(r.l) : status === "Completed" ? r.s === "Completed" : r.s === status)));
    if (q) { const k = q.toLowerCase(); rows = rows.filter(r => [r.l, r.c, r.p, r.b, r.cur, r.d].some(x => String(x || "").toLowerCase().includes(k))); }
    const val = r => sortBy === "usd" ? (r.usd || 0) : sortBy === "l" ? r.l : (r.d || "");
    rows.sort((a, b) => (val(a) < val(b) ? -1 : val(a) > val(b) ? 1 : 0) * (desc ? -1 : 1));
    const show = all ? rows : rows.slice(0, 12), g = kind === "guarantees";
    const th = (k, t) => `<th${k ? ` data-sort="${k}" aria-sort="${sortBy === k ? (desc ? "descending" : "ascending") : "none"}"` : ""}>${t}${sortBy === k ? (desc ? " ↓" : " ↑") : ""}</th>`;
    $("lendTbl").innerHTML = `<thead><tr>${th("d", "Signed")}${th("l", "Lender")}<th>${g ? "For whom, and what" : "What for"}</th><th class="r">Amount</th>${th("usd", "In US$")}<th class="st">Project</th></tr></thead><tbody>`
      + show.map(r => `<tr><td class="num sg">${r.d ? r.d.slice(0, 4) : "–"}<small>${r.d ? MV.dayLabel(r.d).replace(/ \d{4}$/, "") : ""}</small></td>
        <td>${esc(r.l)}${paid(r.l) ? `<span class="lend-flag" title="Debt Bulletin for ${MV.mLabel(O().latest)} shows nothing owed to this lender">nothing owed now</span>` : ""}<small><button type="button" class="cty" data-who="${esc(whoOf(r))}">${flag(r.c, r.pl)}${esc(isInst(r.pl) ? r.c.replace("Multilateral institutions", "Development bank or fund") : nameOf(r.c))}</button></small></td>
        <td>${g && r.b ? `<b>${esc(r.b)}</b><small>${esc(r.p)}</small>` : esc(r.p)}</td>
        <td class="r num am">${esc(r.cur)} ${r.a == null ? "–" : MV.short(r.a)}</td><td class="r num us">${usd(r.usd)}</td><td class="st">${r.s === "Ongoing" ? "Under way" : r.s === "Completed" ? "Finished" : esc(r.s && r.s !== "NA" ? r.s : "–")}</td></tr>`).join("")
      + `</tbody>`;
    $("lendCount").innerHTML = `${fmt(rows.length)} ${rows.length === 1 ? "item" : "items"}, ${usd(rows.reduce((s, r) => s + (r.usd || 0), 0))}`;
    $("lendMore").hidden = rows.length <= 12; $("lendMore").textContent = all ? "Show fewer" : `Show all ${fmt(rows.length)}`;
  }

  document.addEventListener("click", e => {
    if (e.target.closest("#whatIn")) { e.preventDefault(); whatIn(); return; }
    if (e.target.closest("#lendBtn")) { toggle(); return; }
    const k = e.target.closest("[data-lk]"); if (k) { kind = k.dataset.lk; group = "all"; only = null; all = false; k.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === k)); document.querySelectorAll("[data-lg]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lg === "all")); draw(); return; }
    const gb = e.target.closest("[data-lg]"); if (gb) { group = gb.dataset.lg; only = null; gb.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === gb)); draw(); return; }
    const c = e.target.closest(".lb[data-c]"); if (c) { go("lender=" + encodeURIComponent(c.dataset.c)); return; }
    const s = e.target.closest("[data-sort]"); if (s) { if (sortBy === s.dataset.sort) desc = !desc; else { sortBy = s.dataset.sort; desc = sortBy !== "l"; } drawTable(); return; }
    if (e.target.closest("#lendMore")) { all = !all; drawTable(); return; }
    const mz = e.target.closest("[data-mz]"); if (mz) { mzoom = mz.dataset.mz; mz.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === mz)); drawMap(); return; }
    const mb = e.target.closest("[data-mb]"); if (mb) { mbasis = mb.dataset.mb; stopPlay(); document.querySelectorAll("#mapBasis [data-mb]").forEach(b => b.setAttribute("aria-pressed", b.dataset.mb === mbasis)); drawMap(); return; }
    if (e.target.closest("#mapPlay")) { if (playing) { stopPlay(); return; } if (mq >= QS().length - 1) mq = 0; $("mapPlay").textContent = "❚❚"; $("mapPlay").setAttribute("aria-label", "Pause");
      playing = setInterval(() => { if (mq >= QS().length - 1) { stopPlay(); return; } mq++; drawMap(); drawBul(); }, 650); drawMap(); drawBul(); return; }
    const ms = e.target.closest("[data-ms]"); if (ms) { mshow = ms.dataset.ms; ms.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === ms)); drawMap(); return; }
    const pl = e.target.closest("#lendMap [data-pl]"); if (pl) { stopPlay(); mpick = pl.dataset.pl; drawMap(); go("lender=" + encodeURIComponent(pl.dataset.pl)); return; }
    const pt = e.target.closest("[data-part]"); if (pt) { document.getElementById(pt.dataset.part)?.scrollIntoView({ behavior: "smooth", block: "start" }); return; }
    const bn = e.target.closest("[data-ben]"); if (bn) { go("borrower=" + encodeURIComponent(bn.dataset.ben)); return; }
    const who = e.target.closest("[data-who]"); if (who) { e.preventDefault(); go("lender=" + encodeURIComponent(who.dataset.who)); return; }
    const yr = e.target.closest("[data-yr]"); if (yr) { go(`signed=${yr.dataset.yr}-${kind}`); return; }
    if (e.target.closest(".sheet-back")) { back(); return; }
    const cp = e.target.closest("[data-copy]"); if (cp && sheetEl) { copy(cp, cp.dataset.copy === "cite" ? sheetEl._cite() : sheetEl._link); return; }
    const gq = e.target.closest("#lendSvc [data-q], #homeChart [data-q]"); if (gq) { const j = QS().indexOf(gq.dataset.q); if (j >= 0) { stopPlay(); mq = j; drawMap(); drawBul(); } return; }
    const qs = e.target.closest("[data-qs]"); if (qs) { stopPlay(); mq = Math.max(0, Math.min(QS().length - 1, mq + +qs.dataset.qs)); drawMap(); drawBul(); return; }
    const st = e.target.closest("[data-st]"); if (st) { status = st.dataset.st; all = false; st.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === st)); drawTable(); return; }
    if (e.target.closest("#oweCta")) { openPanel(true); return; }
    const av = e.target.closest("[data-asof]"); if (av) { e.preventDefault(); asof = av.dataset.asof; draw(); return; }
  });
  document.addEventListener("input", e => { if (e.target.id === "lendQ") { q = e.target.value.trim(); all = false; drawTable(); } });
  function stopPlay() { clearInterval(playing); playing = null; if ($("mapPlay")) { $("mapPlay").textContent = "▶"; $("mapPlay").setAttribute("aria-label", "Play the years"); } }
  document.addEventListener("input", e => { if (e.target.id === "mapQ") { stopPlay(); mq = +e.target.value; drawMap(); drawBul(); } });
  document.addEventListener("change", e => { if (e.target.id === "lendC") { only = e.target.value || null; all = false; drawTable(); } if (e.target.id === "lendAsof") { asof = e.target.value; draw(); } if (e.target.id === "mapInst") { minst = e.target.checked; drawMap(); } });
  document.addEventListener("keydown", e => { const n = e.target.closest?.("#lendMap .node, [data-yr]"); if (n && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); n.dispatchEvent(new MouseEvent("click", { bubbles: true })); } });
  document.querySelectorAll("[data-mz]").forEach(b => b.setAttribute("aria-pressed", b.dataset.mz === mzoom));
  if (/^#(lender|signed|borrower)=/.test(location.hash)) addEventListener("load", () => openPanel(false));   // a shared link to a lender or year
  MV.onPrefs?.(() => { draw(); drawBul(); });
  let rw = 0; addEventListener("resize", () => { if (L && Math.abs(innerWidth - rw) > 40) { rw = innerWidth; draw(); } });
})();
