/* Maldives National Debt Clock: every active external loan and sovereign guarantee (home page, "Who is the money owed to?").
   Reads lenders.json, built by build_lenders.py from the Ministry of Finance lists. Also the "What's in this number?" pop-up. */
(() => {
  const $ = id => document.getElementById(id);
  const { fmt } = MV;
  const usd = v => v == null ? "–" : "US$ " + MV.short(v);
  const day = d => d ? MV.dayLabel(d) : "–";
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const COL = { "Multilateral institutions": "#3fb8b0", China: "#ff5f56", India: "#f2a541", "Saudi Arabia": "#7ddc7a", "Bond holders": "#a98bd6",
    "United Arab Emirates": "#6fa8dc", Kuwait: "#e0a3c8", Japan: "#ff8a6b", Maldives: "#f4c95d", Oman: "#9fe0d6" };
  const colour = c => COL[c] || "#7f9aa5";
  let L = null, kind = "loans", group = "all", asof = null, only = null, q = "", sortBy = "d", desc = true, all = false;
  let onlyPl = null, W = null, mshow = "both", minst = true, mpick = null, mzoom = innerWidth < 700 ? "region" : "world";   // map: what to show, and the place picked
  let mbasis = "owed", mq = 0, playing = null;   // map: still owed (Debt Bulletins) or originally borrowed (Ministry lists), and which quarter
  const O = () => L?.owed, QS = () => O()?.quarters || [], qNow = () => QS()[mq];
  const qLabel = d => "End of " + MV.mLabel(d);
  const mvr = (v, d) => MV.moneyNow(v * 1e6, d);
  // what is still owed to each lender at a quarter, in the same shape as a list row
  function owedRows(k, d, home) {   // home: also guaranteed debt owed to banks in the Maldives (not on the map)
    const o = O(); if (!o) return [];
    const rate = o.rate[d] || 15.42, row = ([l, v]) => { const w = o.who[l] || {}; return { l, c: w.c, pl: w.pl, m: v[d], usd: v[d] * 1e6 / rate }; };
    const ext = Object.entries(o[k] || {}).filter(([, v]) => v[d] > 0).map(row);
    return home && k === "guarantees" ? ext.concat(Object.entries(o.guarantees_home || {}).filter(([, v]) => v[d] > 0).map(row)) : ext;
  }
  const KC = { loans: "#3fb8b0", guarantees: "#f2a541" }, KW = { loans: "loan", guarantees: "guarantee" };

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
      const r = (3 + 7 * Math.sqrt((n.lu + n.gu) / maxT)) * px, col = n.lu && n.gu ? "#fff" : n.lu ? KC.loans : KC.guarantees;
      const mark = n.kind === "institution"
        ? `<rect x="${(n.x - r).toFixed(1)}" y="${(n.y - r).toFixed(1)}" width="${(2 * r).toFixed(1)}" height="${(2 * r).toFixed(1)}" rx="${(r * .3).toFixed(1)}" transform="rotate(45 ${n.x.toFixed(1)} ${n.y.toFixed(1)})" fill="${col}"/>`
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
    box.innerHTML = `<svg viewBox="${vb.map(v => v.toFixed(1)).join(" ")}" role="img" aria-label="Map of where the Maldives' external loans and guaranteed loans come from">${g}</svg>`;
    // the quarter, and the totals at that quarter
    const owed = mbasis === "owed" && O();
    $("mapTime").hidden = !owed;
    $("mapBasis").hidden = !O();
    if (owed) {
      const d = qNow(), sum = k => owedRows(k, d).reduce((s, r) => s + r.m, 0);
      $("mapQ").max = QS().length - 1; $("mapQ").value = mq; $("mapQl").textContent = qLabel(d);
      $("mapTot").innerHTML = `Still owed abroad: <b>${mvr(sum("loans"), d)}</b> by the government, <b>${mvr(sum("guarantees"), d)}</b> by others with a government guarantee. Press ▶ to watch it change since ${MV.mLabel(QS()[0])}.`;
    } else $("mapTot").innerHTML = O() ? `What was originally borrowed or guaranteed, for every loan and guarantee on the Ministry's lists as of ${day(asof)}, whether or not it has since been repaid.` : "";
    // not on the map
    const off = {};
    kinds.forEach(k => rowsAll(k).forEach(r => { if (!r.pl || !P[r.pl] || (!minst && P[r.pl].kind === "institution")) { const key = r.pl && P[r.pl] ? "Development banks and funds (hidden)" : (r.c === "Maldives" ? "Maldivian banks" : r.l); (off[key] = off[key] || { loans: [], guarantees: [] })[k].push(r); } }));
    $("mapOff").innerHTML = Object.keys(off).length ? "<b>Not on the map:</b> " + Object.entries(off).map(([k, v]) => `${esc(k)}, ` + ["loans", "guarantees"].filter(x => v[x].length).map(x => owed ? `${mvr(v[x].reduce((s, r) => s + r.m, 0), qNow())} still owed in ${KW[x]}s` : `${usd(v[x].reduce((s, r) => s + (r.usd || 0), 0))} in ${KW[x]}s (${curMix(v[x])})`).join(" and ")).join("; ") + "." : "";
    drawCard(nodes);
  }
  function spark(pl) {   // what this place was owed, quarter by quarter
    const qs = QS(), ks = mshow === "both" ? ["loans", "guarantees"] : [mshow];
    const ser = ks.map(k => qs.map(d => owedRows(k, d).filter(r => r.pl === pl).reduce((s, r) => s + r.m, 0)));
    const top = Math.max(1, ...qs.map((_, i) => ser.reduce((s, a) => s + a[i], 0))), w = 300, h = 46, x = i => i / (qs.length - 1) * w;
    let base = qs.map(() => 0);
    const areas = ser.map((a, j) => { const lo = base.slice(), hi = base.map((b, i) => b + a[i]); base = hi;
      return `<path d="M${hi.map((v, i) => `${x(i).toFixed(1)} ${(h - v / top * (h - 4)).toFixed(1)}`).join(" L")} L${lo.map((v, i) => `${x(i).toFixed(1)} ${(h - v / top * (h - 4)).toFixed(1)}`).reverse().join(" L")} Z" fill="${KC[ks[j]]}" opacity=".75"/>`; }).join("");
    return `<div class="mc-spark"><svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true">${areas}<line x1="${x(mq)}" x2="${x(mq)}" y1="0" y2="${h}" stroke="#fff" stroke-width="1.5"/></svg><div class="mc-row"><span>${MV.mLabel(qs[0])}</span><span>${MV.mLabel(qs[qs.length - 1])}</span></div></div>`;
  }
  function drawCard(nodes) {
    const n = nodes?.[mpick];
    if (!n) { $("mapCard").innerHTML = `<p class="hint">${mbasis === "owed" && O() ? "Tap a country, a development bank or a line to see what is still owed to it, and how that has changed since " + MV.mLabel(QS()[0]) + "." : "Tap a country, a development bank or a line to see what it lent or guaranteed, in US dollars and in the original currencies."}</p>`; return; }
    if (mbasis === "owed" && O()) {
      const d = qNow(), part = k => { const rs = n[k].slice().sort((a, b) => b.m - a.m); if (!rs.length) return "";
        return `<div class="mc-k" style="--kc:${KC[k]}"><span class="mc-h">${k === "loans" ? "Owed by the government" : "Owed by others, guaranteed by the government"}</span>
          <b class="num">${mvr(rs.reduce((s, r) => s + r.m, 0), d)}</b>${rs.map(r => `<span class="mc-row"><span>${esc(r.l)}</span><b>${mvr(r.m, d)}</b></span>`).join("")}
          <button type="button" class="pill mc-go" data-go="${k}">List the ${KW[k]}s signed</button></div>`; };
      $("mapCard").innerHTML = `<div class="mc-t">${esc(n.kind === "institution" ? `${n.key}` : n.label)}<small>${qLabel(d)}${n.city ? `, ${esc(n.city)}` : ""}</small><button type="button" class="mc-x" aria-label="Close">×</button></div><div class="mc-b">${part("loans")}${part("guarantees")}</div>${spark(n.key)}`;
      return;
    }
    const part = k => { const rs = n[k]; if (!rs.length) return "";
      const lenders = [...new Set(rs.map(r => r.l))];
      return `<div class="mc-k" style="--kc:${KC[k]}"><span class="mc-h">${k === "loans" ? "Loans to the government" : "Loans the government guaranteed"}</span>
        <b class="num">${usd(rs.reduce((s, r) => s + (r.usd || 0), 0))}</b><span class="mc-n">${rs.length} ${KW[k]}${rs.length > 1 ? "s" : ""}, in ${esc(curMix(rs))}</span>
        <span class="mc-l">${lenders.slice(0, 4).map(esc).join(", ")}${lenders.length > 4 ? ` and ${lenders.length - 4} more` : ""}</span>
        <button type="button" class="pill mc-go" data-go="${k}">List them below</button></div>`; };
    $("mapCard").innerHTML = `<div class="mc-t">${esc(n.kind === "institution" ? `${n.key}` : n.label)}${n.city ? `<small>${esc(n.city)}</small>` : ""}<button type="button" class="mc-x" aria-label="Close">×</button></div><div class="mc-b">${part("loans")}${part("guarantees")}</div>`;
  }

  // ---------- from the Debt Bulletins: repayments, money still to come, loans passed on ----------
  function drawBul() {
    const o = O(); $("lendBul").hidden = !o; if (!o) return;
    const S = o.service, qs = Object.keys(S).sort(), last = o.latest, tot = d => ["gp", "gi", "sp", "si"].reduce((a, k) => a + (S[d][k] || 0), 0);
    const yr = qs.slice(-4), sum = k => yr.reduce((a, d) => a + (S[d][k] || 0), 0);
    // the biggest repayments in the latest quarter: lenders owed much less than three months before
    const prev = o.quarters[o.quarters.length - 2], drops = [];
    ["loans", "guarantees"].forEach(k => Object.entries(o[k]).forEach(([l, v]) => { const dlt = (v[prev] || 0) - (v[last] || 0); if (dlt > 300) drops.push([l, dlt]); }));
    drops.sort((a, b) => b[1] - a[1]);
    const peak = qs.reduce((a, d) => tot(d) > tot(a) ? d : a, qs[0]);
    $("svcNote").innerHTML = `Every three months the government pays back part of what it owes, and pays interest. Over the four quarters to ${MV.mLabel(last)} it paid <b>${mvr(sum("gp"), last)}</b> in repayments and <b>${mvr(sum("gi"), last)}</b> in interest. `
      + `State companies and others paid <b>${mvr(sum("sp") + sum("si"), last)}</b> on the debt the government guaranteed for them, <b>${mvr(sum("si"), last)}</b> of it interest: that interest is not in the clock's <i>interest accrued</i>, as the government doesn't pay it.`
      + (peak ? ` The biggest quarter was ${MV.mLabel(peak)}, ${mvr(tot(peak), peak)}` + (peak === last && drops.length ? `. What was owed fell most for ${drops.slice(0, 2).map(([l, v]) => `${esc(l)} (down ${mvr(v, last)})`).join(" and ")}.` : ".") : "");
    const Wd = Math.max(300, $("lendSvc").clientWidth || 640), Hh = 150, bw = (Wd - 30) / qs.length, top = Math.max(...qs.map(tot), 1);
    const COLS = { gp: "#3fb8b0", gi: "#9fe0d6", sp: "#f2a541", si: "#f8d49b" }, NAMES = { gp: "government repayments", gi: "government interest", sp: "guaranteed repayments", si: "guaranteed interest" };
    $("lendSvc").innerHTML = `<svg viewBox="0 0 ${Wd} ${Hh + 22}" role="img" aria-label="Repayments and interest each quarter">`
      + qs.map((d, i) => { let y = Hh; return ["gp", "gi", "sp", "si"].map(k => { const h = (S[d][k] || 0) / top * Hh; y -= h;
          return `<rect x="${(15 + i * bw + 1).toFixed(1)}" y="${y.toFixed(1)}" width="${Math.max(1, bw - 2).toFixed(1)}" height="${h.toFixed(1)}" fill="${COLS[k]}"><title>${MV.mLabel(d)}: ${NAMES[k]} ${mvr(S[d][k] || 0, d)}</title></rect>`; }).join(""); }).join("")
      + qs.map((d, i) => d.endsWith("03-31") && (bw > 14 || d.slice(0, 4) % 2 === 0) ? `<text x="${(15 + i * bw).toFixed(1)}" text-anchor="start" y="${Hh + 16}">${d.slice(0, 4)}</text>` : "").join("")
      + `<line x1="15" x2="${Wd - 15}" y1="${Hh}" y2="${Hh}" stroke="rgba(169,205,214,.3)"/></svg><p class="hint">Each bar is three months. Tap or hover a bar for its figures.</p>`;
    // still to come, and passed on
    const cub = Object.entries(o.cub).sort((a, b) => b[1] - a[1]), sub = Object.entries(o.subsidiary).sort((a, b) => b[1] - a[1]);
    const t = a => a.reduce((s, [, v]) => s + v, 0), list = a => a.slice(0, 3).map(([n, v]) => `${esc(n.replace(/ (Limited|Ltd|PLC|Private Limited)$/, ""))} ${mvr(v, last)}`).join(", ");
    $("lendExtra").innerHTML = (cub.length ? `<div><b class="num">${mvr(t(cub), last)}</b><span>agreed with lenders abroad but not yet paid out, at the end of ${MV.mLabel(last)}. It becomes debt as it is drawn.</span><small>Largest: ${list(cub)}</small></div>` : "")
      + (sub.length ? `<div><b class="num">${mvr(t(sub), last)}</b><span>borrowed by the government and lent on to state companies, which repay it to the government.</span><small>Largest: ${list(sub)}</small></div>` : "");
    // guaranteed for whom
    const ben = Object.entries(o.guaranteed_for).map(([n, v]) => [n, (v.ext || 0) + (v.dom || 0), v]).sort((a, b) => b[1] - a[1]), bm = ben[0]?.[1] || 1;
    $("lendFor").innerHTML = ben.map(([n, v, p]) => `<div class="lb" role="img" aria-label="${esc(n)}: ${mvr(v, last)}"><span class="n">${esc(n.replace(/ (Limited|Ltd|PLC|Private Limited|Pvt Ltd)$/, ""))}</span><span class="t"><i style="width:${v / bm * 100}%;background:#f2a541"></i></span><span class="v num">${mvr(v, last)}${p.dom ? `<small>${p.ext ? `${mvr(p.dom, last)} of it` : "all"} at home</small>` : ""}</span></div>`).join("")
      + `<p class="hint">Still owed at the end of ${MV.mLabel(last)}. The Maldives Monetary Authority's is the currency swap with the Reserve Bank of India.</p>`;
    $("bulSrc").innerHTML = `Source: Ministry of Finance, <a href="${esc(o.sources[o.sources.length - 1].url || "https://www.finance.gov.mv/publications/reports-and-analyses/quarterly-debt-bulletin")}" target="_blank" rel="noopener">Quarterly Debt Bulletin, ${MV.mLabel(last)}</a>, and earlier bulletins back to ${MV.mLabel(o.quarters[0])}. Where a later bulletin revised a quarter, the later figure is used.`;
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
      <p>The clock counts all public debt, the standard measure: what the government owes itself, plus what it has guaranteed for others. Official figures at the end of ${MV.mLabel(tot.date)}:</p>
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
    $("lendBtn").querySelector(".t").textContent = open ? "Hide the loans and guarantees" : "See every external loan and sovereign guarantee";
    if (open && !L) Promise.all([MV.getJSON("lenders.json"), MV.getJSON("assets/worldmap.json").catch(() => null)]).then(([j, w]) => { L = j; W = w; asof = j.versions[j.versions.length - 1]; mbasis = j.owed ? "owed" : "signed"; mq = Math.max(0, QS().length - 1); draw(); drawBul(); })
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
      ? `Every external loan the government still has on its books, as the Ministry of Finance lists them, as of <b>${day(asof)}</b>. Amounts are <b>what was originally borrowed</b>, not what is still owed: many have been partly repaid.`
      : `Every loan the government has guaranteed for others, as the Ministry of Finance lists them, as of <b>${day(asof)}</b>. If the borrower can't repay, the government has promised to. Amounts are <b>what was originally guaranteed</b>, not what is still owed.`;
    history(rows, word);
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
    $("lendBars").innerHTML = groups.map(([c, v]) => `<button type="button" class="lb${only === c ? " on" : ""}" data-c="${esc(c)}" aria-pressed="${only === c}">
      <span class="n">${esc(c)}</span><span class="t">${hasOw ? `<i class="f" style="width:${v / max * 100}%;background:${colour(c)}"></i><i style="width:${(ow[c] || 0) / max * 100}%;background:${colour(c)}"></i>` : `<i style="width:${v / max * 100}%;background:${colour(c)}"></i>`}</span>
      <span class="v num">${hasOw ? `${none(ow[c] || 0)}<small>of ${none(v)}</small>` : usd(v)}</span></button>`).join("")
      + `<p class="hint">${hasOw ? `Solid: still owed at the end of ${MV.mLabel(oq)}, from the Debt Bulletin. Faint: originally ${kind === "loans" ? "borrowed" : "guaranteed"}, from the Ministry's list. ` : ""}Tap a lender to list only its ${word}s.${only ? ` <a href="#" id="lendAll">Show all lenders</a>` : ""}</p>`;
    // signed each year
    const yrs = {}; rows.forEach(r => { if (r.d) { const y = r.d.slice(0, 4); yrs[y] = (yrs[y] || 0) + (r.usd || 0); } });
    const ys = Object.keys(yrs).sort(), y0 = +ys[0], y1 = +ys[ys.length - 1], ym = Math.max(...Object.values(yrs), 1);
    const W = Math.max(300, $("lendYears").clientWidth || 640), Hh = 140, bw = (W - 40) / (y1 - y0 + 1), step = W < 500 ? 10 : 5;
    $("lendYears").innerHTML = ys.length ? `<svg viewBox="0 0 ${W} ${Hh + 22}" role="img" aria-label="${word}s signed each year, in US dollars">`
      + ys.map(y => { const h = yrs[y] / ym * Hh; return `<rect x="${20 + (y - y0) * bw + 1}" y="${Hh - h}" width="${Math.max(1, bw - 2)}" height="${h}" fill="#3fb8b0"><title>${y}: ${usd(yrs[y])}</title></rect>`; }).join("")
      + Array.from({ length: y1 - y0 + 1 }, (_, i) => y0 + i).filter(y => y % step === 0).map(y => `<text x="${20 + (y - y0 + .5) * bw}" y="${Hh + 16}" text-anchor="middle">${y}</text>`).join("")
      + `<line x1="20" x2="${W - 20}" y1="${Hh}" y2="${Hh}" stroke="rgba(169,205,214,.3)"/></svg><p class="hint">Highest year: ${Object.entries(yrs).sort((a, b) => b[1] - a[1])[0][0]}, ${usd(ym)}. Tap or hover a bar for its year.</p>` : "";
    drawTable(); drawMap();
    // exchange rates
    const fx = L.fx[asof] || {}, cur = [...new Set(rowsNow().map(r => r.cur))].sort();
    $("lendFx").innerHTML = `<p>Each amount is converted to US dollars at the rate on <b>${day(fx.rate_date || fx.date)}</b>${(fx.rate_date || fx.date) === fx.date ? ", the date of the Ministry's list" : `, the last month-end before the Ministry's list of ${day(fx.date)}`}, so all ${word}s are compared at the same rates.</p><ul>`
      + cur.map(c => `<li><b>${c}</b> ${c === "USD" ? "US dollar" : `${fmt(fx.per_usd?.[c], fx.per_usd?.[c] < 10 ? 4 : 2)} per US dollar${fx.notes?.[c] ? `, ${fx.notes[c]}` : ""}`}${c === "XDR" ? " (the IMF's Special Drawing Right, used by IDA, IFAD and others)" : ""}</li>`).join("")
      + `</ul><p class="hint">${esc(fx.source || "")}.</p>`;
  }
  // each list the Ministry publishes is kept: an older one stays here as history when a new one comes in
  function history(rows, word) {
    const ks = Object.keys(L.lists[kind]).sort(), i = ks.indexOf(asof), latest = ks[ks.length - 1], el = $("lendHist");
    if (!el) return;
    if (ks.length < 2) { el.innerHTML = `This is the first ${word} list saved here. When the Ministry of Finance publishes a new one, this list will be kept as history: pick its date under <b>As of</b> to see it again.`; return; }
    const key = r => [r.l, r.d, r.cur, r.a, r.b].join("|"), sum = a => a.reduce((s, r) => s + (r.usd || 0), 0);
    let t = asof !== latest ? `This is an older list. <a href="#" data-asof="${latest}">See the latest, ${day(latest)}</a>. ` : "";
    if (i > 0) {
      const prev = (L.lists[kind][ks[i - 1]] || []).filter(r => group === "all" || r.g === group), was = new Set(prev.map(key)), now = new Set(rows.map(key));
      const added = rows.filter(r => !was.has(key(r))), gone = prev.filter(r => !now.has(key(r)));
      t += `Since the list of ${day(ks[i - 1])}: <b>${fmt(added.length)}</b> added${added.length ? ` (${esc([...new Set(added.map(r => r.l))].slice(0, 3).join(", "))}${added.length > 3 ? "…" : ""})` : ""}, <b>${fmt(gone.length)}</b> no longer listed. Total ${usd(sum(prev))} then, ${usd(sum(rows))} now.`;
    } else t += `This is the oldest list saved here.`;
    el.innerHTML = t;
  }
  // a lender the latest Debt Bulletin lists with nothing owed (and no other amount owed to it)
  function paid(l) {
    const o = O(); if (!o) return false;
    const vs = ["loans", "guarantees", "guarantees_home"].map(k => (o[k] || {})[l]).filter(Boolean);
    return vs.length > 0 && vs.every(v => !(v[o.latest] > 0));
  }
  function drawTable() {
    let rows = rowsNow().filter(r => (!only || r.c === only) && (!onlyPl || r.pl === onlyPl));
    if (q) { const k = q.toLowerCase(); rows = rows.filter(r => [r.l, r.c, r.p, r.b, r.cur, r.d].some(x => String(x || "").toLowerCase().includes(k))); }
    const val = r => sortBy === "usd" ? (r.usd || 0) : sortBy === "l" ? r.l : (r.d || "");
    rows.sort((a, b) => (val(a) < val(b) ? -1 : val(a) > val(b) ? 1 : 0) * (desc ? -1 : 1));
    const show = all ? rows : rows.slice(0, 12), g = kind === "guarantees";
    const th = (k, t) => `<th${k ? ` data-sort="${k}" aria-sort="${sortBy === k ? (desc ? "descending" : "ascending") : "none"}"` : ""}>${t}${sortBy === k ? (desc ? " ↓" : " ↑") : ""}</th>`;
    $("lendTbl").innerHTML = `<thead><tr>${th("d", "Signed")}${th("l", "Lender")}<th>${g ? "For whom, and what" : "What for"}</th><th class="r">Amount</th>${th("usd", "In US$")}<th class="st">Status</th></tr></thead><tbody>`
      + show.map(r => `<tr><td class="num sg">${r.d ? r.d.slice(0, 4) : "–"}<small>${r.d ? MV.dayLabel(r.d).replace(/ \d{4}$/, "") : ""}</small></td>
        <td>${esc(r.l)}${paid(r.l) ? `<span class="lend-flag" title="The Debt Bulletin for ${MV.mLabel(O().latest)} shows nothing owed to this lender">nothing owed now</span>` : ""}<small>${esc(r.c)}</small></td>
        <td>${g && r.b ? `<b>${esc(r.b)}</b><small>${esc(r.p)}</small>` : esc(r.p)}</td>
        <td class="r num am">${esc(r.cur)} ${r.a == null ? "–" : MV.short(r.a)}</td><td class="r num us">${usd(r.usd)}</td><td class="st">${esc(r.s && r.s !== "NA" ? r.s : "–")}</td></tr>`).join("")
      + `</tbody>`;
    $("lendCount").innerHTML = `${fmt(rows.length)} ${rows.length === 1 ? "item" : "items"}${only ? ` from ${esc(only)}` : ""}${onlyPl ? ` from ${esc(L.places[onlyPl]?.kind === "institution" ? onlyPl : L.places[onlyPl]?.label || onlyPl)} <a href="#" id="lendAllPl">show all</a>` : ""}`;
    $("lendMore").hidden = rows.length <= 12; $("lendMore").textContent = all ? "Show fewer" : `Show all ${fmt(rows.length)}`;
  }

  document.addEventListener("click", e => {
    if (e.target.closest("#whatIn")) { e.preventDefault(); whatIn(); return; }
    if (e.target.closest("#lendBtn")) { toggle(); return; }
    const k = e.target.closest("[data-lk]"); if (k) { kind = k.dataset.lk; group = "all"; only = null; all = false; k.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === k)); document.querySelectorAll("[data-lg]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lg === "all")); draw(); return; }
    const gb = e.target.closest("[data-lg]"); if (gb) { group = gb.dataset.lg; only = null; gb.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === gb)); draw(); return; }
    const c = e.target.closest(".lb"); if (c) { only = only === c.dataset.c ? null : c.dataset.c; all = false; draw(); return; }
    if (e.target.closest("#lendAll")) { e.preventDefault(); only = null; draw(); return; }
    const s = e.target.closest("[data-sort]"); if (s) { if (sortBy === s.dataset.sort) desc = !desc; else { sortBy = s.dataset.sort; desc = sortBy !== "l"; } drawTable(); return; }
    if (e.target.closest("#lendMore")) { all = !all; drawTable(); return; }
    const mz = e.target.closest("[data-mz]"); if (mz) { mzoom = mz.dataset.mz; mz.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === mz)); drawMap(); return; }
    const mb = e.target.closest("[data-mb]"); if (mb) { mbasis = mb.dataset.mb; stopPlay(); mb.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === mb)); drawMap(); return; }
    if (e.target.closest("#mapPlay")) { if (playing) { stopPlay(); return; } if (mq >= QS().length - 1) mq = 0; $("mapPlay").textContent = "❚❚"; $("mapPlay").setAttribute("aria-label", "Pause");
      playing = setInterval(() => { if (mq >= QS().length - 1) { stopPlay(); return; } mq++; drawMap(); }, 650); drawMap(); return; }
    const ms = e.target.closest("[data-ms]"); if (ms) { mshow = ms.dataset.ms; ms.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === ms)); drawMap(); return; }
    const pl = e.target.closest("#lendMap [data-pl]"); if (pl) { mpick = mpick === pl.dataset.pl ? null : pl.dataset.pl; drawMap(); return; }
    if (e.target.closest(".mc-x")) { mpick = null; drawMap(); return; }
    const go = e.target.closest("[data-go]"); if (go) { const k = go.dataset.go; kind = k; group = "all"; only = null; onlyPl = mpick; all = true;
      document.querySelectorAll("[data-lk]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lk === k)); document.querySelectorAll("[data-lg]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lg === "all"));
      draw(); $("lendQ").scrollIntoView({ behavior: "smooth", block: "center" }); return; }
    const av = e.target.closest("[data-asof]"); if (av) { e.preventDefault(); asof = av.dataset.asof; draw(); return; }
    if (e.target.closest("#lendAllPl")) { e.preventDefault(); onlyPl = null; drawTable(); }
  });
  document.addEventListener("input", e => { if (e.target.id === "lendQ") { q = e.target.value.trim(); all = false; drawTable(); } });
  function stopPlay() { clearInterval(playing); playing = null; if ($("mapPlay")) { $("mapPlay").textContent = "▶"; $("mapPlay").setAttribute("aria-label", "Play the years"); } }
  document.addEventListener("input", e => { if (e.target.id === "mapQ") { stopPlay(); mq = +e.target.value; drawMap(); } });
  document.addEventListener("change", e => { if (e.target.id === "lendAsof") { asof = e.target.value; draw(); } if (e.target.id === "mapInst") { minst = e.target.checked; drawMap(); } });
  document.addEventListener("keydown", e => { const n = e.target.closest?.("#lendMap .node"); if (n && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); n.dispatchEvent(new MouseEvent("click", { bubbles: true })); } });
  document.querySelectorAll("[data-mz]").forEach(b => b.setAttribute("aria-pressed", b.dataset.mz === mzoom));
  MV.onPrefs?.(() => { draw(); drawBul(); });
  let rw = 0; addEventListener("resize", () => { if (L && Math.abs(innerWidth - rw) > 40) { rw = innerWidth; draw(); } });
})();
