"""Dhivehi taxes page (dv-revenue.html) from revenue.html. See common.py and GLOSSARY.md."""
from common import Page

p = Page("revenue")
p.head("ޓެކްސް · ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި",
       "2010 އިން ފެށިގެން MIRA އިން ހޯދި ޓެކްސް، ފީ އަދި ކުލި، އަދި އޭގެ ތެރެއިން އެމެރިކާ ޑޮލަރުން ދެއްކި މިންވަރު.")
p.header()
p.R('content="An island above a sea, with a dashed line deep below the surface, showing what the Maldivian government owes and the debt as a share of GDP."',
    'content="ކަނޑުގެ މައްޗަށް ފެންނަ ރަށެއް، އަދި ފެނުގެ ފުނޔަށް ދަމާފައިވާ ރޮނގެއް. ދިވެހި ސަރުކާރުގެ ދަރަނި އަދި ޖީޑީޕީއާ އަޅާކިޔާއިރު ދަރަނި."')

# ---- right-to-left fixes for this page's own styles ----
p.R('</style>\n</head>', '''  /* Dhivehi (right to left) */
  html[lang="dv"] .rev-table th, html[lang="dv"] .rev-table td { text-align: left; }
  html[lang="dv"] .rev-table th:first-child, html[lang="dv"] .rev-table td:first-child { text-align: right; }
  html[lang="dv"] .rev-table td .sw { margin-right: 0; margin-left: .5rem; }
  html[lang="dv"] .rev-table tr.sub td:first-child { padding-left: .75rem; padding-right: 2rem; }
  html[lang="dv"] .bar-share { margin-left: 0; margin-right: .6rem; }
  html[lang="dv"] .tip .row span:last-child { direction: ltr; unicode-bidi: isolate; }
  html[lang="dv"] .cmp-sum .v, html[lang="dv"] .rev-table td:not(:first-child) { unicode-bidi: plaintext; }
</style>
</head>''')

# ---- intro ----
p.R('<h1>What MIRA collects, and how much is paid in dollars</h1>', '<h1>MIRA އިން ހޯދާ ފައިސާ، އަދި އޭގެ ތެރެއިން ޑޮލަރުން ދައްކާ މިންވަރު</h1>')
p.R("<p class=\"lede\">Maldives Inland Revenue Authority (MIRA) collects most of the government's taxes, along with fees and rents such as resort land rent. A large part is paid in US dollars, mainly by resorts and other tourism businesses. Those dollars matter for the debt, because loans from abroad have to be repaid in foreign currency.</p>",
    '<p class="lede">ސަރުކާރުގެ ގިނަ ޓެކްސްތަކާއި، ރިސޯޓް ބިމުގެ ކުލި ފަދަ ފީތަކާއި ކުލިތައް ހޯދަނީ މޯލްޑިވްސް އިންލެންޑް ރެވެނިއު އޮތޯރިޓީ (MIRA) އިންނެވެ. އޭގެ ބޮޑު ބައެއް ދައްކަނީ އެމެރިކާ ޑޮލަރުންނެވެ. ގިނައިން ދައްކަނީ ރިސޯޓުތަކާއި ފަތުރުވެރިކަމުގެ އެހެން ވިޔަފާރިތަކުންނެވެ. ބޭރުން ނަގާ ލޯންތައް އަނބުރާ ދައްކަންޖެހެނީ ބޭރުގެ ފައިސާއިން ކަމުން، ދަރަނީގެ ހިސާބުގައި އެ ޑޮލަރު މުހިންމެވެ.</p>')
p.R("<p class=\"goodtoknow\"><b>Good to know.</b> Tax collected by MIRA isn't the same as all of the government's income. <span class=\"term\" role=\"button\" tabindex=\"0\" data-term=\"taxrev\">Why not?</span></p>",
    '<p class="goodtoknow"><b>އެނގިލައްވާ.</b> MIRA އިން ހޯދާ ޓެކްސް އަކީ ސަރުކާރުގެ ހުރިހާ އާމްދަނީއެއް ނޫނެވެ. <span class="term" role="button" tabindex="0" data-term="taxrev">ސަބަބަކީ ކޮބާ؟</span></p>')

# ---- latest figures ----
p.R('<h2>Latest figures</h2>', '<h2>އެންމެ ފަހުގެ އަދަދުތައް</h2>')
p.R('id="sMonthL">collected in the latest month</div>', 'id="sMonthL">އެންމެ ފަހު މަހު ހޯދި</div>')
p.R('id="s12L">collected in the last 12 months</div>', 'id="s12L">ފާއިތުވި 12 މަހު ހޯދި</div>')
p.R('id="sYtdL">collected this year so far</div>', 'id="sYtdL">މި އަހަރު މިހާތަނަށް ހޯދި</div>')

# ---- compare ----
p.R('<h2>Compare any two periods</h2>', '<h2>ދެ މުއްދަތެއް އަޅާކިޔުއްވާ</h2>')
p.R('<p>Pick a month, a year or any run of months, and compare it with another. Use the shortcuts or set the dates yourself.</p>',
    '<p>މަހެއް، އަހަރެއް ނުވަތަ ފަހަރަށް އަންނަ މަސްތަކެއް ހޮވާލައްވައި، އެހެން މުއްދަތަކާ އަޅާކިޔުއްވާ. ކުރުމަގުތައް ބޭނުންކުރައްވާ، ނުވަތަ ތާރީޚުތައް އަމިއްލައަށް ހޮވާލައްވާ.</p>')
