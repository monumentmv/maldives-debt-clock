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
  let fx = [], cpi = [], USD = 15.42, cpiLast = null, cpiBase = null, baseFrom = null;
  function setData(S) {
    fx = (S.usd_rate?.points || []).filter(p => p.value > 0);
    if (fx.length) USD = fx[fx.length - 1].value;
    cpi = (S.cpi?.points || []).filter(p => p.value > 0);
    cpiLast = cpi.length ? cpi[cpi.length - 1] : null;
    // price base for "Real": the average CPI of the latest 12 months, which smooths out month-to-month swings
    if (cpi.length >= 12) { const l12 = cpi.slice(-12); cpiBase = l12.reduce((a, p) => a + p.value, 0) / 12; baseFrom = l12[0].date; }
    else if (cpiLast) { cpiBase = cpiLast.value; baseFrom = cpiLast.date; }
    if (!cpi.length) document.querySelectorAll('[data-pref="real"]').forEach(t => t.hidden = true);
  }
  const lastBefore = (arr, date) => { let r = null; for (const p of arr) { if (p.date <= date) r = p; else break; } return r; };
  const rateAt = date => (lastBefore(fx, date) || fx[0] || { value: USD }).value;
  const cpiAt = date => (lastBefore(cpi, date) || null)?.value;
  /** multiply a past rufiyaa amount by this to express it in base-period prices */
  const realFactor = date => {
    if (!state.real || !cpiBase || !date) return 1;
    const c = cpiAt(date); return c ? cpiBase / c : 1;
  };
  /** for comparisons over time: convert a rufiyaa amount recorded at `date`, applying "Real" if it is on */
  const conv = (mvr, date) => {
    const v = mvr * realFactor(date);
    if (state.cur !== "USD") return v;
    return v / (state.real || !date ? USD : rateAt(date));
  };
  /** for current figures: never inflation-adjusted, only converted to the chosen currency */
  const convNow = (mvr, date) => state.cur !== "USD" ? mvr : mvr / (date ? rateAt(date) : USD);
  const isReal = () => state.real && !!cpiBase;
  const baseLabel = () => cpiLast ? `average prices of the 12 months to ${MONTHS[new Date(cpiLast.date).getUTCMonth()]} ${new Date(cpiLast.date).getUTCFullYear()}` : "";
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
  const money = (mvr, date) => sym() + " " + short(conv(mvr, date));          // applies "Real"
  const moneyNow = (mvr, date) => sym() + " " + short(convNow(mvr, date));    // never adjusted
  const moneyFull = (mvr, d = 0, date) => sym() + " " + fmt(convNow(mvr, date), d);
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
    document.body.classList.toggle("is-real", state.real && !!cpiBase && !document.querySelector('[data-pref="real"][hidden]'));
    const note = document.querySelector(".real-note");
    if (note && cpiBase) note.innerHTML = `<span class="long">Real mode. Charts and comparisons over time are adjusted for inflation, in ${baseLabel()}. Current figures are always in today's money.</span><span class="short">Real mode, past amounts adjusted for inflation</span>`;
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
    const pad = { l: 44, r: hasR ? 44 : 10, t: opts.bands?.length ? 40 : (opts.yTitle ? 24 : 14), b: 28 };
    const x0 = ts(rows[0].date), x1 = ts(rows[rows.length - 1].date);
    const X = t => pad.l + (t - x0) / (x1 - x0 || 1) * (W - pad.l - pad.r);
    const ext = axis => { let m = 0; opts.series.filter(s => (s.axis || "left") === axis).forEach(s => rows.forEach(r => { const v = s.val(r); if (v != null && v > m) m = v; })); if (opts.ref && axis === "left") m = Math.max(m, opts.ref.value); return m * 1.08 || 1; };
    const yL = ext("left"), yR = hasR ? ext("right") : 1;
    const Y = (v, axis) => Hc - pad.b - v / (axis === "right" ? yR : yL) * (Hc - pad.t - pad.b);
    const nice = (max, n) => { const mag = Math.pow(10, Math.floor(Math.log10(max / n))); return [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => max / s <= n); };
    let g = "";
    // bands
    let lastBadge = -1e9, row = 0;
    (opts.bands || []).forEach((b, i) => {
      const a = Math.max(X(ts(b.from)), pad.l), z = Math.min(X(ts(b.to)), W - pad.r); if (z <= pad.l || a >= W - pad.r) return;
      g += `<rect x="${a}" y="${pad.t}" width="${Math.max(3, z - a)}" height="${Hc - pad.t - pad.b}" fill="${b.color}" fill-opacity=".22"/>`;
      if (b.n != null) {
        const cx = (a + z) / 2; row = cx - lastBadge < 20 ? 1 - row : 0; lastBadge = cx;
        const cy = pad.t - 10 - row * 0, cyy = row ? pad.t - 30 + 0 : pad.t - 12;
        g += `<line x1="${cx}" x2="${cx}" y1="${cyy + 8}" y2="${pad.t}" stroke="${b.color}" stroke-width="1"/><circle cx="${cx}" cy="${cyy}" r="8.5" fill="${b.color}"/><text x="${cx}" y="${cyy + 4}" text-anchor="middle" style="fill:#072f40;font-weight:800;font-size:11px">${b.n}</text>`;
      }
    });
    if (opts.yTitle) g += `<text x="${pad.l - 8}" y="${opts.bands?.length ? 12 : pad.t - 10}" text-anchor="end" style="font-weight:700">${opts.yTitle}</text>`;
    if (opts.yTitleR && hasR) g += `<text x="${W - 2}" y="${opts.bands?.length ? 12 : pad.t - 10}" text-anchor="end" style="font-weight:700">${opts.yTitleR}</text>`;
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
      g += `<circle cx="${x}" cy="${y}" r="6" fill="${m.color}" stroke="#072f40" stroke-width="2"/>` + (small ? "" : `<text class="mark-label" x="${x + dx}" y="${y + up}" text-anchor="${anchor}" style="fill:${m.color}">${m.label}</text>`);
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

  // ---------- warnings when data stops updating ----------
  function checkStale(data) {
    const msgs = [], now = Date.now(), day = 86400000;
    const tot = data.series?.total?.points; const L = tot?.length ? tot[tot.length - 1] : null;
    if (L && now - ts(L.date) > 215 * day) msgs.push(`The latest official debt figure is for ${mLabel(L.date)}, more than seven months ago. The clock is still estimating from it, so treat it with extra caution.`);
    if (data.fetched_at && now - new Date(data.fetched_at).getTime() > 8 * day) msgs.push(`The data hasn't been refreshed since ${fetched(data.fetched_at)}. Figures shown are the last ones received.`);
    (data.carried_over || []).length && msgs.push("Some figures couldn't be updated at the last refresh, so their previous values are shown.");
    if (!msgs.length) return;
    const el = document.createElement("div"); el.className = "stale-note"; el.setAttribute("role", "status"); el.innerHTML = msgs.map(m => `<p>${m}</p>`).join("");
    document.querySelector(".site-head")?.after(el);
  }

  const row = (l, v) => v == null ? "" : `<div class="row"><span>${l}</span><span>${v}</span></div>`;
  const onResize = fn => { let t; addEventListener("resize", () => { clearTimeout(t); t = setTimeout(fn, 120); }); };


  // ---------- small graphics for stat cards ----------
  const clamp01 = x => Math.max(0, Math.min(1, x));
  const mini = {
    /** progress bar, with an optional white line (for example, how much of the year has passed) */
    meter: (share, mark, color, left = "", right = "") => `<div class="mini" style="color:${color}"><div class="meter" role="img" aria-label="${left}"><i style="width:${clamp01(share) * 100}%"></i>${mark != null ? `<b style="left:calc(${clamp01(mark) * 100}% - 1px)"></b>` : ""}</div>${left || right ? `<div class="cap"><span>${left}</span><span>${right}</span></div>` : ""}</div>`,
    /** small bar chart of recent values; hi = index to highlight, ref = index to outline */
    spark: (vals, color, { hi = vals.length - 1, ref = null, left = "", right = "" } = {}) => {
      const max = Math.max(...vals.filter(v => v != null)) || 1, n = vals.length, w = 100 / n;
      const bars = vals.map((v, i) => v == null ? "" : `<rect x="${i * w + w * .12}" y="${40 - v / max * 38}" width="${w * .76}" height="${Math.max(1, v / max * 38)}" rx=".8" fill="${color}" fill-opacity="${i === hi ? 1 : i === ref ? .75 : .35}"${i === ref ? ` stroke="${color}" stroke-width=".8"` : ""}/>`).join("");
      return `<div class="mini spark"><svg viewBox="0 0 100 40" preserveAspectRatio="none" role="img" aria-label="${left}">${bars}</svg>${left || right ? `<div class="cap"><span>${left}</span><span>${right}</span></div>` : ""}</div>`;
    },
    /** 100 squares, share of them filled */
    waffle: (pct, color, caption = "") => `<div class="mini" style="color:${color}"><div class="waffle" role="img" aria-label="${caption}">${Array.from({ length: 100 }, (_, i) => `<i${i < Math.round(pct) ? ' class="on"' : ""}></i>`).join("")}</div>${caption ? `<div class="cap"><span>${caption}</span></div>` : ""}</div>`,
    /** two or three bars on the same scale: [label, value, colour, text] */
    duo: rows => { const max = Math.max(...rows.map(r => r[1])) || 1;
      return `<div class="mini duo">${rows.map(([l, v, c, t]) => `<div><span>${l}<b>${t}</b></span><div class="t"><i style="width:${clamp01(v / max) * 100}%;background:${c}"></i></div></div>`).join("")}</div>`; },
  };

  // ---------- icons for headline figures ----------
  const ICONS = {
    car: "<path d=\"M5 11l1.8-4.2A2 2 0 0 1 8.6 5.6h6.8a2 2 0 0 1 1.8 1.2L19 11\" /><rect x=\"3\" y=\"11\" width=\"18\" height=\"6\" rx=\"2\" fill=\"currentColor\" fill-opacity=\".18\"/><circle cx=\"7.5\" cy=\"17.5\" r=\"1.8\"/><circle cx=\"16.5\" cy=\"17.5\" r=\"1.8\"/>",
    lock: "<rect x=\"4.5\" y=\"10.5\" width=\"15\" height=\"10\" rx=\"2\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M8 10.5V7a4 4 0 0 1 7.6-1.7M12 14.5v2.5\"/>",
    hammer: "<path d=\"M13 5.5l5 5-2.5 2.5-5-5z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M14.5 4l5 5M10.8 9.7L3.5 17l3.5 3.5 7.3-7.3\"/>",
    alert: "<path d=\"M12 3.5l9.5 16.5h-19z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M12 10v4.5M12 17.5v.5\"/>",
    interest: "<circle cx=\"12\" cy=\"12\" r=\"9\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M15.5 8.5l-7 7\"/><circle cx=\"9\" cy=\"9\" r=\"1.4\"/><circle cx=\"15\" cy=\"15\" r=\"1.4\"/>",
    coins: "<ellipse cx=\"12\" cy=\"6.5\" rx=\"7.5\" ry=\"2.8\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M4.5 6.5v5c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-5M4.5 11.5v5c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-5\"/>",
    moneyIn: "<path d=\"M6.5 10h11v8a3 3 0 0 1-3 3h-5a3 3 0 0 1-3-3z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M5.5 10h13\"/><circle cx=\"12\" cy=\"4.6\" r=\"2.3\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M12 7.6v4.6M10 10.4l2 2 2-2\"/>",
    moneyOut: "<rect x=\"3\" y=\"8.5\" width=\"16\" height=\"12\" rx=\"2\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M15 12.5h5v4h-5a2 2 0 0 1 0-4z\"/><path d=\"M6.5 8.5L14 4.2l2.3 4.3\"/>",
    gap: "<path d=\"M3 9.5L12 4l9 5.5z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M5.5 11v6.5M10 11v6.5M14 11v6.5M18.5 11v6.5M3 20.5h18\"/>",
    police: "<path d=\"M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M12 8.2l1.2 2.4 2.6.4-1.9 1.8.5 2.6-2.4-1.3-2.4 1.3.5-2.6-1.9-1.8 2.6-.4z\"/>",
    prison: "<rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"1.5\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M8.5 4v16M12 4v16M15.5 4v16\"/>",
    gavel: "<path d=\"M11.4 5.6l7 7-2.8 2.8-7-7z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M13.5 3.5l7 7M8 11l-5 5 2.5 2.5 5-5M4 21h9\"/>",
    search: "<circle cx=\"10.5\" cy=\"10.5\" r=\"6.5\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M15.5 15.5L21 21\"/>",
    family: "<path d=\"M5.5 9.5V20h13V9.5L12 4z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M3.5 11L12 4l8.5 7\"/><path d=\"M12 17.5s-3.2-1.9-3.2-3.8a1.7 1.7 0 0 1 3.2-.8 1.7 1.7 0 0 1 3.2.8c0 1.9-3.2 3.8-3.2 3.8z\"/>",
    child: "<circle cx=\"12\" cy=\"5.5\" r=\"2.6\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M7.5 10.5l4.5 1.5 4.5-1.5M12 12v4M9.5 21l2.5-5 2.5 5\"/>",
    scales: "<path d=\"M12 4v16M8 20h8M5 7.5h14\"/><path d=\"M5 7.5L2.5 13a2.6 2.6 0 0 0 5 0zM19 7.5L16.5 13a2.6 2.6 0 0 0 5 0z\" fill=\"currentColor\" fill-opacity=\".18\"/>",
    pill: "<path d=\"M10.5 20.5a4.95 4.95 0 0 1-7-7l6-6a4.95 4.95 0 0 1 7 7z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M8.5 8.5l7 7\"/>",
    school: "<path d=\"M2 9l10-5 10 5-10 5z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M6 11v5c0 1.6 2.7 3 6 3s6-1.4 6-3v-5M22 9v6\"/>",
    hospital: "<rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2.5\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M12 8v8M8 12h8\"/>",
    shield: "<path d=\"M12 3l8 3v5.5c0 4.6-3.4 8-8 9.5-4.6-1.5-8-4.9-8-9.5V6z\" fill=\"currentColor\" fill-opacity=\".18\"/>",
    fuel: "<path d=\"M4 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M3 21h12M6.5 7.5h5\"/><path d=\"M14 9h2a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V8l-3-3\"/>",
    ship: "<path d=\"M3 15l2.5 5h13L21 15z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M6 15V10h12v5M9.5 10V6h5v4\"/><path d=\"M2 21.5c2 0 2-1 4-1s2 1 4 1 2-1 4-1 2 1 4 1\"/>",
    person: "<circle cx=\"9\" cy=\"7.5\" r=\"3.2\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M3 20c0-3.6 2.7-6.2 6-6.2s6 2.6 6 6.2\"/><circle cx=\"17\" cy=\"9\" r=\"2.4\"/><path d=\"M15.8 13.9c2.8.3 5.2 2.6 5.2 6.1\"/>",
    clock: "<circle cx=\"12\" cy=\"13\" r=\"8\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M12 9v4l3 2M9.5 2.5h5M12 2.5V5\"/>",
    calendar: "<rect x=\"3.5\" y=\"5\" width=\"17\" height=\"15\" rx=\"2\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M3.5 10h17M8 3v4M16 3v4M8 14h2M14 14h2M8 17h2\"/>",
    cases: "<rect x=\"5\" y=\"4\" width=\"14\" height=\"17\" rx=\"2\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M9 4V3h6v1M9 10h6M9 14h6M9 18h3\"/>",
    dollar: "<circle cx=\"12\" cy=\"12\" r=\"9\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M12 6v12M15 8.8c0-1.2-1.3-2-3-2s-3 .8-3 2 1.3 1.8 3 2.2 3 1 3 2.2-1.3 2-3 2-3-.8-3-2\"/>",
    chart: "<path d=\"M4 20V4M4 20h16\"/><path d=\"M7.5 15l4-4 3 3 5-6v12h-12z\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M7.5 15l4-4 3 3 5-6\"/>",
    globe: "<circle cx=\"12\" cy=\"12\" r=\"8.5\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M3.5 12h17M12 3.5c2.5 2.4 3.5 5.3 3.5 8.5s-1 6.1-3.5 8.5c-2.5-2.4-3.5-5.3-3.5-8.5s1-6.1 3.5-8.5z\"/>",
    trend: "<path d=\"M3 17l6-6 4 4 8-8\" /><path d=\"M15 7h6v6\"/>",
    people: "<circle cx=\"9\" cy=\"7.5\" r=\"3.2\" fill=\"currentColor\" fill-opacity=\".18\"/><path d=\"M3 20c0-3.6 2.7-6.2 6-6.2s6 2.6 6 6.2\"/><circle cx=\"17\" cy=\"9\" r=\"2.4\"/><path d=\"M15.8 13.9c2.8.3 5.2 2.6 5.2 6.1\"/>",
  };
  const icon = (name, cls = "ico") => ICONS[name] ? `<span class="${cls}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg></span>` : "";
  function paintIcons(root = document) {
    root.querySelectorAll(".stat[data-icon]").forEach(s => { if (!s.querySelector(":scope > .ico")) s.insertAdjacentHTML("afterbegin", icon(s.dataset.icon)); });
  }

  // ---------- how recent the figures are, so visitors know when to come back ----------
  const daysAgo = d => Math.floor((Date.now() - new Date(String(d).length <= 10 ? d + "T12:00:00+05:00" : d)) / 86400000);
  const ago = d => { const n = daysAgo(d); return n <= 0 ? "today" : n === 1 ? "yesterday" : n < 14 ? `${n} days ago` : n < 60 ? `${Math.round(n / 7)} weeks ago` : `${Math.round(n / 30.4)} months ago`; };
  const CADENCE = { weekly: ["every week", 10], monthly: ["every month", 45], quarterly: ["every three months", 120], daily: ["every day", 3] };
  /** el: where to write. asOf: date the figures run to. what: plain description. cadence: weekly, monthly, quarterly or daily */
  function fresh(el, { asOf, what, cadence = "weekly", next = "" }) {
    if (!el || !asOf) return;
    const [every, newDays] = CADENCE[cadence] || CADENCE.weekly, isNew = daysAgo(asOf) <= newDays;
    el.className = "fresh" + (isNew ? " is-new" : "");
    el.innerHTML = `<span class="dot" aria-hidden="true"></span>${isNew ? `<span class="badge">Recent</span>` : ""}<span>${what} to <b>${dayLabel(asOf)}</b>, ${ago(asOf)}. New figures come out ${every}${next ? `, ${next}` : ""}, so check back for the latest.</span>`;
  }

  /** remembers a few headline figures and, on a later visit, says what has changed */
  function since(key, items, el) {
    let prev = null; const nowT = Date.now();
    try { prev = JSON.parse(localStorage.getItem("seen:" + key) || "null"); } catch (e) {}
    const store = () => { try { localStorage.setItem("seen:" + key, JSON.stringify({ t: nowT, v: Object.fromEntries(items.map(i => [i.id, i.value])), tag: Object.fromEntries(items.map(i => [i.id, i.tag || ""])) })); } catch (e) {} };
    if (!prev) { store(); return; }
    if (nowT - prev.t < 3 * 3600e3) return;
    const changes = items.filter(i => prev.v[i.id] != null && i.value != null && (i.value !== prev.v[i.id] || (i.tag || "") !== (prev.tag?.[i.id] || ""))).map(i => i.say(prev.v[i.id], prev.tag?.[i.id])).filter(Boolean);
    store();
    if (!changes.length) return;
    const box = el || (() => { const b = document.createElement("div"); document.querySelector("main .wrap")?.prepend(b); return b; })();
    box.className = "since";
    box.innerHTML = `<b>Since your last visit ${ago(new Date(prev.t).toISOString())}</b><ul>${changes.map(c => `<li>${c}</li>`).join("")}</ul><button type="button" aria-label="Close">×</button>`;
    box.querySelector("button").onclick = () => box.remove();
  }

  /** a "showing" picker so visitors can look at an earlier period. options: [{v, label}] newest first */
  function asOf(el, options, value, onChange) {
    if (!el || !options.length) return;
    const latest = options[0].v;
    let html = "", g = null;
    options.forEach(o => {
      if (o.group !== g) { if (g !== null) html += "</optgroup>"; g = o.group; if (g != null) html += `<optgroup label="${g}">`; }
      html += `<option value="${o.v}"${o.v === value ? " selected" : ""}>${o.label}</option>`;
    });
    if (g != null) html += "</optgroup>";
    const idx = Math.max(0, options.findIndex(o => o.v === value)), cur = options[idx];
    el.className = "period-pick";
    el.innerHTML = `<span class="yr-chip" title="Year shown">${cur.group ?? String(cur.v).slice(0, 4)}</span>` +
      `<button type="button" class="step" data-d="1"${idx >= options.length - 1 ? " disabled" : ""} aria-label="Earlier period">‹ Earlier</button>` +
      `<label><span>Showing</span> <select aria-label="Period shown">${html}</select></label>` +
      `<button type="button" class="step" data-d="-1"${idx <= 0 ? " disabled" : ""} aria-label="Later period">Later ›</button>` +
      `<button type="button" class="pill back"${value === latest ? " hidden" : ""}>Back to the latest</button>`;
    const sel = el.querySelector("select");
    const go = v => { onChange(v); asOf(el, options, v, onChange); try { const u = new URL(location.href); v === latest ? u.searchParams.delete("p") : u.searchParams.set("p", v); history.replaceState(null, "", u); } catch (e) {} };
    sel.onchange = () => go(sel.value);
    el.querySelectorAll(".step").forEach(b => b.onclick = () => { const o = options[idx + Number(b.dataset.d)]; if (o) go(o.v); });
    el.querySelector(".back").onclick = () => go(latest);
  }
  /** the period asked for in the page address (?p=...), if any */
  const wantedPeriod = () => { try { return new URLSearchParams(location.search).get("p"); } catch (e) { return null; } };

  // ---------- short explanations in a pop-up, instead of sending readers to another page ----------
  const EXPLAIN = {
    budget: ["Weekly budget figures", "Every week the Ministry of Finance publishes running totals for the year so far, covering money collected, money spent and the gap between them. They are early figures and can change a little as accounts are checked. The site reads each new report as soon as it appears."],
    fuel: ["Fuel imports", "These are the values of petroleum products brought into the country each month, such as diesel, petrol and aviation fuel, as published by MMA. Almost all of the country's energy is imported, so when world oil prices jump, this bill jumps too."],
    fiscal: ["Revenue and spending", "Revenue is what the government collects, mostly taxes. Spending is what it pays out for salaries, services, subsidies, interest and building projects. When spending is bigger, the difference is borrowed and adds to the debt. Paying back old loans isn't counted as spending."],
    population: ["Per-citizen figures", "The debt is divided by the number of Maldivian citizens on the national register, grown forward at the recent population growth rate. Foreign workers and visitors aren't counted. It shows the size of the debt in a way people can picture, not a bill anyone receives."],
    priorities: ["Interest compared with other spending", "Interest is the extra the government pays lenders for money borrowed in the past. It doesn't pay for any service this year. This page puts it beside what the police, justice offices and rights bodies spend over the same weeks, using the Ministry of Finance's weekly reports. Case counts are reports made to the police."],
    revenue: ["Revenue collected by MIRA", "MIRA, the tax office, publishes how much it collects each month and how much of it is paid in US dollars. The figures cover the taxes, fees and rents MIRA handles. They don't include everything the government receives, such as grants from abroad."],
    clock: ["How the clock works", "Official debt figures come out once every three months. Between releases, the clock starts from the latest official figure and adds debt at the average pace of the last year, so the number is an estimate. When a new official figure is published, the clock resets to it."],
    gdp: ["Debt compared with the economy", "GDP is the value of everything the country produces in a year. Comparing debt with GDP shows how big the debt is next to the size of the economy. Above 100% means the debt is bigger than a whole year of the country's output."],
    owed: ["Who the debt is owed to", "Domestic debt is owed to lenders inside Maldives, mostly banks, MMA and the pension fund. External debt is owed abroad, to other governments, development banks and investors, and has to be paid back in foreign currency."],
    guaranteed: ["Guaranteed debt", "Guaranteed debt is money borrowed by someone other than the government, mostly state-owned companies such as the housing, electricity and trading companies, where the government has promised to pay if the borrower can't. The lenders include foreign and local banks and some private companies. It counts towards public debt because, if things go wrong, the government is on the hook."],
    interest: ["Interest", "Interest is the extra paid to lenders for using their money, on top of paying back what was borrowed. It builds up every day on everything owed. It is a cost that pays for no school, road or salary."],
    deficit: ["Deficit", "A deficit is when the government spends more than it collects. The gap is filled by borrowing, so each year's deficit adds to the debt."],
    real: ["Nominal and real", "Nominal shows amounts as they were at the time. Real adjusts older amounts for price rises, so a rufiyaa from ten years ago can be compared fairly with a rufiyaa today."],
    taxrev: ["Taxes are not all of the government's income", "MIRA's figures cover the taxes, fees and rents MIRA collects. Total government revenue is bigger. It also includes import duties collected by Customs, dividends from state-owned companies, airport and other fees, rents, and grants from abroad. So MIRA's total will always be less than the revenue shown on the budget page."],
    usd: ["US dollar figures", "Amounts can be shown in US dollars using MMA's official exchange rate. Past amounts use the rate of the time, so changes in the exchange rate don't distort the history."],
  };
  function explain(key, anchor) {
    const e = EXPLAIN[key]; if (!e) return false;
    let dlg = document.getElementById("explain");
    if (!dlg) {
      dlg = document.createElement("div"); dlg.id = "explain"; dlg.className = "explain"; dlg.hidden = true;
      dlg.innerHTML = `<div class="explain-box" role="dialog" aria-modal="true" aria-labelledby="explainT"><button type="button" class="x" aria-label="Close">×</button><h3 id="explainT"></h3><p></p><a class="more" href="#">Read more in the methodology</a></div>`;
      document.body.appendChild(dlg);
      const close = () => { dlg.hidden = true; dlg._from?.focus?.(); };
      dlg.addEventListener("click", ev => { if (ev.target === dlg || ev.target.closest(".x")) close(); });
      document.addEventListener("keydown", ev => { if (ev.key === "Escape" && !dlg.hidden) close(); });
    }
    dlg.querySelector("h3").textContent = e[0]; dlg.querySelector("p").textContent = e[1];
    dlg.querySelector(".more").href = "methodology.html#" + (anchor || { deficit: "fiscal", guaranteed: "debt" }[key] || key);
    dlg._from = document.activeElement; dlg.hidden = false; dlg.querySelector(".x").focus();
    return true;
  }
  document.addEventListener("click", ev => {
    const t = ev.target.closest("[data-term]");
    if (t) { ev.preventDefault(); explain(t.dataset.term, t.dataset.anchor); return; }
    const a = ev.target.closest('a[href^="methodology.html#"]');
    if (a && !a.closest(".explain") && !/methodology\.html$/.test(location.pathname)) { const k = a.getAttribute("href").split("#")[1]; if (explain(k)) ev.preventDefault(); }
  });
  document.addEventListener("keydown", ev => { const t = ev.target.closest?.("[data-term]"); if (t && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); explain(t.dataset.term, t.dataset.anchor); } });
  function realHelp() {
    const t = document.querySelector('.toggle[data-pref="real"]');
    if (!t || t.nextElementSibling?.classList.contains("q")) return;
    t.insertAdjacentHTML("afterend", `<button type="button" class="q" data-term="real" aria-label="What do nominal and real mean?">?</button>`);
  }

  // ---------- the header's height, so pickers can stick just below it ----------
  function headHeight() { const h = document.querySelector(".site-head"); if (h) document.documentElement.style.setProperty("--headH", h.offsetHeight + "px"); }
  addEventListener("resize", headHeight);

  // ---------- a way back, when someone followed a link from another page ----------
  const FROM = { updates: "Back to Updates", home: "Back to the home page", priorities: "Back to Priorities" };
  function backLink() {
    let from = null; try { from = new URLSearchParams(location.search).get("from"); } catch (e) {}
    if (!from || !FROM[from] || document.querySelector(".back-to")) return;
    const a = document.createElement("a");
    a.className = "back-to"; a.href = from === "home" ? "./" : `${from}.html`; a.textContent = "← " + FROM[from];
    a.addEventListener("click", ev => { if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) { ev.preventDefault(); history.back(); } });
    document.body.appendChild(a);
  }

  // ---------- "Updates" in the menu gets a badge when there is something new since the last look ----------
  function updatesBadge() {
    const link = document.querySelector('.site-nav a[data-page="updates"]'); if (!link) return;
    getJSON("priorities.json").then(P => {
      const newest = P?.latest?.d; if (!newest) return;
      let seen = null; try { seen = localStorage.getItem("updatesSeen"); } catch (e) {}
      if (/updates\.html$/.test(location.pathname)) { try { localStorage.setItem("updatesSeen", newest); } catch (e) {} return; }
      if (!seen || seen < newest) link.insertAdjacentHTML("beforeend", `<span class="badge">New</span>`);
    }).catch(() => {});
  }

  // ---------- colour themes ----------
  const THEMES = [["", "Ocean"], ["light", "Daylight"], ["contrast", "High contrast"]];
  function setTheme(t) {
    if (t) document.documentElement.dataset.theme = t; else delete document.documentElement.dataset.theme;
    try { t ? localStorage.setItem("theme", t) : localStorage.removeItem("theme"); } catch (e) {}
    const b = document.querySelector(".theme-btn"), name = (THEMES.find(x => x[0] === t) || THEMES[0])[1];
    if (b) { b.setAttribute("aria-label", `Colour theme, ${name}. Change theme`); b.title = `Theme, ${name}`; }
    listeners.forEach(fn => fn());
  }
  function themeButton() {
    const box = document.querySelector(".prefs") || document.querySelector(".site-head");
    if (!box || box.querySelector(".theme-btn")) return;
    const b = document.createElement("button");
    b.type = "button"; b.className = "theme-btn";
    b.innerHTML = `<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 2a8 8 0 0 1 0 16z" fill="currentColor"/></svg>`;
    b.addEventListener("click", () => { const cur = document.documentElement.dataset.theme || "", i = THEMES.findIndex(x => x[0] === cur); setTheme(THEMES[(i + 1) % THEMES.length][0]); });
    box.appendChild(b);
    setTheme(document.documentElement.dataset.theme || "");
  }

  // ---------- interest ticker, counting from when the visitor arrived ----------
  function ticker() {
    let off = false; try { off = sessionStorage.getItem("tickerOff") === "1"; } catch (e) {}
    if (off || document.querySelector(".ticker")) return;
    getJSON("priorities.json").then(P => {
      const it = P?.latest?.interest?.[2], days = P?.latest?.days;
      if (!it || !days) return;
      const perSec = it * 1e6 / days / 86400;
      let start = Date.now(); try { start = Number(sessionStorage.getItem("arrived")) || start; sessionStorage.setItem("arrived", start); } catch (e) {}
      const el = document.createElement("div");
      el.className = "ticker";
      el.innerHTML = `<span class="dot" aria-hidden="true"></span><a href="priorities.html" title="Interest builds up every second on the money the government owes"><span>Interest accrued since you arrived</span><span class="v">…</span></a><button type="button" aria-label="Hide the interest counter">×</button>`;
      document.body.appendChild(el);
      const v = el.querySelector(".v");
      let last = 0;
      const tick = t => { if (!el.isConnected) return; if (t - last > 100) { last = t; v.textContent = sym() + " " + fmt(convNow((Date.now() - start) / 1000 * perSec)); } requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
      el.querySelector("button").addEventListener("click", () => { el.remove(); try { sessionStorage.setItem("tickerOff", "1"); } catch (e) {} });
    }).catch(() => {});
  }
  const boot = () => { headHeight(); themeButton(); realHelp(); ticker(); paintIcons(); backLink(); updatesBadge(); };
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", boot) : boot();

  return { SEC_YEAR, mini, setTheme, explain, wantedPeriod, icon, paintIcons, fresh, since, asOf, ago, daysAgo, MONTHS, state, setData, rateAt, cpiAt, realFactor, conv, convNow, isReal, baseLabel, checkStale, fromUSD, fmt, sym, short, money, moneyNow, moneyFull,
    ts, mLabel, mShort, qLabel, dayLabel, last, getJSON, fetched, onPrefs, paintPrefs, lineChart, barChart, row, onResize,
    get USD() { return USD; }, get cpiLast() { return cpiLast; } };
})();
