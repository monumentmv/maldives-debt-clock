"""Dhivehi interest page (dv-priorities.html) from priorities.html. See common.py."""
from common import Page

p = Page("priorities")
p.head("އިންޓަރެސްޓުގެ ބިލު · ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި",
       "ސަރުކާރުން އިންޓަރެސްޓަށް ދައްކާ ފައިސާ، ފުލުހުންނާއި، ޝަރީޢަތާއި، އާއިލާތަކާއި ކުޑަކުދިންނާއި އިންސާނީ ޙައްޤުތައް ރައްކާތެރިކުރުމަށް ހޭދަކުރާ ފައިސާއާ އަޅާބަލާއިރު.",
       extra_js=("dv-priorities.js",))
p.header()

# ---- right-to-left fixes for this page ----
p.R('</style>\n</head>', '''  /* Dhivehi: bars grow from the right */
  html[lang="dv"] .ctx .t i, html[lang="dv"] .cases-list .bar i { left: auto; right: 0; }
  html[lang="dv"] :is(.ctx .v, .cases-list .row span:last-child) { text-align: left; }
  html[lang="dv"] .meter { transform: scaleX(-1); }
  html[lang="dv"] .chip { padding: .25rem .3rem .25rem .7rem; }
  html[lang="dv"] .eyebrow { letter-spacing: 0; }
</style>
</head>''')

# ---- static text ----
p.R('<p class="eyebrow">Interest Bill</p>', '<p class="eyebrow">އިންޓަރެސްޓުގެ ބިލު</p>')
p.R('<h1 class="often-h">Interest now costs more than law, order and protection</h1>',
    '<h1 class="often-h">މިހާރު އިންޓަރެސްޓަށް ހިނގާ ޚަރަދު، ޤާނޫނާއި ނިޒާމާއި ރައްކާތެރިކަމަށް ހިނގާ ޚަރަދަށްވުރެ ބޮޑެވެ</h1>')
p.R('<p class="lede">The government spends more paying interest on its loans than on the police, prisons and child protection combined, and has every year since 2022.</p>',
    '<p class="lede">ސަރުކާރުން ދަރަނީގެ އިންޓަރެސްޓަށް ހޭދަކުރާ ފައިސާ، ފުލުހުންނާއި، ޖަލުތަކާއި، ކުޑަކުދިން ރައްކާތެރިކުރުމަށް ހޭދަކުރާ ފައިސާ އެއްކޮށްލި އަދަދަށްވުރެ ބޮޑެވެ. 2022 އިން ފެށިގެން ކޮންމެ އަހަރަކު ވެސް ވަނީ މިގޮތަށެވެ.</p>')
p.R('<button type="button" class="step" id="cPrev" aria-label="Earlier">‹ Earlier</button>', '<button type="button" class="step" id="cPrev" aria-label="ކުރީގެ">ކުރީގެ ›</button>')
p.R('<label><span>Year</span> <select id="cYear" aria-label="Year"></select></label>', '<label><span>އަހަރު</span> <select id="cYear" aria-label="އަހަރު"></select></label>')
p.R('<label><span>Period</span> <select id="cMonth" aria-label="Period"></select></label>', '<label><span>މުއްދަތު</span> <select id="cMonth" aria-label="މުއްދަތު"></select></label>')
p.R('<button type="button" class="step" id="cNext" aria-label="Later">Later ›</button>', '<button type="button" class="step" id="cNext" aria-label="ފަހުގެ">‹ ފަހުގެ</button>')
p.R('<h3 style="margin-top:2.5rem">Every type of case</h3>', '<h3 style="margin-top:2.5rem">ކޮންމެ ބާވަތެއްގެ މައްސަލަ</h3>')
p.R('<h3 style="margin-top:3rem">Year by year</h3>', '<h3 style="margin-top:3rem">އަހަރުން އަހަރަށް</h3>')
p.R('Cases reported each year. The latest year is the year so far.</p>', 'ކޮންމެ އަހަރަކު ރިޕޯޓުކުރެވުނު މައްސަލަތައް. އެންމެ ފަހުގެ އަހަރުގެ އަދަދަކީ މިހާތަނަށް ހުރި އަދަދެވެ.</p>')
p.R('<h2 id="headline" class="big-h">What interest costs, next to what keeps people safe</h2>',
    '<h2 id="headline" class="big-h">އިންޓަރެސްޓަށް ހިނގާ ޚަރަދު، މީހުން ރައްކާތެރިކުރުމަށް ހިނގާ ޚަރަދާ އަޅާބަލާއިރު</h2>')
p.R('<p class="lede" id="lede">Interest pays lenders for borrowing that has already been done. It doesn\'t build a school, run a hospital or pay a police officer. This page sets it beside what the government spends on policing, justice and protecting people\'s rights.</p>',
    '<p class="lede" id="lede">އިންޓަރެސްޓަކީ ކުރިން ނަގާފައިވާ ދަރަންޏަށް ދަރަނި ދިން ފަރާތްތަކަށް ދައްކާ ފައިސާއެވެ. އެއިން ސްކޫލެއް ނުބިނާކުރެވޭ، ހޮސްޕިޓަލެއް ނުހިންގޭ، އަދި ފުލުހެއްގެ މުސާރައެއް ނުދެވެއެވެ. މި ޞަފްޙާގައި އެ ފައިސާ އަޅާކިޔާފައިވަނީ ފުލުހުންނާއި، ޝަރީޢަތާއި، މީހުންގެ ޙައްޤުތައް ރައްކާތެރިކުރުމަށް ސަރުކާރުން ހޭދަކުރާ ފައިސާއާއެވެ.</p>')