p.R('aria-label="Shortcuts"', 'aria-label="ކުރުމަގުތައް"')
p.R('</i>This period</span>', '</i>މި މުއްދަތު</span>')
p.R('</i>Compared with</span>', '</i>އަޅާކިޔަނީ</span>')
p.R_all('aria-label="Show as"', 'aria-label="ދައްކާ ގޮތް"')
p.R('aria-pressed="true">Totals</button><button type="button" data-avg="1" aria-pressed="false">Average per month</button>',
    'aria-pressed="true">ޖުމްލަ</button><button type="button" data-avg="1" aria-pressed="false">މަހަކަށް އެވަރެޖް</button>')

# ---- this year against other years ----
p.R('<h2>This year against other years</h2>', '<h2>މި އަހަރު، އެހެން އަހަރުތަކާ އަޅާކިޔާއިރު</h2>')
p.R('aria-label="Figures shown"><button type="button" data-ymode="ytd" aria-pressed="true">Year so far</button><button type="button" data-ymode="month" aria-pressed="false">Each month</button>',
    'aria-label="ދައްކާ އަދަދުތައް"><button type="button" data-ymode="ytd" aria-pressed="true">އަހަރު ފެށުނީއްސުރެ</button><button type="button" data-ymode="month" aria-pressed="false">ކޮންމެ މަހެއް</button>')
p.R('aria-label="What to show"', 'aria-label="ދައްކާނެ އަދަދު"')
p.R('aria-label="Years to show"', 'aria-label="ދައްކާނެ އަހަރުތައް"')

# ---- history ----
p.R('<h2>The whole history</h2>', '<h2>ފުރިހަމަ ތާރީޚު</h2>')
p.R('aria-label="Detail"><button type="button" data-gran="year" aria-pressed="true">By year</button><button type="button" data-gran="month" aria-pressed="false">By month</button>',
    'aria-label="ތަފްސީލު"><button type="button" data-gran="year" aria-pressed="true">އަހަރުން</button><button type="button" data-gran="month" aria-pressed="false">މަހުން</button>')
p.R('aria-label="Period" id="rangeCtl" hidden><button type="button" data-range="all" aria-pressed="true">All</button><button type="button" data-range="2015" aria-pressed="false">Since 2015</button><button type="button" data-range="3" aria-pressed="false">3 years</button>',
    'aria-label="މުއްދަތު" id="rangeCtl" hidden><button type="button" data-range="all" aria-pressed="true">ހުރިހާ</button><button type="button" data-range="2015" aria-pressed="false">2015 އިން ފެށިގެން</button><button type="button" data-range="3" aria-pressed="false">3 އަހަރު</button>')
p.R('<div class="hint">Hover or tap the chart to see the figures.</div>', '<div class="hint">އަދަދުތައް ބެއްލެވުމަށް ޗާޓުގެ މައްޗަށް މައުސް ގެންދަވާ، ނުވަތަ ފިއްތަވާ.</div>')

# ---- by tax ----
p.R('<h2>Where the money comes from</h2>', '<h2>ފައިސާ ލިބެނީ ކޮންތާކުން</h2>')
p.R('aria-label="Which collections"><button type="button" data-which="all" aria-pressed="true">All collections</button>',
    'aria-label="ހިމަނާ ފައިސާ"><button type="button" data-which="all" aria-pressed="true">ހުރިހާ ފައިސާ</button>')
p.R('data-as="amt" aria-pressed="true">Amounts</button><button type="button" data-as="pct" aria-pressed="false">Shares</button>',
    'data-as="amt" aria-pressed="true">އަދަދު</button><button type="button" data-as="pct" aria-pressed="false">ބައި (%)</button>')
p.R('<div class="hint">Hover or tap a year to see each tax.</div>', '<div class="hint">ކޮންމެ ޓެކްހެއް ބެއްލެވުމަށް އަހަރެއްގެ މައްޗަށް މައުސް ގެންދަވާ، ނުވަތަ ފިއްތަވާ.</div>')
p.R('<h3>Where the dollars came from in</h3><select id="tblYear" aria-label="Year">', '<h3>ޑޮލަރު ލިބުނު ތަންތަން، އަހަރު</h3><select id="tblYear" aria-label="އަހަރު">')

