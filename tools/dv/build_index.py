"""Dhivehi home page (dv.html) from index.html. See common.py."""
from common import Page

p = Page("clock")
p.head("ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި", "ދިވެހި ސަރުކާރުގެ ދަރަނި، ވަގުތުން ވަގުތަށް. ރަސްމީ އަދަދުތަކުން.")
p.header()

# ---- hero ----
p.R('aria-label="Debt clock">', 'aria-label="ދަރަނީގެ ގަޑި">')
p.R('<b id="ratioVal">…</b>of GDP</div>', '<b id="ratioVal">…</b>ޖީޑީޕީގެ</div>')
p.R('<h1>Maldives National Debt Clock</h1>', '<h1>ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި</h1>')
p.R('<p class="asof">As of <time id="mvTime">…</time> in Malé <button type="button" class="what-in-btn" id="whatIn">What\'s in this number?</button></p>',
  '<p class="asof">މާލޭ ވަގުތުން <time id="mvTime">…</time> <button type="button" class="what-in-btn" id="whatIn">މި އަދަދުގައި ހިމެނެނީ ކޮބާ؟</button></p>')
p.R('<b>Who is this money owed to?</b><small>Explore the map of every lender and every loan</small>', '<b>މި ދަރަނި ދައްކަންޖެހެނީ ކާކަށް؟</b><small>ދަރަނި ދިން ކޮންމެ ފަރާތަކާއި ކޮންމެ ލޯނެއް ފެންނަ ނަގުޝާ</small>')
p.R('Loading the latest figures from Maldives Monetary Authority.', 'މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީގެ އެންމެ ފަހުގެ އަދަދުތައް ލޯޑުވަނީ…')
p.R('<div class="l">owed for every Maldivian citizen, rising every second</div>', '<div class="l">ކޮންމެ ދިވެހި ރައްޔިތަކަށް ބަހާލާއިރު ދަރަނި. ކޮންމެ ސިކުންތެއްގައި އިތުރުވަމުން</div>')
p.R('id="perSecondLbl">added to the debt each second, on the pace of the last year</div>', 'id="perSecondLbl">ކޮންމެ ސިކުންތެއްގައި ދަރަންޏަށް އިތުރުވާ މިންވަރު، ފާއިތުވި އަހަރުގެ މިންވަރުން</div>')
p.R('id="interestLbl">spent on interest and financing costs every day</div>', 'id="interestLbl">ކޮންމެ ދުވަހަކު އިންޓަރެސްޓާއި ފައިނޭންސިންގ ޚަރަދަށް ހޭދަވާ ފައިސާ</div>')

p.R('<span class="owe-arr" aria-hidden="true">→</span>', '<span class="owe-arr" aria-hidden="true">←</span>')
# ---- chapters (static) ----
p.R('<h2>Want to know more?</h2>\n      <p>Each question opens up the charts and figures behind it.</p>', '<h2>އިތުރަށް ބައްލަވަން ބޭނުންތޯ؟</h2>\n      <p>ކޮންމެ ސުވާލަކަށް ފިތާލުމުން، އޭގެ ފަހަތުގައިވާ ޗާޓުތަކާއި އަދަދުތައް ފެންނާނެއެވެ.</p>') if '<h2>Want to know more?</h2>\n      <p>' in p.s else None
p.s = p.s.replace('<h2>Want to know more?</h2>', '<h2>އިތުރަށް ބައްލަވަން ބޭނުންތޯ؟</h2>').replace('<p>Each question opens up the charts and figures behind it.</p>', '<p>ކޮންމެ ސުވާލަކަށް ފިތާލުމުން، އޭގެ ފަހަތުގައިވާ ޗާޓުތަކާއި އަދަދުތައް ފެންނާނެއެވެ.</p>')
p.R('<span class="chap-q">Who is the money owed to?</span><span class="chap-a" id="aOwed">Lenders at home and abroad.</span>', '<span class="chap-q">ދަރަނި ދައްކަންޖެހެނީ ކާކަށް؟</span><span class="chap-a" id="aOwed">ރާއްޖޭގައާއި ބޭރުގައި ދަރަނި ދިން ފަރާތްތަކަށް.</span>')
p.s = p.s.replace('<span class="show">Show the details</span><span class="hide">Hide the details</span>', '<span class="show">ތަފްސީލު ދައްކާ</span><span class="hide">ތަފްސީލު ފޮރުވާ</span>')
p.R('<p>Domestic debt is owed to lenders inside Maldives, mostly banks, the central bank and the pension fund. Foreign debt is owed abroad, to other governments, development banks and bondholders. <a href="#" class="term" data-term="guaranteed">Guaranteed debt</a> is borrowed mostly by state-owned companies, from banks and other lenders, with the government promising to pay if they can\'t.</p>',
  '<p>ދާޚިލީ ދަރަނި ދައްކަންޖެހެނީ ރާއްޖޭގެ ތެރޭގެ ފަރާތްތަކަށެވެ. ގިނައިން ބޭންކުތަކާއި، މަރުކަޒީ ބޭންކާއި، ޕެންޝަން ފަންޑަށެވެ. ބޭރުގެ ދަރަނި ދައްކަންޖެހެނީ ބޭރުގެ ސަރުކާރުތަކާއި، ތަރައްޤީގެ ބޭންކުތަކާއި، ބޮންޑު ގަނެފައިވާ ފަރާތްތަކަށެވެ. <a href="#" class="term" data-term="guaranteed">ގެރެންޓީ ދީފައިވާ ދަރަނި</a> ނަގަނީ ގިނައިން ސަރުކާރު ކުންފުނިތަކުންނެވެ. އެ ކުންފުންޏަކަށް ދައްކާނުލެވިއްޖެނަމަ ސަރުކާރުން ދައްކާނެކަމަށް ސަރުކާރުން ވަޢުދުވެފައިވެއެވެ.</p>')
