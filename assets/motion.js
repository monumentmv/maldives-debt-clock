/* Maldives National Debt Clock: a little motion, only where it helps read the figures.
   - headline figures count up the first time they come into view
   - meters and bars grow to their value
   Nothing moves for readers who ask for reduced motion. */
(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

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
  }

  // ---------- run both as things come into view ----------
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
