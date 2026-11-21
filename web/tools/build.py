"""Builds the SmarType website into web/site from the pages below and the brand assets in design/.

    python3 web/tools/build.py

Static HTML and CSS, no framework. Brand marks, favicons and illustrations are copied from design/assets, so the
website always matches the brand kit. Vercel serves web/site."""
import html
import json
import os
import re
import shutil

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(WEB)
DESIGN = os.path.join(ROOT, "design", "assets")
OUT = os.path.join(WEB, "site")
E = html.escape

SUPPORT = "contact@smartype.in"
PLAY_STORE_URL = "https://play.google.com/store/apps/details?id=bha.keys.smartype"
YEAR = 2026
UPDATED = "2026-11-21"
SITE = "https://smartype.in"
INDIAN_TRANSLATE = ["Hindi", "Telugu", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali", "Gujarati", "Punjabi", "Odia", "Urdu"]
OTHER_TRANSLATE = ["English", "Arabic", "Chinese (Simplified)", "Dutch", "French", "German", "Greek", "Hebrew", "Indonesian", "Italian", "Japanese",
                   "Korean", "Polish", "Portuguese", "Russian", "Spanish", "Swedish", "Thai", "Turkish", "Vietnamese"]
TRANSLATE_FAQ = ("31 languages: " + ", ".join(INDIAN_TRANSLATE) + ", and " + ", ".join(OTHER_TRANSLATE[:-1]) + " and " + OTHER_TRANSLATE[-1]
                 + ". It detects the language you wrote in, so there is nothing to set first.")
LLMS_TRANSLATE = ", ".join(INDIAN_TRANSLATE + OTHER_TRANSLATE)
ILLUSTRATIONS = ["art_welcome", "art_signin", "art_ai", "art_premium", "art_empty_languages", "art_empty_notes", "art_done"]


# ---------- icons (Material Symbols Rounded, the brand spark) ----------

def icon(name, cls="ic"):
    if name == "spark":
        src = os.path.join(DESIGN, "icons/brand/spark.svg")
    else:
        src = os.path.join(DESIGN, "icons/material-symbols-rounded", f"{name}.svg")
    with open(src, encoding="utf-8") as fh:
        s = fh.read()
    view = re.search(r'viewBox="([^"]+)"', s).group(1)
    paths = "".join(re.findall(r"<path[^>]*/>", s))
    return f'<svg class="{cls}" viewBox="{view}" aria-hidden="true" fill="currentColor">{paths}</svg>'


# The Google Play logo, so the button reads as Play at a glance (used as Google's brand guidelines allow, to point to the app).
PLAY = ('<svg class="play" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="#00D7FE" d="M3.6 1.8 13.3 12 3.6 22.2c-.4-.2-.6-.6-.6-1.1V2.9c0-.5.2-.9.6-1.1z"/>'
        '<path fill="#00F076" d="M16.6 8.6 13.3 12 3.6 1.8c.3-.2.8-.2 1.2 0z"/>'
        '<path fill="#FFC900" d="M20.4 10.7c.8.4.8 1.6 0 2.1l-3.8 2.2-3.3-3 3.3-3.4z"/>'
        '<path fill="#F7304B" d="M16.6 15.4 4.8 22.2c-.4.2-.9.2-1.2 0l9.7-10.2z"/></svg>')


def play_button(label="Get it on Google Play", cls=""):
    """The one call to action: a flat button with the Play logo linking to the Google Play listing."""
    cls_attr = f"btn key {cls}".strip()
    return f'<a class="{cls_attr}" href="{E(PLAY_STORE_URL)}"><span class="play-chip">{PLAY}</span>{E(label)}</a>'


# The Apple logo, so the badge reads as the App Store at a glance (path from Simple Icons, CC0).
APPLE = ('<svg class="apple" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>')


def soon_badge():
    """The iPhone app is on its way: a badge, not a link, until it is on the App Store."""
    return '<span class="btn soon" role="note">' + APPLE + '<span class="soon-t"><small>Coming soon</small>App Store for iPhone</span></span>'


def ver(name):
    """A version from the file's contents for its link, so a browser never keeps an old copy after a change."""
    import hashlib
    path = os.path.join(WEB, "tools", name) if os.path.exists(os.path.join(WEB, "tools", name)) else os.path.join(WEB, "tools/vendor", name)
    with open(path, "rb") as fh:
        return f"/assets/{'js/' if name.endswith('.js') else ''}{name}?v={hashlib.sha1(fh.read()).hexdigest()[:8]}"


def art(name, size, cls="", eager=False):
    """An illustration that switches to its dark version with the system theme. Above the fold it loads first."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="art {cls}"><source media="(prefers-color-scheme: dark)" srcset="/assets/art/{name}-dark.svg">'
            f'<img src="/assets/art/{name}.svg" alt="" width="{size}" height="{size}" {load}></picture>')


def not_looking():
    """The brand key with its eyes squeezed shut, turning away from a message it can't read. The key, lip, ink and blush
    colours are the illustration set's (design/src/illustration_set.py); the privacy section is always dark."""
    ink, lip, mint = "#08323B", "#C3D5DA", "#4BDCA4"
    x, y, k = 148, 80, 72
    ex1, ex2, ey, rx, ry = x + .35 * k, x + .65 * k, y + .40 * k, .07 * k, .095 * k
    eyes = (f'<path d="M{ex1 - rx:.1f} {ey - ry * .8:.1f} L{ex1 + rx:.1f} {ey:.1f} L{ex1 - rx:.1f} {ey + ry * .8:.1f}"/>'
            f'<path d="M{ex2 + rx:.1f} {ey - ry * .8:.1f} L{ex2 - rx:.1f} {ey:.1f} L{ex2 + rx:.1f} {ey + ry * .8:.1f}"/>')
    mx, my = x + .5 * k, y + .63 * k
    lines = "".join(f'<rect x="28" y="{yy}" width="{w}" height="8" rx="4"/>' for yy, w in ((60, 92), (74, 104), (88, 60)))
    return (f'<svg class="peek" viewBox="0 0 240 170" role="img" aria-label="The SmarType key with its eyes shut, not looking at your message">'
            '<defs><filter id="peek-blur" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="2.6"/></filter>'
            f'<linearGradient id="peek-key" x1="0" y1="{y}" x2="0" y2="{y + k}" gradientUnits="userSpaceOnUse"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDF3F5"/></linearGradient></defs>'
            # your message, too blurred to read
            '<path class="peek-msg" d="M26 40 h96 a14 14 0 0 1 14 14 v42 a14 14 0 0 1 -14 14 H44 l-14 12 l2 -12 H26 a14 14 0 0 1 -14 -14 v-42 a14 14 0 0 1 14 -14 z"/>'
            f'<g class="peek-words" filter="url(#peek-blur)">{lines}</g>'
            # the key, turned away
            f'<g class="peek-key"><rect x="{x}" y="{y + .06 * k:.1f}" width="{k}" height="{k}" rx="{.24 * k:.1f}" fill="{lip}"/>'
            f'<rect x="{x}" y="{y}" width="{k}" height="{k}" rx="{.24 * k:.1f}" fill="url(#peek-key)"/>'
            f'<g fill="none" stroke="{ink}" stroke-width="{.045 * k:.1f}" stroke-linecap="round" stroke-linejoin="round">{eyes}'
            f'<path d="M{mx - .09 * k:.1f} {my:.1f} q{.045 * k:.1f} -{.04 * k:.1f} {.09 * k:.1f} 0 q{.045 * k:.1f} {.04 * k:.1f} {.09 * k:.1f} 0"/></g>'
            + "".join(f'<ellipse cx="{cx:.1f}" cy="{y + .58 * k:.1f}" rx="{.07 * k:.1f}" ry="{.04 * k:.1f}" fill="{mint}" opacity=".55"/>' for cx in (x + .2 * k, x + .8 * k))
            + '</g>'
            # what it says
            '<g class="peek-say"><path d="M150 26 h70 a12 12 0 0 1 12 12 v6 a12 12 0 0 1 -12 12 H204 l-6 9 l-2 -9 H150 a12 12 0 0 1 -12 -12 v-6 a12 12 0 0 1 12 -12 z" fill="#FFFFFF"/>'
            f'<text x="185" y="45" text-anchor="middle" fill="{ink}" font-size="12.5" font-weight="700" font-family="\'Google Sans Flex\', system-ui, sans-serif">not looking!</text></g>'
            '</svg>')


# ---------- layout ----------

# The header links: sections of the home page, then pages. On the home page a section link only scrolls.
NAV = [("how", "How it works"), ("features", "Features"), ("/languages.html", "Languages"), ("/compare.html", "Compare"), ("privacy", "Privacy"), ("/help.html", "Help")]


def nav_links(name):
    out = []
    for h, label in NAV:
        if h.startswith("/"):
            out.append(f'<a href="{h}"{" aria-current=page" if h == "/" + name else ""}>{E(label)}</a>')
        else:
            out.append(f'<a href="{"" if name == "index.html" else "/"}#{h}" data-sec="{h}">{E(label)}</a>')
    return "".join(out)


def lockup(height):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="/assets/lockup-porcelain.svg">'
            f'<img src="/assets/lockup-ink.svg" alt="SmarType" height="{height}"></picture>')


