"""Builds the SmarType website into web/site from the pages below and the brand assets in design/.

    python3 web/tools/build.py

Static HTML and CSS, no framework. Brand marks, favicons and illustrations are copied from design/assets, so the
website always matches the brand kit. Vercel serves web/site."""
import html
import os
import re
import shutil

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(WEB)
DESIGN = os.path.join(ROOT, "design", "assets")
OUT = os.path.join(WEB, "site")
E = html.escape

SUPPORT = "contact@smartype.in"
YEAR = 2026
ILLUSTRATIONS = ["art_welcome", "art_signin", "art_ai", "art_premium", "art_empty_languages", "art_empty_notes", "art_done"]


# ---------- icons (Material Symbols Rounded, the brand spark) ----------

def icon(name, cls="ic"):
    if name == "spark":
        src = os.path.join(DESIGN, "icons/brand/spark.svg")
    else:
        src = os.path.join(DESIGN, "icons/material-symbols-rounded", f"{name}.svg")
    s = open(src).read()
    view = re.search(r'viewBox="([^"]+)"', s).group(1)
    paths = "".join(re.findall(r"<path[^>]*/>", s))
    return f'<svg class="{cls}" viewBox="{view}" aria-hidden="true" fill="currentColor">{paths}</svg>'


# The Google Play logo, so the button reads as Play at a glance (used as Google's brand guidelines allow, to point to the app).
PLAY = ('<svg class="play" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="#00D7FE" d="M3.6 1.8 13.3 12 3.6 22.2c-.4-.2-.6-.6-.6-1.1V2.9c0-.5.2-.9.6-1.1z"/>'
        '<path fill="#00F076" d="M16.6 8.6 13.3 12 3.6 1.8c.3-.2.8-.2 1.2 0z"/>'
        '<path fill="#FFC900" d="M20.4 10.7c.8.4.8 1.6 0 2.1l-3.8 2.2-3.3-3 3.3-3.4z"/>'
        '<path fill="#F7304B" d="M16.6 15.4 4.8 22.2c-.4.2-.9.2-1.2 0l9.7-10.2z"/></svg>')


def play_button(label="Coming soon to Google Play", cls=""):
    """The one call to action: a flat button with the Play logo. A span while the app isn't on Play; swap for a link later."""
    return f'<span class="btn key {cls}" aria-disabled="true"><span class="play-chip">{PLAY}</span>{E(label)}</span>'


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
NAV = [("how", "How it works"), ("features", "Features"), ("privacy", "Privacy"), ("/help.html", "Help")]


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


def page(name, title, description, body, extra=""):
    """A page: the floating header (a pill; on phones a Menu sheet), the content and the footer. Links and assets
    start at the site root, so the 404 page also works at any depth."""
    links = nav_links(name)
    url = "https://smartype.in/" + ("" if name == "index.html" else name.replace(".html", ""))
    where = ('<meta name="robots" content="noindex">' if name == "404.html"
             else f'<link rel="canonical" href="{url}"><meta property="og:url" content="{url}">')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(description)}">{where}
