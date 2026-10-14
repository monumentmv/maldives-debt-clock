"""Dhivehi about page (dv-about.html) from about.html, with the contact form in Dhivehi.
The topics keep their English values, so messages reach the Google Form exactly as from the English page. See common.py."""
from common import Page

p = Page("about")
p.head("ސައިޓާ ބެހޭ، އަދި ގުޅުއްވުމަށް · ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި", "ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑި ހެދީ ކާކު، ކީއްވެ، އަދި ގުޅުއްވާނެ ގޮތް.")
p.header()

# right-to-left: the hidden spam trap goes off the right edge, the send button sits at the start (right)
p.R('</style>\n</head>', '''  html[lang="dv"] .hp { left: auto; right: -9999px; }
  html[lang="dv"] input[type="email"] { direction: ltr; text-align: right; }
</style>
</head>''')

p.R('<h1>About this site</h1>', '<h1>މި ސައިޓާ ބެހޭ</h1>')
p.R('<p>Maldives National Debt Clock shows how much the Maldivian government owes, what that means for each citizen, and how the government\'s income and spending compare. It is built entirely from official statistics, published by Maldives Monetary Authority, Ministry of Finance, Maldives Inland Revenue Authority and Maldives Police Service, and every figure is explained on the <a href="methodology.html">methodology page</a>.</p>',
    '<p>ދިވެހިރާއްޖޭގެ ޤައުމީ ދަރަނީގެ ގަޑިން ދައްކަނީ ދިވެހި ސަރުކާރުން ދައްކަންޖެހޭ ދަރަނީގެ މިންވަރާއި، އެއީ ކޮންމެ ރައްޔިތަކަށް ކިހާވަރެއްކަމާއި، ސަރުކާރުގެ އާމްދަނީއާއި ޚަރަދު އަޅާކިޔާ ގޮތެވެ. މި ސައިޓު ހަދާފައިވަނީ މުޅިން ރަސްމީ ތަފާސްހިސާބުތަކުންނެވެ. އެއީ މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީ، މާލިއްޔަތު ވުޒާރާ، މޯލްޑިވްސް އިންލެންޑް ރެވެނިއު އޮތޯރިޓީ އަދި ދިވެހި ފުލުހުންގެ ޚިދުމަތުން ޝާއިޢުކުރާ ތަފާސްހިސާބުތަކެވެ. ކޮންމެ އަދަދެއް <a href="methodology.html">ހިސާބުކުރާ ގޮތުގެ ޞަފްޙާ</a>ގައި ބަޔާންކޮށްފައިވެއެވެ.</p>')
p.R('<p>Public debt affects everyone. It shapes what the government can spend on schools, hospitals and islands, and what future generations will have to repay. The aim is to make those numbers easy to see and understand.</p>',
    '<p>ސަރުކާރުގެ ދަރަނީގެ އަސަރު ކޮންމެ މީހަކަށް ކުރެއެވެ. ސްކޫލުތަކާއި، ހޮސްޕިޓަލްތަކާއި، ރަށްތަކަށް ސަރުކާރަށް ހޭދަކުރެވޭނެ މިންވަރާއި، ކުރިއަށް އޮތް ޖީލުތަކަށް އަނބުރާ ދައްކަންޖެހޭނެ މިންވަރު ކަނޑައެޅެނީ ދަރަނީގެ ސަބަބުންނެވެ. މި ސައިޓުގެ މަޤްޞަދަކީ އެ އަދަދުތައް ފަސޭހައިން ފެނި، ވިސްނޭނެ ގޮތް ހެދުމެވެ.</p>')
p.R('<p>The site is independent, and not affiliated with any state institution.</p>', '<p>މިއީ މިނިވަން ސައިޓެކެވެ. ދައުލަތުގެ އެއްވެސް މުއައްސަސާއަކާ ގުޅުމެއް ނެތެވެ.</p>')
p.R('<h2>Why I made this</h2>', '<h2>މި ސައިޓު ހެދި ސަބަބު</h2>')
p.R('<p>The figures are public but scattered across different websites, so I made this to keep track of what the government borrows, earns and spends, all in one place.</p>',
    '<p>މި އަދަދުތައް ހާމަ ނަމަވެސް، އެކި ވެބްސައިޓުތަކުގައި ފުރަގަސްވެފައި ހުރެއެވެ. އެހެންކަމުން، ސަރުކާރުން ދަރަނި ނަގާ މިންވަރާއި، ލިބޭ ފައިސާއާއި، ހޭދަކުރާ ފައިސާ، އެއް ތަނަކުން ބަލަހައްޓަން މި ސައިޓު ހެދީމެވެ.</p>')
