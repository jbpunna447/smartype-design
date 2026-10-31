"""Builds the static site in site/ from the sources in src/ and assets/.

Usage, from the repository root: python3 tools/build_site.py
Needs the `markdown` package (pip install markdown).
"""
import html
import json
import os
import re
import shutil
import sys
import zipfile

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "src/pages")
EARLIER = os.path.join(ROOT, "src/earlier")
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "site")

ART = {
    "35LbtmyEzT7Fo2dtRtjKr3": "fix-1.html",
    "FxYnWeVkWAqp9jiFsF7eX9": "fix-1b.html",
    "S9q9FYBfXkpjXAcdkVzZ8x": "fix-2.html",
    "D3bcP4UMorE7H4W5rwbLyG": "fix-4.html",
    "75JNwaBPJxeKmsfuEyZroy": "fix-5.html",
    "GT2ALjSxSacdjsXVZKyNcp": "design-system/index.html",
    "KuPQvh8SvC84k8hfWpwSWv": "brand.html",
    "T4oCuTJSNaGKPxsLmRAWTV": "art.html",
    "4q7weqFHQKBAJesyBaZHXz": "review.html",
    "1uKRxMiqhVnyA2AeXy6hkx": "specs.html",
    "JWLJCTirqnZnqtBPyespDQ": "index.html",
    "2RqjhWzGiQBbEwiVxLbA7a": "audit.html",
}

NAV = [
    ("index.html", "Hand-off"),
    ("audit.html", "Audit"),
    ("fix-1b.html", "1b Smartbar"),
    ("fix-1.html", "1 AI panel"),
    ("fix-2.html", "2 Languages"),
    ("fix-4.html", "4 Errors"),
    ("fix-5.html", "5 Setup"),
    ("design-system/index.html", "Design system"),
    ("review.html", "Review"),
    ("specs.html", "Specs"),
    ("brand.html", "Brand"),
    ("art.html", "Art"),
]

NAV_CSS = """<style>
.stx-nav{position:sticky;top:0;z-index:1000;display:flex;gap:2px;align-items:center;overflow-x:auto;
  background:#0b1416;border-bottom:1px solid #22363a;padding:0 max(12px,env(safe-area-inset-left,0px));
  font:500 13px/1 "Google Sans Flex","DM Sans",system-ui,sans-serif;scrollbar-width:none}
.stx-nav::-webkit-scrollbar{display:none}
.stx-nav a{color:#b5cacf;text-decoration:none;padding:13px 10px;white-space:nowrap;border-bottom:2px solid transparent}
.stx-nav a:hover,.stx-nav a:focus-visible{color:#fff}
.stx-nav a[aria-current=page]{color:#5fd3df;border-bottom-color:#5fd3df}
.stx-nav .stx-brand{color:#fff;font-weight:700;padding-right:14px}
.stx-note{max-width:1040px;margin:18px auto 0;padding:12px 16px;border-radius:12px;background:#fbf0d9;color:#4d3800;
  font:14px/1.5 "Google Sans Flex","DM Sans",system-ui,sans-serif;box-sizing:border-box}
.stx-note a{color:#4d3800;font-weight:700}
.stx-notewrap{padding:0 16px}
@media (prefers-color-scheme:dark){.stx-note{background:#352a10;color:#f6dfa6}.stx-note a{color:#f6dfa6}}
</style>"""


def nav(current, depth):
    up = "../" * depth
    links = [f'<a class="stx-brand" href="{up}index.html">SmarType UX</a>']
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{up}{href}"{cur}>{label}</a>')
    return NAV_CSS + '<nav class="stx-nav" aria-label="Site">' + "".join(links) + "</nav>"


def note(text):
    return f'<div class="stx-notewrap"><div class="stx-note">{text}</div></div>'


def relink(s, depth):
    up = "../" * depth

    def sub(m):
        target = ART.get(m.group(1))
        return up + target if target else m.group(0)

    return re.sub(r"https://claude\.ai/artifact/([A-Za-z0-9]+)", sub, s)


HEAD_RE = re.compile(r"^\s*(?:<title>.*?</title>|<meta[^>]*>|<link[^>]*>|<style>.*?</style>|\s)+", re.S)


def wrap_fragment(src, current, depth=0, banner=""):
    m = HEAD_RE.match(src)
    head, body = (m.group(0), src[m.end():]) if m else ("", src)
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        + head + "</head><body>" + nav(current, depth) + banner + relink(body, depth) + "</body></html>\n"
    )


def inject_full(src, current, depth=0, banner=""):
    i = src.index("<body>") + len("<body>")
    return relink(src[:i] + nav(current, depth) + banner + src[i:], depth)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


def read(path):
    with open(path) as f:
        return f.read()


if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

# Pages written in this project (fragments)
for src, dst in [
    ("handoff.html", "index.html"),
    ("audit.html", "audit.html"),
    ("fix1-ai-panel.html", "fix-1.html"),
    ("fix1b-smartbar.html", "fix-1b.html"),
    ("fix2-languages.html", "fix-2.html"),
    ("fix4-errors.html", "fix-4.html"),
    ("fix5-setup.html", "fix-5.html"),
]:
    write(dst, wrap_fragment(read(os.path.join(PAGES, src)), dst))

