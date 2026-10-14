/* Builds the list of updates from the site's own data: one entry for every weekly budget report,
   every month of fuel imports and MIRA revenue, every quarter of official debt, and every month of
   police cases. Used by updates.html and the "Latest updates" strip on the home page. */
window.MVUpdates = (() => {
  const { fmt, mLabel, dayLabel, sym, short } = MV;
  // Dhivehi pages load assets/dv.js first; every sentence below then has a whole-sentence Dhivehi version
  const DV = window.MV_DV || null;
  const CRIME_DV = { "Theft": "ވަގަށް ނެގުން", "Drugs": "މަސްތުވާތަކެތި", "Traffic Accidents": "ޓްރެފިކް އެކްސިޑެންޓް", "Assault": "ޙަމަލާ", "Sexual Offences": "ޖިންސީ ކުށް",
    "Domestic violence": "ގޭތެރޭގެ އަނިޔާ", "Embezzlement": "ޚިޔާނާތް", "Fraud": "އޮޅުވާލުން", "Robbery": "ފޭރުން", "Vandalism": "ތަކެތި ހަލާކުކުރުން",
    "Counterfeit and forgery": "ނަކަލީ ތަކެތި ހެދުމާއި ޖަލްސާޒީ", "Lost items": "ގެއްލުނު ތަކެތި", "Cheque Bounce": "ޗެކް ބައުންސްވުން" };
  const crime = c => DV ? (CRIME_DV[c] || c) : c;
  const list3 = a => a.length < 2 ? a.join("") : a.slice(0, -1).join("، ") + " އަދި " + a[a.length - 1];   // Dhivehi "a، b އަދި c"
  const pct = v => v == null ? null : (v < 5 ? v * 100 : v);
  const m = (mvr, d) => MV.moneyNow(mvr, d);
  const usd = (v, d) => sym() + " " + short(MV.fromUSD(v, d));
  const chg = (a, b) => (a != null && b) ? (a / b - 1) * 100 : null;
  const chgTxt = c => c == null ? "" : `${c >= 0 ? "up" : "down"} ${fmt(Math.abs(c), 0)}%`;
  const chgDV = c => `${fmt(Math.abs(c), 0)}% ${c >= 0 ? "އިތުރުވި" : "ދަށްވި"}`;
  const ym = d => d.slice(0, 7);
  const sameMonthLastYear = d => `${Number(d.slice(0, 4)) - 1}${d.slice(4, 7)}`;
  const TYPES = {
    budget: { label: DV ? "ހަފްތާގެ ބަޖެޓް" : "Weekly budget", icon: "moneyOut", color: "#f4c95d" },
    revenue: { label: DV ? "ލިބުނު ޓެކްސް" : "Taxes collected", icon: "moneyIn", color: "#3fb8b0" },
    fuel: { label: DV ? "ތެޔޮ އެތެރެކުރުން" : "Fuel imports", icon: "fuel", color: "#ff8a6b" },
    debt: { label: DV ? "ރަސްމީ ދަރަނި" : "Official debt", icon: "chart", color: "#ff5f56" },
    police: { label: DV ? "ފުލުހުންގެ މައްސަލަތައް" : "Police cases", icon: "police", color: "#a9cdd6" },
  };

  function build({ data, budget, revenue, priorities, lenders }) {
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
      if (p && pv("total_expenditure") != null) lines.push(DV ? `ހަފްތާގެ ތެރޭގައި ޚަރަދު ${M(exp - pv("total_expenditure"))} އިތުރުވިއެވެ. ލިބުނު ފައިސާ ${M(rev - pv("revenue_and_grants"))} އިތުރުވިއެވެ.` : `Over the week, spending rose by ${M(exp - pv("total_expenditure"))} and money collected by ${M(rev - pv("revenue_and_grants"))}.`);
      if (it != null) {
        const bn = x => `${sym()} ${fmt(MV.convNow(x * 1e6, r.d) / 1e9, 2)} ${DV ? DV.bn : "bn"}`, di = p && pv("interest_costs") != null ? it - pv("interest_costs") : null;
        if (DV) lines.push(`މި އަހަރު މިހާތަނަށް ދެއްކި އިންޓަރެސްޓް ${bn(it)} އަށް އަރައިފިއެވެ.` + (di == null ? "" : Math.abs(di) < 1 ? " އެއީ ހަފްތާއެއް ކުރިން ހުރި މިންވަރާ ގާތްގަނޑަކަށް އެއްވަރެވެ." : di > 0 ? ` އެއީ ހަފްތާއެއް ކުރިން ހުރި ${bn(pv("interest_costs"))} އަށްވުރެ ${M(di)} އިތުރެވެ.` : ` ކުރީގެ އަދަދުތައް ރަނގަޅުކުރެވުމުން، އެއީ ހަފްތާއެއް ކުރިން ހުރި އަދަދަށްވުރެ ${M(-di)} ދަށެވެ.`));
        else lines.push(`Interest paid so far this year reached ${bn(it)}` + (di == null ? "." : Math.abs(di) < 1 ? ", about the same as a week earlier." : di > 0 ? `, up ${M(di)} from ${bn(pv("interest_costs"))} a week earlier.` : `, ${M(-di)} lower than a week earlier, as earlier figures were corrected.`));
      }
      const yearRows = R.slice(0, i + 1).filter(x => x.d.slice(0, 4) === r.d.slice(0, 4));
      out.push({ type: "budget", d: r.d, big: (gap > 0 ? "−" : "+") + M(Math.abs(gap)).replace(/^\S+ /, `${sym()} `), bigLabel: DV ? (gap > 0 ? "މިހާތަނަށް ތަފާތު" : "މިހާތަނަށް އިތުރު") : gap > 0 ? "gap so far" : "ahead so far",
        spark: yearRows.map(x => Math.abs((x.v.total_expenditure?.[0] || 0) - (x.v.revenue_and_grants?.[0] || 0))), sparkCap: DV ? "މި އަހަރު، ހަފްތާއިން ހަފްތާއަށް" : "week by week this year",
        title: DV ? (() => { if (!p || pv("total_expenditure") == null) return `${r.d.slice(0, 4)} ގެ ފުރަތަމަ ހަފްތާގެ އަދަދުތައް`; const pg = pv("total_expenditure") - pv("revenue_and_grants"), dg = gap - pg;
          if (gap > 0 && pg > 0) return Math.abs(dg) < 1 ? "ޚަރަދާއި އާމްދަނީގެ ތަފާތު މި ހަފްތާގައި ބަދަލެއް ނުވި" : `ޚަރަދާއި އާމްދަނީގެ ތަފާތު މި ހަފްތާގައި ${M(Math.abs(dg))} ${dg > 0 ? "ބޮޑުވި" : "ކުޑަވި"}`;
          if (gap > 0) return "މި ހަފްތާގައި ޚަރަދު އާމްދަނީއަށްވުރެ ބޮޑުވި"; return pg > 0 ? "މި ހަފްތާގައި އާމްދަނީ ޚަރަދަށްވުރެ ބޮޑުވި" : "މި އަހަރު އަދިވެސް އާމްދަނީ ޚަރަދަށްވުރެ ބޮޑު"; })()
        : (() => { if (!p || pv("total_expenditure") == null) return `The first weekly figures of ${r.d.slice(0, 4)}`; const pg = pv("total_expenditure") - pv("revenue_and_grants"), dg = gap - pg;
          if (gap > 0 && pg > 0) return Math.abs(dg) < 1 ? "The gap between spending and income held steady this week" : `The gap between spending and income ${dg > 0 ? "grew" : "shrank"} by ${M(Math.abs(dg))} this week`;
          if (gap > 0) return "Spending moved ahead of income this week"; return pg > 0 ? "Income moved ahead of spending this week" : "Income is still ahead of spending this year"; })(),
        lead: DV ? `1 ޖަނަވަރީއިން ${dayLabel(r.d)} އާ ހަމައަށް ސަރުކާރުން ${M(exp)} ހޭދަކޮށްފައިވެއެވެ. އަދި ${M(rev)} ލިބިފައިވެއެވެ.` : `By ${dayLabel(r.d)} the government had spent ${M(exp)} and collected ${M(rev)} since 1 January.`,
        lines, link: `budget.html?p=${r.d}`, linkText: DV ? "އެ ހަފްތާގެ އަދަދުތައް ބައްލަވާ" : "See that week's figures", period: DV ? `${dayLabel(r.d)} އާ ހަމައަށް${r.w ? `، ${r.w} ވަނަ ހަފްތާ` : ""}` : `Figures to ${dayLabel(r.d)}${r.w ? `, week ${r.w}` : ""}` });
    });

    // fuel imports, monthly
    const F = S.fuel_imports?.points || [], IMP = Object.fromEntries((S.imports_goods?.points || []).map(x => [ym(x.date), x.value]));
    const FBY = Object.fromEntries(F.map(x => [ym(x.date), x.value]));
    F.forEach(x => {
      const k = ym(x.date), ly = FBY[sameMonthLastYear(x.date)], c = chg(x.value, ly), share = IMP[k] ? 100 * x.value / IMP[k] : null;
      const fi = F.indexOf(x);
      out.push({ type: "fuel", d: x.date, big: usd(x.value, x.date), bigLabel: DV ? `ތެލުގެ ބިލު، ${mLabel(x.date)}` : `fuel bill, ${mLabel(x.date)}`, spark: F.slice(Math.max(0, fi - 12), fi + 1).map(y => y.value), sparkCap: DV ? "ފަހުގެ 13 މަސް" : "last 13 months",
        title: DV ? (c != null ? `ތެލުގެ ބިލު، ކުރީ އަހަރާ އަޅާބަލާއިރު ${chgDV(c)}` : `${mLabel(x.date)} ގެ ތެލުގެ ބިލު`) : c != null ? `The fuel bill was ${chgTxt(c)} on a year earlier` : `The fuel bill for ${mLabel(x.date)}`,
        lead: DV ? `${mLabel(x.date)} ގައި ބޭރުން ގެނައި ޑީސަލް، ޕެޓްރޯލް އަދި އެހެނިހެން ތެލަށް ޤައުމުން ދެއްކި އަގެވެ.` : `What the country paid for imported diesel, petrol and other fuel in ${mLabel(x.date)}.`,
        lines: share ? [DV ? `އެ މަހު ޤައުމަށް އެތެރެކުރި ހުރިހާ މުދަލުގެ އަގުގެ ${fmt(share, 0)}% އަކީ ތެލުގެ އަގެވެ.` : `Fuel was ${fmt(share, 0)}% of all goods brought into the country that month.`] : [],
        link: `fuel.html?p=${k}`, linkText: DV ? "އެ މަސް ބައްލަވާ" : "See that month", period: mLabel(x.date) });
    });

    // MIRA revenue, monthly
    if (revenue?.months) {
      const keys = (revenue.groups || []).map(g => g.key), RIDX = Object.fromEntries(revenue.months.map((k, i) => [k, i]));
      revenue.months.forEach((k, i) => {
        const tot = revenue.total?.mvr?.[i]; if (!tot) return;
        const date = new Date(Date.UTC(Number(k.slice(0, 4)), Number(k.slice(5, 7)), 0)).toISOString().slice(0, 10);
        const li = RIDX[`${Number(k.slice(0, 4)) - 1}-${k.slice(5, 7)}`], c = li != null ? chg(tot, revenue.total.mvr[li]) : null;
        // the dollar part in rufiyaa at that month's rate, each tax capped at its own total, as on the taxes page
        const dol = keys.reduce((a, g) => { const u = revenue.usd?.[g]?.[i]; return u == null ? a : a + Math.min(revenue.mvr?.[g]?.[i] || 0, u * MV.rateAt(date)); }, 0), dsh = dol ? 100 * dol / tot : null;
        out.push({ type: "revenue", d: date, big: m(tot, date), bigLabel: DV ? `ލިބުނު، ${mLabel(date)}` : `collected, ${mLabel(date)}`, spark: revenue.total.mvr.slice(Math.max(0, i - 12), i + 1), sparkCap: DV ? "ފަހުގެ 13 މަސް" : "last 13 months",
          title: DV ? (c != null ? `ޓެކްސްއިން ލިބުނު ފައިސާ، ކުރީ އަހަރާ އަޅާބަލާއިރު ${chgDV(c)}` : `${mLabel(date)} ގައި ޓެކްސްއިން ލިބުނު ފައިސާ`) : c != null ? `Tax collections were ${chgTxt(c)} on a year earlier` : `Tax collections for ${mLabel(date)}`,
          lead: DV ? `ޓެކްސް އޮފީސް ކަމަށްވާ MIRA އިން ${mLabel(date)} ގައި ހޯދި ފައިސާއެވެ.` : `What MIRA, the tax office, collected in ${mLabel(date)}.`,
          lines: (dsh && dsh < 100 ? [DV ? `އޭގެ ގާތްގަނޑަކަށް ${fmt(dsh, 0)}% ދައްކާފައިވަނީ އެމެރިކާ ޑޮލަރުންނެވެ.` : `About ${fmt(dsh, 0)}% of it was paid in US dollars.`] : []).concat([`<span class="term" role="button" tabindex="0" data-term="taxrev">${DV ? "މިއީ ސަރުކާރުގެ ހުރިހާ އާމްދަނީއެއް ނޫން ސަބަބު" : "Why this isn't all of the government's income"}</span>`]),
          link: `revenue.html?p=${k}`, linkText: DV ? "އެ މަސް ބައްލަވާ" : "See that month", period: mLabel(date) });
      });
    }

    // official debt, quarterly
    const T = (S.total?.points || []).filter(x => x.value > 0), G = Object.fromEntries((S.debt_to_gdp?.points || []).map(x => [x.date, pct(x.value)]));
    const at = k => Object.fromEntries((S[k]?.points || []).map(x => [x.date, x.value])), EX = at("external"), DO = at("domestic"), OW = lenders?.owed;
    T.forEach((x, i) => {
      const p = T[i - 1], dlt = p ? x.value - p.value : null;
      // where the change came from: abroad or at home, and (from the Debt Bulletin) the biggest repayments
      const why = [];
      if (p && EX[x.date] != null && EX[p.date] != null && DO[x.date] != null && DO[p.date] != null) {
        const de = EX[x.date] - EX[p.date], dd = DO[x.date] - DO[p.date], mv = v => m(Math.abs(v), x.date);
        if (DV) why.push(`ބޭރުގެ ދަރަނި ${mv(de)} ${de >= 0 ? "އިތުރުވިއެވެ" : "މަދުވިއެވެ"}. ދާޚިލީ ދަރަނި ${mv(dd)} ${dd >= 0 ? "އިތުރުވިއެވެ" : "މަދުވިއެވެ"}.`
          + (de < -2e9 && dd > -de / 3 ? " ބޭރަށް ބޮޑެތި ފައިސާތައް އަނބުރާ ދެއްކި ދުވަސްވަރު، ރާއްޖޭގެ ތެރެއިން ނަގާ ދަރަނި އިތުރުވިއެވެ." : ""));
        else why.push(`Debt owed abroad ${de >= 0 ? "rose" : "fell"} by ${mv(de)}, and debt owed at home ${dd >= 0 ? "rose" : "fell"} by ${mv(dd)}.`
          + (de < -2e9 && dd > -de / 3 ? " Large repayments abroad were made while borrowing at home rose." : ""));
      }
      if (p && OW?.quarters?.includes(x.date) && OW.quarters.includes(p.date)) {
        const drops = [];
        ["loans", "guarantees"].forEach(k => Object.entries(OW[k] || {}).forEach(([l, v]) => { const dl = (v[p.date] || 0) - (v[x.date] || 0); if (dl > 500) drops.push([l, dl]); }));
        drops.sort((a, b) => b[1] - a[1]);
        if (drops.length && DV) why.push(`މާލިއްޔަތު ވުޒާރާގެ Debt Bulletin ގައިވާ ގޮތުން، ބޭރަށް ދައްކަންޖެހޭ ދަރަނި އެންމެ ގިނައިން މަދުވީ ${list3(drops.slice(0, 2).map(([l, v]) => `<bdi>${l}</bdi> (${m(v * 1e6, x.date)} މަދުވި)`))} ގެ ދަރަންޏެވެ.`);
        else if (drops.length) why.push(`Abroad, what was owed fell most for ${drops.slice(0, 2).map(([l, v]) => `${l} (down ${m(v * 1e6, x.date)})`).join(" and ")}, according to Ministry of Finance's Debt Bulletin.`);
      }
      out.push({ type: "debt", d: x.date, big: m(x.value, x.date), bigLabel: DV ? `${mLabel(x.date)} ގެ ނިޔަލަށް ދަރަނި` : `owed at the end of ${mLabel(x.date)}`, spark: T.slice(Math.max(0, i - 11), i + 1).map(y => y.value), sparkCap: DV ? "ފަހުގެ 3 އަހަރު" : "last 3 years",
        title: DV ? (dlt != null ? `ތިން މަހު ރަސްމީ ދަރަނި ${m(Math.abs(dlt), x.date)} ${dlt >= 0 ? "އިތުރުވި" : "މަދުވި"}` : `${mLabel(x.date)} ގެ ރަސްމީ ދަރަނީގެ އަދަދު`) : dlt != null ? `Official debt ${dlt >= 0 ? "rose" : "fell"} by ${m(Math.abs(dlt), x.date)} in three months` : `The official debt figure for ${mLabel(x.date)}`,
        lead: DV ? "ތިން މަހުން އެއްފަހަރު ޝާއިޢުކުރާ، އެންމެ ފަހުގެ ރަސްމީ ޖުމްލަ އަދަދެވެ." : `The latest official total, published every three months.`,
        lines: (G[x.date] ? [DV ? `އެއީ ޖީޑީޕީގެ ${fmt(G[x.date], 1)}% އެވެ. ޖީޑީޕީ އަކީ އަހަރެއްގެ ތެރޭގައި ޤައުމުގައި އުފައްދާ ހުރިހާ އެއްޗެއްގެ އަގެވެ.` : `That is ${fmt(G[x.date], 1)}% of GDP, the value of everything the country produces in a year.`] : []).concat(why),
        link: "./", linkText: DV ? "ދަރަނީގެ ގަޑި ބައްލަވާ" : "See the debt clock", period: DV ? `${mLabel(x.date)} ގެ ނިޔަލަށް` : `End of ${mLabel(x.date)}` });
    });

    // police cases, monthly
    const C = priorities?.crime;
    if (C?.monthly) Object.entries(C.monthly).forEach(([y, months]) => Object.entries(months).forEach(([mo, cats]) => {
      const date = new Date(Date.UTC(Number(y), Number(mo), 0)).toISOString().slice(0, 10), list = Object.entries(cats).sort((a, b) => b[1] - a[1]);
      const tot = list.reduce((s, [, n]) => s + n, 0); if (!tot) return;
      // a month still under way counts only the days up to when the figures were read
      const got = C.retrieved || "", days = got.slice(0, 7) === date.slice(0, 7) ? Math.max(1, Number(got.slice(8, 10))) : new Date(date).getUTCDate(), sofar = days < new Date(date).getUTCDate();
      out.push({ type: "police", d: date, big: fmt(tot), bigLabel: DV ? `މައްސަލަ، ${mLabel(date)}` : `cases, ${mLabel(date)}`, spark: [], sparkCap: "", title: DV ? `${mLabel(date)} ގައި އެންމެ ގިނައިން ހުށަހެޅުނީ ${crime(list[0][0])} ގެ މައްސަލަ` : `${list[0][0]} was the most reported case in ${mLabel(date)}`,
        lead: DV ? `${sofar ? "މި މަހު މިހާތަނަށް، " : ""}ގާތްގަނޑަކަށް ކޮންމެ ${fmt(Math.round(days * 1080 / tot))} މިނެޓަކުން މައްސަލައެއް ހުށަހެޅިއެވެ. މި ހިސާބުކުރީ ހޭލައިތިބޭ ގަޑިތައް، ހެނދުނު 6 އިން ރޭގަނޑު 12 އަށް ގުނައިގެންނެވެ.` : `A case was reported about every ${fmt(Math.round(days * 1080 / tot))} minutes${sofar ? ` so far this month` : ""}, counting waking hours from 6 am to midnight.`,
        lines: [DV ? `އެންމެ ގިނައިން ހުށަހެޅުނީ ${list3(list.slice(0, 3).map(([c, n]) => `${crime(c)} (${fmt(n)})`))} ގެ މައްސަލަތަކެވެ.` : `The most common were ${list.slice(0, 3).map(([c, n]) => `${c.toLowerCase()} (${fmt(n)})`).join(", ")}.`],
        link: `priorities.html?cy=${y}&cm=${mo}`, linkText: DV ? "އެ މަހުގެ ފުލުހުންގެ އަދަދުތައް ބައްލަވާ" : "See that month's police figures", period: mLabel(date) });
    }));


    return out.sort((a, b) => b.d.localeCompare(a.d) || Object.keys(TYPES).indexOf(a.type) - Object.keys(TYPES).indexOf(b.type));
  }

  const withFrom = (link, from) => (link = DV ? DV.page(link) : link, !from ? link : link + (link.includes("?") ? "&" : "?") + "from=" + from);
  const card = (e, from) => { const t = TYPES[e.type];
    const viz = e.big ? `<div class="upd-viz"><div class="upd-big">${e.big}</div><div class="upd-bl">${e.bigLabel || ""}</div>${e.spark?.length > 1 ? MV.mini.spark(e.spark, t.color, { left: e.sparkCap }) : ""}</div>` : "";
    return `<article class="upd" style="--c:${t.color}">${MV.icon(t.icon)}<div class="upd-b"><div class="upd-tag"><b>${t.label}</b><span>${e.period}</span></div>
      <h3>${e.title}</h3>${e.lead ? `<p>${e.lead}</p>` : ""}${e.lines.map(l => `<p>${l}</p>`).join("")}<a class="upd-go" href="${withFrom(e.link, from)}">${e.linkText} ${DV ? "←" : "→"}</a></div>${viz}</article>`; };

  /** the newest entry of each kind, newest first */
  const latestOfEach = list => Object.keys(TYPES).map(k => list.find(e => e.type === k)).filter(Boolean).sort((a, b) => b.d.localeCompare(a.d));

  return { build, card, latestOfEach, TYPES };
})();