# ---- reading these figures ----
p.R('<h2>Reading these figures</h2>', '<h2>މި އަދަދުތައް ކިޔާނެ ގޮތް</h2>')
p.R("<p>These figures come from MIRA's monthly revenue collection files. One lists everything MIRA collected, and the other lists the part paid in US dollars. MIRA isn't the only collector. Import duties are collected by Maldives Customs Service, and the government also receives dividends from state companies, other income and grants, so these totals are smaller than all government revenue. <span id=\"shareOfAll\"></span></p>",
    '<p>މި އަދަދުތައް ނަގާފައިވަނީ MIRA އިން ކޮންމެ މަހަކު ޝާއިޢުކުރާ ފައިސާ ހޯދުމުގެ ފައިލުތަކުންނެވެ. އެއް ފައިލުގައި MIRA އިން ހޯދި ހުރިހާ ފައިސާ ހިމެނެއެވެ. އަނެއް ފައިލުގައި ހިމެނެނީ އެމެރިކާ ޑޮލަރުން ދެއްކި ބައެވެ. ސަރުކާރަށް ފައިސާ ހޯދަނީ MIRA އެކަނި ނޫނެވެ. އިމްޕޯޓް ޑިއުޓީ ހޯދަނީ ދިވެހި ކަސްޓަމްސް އިންނެވެ. އަދި ސަރުކާރު ކުންފުނިތަކުގެ ޑިވިޑެންޑާއި، އެހެނިހެން އާމްދަނީއާއި، އެހީ ވެސް ސަރުކާރަށް ލިބެއެވެ. އެހެންކަމުން، މި ޖުމްލަތައް ސަރުކާރުގެ ހުރިހާ އާމްދަނީއަށްވުރެ ކުޑައެވެ. <span id="shareOfAll"></span></p>')
p.R("<p>MIRA's rufiyaa figures already include the dollar payments, converted at MIRA's own rate, which is slightly below MMA's reference rate. This page converts the dollar figures at each month's MMA reference rate. For taxes paid almost entirely in dollars, such as tourism GST and green tax, that can come out a little above MIRA's own rufiyaa total, so the dollar part of each tax is capped at that total. Dollar figures start in January 2011.</p>",
    '<p>MIRA ގެ ރުފިޔާގެ އަދަދުތަކުގައި ޑޮލަރުން ދެއްކި ފައިސާ ވެސް ހިމެނެއެވެ. އެ ފައިސާ ރުފިޔާއަށް ބަދަލުކޮށްފައިވަނީ MIRA ގެ އަމިއްލަ ރޭޓުންނެވެ. އެ ރޭޓަކީ MMA ގެ ރިފަރެންސް ރޭޓަށްވުރެ ކުޑަކޮށް ދަށް ރޭޓެކެވެ. މި ޞަފްޙާގައި ޑޮލަރުގެ އަދަދުތައް ބަދަލުކުރަނީ ކޮންމެ މަހެއްގެ MMA ގެ ރިފަރެންސް ރޭޓުންނެވެ. ޓޫރިޒަމް ޖީއެސްޓީ އާއި ގްރީން ޓެކްސް ފަދަ، ގާތްގަނޑަކަށް މުޅިން ޑޮލަރުން ދައްކާ ޓެކްސްތަކުގައި، އެ ގޮތަށް ހިސާބުކުރުމުން MIRA ގެ ރުފިޔާގެ ޖުމްލައަށްވުރެ ކުޑަކޮށް ބޮޑުވެދާނެއެވެ. އެހެންކަމުން، ކޮންމެ ޓެކްހެއްގެ ޑޮލަރުގެ ބައި، އެ ޖުމްލައަށްވުރެ ބޮޑުނުވާނެ ގޮތަށް ހަދާފައިވެއެވެ. ޑޮލަރުގެ އަދަދުތައް ފެށެނީ ޖަނަވަރީ 2011 އިންނެވެ.</p>')
p.R("<p>Resort land and leases includes one-off payments. Lease period extension fees, paid by resorts to extend their island leases, jump in some years and fall back in others, so a big year for this line is not a sign of lasting growth. The compare table and the chart pop-ups show them separately. Tourism tax was a fixed charge for each tourist night that ended in 2014. Tourism GST began in 2011 and is now the largest single tax.</p>",
    '<p>ރިސޯޓް ކުލި އަދި ލީސްގައި އެއްފަހަރު ދައްކާ ފައިސާ ވެސް ހިމެނެއެވެ. ރިސޯޓުތަކުން ރަށުގެ ލީސް މުއްދަތު އިތުރުކުރުމަށް ދައްކާ ފީ، ބައެއް އަހަރުތަކުގައި ވަރަށް ބޮޑުވެ، އަނެއްކާ ދަށްވެއެވެ. އެހެންކަމުން، މި ބައިގައި ބޮޑު އަހަރެއް އައުމަކީ ދެމިއޮންނަ ކުރިއެރުމެއްގެ ނިޝާނެއް ނޫނެވެ. އަޅާކިޔާ ތާވަލާއި ޗާޓުގެ ޕޮޕްއަޕްތަކުގައި އެ ފީ ވަކިން ދައްކައެވެ. ޓޫރިޒަމް ޓެކްސް އަކީ ކޮންމެ ފަތުރުވެރިއެއްގެ ކޮންމެ ރެއަކަށް ނަގާ ކަނޑައެޅިފައިވާ ފީއެކެވެ. އެ ޓެކްސް ނިމުނީ 2014 ގައެވެ. ޓޫރިޒަމް ޖީއެސްޓީ ފެށުނީ 2011 ގައެވެ. މިހާރު އެއީ އެންމެ ބޮޑު ޓެކްސްއެވެ.</p>')
