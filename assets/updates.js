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
      if (it != null) lines.push(`Interest paid so far this year reached ${M(it)}${p && pv("interest_costs") != null && it > pv("interest_costs") ? `, ${M(it - pv("interest_costs"))} more than a week earlier` : ""}.`);
      out.push({ type: "budget", d: r.d,
        title: gap > 0 ? `${M(gap)} more spent than collected so far this year` : `${M(-gap)} more collected than spent so far this year`,
        lead: `By ${dayLabel(r.d)} the government had spent ${M(exp)} and collected ${M(rev)} since 1 January.`,
        lines, link: `budget.html?p=${r.d}`, linkText: "See that week's figures", period: `Figures to ${dayLabel(r.d)}${r.w ? `, week ${r.w}` : ""}` });
    });

    // fuel imports, monthly
    const F = S.fuel_imports?.points || [], IMP = Object.fromEntries((S.imports_goods?.points || []).map(x => [ym(x.date), x.value]));
    const FBY = Object.fromEntries(F.map(x => [ym(x.date), x.value]));
    F.forEach(x => {
      const k = ym(x.date), ly = FBY[sameMonthLastYear(x.date)], c = chg(x.value, ly), share = IMP[k] ? 100 * x.value / IMP[k] : null;
      out.push({ type: "fuel", d: x.date, title: `Fuel imports cost ${usd(x.value, x.date)} in ${mLabel(x.date)}`,
        lead: c != null ? `That is ${chgTxt(c)} on the same month a year earlier.` : "",
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
        out.push({ type: "revenue", d: date, title: `MIRA collected ${m(tot, date)} in ${mLabel(date)}`,
          lead: c != null ? `That is ${chgTxt(c)} on the same month a year earlier.` : "",
          lines: dsh && dsh < 100 ? [`About ${fmt(dsh, 0)}% of it was paid in US dollars.`] : [],
          link: `revenue.html?p=${k}`, linkText: "See that month", period: mLabel(date) });
      });
    }

    // official debt, quarterly
    const T = (S.total?.points || []).filter(x => x.value > 0), G = Object.fromEntries((S.debt_to_gdp?.points || []).map(x => [x.date, pct(x.value)]));
    T.forEach((x, i) => {
      const p = T[i - 1], dlt = p ? x.value - p.value : null;
      out.push({ type: "debt", d: x.date, title: `Official debt reached ${m(x.value, x.date)} at the end of ${mLabel(x.date)}`,
        lead: dlt != null ? `It ${dlt >= 0 ? "rose" : "fell"} by ${m(Math.abs(dlt), x.date)} in three months.` : "",
        lines: G[x.date] ? [`That is ${fmt(G[x.date], 1)}% of GDP, the value of everything the country produces in a year.`] : [],
        link: "./", linkText: "See the debt clock", period: `End of ${mLabel(x.date)}` });
    });

    // police cases, monthly
    const C = priorities?.crime;
    if (C?.monthly) Object.entries(C.monthly).forEach(([y, months]) => Object.entries(months).forEach(([mo, cats]) => {
      const date = new Date(Date.UTC(Number(y), Number(mo), 0)).toISOString().slice(0, 10), list = Object.entries(cats).sort((a, b) => b[1] - a[1]);
      const tot = list.reduce((s, [, n]) => s + n, 0); if (!tot) return;
      out.push({ type: "police", d: date, title: `${fmt(tot)} cases reported to the police in ${mLabel(date)}`,
        lead: `About one every ${fmt(Math.round(new Date(date).getUTCDate() * 1440 / tot))} minutes.`,
        lines: [`The most common were ${list.slice(0, 3).map(([c, n]) => `${c.toLowerCase()} (${fmt(n)})`).join(", ")}.`],
        link: "priorities.html", linkText: "See the police figures", period: mLabel(date) });
    }));

    return out.sort((a, b) => b.d.localeCompare(a.d) || Object.keys(TYPES).indexOf(a.type) - Object.keys(TYPES).indexOf(b.type));
  }

  const card = e => { const t = TYPES[e.type];
    return `<article class="upd" style="--c:${t.color}">${MV.icon(t.icon)}<div class="upd-b"><div class="upd-tag"><b>${t.label}</b><span>${e.period}</span></div>
      <h3>${e.title}</h3>${e.lead ? `<p>${e.lead}</p>` : ""}${e.lines.map(l => `<p>${l}</p>`).join("")}<a class="upd-go" href="${e.link}">${e.linkText} →</a></div></article>`; };

  /** the newest entry of each kind, newest first */
  const latestOfEach = list => Object.keys(TYPES).map(k => list.find(e => e.type === k)).filter(Boolean).sort((a, b) => b.d.localeCompare(a.d));

  return { build, card, latestOfEach, TYPES };
})();
