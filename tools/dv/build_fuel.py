"""Dhivehi fuel imports page (dv-fuel.html) from fuel.html. See common.py and GLOSSARY.md."""
from common import Page

p = Page("fuel")
p.head("ތެޔޮ އެތެރެކުރުން · ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި",
       "ކޮންމެ މަހަކު ރާއްޖެއިން ތެޔޮ އެތެރެކުރުމަށް ހޭދަކުރާ ފައިސާ، އަދި ހަނގުރާމަތަކާއި ބުހުރާންތަކުން އެ ބިލަށް އަސަރުކުރި ގޮތް.")
p.header()
p.R('content="An island above a sea, with a dashed line deep below the surface, showing what the Maldivian government owes and the debt as a share of GDP."',
    'content="ކަނޑުގެ މައްޗަށް ފެންނަ ރަށެއް، އަދި ފެނުގެ ފުނޔަށް ދަމާފައިވާ ރޮނގެއް. ދިވެހި ސަރުކާރުގެ ދަރަނި އަދި ޖީޑީޕީއާ އަޅާކިޔާއިރު ދަރަނި."')

# ---- right-to-left fixes for this page's own styles ----
p.R('</style>\n</head>', '''  /* Dhivehi (right to left) */
  html[lang="dv"] .crisis { border-left: 0; border-right: 4px solid; border-radius: 6px 0 0 6px; }
  html[lang="dv"] .crisis h3 .num { margin-right: 0; margin-left: .4rem; }
  html[lang="dv"] .ctl-label { margin-right: 0; margin-left: -.5rem; }
  html[lang="dv"] .tip .row span:last-child { direction: ltr; unicode-bidi: isolate; }
</style>
</head>''')

# ---- intro ----
p.R('<h1>What Maldives spends on imported fuel</h1>', '<h1>ރާއްޖެއިން ތެޔޮ އެތެރެކުރުމަށް ހޭދަކުރާ ފައިސާ</h1>')
p.R("<p class=\"lede\">Maldives imports almost all of its energy as petroleum products. Diesel accounts for a large share of fuel use, generating most of the country's electricity and powering many road vehicles, boats and fishing vessels. Petrol is also widely used in cars, motorcycles and smaller boats, while aviation fuel, cooking gas and other petroleum products make up the remainder. When wars or other global crises push up oil prices, the country's fuel import bill rises with them, and the foreign currency spent on these imports flows out of the economy.</p>",
    '<p class="lede">ދިވެހިރާއްޖެއަށް ބޭނުންވާ ހަކަތައިގެ ގާތްގަނޑަކަށް ހުރިހާ ބައެއް އެތެރެކުރަނީ ތެލުގެ ބާވަތްތަކުގެ ގޮތުގައެވެ. ބޭނުންކުރާ ތެލުގެ ބޮޑު ބައެއް ޑީސަލެވެ. ޤައުމުގެ ކަރަންޓުގެ ގިނަ ބައެއް އުފައްދަނީ ޑީސަލުންނެވެ. އަދި ގިނަ ސަވާރީތަކާއި، ދޯނިތަކާއި، މަސްވެރި އުޅަނދުތައް ދުއްވަނީ ވެސް ޑީސަލުންނެވެ. ކާރާއި، މޮޓަރުސައިކަލާއި، ކުދި ދޯނިތަކުގައި ޕެޓްރޯލް ވެސް ގިނައިން ބޭނުންކުރެއެވެ. ބާކީ ބައިގައި މަތިންދާބޯޓުތަކުގެ ތެޔޮއާއި، ކައްކާ ގޭހާއި، ތެލުގެ އެހެން ބާވަތްތައް ހިމެނެއެވެ. ހަނގުރާމަތަކާއި ދުނިޔޭގެ އެހެން ބުހުރާންތަކުގެ ސަބަބުން ތެލުގެ އަގު މައްޗަށް ދާއިރު، ޤައުމުގެ ތެޔޮ އެތެރެކުރުމުގެ ބިލު ވެސް ބޮޑުވެއެވެ. އަދި އެ އެތެރެކުރުމަށް ހޭދަކުރާ ބޭރުގެ ފައިސާ، އިޤްތިޞާދުން ބޭރަށް ދެއެވެ.</p>')