p.R("<p>Comparisons between periods follow the Real switch. With Real on, both periods are shown in today's prices, so the change reflects growth after inflation. The latest figures at the top are always in the money of the time. MIRA updates these files around the middle of each month, and recent months are provisional until MIRA reconciles them. <a href=\"methodology.html#revenue\">More in the methodology</a>.</p>",
    '<p>މުއްދަތުތައް އަޅާކިޔާއިރު، "ރިއަލް" ސްވިޗު ބޭނުންކުރެވެއެވެ. ރިއަލް ހުޅުވާފައިވާނަމަ، ދެ މުއްދަތުވެސް ދައްކަނީ މިއަދުގެ އަގުތަކުންނެވެ. އެހެންވުމުން، ފެންނަ ބަދަލަކީ އިންފްލޭޝަން ކަނޑާލުމަށްފަހު ވާ ކުރިއެރުމެވެ. މަތީގައިވާ އެންމެ ފަހުގެ އަދަދުތައް އަބަދުވެސް ދައްކަނީ އެ ވަގުތުގެ ފައިސާއިންނެވެ. MIRA އިން މި ފައިލުތައް އާކުރަނީ ކޮންމެ މަހެއްގެ މެދުތެރޭގައެވެ. MIRA އިން ހިސާބުތައް ބައްލަވައި ނިންމަންދެން، ފަހުގެ މަސްތަކުގެ އަދަދުތައް ބަދަލުވެދާނެއެވެ. <a href="methodology.html#revenue">މެތަޑޮލޮޖީގައި އިތުރަށް ކިޔުއްވާ</a>.</p>')

p.R('<span id="fetched">Figures from Maldives Inland Revenue Authority, with exchange rates and prices from Maldives Monetary Authority Statistics Database.</span>',
    '<span id="fetched">އަދަދުތައް ނަގާފައިވަނީ މޯލްޑިވްސް އިންލެންޑް ރެވެނިއު އޮތޯރިޓީންނެވެ. އެކްސްޗޭންޖް ރޭޓާއި އަގުތައް ނަގާފައިވަނީ މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިންނެވެ.</span>')
p.footer()

# ================= inline script =================
# tax names
p.R('LABEL = Object.fromEntries(R.groups.map(g => [g.key, g.label]));',
    'LABEL = Object.fromEntries(R.groups.map(g => [g.key, TAX_DV[g.key] || g.label]));')
p.R('const MON = MV.MONTHS.map(m => m.slice(0, 3));',
    '''const MON = MV.MONTHS;
  const TAX_DV = { tourism_gst: "ޓޫރިޒަމް ޖީއެސްޓީ", gst_other: "ފަތުރުވެރިކަމުން ބޭރުގެ ޖީ.އެސް.ޓީ", green: "ގްރީން ޓެކްސް", airport: "އެއާޕޯޓް ޓެކްސް އަދި ފީ",
                   resort_land: "ރިސޯޓް ކުލި އަދި ލީސް", business: "ބިޒްނަސް ޕްރޮފިޓް ޓެކްސް", personal: "އިންކަމް ޓެކްސް", tourism_tax: "ޓޫރިޒަމް ޓެކްސް (2014 ގައި ނިމުނު)", other: "އެހެނިހެން ޓެކްސް އަދި ފީ" };
  const EN_MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];''')

# latest figures
p.R('`<span class="gold">${fmt(pct(raw(dolM, idx), raw(allM, idx)), 0)}% paid in US dollars</span>`',
    '`<span class="gold">ޑޮލަރުން ދެއްކީ ${fmt(pct(raw(dolM, idx), raw(allM, idx)), 0)}%</span>`')
p.R('`<span class="${chgCls(c)}">${chgTxt(c)} on ${label}</span>`', '`<span class="${chgCls(c)}">${label} އާ އަޅާކިޔާއިރު ${chgTxt(c)}</span>`')
p.R('(selI === N - 1 ? `The latest month MIRA has published is ${mLabel(lastM.date)}.` : `Showing ${mLabel(lastM.date)}, an earlier month.`) + ` Changes are against the same period a year earlier, in the money of the time.`',
    '(selI === N - 1 ? `MIRA އިން ޝާއިޢުކޮށްފައިވާ އެންމެ ފަހު މަހަކީ ${mLabel(lastM.date)} އެވެ.` : `ދައްކަނީ ކުރީގެ މަހެއް، ${mLabel(lastM.date)} ގެ އަދަދުތަކެވެ.`) + ` ބަދަލު ދައްކަނީ އެއް އަހަރު ކުރީގެ އެ މުއްދަތާ އަޅާކިޔައި، އެ ވަގުތުގެ ފައިސާއިންނެވެ.`')
p.R('`collected in ${mLabel(lastM.date)}`', '`${mLabel(lastM.date)} ގައި ހޯދި`')
p.R('`collected in the 12 months to ${mLabel(lastM.date)}`', '`${mLabel(lastM.date)} އާ ހަމައަށް 12 މަހު ހޯދި`')
p.R('line(l12, p12, "the 12 months before")', 'line(l12, p12, "ކުރީގެ 12 މަހާ")')
p.R('`collected from January to ${MV.MONTHS[lastM.mo - 1]} ${lastM.y}`', '`${lastM.y} ގެ ޖަނަވަރީއިން ${MV.MONTHS[lastM.mo - 1]} އާ ހަމައަށް ހޯދި`')
p.R('`the same months of ${Number(lastM.y) - 1}`', '`${Number(lastM.y) - 1} ގެ އެ މަސްތަކާ`')
p.R('(k === 0 ? ", latest" : "")', '(k === 0 ? "، އެންމެ ފަހު" : "")')
p.R('what: "MIRA\'s monthly collection figures"', 'what: "MIRA އިން ކޮންމެ މަހަކު ހޯދާ ފައިސާގެ އަދަދުތައް"')
p.R('`MIRA\'s figures for <b>${mLabel(LM.date)}</b> are out. The last month you saw was ${mLabel(p + "-15")}.`',
    '`MIRA ގެ <b>${mLabel(LM.date)}</b> ގެ އަދަދުތައް ނެރެފިއެވެ. ފަހުން ބެއްލެވި މަހަކީ ${mLabel(p + "-15")} އެވެ.`')