p.R('<h2>Office by office</h2>', '<h2>އޮފީހުން އޮފީހަށް</h2>')
p.R('<h2>Next to other big services</h2>', '<h2>އެހެން ބޮޑެތި ޚިދުމަތްތަކާ އަޅާބަލާއިރު</h2>')
p.R('<div><h2>Year by year</h2>', '<div><h2>އަހަރުން އަހަރަށް</h2>')
p.R('<label>Compare interest with <select id="gSel" aria-label="Compare interest with"></select></label>',
    '<label>އިންޓަރެސްޓް އަޅާކިޔާނީ <select id="gSel" aria-label="އިންޓަރެސްޓް އަޅާކިޔާ ބައި"></select></label>')
p.R('<div class="subtoggle" role="group" aria-label="View" id="viewPick"><button type="button" data-v="amount" aria-pressed="true">Amounts</button><button type="button" data-v="growth" aria-pressed="false">Growth</button><button type="button" data-v="ratio" aria-pressed="false">Times as much</button></div>',
    '<div class="subtoggle" role="group" aria-label="ބައްލަވާ ގޮތް" id="viewPick"><button type="button" data-v="amount" aria-pressed="true">އަދަދު</button><button type="button" data-v="growth" aria-pressed="false">ބޮޑުވި މިންވަރު</button><button type="button" data-v="ratio" aria-pressed="false">ކިތައް ގުނަ</button></div>')
p.R('<h2>Where interest goes</h2>', '<h2>އިންޓަރެސްޓް ދަނީ ކޮންތާކަށް</h2>')
p.R('<p>Interest is income for whoever lent to the government. That makes it different from almost everything else in the budget.</p>',
    '<p>އިންޓަރެސްޓަކީ ސަރުކާރަށް ދަރަނި ދިން ފަރާތްތަކަށް ލިބޭ އާމްދަނީއެކެވެ. އެހެންވެ، ބަޖެޓުގެ ގާތްގަނޑަކަށް އެހެން ހުރިހާ ޚަރަދަކާ މިއީ ތަފާތު ޚަރަދެކެވެ.</p>')
p.R('<div><h3>Lenders in Maldives</h3><p>Commercial banks, MMA, the pension fund and other financial institutions hold most Treasury bills and bonds. Their interest stays in the economy, but it goes to lenders rather than public services.</p></div>',
    '<div><h3>ރާއްޖޭގެ ދަރަނި ދިން ފަރާތްތައް</h3><p>ގިނަ ޓްރެޜަރީ ބިލުތަކާއި ބޮންޑުތައް ހުރީ ވިޔަފާރި ބޭންކުތަކާއި، MMA އާއި، ޕެންޝަން ފަންޑާއި، އެހެން މާލީ މުއައްސަސާތަކުގެ އަތުގައެވެ. އެ ފަރާތްތަކަށް ދައްކާ އިންޓަރެސްޓް ރާއްޖޭގެ އިޤްތިޞާދުގައި ހުރި ނަމަވެސް، އެ ފައިސާ ދަނީ ޢާންމު ޚިދުމަތްތަކަކަށް ނޫން، ދަރަނި ދިން ފަރާތްތަކަށެވެ.</p></div>')
p.R('<div><h3>Lenders abroad</h3><p>Interest on external loans, sukuk and international bonds leaves the country in foreign currency and draws on reserves.</p></div>',
    '<div><h3>ބޭރުގެ ދަރަނި ދިން ފަރާތްތައް</h3><p>ބޭރުގެ ލޯނުތަކާއި، ސުކޫކާއި، ބައިނަލްއަޤްވާމީ ބޮންޑުތަކުގެ އިންޓަރެސްޓް ރާއްޖެއިން ބޭރަށް ދަނީ ބޭރުގެ ފައިސާއިންނެވެ. އެއީ ބޭރުގެ ފައިސާގެ ރިޒާވުން ހޭދަވާ ފައިސާއެވެ.</p></div>')
p.R('<div><h3>What it crowds out</h3><p>Every rufiyaa paid in interest is a rufiyaa the budget can\'t spend on policing, schools, hospitals or anything else that year.</p></div>',
    '<div><h3>އޭގެ ސަބަބުން ގެއްލޭ ފުރުޞަތު</h3><p>އިންޓަރެސްޓަށް ދައްކާ ކޮންމެ ރުފިޔާއަކީ، އެ އަހަރު ފުލުހުންނަށް، ސްކޫލުތަކަށް، ހޮސްޕިޓަލްތަކަށް ނުވަތަ އެހެން އެއްވެސް ކަމަކަށް ބަޖެޓުން ހޭދަނުކުރެވޭ ރުފިޔާއެކެވެ.</p></div>')
