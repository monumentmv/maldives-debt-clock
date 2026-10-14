"""Dhivehi updates page (dv-updates.html) from updates.html. The summaries themselves come from
assets/updates.js, which writes Dhivehi sentences when assets/dv.js is loaded. See common.py."""
from common import Page

p = Page("updates")
p.head("އާ މަޢުލޫމާތު · ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި", "ސަރުކާރުގެ މާލިއްޔަތާ ބެހޭ ކޮންމެ އާ ރަސްމީ އަދަދެއް، ފަސޭހަ ބަހުން ކުރުކޮށް.")
p.header()

# right-to-left layout for this page
p.R('</style>\n</head>', '''  html[lang="dv"] .upd-viz { text-align: left; }
  html[lang="dv"] .upd-tag b { letter-spacing: 0; text-transform: none; font-size: .8rem; }
  @media (max-width: 640px) { html[lang="dv"] .upd-viz { text-align: right; } }
</style>
</head>''')

p.R('<h1>Updates</h1>', '<h1>އާ މަޢުލޫމާތު</h1>')
p.R('<p class="lede">New official figures come out every week. Each time they do, the change is summed up here in plain words, with a small chart of how it got there. Check back to see what moved, or go back to any week or month since 2004.</p>',
    '<p class="lede">ކޮންމެ ހަފްތާއަކު އާ ރަސްމީ އަދަދުތައް ނެރެއެވެ. އެ ނެރޭ ކޮންމެ ފަހަރަކު، އައި ބަދަލު މިތާގައި ފަސޭހަ ބަހުން ކުރުކޮށް ލިޔެ، އެ ބަދަލު އައި ގޮތް ކުޑަ ޗާޓަކުން ދައްކައެވެ. ބަދަލުވި ކަންތައްތައް ބެލުމަށް އަނބުރާ ވަޑައިގަންނަވާ. ނުވަތަ 2004 އިން ފެށިގެން ކޮންމެ ހަފްތާއަކަށް ނުވަތަ މަހަކަށް ވަޑައިގަންނަވާ.</p>')
p.R('aria-label="Show updates about"', 'aria-label="ދައްކާނީ ކޮން ބާވަތެއްގެ އާ މަޢުލޫމާތު"')
p.R('<label>Go to <select id="jump" aria-label="Go to a month"></select></label>', '<label>މަހަކަށް ދާން <select id="jump" aria-label="މަހަކަށް ދާން"></select></label>')
p.R('<button type="button" class="more-btn" id="more">Show earlier updates</button>', '<button type="button" class="more-btn" id="more">ކުރީގެ އާ މަޢުލޫމާތު ދައްކާ</button>')
p.R('<span id="fetched">Summaries are written automatically from the same official figures used across the site.</span>',
    '<span id="fetched">މި ޚުލާޞާތައް ލިޔެވެނީ، މުޅި ސައިޓުގައި ބޭނުންކުރާ ރަސްމީ އަދަދުތަކުން، އޮޓޮމެޓިކުންނެވެ.</span>')

# ---- the page's own script ----
p.R('aria-pressed="true">Everything</button>', 'aria-pressed="true">ހުރިހާ</button>')
p.R('`<option value="">The latest</option>`', '`<option value="">އެންމެ ފަހުގެ</option>`')
p.R('<small>${items.length} update${items.length === 1 ? "" : "s"}</small>', '<small>އާ މަޢުލޫމާތު ${items.length}</small>')
p.R('"<p>No updates of this kind yet.</p>"', '"<p>މި ބާވަތެއްގެ އާ މަޢުލޫމާތެއް އަދި ނެތެވެ.</p>"')
p.R('say: () => `There are new updates since you last looked. The newest is <b>${newest.title}</b>.`', 'say: () => `ފަހުން ބެއްލެވި ފަހަރަށްފަހު އާ މަޢުލޫމާތު އެބަހުއްޓެވެ. އެންމެ އާ އެއްޗަކީ <b>${newest.title}</b>.`')
p.R('"<p>Updates couldn\'t load. Please refresh the page.</p>"', '"<p>އާ މަޢުލޫމާތު ލޯޑެއް ނުވި. ޞަފްޙާ ރިފްރެޝް ކުރައްވާ.</p>"')

p.footer()
p.relink()
p.write()