# compare tool
p.R('aria-label="From month">', 'aria-label="ފަށާ މަސް">')
p.R('aria-label="From year">', 'aria-label="ފަށާ އަހަރު">')
p.R('<span class="to">to</span>', '<span class="to">އިން</span>')
p.R('aria-label="To month">', 'aria-label="ނިމޭ މަސް">')
p.R('aria-label="To year">', 'aria-label="ނިމޭ އަހަރު">')
p.R('label: "Latest month vs a year earlier"', 'label: "އެންމެ ފަހު މަސް، އަހަރެއް ކުރީގެ އެ މަހާ"')
p.R('label: "Last 12 months vs the 12 before"', 'label: "ފާއިތުވި 12 މަސް، ކުރީގެ 12 މަހާ"')
p.R('label: `${lastM.y} so far vs the same months of ${Number(lastM.y) - 1}`', 'label: `${lastM.y} މިހާތަނަށް، ${Number(lastM.y) - 1} ގެ އެ މަސްތަކާ`')
p.R('label: `${fy} vs ${fyPrev}`', 'label: `${fy}، ${fyPrev} އާ`')
p.R('label: `${fy} vs 2019, before COVID`', 'label: `${fy}، ކޮވިޑުގެ ކުރީގެ 2019 އާ`')
p.R('`${k === "B" ? "This period" : "Compared with"} ends before it starts.`', '`${k === "B" ? "މި މުއްދަތު" : "އަޅާކިޔާ މުއްދަތު"} ނިމެނީ ފެށުމުގެ ކުރިންނެވެ. ތާރީޚުތައް ބަދަލުކުރައްވާ.`')
p.R('if (A.y === B.y) return `${MV.MONTHS[A.mo - 1]} to ${MV.MONTHS[B.mo - 1]} ${A.y}`;\n      return `${MV.MONTHS[A.mo - 1]} ${A.y} to ${MV.MONTHS[B.mo - 1]} ${B.y}`;',
    'if (A.y === B.y) return `${MV.MONTHS[A.mo - 1]} އިން ${MV.MONTHS[B.mo - 1]} ${A.y} އަށް`;\n      return `${MV.MONTHS[A.mo - 1]} ${A.y} އިން ${MV.MONTHS[B.mo - 1]} ${B.y} އަށް`;')
p.R('per = avg && (nA > 1 || nB > 1) ? " a month" : "";', 'per = avg && (nA > 1 || nB > 1) ? " މަހަކަށް" : "";')
p.R('const sufA = avg && nA > 1 ? ", average a month" : "", sufB = avg && nB > 1 ? ", average a month" : "";',
    'const sufA = avg && nA > 1 ? "، މަހަކަށް އެވަރެޖް" : "", sufB = avg && nB > 1 ? "، މަހަކަށް އެވަރެޖް" : "";')
p.R('uB ? `${money(xB)} paid in US dollars, ${fmt(pct(raw(dolM, iB), raw(allM, iB)), 0)}%`', 'uB ? `ޑޮލަރުން ދެއްކީ ${money(xB)}، ${fmt(pct(raw(dolM, iB), raw(allM, iB)), 0)}%`')
p.R('uA ? `${money(xA)} paid in US dollars, ${fmt(pct(raw(dolM, iA), raw(allM, iA)), 0)}%`', 'uA ? `ޑޮލަރުން ދެއްކީ ${money(xA)}، ${fmt(pct(raw(dolM, iA), raw(allM, iA)), 0)}%`')
p.R_all('"Dollar split not published before 2011"', '"ޑޮލަރުގެ ބައި 2011 ގެ ކުރިން ޝާއިޢުނުކުރެއެވެ"')
p.R('card("Change in everything collected"', 'card("ހޯދި ހުރިހާ ފައިސާގެ ބަދަލު"')
p.R('card("Change in the part paid in dollars"', 'card("ޑޮލަރުން ދެއްކި ބައިގެ ބަދަލު"')
p.R('`The two periods have different lengths (${nB} and ${nA} months). Switch to average per month for a fair comparison.`',
    '`ދެ މުއްދަތުގެ ދިގުމިން ތަފާތެވެ (${nB} މަސް އަދި ${nA} މަސް). ޢަދުލުވެރިކޮށް އަޅާކިޔުމަށް "މަހަކަށް އެވަރެޖް" އަށް ބަދަލުކުރައްވާ.`')
