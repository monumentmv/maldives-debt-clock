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
  const KC = { loans: "#3fb8b0", guarantees: "#f2a541" }, KW = { loans: "loan", guarantees: "guarantee" };

  // ---------- the map: every lender, with a line to Malé, thicker for more money ----------
  function rowsAll(k) { const v = L.lists[k], a = v[asof] ? asof : Object.keys(v).sort().pop(); return v[a] || []; }
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
    const max = Math.max(1, ...list.map(n => Math.max(n.lu, n.gu))), maxT = Math.max(1, ...list.map(n => n.lu + n.gu));
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
      const cx = (n.x + mx) / 2 + nx * bend, cy = (n.y + my) / 2 + ny * bend, w = (.9 + 4 * Math.sqrt(v / max)) * px;
      return `<path class="arc ${k}${mpick && mpick !== n.key ? " dim" : ""}" data-pl="${esc(n.key)}" d="M${n.x.toFixed(1)} ${n.y.toFixed(1)} Q${cx.toFixed(1)} ${cy.toFixed(1)} ${mx.toFixed(1)} ${my.toFixed(1)}" style="stroke-width:${w.toFixed(2)};stroke-dasharray:${(6 * px).toFixed(1)} ${(5 * px).toFixed(1)}"><title>${esc(n.label)}: ${usd(v)} in ${KW[k]}s</title></path>`;
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
    // not on the map
    const off = {};
    kinds.forEach(k => rowsAll(k).forEach(r => { if (!r.pl || !P[r.pl] || (!minst && P[r.pl].kind === "institution")) { const key = r.pl && P[r.pl] ? "Development banks and funds (hidden)" : (r.c === "Maldives" ? "Maldivian banks" : r.l); (off[key] = off[key] || { loans: [], guarantees: [] })[k].push(r); } }));
    $("mapOff").innerHTML = Object.keys(off).length ? "<b>Not on the map:</b> " + Object.entries(off).map(([k, v]) => `${esc(k)}, ` + ["loans", "guarantees"].filter(x => v[x].length).map(x => `${usd(v[x].reduce((s, r) => s + (r.usd || 0), 0))} in ${KW[x]}s (${curMix(v[x])})`).join(" and ")).join("; ") + "." : "";
    drawCard(nodes);
  }
  function drawCard(nodes) {
    const n = nodes?.[mpick];
    if (!n) { $("mapCard").innerHTML = `<p class="hint">Tap a country, a development bank or a line to see what it lent or guaranteed, in US dollars and in the original currencies.</p>`; return; }
    const part = k => { const rs = n[k]; if (!rs.length) return "";
      const lenders = [...new Set(rs.map(r => r.l))];
      return `<div class="mc-k" style="--kc:${KC[k]}"><span class="mc-h">${k === "loans" ? "Loans to the government" : "Loans the government guaranteed"}</span>
        <b class="num">${usd(rs.reduce((s, r) => s + (r.usd || 0), 0))}</b><span class="mc-n">${rs.length} ${KW[k]}${rs.length > 1 ? "s" : ""}, in ${esc(curMix(rs))}</span>
        <span class="mc-l">${lenders.slice(0, 4).map(esc).join(", ")}${lenders.length > 4 ? ` and ${lenders.length - 4} more` : ""}</span>
        <button type="button" class="pill mc-go" data-go="${k}">List them below</button></div>`; };
    $("mapCard").innerHTML = `<div class="mc-t">${esc(n.kind === "institution" ? `${n.key}` : n.label)}${n.city ? `<small>${esc(n.city)}</small>` : ""}<button type="button" class="mc-x" aria-label="Close">×</button></div><div class="mc-b">${part("loans")}${part("guarantees")}</div>`;
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
    if (open && !L) Promise.all([MV.getJSON("lenders.json"), MV.getJSON("assets/worldmap.json").catch(() => null)]).then(([j, w]) => { L = j; W = w; asof = j.versions[j.versions.length - 1]; draw(); })
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
    // summary
    const by = {}; rows.forEach(r => { by[r.c] = (by[r.c] || 0) + (r.usd || 0); });
    const groups = Object.entries(by).sort((a, b) => b[1] - a[1]);
    $("lendSum").innerHTML = `<div><b class="num">${fmt(rows.length)}</b><span>${word}s${open ? `, ${fmt(open)} still being carried out` : ""}</span></div>`
      + `<div><b class="num">${usd(tot)}</b><span>${kind === "loans" ? "borrowed" : "guaranteed"} in all, in US dollars</span></div>`
      + (groups[0] ? `<div><b>${esc(groups[0][0])}</b><span>the largest source, ${fmt(groups[0][1] / tot * 100, 0)}%</span></div>` : "");
    // by lender
    const max = groups[0]?.[1] || 1;
    $("lendBars").innerHTML = groups.map(([c, v]) => `<button type="button" class="lb${only === c ? " on" : ""}" data-c="${esc(c)}" aria-pressed="${only === c}">
      <span class="n">${esc(c)}</span><span class="t"><i style="width:${v / max * 100}%;background:${colour(c)}"></i></span><span class="v num">${usd(v)}</span></button>`).join("")
      + `<p class="hint">Tap a lender to list only its ${word}s.${only ? ` <a href="#" id="lendAll">Show all lenders</a>` : ""}</p>`;
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
    $("lendFx").innerHTML = `<p>Each amount is converted to US dollars at the rate on <b>${day(fx.date)}</b>, the date of the Ministry's list, so all ${word}s are compared at the same rates.</p><ul>`
      + cur.map(c => `<li><b>${c}</b> ${c === "USD" ? "US dollar" : `${fmt(fx.per_usd?.[c], fx.per_usd?.[c] < 10 ? 4 : 2)} per US dollar${fx.notes?.[c] ? `, ${fx.notes[c]}` : ""}`}${c === "XDR" ? " (the IMF's Special Drawing Right, used by IDA, IFAD and others)" : ""}</li>`).join("")
      + `</ul><p class="hint">${esc(fx.source || "")}. The rufiyaa rate is MMA's reference rate.</p>`;
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
        <td>${esc(r.l)}<small>${esc(r.c)}</small></td>
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
    const ms = e.target.closest("[data-ms]"); if (ms) { mshow = ms.dataset.ms; ms.parentElement.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === ms)); drawMap(); return; }
    const pl = e.target.closest("#lendMap [data-pl]"); if (pl) { mpick = mpick === pl.dataset.pl ? null : pl.dataset.pl; drawMap(); return; }
    if (e.target.closest(".mc-x")) { mpick = null; drawMap(); return; }
    const go = e.target.closest("[data-go]"); if (go) { const k = go.dataset.go; kind = k; group = "all"; only = null; onlyPl = mpick; all = true;
      document.querySelectorAll("[data-lk]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lk === k)); document.querySelectorAll("[data-lg]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lg === "all"));
      draw(); $("lendQ").scrollIntoView({ behavior: "smooth", block: "center" }); return; }
    if (e.target.closest("#lendAllPl")) { e.preventDefault(); onlyPl = null; drawTable(); }
  });
  document.addEventListener("input", e => { if (e.target.id === "lendQ") { q = e.target.value.trim(); all = false; drawTable(); } });
  document.addEventListener("change", e => { if (e.target.id === "lendAsof") { asof = e.target.value; draw(); } if (e.target.id === "mapInst") { minst = e.target.checked; drawMap(); } });
  document.addEventListener("keydown", e => { const n = e.target.closest?.("#lendMap .node"); if (n && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); n.dispatchEvent(new MouseEvent("click", { bubbles: true })); } });
  document.querySelectorAll("[data-mz]").forEach(b => b.setAttribute("aria-pressed", b.dataset.mz === mzoom));
  MV.onPrefs?.(() => draw());
  let rw = 0; addEventListener("resize", () => { if (L && Math.abs(innerWidth - rw) > 40) { rw = innerWidth; draw(); } });
})();