p.R('aria-label="Debt breakdown"', 'aria-label="ދަރަނީގެ ބައިތައް"')
p.R('<span class="t">See who it is owed to, at home and abroad</span>', '<span class="t">ރާއްޖޭގައާއި ބޭރުގައި ދަރަނި ދައްކަންޖެހޭ ފަރާތްތައް ބައްލަވާ (މި ބައި އަދި އިނގިރޭސިން)</span>')
p.R('<span class="chap-q">How did the debt get this big?</span><span class="chap-a" id="aHist">It has grown year after year.</span>', '<span class="chap-q">ދަރަނި މިހާ ބޮޑުވީ ކިހިނެއް؟</span><span class="chap-a" id="aHist">އަހަރުން އަހަރަށް ބޮޑުވަމުން އައިސްފައި.</span>')
p.R('aria-label="Chart view">', 'aria-label="ޗާޓު ބައްލަވާ ގޮތް">')
p.R('data-view="amount" aria-pressed="true">Amount</button>', 'data-view="amount" aria-pressed="true">އަދަދު</button>')
p.R('data-view="ratio" aria-pressed="false">% of GDP</button>', 'data-view="ratio" aria-pressed="false">ޖީޑީޕީގެ %</button>')
p.R('<div class="hint">Hover or tap the chart to see each quarter.</div>', '<div class="hint">ކޮންމެ ކުއާޓަރެއް ބެލުމަށް ޗާޓަށް ފިތާލައްވާ.</div>')
p.R('<span class="chap-q">Why does the government keep borrowing?</span><span class="chap-a" id="aFisc">Most years it spends more than it collects.</span>', '<span class="chap-q">ސަރުކާރުން ދަރަނި ނަގަމުން ދަނީ ކީއްވެ؟</span><span class="chap-a" id="aFisc">ގިނަ އަހަރުތަކުގައި ލިބޭ އާމްދަނީއަށްވުރެ ޚަރަދު ބޮޑު.</span>')
p.R('<div class="l">collected per citizen in a year, in taxes, fees and grants</div>', '<div class="l">އަހަރަކު ކޮންމެ ރައްޔިތަކަށް ބަހާލާއިރު ލިބޭ ފައިސާ (ޓެކްސް، ފީ އަދި އެހީ)</div>')
p.R('<div class="l">spent per citizen in a year</div>', '<div class="l">އަހަރަކު ކޮންމެ ރައްޔިތަކަށް ބަހާލާއިރު ހިނގާ ޚަރަދު</div>')
p.R('id="gapLbl">gap per citizen, covered by borrowing</div>', 'id="gapLbl">ކޮންމެ ރައްޔިތަކަށް ބަހާލާއިރު ތަފާތު، ދަރަނިން ފުރިހަމަކުރެވޭ</div>')
p.R('<h3>Every second, the government</h3>', '<h3>ކޮންމެ ސިކުންތެއްގައި</h3>')
p.R('<div class="l">collects</div>', '<div class="l">ސަރުކާރަށް ލިބޭ</div>')
p.R('<div class="l">spends</div>', '<div class="l">ސަރުކާރުން ހޭދަކުރާ</div>')
p.R('<h3>Year by year</h3>', '<h3>އަހަރުން އަހަރަށް</h3>')
p.R('<i style="background:#3fb8b0"></i>Revenue</span><span><i style="background:#ff5f56"></i>Spending</span><span style="color:#ff5f56;font-weight:700">Red figure under each year shows the deficit</span>',
  '<i style="background:#3fb8b0"></i>އާމްދަނީ</span><span><i style="background:#ff5f56"></i>ޚަރަދު</span><span style="color:#ff5f56;font-weight:700">ކޮންމެ އަހަރެއްގެ ދަށުގައިވާ ރަތް އަދަދަކީ ޑެފިސިޓް</span>')
p.R('<h3 id="spendHead">Where a year\'s spending goes</h3>', '<h3 id="spendHead">އަހަރެއްގެ ޚަރަދު ހިނގަނީ ކޮންތާކަށް</h3>')
p.R('<span class="chap-q">How does the clock work?</span><span class="chap-a" id="aHow">It starts from the latest official figure and adds debt at the recent pace.</span>', '<span class="chap-q">ގަޑި މަސައްކަތްކުރާ ގޮތް</span><span class="chap-a" id="aHow">އެންމެ ފަހުގެ ރަސްމީ އަދަދުން ފަށައި، ފަހުގެ މިންވަރުން ދަރަނި އިތުރުކުރޭ.</span>')
p.R('<p>Official debt figures come out once a quarter. The clock starts from the latest published total and adds debt at the average pace of the most recent four quarters, so the number between releases is an <b>estimate</b>. When a new quarter is published, the clock resets to the official figure. The site checks for new data every morning.</p>',
  '<p>ދަރަނީގެ ރަސްމީ އަދަދުތައް ނެރެނީ ތިން މަހުން އެއްފަހަރެވެ. ގަޑި ފަށަނީ ޝާއިޢުކޮށްފައިވާ އެންމެ ފަހުގެ ޖުމްލަ އަދަދުންނެވެ. އަދި ފާއިތުވި ހަތަރު ކުއާޓަރުގެ އެވަރެޖް މިންވަރުން ދަރަނި އިތުރުކުރެއެވެ. އެހެންކަމުން، ރަސްމީ އަދަދުތައް ނެރޭ ދެމެދު ފެންނަ އަދަދަކީ <b>ލަފާކުރެވޭ</b> އަދަދެކެވެ. އާ ކުއާޓަރެއްގެ އަދަދު ނެރުމުން، ގަޑި ރަސްމީ އަދަދަށް ބަދަލުވެއެވެ. ކޮންމެ ދުވަހަކު ހެނދުނު ސައިޓުން އާ ޑޭޓާ ޗެކްކުރެއެވެ.</p>')