<meta property="og:type" content="website"><meta property="og:site_name" content="SmarType"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}"><meta property="og:image" content="https://smartype.in/assets/og.png"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5FAFB" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0B1416" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/assets/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{ver("site.css")}"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="top-pill"><a class="brand" href="/" aria-label="SmarType home">{lockup(28)}</a>
<nav class="top-nav" aria-label="Main"><span class="nav-hl" aria-hidden="true"></span>{links}</nav>{play_button("Coming soon", "sm")}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button></div>
<nav class="menu" id="menu" aria-label="Menu" hidden>{links}{play_button()}</nav></header>
<main id="main">{body}</main>
<footer class="foot"><div class="wrap foot-in">
<div>{lockup(26)}<p>The Android keyboard that helps you type, speak and get it right.</p></div>
<nav aria-label="Footer"><a href="/help.html">Help</a><a href="/contact.html">Contact</a><a href="/privacy.html">Privacy policy</a><a href="/terms.html">Terms</a></nav>
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
            '<i class="fn k3">⇧</i>' + letters("zxcvbnm") + '<i class="fn k3">⌫</i>',
            f'<i class="fn k3">?123</i><i class="fn">{icon("language", "ic sm")}</i><i class="space k10" data-c=" ">English</i>'
            '<i class="fn" data-c=".">.</i><i class="ent k3">↵</i>']
    bar = (sb("spark", "fix") + sb("translate", "tr") + sb("format_list_bulleted") + sb("content_paste", ai=False)
           + sb("sticky_note_2", ai=False) + sb("more_horiz", ai=False) + '<span class="sp"></span>' + sb("mic", "mic"))
    voice = (sb("delete", ai=False) + '<span class="rec"><i></i><span class="rec-t">0:00</span></span><span class="veq">'
             + "<i></i>" * 18 + '</span><span class="vprog">Transcribing and tidying up…</span><span class="vlang">Auto</span>' + sb("check"))

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
            + panel("tr", "Translate", [("हिन्दी", "hi"), ("Español", "es"), ("Français", "fr"), ("العربية", "ar")], "Hindi", HINDI, "hi")
            + "</div>")


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
        ("Translate", "Send it in Hindi, Spanish, French, Arabic and 16 more languages.", "translate",
         '<span class="tag">English</span>' + icon("chevron_right", "ic sm") + '<span class="tag on" lang="hi">हिन्दी</span>'
         '<span class="tag" lang="es">Español</span><span class="tag" lang="fr">Français</span>'),
        ("Speak", "Or just say it. Speech becomes text on your phone, then it's tidied up.", "mic",
         '<span class="tag on"><span class="wave"><i></i><i></i><i></i><i></i><i></i></span>Speech to text on your phone</span>'),
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
        ("c-langs", "language", "Your languages,<br><em>one key apart.</em>", "Type in English, Hindi, Telugu, Tamil, Bengali and more. Switch with the globe key.",
         '<div class="mini hello"><div class="hello-card" aria-hidden="true"><span class="hello-word">Hello</span><i class="caret dc"></i></div>'
         f'<div class="hello-foot"><span class="globe" aria-hidden="true">{icon("language")}</span><ul class="lang-names">{lang_names}</ul></div></div>'),
    ]
    card_html = "".join(f'<article class="card {c}"><div class="card-copy"><div class="card-ic">{icon(i)}</div><h3>{h}</h3><p>{E(d)}</p></div>'
                        f'<div class="card-vis">{v}</div></article>' for c, i, h, d, v in cards)

    # Privacy: three promises, and one picture of where text goes (home.js plays one promise at a time).
    vows = [("keyboard", "Typing stays on your phone", "Suggestions are learned here. Your clipboard and notes stay here too."),
            ("spark", "AI sees only what you send", "Text leaves only when you tap an AI button or finish a voice message, and it travels encrypted."),
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
<div class="cta" data-reveal>{play_button()}<a class="btn key alt" href="#how">See how it works</a></div>
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
<p class="lede" data-reveal>A keyboard sees everything you type. SmarType keeps it on your phone, and sends text only when you ask.</p>
<ol class="vows">{vow_html}</ol>
</div>
{seal}</div>
<div class="wrap"><div class="peek-note" data-reveal>{not_looking()}<div><h3>We don't know what you type. Honestly.</h3>
<p>Nothing in SmarType tracks your words. Sign in, and we know your name, email and Google photo, just so your free AI tries and Premium follow you to every phone. The "love you" you typed three times before sending? No idea. We never sell your data or use what you type for ads.</p>
<a class="link" href="/privacy.html">Read the privacy policy {icon("chevron_right", "ic sm")}</a></div></div></div></section>

<section class="closing2"><div class="glow g-close" data-depth=".2"></div>
<div class="wrap split"><div class="close-art" data-reveal>{art("art_signin", 320)}</div><div>
<h2 data-type>Try the AI <em>for free.</em></h2>
<p class="lede" data-reveal>Sign in with Google to get free AI tries. Typing, suggestions and voice work without an account.</p>
<div class="cta" data-reveal>{play_button()}</div></div></div>
</section>
"""
    scripts = "".join(f'<script src="{ver(f)}" defer></script>' for f in ("gsap.min.js", "ScrollTrigger.min.js", "home.js"))
    return page("index.html", "SmarType: the AI keyboard for Android", "An Android keyboard with AI that fixes, translates and tidies your words, in every app.",
                body, extra=scripts)


DRAFT = ('<div class="draft"><b>Draft.</b> This text was drafted from how the app works today and has not been approved yet. '
         "It must be reviewed by SmarType (and a lawyer) before the app is published.</div>")


def doc(name, title, description, h1, updated, sections, draft=False):
    toc = "".join(f'<li><a href="#{E(sid)}">{E(t)}</a></li>' for sid, t, _ in sections)
    body = "".join(f'<section id="{E(sid)}"><h2>{E(t)}</h2>{content}</section>' for sid, t, content in sections)
    return page(name, title, description,
                f'<div class="wrap doc">{DRAFT if draft else ""}<h1>{E(h1)}</h1><p class="meta">Last updated: {E(updated)}</p>'
                f'<nav class="toc" aria-label="On this page"><ol>{toc}</ol></nav>{body}</div>')


def privacy():
    s = [
        ("summary", "In short", "<ul><li>What you type stays on your phone. Suggestions are learned on the device.</li>"
         "<li>Text is sent only when you ask for AI: Rewrite, Translate, Format, Notes AI, or tidying up a voice message.</li>"
         "<li>Nothing is learned or sent from password fields.</li>"
         "<li>If you sign in, we keep your Google account's name, email, photo and sign-in dates, and how many AI tries you've used.</li>"
         "<li>We don't sell your data and we don't use what you type for advertising.</li></ul>"),
        ("typing", "What stays on your phone", "<p>Your keystrokes, the words SmarType learns for suggestions, your clipboard history, your notes and your settings are stored only on your phone. "
         "They are not sent to us. Clipboard history skips content Android marks as sensitive. Uninstalling the app or clearing its data removes them.</p>"),
        ("ai", "When you use AI", "<p>When you tap Rewrite, Translate or Format, ask AI to change a note, or finish a voice message, the text you chose is sent over an encrypted connection to SmarType's server (Google Firebase), "
         "which sends it to an AI model provider (currently Google's Gemini) to produce the result and returns it to you.</p>"
         "<p>We use the text only to produce that result. We don't keep it after the request, and we don't use it to train models. "
         "Our AI provider processes it under its terms for API customers. We count each use against your free tries or plan.</p>"
         "<p>Voice: speech is turned into text on your phone. Only the text is sent, to tidy it up.</p>"),
        ("account", "Your account", "<p>Signing in is optional. If you sign in with Google, we store your account ID, name, email address, profile photo, and when you created the account and last signed in. "
         "We use them to give you free AI tries, keep Premium on all your phones and help you if you contact us.</p>"),
        ("payments", "Payments", "<p>Premium is bought through Google Play. Google handles payment details; we receive only whether your subscription is active and when it renews.</p>"),
        ("device", "Keeping the service safe", "<p>To stop abuse of the AI service, the app uses Firebase App Check with Google Play Integrity, which confirms requests come from a real copy of the app on a real device.</p>"),
        ("analytics", "Usage analytics", "<p>The app includes Google Analytics for Firebase, which collects basic, non-content information such as app opens, device model, Android version and approximate country. "
         "It never receives what you type.</p>"),
        ("sharing", "Who we share data with", "<p>Only the service providers that run SmarType: Google (Firebase, Gemini, Google Play) and, if you set one up yourself, the AI provider of your own key. "
         "We don't sell personal data. We may disclose data if the law requires it.</p>"),
        ("choices", "Your choices", "<ul><li>Use SmarType without signing in: typing, suggestions and voice still work.</li>"
         "<li>Turn off clipboard history in Settings.</li>"
         f"<li>Delete your account and its data: write to <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a>. We delete it within 30 days.</li></ul>"),
        ("children", "Children", "<p>SmarType isn't directed at children under 13 and we don't knowingly collect their data.</p>"),
        ("changes", "Changes and contact", f"<p>We'll update this page when how we handle data changes, and change the date at the top. Questions: <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a>.</p>"),
    ]
    return doc("privacy.html", "Privacy policy · SmarType", "How SmarType handles your data: typing stays on your phone; text is sent only when you use AI.",
               "Privacy policy", "1 November 2026", s, draft=True)


def terms():
    s = [
        ("about", "About these terms", "<p>These terms apply when you use the SmarType keyboard app and its AI features. By using SmarType you agree to them.</p>"),
        ("use", "Using SmarType", "<p>Use SmarType lawfully and don't try to misuse or overload the AI service, get around limits or copy the app.</p>"),
        ("ai", "AI results", "<p>AI suggestions can be wrong or unsuitable. Read them before you send. You're responsible for what you send.</p>"),
        ("tries", "Free tries and Premium", "<p>Signed-in users get a number of free AI tries; this number can change. Premium is a subscription sold through Google Play; "
         "Google Play's terms cover billing, renewals, cancellations and refunds. You can cancel any time in Google Play.</p>"),
        ("content", "Your content", "<p>What you write stays yours. You give us only the permission needed to process text you send to AI and return the result.</p>"),
        ("availability", "Availability", "<p>We work to keep SmarType running, but features can change and the AI service can be unavailable at times.</p>"),
        ("liability", "Liability", "<p>To the extent the law allows, SmarType is provided as is, and we aren't liable for indirect losses from using it.</p>"),
        ("changes", "Changes and contact", f"<p>We may update these terms and will change the date at the top. Questions: <a href=\"mailto:{SUPPORT}\">{SUPPORT}</a>.</p>"),
    ]
    return doc("terms.html", "Terms · SmarType", "The terms for using the SmarType keyboard and its AI features.", "Terms of use", "1 November 2026", s, draft=True)


FAQ = [
    ("Getting started", [
        ("How do I turn on SmarType?", "Open SmarType and follow the two steps: allow it in Android's keyboard settings, then choose it as your keyboard. The app moves on by itself when each step is done."),
        ("How do I switch back to my old keyboard?", "Long-press the globe key, or tap the keyboard icon in the navigation bar, and pick another keyboard."),
        ("Do I need an account?", "No. Typing, suggestions and voice work without one. Sign in with Google only if you want free AI tries or Premium."),
    ]),
    ("AI features", [
        ("What happens to the text I send to AI?", "It goes to our server and our AI provider only to produce your result, and isn't kept. See the privacy policy."),
        ("How many free tries do I get?", "Signed-in users get a set number of free AI tries; the app shows how many are left. Premium removes the limit."),
        ("Why doesn't AI work in password fields?", "On purpose: SmarType never sends or learns anything typed in a password field."),
    ]),
    ("Languages and voice", [
        ("Which languages can I type in?", "English and Indian languages including Hindi, Telugu, Tamil and Bengali. Add them in Languages and switch with the globe key."),
        ("Does voice typing send my audio?", "No. Speech is turned into text on your phone; only the text is sent, to tidy it up."),
    ]),
    ("Account and data", [
        ("How do I delete my account?", f"Write to {SUPPORT} from your account's email address. We delete your account and its data within 30 days."),
        ("How do I cancel Premium?", "In Google Play: Profile → Payments and subscriptions → Subscriptions → SmarType → Cancel."),
    ]),
]


def help_page():
    groups = "".join(f'<section><h2>{E(g)}</h2>' + "".join(
        f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items) + "</section>" for g, items in FAQ)
    return page("help.html", "Help · SmarType", "Answers about setting up SmarType, its AI features, languages, voice and your account.",
                f'<div class="wrap doc"><h1>Help</h1><p class="lede">Quick answers. Still stuck? <a href="/contact.html">Contact us</a>.</p>{groups}</div>')


def contact():
    return page("contact.html", "Contact · SmarType", "How to reach SmarType.",
                f'<div class="wrap doc contact">{art("art_done", 200)}<h1>Contact us</h1>'
                f'<p class="lede">Questions, feedback or a problem? Write to <a href="mailto:{SUPPORT}">{SUPPORT}</a>. We usually reply within two working days.</p>'
                '<p>To delete your account, write from the email address you sign in with. For billing, Google Play handles payments and refunds.</p></div>')


def notfound():
    return page("404.html", "Page not found · SmarType", "This page doesn't exist.",
                f'<div class="wrap doc contact">{art("art_empty_notes", 200)}<h1>Page not found</h1><p class="lede"><a href="/">Go to the home page</a>.</p></div>')


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
    for f in ("site.js", "home.js"):
        shutil.copy(os.path.join(WEB, "tools", f), os.path.join(OUT, "assets/js", f))
    pages = {"index.html": home(), "privacy.html": privacy(), "terms.html": terms(), "help.html": help_page(),
             "contact.html": contact(), "404.html": notfound()}
    for name, text in pages.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(text)
    with open(os.path.join(OUT, "vercel.json"), "w") as fh:
        fh.write('{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nAllow: /\nSitemap: https://smartype.in/sitemap.xml\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        urls = "".join(f"<url><loc>https://smartype.in/{p.replace('.html', '') if p != 'index.html' else ''}</loc></url>" for p in pages if p != "404.html")
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("website written to", OUT)


if __name__ == "__main__":
    main()