p.R('id="sLatestL">latest month</div>', 'id="sLatestL">އެންމެ ފަހު މަސް</div>')
p.R('id="s12L">spent on fuel imports in the last 12 months</div>', 'id="s12L">ފާއިތުވި 12 މަހު ތެޔޮ އެތެރެކުރުމަށް ހޭދަވި</div>')
p.R('id="sShareL">of everything Maldives imports</div>', 'id="sShareL">ރާއްޖެއަށް އެތެރެކުރާ ހުރިހާ މުދަލުގެ ތެރެއިން</div>')

# ---- monthly chart ----
p.R('<h2>Every month since <span id="sinceYr">2004</span></h2>', '<h2><span id="sinceYr">2004</span> އިން ފެށިގެން ކޮންމެ މަހެއް</h2>')
p.R('aria-label="Period"><button type="button" data-range="all" aria-pressed="true">All</button><button type="button" data-range="2015" aria-pressed="false">Since 2015</button><button type="button" data-range="5" aria-pressed="false">5 years</button>',
    'aria-label="މުއްދަތު"><button type="button" data-range="all" aria-pressed="true">ހުރިހާ</button><button type="button" data-range="2015" aria-pressed="false">2015 އިން ފެށިގެން</button><button type="button" data-range="5" aria-pressed="false">5 އަހަރު</button>')
p.R('aria-label="Detail"><button type="button" data-split="0" aria-pressed="true">Total</button><button type="button" data-split="1" aria-pressed="false">By product</button>',
    'aria-label="ތަފްސީލު"><button type="button" data-split="0" aria-pressed="true">ޖުމްލަ</button><button type="button" data-split="1" aria-pressed="false">ބާވަތުން</button>')
p.R('<span class="dot"></span>World oil price</button>', '<span class="dot"></span>ދުނިޔޭގެ ތެލުގެ އަގު</button>')
p.R('aria-label="Crises shaded on the chart"', 'aria-label="ޗާޓުގައި ކުލަ ޖަހާފައިވާ ބުހުރާންތައް"')
p.R('<div class="hint">Hover or tap the chart to see each month. Numbers match the crises listed below.</div>',
    '<div class="hint">ކޮންމެ މަހެއް ބެއްލެވުމަށް ޗާޓުގެ މައްޗަށް މައުސް ގެންދަވާ، ނުވަތަ ފިއްތަވާ. ނަންބަރުތަކަކީ ތިރީގައިވާ ބުހުރާންތަކުގެ ނަންބަރުތަކެވެ.</div>')

# ---- crises ----
p.R('<h2>Crises that moved the bill</h2>', '<h2>ބިލަށް އަސަރުކުރި ބުހުރާންތައް</h2>')
p.R('<p>For each crisis, the average monthly fuel bill during the shaded period is compared with the average over the 12 months before it began, alongside the world crude oil price over the same months.</p>',
    '<p>ކޮންމެ ބުހުރާނެއްގައި، ކުލަ ޖަހާފައިވާ މުއްދަތުގައި ތެޔޮ އެތެރެކުރުމަށް މަހަކަށް ހޭދަވި އެވަރެޖް ފައިސާ، އެ ބުހުރާން ފެށުމުގެ ކުރީގެ 12 މަހުގެ އެވަރެޖާ އަޅާކިޔާފައިވެއެވެ. އަދި އެ މަސްތަކުގައި ދުނިޔޭގެ ތެލުގެ އަގު ވެސް ދައްކާފައިވެއެވެ.</p>')
p.R('<h2>Year by year</h2>', '<h2>އަހަރުން އަހަރަށް</h2>')