p.R('<p>The <a href="methodology.html">full methodology</a> explains where every number comes from, how it\'s calculated, and what it leaves out.</p>',
  '<p>ކޮންމެ އަދަދެއް ލިބެނީ ކޮންތާކުންކަމާއި، ހިސާބުކުރާ ގޮތާއި، ނުހިމެނޭ ކަންތައްތައް <a href="methodology.html">ފުރިހަމަ މެތަޑޮލޮޖީ</a>ގައި ބަޔާންކޮށްފައިވެއެވެ.</p>')
p.R('<h2>The short version</h2>\n', '<h2>ކުރުކޮށް</h2>\n') if '<h2>The short version</h2>\n' in p.s else None
p.s = p.s.replace('<h2>The short version</h2>', '<h2>ކުރުކޮށް</h2>')
p.R('<p>Four things to know, in plain words. Tap any of them to see the details behind it.</p>', '<p>ދެނެގަންނަންޖެހޭ ހަތަރު ކަމެއް، ފަސޭހަ ބަހުން. ތަފްސީލު ބެލުމަށް ކޮންމެ އެއްޗަކަށް ފިތާލައްވާ.</p>')
p.R('<span id="fetched">Figures from Maldives Monetary Authority Statistics Database.</span>', '<span id="fetched">އަދަދުތައް ނަގާފައިވަނީ މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން.</span>')

# ---- lenders panel headings (contents stay English in this draft) ----
p.R('<span id="homeHead">Domestic debt, owed at home</span>', '<span id="homeHead">ދާޚިލީ ދަރަނި، ރާއްޖޭގައި ދައްކަންޖެހޭ</span>')
p.R('<span class="part-n">2</span>Foreign debt, owed abroad</h3>', '<span class="part-n">2</span>ބޭރުގެ ދަރަނި، ބޭރަށް ދައްކަންޖެހޭ</h3>')
p.R('<span class="part-n">3</span>Paying it back, and what is still to come</h3>', '<span class="part-n">3</span>އަނބުރާ ދެއްކުން، އަދި ކުރިއަށް ދައްކަންޖެހޭ</h3>')
p.R('<h4>Every loan and guarantee</h4>', '<h4>ހުރިހާ ލޯނަކާއި ގެރެންޓީއެއް</h4>')

# ---- script: words built by the page ----
p.R('const LABELS = { domestic_cg: "Domestic, central government", domestic_guaranteed: "Domestic, guaranteed", external_cg: "Foreign, central government", external_guaranteed: "Foreign, guaranteed" };',
  'const LABELS = { domestic_cg: "ދާޚިލީ، ސަރުކާރު", domestic_guaranteed: "ދާޚިލީ، ގެރެންޓީ", external_cg: "ބޭރު، ސަރުކާރު", external_guaranteed: "ބޭރު، ގެރެންޓީ" };')
p.R('const mvTick = () => { const p = Object.fromEntries(mvFmt.formatToParts(new Date()).map(x => [x.type, x.value])); $("mvTime").textContent = `${p.hour}:${p.minute}:${p.second}, ${p.weekday} ${p.day} ${p.month} ${p.year}`; };',
  'const mvTick = () => { $("mvTime").textContent = MV_DV.clock(Date.now()); };')
p.R('n.innerHTML = `The latest figures didn\'t load. Please refresh the page. <button', 'n.innerHTML = `އެންމެ ފަހުގެ އަދަދުތައް ލޯޑެއް ނުވި. ޞަފްޙާ ރިފްރެޝް ކުރައްވާ. <button')
p.R('cursor:pointer">Refresh</button>`', 'cursor:pointer">ރިފްރެޝް</button>`')
p.R('what: "Official quarterly debt figures"', 'what: "ދަރަނީގެ ރަސްމީ ކުއާޓަރުލީ އަދަދުތައް"')
p.R('say: p => `A new official debt figure is out, for the end of <b>${MV.mLabel(latest.date)}</b>. The last one you saw was for ${MV.mLabel(p)}.` }',
  'say: p => `<b>${MV.mLabel(latest.date)}</b> ގެ ނިޔަލަށް ދަރަނީގެ އާ ރަސްމީ އަދަދެއް ނެރެފިއެވެ. ކުރިން ފެނިވަޑައިގެންނެވީ ${MV.mLabel(p)} ގެ އަދަދެވެ.` }')
p.R('say: p => debtNow() > p ? `The clock has added about <b>${MV.moneyNow(debtNow() - p)}</b> to the debt since then.` : null }',
  'say: p => debtNow() > p ? `އެއަށްފަހު ގަޑިން ދަރަންޏަށް ގާތްގަނޑަކަށް <b>${MV.moneyNow(debtNow() - p)}</b> އިތުރުކޮށްފިއެވެ.` : null }')