def ld(*objs):
    """JSON-LD blocks for search engines and AI answer engines."""
    return "".join('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", **o}, ensure_ascii=False).replace("</", "<\\/") + "</script>" for o in objs)


def crumbs(name, label):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": label, "item": SITE + "/" + name.replace(".html", "")}]}


def page(name, title, description, body, extra="", schema=None):
    """A page: the floating header (a pill; on phones a Menu sheet), the content and the footer. Links and assets
    start at the site root, so the 404 page also works at any depth."""
    links = nav_links(name)
    url = "https://smartype.in/" + ("" if name == "index.html" else name.replace(".html", ""))
    where = ('<meta name="robots" content="noindex">' if name == "404.html"
             else f'<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><link rel="canonical" href="{url}">'
                  f'<link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}"><meta property="og:url" content="{url}">')
    if schema is None and name not in ("index.html", "404.html"):
        schema = [crumbs(name, title.split(" · ")[0])]
    jsonld = ld(*schema) if schema else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(description)}">{where}
<meta property="og:type" content="website"><meta property="og:site_name" content="SmarType"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}"><meta property="og:locale" content="en_US"><meta property="og:image" content="https://smartype.in/assets/og.png">
<meta property="og:image:width" content="1024"><meta property="og:image:height" content="500"><meta property="og:image:alt" content="SmarType, the AI keyboard for Android">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(description)}"><meta name="twitter:image" content="https://smartype.in/assets/og.png">
<meta name="theme-color" content="#F5FAFB" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0B1416" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/assets/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{ver("site.css")}">{jsonld}</head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="top-pill"><a class="brand" href="/" aria-label="SmarType home">{lockup(28)}</a>
<nav class="top-nav" aria-label="Main"><span class="nav-hl" aria-hidden="true"></span>{links}</nav>{play_button("Google Play", "sm")}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button></div>
<nav class="menu" id="menu" aria-label="Menu" hidden>{links}{play_button()}</nav></header>
<main id="main">{body}</main>
<footer class="foot"><div class="wrap foot-in">
<div>{lockup(26)}<p>The Android keyboard that helps you type, speak and get it right.</p></div>
<nav class="foot-links" aria-label="Footer"><div><h2>Product</h2><a href="/languages.html">Indian languages</a><a href="/compare.html">Compare</a><a href="/help.html">Help</a><a href="/contact.html">Contact</a></div><div><h2>Free tools</h2><a href="/polite-whatsapp-rewriter.html">Polite WhatsApp rewriter</a><a href="/ai-tone-translator.html">AI tone translator</a><a href="/rough-notes-to-neat-list.html">Rough notes to neat list</a></div><div><h2>Privacy &amp; legal</h2><a href="/privacy-architecture.html">Privacy architecture</a><a href="/privacy.html">Privacy policy</a><a href="/terms.html">Terms</a></div></nav>
<p class="copy">© {YEAR} SmarType</p></div></footer><script src="{ver("site.js")}" defer></script>{extra}</body></html>
"""


# ---------- home ----------

# The phone in How it works, as in the design system's keyboard mockups (design/src/components.py): the smartbar
# (Rewrite, Translate, Format, Clipboard, Notes, More, then Voice), suggestions and four rows of keys. Its texts:
ROUGH = "great, can u send the adress"
FIXED = "Great! Can you send me the address?"
HINDI = "बढ़िया! क्या तुम मुझे पता भेज सकते हो?"
SPOKEN = "Can't wait, see you on Saturday!"


def sb(name, k="", ai=True):
    """A smartbar button: AI actions sit in a gradient circle."""
    data = f' data-k="{k}"' if k else ""
    inner = f"<span>{icon(name)}</span>" if ai else icon(name)
    return f'<span class="sb{" ai" if ai else ""}"{data}>{inner}</span>'


def keyboard():
    letters = lambda row: "".join(f'<i data-c="{c}">{c}</i>' for c in row)
    rows = [letters("qwertyuiop"), "<b></b>" + letters("asdfghjkl") + "<b></b>",
            f'<i class="fn k3">{icon("shift", "ic key")}</i>' + letters("zxcvbnm") + f'<i class="fn k3">{icon("backspace", "ic key")}</i>',
            f'<i class="fn k3">?123</i><i class="fn">{icon("language", "ic sm")}</i><i class="space k10" data-c=" ">English</i>'
            f'<i class="fn" data-c=".">.</i><i class="ent k3">{icon("keyboard_return", "ic key")}</i>']
    bar = (sb("spark", "fix") + sb("translate", "tr") + sb("format_list_bulleted") + sb("content_paste", ai=False)
           + sb("sticky_note_2", ai=False) + sb("more_horiz", ai=False) + '<span class="sp"></span>' + sb("mic", "mic"))
    voice = (sb("delete", ai=False) + '<span class="rec"><i></i><span class="rec-t">0:00</span></span><span class="veq">'
             + "<i></i>" * 18 + '</span><span class="vprog">Writing it up…</span><span class="vlang">Auto</span>' + sb("check"))

    def panel(k, title, chips, meta, text, lang=""):
        ch = "".join(f'<span{" class=sel" if i == 0 else ""}{f" lang={l}" if l else ""}>{E(c)}</span>' for i, (c, l) in enumerate(chips))
        return (f'<div class="ime-panel ip-{k}"><div class="ip-head">{sb("arrow_back", ai=False)}<span>{E(title)}</span></div>'
                f'<div class="ip-body"><div class="ip-chips">{ch}</div><div class="ip-res"><div class="ip-meta">{E(meta)}</div>'
                f'<div class="ip-text"{f" lang={lang}" if lang else ""}>{E(text)}</div></div>'
                '<div class="ip-dock"><span class="ip-btn">Copy</span><span class="ip-btn ai">Replace</span></div></div></div>')

    return (f'<div class="ime"><div class="ime-top"><div class="ime-bar">{bar}</div><div class="ime-voice">{voice}</div></div>'
            '<div class="ime-sugg"><span>adress</span><span class="b">address</span><span>addresses</span></div>'
            '<div class="ime-keys">' + "".join(f'<div class="krow">{r}</div>' for r in rows) + "</div>"
            + panel("fix", "Rewrite", [("Grammar fix", ""), ("Professional", ""), ("Casual", ""), ("Polite", "")], "Grammar fix", FIXED)
            + panel("tr", "Translate", [("हिन्दी", "hi"), ("తెలుగు", "te"), ("தமிழ்", "ta"), ("বাংলা", "bn")], "Hindi", HINDI, "hi")
            + "</div>")


HOME_DESC = ("Free AI keyboard for Android: fix grammar and tone in one tap, translate English to Hindi, Telugu, Tamil "
             "and 28 more languages, and voice type with punctuation. Private by default.")


def home():
    """The home page, one idea per section: what it is, how it works, styles, everything around it, privacy, try it.
    Text is typed in as each part appears and only the section in the middle of the screen moves (home.js); without
    JavaScript, or with reduced motion, every part shows its final state and the steps still switch on a tap."""
    steps = [
        ("Type", "Type the way you always do. Suggestions learn your words, on your phone.", "keyboard",
         '<span class="tag">' + icon("keyboard", "ic sm") + "Learns on your phone</span>"),
        ("Fix", "Tap the spark. Grammar, spelling and tone are fixed right where you type.", "spark",
         '<span class="diff"><s>u</s><b>you</b></span><span class="diff"><s>adress</s><b>address</b></span>'
         '<span class="diff"><s>great,</s><b>Great!</b></span>'),
        ("Translate", "Send it in Hindi, Telugu, Tamil, Bengali and 27 more languages. Add the ones you use and they stay one tap away.", "translate",
         '<span class="tag">English</span>' + icon("chevron_right", "ic sm") + '<span class="tag on" lang="hi">हिन्दी</span>'
         '<span class="tag" lang="te">తెలుగు</span><span class="tag" lang="ta">தமிழ்</span>'),
        ("Speak", "Or just say it. Tap the mic and speak for up to a minute; pausing to think won't stop it. Tap Check for clean, punctuated text.", "mic",
         '<span class="tag on"><span class="wave"><i></i><i></i><i></i><i></i><i></i></span>Clean text on Check</span>'),
    ]
    acc = "".join(
        f'<li class="acc-item{" on" if i == 0 else ""}" data-step="{i}"><div class="acc-bar" aria-hidden="true"><i class="acc-fill"></i></div>'
        f'<h3 class="acc-h"><button class="acc-head" type="button" id="acc-h{i}" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="acc-b{i}">'
        f'<span class="acc-num">0{i + 1}</span><span class="acc-title">{E(t)}</span><span class="acc-icon" aria-hidden="true">{icon(ic, "ic sm")}</span></button></h3>'
        f'<div class="acc-body" id="acc-b{i}" role="region" aria-labelledby="acc-h{i}"><div class="acc-body-in"><div class="acc-pad"><p>{E(d)}</p>'
        f'<div class="step-detail">{det}</div></div></div></div></li>' for i, (t, d, ic, det) in enumerate(steps))
    phone = (f'<div class="phone" aria-hidden="true" data-rough="{E(ROUGH)}" data-fixed="{E(FIXED)}" data-hindi="{E(HINDI)}" data-spoken="{E(SPOKEN)}">'
             '<div class="ph-screen"><div class="ph-chat"><div class="incoming">Party at our new place on Saturday!</div>'
             f'<div class="ph-field"><span class="field-text">{E(FIXED)}</span><i class="caret dc"></i></div></div>{keyboard()}</div></div>')

    # Real styles from the app (AiSuggestionStyle): it has more than 20, plus the user's own.
    tones = {"Professional": "I'd like to request leave on Friday. I'll finish my work before then.",
             "Casual": "Mind if I take Friday off? I'll wrap up my work before.",
             "Polite": "Would it be okay if I took Friday off? I'll make sure my work is done first.",
             "Simple": "Can I take Friday off? I'll finish my work first."}
    tone_chips = "".join(f'<button class="chip{" on" if i == 0 else ""}" type="button" aria-pressed="{"true" if i == 0 else "false"}" data-tone="{E(v)}">{E(k)}</button>'
                         for i, (k, v) in enumerate(tones.items()))

    hellos = [("Hello", "English", "en"), ("नमस्ते", "Hindi", "hi"), ("నమస్కారం", "Telugu", "te"), ("வணக்கம்", "Tamil", "ta"),
              ("নমস্কার", "Bengali", "bn"), ("Hola", "Spanish", "es"), ("Bonjour", "French", "fr")]
    lang_names = "".join(f'<li data-hello="{E(h)}" data-lang="{l}">{E(n)}</li>' for h, n, l in hellos)
    cards = [
        ("c-format", "format_list_bulleted", "Rough notes,<br><em>neat lists.</em>", "Bullets, numbered steps or a table, from whatever you typed.",
         '<div class="mini"><div class="raw">need tickets, hotel for 2 nights, cab from airport, dinner sat</div>'
         '<ul class="list"><li data-typeon>Tickets</li><li data-typeon>Hotel for 2 nights</li><li data-typeon>Cab from the airport</li><li data-typeon>Dinner on Saturday</li></ul></div>'),
        ("c-notes", "sticky_note_2", "Notes that<br><em>AI can polish.</em>", "Jot a list or keep something you copied. Ask AI to add to it or change its tone; undo in one tap.",
         '<div class="mini"><div class="ask">' + icon("spark", "ic sm") + '<span data-typeon>add that I\'ll pay the rent on Friday</span></div>'
         '<div class="note">Hey Ravi, the tap\'s fixed, thanks a lot! <mark data-typeon>I\'ll pay the rent on Friday.</mark></div></div>'),
        ("c-clip", "content_paste", "Copied it?<br><em>Paste in one tap.</em>", "Recent and pinned clips sit right above your keys, and stay on your phone.",
         '<div class="mini"><div class="clip pin">Office Wi-Fi: Lake-5G ' + icon("keep", "ic sm") + '</div><div class="clip">Order #48213 confirmed for Friday</div>'
         '<div class="clip">maps.app/meet-point</div></div>'),
        ("c-langs", "language", "Your languages,<br><em>one key apart.</em>", "Type in English, Hindi, Telugu, Tamil, Bengali and more. Add a language and English stays with it, so the globe key switches between them.",
         '<div class="mini hello"><div class="hello-card" aria-hidden="true"><span class="hello-word">Hello</span><i class="caret dc"></i></div>'
         f'<div class="hello-foot"><span class="globe" aria-hidden="true">{icon("language")}</span><ul class="lang-names">{lang_names}</ul></div></div>'),
    ]
    card_html = "".join(f'<article class="card {c}"><div class="card-copy"><div class="card-ic">{icon(i)}</div><h3>{h}</h3><p>{E(d)}</p></div>'
                        f'<div class="card-vis">{v}</div></article>' for c, i, h, d, v in cards)

    # Privacy: three promises, and one picture of where text goes (home.js plays one promise at a time).
    vows = [("keyboard", "Typing stays on your phone", "Suggestions are learned here. Your clipboard and notes stay here too."),
            ("spark", "AI sees only what you send", "SmarType sends text or AI voice audio encrypted only when you tap an AI button or Check. Offline or out of tries, system voice runs under its provider."),
            ("lock", "Password fields switch it off", "No AI, no voice and no learning while you type a password.")]
    vow_html = "".join(f'<li class="vow{" on" if i == 0 else ""}" data-phase="{i}"><button type="button" aria-pressed="{"true" if i == 0 else "false"}">'
                       f'<span class="pk">{icon(ic)}</span><span class="vow-t"><b>{E(t)}</b><span>{E(d)}</span></span></button></li>'
                       for i, (ic, t, d) in enumerate(vows))
    offs = "".join(f'<span>{icon("check_circle", "ic sm")}{t}</span>' for t in ("AI off", "Voice off", "Learning off"))
    seal = ('<div class="seal" aria-hidden="true" data-rough="hi mom ill be home by 6" data-fixed="Hi Mom, I\'ll be home by 6.">'
            f'<div class="seal-phone"><div class="seal-head"><span class="seal-lock">{icon("lock", "ic sm")}</span>Your phone<span class="seal-badge">Stays here</span></div>'
            '<div class="seal-field"><span class="seal-label">Message</span><span class="seal-text">Hi Mom, I\'ll be home by 6.</span><i class="caret dc"></i></div>'
            f'<div class="seal-bar">{sb("spark", "fix")}{sb("translate")}{sb("format_list_bulleted")}<span class="sp"></span>{sb("mic")}</div>'
            f'<div class="seal-offs">{offs}</div></div>'
            f'<div class="seal-pipe"><i class="pipe"></i><span class="packet">a7 f3 0c</span><span class="pipe-tag">{icon("lock", "ic sm")}<span>Encrypted</span></span></div>'
            f'<div class="seal-ai"><span class="ai-orb">{icon("spark", "ic sm")}</span>AI</div></div>')

    body = f"""