# ---- reading these figures ----
p.R('<h2>Reading these figures</h2>', '<h2>މި އަދަދުތައް ކިޔާނެ ގޮތް</h2>')
p.R("<p>Fuel import values come from Maldives Customs Service (MMA series 3503, with petrol 3504, diesel 3505 and other products 3507). The oil price is the World Bank's monthly average of Brent, Dubai and WTI crude (series 3787). Fuel is bought and recorded in US dollars, so the charts and crisis comparisons stay in dollars. That keeps the history undistorted. The rufiyaa was fixed at 12.80 per dollar until March 2011, then moved to about 15.40, so converting the history to rufiyaa would add a jump that has nothing to do with fuel. Only the headline figures at the top follow the MVR/US$ switch, converted at each month's MMA reference rate.</p>",
    '<p>ތެޔޮ އެތެރެކުރުމުގެ އަދަދުތައް ނަގާފައިވަނީ ދިވެހި ކަސްޓަމްސް އިންނެވެ (MMA ސީރީޒް 3503. ޕެޓްރޯލް 3504، ޑީސަލް 3505، އަދި އެހެން ބާވަތްތައް 3507). ތެލުގެ އަގަކީ ވޯލްޑް ބޭންކުން ހިސާބުކުރާ، Brent، Dubai އަދި WTI ކްރޫޑް އޮއިލްގެ މަހު އެވަރެޖެވެ (ސީރީޒް 3787). ތެޔޮ ގަނެ ރެކޯޑުކުރަނީ އެމެރިކާ ޑޮލަރުންނެވެ. އެހެންކަމުން، ޗާޓުތަކާއި ބުހުރާންތައް އަޅާކިޔާ ހިސާބުތައް ދައްކަނީ ޑޮލަރުންނެވެ. އެގޮތުން ތާރީޚު ބަދަލުނުވެ ހުރެއެވެ. 2011 ގެ މާރިޗާ ހަމައަށް ޑޮލަރަކަށް 12.80 ރުފިޔާގެ ރޭޓެއް ކަނޑައަޅާފައި އޮތެވެ. އޭގެފަހުން ރޭޓު ގާތްގަނޑަކަށް 15.40 އަށް ބަދަލުވިއެވެ. އެހެންކަމުން، ތާރީޚު ރުފިޔާއަށް ބަދަލުކުރިނަމަ، ތެލާ ގުޅުމެއް ނެތް ފުންމުމެއް ފެންނާނެއެވެ. ރުފިޔާ/ޑޮލަރު ސްވިޗާ އެއްގޮތަށް ބަދަލުވަނީ މަތީގައިވާ މައި އަދަދުތައް އެކަނިއެވެ. އެ އަދަދުތައް ބަދަލުކުރަނީ ކޮންމެ މަހެއްގެ MMA ގެ ރިފަރެންސް ރޭޓުންނެވެ.</p>')
p.R("<p><b>Break in April 2015.</b> After duty on petroleum products was reinstated from 1 April 2015, the series only includes fuel sold within Maldives. Earlier months also include fuel that was not sold locally, so values before and after the dotted line are not fully comparable.</p>",
    '<p><b>2015 ގެ އެޕްރީލްގައި އައި ބަދަލު.</b> 1 އެޕްރީލް 2015 އިން ފެށިގެން ތެލުގެ ބާވަތްތަކަށް ޑިއުޓީ އަލުން ނެގުމަށްފަހު، މި ސީރީޒްގައި ހިމެނެނީ ރާއްޖޭގެ ތެރޭގައި ވިއްކާ ތެޔޮ އެކަނިއެވެ. ކުރީގެ މަސްތަކުގައި ރާއްޖޭގައި ނުވިއްކާ ތެޔޮ ވެސް ހިމެނެއެވެ. އެހެންކަމުން، ތިކި ރޮނގުގެ ކުރީގެ އަދަދުތަކާއި ފަހުގެ އަދަދުތައް ފުރިހަމައަށް އަޅާނުކިޔެވޭނެއެވެ.</p>')
p.R("<p>The import bill reflects both prices and quantities. A higher bill can mean fuel cost more, or that the country bought more of it, for example when tourism grows. The inflation adjustment (\"Real\") isn't applied on this page because fuel is priced in US dollars, and Maldivian consumer prices aren't the right measure for that. <a href=\"methodology.html#fuel\">More in the methodology</a>.</p>",
    '<p>އެތެރެކުރުމުގެ ބިލުގައި އަގާއި މިންވަރު ދެކަންވެސް ހިމެނެއެވެ. ބިލު ބޮޑުވުމުގެ މާނައަކީ ތެލުގެ އަގު ބޮޑުވުން ކަމުގައި ވެދާނެއެވެ. ނުވަތަ، މިސާލަކަށް ފަތުރުވެރިކަން ބޮޑުވާއިރު، ޤައުމުން ގަންނަ ތެލުގެ މިންވަރު ގިނަވުން ކަމުގައި ވެދާނެއެވެ. ތެލުގެ އަގު ކަނޑައަޅަނީ އެމެރިކާ ޑޮލަރުން ކަމުން، މި ޞަފްޙާގައި އިންފްލޭޝަން ("ރިއަލް") ބޭނުން ނުކުރެއެވެ. ރާއްޖޭގެ ކޮންސިއުމަރ އަގުތަކަކީ އެކަމަށް ރަނގަޅު މިންގަނޑެއް ނޫނެވެ. <a href="methodology.html#fuel">މެތަޑޮލޮޖީގައި އިތުރަށް ކިޔުއްވާ</a>.</p>')