# Earlier pages (full HTML), each with a note on what's superseded
write("review.html", inject_full(read(os.path.join(EARLIER, "review.html")), "review.html",
      banner=note('Source review from 25 Oct (build 138). The fixes are in the fix pages; <a href="audit.html">the audit</a> lists which findings are covered.')))
write("specs.html", inject_full(read(os.path.join(EARLIER, "specs.html")), "specs.html",
      banner=note('Partly superseded by <a href="fix-1b.html">Fix 1b</a>: the feature is called <b>Notes</b>, voice records in the smartbar and inserts with ✓, and Back is ‹ (no ABC key). Still valid here: the voice engine, pause handling, spoken commands, permission, privacy, and the Notes data and migration rules. The free AI allowance is a one-time trial, not daily.')))
write("brand.html", inject_full(read(os.path.join(EARLIER, "brand.html")), "brand.html",
      banner=note('The icon, logo and usage rules here stand. The "App interface" colour proposal (blue accent, blue AI gradient) was <b>not adopted</b>: the app keeps its teal. Use the <a href="design-system/index.html">design system</a> colours. Downloads are on the <a href="index.html#downloads">hand-off page</a>.')))
write("art.html", inject_full(read(os.path.join(EARLIER, "art.html")), "art.html",
      banner=note("The clay art placed in today's layouts and wording. The onboarding and sign-in screens are replaced by <a href=\"fix-5.html\">Fix 5</a>; build those from there.")))

# Design system
DS = os.path.join(ROOT, "src/design-system")
tokens = json.load(open(os.path.join(DS, "tokens.json")))


def tokens_css():
    themes = {"dark": {}, "light": {}, "amoled": {}}
    for t in tokens["color"]["tokens"]:
        v = t["value"]
        for th in themes:
            themes[th][t["name"]] = v if isinstance(v, str) else v.get(th) or v.get("dark")
    for group in ("spacing", "radius", "opacity"):
        for t in tokens[group]["tokens"]:
            val = t["value"]
            for th in themes:
                themes[th][t["name"]] = val if isinstance(val, str) else val.get(th) or val.get("dark")
    for t in tokens["shadow"]["tokens"]:
        v = t["value"]
        for th in themes:
            themes[th][t["name"]] = v if isinstance(v, str) else v.get(th) or v.get("dark")
    def block(d):
        return "".join(f"--{k}:{v};" for k, v in d.items())
    fam = tokens["type"]["families"]["sans"]
    return (
        f":root{{--font-sans:{fam};{block(themes['dark'])}color-scheme:dark}}\n"
        f"@media (prefers-color-scheme:light){{:root:not([data-theme]){{{block(themes['light'])}color-scheme:light}}}}\n"
        f":root[data-theme=light]{{{block(themes['light'])}color-scheme:light}}\n"
        f":root[data-theme=amoled]{{{block(themes['amoled'])}}}\n"
    )


write("design-system/tokens.css", tokens_css())
shutil.copy(os.path.join(DS, "components/bundle.css"), os.path.join(OUT, "design-system/bundle.css"))

DS_CSS = """<style>
body{margin:0;background:var(--background);color:var(--on-surface);font:15px/1.6 var(--font-sans)}
.wrap{max-width:980px;margin:0 auto;padding:28px 16px 70px}
.wrap h1{font-size:34px;line-height:1.15;margin:8px 0 12px}.wrap h2{font-size:22px;margin:34px 0 8px}.wrap h3{font-size:17px}
.wrap table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}
.wrap th,.wrap td{border-bottom:1px solid var(--outline-variant);padding:8px 10px;text-align:left;vertical-align:top}
.wrap code{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:.85em;background:var(--surface-container);padding:1px 5px;border-radius:4px}
.wrap a{color:var(--primary)}
.eyebrow{font:500 12px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--primary)}
.toc{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:18px 0}
.toc a{display:block;background:var(--surface-container-low);border-radius:14px;padding:12px 14px;text-decoration:none;color:var(--on-surface)}
.toc a b{display:block}.toc a span{color:var(--on-surface-variant);font-size:13px}
.pv{border:1px solid var(--outline-variant);border-radius:16px;padding:16px;margin:16px 0;background:var(--surface-container-low);overflow-x:auto}
.swatch{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px}
.swatch div{border:1px solid var(--outline-variant);border-radius:10px;overflow:hidden;font-size:12.5px}
.swatch i{display:block;height:44px}.swatch p{margin:0;padding:6px 8px}
.themes{display:flex;gap:6px;margin:10px 0}.themes button{font:inherit;border:1px solid var(--outline);background:transparent;color:var(--on-surface);border-radius:8px;padding:4px 10px;cursor:pointer}
</style>"""

THEME_JS = """<div class="themes" role="group" aria-label="Theme"><button data-t="dark">Dark</button><button data-t="light">Light</button><button data-t="amoled">AMOLED</button></div>
<script>document.querySelectorAll('.themes button').forEach(b=>b.onclick=()=>document.documentElement.dataset.theme=b.dataset.t)</script>"""