<section class="hero2" id="top"><div class="glow g1" data-depth="-.25"></div>
<div class="wrap hero2-in"><div class="hero2-copy">
<p class="kicker" data-reveal>The AI keyboard for Android</p>
<h1 data-type="hero">Type it.<br>Say it.<br><em>Get it right.</em></h1>
<p class="lede" data-reveal>SmarType fixes, translates and tidies your words, right where you type, in every app.</p>
<div class="cta" data-reveal>{play_button()}{soon_badge()}</div>
<p class="assure-link" data-reveal><a class="link" href="#how">See how it works</a></p>
<p class="assure" data-reveal>{icon("lock", "ic sm")}Typing stays on your phone. No account needed to type.</p></div>
<div class="hero2-art">{art("art_welcome", 480, eager=True)}</div></div></section>

<section class="story" id="how"><div class="glow g-story" data-depth=".3"></div>
<div class="wrap story-head"><p class="kicker" data-reveal>How it works</p><h2 data-type>Watch it <em>work.</em></h2></div>
<div class="wrap story-in"><ol class="accordion">{acc}</ol><div class="story-stage">{phone}</div></div></section>

<section class="tone" id="styles"><div class="glow g-tone" data-depth=".2"></div>
<div class="wrap"><p class="kicker" data-reveal>Styles</p><h2 data-type>Say it <em>your way.</em></h2>
<p class="lede" data-reveal>Same message, the tone you need. Pick from more than 20 styles, or write your own.</p>
<div class="tone-box" data-reveal><p class="tone-in"><span>You typed</span>can i take friday off? ill finish my work before</p>
<div class="tone-chips" role="group" aria-label="Writing styles"><span class="chip-pill" aria-hidden="true"></span>{tone_chips}</div>
<div class="tone-screen"><p class="tone-text"><span class="tone-words">{E(list(tones.values())[0])}</span><i class="caret dc" aria-hidden="true"></i></p></div></div>
</div></section>

<section class="stack" id="features"><div class="wrap"><p class="kicker" data-reveal>And more</p><h2 data-type>Everything <em>around it.</em></h2></div>
<div class="wrap cards">{card_html}<div class="stack-end" aria-hidden="true"></div></div></section>

<section class="vault" id="privacy"><div class="glow g3" data-depth=".25"></div>
<div class="wrap vault-grid"><div class="vault-copy"><p class="kicker" data-reveal>Privacy</p><h2 data-type>Private <em>by default.</em></h2>
<p class="lede" data-reveal>A keyboard sees everything you type. SmarType keeps typing on your phone, and sends text or voice audio only when you ask.</p>
<ol class="vows">{vow_html}</ol>
</div>
{seal}</div>
<div class="wrap"><div class="peek-note" data-reveal>{not_looking()}<div><h3>We don't know what you type. Honestly.</h3>
<p>Nothing in SmarType tracks your words. If you sign in, we keep your name, email and Google photo, so your free AI tries and Premium can follow you to a new phone. What you write, rewrite and almost send is your business, not ours. We never sell your data or use what you type for ads.</p>
<a class="link" href="/privacy.html">Read the privacy policy {icon("chevron_right", "ic sm")}</a> · <a class="link" href="/privacy-architecture.html">See the privacy architecture {icon("chevron_right", "ic sm")}</a></div></div></div></section>