p.R('<h2>Reading these figures</h2>', '<h2>މި އަދަދުތައް ކިޔާނެ ގޮތް</h2>')
p.R('<p>Spending and interest come from Ministry of Finance\'s weekly fiscal reports. Each figure is the total from 1 January to the date of the report. Interest is what the Ministry reports as financing and interest costs, and doesn\'t include loan repayments. Weekly figures are early and change as accounts are reconciled.</p>',
    '<p>ޚަރަދާއި އިންޓަރެސްޓުގެ އަދަދުތައް ނަގާފައިވަނީ މާލިއްޔަތު ވުޒާރާގެ ހަފްތާއިން ހަފްތާއަށް ނެރޭ މާލީ ރިޕޯޓުތަކުންނެވެ. ކޮންމެ އަދަދަކީ 1 ޖަނަވަރީ އިން ރިޕޯޓުގެ ތާރީޚާ ހަމައަށް ޖުމްލަ އަދަދެވެ. އިންޓަރެސްޓަކީ ވުޒާރާއިން ފައިނޭންސިންގ އަދި އިންޓަރެސްޓް ޚަރަދުގެ ގޮތުގައި ރިޕޯޓުކުރާ އަދަދެވެ. އޭގައި ލޯނު އަނބުރާ ދެއްކުން ނުހިމެނެއެވެ. ހަފްތާއިން ހަފްތާއަށް ނެރޭ އަދަދުތަކަކީ ފުރަތަމަ އަދަދުތަކެވެ. ހިސާބުތައް ބައްޓަންކުރުމުން އެ އަދަދުތައް ބަދަލުވެއެވެ.</p>')
p.R('<p>Case counts are cases reported to Maldives Police Service. They count reports, not convictions, and include traffic accidents and lost items. Placing an office next to a type of case shows scale only.</p>',
    '<p>މައްސަލަތަކުގެ އަދަދަކީ ދިވެހި ފުލުހުންގެ ޚިދުމަތަށް ރިޕޯޓުކުރެވުނު މައްސަލަތަކުގެ އަދަދެވެ. އެ ގުނަނީ ރިޕޯޓުތަކެވެ، ކުށް ސާބިތުވުން ނޫނެވެ. އަދި އޭގެ ތެރޭގައި މަގުމަތީގެ ޙާދިސާތަކާއި ގެއްލުނު ތަކެތި ވެސް ހިމެނެއެވެ. އޮފީހެއް މައްސަލައެއްގެ ބާވަތަކާ ގުޅުވާފައިވަނީ ހަމައެކަނި ބޮޑުމިން ދެއްކުމަށެވެ.</p>')
p.R('<p>Office names change as ministries are merged or split, so the same office can appear under different names in different years. Courts aren\'t shown because judiciary spending moved into the Special Budget in April 2026. <a href="methodology.html#priorities">More in the methodology</a>.</p>',
    '<p>ވުޒާރާތައް އެއްކުރުމުންނާއި ވަކިކުރުމުން އޮފީސްތަކުގެ ނަންތައް ބަދަލުވެއެވެ. އެހެންވެ، އެއް އޮފީސް ވެސް އެކި އަހަރުތަކުގައި އެކި ނަންނަމުން ފެނިދާނެއެވެ. ކޯޓުތައް ނުދައްކަނީ، 2026 ގެ އެޕްރީލްގައި ޝަރީޢަތުގެ ޚަރަދު ސްޕެޝަލް ބަޖެޓަށް ބަދަލުކުރި ކަމުންނެވެ. <a href="methodology.html#priorities">މެތަޑޮލޮޖީގައި އިތުރަށް</a>.</p>')
p.R('<span id="fetched">Figures from Ministry of Finance, Weekly Fiscal Developments, and Maldives Police Service.</span>',
    '<span id="fetched">އަދަދުތައް ނަގާފައިވަނީ މާލިއްޔަތު ވުޒާރާގެ Weekly Fiscal Developments އާއި ދިވެހި ފުލުހުންގެ ޚިދުމަތުންނެވެ.</span>')

# ---- script ----
p.R('const RP = P.reports, O = P.offices, C = P.crime, LR = RP[RP.length - 1];',
    'const RP = P.reports, O = P.offices, C = P.crime, LR = RP[RP.length - 1];\n'
    '    O.forEach(o => { o.name = MV_DV.t[o.name] || o.name; if (o.case_noun) o.case_noun = MV_DV.caseNoun[o.key] || o.case_noun; });   // office names in Dhivehi\n'
    '    const CN = c => MV_DV.t[c] || c;   // police case types in Dhivehi')
p.R('label: dayLabel(r.d) + (i === 0 ? ", latest" : "")', 'label: dayLabel(r.d) + (i === 0 ? "، އެންމެ ފަހުގެ" : "")')
p.R('what: "Ministry of Finance weekly figures"', 'what: "މާލިއްޔަތު ވުޒާރާގެ ހަފްތާއިން ހަފްތާއަށް ނެރޭ އަދަދުތައް"')
p.R('label: m === 1 ? `January ${y}` : `January to ${MONTHS[m - 1]} ${y}` };',
    'label: m === 1 ? `${MONTHS[0]} ${y} ގައި` : `${MONTHS[0]} އިން ${MONTHS[m - 1]} ${y} އަށް` };')
