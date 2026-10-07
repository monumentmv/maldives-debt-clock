/* Maldives National Debt Clock: gentle motion for every page.
   - underwater bubbles and light rays behind the page heading (the home page keeps its own sea)
   - headline figures count up the first time they come into view
   - sections and cards fade in, meters and bars grow to their value
   - a thin reading progress line under the header
   Nothing moves for readers who ask for reduced motion. */
(() => {
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;
  const css = n => getComputedStyle(root).getPropertyValue(n).trim();

  // ---------- reading progress ----------
  const bar = document.createElement("div");
  bar.className = "mo-progress"; bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);
  const progress = () => {
    const h = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${h > 0 ? Math.min(1, scrollY / h) : 0})`;
  };
  addEventListener("scroll", progress, { passive: true }); addEventListener("resize", progress); progress();

  if (calm) return;

  // ---------- the sea behind the heading ----------
  const host = document.querySelector(".hero") ? null : (document.querySelector(".masthead") || document.querySelector("main.dark, main.wrap"));
  if (host) {
    host.classList.add("mo-host");
    const cv = document.createElement("canvas");
    cv.className = "mo-sea"; cv.setAttribute("aria-hidden", "true");
    host.prepend(cv);
    const ctx = cv.getContext("2d");
    let w, h, bubbles = [], rays = [], col, raf = 0, seen = true, last = 0;
    const rand = (a, b) => a + Math.random() * (b - a);
    const rgba = (hex, a) => {
      const m = /^#?([0-9a-f]{6})$/i.exec(hex || ""); if (!m) return `rgba(169,205,214,${a})`;
      const n = parseInt(m[1], 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`;
    };
    const colours = () => { col = { foam: css("--foam") || "#ffffff", lagoon: css("--lagoon") || "#3fb8b0", sun: css("--sun") || "#f4c95d", light: root.dataset.theme === "light" }; };
    const bubble = y => ({ x: rand(0, w), y, r: rand(1.5, 7), v: rand(.25, .8), ph: rand(0, 6), wob: rand(4, 14) });
    function size() {
      const r = cv.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
      w = r.width; h = r.height; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      bubbles = Array.from({ length: Math.round(Math.min(60, w / 22)) }, () => bubble(rand(0, h)));
      rays = Array.from({ length: 5 }, (_, i) => ({ x: w * (.1 + i * .2) + rand(-40, 40), wd: rand(40, 110), ph: rand(0, 6) }));
    }
    function frame(t) {
      const dt = last ? Math.min((t - last) / 16.7, 3) : 1; last = t;
      ctx.clearRect(0, 0, w, h);
      // soft light rays from the surface
      rays.forEach(r => {
        const a = (col.light ? .05 : .06) * (0.6 + 0.4 * Math.sin(t / 2600 + r.ph));
        const g = ctx.createLinearGradient(0, 0, 0, h * .9);
        g.addColorStop(0, rgba(col.light ? col.lagoon : col.foam, a)); g.addColorStop(1, rgba(col.foam, 0));
        ctx.fillStyle = g;
        const sway = Math.sin(t / 4000 + r.ph) * 30;
        ctx.beginPath(); ctx.moveTo(r.x + sway, 0); ctx.lineTo(r.x + r.wd + sway, 0); ctx.lineTo(r.x + r.wd * .4 + sway - 120, h * .9); ctx.lineTo(r.x - r.wd * .3 + sway - 120, h * .9); ctx.closePath(); ctx.fill();
      });
      // bubbles rising, wobbling as they go
      bubbles.forEach((b, i) => {
        b.y -= b.v * dt; if (b.y < -10) bubbles[i] = b = bubble(h + 10);
        const x = b.x + Math.sin(t / 900 + b.ph) * b.wob, fade = Math.min(1, b.y / (h * .35));
        ctx.lineWidth = 1.2;
        ctx.strokeStyle = rgba(col.light ? col.lagoon : col.foam, (col.light ? .45 : .35) * fade);
        ctx.beginPath(); ctx.arc(x, b.y, b.r, 0, 7); ctx.stroke();
        ctx.fillStyle = rgba(col.foam, .25 * fade);
        ctx.beginPath(); ctx.arc(x - b.r * .35, b.y - b.r * .35, b.r * .25, 0, 7); ctx.fill();
      });
      raf = seen && !document.hidden ? requestAnimationFrame(frame) : 0;
    }
    const start = () => { if (!raf) { last = 0; raf = requestAnimationFrame(frame); } };
    colours(); size(); start();
    addEventListener("resize", () => { size(); start(); });
    document.addEventListener("visibilitychange", start);
    new IntersectionObserver(e => { seen = e[0].isIntersecting; if (seen) start(); }).observe(cv);
    new MutationObserver(colours).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
  }

  // ---------- count up a figure, keeping its words and units ----------
  const NUM = /-?\d[\d,]*(\.\d+)?/;
  function countUp(el) {
    if (el.dataset.moCounted) return;
    // the first piece of text in the figure that holds a number
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let node = null, m = null;
    while (tw.nextNode()) { m = NUM.exec(tw.currentNode.nodeValue); if (m) { node = tw.currentNode; break; } }
    if (!node) return;                                   // no figure yet: try again when it arrives
    const text = node.nodeValue, target = parseFloat(m[0].replace(/,/g, ""));
    if (!isFinite(target) || target === 0) return;
    el.dataset.moCounted = "1";
    const dec = m[1] ? m[1].length - 1 : 0, comma = m[0].includes(",") || Math.abs(target) >= 1e4;
    const before = text.slice(0, m.index), after = text.slice(m.index + m[0].length);
    const f = v => before + v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec, useGrouping: comma }) + after;
    const t0 = performance.now(), dur = 1300;
    let shown = text;
    (function step(t) {
      if (!node.isConnected || node.nodeValue !== shown) return;   // the page changed it: stop
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      shown = k < 1 ? f(target * e) : text;
      node.nodeValue = shown;
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  // ---------- grow meters and bars from zero ----------
  function grow(scope) {
    scope.querySelectorAll(".meter i, .duo .t i, .hbar .fill, .bar > *, .sbar > *").forEach((el, i) => {
      if (el.dataset.moGrown) return;
      el.dataset.moGrown = "1";
      const w = el.style.width, flex = el.style.flex;
      if (!w && !flex) return;                           // only bars sized by the page's own figures
      el.style.transition = "none"; el.style.width = "0"; if (flex) el.style.flex = "0 0 0";
      void el.offsetWidth;
      el.style.transition = `width 1s cubic-bezier(.2,.7,.2,1) ${Math.min(i, 8) * 40}ms, flex 1s cubic-bezier(.2,.7,.2,1) ${Math.min(i, 8) * 40}ms`;
      el.style.width = w; if (flex) el.style.flex = flex;
    });
    scope.querySelectorAll(".waffle").forEach(wf => {
      if (wf.dataset.moGrown) return; wf.dataset.moGrown = "1";
      [...wf.children].forEach((sq, i) => { sq.style.animation = `mo-pop .4s ease ${Math.min(i, 200) * 6}ms both`; });
    });
  }

  // ---------- fade in as things come into view ----------
  const FIGS = ".stat .n, .pcard .big, .split .big, .upd-big";
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target;
    el.classList.add("mo-in");
    el.querySelectorAll(FIGS).forEach(countUp);
    if (el.matches(FIGS)) countUp(el);
    grow(el);
    io.unobserve(el);
  }), { threshold: 0, rootMargin: "0px 0px -8% 0px" });

  function watch() {
    document.querySelectorAll("main section, .pcard, .upd, .stat, .chap-head, .callout").forEach(el => {
      if (el.dataset.moWatch || el.closest(".hero")) return;
      el.dataset.moWatch = "1";
      // only things below the fold fade in, so nothing on screen at load flickers
      if (el.getBoundingClientRect().top > innerHeight * .9) el.classList.add("mo-reveal");
      io.observe(el);
    });
  }
  // figures and cards are often filled in after the data arrives, so look again when the page changes
  watch();
  let pending = false;
  new MutationObserver(() => {
    if (pending) return; pending = true;
    requestAnimationFrame(() => {
      pending = false; watch();
      document.querySelectorAll(".mo-in").forEach(el => { el.querySelectorAll(FIGS).forEach(countUp); grow(el); });
    });
  }).observe(document.querySelector("main") || document.body, { childList: true, subtree: true });
})();