p.R('<p>Shaheed (<a href="https://x.com/AShaheed121"', '<p>ޝަހީދު (<a href="https://x.com/AShaheed121" dir="ltr"')

p.R('<h2>Get in touch</h2>', '<h2>ގުޅުއްވުމަށް</h2>')
p.R('<p>Spotted an error, have a question about the data, or want to use the figures? Send a message using the form below.</p>',
    '<p>ކުށެއް ފާހަގަކުރެއްވިންތޯ؟ ޑޭޓާއާ ބެހޭ ސުވާލެއް އެބައޮތްތޯ؟ ނުވަތަ މި އަދަދުތައް ބޭނުންކުރައްވަން ބޭނުންތޯ؟ ތިރީގައިވާ ފޯމުން މެސެޖެއް ފޮނުއްވާ.</p>')
p.R('<label>Your name<input', '<label>ނަން<input')
p.R('<label>Your email<input', '<label>އީމެއިލް<input')
p.R("<label>What's it about?", '<label>މެސެޖު ކޮން ކަމަކާ ބެހޭ؟')
p.R('<option>General question</option>', '<option value="General question">އާންމު ސުވާލެއް</option>')
p.R('<option>Possible error in the data</option>', '<option value="Possible error in the data">ޑޭޓާގައި ކުށެއް ހުރިހެން ހީވޭ</option>')
p.R('<option>Media or research enquiry</option>', '<option value="Media or research enquiry">މީޑިއާ ނުވަތަ ދިރާސާއާ ބެހޭ ސުވާލެއް</option>')
p.R('<option>Suggestion for the site</option>', '<option value="Suggestion for the site">ސައިޓަށް ހުށަހަޅާ ޚިޔާލެއް</option>')
p.R('<label>Message<textarea', '<label>މެސެޖު<textarea')
p.R('<button class="send" type="submit">Send message</button>', '<button class="send" type="submit">މެސެޖު ފޮނުއްވާ</button>')
p.R('<p class="small" style="margin:0">Your name and email are only used to reply to you.</p>', '<p class="small" style="margin:0">ތިޔަ ނަމާއި އީމެއިލް ބޭނުންކުރާނީ ހަމައެކަނި ޖަވާބު ދިނުމަށެވެ.</p>')
p.R('<span id="fetched">Figures from Maldives Monetary Authority Statistics Database.</span>', '<span id="fetched">އަދަދުތައް ނަގާފައިވަނީ މޯލްޑިވްސް މަނިޓަރީ އޮތޯރިޓީގެ ސްޓެޓިސްޓިކްސް ޑޭޓާބޭސްއިން.</span>')

# ---- the form's messages ----
p.R('"The contact form isn\'t switched on yet. Please check back soon."', '"ގުޅުއްވާ ފޯމު އަދި ހުޅުވިފައެއް ނުވެއެވެ. ކުރިއަށް އަނބުރާ ބައްލަވާ."')
p.R('"Add your name, a valid email address and a message, then send again."', '"ނަމާއި، ރަނގަޅު އީމެއިލް އެޑްރެހަކާއި، މެސެޖެއް ލިޔުއްވާފައި އަލުން ފޮނުއްވާ."')
p.R('btn.textContent = "Sending…";', 'btn.textContent = "ފޮނުވަނީ…";')
p.R('"Message sent. Thank you, you\'ll get a reply by email."', '"މެސެޖު ފޮނުވިއްޖެ. ޝުކުރިއްޔާ. ޖަވާބު އީމެއިލުން ލިބޭނެއެވެ."')
p.R('"The message didn\'t send. Check your connection and try again."', '"މެސެޖު ނުފޮނުވުނު. އިންޓަނެޓް ކަނެކްޝަން ޗެކްކޮށް އަލުން މަސައްކަތް ކުރައްވާ."')
p.R('btn.textContent = "Send message";', 'btn.textContent = "މެސެޖު ފޮނުއްވާ";')

p.footer()
p.relink()
p.write()