p.R('return { cases: C.yearly[y], label: `so far in ${y}` };', 'return { cases: C.yearly[y], label: `${y} ގައި މިހާތަނަށް` };')
p.R('return { cases: C.book.yearly[y], label: `in ${y}` };', 'return { cases: C.book.yearly[y], label: `${y} ގައި` };')
p.R('const W = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight"]', 'const W = ["އެއްވެސް", "އެއް", "ދެ", "ތިން", "ހަތަރު", "ފަސް", "ހަ", "ހަތް", "އަށް"]')
p.R('''$("headline").textContent = ratio >= 1.02 ? "Interest cost more than policing, justice and rights put together"
        : ratio >= .9 ? "Interest cost about as much as policing, justice and rights put together"
        : `Interest cost ${fmt(ratio * 100)}% as much as policing, justice and rights put together`;''',
    '''$("headline").textContent = ratio >= 1.02 ? "ފުލުހުންނާއި، ޝަރީޢަތާއި، ޙައްޤުތަކަށް ހިނގި ޚަރަދު އެއްކޮށްލި އަދަދަށްވުރެ އިންޓަރެސްޓަށް ހިނގި ޚަރަދު ބޮޑެވެ"
        : ratio >= .9 ? "އިންޓަރެސްޓަށް ހިނގި ޚަރަދު، ފުލުހުންނާއި، ޝަރީޢަތާއި، ޙައްޤުތަކަށް ހިނގި ޚަރަދު އެއްކޮށްލި އަދަދާ ގާތްގަނޑަކަށް އެއްވަރެވެ"
        : `އިންޓަރެސްޓަށް ހިނގި ޚަރަދަކީ، ފުލުހުންނާއި، ޝަރީޢަތާއި، ޙައްޤުތަކަށް ހިނގި ޚަރަދު އެއްކޮށްލި އަދަދުގެ ${fmt(ratio * 100)}% އެވެ`;''')
p.R('''$("lede").innerHTML = `From 1 January to ${dayLabel(d)}, the government paid <b>${cur(it, d)}</b> in interest and financing costs. That money pays lenders for borrowing already done. It doesn't build a school, run a hospital or pay a police officer. Over the same period the police, prisons, prosecutors, the Anti-Corruption Commission and the ${nR === 4 ? "four offices that protect families, children, human rights and people affected by drugs" : `${W[nR]} protection and rights offices then listed`} spent <b>${cur(both, d)}</b> between them.`;''',
    '''$("lede").innerHTML = `1 ${MONTHS[0]} އިން ${dayLabel(d)} އަށް، ސަރުކާރުން އިންޓަރެސްޓާއި ފައިނޭންސިންގ ޚަރަދަށް <b>${cur(it, d)}</b> ދައްކާފައިވެއެވެ. އެ ފައިސާ ދެނީ ކުރިން ނެގި ދަރަންޏަށް ދަރަނި ދިން ފަރާތްތަކަށެވެ. އެއިން ސްކޫލެއް ނުބިނާކުރެވޭ، ހޮސްޕިޓަލެއް ނުހިންގޭ، އަދި ފުލުހެއްގެ މުސާރައެއް ނުދެވެއެވެ. އެ މުއްދަތުގައި ފުލުހުންނާއި، ޖަލުތަކާއި، ޕްރޮސިކިއުޓަރުންނާއި، އެންޓި ކޮރަޕްޝަން ކޮމިޝަނާއި، ${nR === 4 ? "އާއިލާތަކާއި، ކުޑަކުދިންނާއި، އިންސާނީ ޙައްޤުތަކާއި، މަސްތުވާތަކެތީގެ އަސަރު ކުރާ މީހުން ރައްކާތެރިކުރާ ހަތަރު އޮފީހުން" : `އެ ދުވަސްވަރު ލިސްޓުގައިވާ ރައްކާތެރިކުރުމާއި ޙައްޤުތަކާ ބެހޭ ${W[nR]} އޮފީހުން`} ޖުމްލަ <b>${cur(both, d)}</b> ހޭދަކޮށްފައިވެއެވެ.`;''')
p.R('title="${office(k).name}, ${cur(val(R, k), d)}"', 'title="${office(k).name}، ${cur(val(R, k), d)}"')
p.R('<span class="name">Interest and financing costs<small>paid to lenders</small></span>', '<span class="name">އިންޓަރެސްޓް އަދި ފައިނޭންސިންގ ޚަރަދު<small>ދަރަނި ދިން ފަރާތްތަކަށް ދެއްކި</small></span>')
p.R('<span class="name">Policing, justice and rights<small>eight offices, from the police to child protection</small></span>',
    '<span class="name">ފުލުހުން، ޝަރީޢަތް އަދި ޙައްޤުތައް<small>ފުލުހުންގެ ފެށިގެން ކުޑަކުދިން ރައްކާތެރިކުރުމާ ހަމައަށް، އަށް އޮފީސް</small></span>')
