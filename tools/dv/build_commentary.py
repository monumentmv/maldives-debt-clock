"""Dhivehi commentary page (dv-commentary.html) from commentary.html. The posts are read from
assets/commentary.json, using their *_dv fields (title_dv, body_dv, sources[].name_dv) and falling
back to English where a post has none. See common.py."""
from common import Page

p = Page("commentary")
p.head("ކޮމެންޓަރީ · ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި", "ސަރުކާރުގެ މާލިއްޔަތުގައި ފަހުން ހިނގި ކަންތައްތަކަށް ގާތުން ބެލުމާއި، އޭގެ މާނައާ ބެހޭ ޚިޔާލު.")
p.header()

# right-to-left: the coloured blocks keep their colours, with the bar on the right
p.R('</style>\n</head>', '''  html[lang="dv"] .cm-b { border-left-width: 0 !important; border-right-width: 4px !important; border-right-style: solid !important; }
  html[lang="dv"] .cm-body ul { padding-left: 0; padding-right: 1.2rem; }
</style>
</head>''')

p.R('<h1>Commentary</h1>', '<h1>ކޮމެންޓަރީ</h1>')
p.R('<p class="cm-intro">A closer look at recent events in Maldives public finance, with views on what they mean.</p>',
    '<p class="cm-intro">ދިވެހިރާއްޖޭގެ ސަރުކާރުގެ މާލިއްޔަތުގައި ފަހުން ހިނގި ކަންތައްތަކަށް ގާތުން ބަލައި، އެ ކަންތައްތަކުގެ މާނައާ ބެހޭ ޚިޔާލު ފާޅުކުރުން.</p>')
p.R('<div id="posts"><p>Loading…</p></div>', '<div id="posts"><p>ލޯޑުވަނީ…</p></div>')
p.R('<span id="fetched">Figures from Maldives Monetary Authority Statistics Database.</span>', '<span id="fetched">އަދަދުތައް ނަގާފައިވަނީ މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން.</span>')

# ---- the page's own script ----
p.R('''  const when = d => { const x = new Date(d), o = { timeZone: "Indian/Maldives" };
    return `${x.toLocaleDateString("en-GB", { ...o, day: "numeric", month: "long", year: "numeric" })}, ${x.toLocaleTimeString("en-GB", { ...o, hour: "2-digit", minute: "2-digit", hour12: false })} Malé time`; };''',
    '''  const when = d => { const t = MV_DV.male(d); return `${t.d} ${t.m} ${t.y}، ${t.hh}:${t.mm} (މާލޭ ވަގުތު)`; };
  const dv = (p, k) => p[k + "_dv"] || p[k];''')
key = lambda bg, c, name: f'<i style="display:inline-block;width:.8rem;height:.8rem;border-radius:3px;margin:0 .6rem 0 .3rem;background:{bg};border-right:3px solid {c};vertical-align:-.05rem"></i>{name}'
p.R('${p.body.includes("cm-b ") ? `<span class="cm-key" style="color:#4d6a74;font-weight:600;font-size:.8rem"><i style="display:inline-block;width:.8rem;height:.8rem;border-radius:3px;margin:0 .3rem 0 .6rem;background:#fffdf7;border-left:3px solid #d8ccaa;vertical-align:-.05rem"></i>Facts<i style="display:inline-block;width:.8rem;height:.8rem;border-radius:3px;margin:0 .3rem 0 .6rem;background:#dcf0df;border-left:3px solid #3f9a5c;vertical-align:-.05rem"></i>Positive<i style="display:inline-block;width:.8rem;height:.8rem;border-radius:3px;margin:0 .3rem 0 .6rem;background:#f8dcd5;border-left:3px solid #cf634d;vertical-align:-.05rem"></i>Concerns</span>` : ""}',
    '${dv(p, "body").includes("cm-b ") ? `<span class="cm-key" style="color:#4d6a74;font-weight:600;font-size:.8rem">'
    + key("#fffdf7", "#d8ccaa", "ޙަޤީޤަތްތައް") + key("#dcf0df", "#3f9a5c", "ހެޔޮ ކަންތައްތައް") + key("#f8dcd5", "#cf634d", "ކަންބޮޑުވުންތައް") + '</span>` : ""}')
p.R('<h2 class="cm-title">${esc(p.title)}</h2>', '<h2 class="cm-title">${esc(dv(p, "title"))}</h2>')
p.R('<div class="cm-body">${p.body}</div>', '<div class="cm-body">${dv(p, "body")}</div>')
p.R('<p class="cm-src">Sources: ${p.sources.map(x => `<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.name)}</a>`).join(", ")}.</p>',
    '<p class="cm-src">މަޢުލޫމާތު ލިބުނު ތަންތަން: ${p.sources.map(x => `<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(dv(x, "name"))}</a>`).join("؛ ")}.</p>')
p.R('<button type="button" data-share="${esc(p.id)}">Copy a link to this</button>', '<button type="button" data-share="${esc(p.id)}">މި ލިޔުމުގެ ލިންކު ކޮޕީކުރައްވާ</button>')
p.R('"<p>No commentary yet.</p>"', '"<p>އަދި އެއްވެސް ކޮމެންޓަރީއެއް ނެތެވެ.</p>"')
p.R('"<p>Commentary couldn\'t be loaded. Please try again later.</p>"', '"<p>ކޮމެންޓަރީ ލޯޑެއް ނުވި. ފަހުން އަލުން މަސައްކަތް ކުރައްވާ.</p>"')
p.R('b.textContent = "Copied"; setTimeout(() => { b.textContent = "Copy a link to this"; }, 1800);', 'b.textContent = "ކޮޕީކުރެވިއްޖެ"; setTimeout(() => { b.textContent = "މި ލިޔުމުގެ ލިންކު ކޮޕީކުރައްވާ"; }, 1800);')

p.footer()
p.relink()
p.write()