p.R('<span id="fetched">Figures from Maldives Monetary Authority Statistics Database.</span>',
    '<span id="fetched">އަދަދުތައް ނަގާފައިވަނީ މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން.</span>')
p.footer()

# ================= inline script =================
CR = [
    ('label: "Tsunami", kind: "shock", title: "Indian Ocean tsunami", when: "From 26 December 2004", text: "The tsunami struck islands across Maldives, followed by months of rebuilding."',
     'label: "ސުނާމީ", kind: "shock", title: "ހިންދު ކަނޑުގެ ސުނާމީ", when: "26 ޑިސެމްބަރު 2004 އިން ފެށިގެން", text: "ސުނާމީ ރާއްޖޭގެ ގިނަ ރަށްރަށަށް ކައްސާލިއެވެ. އޭގެ ފަހުން މަސްތަކެއްވަންދެން އަލުން ބިނާކުރުމުގެ މަސައްކަތް ކުރިއަށް ދިޔައެވެ."'),
    ('label: "2008 spike", kind: "shock", title: "Oil price spike and financial crash", when: "2008", text: "Oil climbed to record highs in mid-2008, then collapsed as the global financial crisis took hold."',
     'label: "2008 ގެ އަގު", kind: "shock", title: "ތެލުގެ އަގު އެރުމާއި މާލީ ބުހުރާން", when: "2008", text: "2008 ގެ މެދުތެރޭގައި ތެލުގެ އަގު ކުރިން ނުދާހާ މަތިވެގެން ދިޔައެވެ. ދެން ދުނިޔޭގެ މާލީ ބުހުރާން ފެށުމާއެކު އަގު ވަރަށް ބޮޑަށް ވެއްޓުނެވެ."'),
    ('label: "Libya", kind: "war", title: "Libyan civil war and the Arab Spring", when: "February to October 2011", text: "War in Libya and unrest across the Middle East cut supply and pushed oil above $100 a barrel."',
     'label: "ލީބިޔާ", kind: "war", title: "ލީބިޔާގެ ސިވިލް ހަނގުރާމައާއި އަރަބި ރަބީޢު", when: "ފެބުރުއަރީ އިން އޮކްޓޫބަރު 2011 އަށް", text: "ލީބިޔާގެ ހަނގުރާމައާއި މެދުއިރުމަތީގެ ހަލަބޮލިކަމާއެކު ތެލުގެ ސަޕްލައި މަދުވެ، ތެލުގެ އަގު ބެރަލަކަށް 100 ޑޮލަރަށްވުރެ މައްޗަށް ދިޔައެވެ."'),
    ('label: "Oil glut", kind: "shock", title: "Oil price collapse", when: "Mid-2014 to early 2016", text: "A global supply glut, driven by US shale oil and OPEC\'s decision to keep pumping, more than halved oil prices."',
     'label: "ތެޔޮ ގިނަވުން", kind: "shock", title: "ތެލުގެ އަގު ވެއްޓުން", when: "2014 ގެ މެދުން 2016 ގެ ފެށުމަށް", text: "އެމެރިކާގެ ޝޭލް އޮއިލް އާއި، ތެޔޮ އުފެއްދުން ކުޑަނުކުރުމަށް OPEC އިން ނިންމި ނިންމުމުގެ ސަބަބުން ދުނިޔޭގައި ތެޔޮ ގިނަވިއެވެ. އަދި ތެލުގެ އަގު ދެބައިކުޅަ އެއްބަޔަށްވުރެ ދަށަށް ވެއްޓުނެވެ."'),
    ('label: "COVID-19", kind: "shock", title: "COVID-19 border closure", when: "27 March to 15 July 2020", text: "Maldives closed its borders to tourists, resorts emptied, and world oil demand collapsed."',
     'label: "ކޮވިޑް-19", kind: "shock", title: "ކޮވިޑް-19 ގައި ބޯޑަރު ބަންދުކުރުން", when: "27 މާރިޗު އިން 15 ޖުލައި 2020 އަށް", text: "ދިވެހިރާއްޖޭގެ ބޯޑަރު ފަތުރުވެރިންނަށް ބަންދުކޮށް، ރިސޯޓުތައް ހުސްވިއެވެ. އަދި ދުނިޔޭގައި ތެޔޮ ބޭނުންވާ މިންވަރު ވަރަށް ބޮޑަށް ދަށްވިއެވެ."'),
    ('label: "Russia-Ukraine", kind: "war", title: "Russia-Ukraine war", when: "From 24 February 2022", text: "The outbreak of full-scale war in February 2022 sent oil, shipping and insurance costs soaring."',
     'label: "ރަޝިޔާ-ޔުކްރެއިން", kind: "war", title: "ރަޝިޔާ-ޔުކްރެއިން ހަނގުރާމަ", when: "24 ފެބުރުއަރީ 2022 އިން ފެށިގެން", text: "2022 ގެ ފެބުރުއަރީގައި ފުރިހަމަ ހަނގުރާމައެއް ފެށުމާއެކު، ތެލާއި، މުދާ ފޮނުވުމާއި، އިންޝުއަރަންސްގެ އަގުތައް ވަރަށް ބޮޑަށް މައްޗަށް ދިޔައެވެ."'),
    ('label: "Twelve-Day War", kind: "war", title: "Twelve-Day War (Israel and Iran)", when: "13 to 24 June 2025", text: "Israel and Iran exchanged strikes for twelve days, and the US bombed Iranian nuclear sites near the end, briefly lifting oil prices."',
     'label: "ބާރަ ދުވަހުގެ ހަނގުރާމަ", kind: "war", title: "ބާރަ ދުވަހުގެ ހަނގުރާމަ (އިސްރާއީލާއި އީރާން)", when: "13 އިން 24 ޖޫން 2025 އަށް", text: "ބާރަ ދުވަހުވަންދެން އިސްރާއީލާއި އީރާން ދެމެދު ހަމަލާތައް ދެވުނެވެ. ނިމުމާ ކައިރިކޮށް އެމެރިކާއިން އީރާނުގެ ނިއުކްލިއާ ތަންތަނަށް ބޮމު އެޅިއެވެ. މީގެ ސަބަބުން ކުރު މުއްދަތަކަށް ތެލުގެ އަގު މައްޗަށް ދިޔައެވެ."'),
    ('label: "2026 Iran war", kind: "war", title: "2026 Iran war and Strait of Hormuz closure", when: "From 28 February 2026", text: "The United States and Israel went to war with Iran, and the Strait of Hormuz was closed. The International Energy Agency called it the largest oil supply disruption in history."',
     'label: "2026 ގެ އީރާން ހަނގުރާމަ", kind: "war", title: "2026 ގެ އީރާން ހަނގުރާމައާއި ހޯރމުޒް ކަނޑުއޮޅި ބަންދުކުރުން", when: "28 ފެބުރުއަރީ 2026 އިން ފެށިގެން", text: "އެމެރިކާއާއި އިސްރާއީލް، އީރާނާ ހަނގުރާމަ ފެށިއެވެ. އަދި ހޯރމުޒް ކަނޑުއޮޅި ބަންދުކުރެވުނެވެ. އިންޓަރނޭޝަނަލް އެނަރޖީ އޭޖެންސީން ބުނީ، މިއީ ތާރީޚުގައި ތެލުގެ ސަޕްލައިއަށް އެރި އެންމެ ބޮޑު ހުރަސް ކަމަށެވެ."'),
]
for a, b in CR:
    p.R(a, b)