p.R('''? `Interest was <b>${cur(it - both, d)} more</b> than all ${W[nAll]} offices put together. That is <b>${times(ratio)} times</b> as much.`
        : `Interest was <b>${fmt(ratio * 100)}%</b> of what all ${W[nAll]} offices spent put together.`;''',
    '''? `އިންޓަރެސްޓަށް ހިނގި ޚަރަދު، ${W[nAll]} އޮފީހުގެ ޚަރަދު އެއްކޮށްލި އަދަދަށްވުރެ <b>${cur(it - both, d)} ބޮޑެވެ</b>. އެއީ <b>${times(ratio)} ގުނަ</b> އެވެ.`
        : `އިންޓަރެސްޓަށް ހިނގި ޚަރަދަކީ، ${W[nAll]} އޮފީހުގެ ޚަރަދު އެއްކޮށްލި އަދަދުގެ <b>${fmt(ratio * 100)}%</b> އެވެ.`;''')
p.R('$("officeNote").textContent = `Spending by each office from 1 January to ${dayLabel(d)}, and how it compares with interest over the same period.`;',
    '$("officeNote").textContent = `1 ${MONTHS[0]} އިން ${dayLabel(d)} އަށް ކޮންމެ އޮފީހަކުން ހޭދަކުރި ފައިސާ، އަދި އެ މުއްދަތުގައި އިންޓަރެސްޓަށް ހިނގި ޚަރަދާ އަޅާބަލާއިރު.`;')
p.R('<div class="share">Interest was ${times(it / v)} times as much${n != null ? `<br>${fmt(n)} ${o.case_noun} cases reported, ${cs.label}` : ""}${pol != null ? `<br>${fmt(pol)} cases reported, ${cs.label}` : ""}</div>',
    '<div class="share">އިންޓަރެސްޓަށް ހިނގީ މީގެ ${times(it / v)} ގުނަ${n != null ? `<br>${cs.label}، ${o.case_noun} ${fmt(n)} މައްސަލަ ރިޕޯޓުކުރެވިފައި` : ""}${pol != null ? `<br>${cs.label}، ${fmt(pol)} މައްސަލަ ރިޕޯޓުކުރެވިފައި` : ""}</div>')
p.R('`${fmt(v / it * 100, v / it < .1 ? 1 : 0)}% of what interest cost`', '`އިންޓަރެސްޓަށް ހިނގި ޚަރަދުގެ ${fmt(v / it * 100, v / it < .1 ? 1 : 0)}%`')
p.R('const ctx = [["interest", "Interest and financing costs", it, INT, true]', 'const ctx = [["interest", "އިންޓަރެސްޓް އަދި ފައިނޭންސިންގ ޚަރަދު", it, INT, true]')
p.R('["police", "Policing, justice and rights", both, "#f4c95d"]]', '["police", "ފުލުހުން، ޝަރީޢަތް އަދި ޙައްޤުތައް", both, "#f4c95d"]]')
p.R('''$("ctxNote").innerHTML = `To see the size of interest, here it is beside some of the biggest parts of government, over the same period.` + (near && Math.abs(1 - near.r) < .15 ? ` Interest was about the same as the whole of the <b>${near.nm}</b>'s spending.` : "");''',
    '''$("ctxNote").innerHTML = `އިންޓަރެސްޓުގެ ބޮޑުމިން ދެނެގަތުމަށް، އެ މުއްދަތުގައި ސަރުކާރުގެ އެންމެ ބޮޑެތި ބައެއް ބައިތަކާ އެކު މިތަނުގައި ދައްކާލައިފައިވެއެވެ.` + (near && Math.abs(1 - near.r) < .15 ? ` އިންޓަރެސްޓަށް ހިނގި ޚަރަދަކީ <b>${near.nm}</b> ގެ މުޅި ޚަރަދާ ގާތްގަނޑަކަށް އެއްވަރެވެ.` : "");''')
p.R('''{ id: "all", name: "Policing, justice and rights", short: "Policing, justice and rights", noun: "policing, justice and rights", keys: [...SAFE, ...RIGHTS] },
      { id: "safety", name: "Policing and justice", short: "Policing and justice", noun: "policing and justice", keys: SAFE },
      { id: "rights", name: "Protection and rights", short: "Protection and rights", noun: "protection and rights", keys: RIGHTS },
      ...O.map(o => ({ id: o.key, name: o.name, short: o.name, noun: "the " + o.name, keys: [o.key] })),''',
    '''{ id: "all", name: "ފުލުހުން، ޝަރީޢަތް އަދި ޙައްޤުތައް", short: "ފުލުހުން، ޝަރީޢަތް، ޙައްޤު", noun: "ފުލުހުންނާއި ޝަރީޢަތާއި ޙައްޤުތައް", keys: [...SAFE, ...RIGHTS] },
      { id: "safety", name: "ފުލުހުން އަދި ޝަރީޢަތް", short: "ފުލުހުން، ޝަރީޢަތް", noun: "ފުލުހުންނާއި ޝަރީޢަތް", keys: SAFE },
      { id: "rights", name: "ރައްކާތެރިކުރުން އަދި ޙައްޤުތައް", short: "ރައްކާތެރިކަން، ޙައްޤު", noun: "ރައްކާތެރިކުރުމާއި ޙައްޤުތައް", keys: RIGHTS },
      ...O.map(o => ({ id: o.key, name: o.name, short: o.name, noun: o.name, keys: [o.key] })),''')
