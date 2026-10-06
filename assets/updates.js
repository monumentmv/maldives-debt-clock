/* Builds the list of updates from the site's own data: one entry for every weekly budget report,
   every month of fuel imports and MIRA revenue, every quarter of official debt, and every month of
   police cases. Used by updates.html and the "Latest updates" strip on the home page. */
window.MVUpdates = (() => {
  const { fmt, mLabel, dayLabel, sym, short } = MV;
  const pct = v => v == null ? null : (v < 5 ? v * 100 : v);
  const m = (mvr, d) => MV.moneyNow(mvr, d);
  const usd = (v, d) => sym() + " " + short(MV.fromUSD(v, d));
  const chg = (a, b) => (a != null && b) ? (a / b - 1) * 100 : null;
  const chgTxt = c => c == null ? "" : `${c >= 0 ? "up" : "down"} ${fmt(Math.abs(c), 0)}%`;
  const ym = d => d.slice(0, 7);
  const sameMonthLastYear = d => `${Number(d.slice(0, 4)) - 1}${d.slice(4, 7)}`;
  const TYPES = {
    budget: { label: "Weekly budget", icon: "moneyOut", color: "#f4c95d" },
    revenue: { label: "Taxes collected", icon: "moneyIn", color: "#3fb8b0" },
    fuel: { label: "Fuel imports", icon: "fuel", color: "#ff8a6b" },
    debt: { label: "Official debt", icon: "chart", color: "#ff5f56" },
    police: { label: "Police cases", icon: "police", color: "#a9cdd6" },
  };

  function build({ data, budget, revenue, priorities }) {
    const out = [];
    const S = data?.series || {};

    // weekly budget reports
    const R = budget?.reports || [];
    R.forEach((r, i) => {
      const v = k => r.v?.[k]?.[0], p = R[i - 1] && R[i - 1].d.slice(0, 4) === r.d.slice(0, 4) ? R[i - 1] : null, pv = k => p?.v?.[k]?.[0];
      const rev = v("revenue_and_grants"), exp = v("total_expenditure"), it = v("interest_costs");
      if (rev == null || exp == null) return;
      const M = x => m(x * 1e6, r.d), gap = exp - rev;
      const lines = [];
      if (p && pv("total_expenditure") != null) lines.push(`Over the week, spending rose by ${M(exp - pv("total_expenditure"))} and money collected by ${M(rev - pv("revenue_and_grants"))}.`);
      if (it != null) {
        const bn = x => `${sym()} ${fmt(MV.convNow(x * 1e6, r.d) / 1e9, 2)} bn`, di = p && pv("interest_costs") != null ? it - pv("interest_costs") : null;
        lines.push(`Interest paid so far this year reached ${bn(it)}` + (di == null ? "." : Math.abs(di) < 1 ? ", about the same as a week earlier." : di > 0 ? `, up ${M(di)} from ${bn(pv("interest_costs"))} a week earlier.` : `, ${M(-di)} lower than a week earlier, as earlier figures were corrected.`));
      }
      const yearRows = R.slice(0, i + 1).filter(x => x.d.slice(0, 4) === r.d.slice(0, 4));
      out.push({ type: "budget", d: r.d, big: (gap > 0 ? "−" : "+") + M(Math.abs(gap)).replace(/^\S+ /, `${sym()} `), bigLabel: gap > 0 ? "gap so far" : "ahead so far",
        spark: yearRows.map(x => Math.abs((x.v.total_expenditure?.[0] || 0) - (x.v.revenue_and_grants?.[0] || 0))), sparkCap: "week by week this year",
        title: (() => { if (!p || pv("total_expenditure") == null) return `The first weekly figures of ${r.d.slice(0, 4)}`; const pg = pv("total_expenditure") - pv("revenue_and_grants"), dg = gap - pg;
          if (gap > 0 && pg > 0) return Math.abs(dg) < 1 ? "The gap between spending and income held steady this week" : `The gap between spending and income ${dg > 0 ? "grew" : "shrank"} by ${M(Math.abs(dg))} this week`;
          if (gap > 0) return "Spending moved ahead of income this week"; return pg > 0 ? "Income moved ahead of spending this week" : "Income is still ahead of spending this year"; })(),
        lead: `By ${dayLabel(r.d)} the government had spent ${M(exp)} and collected ${M(rev)} since 1 January.`,
        lines, link: `budget.html?p=${r.d}`, linkText: "See that week's figures", period: `Figures to ${dayLabel(r.d)}${r.w ? `, week ${r.w}` : ""}` });
    });

    // fuel imports, monthly
    const F = S.fuel_imports?.points || [], IMP = Object.fromEntries((S.imports_goods?.points || []).map(x => [ym(x.date), x.value]));
    const FBY = Object.fromEntries(F.map(x => [ym(x.date), x.value]));
    F.forEach(x => {
      const k = ym(x.date), ly = FBY[sameMonthLastYear(x.date)], c = chg(x.value, ly), share = IMP[k] ? 100 * x.value / IMP[k] : null;
      const fi = F.indexOf(x);
      out.push({ type: "fuel", d: x.date, big: usd(x.value, x.date), bigLabel: `fuel bill, ${mLabel(x.date)}`, spark: F.slice(Math.max(0, fi - 12), fi + 1).map(y => y.value), sparkCap: "last 13 months",
        title: c != null ? `The fuel bill was ${chgTxt(c)} on a year earlier` : `The fuel bill for ${mLabel(x.date)}`,
        lead: `What the country paid for imported diesel, petrol and other fuel in ${mLabel(x.date)}.`,
        lines: share ? [`Fuel was ${fmt(share, 0)}% of all goods brought into the country that month.`] : [],
        link: `fuel.html?p=${k}`, linkText: "See that month", period: mLabel(x.date) });
    });

    // MIRA revenue, monthly
    if (revenue?.months) {
      const keys = (revenue.groups || []).map(g => g.key), RIDX = Object.fromEntries(revenue.months.map((k, i) => [k, i]));
      revenue.months.forEach((k, i) => {
        const tot = revenue.total?.mvr?.[i]; if (!tot) return;
        const date = new Date(Date.UTC(Number(k.slice(0, 4)), Number(k.slice(5, 7)), 0)).toISOString().slice(0, 10);
        const li = RIDX[`${Number(k.slice(0, 4)) - 1}-${k.slice(5, 7)}`], c = li != null ? chg(tot, revenue.total.mvr[li]) : null;
        const dol = keys.reduce((a, g) => a + (revenue.usd?.[g]?.[i] || 0), 0), dsh = dol ? 100 * dol / tot : null;
        out.push({ type: "revenue", d: date, big: m(tot, date), bigLabel: `collected, ${mLabel(date)}`, spark: revenue.total.mvr.slice(Math.max(0, i - 12), i + 1), sparkCap: "last 13 months",
          title: c != null ? `Tax collections were ${chgTxt(c)} on a year earlier` : `Tax collections for ${mLabel(date)}`,
          lead: `What MIRA, the tax office, collected in ${mLabel(date)}.`,
          lines: (dsh && dsh < 100 ? [`About ${fmt(dsh, 0)}% of it was paid in US dollars.`] : []).concat([`<span class="term" role="button" tabindex="0" data-term="taxrev">Why this isn't all of the government's income</span>`]),
          link: `revenue.html?p=${k}`, linkText: "See that month", period: mLabel(date) });
      });
    }

    // official debt, quarterly
    const T = (S.total?.points || []).filter(x => x.value > 0), G = Object.fromEntries((S.debt_to_gdp?.points || []).map(x => [x.date, pct(x.value)]));
    T.forEach((x, i) => {
      const p = T[i - 1], dlt = p ? x.value - p.value : null;
      out.push({ type: "debt", d: x.date, big: m(x.value, x.date), bigLabel: `owed at the end of ${mLabel(x.date)}`, spark: T.slice(Math.max(0, i - 11), i + 1).map(y => y.value), sparkCap: "last 3 years",
        title: dlt != null ? `Official debt ${dlt >= 0 ? "rose" : "fell"} by ${m(Math.abs(dlt), x.date)} in three months` : `The official debt figure for ${mLabel(x.date)}`,
        lead: `The latest official total, published every three months.`,
        lines: G[x.date] ? [`That is ${fmt(G[x.date], 1)}% of GDP, the value of everything the country produces in a year.`] : [],
        link: "./", linkText: "See the debt clock", period: `End of ${mLabel(x.date)}` });
    });

    // police cases, monthly
    const C = priorities?.crime;
    if (C?.monthly) Object.entries(C.monthly).forEach(([y, months]) => Object.entries(months).forEach(([mo, cats]) => {
      const date = new Date(Date.UTC(Number(y), Number(mo), 0)).toISOString().slice(0, 10), list = Object.entries(cats).sort((a, b) => b[1] - a[1]);
      const tot = list.reduce((s, [, n]) => s + n, 0); if (!tot) return;
      out.push({ type: "police", d: date, big: fmt(tot), bigLabel: `cases, ${mLabel(date)}`, spark: [], sparkCap: "", title: `${list[0][0]} was the most reported case in ${mLabel(date)}`,
        lead: `About one every ${fmt(Math.round(new Date(date).getUTCDate() * 1440 / tot))} minutes.`,
        lines: [`The most common were ${list.slice(0, 3).map(([c, n]) => `${c.toLowerCase()} (${fmt(n)})`).join(", ")}.`],
        link: "priorities.html", linkText: "See the police figures", period: mLabel(date) });
    }));

    return out.sort((a, b) => b.d.localeCompare(a.d) || Object.keys(TYPES).indexOf(a.type) - Object.keys(TYPES).indexOf(b.type));
  }

  const withFrom = (link, from) => !from ? link : link + (link.includes("?") ? "&" : "?") + "from=" + from;
  const card = (e, from) => { const t = TYPES[e.type];
    const viz = e.big ? `<div class="upd-viz"><div class="upd-big">${e.big}</div><div class="upd-bl">${e.bigLabel || ""}</div>${e.spark?.length > 1 ? MV.mini.spark(e.spark, t.color, { left: e.sparkCap }) : ""}</div>` : "";
    return `<article class="upd" style="--c:${t.color}">${MV.icon(t.icon)}<div class="upd-b"><div class="upd-tag"><b>${t.label}</b><span>${e.period}</span></div>
      <h3>${e.title}</h3>${e.lead ? `<p>${e.lead}</p>` : ""}${e.lines.map(l => `<p>${l}</p>`).join("")}<a class="upd-go" href="${withFrom(e.link, from)}">${e.linkText} →</a></div>${viz}</article>`; };

  /** the newest entry of each kind, newest first */
  const latestOfEach = list => Object.keys(TYPES).map(k => list.find(e => e.type === k)).filter(Boolean).sort((a, b) => b.d.localeCompare(a.d));

  return { build, card, latestOfEach, TYPES };
})();