p.R('"Fuel figures aren\'t available right now. Please check back soon."', '"ތެޔޮ އެތެރެކުރުމުގެ އަދަދުތައް މިވަގުތު ނުލިބެއެވެ. ކުޑަ ވަގުތުކޮޅަކަށްފަހު އަނބުރާ ވަޑައިގަންނަވާ."')
p.R('const usd = v => "US$ " + short(v);', 'const usd = v => "$ " + short(v);')
p.R('`spent on fuel imports in ${mLabel(L.date)}${sel === all.length - 1 ? ", the latest month published" : ""}`',
    '`${mLabel(L.date)}${sel === all.length - 1 ? " (ޝާއިޢުކުރި އެންމެ ފަހު މަސް)" : ""} ގައި ތެޔޮ އެތެރެކުރުމަށް ހޭދަވި`')
p.R('${pc(L.v, P.v) >= 0 ? "+" : ""}${fmt(pc(L.v, P.v), 0)}% on ${mShort(P.date)}</span>', '${mShort(P.date)} އާ އަޅާކިޔާއިރު ${pc(L.v, P.v) >= 0 ? "+" : ""}${fmt(pc(L.v, P.v), 0)}%</span>')
p.R('${pc(L.v, Y.v) >= 0 ? "+" : ""}${fmt(pc(L.v, Y.v), 0)}% on ${mShort(Y.date)}</span>', '${mShort(Y.date)} އާ އަޅާކިޔާއިރު ${pc(L.v, Y.v) >= 0 ? "+" : ""}${fmt(pc(L.v, Y.v), 0)}%</span>')
p.R('`spent on fuel imports in the 12 months to ${mLabel(L.date)}`', '`${mLabel(L.date)} އާ ހަމައަށް 12 މަހު ތެޔޮ އެތެރެކުރުމަށް ހޭދަވި`')
p.R('`of all goods imported over the same 12 months was fuel`', '`އެ 12 މަހު އެތެރެކުރި ހުރިހާ މުދަލުގެ ތެރެއިން ތެލުގެ ބައި`')
p.R('[`12 months to ${mShort(L.date)}`, s12', '[`${mShort(L.date)} އާ ހަމައަށް 12 މަސް`, s12')
p.R('[`12 months before`, sp', '[`ކުރީގެ 12 މަސް`, sp')
p.R('"Each square is 1% of goods imported"', '"ކޮންމެ ހަތަރެސްކަނަކީ އެތެރެކުރި މުދަލުގެ 1%"')
p.R('"Value of Maldives\' petroleum imports each month, in millions of US dollars, the currency fuel is bought in." + (showCrude ? " The dashed line is the world crude oil price, in US dollars a barrel (right axis)." : "")',
    '"ކޮންމެ މަހަކު ރާއްޖެއަށް ތެލުގެ ބާވަތްތައް އެތެރެކުރި އަގު، މިލިއަން އެމެރިކާ ޑޮލަރުން. ތެޔޮ ގަންނަނީ ޑޮލަރުންނެވެ." + (showCrude ? " ކަށިކަށި ރޮނގަކީ ދުނިޔޭގެ ތެލުގެ އަގު، ބެރަލަކަށް ޑޮލަރުން (ކަނާތް ފަރާތުގައިވާ މިންގަނޑު)." : "")')