p.R('end(yI, INT, z.i, "Interest") + end(yG, GRP, z.g, g.short.length > 18 ? g.short.slice(0, 17) + "…" : g.short);',
    'end(yI, INT, z.i, "އިންޓަރެސްޓް") + end(yG, GRP, z.g, g.short.length > 26 ? g.short.slice(0, 25) + "…" : g.short);')
p.R('aria-label="Growth of interest and ${g.name} since ${a.year}"', 'aria-label="${a.year} އިން ފެށިގެން އިންޓަރެސްޓާއި ${g.name} ބޮޑުވި މިންވަރު"')
p.R('row("Interest", MV.money(p.h.r.i[2] * M, p.h.d) + `, ×${fmt(p.i, 1)}`) + row(g.short, MV.money(gsum(p.h, g) * M, p.h.d) + `, ×${fmt(p.g, 1)}`);',
    'row("އިންޓަރެސްޓް", MV.money(p.h.r.i[2] * M, p.h.d) + `، <bdi>×${fmt(p.i, 1)}</bdi>`) + row(g.short, MV.money(gsum(p.h, g) * M, p.h.d) + `، <bdi>×${fmt(p.g, 1)}</bdi>`);')
p.R('$("yearNote").textContent = "No figures for this office yet."; return; }', '$("yearNote").textContent = "މި އޮފީހުގެ އަދަދުތައް އަދި ނެތެވެ."; return; }')
p.R('const partNote = all.some(h => !h.full) ? ` ${ly}* is the year so far.` : "";'.replace("const partNote", "partNote"), 'partNote = all.some(h => !h.full) ? ` ${ly}* އަކީ މިހާތަނަށް ހުރި އަދަދެވެ.` : "";')
p.R('$("yearNote").textContent = `How much each has grown since ${a.year}, in the money of each year. ×2 means it doubled. Full years only.`;',
    '$("yearNote").textContent = `${a.year} އިން ފެށިގެން ކޮންމެ ބައެއް ބޮޑުވި މިންވަރު، ކޮންމެ އަހަރެއްގެ ފައިސާއިން. \\u2066×2\\u2069 ގެ މާނައަކީ ދެގުނަ ވުމެވެ. ހިމަނާފައިވަނީ ފުރިހަމަ އަހަރުތައް އެކަނި.`;')
p.R_all('[INT, "Interest and financing costs"]', '[INT, "އިންޓަރެސްޓް އަދި ފައިނޭންސިންގ ޚަރަދު"]')
p.R('label: `Interest as a multiple of ${g.name}`', 'label: `${g.name} އާ އަޅާބަލާއިރު އިންޓަރެސްޓް ކިތައް ގުނަ`')
p.R_all('return `<b>${h.full ? h.year : `${h.year}, to ${dayLabel(h.d)}`}</b>` + row("Interest", MV.money(h.r.i[2] * M, h.d))',
        'return `<b>${h.full ? h.year : `${h.year}، ${dayLabel(h.d)} އާ ހަމައަށް`}</b>` + row("އިންޓަރެސްޓް", MV.money(h.r.i[2] * M, h.d))')
p.R('row("Interest is", times(h.r.i[2] / gsum(h, g)) + " times as much")', 'row("އިންޓަރެސްޓް", times(h.r.i[2] / gsum(h, g)) + " ގުނަ")')
p.R('$("yearNote").textContent = `For every rufiyaa spent on ${g.noun}, how many were paid in interest.` + partNote;',
    '$("yearNote").textContent = `${g.noun} އަށް ހޭދަކުރި ކޮންމެ ރުފިޔާއަކަށް، އިންޓަރެސްޓަށް ދެއްކި ރުފިޔާ.` + partNote;')
p.R('key([[INT, `Interest, as a multiple of ${g.noun}`]]);', 'key([[INT, `${g.noun} އާ އަޅާބަލާއިރު އިންޓަރެސްޓް ކިތައް ގުނަ`]]);')
p.R('label: `Interest and ${g.name} by year`', 'label: `އަހަރުން އަހަރަށް އިންޓަރެސްޓް އަދި ${g.name}`')
p.R('$("yearNote").textContent = `Totals for each year in ${big ? "billions" : "millions"} of ${MV.state.cur === "USD" ? "US dollars" : "rufiyaa"}${MV.isReal() ? `, in ${MV.baseLabel()}` : ""}.` + partNote;',
    '$("yearNote").textContent = `ކޮންމެ އަހަރެއްގެ ޖުމްލަ، ${big ? "ބިލިއަން" : "މިލިއަން"} ${MV.state.cur === "USD" ? "ޑޮލަރުން" : "ރުފިޔާއިން"}${MV.isReal() ? `، ${MV.baseLabel()}` : ""}.` + partNote;')