p.R('$("lineLabel").innerHTML = `<b>${fmt(ratio, 1)}% of GDP</b>`;', '$("lineLabel").innerHTML = `<b>ޖީޑީޕީގެ <bdi>${fmt(ratio, 1)}%</bdi></b>`;')
p.R('const other = MV.state.cur === "USD" ? "MVR " + short(debtNow()) : "US$ " + short(debtNow() / MV.USD);', 'const other = MV.state.cur === "USD" ? short(debtNow()) + " ރުފިޔާ" : short(debtNow() / MV.USD) + " ޑޮލަރު";')
p.R('$("sub").innerHTML = `Estimated from the official figure of ${moneyNow(latest.value, latest.date)} at the end of ${mLabel(latest.date)}. About <strong>${other}</strong> today.`;',
  '$("sub").innerHTML = `${mLabel(latest.date)} ގެ ނިޔަލަށް ${moneyNow(latest.value, latest.date)} ގެ ރަސްމީ އަދަދުން ލަފާކޮށްފައި. މިއަދު ގާތްގަނޑަކަށް <strong>${other}</strong>.`;')
p.R('$("perSecondLbl").textContent = rate >= 0 ? "added to the debt each second, on the pace of the last year" : "paid down each second, on the pace of the last year";',
  '$("perSecondLbl").textContent = rate >= 0 ? "ކޮންމެ ސިކުންތެއްގައި ދަރަންޏަށް އިތުރުވާ މިންވަރު، ފާއިތުވި އަހަރުގެ މިންވަރުން" : "ކޮންމެ ސިކުންތެއްގައި ދަރަނި މަދުވާ މިންވަރު، ފާއިތުވި އަހަރުގެ މިންވަރުން";')
p.R('$("interestLbl").textContent = `spent on interest and financing costs every day in ${PL.d.slice(0, 4)} so far`;', '$("interestLbl").textContent = `${PL.d.slice(0, 4)} ގައި މިހާތަނަށް ކޮންމެ ދުވަހަކު އިންޓަރެސްޓާއި ފައިނޭންސިންގ ޚަރަދަށް ހޭދަވި ފައިސާ`;')
p.R('$("interestLbl").textContent = `spent on interest and financing costs every day, over the 12 months to ${mLabel(fEnd)}`;', '$("interestLbl").textContent = `${mLabel(fEnd)} އާ ހަމައަށް 12 މަހު، ކޮންމެ ދުވަހަކު އިންޓަރެސްޓާއި ފައިނޭންސިންގ ޚަރަދަށް ހޭދަވި ފައިސާ`;')
p.R('$("growthLine").innerHTML = `Since ${mLabel(first.date)}, public debt has grown <b>${fmt(mult, 1)} times</b>${realOn ? " after inflation" : ""}, from ${money(first.value, first.date)} to ${money(latest.value, latest.date)}${realOn ? ` (in ${MV.baseLabel()})` : ""}.`',
  '$("growthLine").innerHTML = `${mLabel(first.date)} އިން ފެށިގެން ސަރުކާރުގެ ދަރަނި <b>${fmt(mult, 1)} ގުނަ</b> ބޮޑުވެފައިވެއެވެ${realOn ? " (އިންފްލޭޝަން ބަލައިގެން)" : ""}. ${money(first.value, first.date)} އިން ${money(latest.value, latest.date)} އަށެވެ${realOn ? ` (${MV.baseLabel()})` : ""}.`')
p.R('+ (rev12 ? ` It now equals <b>${fmt(convNow(latest.value, latest.date) / rev12, 1)} years</b> of everything the government collects.` : "");',
  '+ (rev12 ? ` މިހާރު މި ދަރަނި އަކީ ސަރުކާރަށް ލިބޭ ހުރިހާ ފައިސާގެ <b>${fmt(convNow(latest.value, latest.date) / rev12, 1)} އަހަރު</b>ގެ އަދަދެވެ.` : "");')
p.R('const word = (v, up, down) => v >= 0 ? `${up} by ${disp(v)}` : `${down} by ${disp(-v)}`;', 'const word = (v, up, down) => v >= 0 ? `${disp(v)} ${up}` : `${disp(-v)} ${down}`;')
p.R('$("quarterLine").textContent = `In the three months to ${mLabel(latest.date)}, total debt ${word(dt, "rose", "fell")}` + (dd != null && de != null ? `: domestic debt ${word(dd, "rose", "fell")} and external debt ${word(de, "rose", "fell")}.` : ".");',
  '$("quarterLine").textContent = `${mLabel(latest.date)} އާ ހަމައަށް ތިން މަހު، ޖުމްލަ ދަރަނި ${word(dt, "އިތުރުވިއެވެ", "މަދުވިއެވެ")}.` + (dd != null && de != null ? ` ދާޚިލީ ދަރަނި ${word(dd, "އިތުރުވި", "މަދުވި")}، އަދި ބޭރުގެ ދަރަނި ${word(de, "އިތުރުވިއެވެ", "މަދުވިއެވެ")}.` : "");')