p.R_all('"none"', '"ނެތް"')
p.R(': a > 0 ? "−100%" : "new"}', ': a > 0 ? "−100%" : "އާ"}')
p.R('line("of which lease extensions"', 'line("އޭގެ ތެރެއިން ލީސް މުއްދަތު އިތުރުކުރުން"')
p.R('line("of which land conversion"', 'line("އޭގެ ތެރެއިން ބިން ބަދަލުކުރުން"')
p.R('`<tr><th>Tax</th><th>${lB}${sufB} (${sym()})</th><th>${lA}${sufA} (${sym()})</th><th>Change</th></tr>`',
    '`<tr><th>ޓެކްސް</th><th>${lB}${sufB} (${sym()})</th><th>${lA}${sufA} (${sym()})</th><th>ބަދަލު</th></tr>`')
p.R_all('"All MIRA collections"', '"MIRA އިން ހޯދި ހުރިހާ ފައިސާ"')
p.R('"The page address now includes these two periods, so you can copy it to share this comparison."',
    '"މި ދެ މުއްދަތު މިހާރު ޞަފްޙާގެ އެޑްރެހުގައި ހިމެނޭތީ، މި އަޅާކިޔުން ހިއްސާކުރުމަށް އެޑްރެސް ކޮޕީކުރެވޭނެއެވެ."')

# history
p.R('`Everything MIRA collected each year since ${years[0]}, split by the currency it was paid in. The figure under each bar is the share paid in US dollars.` + (partial(lastM.y) ? ` ${lastM.y}* covers January to ${MV.MONTHS[lastM.mo - 1]} only.` : "")',
    '`${years[0]} އިން ފެށިގެން ކޮންމެ އަހަރަކު MIRA އިން ހޯދި ހުރިހާ ފައިސާ، ދެއްކި ފައިސާގެ ބާވަތުން ވަކިކޮށް. ކޮންމެ ބާރެއްގެ ދަށުގައިވާ އަދަދަކީ ޑޮލަރުން ދެއްކި ބައެވެ.` + (partial(lastM.y) ? ` ${lastM.y}* ގައި ހިމެނެނީ ޖަނަވަރީއިން ${MV.MONTHS[lastM.mo - 1]} އާ ހަމައަށް އެކަނިއެވެ.` : "")')
p.R('label: "MIRA collections by year, split by currency", yTitle: `${sym()} bn`', 'label: "MIRA އިން ހޯދި ފައިސާ، އަހަރުން، ފައިސާގެ ބާވަތުން ވަކިކޮށް", yTitle: `${sym()} ބިލިއަން`')
p.R_all('row("Collected by MIRA"', 'row("MIRA އިން ހޯދި"')
p.R('row(`Change on ${years[i - 1]}`', 'row(`${years[i - 1]} އާ އަޅާކިޔާއިރު`')
p.R('row("Paid in rufiyaa"', 'row("ރުފިޔާއިން ދެއްކި"')
p.R_all('row("Share in dollars"', 'row("ޑޮލަރުގެ ބައި"')
p.R('row("In US dollars", "US$ " + short(raw(R.total.usd, ix)))', 'row("ޑޮލަރުން", "$ " + short(raw(R.total.usd, ix)))')
p.R_all('"not published"', '"ޝާއިޢުނުކުރޭ"')
p.R('row("Share of all government revenue"', 'row("ސަރުކާރުގެ ޖުމްލަ އާމްދަނީގެ ބައި"')
p.R('</i>Paid in rufiyaa</span>', '</i>ރުފިޔާއިން ދެއްކި</span>')
p.R('</i>Everything collected</span>', '</i>ހޯދި ހުރިހާ ފައިސާ</span>')
p.R('"Everything MIRA collected each month, and the part paid in US dollars. Collections swing a lot from month to month, because many taxes are paid quarterly or once a year."',
    '"ކޮންމެ މަހަކު MIRA އިން ހޯދި ހުރިހާ ފައިސާ، އަދި އޭގެ ތެރެއިން ޑޮލަރުން ދެއްކި ބައި. ގިނަ ޓެކްސްތައް ދައްކަނީ ތިން މަހުން އެއްފަހަރު ނުވަތަ އަހަރަކު އެއްފަހަރު ކަމުން، މަހުން މަހަށް ހޯދާ ފައިސާ ވަރަށް ބޮޑަށް ތިރިމައްޗަށް ދެއެވެ."')
p.R('label: "MIRA collections by month", maxH: 400, yTitle: `${sym()} m`', 'label: "MIRA އިން ހޯދި ފައިސާ، މަހުން", maxH: 400, yTitle: `${sym()} މިލިއަން`')
p.R('label: `Highest month, ${MV.mShort(hi.date)}`', 'label: `އެންމެ ބޮޑު މަސް، ${MV.mShort(hi.date)}`')
p.R('row(`Change on ${MV.MONTHS[months[r.i].mo - 1].slice(0, 3)} ${months[a].y}`', 'row(`${MV.MONTHS[months[r.i].mo - 1]} ${months[a].y} އާ އަޅާކިޔާއިރު`')
p.R('`In ${f1}, <b>US$ ${short(raw(R.total.usd, fx))}</b> of MIRA\'s collections were paid in US dollars, <b>${fmt(pct(raw(dolM, fx), raw(allM, fx)), 0)}%</b> of the total. In ${f0} it was US$ ${short(raw(R.total.usd, idxOf(f0)))}.`',
    '`${f1} ގައި MIRA އަށް އެމެރިކާ ޑޮލަރުން <b>${short(raw(R.total.usd, fx))} ޑޮލަރު</b> ދައްކާފައިވެއެވެ. އެއީ MIRA އިން ހޯދި ޖުމްލަ ފައިސާގެ <b>${fmt(pct(raw(dolM, fx), raw(allM, fx)), 0)}%</b> އެވެ. ${f0} ގައި އެ އަދަދަކީ ${short(raw(R.total.usd, idxOf(f0)))} ޑޮލަރެވެ.`')