<section class="closing2"><div class="glow g-close" data-depth=".2"></div>
<div class="wrap split"><div class="close-art" data-reveal>{art("art_signin", 320)}</div><div>
<h2 data-type>Try the AI <em>for free.</em></h2>
<p class="lede" data-reveal>Sign in with Google to get free AI tries for rewrite, translate, format and AI voice typing. Typing and suggestions work without an account.</p>
<div class="cta" data-reveal>{play_button()}{soon_badge()}</div></div></div>
</section>
"""
    scripts = "".join(f'<script src="{ver(f)}" defer></script>' for f in ("gsap.min.js", "ScrollTrigger.min.js", "home.js"))
    app = {"@type": "MobileApplication", "@id": SITE + "/#app", "name": "SmarType", "alternateName": "SmarType AI Keyboard",
           "operatingSystem": "Android 8.0+", "applicationCategory": "UtilitiesApplication", "applicationSubCategory": "Keyboard",
           "url": SITE + "/", "downloadUrl": PLAY_STORE_URL, "installUrl": PLAY_STORE_URL, "image": SITE + "/assets/og.png",
           "description": HOME_DESC, "inLanguage": "en", "isAccessibleForFree": True, "publisher": {"@id": SITE + "/#org"},
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
           "featureList": ["One-tap grammar fix and 22 rewrite styles", "AI translation into 31 languages, including " + ", ".join(INDIAN_TRANSLATE),
                           "AI voice typing with punctuation, up to 60 seconds", "Typing in English and Indian languages with a globe key",
                           "Quick Notes and clipboard on your phone", "AI, voice and learning off in password fields"]}
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "SmarType", "url": SITE + "/", "logo": SITE + "/assets/apple-touch-icon.png",
           "email": SUPPORT, "sameAs": [PLAY_STORE_URL]}
    site = {"@type": "WebSite", "@id": SITE + "/#site", "name": "SmarType", "url": SITE + "/", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"}}
    return page("index.html", "SmarType: AI Keyboard for Android – Grammar, Translate & Voice", HOME_DESC,
                body, extra=scripts, schema=[app, org, site])


def doc(name, title, description, h1, updated, sections):
    toc = "".join(f'<li><a href="#{E(sid)}">{E(t)}</a></li>' for sid, t, _ in sections)
    body = "".join(f'<section id="{E(sid)}"><h2>{E(t)}</h2>{content}</section>' for sid, t, content in sections)
    return page(name, title, description,
                f'<div class="wrap doc"><h1>{E(h1)}</h1><p class="meta">Last updated: {E(updated)}</p>'
                f'<nav class="toc" aria-label="On this page"><ol>{toc}</ol></nav>{body}</div>')


def privacy():
    s = [
        ("summary", "In short", "<ul><li>What you type stays on your phone. Suggestions are learned on the device.</li>"
         "<li>Text or voice audio is sent only when you ask for AI: Rewrite, Translate, Format, Notes AI, or voice typing.</li>"
         "<li>Nothing is learned or sent from password fields.</li>"
         "<li>If you sign in, we keep your Google account's ID, name, email, photo and sign-in dates, and how many AI tries you've used.</li>"
         "<li>We don't sell your data and we don't use what you type or say for advertising.</li></ul>"),
        ("typing", "What stays on your phone", "<p>Your keystrokes, glide trails, the words SmarType learns in memory for suggestions, your clipboard history and your Quick Notes text stay on your phone and are excluded from Android backup; your settings, custom styles, personal dictionary and custom themes (including any theme photo and installed keyboard extensions) also stay on your phone unless Android backup or device transfer is enabled on your phone (none are sent to SmarType's servers). "
         "Clipboard history masks items flagged sensitive by Android 13+ or copied/cut with SmarType in password or incognito fields, and periodically removes unpinned sensitive items older than 20 seconds by default. Uninstalling the app or clearing its data removes on-device data. "
         "See <a href=\"/privacy-architecture.html\">Privacy architecture</a> for a full diagram of these boundaries.</p>"),
        ("ai", "When you use AI", "<p>When you tap Rewrite, Translate or Format, or ask AI to change a note, the text you chose is sent over an encrypted connection to SmarType's server (Google Firebase), "
         "which sends it to an AI model provider (currently Google's Gemini) to produce the result and returns it to you.</p>"
         "<p>Voice typing: after you accept the voice notice and microphone permission, SmarType records up to 60 seconds of speech in memory while you dictate. "
         "If you cancel, the audio is deleted immediately on your phone. When you tap Check, the audio is sent over an encrypted connection to SmarType's server (Google Firebase) and Gemini to return clean text. "
         "When you're offline or out of free AI tries, the microphone switches to Android's system voice input when available (processed by that provider under its own privacy terms), or shows a notice in the keyboard.</p>"
         "<p>We use your text and voice audio only to produce that result. We don't store them after the request, and we don't use them to train models. "
         "Our AI provider processes them under its terms for API customers. We count each completed use against your free tries or plan.</p>"),
        ("account", "Your account", "<p>Signing in is optional. If you sign in with Google, we store your account ID, name, email address, profile photo, and when you created the account and last signed in. "
         "We use them to give you free AI tries, keep Premium on all your phones and help you if you contact us.</p>"),
        ("payments", "Payments", "<p>Premium is bought through Google Play. Google handles payment details; we receive only whether your subscription is active and when it renews.</p>"),
        ("device", "Keeping the service safe", "<p>To stop abuse of the AI service, the app uses Firebase App Check with Google Play Integrity, which confirms requests come from a real copy of the app on a real device.</p>"),
        ("analytics", "Usage analytics", "<p>The app includes Google Analytics for Firebase, which collects basic, non-content information such as app opens, device model, Android version and approximate country. "
         "It never receives what you type or dictate.</p>"),
        ("sharing", "Who we share data with", "<p>Only the service providers that run SmarType: Google (Firebase, Gemini, Google Play). "
         "We don't sell personal data. We may disclose data if the law requires it.</p>"),
        ("choices", "Your choices", "<ul><li>Use SmarType without signing in: typing and on-device suggestions work without an account.</li>"
         "<li>Turn off clipboard history in Settings, or reset the voice typing notice in SmarType AI settings.</li>"
         f"<li>Delete your SmarType account and its data: email <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a> from the Google address you signed in with. "
         "Within 30 days we delete your account ID, name, email address, profile photo, sign-in dates, AI usage count and subscription status from our servers. "
         "Google Play keeps its own purchase records under Google's terms, and data stored only on your phone stays there until you clear app data or uninstall SmarType.</li></ul>"),
        ("children", "Children", "<p>SmarType isn't directed at children under 13 and we don't knowingly collect their data.</p>"),
        ("changes", "Changes and contact", f"<p>We'll update this page when how we handle data changes, and change the date at the top. Questions: <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a>.</p>"),
    ]
    return doc("privacy.html", "Privacy policy · SmarType", "How SmarType handles your data: typing stays on your phone; text or voice audio is sent only when you use AI.",
               "Privacy policy", "18 November 2026", s)


def terms():
    s = [
        ("about", "About these terms", "<p>These terms apply when you use the SmarType keyboard app and its AI features. By using SmarType you agree to them.</p>"),
        ("use", "Using SmarType", "<p>Use SmarType lawfully and don't try to misuse or overload the AI service, get around limits or copy the app.</p>"),
        ("ai", "AI results", "<p>AI suggestions can be wrong or unsuitable. Read them before you send. You're responsible for what you send.</p>"),
        ("tries", "Free tries and Premium", "<p>Signed-in users get a number of free AI tries; this number can change. Premium is a subscription sold through Google Play; "
         "Google Play's terms cover billing, renewals, cancellations and refunds. You can cancel any time in Google Play.</p>"),
        ("content", "Your content", "<p>What you write or dictate stays yours. You give us only the permission needed to process text or voice audio you send to AI and return the result.</p>"),
        ("availability", "Availability", "<p>We work to keep SmarType running, but features can change and the AI service can be unavailable at times.</p>"),
        ("liability", "Liability", "<p>To the extent the law allows, SmarType is provided as is, and we aren't liable for indirect losses from using it.</p>"),
        ("changes", "Changes and contact", f"<p>We may update these terms and will change the date at the top. Questions: <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a>.</p>"),
    ]
    return doc("terms.html", "Terms · SmarType", "The terms for using the SmarType keyboard and its AI features.", "Terms of use", "18 November 2026", s)


FAQ = [
    ("Getting started", [
        ("Is SmarType on iPhone?", "Not yet. SmarType is on Google Play for Android 8.0 and later, and the iPhone app is coming soon to the App Store."),
        ("How do I turn on SmarType?", "Open SmarType and follow the two steps: allow it in Android's keyboard settings, then choose it as your keyboard. The app moves on by itself when each step is done."),
        ("How do I switch back to my old keyboard?", "Long-press the globe key, or tap the keyboard icon in the navigation bar, and pick another keyboard."),
        ("Do I need an account?", "No. Typing and suggestions work without one. Sign in with Google if you want AI features (Rewrite, Translate, Format, Notes AI and AI voice typing) or Premium."),
    ]),
    ("AI features", [
        ("What happens to the text or voice audio I send to AI?", "It goes over an encrypted connection to our server and our AI provider only to produce your result, and isn't stored after the request. See the privacy policy."),
        ("How many free tries do I get?", "Signed-in users get a set number of free AI tries; the app shows how many are left. Premium removes the limit."),
        ("Why doesn't AI work in password fields?", "On purpose: SmarType never sends or learns anything typed in a password field."),
    ]),
    ("Languages and voice", [
        ("Which languages can I type in?", "English, Hindi, Telugu, Tamil, Bengali, Urdu and many more. Add one in Languages and English stays in the list, so the globe key switches between English and your language."),
        ("Which languages can Translate write in?", TRANSLATE_FAQ),
        ("How do I keep my languages in Translate?", "Open Translate, tap More, search for a language and add it. Added languages show as chips next to English, so they are one tap away next time."),
        ("What happens if I pause while speaking?", "Nothing: SmarType keeps listening and shows Still listening. Recording ends only when you tap Check, tap Delete or reach 60 seconds."),
        ("Does voice typing send my audio?", "SmarType sends audio only when you use SmarType AI voice typing and tap Check. SmarType records up to 60 seconds in memory, deletes the audio immediately if you cancel, and sends it over an encrypted connection to our server and Gemini only to return your text — it isn't stored after the request. When you're offline or out of free tries, SmarType switches to Android's system voice input when available (handled by that voice provider under its own privacy terms without SmarType's Check step), or shows a notice in the keyboard."),
    ]),
    ("Account and data", [
        ("How do I delete my account?", f"Write to {SUPPORT} from your Google sign-in email address. Within 30 days we delete your SmarType account profile, AI usage count and subscription status from our servers."),
        ("How do I cancel Premium?", "In Google Play: Profile → Payments and subscriptions → Subscriptions → SmarType → Cancel."),
    ]),
]


def help_page():
    groups = "".join(f'<section><h2>{E(g)}</h2>' + "".join(
        f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items) + "</section>" for g, items in FAQ)
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                              for _, items in FAQ for q, a in items]}
    return page("help.html", "Help · SmarType", "Answers about setting up SmarType, AI rewrite and translate, Indian languages, voice typing and your account.",
                schema=[faq, crumbs("help.html", "Help")], body=
                f'<div class="wrap doc"><h1>Help</h1><p class="lede">Quick answers. Still stuck? <a href="/contact.html">Contact us</a>.</p>{groups}</div>')


def contact():
    return page("contact.html", "Contact · SmarType", "How to reach SmarType.",
                f'<div class="wrap doc contact">{art("art_done", 200)}<h1>Contact us</h1>'
                f'<p class="lede">Questions, feedback or a problem? Write to <a href="mailto:{SUPPORT}">{SUPPORT}</a>. We usually reply within two working days.</p>'
                '<p>To delete your account, write from the email address you sign in with. For billing, Google Play handles payments and refunds.</p></div>')


def compare():
    rows = [
        ("One-tap tone rewrite", "22 built-in styles (Polite, Professional, Casual, Simple, Empathetic, Firm and more) + custom styles; pin up to 4 chips on any Android 8.0+ phone.",
         "Proofread and Writing Tools depend on supported Pixel or Gemini devices.", "Copilot tone rewrite inside the toolbar.", "English grammar and tone suggestions."),
        ("Indian typing &amp; AI translation", "Globe-key typing in English, Hindi, Telugu, Tamil, Bengali and 50+ layouts; one-tap AI translation into 31 languages, including Hindi, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia and Urdu.",
         "Broad Indic layouts and Google Translate bar.", "Indic layouts and Microsoft Translator bar.", "English writing assistant; uses layouts from your existing keyboard without built-in Indic AI translation."),
        ("Voice typing cleanup", "Records up to 60 seconds in memory; adds punctuation and trims filler words on Check; instant delete on cancel; system voice fallback offline.",
         "Fast speech-to-text; assistant punctuation varies by phone.", "Uses voice input without 60-second Check cleanup.", "No built-in AI voice cleanup recorder."),
        ("Quick Notes scratchpad", "In-keyboard notes panel plus a movable floating note window over any app, with optional AI polish.",
         "Clipboard history only; no scratchpad.", "Clipboard pins and to-do integration; no floating note window.", "No built-in scratchpad."),
        ("Password-field privacy", "Turns off AI actions and AI voice dictation in password and incognito fields; password fields also turn off composing, autocorrect, glide typing and the microphone button; verified editor ranges only.",
         "Suppresses predictions in password fields.", "Suppresses predictions in password fields.", "Pauses checks in sensitive fields."),
    ]
    trs = "".join(f'<tr><th scope="row">{r[0]}</th><td class="st-col">{E(r[1])}</td><td>{E(r[2])}</td><td>{E(r[3])}</td><td>{E(r[4])}</td></tr>' for r in rows)
    pillars = [
        ("spark", "Polite message rewrite in one tap", "Pick Grammar fix, Polite, Professional, Casual, Simple or any of 22 built-in styles — or write your own custom style and pin up to 4 chips on the top bar."),
        ("translate", "Indian-language typing + 31-language AI translation", "Switch between English, Hindi, Telugu, Tamil, Bengali and 50+ keyboard layouts with the globe key. Tap Translate to send messages in 11 Indian languages, English and 19 more, inside WhatsApp or Gmail. Add the languages you use as one-tap chips."),
        ("mic", "Voice typing punctuation and cleanup", "Speak for up to 60 seconds in memory and tap Check for punctuated text. Cancel deletes the audio immediately. Offline or out of tries, SmarType switches to Android system voice input."),
        ("sticky_note_2", "Quick Notes in and over any app", "Keep a scratchpad inside the keyboard or float a movable Quick Notes window above chats, browsers and forms, with one-tap AI polish and undo."),
        ("lock", "Strict password and everyday privacy", 'Everyday keystrokes stay on your phone without an account. Password and incognito fields shut off AI and voice dictation, and password fields also turn off autocorrect and the mic button. Read <a href="/privacy-architecture.html">what stays on your phone</a>.'),
    ]
    cards = "".join(f'<article class="arch-card"><div class="arch-ic">{icon(ic)}</div><h3>{E(t)}</h3><p>{d}</p></article>' for ic, t, d in pillars)
    body = (f'<div class="wrap page-wide"><p class="kicker">Android keyboard comparison</p>'
            '<h1>SmarType vs Gboard vs SwiftKey vs Grammarly: the best AI keyboard for Android?</h1>'
            '<p class="lede">Gboard and SwiftKey handle everyday typing; Grammarly adds an Android writing assistant alongside your keyboard. SmarType combines one-tap polite tone rewrite, AI translation into 11 Indian languages, 60-second voice cleanup, Quick Notes and on-device everyday typing in one keyboard.</p>'
            f'<div class="cta">{play_button()}<a class="btn key alt" href="/privacy-architecture.html">Privacy architecture</a></div>'
            '<div class="cmp-scroll" tabindex="0" role="region" aria-label="Android keyboard comparison"><table class="cmp-table"><thead><tr><th scope="col">Capability</th><th scope="col" class="st-col">SmarType</th>'
            f'<th scope="col">Gboard</th><th scope="col">SwiftKey</th><th scope="col">Grammarly Android assistant</th></tr></thead><tbody>{trs}</tbody></table></div>'
            f'<h2>Five differences that matter every day</h2><div class="arch-grid">{cards}</div>'
            '<div class="cta-strip"><div><h2>Try SmarType free on Android 8.0+</h2><p>Typing and suggestions need no account. Sign in with Google when you want free AI tries.</p></div>'
            f'{play_button()}</div></div>')
    return page("compare.html", "Best AI Keyboard for Android: SmarType vs Gboard, SwiftKey, Grammarly",
                "Compare SmarType, Gboard, SwiftKey and Grammarly on tone rewrite, AI translation into Hindi, Telugu, Tamil and more, voice punctuation, Quick Notes and privacy.", body)


TYPED = {"hi", "te", "ta", "bn", "ur"}  # languages with a typing layout in the app; the rest are Translate only
TYPING_LANGS = [("हिन्दी", "Hindi", "hi"), ("తెలుగు", "Telugu", "te"), ("தமிழ்", "Tamil", "ta"), ("বাংলা", "Bengali", "bn"),
                ("मराठी", "Marathi", "mr"), ("ಕನ್ನಡ", "Kannada", "kn"), ("മലയാളം", "Malayalam", "ml"), ("ગુજરાતી", "Gujarati", "gu"),
                ("ਪੰਜਾਬੀ", "Punjabi", "pa"), ("ଓଡ଼ିଆ", "Odia", "or"), ("اردو", "Urdu", "ur")]


def languages_page():
    """Landing page for people searching for a keyboard in their language (Hindi keyboard, Telugu keyboard...)."""
    tiles = "".join(f'<article class="arch-card"><h3 lang="{c}">{E(n)}</h3><p>{E(en) + " keyboard · " if c in TYPED else ""}Translate to and from {E(en)}</p></article>'
                    for n, en, c in TYPING_LANGS)
    qa = [("Is SmarType a Hindi keyboard?", "Yes. Add Hindi in Languages and type in Hindi, with English kept beside it. The globe key switches between them, and Translate turns an English message into Hindi in one tap."),
          ("Can I type in Telugu, Tamil, Bengali or Urdu?", "Yes. Add any of them in Languages. English stays in the list, so you switch with the globe key. Marathi, Kannada, Malayalam, Gujarati, Punjabi and Odia are available in Translate."),
          ("Does Translate work from English to Hindi and other Indian languages?", "Yes. Translate writes in " + ", ".join(INDIAN_TRANSLATE) + ", English and 19 more languages. It detects the language you typed in."),
          ("Can I speak in Hindi and get text?", "Yes. Tap the mic and speak in Hindi, English or a mix; SmarType writes it up with punctuation when you tap Check."),
          ("Is it free?", "Typing in every language is free and needs no account. Sign in with Google for free AI tries for Translate, Rewrite and voice typing; Premium removes the limit.")]
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    body = ('<div class="wrap page-wide"><p class="kicker">Indian language keyboard</p>'
            '<h1>Hindi, Telugu, Tamil and more: an AI keyboard for Indian languages</h1>'
            '<p class="lede">Type in your language, switch to English with one key, and translate English to Hindi, Telugu, Tamil or 8 more Indian languages right inside WhatsApp, Instagram or Gmail.</p>'
            f'<div class="cta">{play_button()}{soon_badge()}</div>'
            f'<h2>11 Indian languages in Translate, 5 with a keyboard</h2><div class="arch-grid">{tiles}</div>'
            '<h2>Questions</h2><div class="doc-inline">' + "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in qa) + '</div>'
            '<div class="cta-strip"><div><h2>Get the Indian language AI keyboard</h2><p>Free on Android 8.0+. No account needed to type.</p></div>'
            f'{play_button()}</div></div>')
    return page("languages.html", "Hindi, Telugu & Tamil Keyboard with AI Translate · SmarType",
                "AI keyboard for Indian languages: type in Hindi, Telugu, Tamil, Bengali, Marathi, Kannada and more, switch to English in one tap, and translate English to Hindi instantly.",
                body, schema=[faq, crumbs("languages.html", "Indian languages")])


def privacy_architecture():
    zones = [
        ("keyboard", "1 · Stays on your phone", "Local keyboard storage",
         ["Everyday keystrokes, glide trails and in-memory learned word suggestions stay on your device; settings, custom styles, personal dictionary and custom themes (including any theme photo and installed keyboard extensions) also stay local unless Android backup or device transfer is enabled on your phone (never sent to SmarType's servers).",
          "Clipboard history (masking items flagged sensitive by Android 13+ or copied/cut with SmarType in password or incognito fields, and periodically removing unpinned sensitive items older than 20 seconds by default) and Quick Notes text stay on your phone and are excluded from Android backup.",
          "Everyday typing and suggestions work without an account."]),
        ("lock", "2 · Password &amp; incognito shutoff", "Automatic hard lock",
         ["Password and incognito fields turn off AI actions and AI voice dictation.",
          "Password fields also turn off composing, autocorrect and glide typing, and disable the password-row microphone so speech capture cannot start.",
          "Editor updates replace only verified text ranges — never blind select-all deletion."]),
        ("spark", "3 · Explicit AI tap only", "Encrypted ephemeral request",
         ["Text leaves the phone over HTTPS only when you tap Rewrite, Translate, Format or Notes AI.",
          "Voice typing holds up to 60 seconds in memory; Cancel deletes it immediately, and Check sends it encrypted to Google Firebase and Gemini.",
          "Firebase App Check with Google Play Integrity guards the service. We do not store prompts or audio after the request, and we do not use them to train models."]),
    ]
    zhtml = "".join(
        f'<article class="arch-card"><span class="arch-tag">{tag}</span><div class="arch-ic">{icon(ic)}</div><h3>{E(t)}</h3>'
        + "<ul>" + "".join(f"<li>{E(li)}</li>" for li in items) + "</ul></article>" for ic, tag, t, items in zones
    )
    body = (f'<div class="wrap page-wide"><p class="kicker">Privacy architecture</p>'
            '<h1>What stays on your phone — and what leaves when you tap AI</h1>'
            '<p class="lede">SmarType separates local everyday typing from optional AI requests so your keystrokes, passwords and private notes stay under your control.</p>'
            f'<div class="cta">{play_button()}<a class="btn key alt" href="/privacy.html#choices">Data &amp; deletion choices</a></div>'
            f'<h2>Three privacy boundaries</h2><div class="arch-grid">{zhtml}</div>'
            '<section class="doc-inline"><h2>Optional Google sign-in and system voice fallback</h2>'
            '<p>You can type without signing in. If you sign in with Google for free AI tries or Premium (sold through Google Play), SmarType stores only your account ID, name, email, photo, sign-in dates, AI try count and subscription status. '
            'When your phone is offline or out of AI tries, tapping the microphone switches to Android system voice input when available under that provider\'s privacy terms. '
            'Read the full <a href="/privacy.html">Privacy policy</a> or manage account deletion at <a href="/privacy.html#choices">Your choices</a>.</p></section>'
            '<div class="cta-strip"><div><h2>Private Android AI keyboard</h2><p>Install SmarType from Google Play and start typing without an account.</p></div>'
            f'{play_button()}</div></div>')
    return page("privacy-architecture.html", "Privacy architecture · What stays on your phone · SmarType",
                "How SmarType keeps keystrokes, clipboard items and Quick Notes on your phone, locks down password fields, and sends text or voice only when you tap AI.", body)


MICRO_TOOLS_META = (
    ("polite-whatsapp-rewriter.html", "spark", "Polite WhatsApp rewriter",
     "Preview Polite, Professional, Empathetic and Firm replies for real chat situations."),
    ("ai-tone-translator.html", "translate", "AI tone translator (21 languages)",
     "Switch English to Hindi, English to Spanish, Arabic to English and French to English with register control."),
    ("rough-notes-to-neat-list.html", "format_list_bulleted", "Rough-notes-to-neat-list",
     "Turn comma-separated or line-separated jottings into bullets, numbered steps, checklists or tables in your browser."),
)


def tool_btn_row(items, key, cls, attr, label):
    btns = "".join(f'<button type="button" class="{cls}{" on" if i == 0 else ""}" aria-pressed="{"true" if i == 0 else "false"}">{E(it[key])}</button>' for i, it in enumerate(items))
    return f'<div class="tool-row" role="group" aria-label="{E(label)}" {attr}>{btns}</div>'


def micro_tool_page(fname, title, desc, kicker, h1, lede, card_inner, strip_h2, strip_p, data_obj):
    others = [
        f'<article class="arch-card"><div class="arch-ic">{icon(ic)}</div><h3><a href="/{slug}">{E(name)}</a></h3><p>{E(blurb)}</p></article>'
        for slug, ic, name, blurb in MICRO_TOOLS_META if slug != fname
    ]
    others.append(
        f'<article class="arch-card"><div class="arch-ic">{icon("lock")}</div><h3><a href="/privacy-architecture.html">On-device privacy boundary</a></h3>'
        '<p>See what stays on your phone and how SmarType shuts off AI in password and incognito fields.</p></article>'
    )
    payload_json = json.dumps(data_obj, ensure_ascii=False).replace("</", "<\\/")
    body = (
        f'<div class="wrap page-wide"><p class="kicker">{E(kicker)}</p><h1>{E(h1)}</h1><p class="lede">{E(lede)}</p>'
        f'{card_inner}<h2>Explore more free SmarType web tools</h2><div class="arch-grid">{"".join(others)}</div>'
        f'<div class="cta-strip"><div><h2>{E(strip_h2)}</h2><p>{E(strip_p)}</p></div>{play_button()}</div></div>'
    )
    extra = f'<script id="tool-data" type="application/json">{payload_json}</script><script src="{ver("tools.js")}" defer></script>'
    return page(fname, title, desc, body, extra)


def preset_tool_card(groups, step_labels, src_label, dock_html, note_text):
    g0 = groups[0]
    p0 = g0["presets"][0]
    t0 = p0["tones"][0]
    sub = t0.get("sub", "")
    group_html = f'<span class="tool-label">{E(step_labels[0])}</span>{tool_btn_row(groups, "label", "tool-tab", "data-group-row", step_labels[0])}' if len(groups) > 1 else ""
    p_label, t_label = step_labels[-2], step_labels[-1]
    return (
        f'<div class="tool-card" data-tool="presets">{group_html}'
        f'<span class="tool-label">{E(p_label)}</span>{tool_btn_row(g0["presets"], "label", "tool-tab", "data-preset-row", p_label)}'
        f'<span class="tool-label">{E(src_label)}</span><div class="tool-src" data-source dir="{g0.get("dir", "ltr")}" lang="{g0.get("lang", "en")}">{E(p0["raw"])}</div>'
        f'<span class="tool-label">{E(t_label)}</span>{tool_btn_row(p0["tones"], "name", "tool-chip", "data-tone-row", t_label)}'
        f'<div class="tool-res" aria-live="polite"><div class="tool-res-head"><span class="tool-badge" data-badge>{E(t0["name"])} result</span>'
        f'<button type="button" class="tool-copy" data-copy>{icon("content_copy")}<span data-copy-label>Copy</span></button></div>'
        f'<p class="tool-out" data-output lang="{g0.get("outLang", "en")}">{E(t0["out"])}</p><p class="tool-sub" data-sub{" hidden" if not sub else ""}>{E(sub)}</p></div>'
        f'<div class="tool-dock"><p>{dock_html}</p>{play_button()}</div>'
        f'<p class="tool-note">{icon("lock")}<span>{E(note_text)}</span></p></div>'
    )


def polite_whatsapp_rewriter():
    presets = [
        {"label": "Ask Friday off", "raw": "can i take friday off? ill finish my work before", "tones": [
            {"name": "Polite", "out": "Hi! Would it be alright if I took Friday off? I will finish all of my pending tasks before Thursday evening."},
            {"name": "Professional", "out": "I would like to request leave this Friday. All current deliverables will be completed beforehand."},
            {"name": "Empathetic", "out": "I know the team has a busy week — would Friday off still work if I wrap up everything on my plate by Thursday?"},
            {"name": "Firm", "out": "I am taking Friday off and will hand over my completed tasks by Thursday afternoon."},
        ]},
        {"label": "Pending invoice", "raw": "you still havent paid last weeks invoice, send today", "tones": [
            {"name": "Polite", "out": "Hi Priya, hope your week is going well! Just checking in on last week's invoice — could you let me know when the transfer is planned?"},
            {"name": "Professional", "out": "Hello Priya, following up on last week's invoice. Please share an update on the payment schedule today."},
            {"name": "Empathetic", "out": "Hi Priya, I know schedules get busy! Whenever you have a moment today, could you check on last week's open invoice?"},
            {"name": "Firm", "out": "Hello Priya, last week's invoice remains unpaid. Please complete the transfer today and send confirmation."},
        ]},
        {"label": "Decline weekend call", "raw": "cant do saturday call im with family, monday morning works", "tones": [
            {"name": "Polite", "out": "Thanks for reaching out! I am with family on Saturday, so could we speak on Monday morning instead?"},
            {"name": "Professional", "out": "I am unavailable for a call on Saturday. Let us schedule this for Monday morning."},
            {"name": "Empathetic", "out": "I want to give our chat proper attention, and Saturday is family time on my side — does Monday morning work for you?"},
            {"name": "Firm", "out": "I do not take calls on Saturdays. Let us connect on Monday morning at 10 AM."},
        ]},
        {"label": "Late rent update", "raw": "hey priya rent will be 2 days late bank transfer stuck", "tones": [
            {"name": "Polite", "out": "Hi Priya, wanted to let you know early that my bank transfer is delayed, so rent will reach you in two days. Sorry for the wait!"},
            {"name": "Professional", "out": "Hello Priya, please note that this month's rent transfer is delayed at my bank and will clear within two days."},
            {"name": "Empathetic", "out": "Hi Priya, I want to keep you updated right away — my bank transfer got held up, and the rent will arrive in two days. Thank you for your patience."},
            {"name": "Firm", "out": "Hello Priya, my bank transfer is processing and the full rent will land within two days. I will share the receipt once it clears."},
        ]},
    ]
    card = preset_tool_card(
        [{"presets": presets}], ("1. Pick a real WhatsApp draft", "2. Tap a SmarType tone chip"), "Rough draft",
        "<strong>Stop copying between tabs.</strong> Rewrite any WhatsApp, Gmail or Slack draft in one tap with 22 built-in styles and 4 pinned Smartbar chips on Android.",
        "Runs 100% in your browser tab. Zero text is sent to any server.",
    )
    return micro_tool_page(
        "polite-whatsapp-rewriter.html", "Polite WhatsApp message rewriter · SmarType",
        "Free browser preview of SmarType's polite WhatsApp message rewriter across Polite, Professional, Empathetic and Firm tones.",
        "Free WhatsApp tone tool", "Polite WhatsApp message rewriter",
        "See how SmarType turns blunt chat drafts into Polite, Professional, Empathetic or Firm replies — then rewrite your own messages directly inside WhatsApp on Android.",
        card, "Use all 22 rewrite styles inside your Android keyboard",
        "Pin your 4 go-to tone chips on the Smartbar and rewrite messages without leaving WhatsApp.", {"presets": presets},
    )


def ai_tone_translator():
    groups = [
        {"label": "English → Hindi (हिन्दी)", "dir": "ltr", "lang": "en", "outLang": "hi", "presets": [
            {"label": "Running 10 mins late", "raw": "I am stuck in traffic, I will reach in 10 minutes.", "tones": [
                {"name": "Respectful (आप)", "out": "मैं ट्रैफ़िक में फँसा हूँ, बस 10 मिनट में पहुँच जाऊँगा। कृपया चिंता न करें।", "sub": "Main traffic mein phansa hoon, bas 10 minute mein pahunch jaaunga. Kripya chinta na karein."},
                {"name": "Warm (तुम)", "out": "थोड़ा ट्रैफ़िक मिल गया है, बस 10 मिनट में पहुँच रहा हूँ।", "sub": "Thoda traffic mil gaya hai, bas 10 minute mein pahunch raha hoon."},
                {"name": "Formal Hindi", "out": "यातायात अधिक होने के कारण मुझे लगभग 10 मिनट का विलंब होगा।", "sub": "Yaatayaat adhik hone ke kaaran mujhe lagbhag 10 minute ka vilamb hoga."},
            ]},
            {"label": "Send address before 5 PM", "raw": "Great! Can you send me the address before 5 PM?", "tones": [
                {"name": "Respectful (आप)", "out": "बहुत बढ़िया! क्या आप शाम 5 बजे से पहले मुझे पता भेज सकते हैं?", "sub": "Bahut badhiya! Kya aap shaam 5 baje se pehle mujhe pata bhej sakte hain?"},
                {"name": "Warm (तुम)", "out": "बढ़िया! क्या तुम शाम 5 बजे से पहले पता भेज सकते हो?", "sub": "Badhiya! Kya tum shaam 5 baje se pehle pata bhej sakte ho?"},
                {"name": "Formal Hindi", "out": "धन्यवाद। कृपया शाम 5 बजे से पूर्व पूरा पता साझा करें।", "sub": "Dhanyavaad. Kripya shaam 5 baje se poorv poora pata saajha karein."},
            ]},
        ]},
        {"label": "English → Spanish (Español)", "dir": "ltr", "lang": "en", "outLang": "es", "presets": [
            {"label": "Move tomorrow's meeting", "raw": "Could we move tomorrow's meeting to 3 PM? A client visit came up.", "tones": [
                {"name": "Polite (usted)", "out": "¿Podríamos pasar la reunión de mañana a las 3 p. m.? Surgió una visita con un cliente.", "sub": "Respectful usted register for clients and new contacts."},
                {"name": "Casual (tú)", "out": "Oye, ¿podemos mover la reunión de mañana a las 3 p. m.? Me salió una visita con un cliente.", "sub": "Relaxed tú register for teammates you know well."},
                {"name": "Professional", "out": "Le agradecería reprogramar nuestra reunión de mañana para las 15:00 debido a una visita con un cliente.", "sub": "Formal workplace Spanish."},
            ]},
            {"label": "Confirm hotel check-in", "raw": "Our flight lands late tonight. Please hold our reservation.", "tones": [
                {"name": "Polite (usted)", "out": "Nuestro vuelo aterriza tarde esta noche. ¿Podrían mantener nuestra reserva, por favor?", "sub": "Courteous hospitality request."},
                {"name": "Casual (tú)", "out": "Nuestro vuelo llega tarde esta noche, ¿nos guardas la reserva por favor?", "sub": "Everyday host chat."},
                {"name": "Professional", "out": "Les informamos que nuestro vuelo llegará tarde esta noche; agradecemos que mantengan activa nuestra reserva.", "sub": "Clear written notice."},
            ]},
        ]},
        {"label": "Arabic → English (العربية)", "dir": "rtl", "lang": "ar", "outLang": "en", "presets": [
            {"label": "Send meeting summary", "raw": "شكراً جزيلاً على وقتكم اليوم، سأرسل الملخص قبل المساء.", "tones": [
                {"name": "Polite", "out": "Thank you very much for your time today! I will send over the summary before this evening.", "sub": "Natural courteous English from Arabic source text."},
                {"name": "Professional", "out": "Thank you for meeting today. I will share the written summary before the end of the day.", "sub": "Clear workplace follow-up."},
                {"name": "Simple", "out": "Thanks for your time today. I will send the summary before evening.", "sub": "Short plain-English phrasing."},
            ]},
            {"label": "Confirm delivery time", "raw": "هل يمكن توصيل الطلب غداً بعد الساعة الثانية ظهراً؟", "tones": [
                {"name": "Polite", "out": "Could you please deliver the order tomorrow after 2 PM?", "sub": "Polite customer request."},
                {"name": "Professional", "out": "Please schedule the delivery for tomorrow after 2:00 PM.", "sub": "Direct scheduling instruction."},
                {"name": "Simple", "out": "Can the order arrive tomorrow after 2 PM?", "sub": "Everyday chat question."},
            ]},
        ]},
        {"label": "French → English (Français)", "dir": "ltr", "lang": "fr", "outLang": "en", "presets": [
            {"label": "Train held up", "raw": "Désolé pour le retard, le train est resté bloqué dix minutes.", "tones": [
                {"name": "Polite", "out": "So sorry for the delay — my train was held up for ten minutes, and I am on my way now.", "sub": "Warm polite English."},
                {"name": "Professional", "out": "Apologies for the delay. My train was held for ten minutes, and I will join shortly.", "sub": "Work-ready update."},
                {"name": "Casual", "out": "Sorry I am running late! The train got stuck for ten minutes.", "sub": "Quick chat message."},
            ]},
        ]},
    ]
    card = preset_tool_card(
        groups, ("1. Choose a language pair", "2. Pick a message", "3. Select tone & register"), "Source message",
        "<strong>Translate while you type.</strong> SmarType auto-detects your draft and translates into Hindi, Spanish, English, Arabic, French and 16 more languages right inside any Android app.",
        "Runs 100% in your browser tab. On Android, SmarType translates across 21 target languages and types natively in 50+ keyboard layouts (including English, Hindi, Telugu and Tamil).",
    )
    return micro_tool_page(
        "ai-tone-translator.html", "AI tone translator — English-to-Hindi, Spanish & Arabic to English · SmarType",
        "Preview English-to-Hindi, English-to-Spanish, Arabic-to-English and French-to-English tone translations, powered on Android by SmarType's 21-language keyboard.",
        "21-language AI keyboard preview", "AI tone translator for Hindi, Spanish, Arabic & 21 languages",
        "Try our English-to-Hindi tone translator alongside English-to-Spanish, Arabic-to-English and French-to-English examples — then translate live inside any Android app.",
        card, "Translate across 21 languages without leaving your chat",
        "Auto-detect any source message and replace it in place from your Android keyboard.", {"groups": groups},
    )


def rough_notes_to_neat_list():
    presets = [
        {"label": "Trip packing", "raw": "book flight tickets, 2 nights hotel near metro, cab from airport, dinner with priya sat"},
        {"label": "Standup notes", "raw": "fixed login timeout; updated hindi strings; review release checklist; check play console"},
        {"label": "Key-value plan", "raw": "Flight: AI-102 at 9 AM\nHotel - 2 nights near metro\nPickup: Priya at Gate 4"},
    ]
    modes = [{"id": "bullets", "name": "Bullet points"}, {"id": "numbered", "name": "Numbered list"}, {"id": "checklist", "name": "Checklist"}, {"id": "table", "name": "Table"}]
    default_out = "• Book flight tickets\n• 2 nights hotel near metro\n• Cab from airport\n• Dinner with priya sat"
    card = (
        f'<div class="tool-card" data-tool="notes"><span class="tool-label">Load a sample or type your own</span>{tool_btn_row(presets, "label", "tool-tab", "data-preset-row", "Load a sample or type your own")}'
        '<label class="tool-label" for="notes-input">Your rough notes (stays in this browser tab)</label>'
        f'<textarea id="notes-input" class="tool-input" data-notes-input maxlength="2000">{E(presets[0]["raw"])}</textarea>'
        f'<span class="tool-label">Output format</span>{tool_btn_row(modes, "name", "tool-chip", "data-mode-row", "Output format")}'
        f'<div class="tool-res" aria-live="polite"><div class="tool-res-head"><span class="tool-badge" data-badge>Bullet points result</span>'
        f'<button type="button" class="tool-copy" data-copy>{icon("content_copy")}<span data-copy-label>Copy</span></button></div>'
        f'<p class="tool-out" data-output data-empty="false">{E(default_out)}</p></div>'
        '<div class="tool-dock"><p><strong>Format notes inside any Android app.</strong> SmarType\'s Format panel and floating Quick Notes turn rough jottings into bullet lists, summaries and tables right above your keys.</p>'
        f'{play_button()}</div><p class="tool-note">{icon("lock")}<span>Formats 100% locally in your browser memory — zero network calls and zero saved text.</span></p></div>'
    )
    return micro_tool_page(
        "rough-notes-to-neat-list.html", "Rough-notes-to-neat-list formatter · SmarType",
        "Paste comma-separated or line-separated rough notes to format clean bullet points, numbered steps, checklists or tables locally in your browser.",
        "Instant browser formatter", "Rough-notes-to-neat-list formatter",
        "Paste comma-separated, semicolon-separated or line-by-line jottings below to turn them into clean bullets, numbered steps, a checklist or a two-column table.",
        card, "Keep Quick Notes and one-tap Format on your Android keyboard",
        "Jot thoughts in a floating Quick Notes window over any app and format lists in a single tap.", {"presets": presets, "modes": modes},
    )


def notfound():
    return page("404.html", "Page not found · SmarType", "This page doesn't exist.",
                f'<div class="wrap doc contact">{art("art_empty_notes", 200)}<h1>Page not found</h1><p class="lede"><a href="/">Go to the home page</a>.</p></div>')


def robots_txt():
    bots = ("*", "Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "ClaudeBot", "PerplexityBot", "Applebot-Extended")
    rules = "\n\n".join(f"User-agent: {b}\nAllow: /" for b in bots)
    return f"{rules}\n\nSitemap: https://smartype.in/sitemap.xml\n"


def sitemap_xml(pages):
    urls = "".join(
        f"<url><loc>https://smartype.in/{p.replace('.html', '') if p != 'index.html' else ''}</loc><lastmod>{UPDATED}</lastmod></url>"
        for p in pages if p != "404.html"
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def llms_txt():
    return f"""# SmarType