p.R('label: "Monthly fuel imports"', 'label: "ކޮންމެ މަހަކު ތެޔޮ އެތެރެކުރުން"')
p.R('yTitle: "US$ m", yTitleR: showCrude ? "US$/barrel" : null', 'yTitle: "$ މިލިއަން", yTitleR: showCrude ? "$ ބެރަލަކަށް" : null')
p.R('label: "Coverage change"', 'label: "ހިމަނާ ބައި ބަދަލުވި"')
p.R('label: `Highest ${unit} ${fmt(val(hi), 0)}m, ${mShort(hi.date)}`', 'label: `އެންމެ ބޮޑު: ${mShort(hi.date)}، $${fmt(val(hi), 0)} މިލިއަން`')
p.R('label: `Lowest ${unit} ${fmt(val(lo), 0)}m, ${mShort(lo.date)}`', 'label: `އެންމެ ކުޑަ: ${mShort(lo.date)}، $${fmt(val(lo), 0)} މިލިއަން`')
p.R_all('row("Maldives fuel imports"', 'row("ރާއްޖެއަށް ތެޔޮ އެތެރެކުރުން"')
p.R('row("Diesel"', 'row("ޑީސަލް"')
p.R('row("Petrol"', 'row("ޕެޓްރޯލް"')
p.R('row("Other"', 'row("އެހެނިހެން"')
p.R_all('row("Share of all imports"', 'row("ހުރިހާ އެތެރެކުރުމުގެ ބައި"')
p.R('row("World crude oil", r.crude ? "US$ " + fmt(r.crude, 1) + " a barrel" : null)', 'row("ދުނިޔޭގެ ތެލުގެ އަގު", r.crude ? "ބެރަލަކަށް $" + fmt(r.crude, 1) : null)')
p.R('>Highest month in view</span>', '>ފެންނަ މުއްދަތުގެ އެންމެ ބޮޑު މަސް</span>')
p.R('>Lowest month in view</span>', '>ފެންނަ މުއްދަތުގެ އެންމެ ކުޑަ މަސް</span>')
p.R('`<span>Highest month <b class="hi">US$ ${fmt(hi.v / 1e6, 0)}m, ${mLabel(hi.date)}</b></span><span>Lowest month <b class="lo">US$ ${fmt(lo.v / 1e6, 1)}m, ${mLabel(lo.date)}</b></span>`',
    '`<span>އެންމެ ބޮޑު މަސް <b class="hi">${mLabel(hi.date)}، ${fmt(hi.v / 1e6, 0)} މިލިއަން ޑޮލަރު</b></span><span>އެންމެ ކުޑަ މަސް <b class="lo">${mLabel(lo.date)}، ${fmt(lo.v / 1e6, 1)} މިލިއަން ޑޮލަރު</b></span>`')