p.R('<span class="v num">${moneyNow(x.p.value, x.p.date)}, ${fmt(100 * x.p.value / sum, 1)}% of debt</span>', '<span class="v num">${moneyNow(x.p.value, x.p.date)}، ދަރަނީގެ ${fmt(100 * x.p.value / sum, 1)}%</span>')
p.R('<div class="lbl">of GDP is owed at home (${moneyNow(dv.value, dv.date)})</div>', '<div class="lbl">ޖީޑީޕީގެ ނިސްބަތުން ރާއްޖޭގައި ދައްކަންޖެހޭ ދަރަނި (${moneyNow(dv.value, dv.date)})</div>')
p.R('<div class="lbl">of GDP is owed abroad (${moneyNow(ev.value, ev.date)})</div>', '<div class="lbl">ޖީޑީޕީގެ ނިސްބަތުން ބޭރަށް ދައްކަންޖެހޭ ދަރަނި (${moneyNow(ev.value, ev.date)})</div>')
p.R('<div class="lbl">of GDP in total, at the end of ${mLabel(latest.date)}</div>', '<div class="lbl">ޖީޑީޕީގެ ނިސްބަތުން ޖުމްލަ ދަރަނި، ${mLabel(latest.date)} ގެ ނިޔަލަށް</div>')
p.R('$("fiscalNote").innerHTML = `Over the 12 months from <b>${mLabel(firstM)} to ${mLabel(fEnd)}</b>, the latest monthly figures published. Per-citizen figures use the same population estimate as the debt clock. For the latest weekly totals, see the <a href="budget.html">budget page</a>. For which taxes bring the money in, and how much is paid in US dollars, see <a href="revenue.html">taxes</a>.`;',
  '$("fiscalNote").innerHTML = `<b>${mLabel(firstM)} އިން ${mLabel(fEnd)} އަށް</b> 12 މަސްދުވަހެވެ. އެއީ ޝާއިޢުކޮށްފައިވާ އެންމެ ފަހުގެ މަހުން މަހަށް އަދަދުތަކެވެ. ކޮންމެ ރައްޔިތަކަށް ބަހާލާ އަދަދުތަކަށް ބޭނުންކުރަނީ ދަރަނީގެ ގަޑީގައި ބޭނުންކުރާ އާބާދީގެ އެ އަދަދެވެ. ހަފްތާއިން ހަފްތާއަށް އެންމެ ފަހުގެ އަދަދުތައް <a href="budget.html">ބަޖެޓް ޞަފްޙާ</a>ގައި ވެއެވެ. ފައިސާ ލިބެނީ ކޮން ޓެކްސްތަކުންކަމާއި، ޑޮލަރުން ދައްކާ މިންވަރު <a href="revenue.html">ޓެކްސް ޞަފްޙާ</a>ގައި ވެއެވެ.`;')
p.R('$("gapLbl").textContent = gap >= 0 ? "more spent than collected per citizen, covered by borrowing" : "more collected than spent per citizen";',
  '$("gapLbl").textContent = gap >= 0 ? "ކޮންމެ ރައްޔިތަކަށް ބަހާލާއިރު ލިބޭ ފައިސާއަށްވުރެ ބޮޑަށް ހިނގާ ޚަރަދު، ދަރަނިން ފުރިހަމަކުރެވޭ" : "ކޮންމެ ރައްޔިތަކަށް ބަހާލާއިރު ޚަރަދަށްވުރެ ބޮޑަށް ލިބޭ ފައިސާ";')
p.R('const items = [["Salaries, wages and pensions", last12("salaries_pensions"), "#3fb8b0"], ["Grants, contributions and subsidies", last12("subsidies"), "#9fe0d6"],',
  'const items = [["މުސާރަ، އުޖޫރަ އަދި ޕެންޝަން", last12("salaries_pensions"), "#3fb8b0"], ["އެހީ، ހިލޭ ދިނުން އަދި ސަބްސިޑީ", last12("subsidies"), "#9fe0d6"],')
p.R('["Interest and financing costs", int12, "#ff8a6b"], ["Capital spending (building and equipment)", last12("capital_exp"), "#f4c95d"]]',
  '["އިންޓަރެސްޓް އަދި ފައިނޭންސިންގ ޚަރަދު", int12, "#ff8a6b"], ["ކެޕިޓަލް ޚަރަދު (ބިނާކުރުމާއި ސާމާނު)", last12("capital_exp"), "#f4c95d"]]')
p.R('cards.push(["trend", "var(--foam)", `${fmt(mult, 1)} times bigger`, `than in ${first.date.slice(0, 4)}`, `The debt was ${money(first.value, first.date)} at the end of ${mLabel(first.date)}. It has grown almost every year since.`, "ch-history", "See how it grew"]);',
  'cards.push(["trend", "var(--foam)", `${fmt(mult, 1)} ގުނަ ބޮޑު`, `${first.date.slice(0, 4)} އާ އަޅާބަލާއިރު`, `${mLabel(first.date)} ގެ ނިޔަލަށް ދަރަނި އޮތީ ${moneyNow(first.value, first.date)} އަށެވެ. އެއަށްފަހު ގާތްގަނޑަކަށް ކޮންމެ އަހަރަކު ދަރަނި އިތުރުވެފައިވެއެވެ.`, "ch-history", "ބޮޑުވި ގޮތް ބައްލަވާ"]);')
p.R('"Borrowed in a year to fill the gap", `Over the last 12 months the government spent more than it collected. The difference, called the <span class="term" role="button" tabindex="0" data-term="deficit">deficit</span>, was borrowed.`, "ch-fiscal", "Why it borrows"]);',
  '"ތަފާތު ފުރިހަމަކުރަން އަހަރަކު ނެގި ދަރަނި", `ފާއިތުވި 12 މަހު، ސަރުކާރަށް ލިބުނު ފައިސާއަށްވުރެ ޚަރަދު ބޮޑުވިއެވެ. އެ ތަފާތަށް ކިޔަނީ <span class="term" role="button" tabindex="0" data-term="deficit">ޑެފިސިޓް</span> އެވެ. އެ ފައިސާ ހޯދީ ދަރަނި ނަގައިގެންނެވެ.`, "ch-fiscal", "ދަރަނި ނަގާ ސަބަބު"]);')