# this year against other years
p.R('`<option value="all">Everything MIRA collected</option>', '`<option value="all">MIRA އިން ހޯދި ހުރިހާ ފައިސާ</option>')
p.R('ywhat === "all" ? "Everything MIRA collected" : ywhat === "usd" ? "The part paid in US dollars"', 'ywhat === "all" ? "MIRA އިން ހޯދި ހުރިހާ ފައިސާ" : ywhat === "usd" ? "ޑޮލަރުން ދެއްކި ބައި"')
p.R('let g = `<text x="${pad.l - 8}" y="12" text-anchor="end" style="font-weight:700">${sym()} m</text>`;', 'let g = `<text x="${pad.l - 8}" y="12" text-anchor="end" style="font-weight:700">${sym()} މިލިއަން</text>`;')
p.R('MV.MONTHS.forEach((m, i) => { if (!small || i % 2 === 0) g += `<text x="${X(i + 1)}" y="${Hc - 8}" text-anchor="middle">${m.slice(0, 3)}</text>`; });',
    'MV.MONTHS.forEach((m, i) => { if (W >= 900 || i % (small ? 3 : 2) === 0) g += `<text x="${X(i + 1)}" y="${Hc - 8}" text-anchor="middle">${m}</text>`; });')
p.R('aria-label="${ytdName()}, ${ymode === "ytd" ? "running total from January" : "each month"}, by year"',
    'aria-label="${ytdName()}، ${ymode === "ytd" ? "ޖަނަވަރީއިން ފެށިގެން ޖުމްލަ" : "ކޮންމެ މަހެއް"}، އަހަރުން"')
p.R('`<b>${ymode === "ytd" ? `January to ${MV.MONTHS[mo - 1]}` : MV.MONTHS[mo - 1]}</b>`', '`<b>${ymode === "ytd" ? `ޖަނަވަރީއިން ${MV.MONTHS[mo - 1]} އާ ހަމައަށް` : MV.MONTHS[mo - 1]}</b>`')
p.R('let note = `${ytdName()}, ${ymode === "ytd" ? "running total from January" : "each month on its own"}, in millions.`;',
    'let note = `${ytdName()}، ${ymode === "ytd" ? "ޖަނަވަރީއިން ފެށިގެން އެއްކޮށް ހިސާބުކޮށް" : "ކޮންމެ މަހެއް ވަކިން"}، މިލިއަނުން.`;')
p.R('` January to ${MV.MONTHS[cur.mo - 1]} ${Ly}: ${money(cur.v * 1e6)}, against ${money(prev.v * 1e6)} in the same months of ${Number(Ly) - 1} (${chgTxt(c)}).` : ` ${MV.MONTHS[cur.mo - 1]} ${Ly}: ${money(cur.v * 1e6)}, against ${money(prev.v * 1e6)} a year earlier (${chgTxt(c)}).`',
    '` ${Ly} ގެ ޖަނަވަރީއިން ${MV.MONTHS[cur.mo - 1]} އާ ހަމައަށް ${money(cur.v * 1e6)} ހޯދިއެވެ. ${Number(Ly) - 1} ގެ އެ މަސްތަކުގައި ހޯދީ ${money(prev.v * 1e6)} އެވެ (${chgTxt(c)}).` : ` ${MV.MONTHS[cur.mo - 1]} ${Ly} ގައި ${money(cur.v * 1e6)} ހޯދިއެވެ. އަހަރެއް ކުރިން ހޯދީ ${money(prev.v * 1e6)} އެވެ (${chgTxt(c)}).`')
p.R('(ymode === "ytd" ? "Each line adds up the months from January, so years can be compared at the same point." : "Each point is one month. Many taxes are paid quarterly or once a year, so some months jump.") + " Pick years above. Hover or tap the chart to compare them."',
    '(ymode === "ytd" ? "ކޮންމެ ރޮނގަކީ ޖަނަވަރީއިން ފެށިގެން މަސްތައް އެއްކުރާ ޖުމްލައެވެ. އެހެންކަމުން، އަހަރުތައް އެއް ހިސާބަކުން އަޅާކިޔޭނެއެވެ." : "ކޮންމެ ތިކިއަކީ އެއް މަހެވެ. ގިނަ ޓެކްސްތައް ދައްކަނީ ތިން މަހުން އެއްފަހަރު ނުވަތަ އަހަރަކު އެއްފަހަރު ކަމުން، ބައެއް މަސްތަކުގައި އަދަދު ފުންމައެވެ.") + " މަތީގައިވާ އަހަރުތައް ހޮވާލައްވާ. އެ އަހަރުތައް އަޅާކިޔުމަށް ޗާޓުގެ މައްޗަށް މައުސް ގެންދަވާ، ނުވަތަ ފިއްތަވާ."')