p.R('${c.from.slice(0, 7) === c.to.slice(0, 7) ? "" : " to " + short2(c.to)}', '${c.from.slice(0, 7) === c.to.slice(0, 7) ? "" : " އިން " + short2(c.to) + " އަށް"}')
p.R('</i>Maldives diesel imports</span>', '</i>ޑީސަލް އެތެރެކުރުން</span>')
p.R('</i>Maldives petrol imports</span>', '</i>ޕެޓްރޯލް އެތެރެކުރުން</span>')
p.R('</i>Other products</span>', '</i>އެހެން ބާވަތްތައް</span>')
p.R('</i>Maldives fuel imports</span>', '</i>ތެޔޮ އެތެރެކުރުން</span>')
p.R('</i>World crude oil price</span>', '</i>ދުނިޔޭގެ ތެލުގެ އަގު</span>')
p.R('</i>War or conflict</span>', '</i>ހަނގުރާމަ ނުވަތަ ތަޅާފޮޅުން</span>')
p.R('</i>Other crisis</span>', '</i>އެހެން ބުހުރާން</span>')
p.R('`Maldives fuel imports averaged <b>${usd(a)}</b> a month, <b class="${ch >= 0 ? "up" : "down"}">${ch >= 0 ? "+" : "−"}${fmt(Math.abs(ch), 0)}%</b> on the year before. The peak was ${usd(pk.v)} in ${mShort(pk.date)}.`',
    '`މި މުއްދަތުގައި ތެޔޮ އެތެރެކުރުމަށް މަހަކަށް އެވަރެޖްކޮށް <b>${usd(a)}</b> ހޭދަވިއެވެ. އެއީ ކުރީގެ އަހަރާ އަޅާކިޔާއިރު <b class="${ch >= 0 ? "up" : "down"}">${ch >= 0 ? "+" : "−"}${fmt(Math.abs(ch), 0)}%</b> އެވެ. އެންމެ ބޮޑު މަހަކީ ${mShort(pk.date)} އެވެ (${usd(pk.v)}).`')
p.R('` World crude oil averaged US$ ${fmt(ca, 0)} a barrel, <b class="${cc >= 0 ? "up" : "down"}">${cc >= 0 ? "+" : "−"}${fmt(Math.abs(cc), 0)}%</b>.`',
    '` ދުނިޔޭގެ ތެލުގެ އަގަކީ ބެރަލަކަށް އެވަރެޖްކޮށް $${fmt(ca, 0)} އެވެ (<b class="${cc >= 0 ? "up" : "down"}">${cc >= 0 ? "+" : "−"}${fmt(Math.abs(cc), 0)}%</b>).`')