p.R('$("yearLine").innerHTML = a && z && a !== z ? `From ${a.year} to ${z.year}, interest grew <b>${fmt(z.r.i[2] / a.r.i[2], 1)} times</b> while spending on ${g.noun} grew <b>${fmt(gsum(z, g) / gsum(a, g), 1)} times</b>. In ${z.year} interest was <b>${times(z.r.i[2] / gsum(z, g))} times</b> what was spent on ${g.noun}.` : "";',
    '$("yearLine").innerHTML = a && z && a !== z ? `${a.year} އިން ${z.year} އަށް، އިންޓަރެސްޓް <b>${fmt(z.r.i[2] / a.r.i[2], 1)} ގުނަ</b> ބޮޑުވިއެވެ. އެ މުއްދަތުގައި ${g.noun} އަށް ހިނގި ޚަރަދު ބޮޑުވީ <b>${fmt(gsum(z, g) / gsum(a, g), 1)} ގުނަ</b>އެވެ. ${z.year} ގައި އިންޓަރެސްޓަކީ ${g.noun} އަށް ހިނގި ޚަރަދުގެ <b>${times(z.r.i[2] / gsum(z, g))} ގުނަ</b> އެވެ.` : "";')

# cases
p.R('`<option value="0">Whole year${y == ly ? " so far" : ""}</option>`', '`<option value="0">މުޅި އަހަރު${y == ly ? "، މިހާތަނަށް" : ""}</option>`')
p.R('`<option value="ytd">January to ${MONTHS[ms[ms.length - 1] - 1]}</option>`', '`<option value="ytd">${MONTHS[0]} އިން ${MONTHS[ms[ms.length - 1] - 1]} އަށް</option>`')
p.R('label: "Cases reported each year",', 'label: "ކޮންމެ އަހަރަކު ރިޕޯޓުކުރެވުނު މައްސަލަތައް",')
p.R('yFmt: v => fmt(v, v % 1 ? 1 : 0) + "k",', 'yFmt: v => fmt(v, v % 1 ? 1 : 0) + " ހާސް",')
p.R('tip: i => `<b>${rows[i].y}${rows[i].y == ly ? ", so far" : ""}</b>` + row("Cases", fmt(rows[i].t)) + row("Source", "Police website") });',
    'tip: i => `<b>${rows[i].y}${rows[i].y == ly ? "، މިހާތަނަށް" : ""}</b>` + row("މައްސަލަ", fmt(rows[i].t)) + row("ލިބުނު ތަން", "ފުލުހުންގެ ވެބްސައިޓް") });')
p.R('const when = m === "0" ? (y == ly ? `so far in ${y}` : `in ${y}`) : m === "ytd" ? `${$("cMonth").selectedOptions[0].text} ${y}` : `in ${MONTHS[m - 1]} ${y}`;',
    'const when = m === "0" ? (y == ly ? `${y} ގައި މިހާތަނަށް` : `${y} ގައި`) : m === "ytd" ? `${y} ގެ ${$("cMonth").selectedOptions[0].text}` : `${MONTHS[m - 1]} ${y} ގައި`;')
p.R('return `${String(t.getUTCHours()).padStart(2, "0")}:${String(t.getUTCMinutes()).padStart(2, "0")}, ${dayLabel(t.toISOString().slice(0, 10))}, Malé time`; })()',
    'return `${dayLabel(t.toISOString().slice(0, 10))}، ${String(t.getUTCHours()).padStart(2, "0")}:${String(t.getUTCMinutes()).padStart(2, "0")} (މާލޭ ވަގުތު)`; })()')
p.R('const src = `Figures from the police website, as of ${asOf}.`;', 'const src = `އަދަދުތައް ނަގާފައިވަނީ ފުލުހުންގެ ވެބްސައިޓުން، ${asOf} ގެ ނިޔަލަށް.`;')
p.R('$("casesNote").textContent = `${fmt(total)} cases ${totalOnly != null ? "logged" : "reported"} ${when}. ${src}`;',
    '$("casesNote").textContent = `${when} ${fmt(total)} މައްސަލަ ${totalOnly != null ? "ރަޖިސްޓަރީކުރެވުނެވެ" : "ރިޕޯޓުކުރެވުނެވެ"}. ${src}`;')
p.R('if (mins < 60) return `${Math.max(1, Math.round(mins))} minutes`; const h = mins / 60; if (h < 10) { const hh = Math.floor(h), mm = Math.round((h - hh) * 60); return mm ? `${hh} hr${hh > 1 ? "s" : ""} ${mm} min` : `${hh} hour${hh > 1 ? "s" : ""}`; } if (h < 48) return `${Math.round(h)} hours`; const d = h / 24; return d < 14 ? `${Math.round(d)} days` : `${Math.round(d / 7)} weeks`; };',
    'if (mins < 60) return `${Math.max(1, Math.round(mins))} މިނިޓު`; const h = mins / 60; if (h < 10) { const hh = Math.floor(h), mm = Math.round((h - hh) * 60); return mm ? `${hh} ގަޑިއިރާއި ${mm} މިނިޓު` : `${hh} ގަޑިއިރު`; } if (h < 48) return `${Math.round(h)} ގަޑިއިރު`; const d = h / 24; return d < 14 ? `${Math.round(d)} ދުވަސް` : `${Math.round(d / 7)} ހަފްތާ`; };')