def ds_page(dst, title, inner, depth=1):
    head = (f'<title>{html.escape(title)}</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">'
            '<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="bundle.css">' + DS_CSS)
    page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            + head + "</head><body>" + nav("design-system/index.html", depth) + '<div class="wrap">' + inner + "</div></body></html>\n")
    write(dst, relink(page, depth))


def md(path):
    return markdown.markdown(read(path), extensions=["tables"])


ADDENDUM = note('<b>Updated after Fix 1b.</b> The panel header is now ‹ and the panel name (no keyboard-icon toggle, no ABC key), the smartbar stays visible above the panel, and the dock holds content actions only. The preview below still shows the earlier frame. Full list: <a href="../audit.html">audit, section 4</a>.')

COMPONENTS = ["Button", "Card", "Chip", "ListRow", "Sheet", "EmptyState", "KeyboardPanel"]
toc = "".join(f'<a href="{c.lower()}.html"><b>{c}</b><span>Component</span></a>' for c in COMPONENTS)
toc += '<a href="tokens.html"><b>Tokens</b><span>Colour, type, spacing, radius</span></a>'
toc += '<a href="audit-buttons.html"><b>Button audit</b><span>Today\'s code</span></a><a href="audit-components.html"><b>Component audit</b><span>Today\'s code</span></a><a href="illustrations.html"><b>Illustrations</b><span>Prompts and export sizes</span></a>'
ds_page("design-system/index.html", "SmarType Design System",
        '<div class="eyebrow">Design system</div><h1>SmarType design system</h1>' + THEME_JS + f'<div class="toc">{toc}</div>' + md(os.path.join(DS, "README.md")))
for c in COMPONENTS:
    pv = read(os.path.join(DS, f"components/{c}/preview.html"))
    banner = ADDENDUM.replace("../audit.html", "../audit.html") if c == "KeyboardPanel" else ""
    ds_page(f"design-system/{c.lower()}.html", f"{c} · SmarType", '<div class="eyebrow">Component</div>' + banner + THEME_JS
            + f'<div class="pv">{pv}</div>' + md(os.path.join(DS, f"components/{c}/README.md")))
for name in ["audit-buttons", "audit-components", "illustrations"]:
    ds_page(f"design-system/{name}.html", f"{name.replace('-', ' ').title()} · SmarType", md(os.path.join(DS, f"{name}.md")))

sw = ""
for t in tokens["color"]["tokens"]:
    sw += f'<div><i style="background:var(--{t["name"]})"></i><p><b>{t["name"]}</b><br>{html.escape(t.get("usage", ""))}</p></div>'
type_rows = "".join(
    f'<tr><td><code>{s["name"]}</code></td><td>{s["fontSize"]} / {s["lineHeight"]}</td><td>{s["fontWeight"]}</td><td>{html.escape(s.get("usage", ""))}</td></tr>'
    for g in tokens["type"]["groups"] for s in g["styles"])
other = ""
for group in ("spacing", "radius", "shadow", "opacity"):
    for t in tokens[group]["tokens"]:
        v = t["value"] if isinstance(t["value"], str) else " / ".join(f"{k}: {x}" for k, x in t["value"].items())
        other += f'<tr><td><code>{t["name"]}</code></td><td>{html.escape(v)}</td><td>{html.escape(t.get("usage", ""))}</td></tr>'
ds_page("design-system/tokens.html", "Tokens · SmarType",
        '<div class="eyebrow">Tokens</div><h1>Tokens</h1>' + THEME_JS + f'<h2>Colour</h2><div class="swatch">{sw}</div>'
        f'<h2>Type</h2><table><tr><th>Style</th><th>Size / line</th><th>Weight</th><th>Use</th></tr>{type_rows}</table>'
        f'<h2>Spacing, radius, elevation, state</h2><table><tr><th>Token</th><th>Value</th><th>Use</th></tr>{other}</table>'
        '<p>Machine-readable: <a href="tokens.css">tokens.css</a>.</p>')

# Downloads
os.makedirs(os.path.join(OUT, "downloads"), exist_ok=True)


def zip_dir(src, dst, prefix, skip=()):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = sorted(d for d in dirs if d not in skip)
            for f in sorted(files):
                if f.startswith("."):
                    continue
                p = os.path.join(root, f)
                z.write(p, os.path.join(prefix, os.path.relpath(p, src)))


zip_dir(os.path.join(ASSETS, "brand"), os.path.join(OUT, "downloads/smartype-brand-assets.zip"), "smartype-brand")
zip_dir(os.path.join(ASSETS, "illustrations"), os.path.join(OUT, "downloads/smartype-illustrations.zip"), "smartype-illustrations", skip=("source",))

with open(os.path.join(OUT, "vercel.json"), "w") as f:
    json.dump({"cleanUrls": False, "trailingSlash": False}, f, indent=2)
    f.write("\n")
print("built", sum(len(fs) for _, _, fs in os.walk(OUT)), "files")

