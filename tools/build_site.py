"""Builds the static site in site/ from src/ and assets/.

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
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "site")
sys.path.insert(0, SRC)

import components  # noqa: E402
from edges import EDGES  # noqa: E402
from taps import TAPS  # noqa: E402
from flows import BUILD_ORDER, FLOWS, RISK, RULES  # noqa: E402
from screens import S  # noqa: E402
from brand_page import brand_body  # noqa: E402
from illustration_concepts import CONCEPTS  # noqa: E402
from illustration_merge import SCENES  # noqa: E402

E = html.escape
DS = os.path.join(SRC, "design-system")
TOKENS = json.load(open(os.path.join(DS, "tokens.json")))
SPRITE = components.sprite()
STATUS = {"ready": ("ready", "Ready to build"), "review": ("ready", "Ready to build"), "decision": ("decision", "Needs a decision")}
KIND = {"change": ("change", "Change"), "new": ("new", "New feature")}


def read(p):
    with open(p) as f:
        return f.read()


def write(rel, text):
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


def tokens_css():
    themes = {"dark": {}, "light": {}, "amoled": {}}

    def put(name, v):
        for th in themes:
            themes[th][name] = v if isinstance(v, str) else v.get(th) or v.get("dark")

    for t in TOKENS["color"]["tokens"]:
        put(t["name"], t["value"])
    for g in ("spacing", "radius", "opacity", "shadow"):
        for t in TOKENS[g]["tokens"]:
            put(t["name"], t["value"])

    def block(d):
        return "".join(f"--{k}:{v};" for k, v in d.items())

    fam = TOKENS["type"]["families"]["sans"]
    return (f":root{{--font-sans:{fam};{block(themes['dark'])}color-scheme:dark}}\n"
            f"@media (prefers-color-scheme:light){{:root:not([data-theme]){{{block(themes['light'])}color-scheme:light}}}}\n"
            f":root[data-theme=light]{{{block(themes['light'])}color-scheme:light}}\n"
            f":root[data-theme=amoled]{{{block(themes['amoled'])}}}\n")


NAV = [("index.html#flows", "Flows"), ("brand.html", "Brand"), ("illustrations.html", "Illustrations"), ("backlog.html", "Backlog"), ("design-system/index.html", "Design system"),
       ("design-system/icons.html", "Icons"), ("downloads.html", "Downloads")]


def page(rel, title, body, current=None, extra_head=""):
    up = "../" * rel.count("/")
    links = "".join(f'<a href="{up}{h}"{" aria-current=page" if h == current else ""}>{E(l)}</a>' for h, l in NAV)
    seg = ('<div class="seg" role="group" aria-label="Theme">' +
           "".join(f'<button type="button" data-theme-btn="{v}">{l}</button>' for v, l in (("auto", "Auto"), ("dark", "Dark"), ("light", "Light"))) + "</div>")
    head = (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{E(title)}</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">'
            f'<link rel="stylesheet" href="{up}assets/tokens.css"><link rel="stylesheet" href="{up}assets/site.css"><link rel="stylesheet" href="{up}assets/spec.css">'
            f'<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{up}assets/favicon-32.png" sizes="32x32">'
            f'<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">'
            f'{extra_head}<script src="{up}assets/spec.js"></script></head>')
    nav = f'<nav class="top" aria-label="Site"><a class="brand" href="{up}index.html">SmarType design</a>{links}<span class="sp"></span>{seg}</nav>'
    return head + "<body>" + SPRITE + nav + f'<main class="wrap">{body}</main></body></html>\n'


def tag(cls, text):
    return f'<span class="tag {cls}">{E(text)}</span>'


def flow_tags(f):
    k, kl = KIND[f["kind"]]
    s, sl = STATUS[f["status"]]
    out = tag(k, kl) + tag(s, sl)
    if f["risky"]:
        out += tag("review", "Plan review")
    return out


# ---------- flow pages ----------

def screen_html(sid, caption, depth):
    dev = S[sid].replace("{root}", "../" * depth)
    return (f'<figure class="spec-screen" id="{sid}"><div class="spec-stage">{dev}</div><figcaption>{E(caption)}</figcaption>'
            '<details class="spec-table"><summary>Spec: sizes, tokens and icons</summary><div class="tbl"><table><thead><tr>'
            '<th>Element</th><th>Size (dp)</th><th>Component</th><th>Tokens</th><th>Icon</th></tr></thead><tbody></tbody></table></div></details></figure>')


def item_html(it, depth):
    if it[0] == "img":
        return f'<figure><img src="{"../" * depth}assets/today/{it[1]}" alt="{E(it[2])}" loading="lazy"><figcaption>{E(it[2])}</figcaption></figure>'
    if it[0] == "scr":
        return screen_html(it[1], it[2], depth)
    return f'<figure><div class="none">{E(it[1])}</div></figure>'


def flow_page(i, f):
    depth = 1
    parts = [f'<div class="crumb"><a href="../index.html#flows">All flows</a> › {E(f["title"])}</div>',
             f'<div class="tags">{flow_tags(f)}{"".join(tag("id", x) for x in f["ids"])}</div>',
             f'<h1>{E(f["title"])}</h1><p class="lede">{E(f["summary"])}</p>',
             '<div class="toolbar"><button type="button" class="mbtn" id="measure-toggle" aria-pressed="false">Show measurements</button>'
             '<span class="hint">New screens are drawn at real size: 1 px = 1 dp on a 360 × 800 dp phone. Open "Spec" under any screen for sizes, tokens and icons.</span></div>']
    parts.append('<section class="problem"><h2>The problem</h2>' + "".join(f"<p>{E(p)}</p>" for p in f["problem"]) + "</section>")
    if f.get("research"):
        r = f["research"]
        parts.append('<h2>What people need</h2><div class="tbl"><table><thead><tr><th>Need</th><th>Why</th></tr></thead><tbody>' +
                     "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in r["needs"]) + "</tbody></table></div>")
        parts.append('<h2>What others do</h2><div class="tbl"><table><thead><tr><th>Product</th><th>How it works</th><th>What we take</th></tr></thead><tbody>' +
                     "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in r["others"]) + "</tbody></table></div>"
                     '<p style="font-size:13.5px;color:var(--on-surface-variant)">Sources: ' +
                     "; ".join(f'<a href="{E(u)}" rel="noopener">{E(t)}</a>' for t, u in r["sources"]) + "</p>")
    if f.get("order"):
        t, n = f["order"]
        parts.append('<div class="flowline"><b>Today</b>' + "".join(f"<span>{E(x)}</span>" for x in t) + "</div>"
                     '<div class="flowline new"><b>New</b>' + "".join(f"<span>{E(x)}</span>" for x in n) + "</div>")
    if f["kind"] == "new":
        parts.append('<h2>What to build</h2><ol class="build">' + "".join(f"<li>{E(x)}</li>" for x in f["build"]) + "</ol>")
        parts.append('<h2>The new screens</h2><div class="shots">' + "".join(item_html(x, depth) for x in f["new"]) + "</div>")
    else:
        parts.append("<h2>Today and new</h2>")
        for label, today, new in f["compare"]:
            tcol = "".join(item_html(x, depth) for x in today)
            ncol = "".join(f'<div class="newtext">{E(x[1])}</div>' if x[0] == "text" else item_html(x, depth) for x in new)
            parts.append(f'<section class="step"><h3>{E(label)}</h3><div class="cmp"><div class="col today"><h4>Today</h4><div class="shots">{tcol}</div></div>'
                         f'<div class="col new"><h4>New</h4><div class="shots">{ncol}</div></div></div></section>')
    for t in f.get("tables", []):
        parts.append(f'<h2>{E(t["title"])}</h2>' + "".join(f"<p>{E(x)}</p>" for x in t.get("intro", [])) +
                     '<div class="tbl"><table><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in t["head"]) + "</tr></thead><tbody>" +
                     "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in t["rows"]) + "</tbody></table></div>" +
                     ("".join(f"<p>{E(x)}</p>" for x in t.get("after", []))) +
                     ('<p style="font-size:13.5px;color:var(--on-surface-variant)">Sources: ' +
                      "; ".join(f'<a href="{E(u)}" rel="noopener">{E(n)}</a>' for n, u in t["sources"]) + "</p>" if t.get("sources") else ""))
    taps = f.get("taps") or TAPS.get(f["slug"])
    if taps:
        parts.append('<h2>Steps and taps</h2><p style="color:var(--on-surface-variant);margin:0 0 10px">The main tasks: how many taps today and in the new design, and whether the user types or speaks.</p>'
                     '<div class="tbl"><table><thead><tr><th>Task</th><th>Today</th><th>New</th><th>Typing or speaking</th></tr></thead><tbody>' +
                     "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in taps) + "</tbody></table></div>")
    if f.get("later"):
        L = f["later"]
        parts.append(f'<h2>Later: new features this needs</h2><p>{E(L["intro"])}</p><ul>' + "".join(f"<li>{E(x)}</li>" for x in L["items"]) +
                     '</ul><div class="shots">' + "".join(item_html(x, depth) for x in L["screens"]) + "</div>")
    if f.get("changes"):
        parts.append('<h2>What changes</h2><div class="tbl"><table><thead><tr><th>Moment</th><th>Today</th><th>New</th></tr></thead><tbody>' +
                     "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in f["changes"]) + "</tbody></table></div>")
    if f.get("copy"):
        parts.append('<h2>Wording</h2><div class="tbl"><table><thead><tr><th>Where</th><th>Text</th></tr></thead><tbody>' +
                     "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in f["copy"]) + "</tbody></table></div>")
    if EDGES.get(f["slug"]):
        parts.append('<h2>Edge cases</h2><div class="tbl"><table><thead><tr><th>Case</th><th>What happens</th></tr></thead><tbody>' +
                     "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in EDGES[f["slug"]]) + "</tbody></table></div>")
    parts.append('<h2>Done when</h2><ul class="check">' + "".join(f"<li>{E(x)}</li>" for x in f["done"]) + "</ul>")
    dev = '<details class="dev"><summary>For developers</summary>'
    if f["decisions"]:
        dev += ('<h3>Open decisions for the owner</h3><div class="tbl"><table><thead><tr><th>Decision</th><th>Recommendation</th></tr></thead><tbody>' +
                "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in f["decisions"]) + "</tbody></table></div>")
    if f.get("decided"):
        dev += ('<h3>Decided</h3><div class="tbl"><table><thead><tr><th>Question</th><th>Decision</th></tr></thead><tbody>' +
                "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in f["decided"]) + "</tbody></table></div>")
    dev += ('<h3>Where in the code</h3><div class="tbl"><table><thead><tr><th>Change</th><th>Where</th></tr></thead><tbody>' +
            "".join(f"<tr><td>{E(a)}</td><td><code>{E(b)}</code></td></tr>" for a, b in f["code"]) + "</tbody></table></div>")
    if f["risky"]:
        dev += ("<h3>Risky areas</h3><p>This touches " + ", ".join(E(RISK[r]) for r in f["risky"]) +
                ". Per the app repository's AGENTS.md, a plan that touches these needs the owner's plan review before work starts.</p>")
    parts.append(dev + "</details>")
    prev = FLOWS[i - 1] if i > 0 else None
    nxt = FLOWS[i + 1] if i + 1 < len(FLOWS) else None
    parts.append('<div class="pn">' + (f'<a href="{prev["slug"]}.html"><small>Previous</small>{E(prev["title"])}</a>' if prev else "<span></span>") +
                 (f'<a href="{nxt["slug"]}.html"><small>Next</small>{E(nxt["title"])}</a>' if nxt else "") + "</div>")
    return page(f"flows/{f['slug']}.html", f"{f['title']} · SmarType", "".join(parts), current="index.html#flows")


# ---------- illustration concepts ----------

ART_NEEDED = [
    ("Welcome", "Setup, first page", "200 dp hero"), ("Sign in", "Setup, after the first try", "200 dp hero"),
    ("You're all set", "Setup, last page", "200 dp hero"), ("Premium", "Premium screen", "200 dp hero"),
    ("SmarType AI", "AI settings screen", "200 dp hero"), ("No notes yet", "Notes list", "160 dp empty state"),
    ("No writing styles yet", "Writing styles", "160 dp empty state"), ("No languages found", "Add language search", "160 dp empty state"),
    ("No keyboard languages", "Keyboard languages", "160 dp empty state"), ("No custom themes", "Themes", "160 dp empty state"),
    ("Empty dictionary", "User dictionary", "160 dp empty state"), ("Extension not found", "Extensions", "160 dp empty state"),
]


def illustrations_page():
    cards = []
    for key, title, fn, idea, good, risks in CONCEPTS:
        cards.append(
            f'<section class="bk-dir" id="{key}"><div class="ill-stage"><div class="ill-light">{fn(240)}</div><div class="ill-dark">{fn(240)}</div></div>'
            f'<div class="bk-body"><h3>{E(title)}</h3><p>{E(idea)}</p><div class="bk-pc"><div><h4>Works</h4><ul>' +
            "".join(f"<li>{E(x)}</li>" for x in good) + '</ul></div><div><h4>Watch out</h4><ul>' + "".join(f"<li>{E(x)}</li>" for x in risks) + "</ul></div></div></div></section>")
    need = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in ART_NEEDED)
    scenes = "".join(
        f'<figure class="ill-scene" id="{key}"><div class="ill-pair"><div class="ill-light">{fn(240)}</div><div class="ill-dark">{fn(240)}</div></div>'
        f'<figcaption><b>{E(title)}</b> · <span>{E(where)}</span><br>{E(text)}</figcaption></figure>' for key, title, fn, where, text in SCENES)
    body = ('<h1>Illustrations</h1><p class="lede">The key, alive and in action: the brand key is the character, and it does what SmarType does. Animated here on light and dark.</p>'
            '<h2>Proposed: the key, in action</h2><p>A merge of two concepts below: the character from <a href="#alive">The key, alive</a> performs the product scenes from <a href="#moments">Moments</a>. '
            'It starts as the app icon: the S lifts off the key and becomes the first letter of a message, and the blank key opens its eyes and watches the rest being typed. Then it fixes, translates and listens. '
            'Every illustration in the set is one of these moments or a pose of the same character (holding a note for Notes, searching for no results, asleep for an empty list).</p>'
            '<div class="ill-scenes">' + scenes + '</div>'
            '<div class="tbl" style="margin-top:16px"><table><thead><tr><th>Rule</th><th>Spec</th></tr></thead><tbody>'
            '<tr><td>Character</td><td>The brand key (white face, light lip). Face: two Ink eyes and a smile, mint cheeks. No arms, no legs, no S while it\'s a character</td></tr>'
            '<tr><td>Where it comes from</td><td>The app icon: the S lifts off the key and becomes the first letter typed; the blank key wakes up. At the end the S flies home to the logo</td></tr>'
            '<tr><td>Expressions</td><td>Watching: eyes follow the caret. Surprised: eyes wide, eyebrows up, a small round mouth, head tilt. Focused: eyes squint, eyebrows down. Happy: ^ ^ eyes, big smile, a hop. Asleep: closed eyes (empty lists)</td></tr>'
            '<tr><td>The spark</td><td>Its idea and its tool: it throws the spark to fix things. Always the brand spark, deep gradient</td></tr>'
            '<tr><td>Motion</td><td>Springy: squash and stretch on hops, a blink every few seconds, loops of 4–6 s. Lottie in the app, a still frame for reduced motion</td></tr>'
            '<tr><td>Words in scenes</td><td>Short and localised: one short message per bubble</td></tr>'
            '</tbody></table></div>'
            '<p>Other ways in, if this one doesn\'t land: the logo key flips over like a card and the back is the face; or the spark taps the key like a press, the S fades and the eyes open. '
            'Morphing the S itself into a face was tried and dropped: one letter doesn\'t turn into a face convincingly.</p>'
            '<h2>Why a new set</h2><p>Today\'s four illustrations are 3D clay renders of a graphite key with a puffy star: they match neither the new white key nor the brand spark, and they\'re images, not vectors. '
            'A first flat-vector try with the brand\'s shapes was clean but read as large icons, with no story and no life. Strong onboarding art (Duolingo, Headspace, Google\'s Material 3 Expressive) gets its life from a story, a character or motion.</p>'
            + '<h2>Earlier concepts</h2>' + "".join(cards) +
            '<h2>Where art is needed</h2><div class="tbl"><table><thead><tr><th>Illustration</th><th>Screen</th><th>Size</th></tr></thead><tbody>' + need + "</tbody></table></div>"
            '<p>Inside the keyboard stays icon-only. All art is vector: SVG for the site and store, Lottie for motion in the app, with a still frame for reduced motion.</p>'
            '<p style="font-size:13.5px;color:var(--on-surface-variant)">References: '
            '<a href="https://speckyboy.com/8-beautifully-illustrated-onboarding-screens-in-mobile-design/" rel="noopener">Speckyboy: illustrated onboarding screens</a>; '
            '<a href="https://fireart.studio/blog/7-tips-to-create-engaging-illustrations-for-mobile-app-onboarding/" rel="noopener">Fireart: engaging onboarding illustrations</a>; '
            '<a href="https://www.dezeen.com/2025/05/28/google-ushers-in-age-of-expressive-interfaces-with-material-design-update/amp/" rel="noopener">Dezeen: Material 3 Expressive</a>; '
            '<a href="https://www.androidauthority.com/google-material-3-expressive-features-changes-availability-supported-devices-3556392/" rel="noopener">Android Authority: Material 3 Expressive</a>.</p>')
    return page("illustrations.html", "Illustrations · SmarType", body, current="illustrations.html")


# ---------- backlog (from the review) ----------

def review_findings():
    s = read(os.path.join(ROOT, "archive/earlier/review.html"))
    out = {}
    for m in re.finditer(r'<article class="finding[^"]*"[^>]*>(.*?)</article>', s, re.S):
        a = m.group(1)
        fid = re.search(r'class="id">([^<]+)<', a).group(1)
        sev = re.search(r'class="sev [^"]+">([^<]+)<', a).group(1)
        title = html.unescape(re.sub("<[^>]+>", "", re.search(r"<h3>(.*?)</h3>", a, re.S).group(1)))
        paras = re.findall(r'<div class="label">([^<]+)</div><p[^>]*>(.*?)</p>', a, re.S)
        d = {k: html.unescape(re.sub("<[^>]+>", "", v)) for k, v in paras}
        out[fid] = dict(sev=sev, title=title, what=d.get("What happens", ""), fix=d.get("Proposed fix", ""))
    return out


BACKLOG = []


def backlog_page():
    R = review_findings()
    rows = []
    for fid in BACKLOG:
        r = R[fid]
        img = f"{fid}-1.jpg"
        shot = (f'<img src="assets/today/{img}" alt="" loading="lazy">' if os.path.exists(os.path.join(ASSETS, "screens/today", img))
                else '<div class="ph"></div>')
        rows.append(f'<div class="bl">{shot}<div><div class="tags">{tag("id", fid)}{tag("later", r["sev"])}</div>'
                    f'<h3 style="margin-top:10px">{E(r["title"])}</h3><p><b>What happens.</b> {E(r["what"])}</p>'
                    f'<p><b>Direction.</b> {E(r["fix"])}</p></div></div>')
    lede = ("What's left from the UX review: each needs a check on a device or a small design. Every other finding is covered by a flow." if rows else
            "Nothing left: every finding from the UX review is covered by a flow. The last three became Autocorrect (K1), the More panel in The bar above the keys (K4) and TalkBack and screen readers (A8).")
    body = f'<h1>Backlog</h1><p class="lede">{E(lede)}</p>' + "".join(rows)
    return page("backlog.html", "Backlog · SmarType", body, current="backlog.html")


# ---------- home ----------

def home_page():
    cards = "".join(f'<a class="card" href="flows/{f["slug"]}.html"><div class="tags">{flow_tags(f)}</div><b>{E(f["title"])}</b>'
                    f'<span class="s">{E(f["summary"])}</span><div class="tags">{"".join(tag("id", x) for x in f["ids"][:6])}</div></a>' for f in FLOWS)
    by = {f["slug"]: f for f in FLOWS}
    order = "".join(f'<li><a href="flows/{s}.html">{E(by[s]["title"])}</a>: {E(t)}</li>' for s, t in BUILD_ORDER)
    dec = "".join(f'<tr><td><a href="flows/{f["slug"]}.html">{E(f["title"])}</a></td><td>{E(a)}</td><td>{E(b)}</td></tr>' for f in FLOWS for a, b in f["decisions"])
    body = (
        '<h1>SmarType: what changes, and why</h1>'
        '<p class="lede">Every flow we\'re changing in the SmarType keyboard app. Each page shows the problem, today\'s screens next to the new ones, '
        'what changes, and when it\'s done. New screens are drawn at real size with measurements, tokens and icons.</p>'
        '<div class="howto"><div><b>1 · The problem</b>What goes wrong for the user today.</div><div><b>2 · Today and new</b>Real screenshots beside the new designs.</div>'
        '<div><b>3 · What changes</b>Each moment: today, new.</div><div><b>4 · Done when</b>The checklist to accept the work.</div>'
        '<div><b>5 · For developers</b>Code, decisions, risky areas.</div></div>'
        f'<h2 id="flows">Flows</h2><div class="grid">{cards}</div>'
        '<p class="note" style="margin-top:16px"><b>Change</b> improves something that exists. <b>New feature</b> is new work. <b>Plan review</b>: it touches a risky area of the app '
        '(sign-in, payments, the AI quota, text in other apps, typed-text privacy), so the owner reviews the plan first.</p>'
        f'<h2>Suggested build order</h2><ol class="build">{order}</ol>'
        f'<h2>Open decisions</h2><div class="tbl"><table><thead><tr><th>Flow</th><th>Decision</th><th>Recommendation</th></tr></thead><tbody>{dec}</tbody></table></div>'
        '<h2>Rules for every change</h2><ul class="check">' + "".join(f"<li>{E(r)}</li>" for r in RULES) + "</ul>"
        '<h2>Also here</h2><div class="grid">'
        f'<a class="card" href="backlog.html"><b>Backlog</b><span class="s">{len(BACKLOG)} problems from the review that still need a check or a design.</span></a>'
        '<a class="card" href="design-system/index.html"><b>Design system</b><span class="s">Principles, components and tokens.</span></a>'
        '<a class="card" href="design-system/icons.html"><b>Icons</b><span class="s">Material Symbols Rounded: which icon goes where, and the files.</span></a>'
        '<a class="card" href="downloads.html"><b>Downloads</b><span class="s">App icon, illustrations and icon files.</span></a></div>')
    return page("index.html", "SmarType design", body, current="index.html#flows")


# ---------- icons ----------

ICON_USES = [
    ("Rewrite (AI)", "spark", "Brand, the only custom icon"), ("Translate", "translate", ""), ("Format", "format_list_bulleted", ""),
    ("Clipboard", "content_paste", ""), ("Notes", "sticky_note_2", "Filled when its panel is open"), ("Emoji", "mood", ""),
    ("More (smartbar)", "more_horiz", ""), ("Mic", "mic", ""), ("Back", "arrow_back", "Every panel and app bar"),
    ("Overflow menu", "more_vert", ""), ("Delete recording, remove", "delete", ""), ("Done (voice), selected row", "check", ""),
    ("New note, add language", "add", ""), ("Pin", "keep", "Filled when pinned"), ("Drag handle", "drag_indicator", ""),
    ("Globe key, languages", "language", ""), ("Copy", "content_copy", ""), ("Share", "share", "Notes ⋯ menu"), ("Undo", "undo", ""),
    ("Search", "search", ""), ("Row opens a screen", "chevron_right", ""), ("Dropdown", "arrow_drop_down", ""),
    ("Info banner", "info", ""), ("Warning and error banners", "error", "The banner colour tells them apart; no triangle icon"), ("Settings", "settings", ""),
    ("Keyboard", "keyboard", ""), ("Smartbar (settings)", "toolbar", ""), ("Success banner", "check_circle", ""), ("Close", "close", ""), ("Send (Ask AI in Notes)", "send", ""),
    ("Password fields", "lock", ""), ("Redo", "redo", ""), ("Cut", "content_cut", ""),
    ("Select all", "select_all", ""), ("Move cursor", "arrow_range", "Replaces the four-way arrows"), ("Autocorrect", "spellcheck", "Filled when on"),
    ("One-handed", "front_hand", "Filled when on"), ("Incognito", "domino_mask", "Filled when on"), ("Google sign-in", "google", "Google's brand mark (ic_google_g_icon)"),
]


def icon_svg(name, fill=False):
    return components.ic(name, fill=fill).replace(' class="s-ic"', "")


def icons_page():
    cards = "".join(
        f'<div><span class="pair">{icon_svg(n)}{icon_svg(n, True) if n not in ("spark", "google") else ""}</span><b>{E(use)}</b><code>{E(n)}</code>'
        f'{f"<span>{E(note)}</span>" if note else ""}</div>' for use, n, note in ICON_USES)
    body = ('<div class="crumb"><a href="index.html">Design system</a> › Icons</div><h1>Icons</h1>'
            '<p class="lede">One package for every icon: <b>Material Symbols Rounded</b> by Google (Apache 2.0). It\'s the native Material 3 set, so it matches Android and Gboard.</p>'
            '<h2>Rules</h2><ul class="check">'
            '<li>Style: Rounded, outlined, weight 400, grade 0, 24 dp. Filled only for a selected or active state (the right-hand icon in each pair).</li>'
            '<li>Import only the icons you use, as Android vector drawables (the download below has them), into one place such as a <code>SmarTypeIcons</code> object.</li>'
            '<li>Replace <code>material-icons-extended</code> (the old Material Icons, no longer updated) over time. Today the app mixes three styles across 104 files: about 280 filled, 100 outlined and 11 rounded.</li>'
            '<li>Exceptions: the brand spark for AI, the Google G on the sign-in button, and keyboard-only glyphs Material doesn\'t have (for example the kana switchers).</li>'
            '<li>Icon colour comes from the surrounding text colour (<code>on-surface-variant</code>, or <code>primary</code> when active). Icon-only buttons always have a content description.</li></ul>'
            f'<h2>Which icon goes where</h2><div class="icons">{cards}</div>'
            '<h2>Files</h2><p><a href="../downloads/smartype-icons.zip" download>smartype-icons.zip</a>: every icon above as SVG and as Android vector drawables (24 dp), plus the licence.</p>')
    return page("design-system/icons.html", "Icons · SmarType", body, current="design-system/icons.html")


def android_vector(svg_text, viewport, translate_y):
    paths = re.findall(r'<path([^>]*?)\sd="([^"]+)"([^>]*)>', svg_text)
    out = []
    for before, d, after in paths:
        fill = re.search(r'fill="([^"]+)"', before + after)
        out.append(f'    <path android:fillColor="{fill.group(1) if fill else "@android:color/white"}" android:pathData="{d}"/>')
    vw, vh = viewport
    inner = "\n".join(out)
    if translate_y:
        inner = f'  <group android:translateY="{translate_y}">\n{inner}\n  </group>'
    return (f'<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp"\n'
            f'    android:viewportWidth="{vw}" android:viewportHeight="{vh}" android:tint="?attr/colorControlNormal">\n{inner}\n</vector>\n')


def icons_zip():
    ms = os.path.join(ASSETS, "icons/material-symbols-rounded")
    with zipfile.ZipFile(os.path.join(OUT, "downloads/smartype-icons.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(ms)):
            s = read(os.path.join(ms, f))
            z.writestr(f"svg/{f}", s)
            z.writestr(f"android/ic_{f[:-4].replace('-', '_')}.xml", android_vector(s, (960, 960), 960))
        sp = read(os.path.join(ASSETS, "icons/brand/spark.svg"))
        z.writestr("svg/spark.svg", sp)
        z.writestr("android/ic_spark.xml", android_vector(sp, (24, 24), 0))
        z.writestr("LICENSE-material-symbols.txt",
                   "Material Symbols by Google, version 0.48.0 (@material-symbols/svg-400, rounded).\n"
                   "Licensed under the Apache License, Version 2.0: https://www.apache.org/licenses/LICENSE-2.0\n")


# ---------- design system ----------

def md(p):
    return markdown.markdown(read(p), extensions=["tables"])


COMPONENTS = ["Button", "Card", "Chip", "ListRow", "Sheet", "EmptyState", "KeyboardPanel"]
DS_HEAD = ('<link rel="stylesheet" href="bundle.css"><style>.pv{border:1px solid var(--outline-variant);border-radius:16px;padding:16px;margin:16px 0;background:var(--surface-container-low);overflow-x:auto}'
           '.swatch{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}.swatch div{border:1px solid var(--outline-variant);border-radius:10px;overflow:hidden;font-size:12.5px}'
           '.swatch i{display:block;height:44px}.swatch p{margin:0;padding:6px 8px}.toc{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:18px 0}'
           '.toc a{display:block;background:var(--surface-container-low);border-radius:14px;padding:12px 14px;text-decoration:none;color:var(--on-surface)}.toc a span{display:block;color:var(--on-surface-variant);font-size:13px}</style>')


def ds_write(rel, title, inner):
    write(rel, page(rel, title, inner, current="design-system/index.html", extra_head=DS_HEAD))


def preview_icons(html_text):
    """{{icon:name}} in a component preview becomes that Material Symbols Rounded icon (or the brand spark) from the sprite."""
    def one(m):
        name = m.group(1)
        ref = "br-spark" if name == "spark" else f"ms-{name}"
        if name != "spark" and not os.path.exists(os.path.join(ASSETS, "icons/material-symbols-rounded", f"{name}.svg")):
            raise SystemExit(f"preview icon not in the library: {name}")
        return f'<svg class="ds-ic" aria-hidden="true"><use href="#{ref}"/></svg>'
    return re.sub(r"\{\{icon:([a-z_]+)\}\}", one, html_text)


def design_system():
    shutil.copy(os.path.join(DS, "components/bundle.css"), os.path.join(OUT, "design-system/bundle.css"))
    toc = "".join(f'<a href="{c.lower()}.html"><b>{c}</b><span>Component</span></a>' for c in COMPONENTS)
    toc += ('<a href="icons.html"><b>Icons</b><span>Material Symbols Rounded</span></a><a href="tokens.html"><b>Tokens</b><span>Colour, type, spacing, radius</span></a>'
            '<a href="audit-buttons.html"><b>Button audit</b><span>Today\'s code</span></a><a href="audit-components.html"><b>Component audit</b><span>Today\'s code</span></a>'
            '<a href="illustrations.html"><b>Illustrations</b><span>Prompts and export sizes</span></a>')
    ds_write("design-system/index.html", "Design system · SmarType", f'<h1>Design system</h1><div class="toc">{toc}</div>' + md(os.path.join(DS, "README.md")))
    for c in COMPONENTS:
        if c == "KeyboardPanel":
            pv = ('<div class="toolbar"><button type="button" class="mbtn" id="measure-toggle" aria-pressed="false">Show measurements</button><span class="hint">Real size: 1 px = 1 dp.</span></div>'
                  '<div class="shots" style="margin:20px 0">' + screen_html("ai-open", "Rewrite panel", 1) + screen_html("er-ai", "Unavailable: one banner, no dock", 1) + "</div>")
        else:
            pv = f'<div class="pv">{preview_icons(read(os.path.join(DS, f"components/{c}/preview.html")))}</div>'
        ds_write(f"design-system/{c.lower()}.html", f"{c} · SmarType",
                 f'<div class="crumb"><a href="index.html">Design system</a> › {c}</div>' + pv + md(os.path.join(DS, f"components/{c}/README.md")))
    for name in ("audit-buttons", "audit-components", "illustrations"):
        ds_write(f"design-system/{name}.html", f"{name.replace('-', ' ').capitalize()} · SmarType",
                 '<div class="crumb"><a href="index.html">Design system</a></div>' + md(os.path.join(DS, f"{name}.md")))
    sw = "".join(f'<div><i style="background:var(--{t["name"]})"></i><p><b>{t["name"]}</b><br>{E(t.get("usage", ""))}</p></div>' for t in TOKENS["color"]["tokens"])
    type_rows = "".join(f'<tr><td><code>{s["name"]}</code></td><td>{s["fontSize"]} / {s["lineHeight"]}</td><td>{s["fontWeight"]}</td><td>{E(s.get("usage", ""))}</td></tr>'
                        for g in TOKENS["type"]["groups"] for s in g["styles"])
    other = ""
    for g in ("spacing", "radius", "shadow", "opacity"):
        for t in TOKENS[g]["tokens"]:
            v = t["value"] if isinstance(t["value"], str) else " / ".join(f"{k}: {x}" for k, x in t["value"].items())
            other += f'<tr><td><code>{t["name"]}</code></td><td>{E(v)}</td><td>{E(t.get("usage", ""))}</td></tr>'
    ds_write("design-system/tokens.html", "Tokens · SmarType",
             '<div class="crumb"><a href="index.html">Design system</a> › Tokens</div><h1>Tokens</h1>'
             '<p>Values are dp in Android, shown as px. Switch the theme at the top right to see light and dark.</p>'
             f'<h2>Colour</h2><div class="swatch">{sw}</div><h2>Type</h2><div class="tbl"><table><thead><tr><th>Style</th><th>Size / line</th><th>Weight</th><th>Use</th></tr></thead><tbody>{type_rows}</tbody></table></div>'
             f'<h2>Spacing, radius, elevation, state</h2><div class="tbl"><table><thead><tr><th>Token</th><th>Value</th><th>Use</th></tr></thead><tbody>{other}</tbody></table></div>'
             '<p>Machine-readable: <a href="../assets/tokens.css">tokens.css</a>.</p>')
    write("design-system/icons.html", icons_page())


# ---------- downloads ----------

def zip_dir(src, dst, prefix, skip=()):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = sorted(d for d in dirs if d not in skip)
            for f in sorted(files):
                if not f.startswith("."):
                    p = os.path.join(root, f)
                    z.write(p, os.path.join(prefix, os.path.relpath(p, src)))


def downloads_page():
    zip_dir(os.path.join(ASSETS, "brand"), os.path.join(OUT, "downloads/smartype-brand-assets.zip"), "smartype-brand")
    zip_dir(os.path.join(ASSETS, "illustrations"), os.path.join(OUT, "downloads/smartype-illustrations.zip"), "smartype-illustrations", skip=("source",))
    shutil.copy(os.path.join(ASSETS, "brand/png/logo-480.png"), os.path.join(OUT, "assets/art/logo.png"))
    shutil.copy(os.path.join(ASSETS, "retired/keycap-3d.png"), os.path.join(OUT, "assets/art/keycap-3d.png"))
    shutil.copytree(os.path.join(ASSETS, "brand/svg"), os.path.join(OUT, "assets/brand"), dirs_exist_ok=True)
    for f in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png"):
        shutil.copy(os.path.join(ASSETS, "brand/web", f), os.path.join(OUT, "assets", f))
    art = "".join(f'<figure><img src="assets/art/{n}.webp" alt=""><figcaption><code>{n}</code></figcaption></figure>'
                  for n in ("art_onb_suggestions", "art_signin", "art_subscription", "art_empty_languages"))
    body = ('<h1>Downloads</h1><p class="lede">Files developers need. Everything else is on the flow pages.</p>'
            '<h2>Icon kit</h2><div class="bl" style="border:0"><img src="assets/art/logo.png" alt="SmarType app icon" style="box-shadow:none;border-radius:24px">'
            '<div><ul class="check"><li>Android: adaptive icon layers as vector drawables, themed icon, debug and beta icons, status-bar icon and splash icon.</li>'
            '<li>Play Store icon (512 px, 32-bit PNG), favicons and web app icons.</li><li>Wordmark and lockup as outlined SVG, and lockup PNGs.</li>'
            '<li>See <a href="brand.html">Brand</a> for how it\'s built and the spark rules. Don\'t recolour, crop or add effects.</li></ul>'
            '<p><a href="downloads/smartype-brand-assets.zip" download>smartype-brand-assets.zip</a>: everything above, with a README on where each file goes in the app.</p></div></div>'
            f'<h2>Illustrations</h2><p>Soft clay art for onboarding, sign-in, Premium and empty states. Show at 160–240 dp; never inside the keyboard.</p><div class="art">{art}</div>'
            '<p><a href="downloads/smartype-illustrations.zip" download>smartype-illustrations.zip</a>: WebP at mdpi, xhdpi and xxhdpi, plus 2000 px masters.</p>'
            '<h2>Icons</h2><p><a href="downloads/smartype-icons.zip" download>smartype-icons.zip</a>: Material Symbols Rounded as SVG and Android vector drawables. '
            'See <a href="design-system/icons.html">Icons</a> for which goes where.</p>')
    return page("downloads.html", "Downloads · SmarType", body, current="downloads.html")


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for d in ("assets/today", "assets/art", "downloads", "flows", "design-system"):
        os.makedirs(os.path.join(OUT, d))
    write("assets/tokens.css", tokens_css())
    for f in ("site.css", "spec.css", "spec.js"):
        shutil.copy(os.path.join(SRC, f), os.path.join(OUT, "assets", f))
    for f in os.listdir(os.path.join(ASSETS, "screens/today")):
        shutil.copy(os.path.join(ASSETS, "screens/today", f), os.path.join(OUT, "assets/today", f))
    for n in ("art_onb_suggestions", "art_signin", "art_subscription", "art_empty_languages"):
        shutil.copy(os.path.join(ASSETS, f"illustrations/android/drawable-xxhdpi/{n}.webp"), os.path.join(OUT, f"assets/art/{n}.webp"))
    icons_zip()
    write("index.html", home_page())
    for i, f in enumerate(FLOWS):
        write(f"flows/{f['slug']}.html", flow_page(i, f))
    write("backlog.html", backlog_page())
    design_system()
    write("downloads.html", downloads_page())
    write("illustrations.html", illustrations_page())
    write("brand.html", page("brand.html", "Brand · SmarType", brand_body(""), current="brand.html"))
    with open(os.path.join(OUT, "vercel.json"), "w") as fh:
        json.dump({"cleanUrls": False, "trailingSlash": False}, fh, indent=2)
        fh.write("\n")
    print("built", sum(len(fs) for _, _, fs in os.walk(OUT)), "files")


if __name__ == "__main__":
    main()