p.R('<span class="big">A case every ${every(total)}</span><span class="sm">About ${fmt(perDay(total), perDay(total) < 10 ? 1 : 0)} a day, ${when}, counting waking hours from 6 am to midnight.</span>',
    '<span class="big">ކޮންމެ ${every(total)} ތެރޭގައި މައްސަލައެއް</span><span class="sm">${when} ދުވާލަކު ގާތްގަނޑަކަށް ${fmt(perDay(total), perDay(total) < 10 ? 1 : 0)} މައްސަލަ. ގުނާފައިވަނީ ހެނދުނު 6 އިން ރޭގަނޑު 12 އާ ހަމައަށް، މީހުން ހޭލައިތިބޭ ގަޑިތަކެވެ.</span>')
p.R('<span class="sm k">${c}</span><span class="big">One every ${every(n)}</span><span class="sm">${perDay(n) >= 1 ? `About ${fmt(perDay(n), perDay(n) < 10 ? 1 : 0)} a day` : `About ${fmt(perDay(n) * 7, perDay(n) * 7 < 10 ? 1 : 0)} a week`}</span>',
    '<span class="sm k">${CN(c)}</span><span class="big">ކޮންމެ ${every(n)} ތެރޭގައި އެކެއް</span><span class="sm">${perDay(n) >= 1 ? `ދުވާލަކު ގާތްގަނޑަކަށް ${fmt(perDay(n), perDay(n) < 10 ? 1 : 0)}` : `ހަފްތާއަކު ގާތްގަނޑަކަށް ${fmt(perDay(n) * 7, perDay(n) * 7 < 10 ? 1 : 0)}`}</span>')
p.R('<div class="row"><span>${c}</span><div class="bar">', '<div class="row"><span>${CN(c)}</span><div class="bar">')
p.R('<p class="hint">The types of case aren\'t published for single months before the police website began.</p>',
    '<p class="hint">ފުލުހުންގެ ވެބްސައިޓް ފެށުމުގެ ކުރިން، ކޮންމެ މަހެއްގެ މައްސަލަތަކުގެ ބާވަތްތައް ވަކިން ޝާއިޢުކޮށްފައެއް ނުވެއެވެ.</p>')
p.R('${k === "police" ? "Handled by the police" : `Also matched to the ${office(k).name}`}', '${k === "police" ? "ފުލުހުން ބަލާ މައްސަލަ" : `${office(k).name} އާ ވެސް ގުޅުވާފައި`}')

# since your last visit, footer, error
p.R('say: p => `New weekly figures, now to <b>${dayLabel(LR.d)}</b>. The last ones you saw ran to ${dayLabel(p)}.` }',
    'say: p => `ހަފްތާގެ އާ އަދަދުތައް ނެރެފިއެވެ. މިހާރު އަދަދުތައް ހުރީ <b>${dayLabel(LR.d)}</b> އާ ހަމައަށެވެ. ކުރިން ފެނިވަޑައިގެންނެވީ ${dayLabel(p)} އާ ހަމައަށް އަދަދުތަކެވެ.` }')
p.R('`Interest paid this year went up by <b>${cur(LR.i[2] - p, LR.d)}</b>, to ${cur(LR.i[2], LR.d)}.`',
    '`މި އަހަރު އިންޓަރެސްޓަށް ދެއްކި ފައިސާ <b>${cur(LR.i[2] - p, LR.d)}</b> އިތުރުވެ، ${cur(LR.i[2], LR.d)} އަށް އަރައިފިއެވެ.`')
p.R('`Policing, justice and rights spending went up by <b>${cur(both(LR) - p, LR.d)}</b>.`',
    '`ފުލުހުންނާއި، ޝަރީޢަތާއި، ޙައްޤުތަކަށް ހިނގި ޚަރަދު <b>${cur(both(LR) - p, LR.d)}</b> އިތުރުވެއްޖެއެވެ.`')
p.R('$("fetched").textContent = `Ministry of Finance, Weekly Fiscal Developments, report of ${dayLabel(LR.d)}` + (C ? ". Maldives Police Service" : "") + `. Exchange rates and prices from MMA Statistics Database, last fetched ${MV.fetched(data.fetched_at)}, Malé time.`;',
    '$("fetched").textContent = `މާލިއްޔަތު ވުޒާރާގެ Weekly Fiscal Developments، ${dayLabel(LR.d)} ގެ ރިޕޯޓު` + (C ? ". ދިވެހި ފުލުހުންގެ ޚިދުމަތް" : "") + `. އެކްސްޗޭންޖް ރޭޓާއި އަގުތައް MMA ގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން. އެންމެ ފަހުން ހޯދީ ${MV.fetched(data.fetched_at)} (މާލޭ ވަގުތު).`;')
p.R('$("lede").textContent = "These figures haven\'t been built yet. They appear after the next automatic update.";',
    '$("lede").textContent = "މި އަދަދުތައް އަދި ތައްޔާރުވެފައެއް ނުވެއެވެ. އަމިއްލައަށް ކުރާ ދެން އަންނަ އަޕްޑޭޓާއެކު މި އަދަދުތައް ފެންނާނެއެވެ.";')

p.footer()
p.relink()
p.write()