> SmarType is a private Android AI keyboard (Android 8.0+, package `bha.keys.smartype`) with one-tap polite tone rewrite, AI translation into 31 languages including 11 Indian languages, 60-second voice typing cleanup with punctuation, and Quick Notes.

- Google Play listing: {PLAY_STORE_URL}
- Support: mailto:{SUPPORT}

## Key Facts

- **One-tap tone rewrite:** 22 built-in styles (Grammar fix, Polite, Professional, Casual, Simple, Empathetic, Firm, and 15 more) plus custom styles, with up to 4 pinned chips on the top bar.
- **Indian typing and 31-language AI translation:** Globe-key typing across English, Hindi, Telugu, Tamil, Bengali, Urdu, and 50+ layouts. In-keyboard AI Translate auto-detects source text and outputs 31 languages: {LLMS_TRANSLATE}. Users add the languages they use as one-tap chips; English is always offered.
- **Voice typing cleanup:** Records up to 60 seconds in memory and keeps listening through pauses; Check adds punctuation and cleans up filler words, Cancel deletes the audio immediately, and Android system voice input serves as the offline or out-of-tries fallback.
- **Quick Notes:** In-keyboard scratchpad and movable floating note window over any app, with optional AI polish and undo.
- **On-device and password privacy:** Everyday keystrokes, glide trails, in-memory learned word suggestions, clipboard items (masking items flagged sensitive by Android 13+ or copied/cut with SmarType in password or incognito fields, and periodically removing unpinned sensitive items older than 20 seconds by default), and Quick Notes text stay on the phone and are excluded from Android backup; settings, custom styles, personal dictionary, and custom themes (including any theme photo and installed keyboard extensions) stay local unless Android backup or device transfer is enabled on the phone (none are sent to SmarType's servers). Password and incognito fields turn off AI actions and AI voice dictation; password fields also turn off composing, autocorrect, and glide typing, and disable the password-row microphone. Text or voice is sent encrypted over HTTPS to Google Firebase and Gemini (guarded by Firebase App Check with Google Play Integrity) only when the user taps an AI action; prompts and audio are not stored after the request and are not used to train models.
- **Plans:** Everyday typing is free without an account; Google sign-in unlocks free AI tries, and Premium is sold through Google Play.

## Pages

- [SmarType Home](https://smartype.in/): Overview of Rewrite, Translate, Voice typing, Quick Notes, and privacy.
- [Indian language keyboard](https://smartype.in/languages): Hindi, Telugu, Tamil and 8 more Indian languages, with English-to-Indian-language AI translation.
- [SmarType vs Gboard vs SwiftKey vs Grammarly](https://smartype.in/compare): Side-by-side comparison across tone rewrite, Indian-language translation, voice cleanup, Quick Notes, and password privacy.
- [Privacy Architecture](https://smartype.in/privacy-architecture): Technical breakdown of what stays on the phone, password-field shutoff, and explicit-tap ephemeral AI requests.
- [Polite WhatsApp Message Rewriter](https://smartype.in/polite-whatsapp-rewriter): Interactive browser showcase of Polite, Professional, Empathetic, and Firm chat rewrites.
- [AI Tone Translator](https://smartype.in/ai-tone-translator): Interactive English-to-Hindi, English-to-Spanish, Arabic-to-English, and French-to-English tone translator preview across SmarType's 21 translation targets.
- [Rough-Notes-to-Neat-List Formatter](https://smartype.in/rough-notes-to-neat-list): Local in-browser list, checklist, and table formatter paired with SmarType Format and Quick Notes.
- [Privacy Policy](https://smartype.in/privacy): Full data handling and account deletion instructions (`https://smartype.in/privacy#choices`).
- [Help & FAQ](https://smartype.in/help): Setup, AI features, languages, voice typing, and billing answers.
- [Terms of Service](https://smartype.in/terms): Service and Google Play subscription terms.
- [Contact](https://smartype.in/contact): Support and account deletion contact (`{SUPPORT}`).
"""


# ---------- build ----------

def main():
    shutil.rmtree(OUT, ignore_errors=True)
    for d in ("assets/art", "assets/shots"):
        os.makedirs(os.path.join(OUT, d))
    for f in os.listdir(os.path.join(DESIGN, "brand/web")):
        shutil.copy(os.path.join(DESIGN, "brand/web", f), os.path.join(OUT, "assets", f))
    for f in ("lockup-ink.svg", "lockup-porcelain.svg"):
        shutil.copy(os.path.join(DESIGN, "brand/svg", f), os.path.join(OUT, "assets", f))
    for n in ILLUSTRATIONS:
        for suf in ("", "-dark"):
            shutil.copy(os.path.join(DESIGN, f"illustrations/svg/{n}{suf}.svg"), os.path.join(OUT, f"assets/art/{n}{suf}.svg"))
    for f in ("01-ai-open.png", "02-tr-open.png", "03-vo-listen.png", "08-privacy.png"):
        shutil.copy(os.path.join(DESIGN, "store/en", f), os.path.join(OUT, "assets/shots", f))
    shutil.copy(os.path.join(DESIGN, "store/en/feature-a.png"), os.path.join(OUT, "assets/og.png"))
    shutil.copy(os.path.join(WEB, "tools/site.css"), os.path.join(OUT, "assets/site.css"))
    os.makedirs(os.path.join(OUT, "assets/js"))
    for f in ("gsap.min.js", "ScrollTrigger.min.js"):
        shutil.copy(os.path.join(WEB, "tools/vendor", f), os.path.join(OUT, "assets/js", f))
    for f in ("site.js", "home.js", "tools.js"):
        shutil.copy(os.path.join(WEB, "tools", f), os.path.join(OUT, "assets/js", f))
    pages = {"index.html": home(), "languages.html": languages_page(), "compare.html": compare(), "privacy-architecture.html": privacy_architecture(),
             "polite-whatsapp-rewriter.html": polite_whatsapp_rewriter(),
             "ai-tone-translator.html": ai_tone_translator(),
             "rough-notes-to-neat-list.html": rough_notes_to_neat_list(),
             "privacy.html": privacy(), "terms.html": terms(), "help.html": help_page(),
             "contact.html": contact(), "404.html": notfound()}
    for name, text in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    with open(os.path.join(OUT, "vercel.json"), "w", encoding="utf-8") as fh:
        fh.write('{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(robots_txt())
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap_xml(pages))
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write(llms_txt())
    print("website written to", OUT)


if __name__ == "__main__":
    main()