p.R('`${fmt(100 * int12 / rev12, 0)} in every 100`, "Rufiyaa collected that go on interest", `Over the last 12 months, this much of every 100 rufiyaa the government collected went to lenders as <span class="term" role="button" tabindex="0" data-term="interest">interest</span>. That money pays for no school, hospital or salary.`, "priorities.html?from=home", "Compare it with policing and rights"]);',
  '`100 ން ${fmt(100 * int12 / rev12, 0)}`, "ލިބޭ ކޮންމެ 100 ރުފިޔާއިން އިންޓަރެސްޓަށް ދާ މިންވަރު", `ފާއިތުވި 12 މަހު، ސަރުކާރަށް ލިބުނު ކޮންމެ 100 ރުފިޔާއިން މި މިންވަރު ދަރަނި ދިން ފަރާތްތަކަށް <span class="term" role="button" tabindex="0" data-term="interest">އިންޓަރެސްޓް</span> ގޮތުގައި ދިޔައެވެ. އެ ފައިސާއިން ސްކޫލެއް، ހޮސްޕިޓަލެއް ނުވަތަ މުސާރައެއް ނުދެވެއެވެ.`, "priorities.html?from=home", "ފުލުހުންނާއި ޙައްޤުތަކާ އަޅާކިޔާލައްވާ"]);')
p.R('`${fmt(dsh, 0)}% at home`, "Who it\'s owed to", `Most is owed to banks and funds inside Maldives. The other ${fmt(100 - dsh, 0)}% is owed abroad and has to be paid back in foreign currency.`, "ch-owed", "See who the lenders are"]);',
  '`${fmt(dsh, 0)}% ރާއްޖޭގައި`, "ދަރަނި ދައްކަންޖެހޭ ފަރާތްތައް", `ގިނަ ބައި ދައްކަންޖެހެނީ ރާއްޖޭގެ ބޭންކުތަކާއި ފަންޑުތަކަށެވެ. ބާކީ ${fmt(100 - dsh, 0)}% ދައްކަންޖެހެނީ ބޭރަށެވެ. އަދި އެ ދައްކަންޖެހެނީ ބޭރުގެ ފައިސާއިންނެވެ.`, "ch-owed", "ދަރަނި ދިން ފަރާތްތައް ބައްލަވާ"]);')
p.s = p.s.replace('${go} →</a>', '${go} ←</a>')
p.R('$("aOwed").textContent = "Banks, MMA and the pension fund at home, and governments, development banks and investors abroad.";', '$("aOwed").textContent = "ރާއްޖޭގައި ބޭންކުތަކާއި، MMA އާއި ޕެންޝަން ފަންޑަށް. ބޭރުގައި ސަރުކާރުތަކާއި، ތަރައްޤީގެ ބޭންކުތަކާއި، އިންވެސްޓަރުންނަށް.";')
p.R('$("aHist").textContent = "Quarter by quarter since 2015, in rufiyaa or against the size of the economy.";', '$("aHist").textContent = "2015 އިން ފެށިގެން ކޮންމެ ކުއާޓަރަކަށް، ރުފިޔާއިން ނުވަތަ އިޤްތިޞާދުގެ ބޮޑުމިނާ އަޅާކިޔައިގެން.";')
p.R('$("aFisc").textContent = "What comes in, what goes out, and why the debt grows faster than the yearly gap.";', '$("aFisc").textContent = "ލިބޭ ފައިސާއާއި ހިނގާ ޚަރަދު، އަދި ކޮންމެ އަހަރެއްގެ ތަފާތަށްވުރެ ދަރަނި ބޮޑަށް އިތުރުވަނީ ކީއްވެކަން.";')
p.R('$("aHow").textContent = "Where the number comes from, and why it is an estimate between official releases.";', '$("aHow").textContent = "އަދަދު ލިބެނީ ކޮންތާކުންކަމާއި، ރަސްމީ އަދަދުތައް ނެރޭ ދެމެދު އެއީ ލަފާކުރެވޭ އަދަދަކަށް ވަނީ ކީއްވެކަން.";')
p.R('$("methodDetail").innerHTML = `Right now that pace is <b>${moneyNow(rate * SEC_YEAR)} a year</b>, from the change between ${mLabel(back.date)} and ${mLabel(latest.date)}. Dollar figures use MMA reference rate (MVR ${fmt(MV.USD, 2)} per US dollar today).`;',
  '$("methodDetail").innerHTML = `މިހާރު އެ މިންވަރަކީ <b>އަހަރަކު ${moneyNow(rate * SEC_YEAR)}</b> އެވެ. މި ހިސާބުކުރަނީ ${mLabel(back.date)} އާއި ${mLabel(latest.date)} އާ ދެމެދު އައި ބަދަލުންނެވެ. ޑޮލަރުން ދައްކާ އަދަދުތަކަށް ބޭނުންކުރަނީ MMA ގެ ރެފަރެންސް ރޭޓެވެ (މިއަދު އެއް ޑޮލަރަކީ ${fmt(MV.USD, 2)} ރުފިޔާ).`;')