p.R('` <i>(Data so far, to ${mShort(during[during.length - 1].date)}.)</i>`', '` <i>(${mShort(during[during.length - 1].date)} އާ ހަމައަށް ލިބިފައިވާ ޑޭޓާ.)</i>`')
p.R('` <i>Part of this change reflects the April 2015 change in what the fuel series covers, not just prices.</i>`',
    '` <i>މި ބަދަލުގެ ބައެއް ވަނީ، އަގުތަކުގެ އިތުރުން، 2015 ގެ އެޕްރީލްގައި ތެލުގެ އަދަދުތަކުގައި ހިމަނާ ބައި ބަދަލުވުމުގެ ސަބަބުންނެވެ.</i>`')
p.R('"Not yet in the published data."', '"ޝާއިޢުކޮށްފައިވާ ޑޭޓާގައި އަދި ނުހިމެނެއެވެ."')
p.R('"Not enough earlier data to compare."', '"އަޅާކިޔުމަށް ފުދޭވަރަށް ކުރީގެ ޑޭޓާ ނެތެވެ."')
p.R('"Maldives\' total fuel imports each full calendar year, in millions of US dollars. The highest year is in red."',
    '"ކޮންމެ ފުރިހަމަ އަހަރަކު ރާއްޖެއަށް ތެޔޮ އެތެރެކުރި ޖުމްލަ އަދަދު، މިލިއަން އެމެރިކާ ޑޮލަރުން. އެންމެ ބޮޑު އަހަރު ދައްކާފައިވަނީ ރަތް ކުލައިންނެވެ."')
p.R('`In the last 12 months (${mLabel(l12[0].date)} to ${mLabel(L.date)}) Maldives spent <b>${usd(v12)}</b> on fuel imports` + (l12.every(r => r.imp) ? `, ${fmt(100 * v12 / l12.reduce((a, r) => a + r.imp, 0), 1)}% of all goods imported` : "") + (MV.state.cur === "MVR" ? `, about MVR ${short(l12.reduce((a, r) => a + fromUSD(r.v, r.date), 0))}` : "") + "."',
    '`ފާއިތުވި 12 މަހު (${mLabel(l12[0].date)} އިން ${mLabel(L.date)} އަށް) ރާއްޖެއިން ތެޔޮ އެތެރެކުރުމަށް <b>${usd(v12)}</b> ހޭދަކުރިއެވެ` + (l12.every(r => r.imp) ? `. އެއީ އެތެރެކުރި ހުރިހާ މުދަލުގެ ${fmt(100 * v12 / l12.reduce((a, r) => a + r.imp, 0), 1)}% އެވެ` : "") + (MV.state.cur === "MVR" ? `. ރުފިޔާއިން ގާތްގަނޑަކަށް ${short(l12.reduce((a, r) => a + fromUSD(r.v, r.date), 0))} ރުފިޔާއެވެ` : "") + "."')
p.R('label: "Fuel imports by year"', 'label: "އަހަރުން ތެޔޮ އެތެރެކުރުން"')
p.R('"Data last fetched " + MV.fetched(data.fetched_at) + ", Malé time. Figures from Maldives Customs Service and the World Bank, via MMA Statistics Database."',
    '"އެންމެ ފަހުން ޑޭޓާ ހޯދީ " + MV.fetched(data.fetched_at) + " (މާލޭ ވަގުތު). އަދަދުތައް ނަގާފައިވަނީ ދިވެހި ކަސްޓަމްސް އާއި ވޯލްޑް ބޭންކުން، MMA ގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސް މެދުވެރިކޮށެވެ."')
p.R('(k === 0 ? ", latest" : "")', '(k === 0 ? "، އެންމެ ފަހު" : "")')
p.R('what: "Monthly fuel import figures"', 'what: "ކޮންމެ މަހަކު ތެޔޮ އެތެރެކުރާ އަދަދުތައް"')
p.R('`Fuel import figures for <b>${mLabel(LA.date)}</b> are out. The last month you saw was ${mLabel(p + "-15")}.`',
    '`<b>${mLabel(LA.date)}</b> ގެ ތެޔޮ އެތެރެކުރުމުގެ އަދަދުތައް ނެރެފިއެވެ. ފަހުން ބެއްލެވި މަހަކީ ${mLabel(p + "-15")} އެވެ.`')
p.R('"Couldn\'t load the data."', '"ޑޭޓާ ލޯޑުނުކުރެވުނެވެ."')

p.relink()
p.write()
