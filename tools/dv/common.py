"""
Shared pieces for building the Dhivehi pages (DRAFT, not linked from the site).
Each tools/dv/build_<page>.py reads an English page, swaps its words for Dhivehi and writes dv-<page>.html
(dv.html for the home page). Every swap must find its English text, so if an English page changes, the
build stops and says which sentence to update. Run all of them with: python3 tools/dv/build_all.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = {"clock": ("index.html", "dv.html", "ދަރަނީގެ ގަޑި"), "priorities": ("priorities.html", "dv-priorities.html", "އިންޓަރެސްޓް"),
         "budget": ("budget.html", "dv-budget.html", "ބަޖެޓް"), "revenue": ("revenue.html", "dv-revenue.html", "ޓެކްސް"),
         "fuel": ("fuel.html", "dv-fuel.html", "ތެޔޮ އެތެރެކުރުން"), "updates": ("updates.html", "dv-updates.html", "އާ މަޢުލޫމާތު"),
         "commentary": ("commentary.html", "dv-commentary.html", "ކޮމެންޓަރީ"), "method": ("methodology.html", "dv-methodology.html", "ހިސާބުކުރާ ގޮތް"),
         "about": ("about.html", "dv-about.html", "ސައިޓާ ބެހޭ")}


class Page:
    def __init__(self, key):
        self.key = key
        self.en, self.out, _ = PAGES[key]
        self.s = (ROOT / self.en).read_text()

    def R(self, old, new, count=1):
        """replace English with Dhivehi; stops the build if the English text isn't there"""
        if old not in self.s:
            raise SystemExit(f"{self.out}: English text not found, update tools/dv/build for:\n  {old[:160]}")
        self.s = self.s.replace(old, new, count)

    def R_all(self, old, new):
        """replace every copy"""
        self.R(old, new, -1)

    def head(self, title, description, extra_js=()):
        s = self.s
        s = s.replace('<html lang="en">', '<html lang="dv" dir="rtl">', 1)
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
        s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
        s = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + description, s)
        s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*', lambda m: m.group(1) + title, s)
        js = "".join(f'<script src="assets/{j}?v=dv1"></script>\n' for j in ("dv.js",) + tuple(extra_js))
        s = re.sub(r'<script src="assets/site\.js', js + '<script src="assets/site.js', s, count=1)
        self.s = s

    def header(self):
        nav = "\n".join(f'    <a href="{out}" data-page="{k}"{" aria-current=\"page\"" if k == self.key else ""}>{name}</a>' for k, (en, out, name) in PAGES.items())
        nav += f'\n    <a href="{self.en if self.en != "index.html" else "./"}" lang="en" dir="ltr" class="lang-sw">English</a>'
        new = f'''<header class="site-head">
  <a class="brand" href="dv.html">MV <span>ދަރަނީގެ ގަޑި</span></a>
  <nav class="site-nav" aria-label="މައި މެނޫ">
{nav}
  </nav>
  <div class="prefs">
    <div class="toggle" data-pref="cur" role="group" aria-label="ފައިސާ"><button type="button" data-v="MVR" aria-pressed="true">ރުފިޔާ</button><button type="button" data-v="USD" aria-pressed="false">ޑޮލަރު</button></div>
    <div class="toggle" data-pref="real" role="group" aria-label="އިންފްލޭޝަން" title="ރިއަލް ގޮތަށް ކުރީގެ އަދަދުތައް ދައްކަނީ މިއަދުގެ އަގުތަކުން"><button type="button" data-v="0" aria-pressed="true">ނޮމިނަލް</button><button type="button" data-v="1" aria-pressed="false">ރިއަލް</button></div>
  </div>
  <div class="real-note" role="status"></div>
</header>'''
        if not re.search(r'<header class="site-head">.*?</header>', self.s, flags=re.S):
            raise SystemExit(f"{self.out}: header not found")
        self.s = re.sub(r'<header class="site-head">.*?</header>', lambda m: new, self.s, count=1, flags=re.S)

    def footer(self):
        self.R('<span class="foot-links"><a href="methodology.html">Methodology</a> <a href="about.html">About and contact</a> <span>Independent, and not affiliated with any state institution.</span></span>',
               '<span class="foot-links"><a href="methodology.html">ހިސާބުކުރާ ގޮތް</a> <a href="about.html">ސައިޓާ ބެހޭ، އަދި ގުޅުއްވުމަށް</a> <span>މިއީ މިނިވަން ސައިޓެކެވެ. ދައުލަތުގެ އެއްވެސް މުއައްސަސާއަކާ ގުޅުމެއް ނެތެވެ.</span></span>')

    def relink(self):
        """links to other pages go to their Dhivehi versions (header and the English switch are left alone)"""
        head_end = self.s.index("</header>")
        body = self.s[head_end:]
        for k, (en, out, _) in PAGES.items():
            if en == "index.html":
                continue
            body = re.sub(rf'href=(["\']){re.escape(en)}', rf'href=\1{out}', body)
        body = re.sub(r'href=(["\'])\./(["\'#])', r'href=\1dv.html\2', body)
        self.s = self.s[:head_end] + body

    def leftovers(self):
        """English words still visible in the page's own markup (scripts and drawings left out)"""
        body = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<head>.*?</head>", "", self.s, flags=re.S)
        return sorted(set(m.strip() for m in re.findall(r">([^<>]*[A-Za-z]{3,}[^<>]*)<", body) if m.strip()) - {"English"})

    def write(self):
        (ROOT / self.out).write_text(self.s)
        left = self.leftovers()
        print(f"{self.out}: written" + (f", {len(left)} English bits left in markup: {left[:12]}" if left else ""))