p.R('$("popLine").innerHTML = `Based on an estimated ${fmt(Math.round(pop))} citizens (national register, end of ${POP.base_date.slice(0, 4)}, grown at ${fmt(POP.annual_growth * 100, 2)}% a year). This will be updated when the government publishes new figures. <a href="methodology.html#population">How this is estimated</a>`;',
  '$("popLine").innerHTML = `ލަފާކުރެވޭ ގޮތުން ${fmt(Math.round(pop))} ރައްޔިތުން (${POP.base_date.slice(0, 4)} ގެ ނިޔަލަށް ނޭޝަނަލް ރަޖިސްޓަރީގައިވާ އަދަދު، އަހަރަކު ${fmt(POP.annual_growth * 100, 2)}% އިން އިތުރުކޮށްގެން). ސަރުކާރުން އާ އަދަދުތައް ޝާއިޢުކުރުމުން މި އަދަދު ބަދަލުކުރެވޭނެއެވެ. <a href="methodology.html#population">ލަފާކުރާ ގޮތް</a>`;')
p.R('$("popNote").innerHTML = `Per-citizen figures divide by an estimated <b>${fmt(Math.round(pop))}</b> Maldivian citizens today. That is the ${fmt(POP.base)} on the national register at the end of 2025, grown at ${fmt(POP.annual_growth * 100, 2)}% a year, the rate the Maldivian population grew between the last two censuses.`;',
  '$("popNote").innerHTML = `ކޮންމެ ރައްޔިތަކަށް ބަހާލާ އަދަދުތައް ހިސާބުކުރަނީ މިއަދު ތިބިކަމަށް ލަފާކުރެވޭ <b>${fmt(Math.round(pop))}</b> ދިވެހި ރައްޔިތުންނަށް ބަހާލައިގެންނެވެ. އެއީ 2025 ގެ ނިޔަލަށް ނޭޝަނަލް ރަޖިސްޓަރީގައިވާ ${fmt(POP.base)} ރައްޔިތުން، އަހަރަކު ${fmt(POP.annual_growth * 100, 2)}% އިން އިތުރުކޮށްގެންނެވެ. އެއީ ފަހުގެ ދެ ސެންސަހުގެ ދެމެދު ދިވެހި އާބާދީ އިތުރުވި މިންވަރެވެ.`;')
p.R('$("fetched").textContent = "Data last fetched " + MV.fetched(data.fetched_at) + ", Malé time. Figures from MMA Statistics Database.";',
  '$("fetched").textContent = "އެންމެ ފަހުން ޑޭޓާ ހޯދީ " + MV.fetched(data.fetched_at) + " (މާލޭ ވަގުތު). އަދަދުތައް ނަގާފައިވަނީ MMA ގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން.";')
p.R('`<b>${n(gaps)}</b> from the yearly gaps between spending and revenue, added up`', '`<b>${n(gaps)}</b> ކޮންމެ އަހަރެއްގެ ޚަރަދާއި އާމްދަނީގެ ތަފާތު، ޖަމާކޮށްގެން`')
p.R('`<b>${n(guar)}</b> from extra borrowing by state-owned companies with a government guarantee, which doesn\'t appear as government spending`', '`<b>${n(guar)}</b> ސަރުކާރުގެ ގެރެންޓީއާއެކު ސަރުކާރު ކުންފުނިތަކުން ނެގި އިތުރު ދަރަނި. މިއީ ސަރުކާރުގެ ޚަރަދުގައި ނުފެންނަ ބައެކެވެ`')
p.R('`<b>${n(other)}</b> from other borrowing that isn\'t counted as spending, such as lending to and investing in state-owned companies, and changes in the government\'s cash balances`', '`<b>${n(other)}</b> ޚަރަދުގެ ގޮތުގައި ނުގުނާ އެހެން ދަރަނި. ސަރުކާރު ކުންފުނިތަކަށް ދަރަނި ދިނުމާއި އިންވެސްޓްކުރުމާއި، ސަރުކާރުގެ ނަގުދު ފައިސާގެ ބެލެންސް ބަދަލުވުން ފަދަ ކަންކަމެވެ`')
p.R('<h3>Why is the debt so much bigger than this gap?</h3>', '<h3>މި ތަފާތަށްވުރެ ދަރަނި މިހާ ބޮޑީ ކީއްވެ؟</h3>')
p.R("<p>The ${sym()} ${fmt(convNow(Math.abs(gapPP)))} gap is just <b>one year's</b> shortfall. The ${sym()} ${fmt(pp)} debt per citizen is what has <b>built up over many years</b>, like a credit card balance compared with one month's overspending. And some borrowing never shows up as government spending at all.</p>",
  "<p>${sym()} ${fmt(convNow(Math.abs(gapPP)))} ގެ ތަފާތަކީ <b>އެއް އަހަރުގެ</b> ތަފާތެވެ. ކޮންމެ ރައްޔިތަކަށް ބަހާލާއިރު ${sym()} ${fmt(pp)} ގެ ދަރަނި އަކީ <b>ގިނަ އަހަރުތަކެއްގައި</b> ޖަމާވެފައިވާ ދަރަންޏެވެ. އެއީ އެއް މަހު ބޭނުންކުރި އިތުރު ފައިސާއާއި، ކްރެޑިޓް ކާޑުގައި ޖަމާވެފައިވާ ބެލެންސް ފަދަ ތަފާތެކެވެ. އަދި ބައެއް ދަރަނި ސަރުކާރުގެ ޚަރަދުގައި އެއްގޮތަކަށްވެސް ނުފެނެއެވެ.</p>")