# by tax
p.R('(which === "usd" ? "The part paid in US dollars, by tax" : "Everything MIRA collected, by tax") + (as === "pct" ? ", as a share of each year\'s total." : ", each year.") + (partial(lastM.y) ? ` ${lastM.y}* is January to ${MV.MONTHS[lastM.mo - 1]}.` : "")',
    '(which === "usd" ? "ޑޮލަރުން ދެއްކި ބައި، ޓެކްސްގެ ބާވަތުން" : "MIRA އިން ހޯދި ހުރިހާ ފައިސާ، ޓެކްސްގެ ބާވަތުން") + (as === "pct" ? "، ކޮންމެ އަހަރެއްގެ ޖުމްލައިން ކޮންމެ ޓެކްހެއްގެ ބައި." : "، ކޮންމެ އަހަރަކު.") + (partial(lastM.y) ? ` ${lastM.y}* ގައި ހިމެނެނީ ޖަނަވަރީއިން ${MV.MONTHS[lastM.mo - 1]} އާ ހަމައަށެވެ.` : "")')
p.R('label: "MIRA collections by tax and year"', 'label: "MIRA އިން ހޯދި ފައިސާ، ޓެކްސާއި އަހަރުން"')
p.R('yTitle: as === "pct" ? "%" : `${sym()} bn`', 'yTitle: as === "pct" ? "%" : `${sym()} ބިލިއަން`')
p.R('>Resort land includes lease extensions ${money(le)}, land conversion ${money(lc)}</span>', '>ރިސޯޓް ކުލީގައި ލީސް މުއްދަތު އިތުރުކުރުން ${money(le)} އާއި ބިން ބަދަލުކުރުން ${money(lc)} ހިމެނެއެވެ</span>')
p.R('row("Total", money(tot[i]))', 'row("ޖުމްލަ", money(tot[i]))')

# table
p.R('`${y}, January to ${MV.MONTHS[idxOf(y).length - 1]}`', '`${y}، ޖަނަވަރީއިން ${MV.MONTHS[idxOf(y).length - 1]} އާ ހަމައަށް`')
p.R('`Each tax collected by MIRA in ${spanTxt(ix[0], ix[ix.length - 1])}, and how much of it was paid in US dollars. Amounts are in the money of the time.`',
    '`MIRA އިން ހޯދި ކޮންމެ ޓެކްހަކާއި، އޭގެ ތެރެއިން ޑޮލަރުން ދެއްކި މިންވަރު (${spanTxt(ix[0], ix[ix.length - 1])}). އަދަދުތައް ދައްކަނީ އެ ވަގުތުގެ ފައިސާއިންނެވެ.`')
p.R('`<tr><th>Tax</th><th>Collected (${sym()})</th><th>Paid in US dollars (${sym()})</th><th>Share in dollars</th></tr>`',
    '`<tr><th>ޓެކްސް</th><th>ހޯދި (${sym()})</th><th>ޑޮލަރުން ދެއްކި (${sym()})</th><th>ޑޮލަރުގެ ބައި</th></tr>`')
p.R('`In ${y}, MIRA\'s collections were ${fmt(s, 0)}% of all government revenue and grants recorded by MMA (series 1999).`',
    '`${y} ގައި MIRA އިން ހޯދި ފައިސާއަކީ، MMA ގެ ރެކޯޑުތަކުގައިވާ ސަރުކާރުގެ ޖުމްލަ އާމްދަނީއާއި އެހީގެ ${fmt(s, 0)}% އެވެ (ސީރީޒް 1999).`')
p.R('`MIRA figures to ${mLabel(lastM.date)}${R.source_note ? `, file updated ${R.source_note.replace(/^Updated on\\s*/i, "").replace(/(\\d+)(st|nd|rd|th)\\b/, "$1")}` : ""}. Exchange rates and prices from MMA Statistics Database, last fetched ${MV.fetched(data.fetched_at)}, Malé time.`',
    '`MIRA ގެ އަދަދުތައް ${mLabel(lastM.date)} އާ ހަމައަށް${R.source_note ? `، ފައިލް އާކުރީ ${R.source_note.replace(/^Updated on\\s*/i, "").replace(/(\\d+)(st|nd|rd|th)\\b/, "$1").replace(/([A-Za-z]+)/, m => EN_MONTHS.includes(m) ? MV.MONTHS[EN_MONTHS.indexOf(m)] : m)}` : ""}. އެކްސްޗޭންޖް ރޭޓާއި އަގުތައް MMA ގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން. އެންމެ ފަހުން ޑޭޓާ ހޯދީ ${MV.fetched(data.fetched_at)} (މާލޭ ވަގުތު).`')
p.R('"Couldn\'t load the revenue data."', '"އާމްދަނީގެ ޑޭޓާ ލޯޑުނުކުރެވުނެވެ."')

# what's left: "Paid in US dollars" (button, chart key, select option, pop-up rows)
p.R_all('Paid in US dollars', 'ޑޮލަރުން ދެއްކި')

p.relink()
p.write()
