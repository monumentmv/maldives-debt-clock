/* Maldives National Debt Clock: shared code for every page */
const MV = (() => {
  const SEC_YEAR = 365.25 * 86400;
  const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  const MON = MONTHS.map(m => m.slice(0, 3));

  // ---------- preferences (currency, inflation adjustment) ----------
  const state = { cur: "MVR", real: false };
  try {
    const q = new URLSearchParams(location.search);
    state.cur = (q.get("cur") || localStorage.getItem("cur") || "MVR").toUpperCase() === "USD" ? "USD" : "MVR";
    state.real = (q.get("real") ?? localStorage.getItem("real")) === "1";
  } catch (e) {}

  // ---------- data-dependent helpers ----------
  let fx = [], cpi = [], USD = 15.42, cpiLast = null;
  function setData(S) {
    fx = (S.usd_rate?.points || []).filter(p => p.value > 0);
    if (fx.length) USD = fx[fx.length - 1].value;
    cpi = (S.cpi?.points || []).filter(p => p.value > 0);
    cpiLast = cpi.length ? cpi[cpi.length - 1] : null;
    if (!cpi.length) document.querySelectorAll('[data-pref="real"]').forEach(t => t.hidden = true);
  }
  const lastBefore = (arr, date) => { let r = null; for (const p of arr) { if (p.date <= date) r = p; else break; } return r; };
  const rateAt = date => (lastBefore(fx, date) || fx[0] || { value: USD }).value;
  const cpiAt = date => (lastBefore(cpi, date) || null)?.value;
  /** multiply a past rufiyaa amount by this to express it in today's prices */
  const realFactor = date => {
    if (!state.real || !cpiLast || !date) return 1;
    const c = cpiAt(date); return c ? cpiLast.value / c : 1;
  };
  /** convert a rufiyaa amount recorded at `date` into what the visitor asked to see */
  const conv = (mvr, date) => {
    const v = mvr * realFactor(date);
    if (state.cur !== "USD") return v;
    return v / (state.real || !date ? USD : rateAt(date));
  };
  /** for series recorded in US dollars (fuel): convert to rufiyaa at that month's rate if needed */
  const fromUSD = (usd, date) => state.cur === "USD" ? usd : usd * (date ? rateAt(date) : USD);

  // ---------- formatting ----------
  const fmt = (n, d = 0) => Number(n).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  const sym = () => state.cur === "USD" ? "US$" : "MVR";
  const short = n => { const a = Math.abs(n);
    if (a >= 1e9) return fmt(n / 1e9, 1) + " bn";
    if (a >= 1e6) return fmt(n / 1e6, 1) + " m";
    if (a >= 1e4) return fmt(n);
    return fmt(n, a < 10 ? 2 : 0); };
  const money = (mvr, date) => sym() + " " + short(conv(mvr, date));
  const moneyFull = (mvr, d = 0, date) => sym() + " " + fmt(conv(mvr, date), d);
  const ts = d => new Date(d + "T23:59:59Z").getTime();
  const dt = d => new Date(d);
  const mLabel = d => MONTHS[dt(d).getUTCMonth()] + " " + dt(d).getUTCFullYear();
  const mShort = d => MON[dt(d).getUTCMonth()] + " " + dt(d).getUTCFullYear();
  const qLabel = d => "Q" + (Math.floor(dt(d).getUTCMonth() / 3) + 1) + " " + dt(d).getUTCFullYear();
  const dayLabel = d => dt(d).getUTCDate() + " " + MONTHS[dt(d).getUTCMonth()] + " " + dt(d).getUTCFullYear();
  const last = s => s?.points?.length ? s.points[s.points.length - 1] : null;
  const getJSON = u => fetch(u, { cache: "no-store" }).then(r => { if (!r.ok) throw new Error(u + " " + r.status); return r.json(); });
  const fetched = d => new Date(d).toLocaleString("en-GB", { timeZone: "Indian/Maldives", dateStyle: "long", timeStyle: "short" });

  // ---------- header toggles ----------
  const listeners = [];
  const onPrefs = fn => listeners.push(fn);
  function paintPrefs() {
    document.querySelectorAll('[data-pref="cur"] button').forEach(b => b.setAttribute("aria-pressed", b.dataset.v === state.cur));
    document.querySelectorAll('[data-pref="real"] button').forEach(b => b.setAttribute("aria-pressed", (b.dataset.v === "1") === state.real));
    document.body.classList.toggle("is-real", state.real && !!cpiLast);
    const note = document.querySelector(".real-note");
    if (note && cpiLast) note.textContent = `Adjusted for inflation: past amounts are shown in ${mLabel(cpiLast.date)} prices, using the national consumer price index.`;
  }
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-pref] button"); if (!b) return;
    const k = b.parentElement.dataset.pref;
    if (k === "cur") state.cur = b.dataset.v; else state.real = b.dataset.v === "1";
    try { localStorage.setItem("cur", state.cur); localStorage.setItem("real", state.real ? "1" : "0"); } catch (err) {}
    paintPrefs(); listeners.forEach(fn => fn());
  });
  document.addEventListener("DOMContentLoaded", paintPrefs);

  // ---------- line chart with bands, markers and hover ----------
  /*
    opts.rows   [{date, ...}] sorted by date
    opts.series [{val: row => number|null, color, axis: "left"|"right", area, width, dash, dot}]
    opts.bands  [{from, to, color, label}]   dates as yyyy-mm-dd
    opts.vlines [{date, label}]
    opts.marks  [{date, value, label, color}] on the left axis
    opts.ref    {value, color}                horizontal reference on left axis
    opts.yFmt, opts.yFmtR  axis label formatters; opts.tip(row) -> html
  */
  function lineChart(box, opts) {
    const tip = box.querySelector(".tip") || box.appendChild(Object.assign(document.createElement("div"), { className: "tip" }));
    const rows = opts.rows; if (!rows.length) return;
    const hasR = opts.series.some(s => s.axis === "right");
    const W = Math.max(300, box.clientWidth), small = W < 560;
    const Hc = Math.round(Math.min(opts.maxH || 380, Math.max(240, W * .42)));
    const pad = { l: 44, r: hasR ? 44 : 10, t: opts.bands?.length && !small ? 26 : 14, b: 28 };
    const x0 = ts(rows[0].date), x1 = ts(rows[rows.length - 1].date);
    const X = t => pad.l + (t - x0) / (x1 - x0 || 1) * (W - pad.l - pad.r);
    const ext = axis => { let m = 0; opts.series.filter(s => (s.axis || "left") === axis).forEach(s => rows.forEach(r => { const v = s.val(r); if (v != null && v > m) m = v; })); if (opts.ref && axis === "left") m = Math.max(m, opts.ref.value); return m * 1.08 || 1; };
    const yL = ext("left"), yR = hasR ? ext("right") : 1;
    const Y = (v, axis) => Hc - pad.b - v / (axis === "right" ? yR : yL) * (Hc - pad.t - pad.b);
    const nice = (max, n) => { const mag = Math.pow(10, Math.floor(Math.log10(max / n))); return [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => max / s <= n); };
    let g = "";
    // bands
    (opts.bands || []).forEach((b, i) => {
      const a = Math.max(X(ts(b.from)), pad.l), z = Math.min(X(ts(b.to)), W - pad.r); if (z <= pad.l || a >= W - pad.r) return;
      g += `<rect x="${a}" y="${pad.t}" width="${Math.max(2, z - a)}" height="${Hc - pad.t - pad.b}" fill="${b.color}" fill-opacity=".2"/>`;
      if (!small && b.label && z - a > 34) g += `<text class="band-label" x="${a + 3}" y="${pad.t - 8 - (i % 2) * 0}" fill="${b.color}" style="fill:${b.color}">${b.label}</text>`;
    });
    // grid
    const sL = nice(yL, small ? 4 : 5);
    for (let v = 0; v <= yL; v += sL) g += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${Y(v)}" y2="${Y(v)}" stroke="rgba(169,205,214,.15)"/><text x="${pad.l - 8}" y="${Y(v) + 4}" text-anchor="end">${(opts.yFmt || fmt)(v)}</text>`;
    if (hasR) { const sR = nice(yR, small ? 4 : 5); for (let v = 0; v <= yR; v += sR) g += `<text x="${W - pad.r + 8}" y="${Y(v, "right") + 4}" text-anchor="start">${(opts.yFmtR || fmt)(v)}</text>`; }
    const y0 = dt(rows[0].date).getUTCFullYear(), y1 = dt(rows[rows.length - 1].date).getUTCFullYear();
    const every = Math.max(1, Math.ceil((y1 - y0 + 1) / Math.max(3, Math.floor((W - pad.l - pad.r) / 70))));
    for (let y = y0 + 1; y <= y1; y += every) { const x = X(Date.UTC(y, 0, 1)); if (x > pad.l + 10 && x < W - pad.r - 10) g += `<text x="${x}" y="${Hc - 8}" text-anchor="middle">${y}</text>`; }
    if (opts.ref) g += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${Y(opts.ref.value)}" y2="${Y(opts.ref.value)}" stroke="${opts.ref.color}" stroke-dasharray="5 4" stroke-width="1.5"/>`;
    (opts.vlines || []).forEach(v => { const x = X(ts(v.date)); g += `<line x1="${x}" x2="${x}" y1="${pad.t}" y2="${Hc - pad.b}" stroke="#a9cdd6" stroke-dasharray="2 3"/>` + (small ? "" : `<text x="${x + 4}" y="${Hc - pad.b - 6}">${v.label}</text>`); });
    // series
    opts.series.forEach((s, si) => {
      const axis = s.axis || "left"; let d = "", started = false;
      rows.forEach(r => { const v = s.val(r); if (v == null) { started = false; return; } d += (started ? "L" : "M") + X(ts(r.date)).toFixed(1) + " " + Y(v, axis).toFixed(1) + " "; started = true; });
      if (s.area) {
        const pts = rows.filter(r => s.val(r) != null);
        g += `<defs><linearGradient id="ga${si}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="${s.color}" stop-opacity=".5"/><stop offset="1" stop-color="${s.color}" stop-opacity="0"/></linearGradient></defs>`;
        g += `<path d="${d} L${X(ts(pts[pts.length - 1].date))} ${Hc - pad.b} L${X(ts(pts[0].date))} ${Hc - pad.b} Z" fill="url(#ga${si})"/>`;
      }
      g += `<path d="${d}" fill="none" stroke="${s.color}" stroke-width="${s.width || 2.5}" stroke-linejoin="round" ${s.dash ? `stroke-dasharray="${s.dash}"` : ""}/>`;
    });
    // markers
    (opts.marks || []).forEach(m => {
      const x = X(ts(m.date)), y = Y(m.value), anchor = x > W * .75 ? "end" : x < W * .25 ? "start" : "middle", dx = anchor === "end" ? -8 : anchor === "start" ? 8 : 0;
      const up = m.below ? 18 : -12;
      g += `<circle cx="${x}" cy="${y}" r="6" fill="${m.color}" stroke="#072f40" stroke-width="2"/><text class="mark-label" x="${x + dx}" y="${y + up}" text-anchor="${anchor}" style="fill:${m.color}">${m.label}</text>`;
    });
    const lastRow = rows[rows.length - 1], s0 = opts.series[0];
    if (s0.val(lastRow) != null && !opts.noEndDot) g += `<circle cx="${X(ts(lastRow.date))}" cy="${Y(s0.val(lastRow), s0.axis)}" r="5" fill="#f4c95d"/>`;
    g += `<g class="hov" style="display:none"><line class="hl" y1="${pad.t}" y2="${Hc - pad.b}" stroke="#fff" stroke-opacity=".5"/>${opts.series.map((s, i) => `<circle class="hc${i}" r="5" fill="#fff" stroke="${s.color}" stroke-width="2.5"/>`).join("")}</g>`;
    g += `<rect class="hit" x="${pad.l}" y="0" width="${W - pad.l - pad.r}" height="${Hc}" fill="transparent"/>`;
    box.querySelector("svg")?.remove();
    box.insertAdjacentHTML("afterbegin", `<svg viewBox="0 0 ${W} ${Hc}" width="${W}" height="${Hc}" role="img" aria-label="${opts.label || "Chart"}">${g}</svg>`);
    const svg = box.querySelector("svg"), hov = svg.querySelector(".hov");
    const show = e => {
      const rc = svg.getBoundingClientRect(), mx = (e.clientX - rc.left) * W / rc.width;
      let i = 0, best = Infinity; rows.forEach((r, j) => { const dx = Math.abs(X(ts(r.date)) - mx); if (dx < best) { best = dx; i = j; } });
      const r = rows[i], cx = X(ts(r.date));
      hov.style.display = ""; const hl = svg.querySelector(".hl"); hl.setAttribute("x1", cx); hl.setAttribute("x2", cx);
      opts.series.forEach((s, k) => { const c = svg.querySelector(".hc" + k), v = s.val(r); if (v == null) { c.style.display = "none"; return; } c.style.display = ""; c.setAttribute("cx", cx); c.setAttribute("cy", Y(v, s.axis || "left")); });
      tip.innerHTML = opts.tip(r); tip.classList.add("on");
      const px = cx * rc.width / W, tw = tip.offsetWidth;
      tip.style.left = Math.min(Math.max(0, px + 14 + tw > rc.width ? px - tw - 14 : px + 14), rc.width - tw) + "px";
    };
    const hide = () => { hov.style.display = "none"; tip.classList.remove("on"); };
    const hit = svg.querySelector(".hit");
    hit.addEventListener("pointermove", show); hit.addEventListener("pointerdown", show); hit.addEventListener("pointerleave", hide);
  }

  // ---------- grouped bar chart ----------
  /* opts.cats [{label, sub?}], opts.groups [{color, vals:[]}], opts.below(i) -> {text,color}, opts.tip(i) -> html, opts.yFmt */
  function barChart(box, opts) {
    const tip = box.querySelector(".tip") || box.appendChild(Object.assign(document.createElement("div"), { className: "tip" }));
    const W = Math.max(300, box.clientWidth), small = W < 560, Hc = Math.round(Math.min(360, Math.max(240, W * .4)));
    const pad = { l: 44, r: 8, t: 14, b: opts.below ? 44 : 28 };
    const n = opts.cats.length, G = opts.groups.length;
    const max = Math.max(...opts.groups.flatMap(g => g.vals.filter(v => v != null))) * 1.08 || 1;
    const Y = v => Hc - pad.b - v / max * (Hc - pad.t - pad.b);
    const slot = (W - pad.l - pad.r) / n, bw = Math.max(3, Math.min(28, slot * .78 / G));
    const mag = Math.pow(10, Math.floor(Math.log10(max / 4))); const step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => max / s <= (small ? 4 : 5));
    let g = "";
    for (let v = 0; v <= max; v += step) g += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${Y(v)}" y2="${Y(v)}" stroke="rgba(169,205,214,.15)"/><text x="${pad.l - 8}" y="${Y(v) + 4}" text-anchor="end">${(opts.yFmt || fmt)(v)}</text>`;
    const labEvery = Math.max(1, Math.ceil(n / Math.floor((W - pad.l) / (small ? 42 : 56))));
    opts.cats.forEach((c, i) => {
      const cx = pad.l + slot * (i + .5);
      opts.groups.forEach((gr, k) => { const v = gr.vals[i]; if (v == null) return; const x = cx - (G * bw) / 2 + k * bw; g += `<rect x="${x + .5}" y="${Y(v)}" width="${bw - 1}" height="${Hc - pad.b - Y(v)}" fill="${gr.color}" rx="1.5"${c.partial ? ' fill-opacity=".55"' : ""}/>`; });
      if (i % labEvery === 0 || i === n - 1) g += `<text x="${cx}" y="${Hc - pad.b + 16}" text-anchor="middle">${c.label}</text>`;
      if (opts.below && (i % labEvery === 0 || i === n - 1)) { const b = opts.below(i); if (b) g += `<text x="${cx}" y="${Hc - pad.b + 32}" text-anchor="middle" style="fill:${b.color};font-weight:700;font-size:11px">${b.text}</text>`; }
    });
    g += `<rect class="hl" x="0" y="${pad.t}" width="${slot}" height="${Hc - pad.t - pad.b}" fill="#fff" fill-opacity="0"/>`;
    g += `<rect class="hit" x="${pad.l}" y="0" width="${W - pad.l - pad.r}" height="${Hc}" fill="transparent"/>`;
    box.querySelector("svg")?.remove();
    box.insertAdjacentHTML("afterbegin", `<svg viewBox="0 0 ${W} ${Hc}" width="${W}" height="${Hc}" role="img" aria-label="${opts.label || "Bar chart"}">${g}</svg>`);
    const svg = box.querySelector("svg"), hl = svg.querySelector(".hl");
    const show = e => {
      const rc = svg.getBoundingClientRect(), mx = (e.clientX - rc.left) * W / rc.width;
      const i = Math.max(0, Math.min(n - 1, Math.floor((mx - pad.l) / slot)));
      hl.setAttribute("x", pad.l + slot * i); hl.setAttribute("fill-opacity", ".06");
      tip.innerHTML = opts.tip(i); tip.classList.add("on");
      const px = (pad.l + slot * (i + .5)) * rc.width / W, tw = tip.offsetWidth;
      tip.style.left = Math.min(Math.max(0, px + 14 + tw > rc.width ? px - tw - 14 : px + 14), rc.width - tw) + "px";
    };
    const hide = () => { hl.setAttribute("fill-opacity", "0"); tip.classList.remove("on"); };
    const hit = svg.querySelector(".hit");
    hit.addEventListener("pointermove", show); hit.addEventListener("pointerdown", show); hit.addEventListener("pointerleave", hide);
  }

  const row = (l, v) => v == null ? "" : `<div class="row"><span>${l}</span><span>${v}</span></div>`;
  const onResize = fn => { let t; addEventListener("resize", () => { clearTimeout(t); t = setTimeout(fn, 120); }); };

  return { SEC_YEAR, MONTHS, state, setData, rateAt, cpiAt, realFactor, conv, fromUSD, fmt, sym, short, money, moneyFull,
    ts, mLabel, mShort, qLabel, dayLabel, last, getJSON, fetched, onPrefs, paintPrefs, lineChart, barChart, row, onResize,
    get USD() { return USD; }, get cpiLast() { return cpiLast; } };
})();