p.R('<p>Since ${mLabel(q0.date)}, debt has risen by <b>${n(rise)}</b>. This is where it came from.</p>', '<p>${mLabel(q0.date)} އިން ފެށިގެން ދަރަނި <b>${n(rise)}</b> އިތުރުވެފައިވެއެވެ. އެ އައީ މި ގޮތަށެވެ.</p>')
p.R('aria-label="Where the rise in debt came from"', 'aria-label="ދަރަނި އިތުރުވި ސަބަބުތައް"')
p.R('<p class="small">The ${n(q0.value)} owed in ${mLabel(q0.date)} came from earlier years. Yearly gaps are summed from monthly figures, ${mLabel(S.revenue.points.find(p => p.date > q0.date).date)} to ${mLabel(q1.date)}. <a href="methodology.html#fiscal">More on how this is worked out</a>.</p>',
  '<p class="small">${mLabel(q0.date)} ގައި އޮތް ${n(q0.value)} ގެ ދަރަނި އަކީ ކުރީގެ އަހަރުތަކުގެ ދަރަންޏެވެ. އަހަރުގެ ތަފާތުތައް ޖަމާކޮށްފައިވަނީ ${mLabel(S.revenue.points.find(p => p.date > q0.date).date)} އިން ${mLabel(q1.date)} އަށް މަހުން މަހަށް އަދަދުތަކުންނެވެ. <a href="methodology.html#fiscal">ހިސާބުކުރި ގޮތް</a>.</p>')
p.R('$("annualNote").textContent = `Revenue and spending each full calendar year, in billions of ${MV.state.cur === "USD" ? "US dollars" : "rufiyaa"}${MV.isReal() ? `, in ${MV.baseLabel()}` : ""}. The red figure under each year is the deficit.`;',
  '$("annualNote").textContent = `ކޮންމެ މީލާދީ އަހަރެއްގެ އާމްދަނީއާއި ޚަރަދު، ބިލިއަން ${MV.state.cur === "USD" ? "ޑޮލަރުން" : "ރުފިޔާއިން"}${MV.isReal() ? `، ${MV.baseLabel()}` : ""}. ކޮންމެ އަހަރެއްގެ ދަށުގައިވާ ރަތް އަދަދަކީ ޑެފިސިޓް.`;')
p.R('`<span>In the last 12 months (${mLabel(firstM)} to ${mLabel(fEnd)}${MV.isReal() ? ", same prices as the chart" : ""})</span><span>Revenue <b>${sym()} ${bn(r12)}</b></span><span>Spending <b class="red">${sym()} ${bn(e12)}</b></span><span>${e12 >= r12 ? "Deficit" : "Surplus"}',
  '`<span>ފާއިތުވި 12 މަސް (${mLabel(firstM)} އިން ${mLabel(fEnd)} އަށް${MV.isReal() ? "، ޗާޓުގެ އަގުތަކުން" : ""})</span><span>އާމްދަނީ <b>${sym()} ${bn(r12)}</b></span><span>ޚަރަދު <b class="red">${sym()} ${bn(e12)}</b></span><span>${e12 >= r12 ? "ޑެފިސިޓް" : "ސަރޕްލަސް"}')
p.R('cats, label: "Government revenue and spending by year",', 'cats, label: "އަހަރުން އަހަރަށް ސަރުކާރުގެ އާމްދަނީ އަދި ޚަރަދު",')
p.R('row("Revenue", sym() + " " + bn(R[i])) + row("Spending", sym() + " " + bn(E[i])) +', 'row("އާމްދަނީ", sym() + " " + bn(R[i])) + row("ޚަރަދު", sym() + " " + bn(E[i])) +')
p.R('row(E[i] >= R[i] ? "Deficit" : "Surplus",', 'row(E[i] >= R[i] ? "ޑެފިސިޓް" : "ސަރޕްލަސް",')
p.R('row("Spending per 100 collected", fmt(100 * E[i] / R[i], 0))', 'row("ލިބޭ ކޮންމެ 100 އަކަށް ޚަރަދު", fmt(100 * E[i] / R[i], 0))')
p.R('$("chartNote").textContent = useRatio ? "Total public debt as a share of the economy (GDP), each quarter. Inflation doesn\'t affect this view." :',
  '$("chartNote").textContent = useRatio ? "ކޮންމެ ކުއާޓަރެއްގައި ޖުމްލަ ދަރަނި، އިޤްތިޞާދުގެ (ޖީޑީޕީގެ) ނިސްބަތުން. މި ގޮތަށް ބަލާއިރު އިންފްލޭޝަނުގެ އަސަރެއް ނުކުރެއެވެ." :')
p.R('`Total public and publicly guaranteed debt at the end of each quarter, in billions of ${MV.state.cur === "USD" ? "US dollars" : "rufiyaa"}${MV.isReal() ? `, in ${MV.baseLabel()}` : ""}.`;',
  '`ކޮންމެ ކުއާޓަރެއްގެ ނިޔަލަށް ސަރުކާރުގެ ދަރަންޏާއި ސަރުކާރުން ގެރެންޓީ ދީފައިވާ ދަރަނި، ބިލިއަން ${MV.state.cur === "USD" ? "ޑޮލަރުން" : "ރުފިޔާއިން"}${MV.isReal() ? `، ${MV.baseLabel()}` : ""}.`;')
p.R('label: "Debt by quarter",', 'label: "ކުއާޓަރުން ކުއާޓަރަށް ދަރަނި",')
p.R('row("Total", money(r.total, r.date)) + row("Domestic", r.dom != null ? money(r.dom, r.date) : null) + row("Foreign", r.ext != null ? money(r.ext, r.date) : null) + row("Share of GDP",',
  'row("ޖުމްލަ", money(r.total, r.date)) + row("ދާޚިލީ", r.dom != null ? money(r.dom, r.date) : null) + row("ބޭރު", r.ext != null ? money(r.ext, r.date) : null) + row("ޖީޑީޕީގެ ނިސްބަތް",')


p.footer()
p.relink()
p.write()
