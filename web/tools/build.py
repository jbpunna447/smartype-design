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


def art(name, size, cls=""):
    """An illustration that switches to its dark version with the system theme."""
    return (f'<picture class="art {cls}"><source media="(prefers-color-scheme: dark)" srcset="assets/art/{name}-dark.svg">'
            f'<img src="assets/art/{name}.svg" alt="" width="{size}" height="{size}" loading="lazy"></picture>')


# ---------- layout ----------

NAV = [("index.html#features", "Features"), ("index.html#privacy", "Privacy"), ("help.html", "Help")]


def page(name, title, description, body, current=None):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == current else ""}>{E(l)}</a>' for h, l in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(description)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:image" content="https://smartype.in/assets/og.png">
<meta name="theme-color" content="#22C3CF">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="manifest" href="assets/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap top-in"><a class="brand" href="index.html" aria-label="SmarType home">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/lockup-porcelain.svg"><img src="assets/lockup-ink.svg" alt="SmarType" height="30"></picture></a>
<nav aria-label="Main">{links}</nav><span class="soon">Coming soon</span></div></header>
<main id="main">{body}</main>
<footer class="foot"><div class="wrap foot-in">
<div><picture><source media="(prefers-color-scheme: dark)" srcset="assets/lockup-porcelain.svg"><img src="assets/lockup-ink.svg" alt="SmarType" height="26"></picture>
<p>The Android keyboard that helps you type, speak and get it right.</p></div>
<nav aria-label="Footer"><a href="help.html">Help</a><a href="contact.html">Contact</a><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms</a></nav>
<p class="copy">© {YEAR} SmarType</p></div></footer></body></html>
"""


# ---------- pages ----------

FEATURES = [
    ("spark", "Fix a message in one tap", "Grammar, spelling and tone fixed right where you type. Pick Polite, Professional, Shorter or your own style."),
    ("translate", "Type in English, send in Hindi", "Translate what you wrote before you send it: Hindi, Telugu, Tamil and more."),
    ("mic", "Speak, and it's tidied up", "Dictate a message. SmarType adds the punctuation and drops the ums."),
    ("format_list_bulleted", "Rough notes, neat lists", "Turn a run-on message into bullets, a numbered list or a table."),
    ("sticky_note_2", "Notes on your keyboard", "Jot a list or keep something you copied. Ask AI to add to it or change its tone."),
    ("content_paste", "Your copied text, one tap away", "Recent and pinned clips right above the keys."),
]


def home():
    feats = "".join(f'<div class="feat"><div class="feat-ic">{icon(i)}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, t, d in FEATURES)
    shots = "".join(f'<img src="assets/shots/{n}.png" alt="{E(a)}" width="270" height="480" loading="lazy">' for n, a in [
        ("01-ai-open", "SmarType fixing a typo-filled message in one tap"),
        ("02-tr-open", "SmarType translating a message from English into Hindi"),
        ("03-vo-listen", "Voice typing in SmarType, with the speech tidied up"),
        ("08-privacy", "SmarType's privacy promises")])
    promises = [("keyboard", "Typing stays on your phone", "Suggestions are learned on the device. What you type isn't sent anywhere."),
                ("spark", "AI sees only what you send", "Text leaves your phone only when you tap Rewrite, Translate or Format, or finish a voice message."),
                ("lock", "Passwords stay private", "No AI, no voice and nothing learned in password fields.")]
    prom = "".join(f'<div class="promise"><div class="feat-ic">{icon(i)}</div><div><h3>{E(t)}</h3><p>{E(d)}</p></div></div>' for i, t, d in promises)
    body = f"""
<section class="hero"><div class="wrap hero-in"><div class="hero-copy">
<h1>Type it. Say it. <em>Get it right.</em></h1>
<p class="lede">SmarType is an Android keyboard with AI that fixes, translates and tidies your words, in every app.</p>
<div class="cta"><span class="btn primary" aria-disabled="true">{icon("android", "ic sm") if os.path.exists(os.path.join(DESIGN, "icons/material-symbols-rounded/android.svg")) else ""}Coming soon to Google Play</span>
<a class="btn ghost" href="#features">See what it does</a></div></div>
<div class="hero-art">{art("art_welcome", 360)}</div></div></section>

<section class="sec" id="features"><div class="wrap"><h2>Everything a keyboard should do, <em>and a bit more</em></h2>
<div class="feats">{feats}</div></div></section>

<section class="sec shots-sec"><div class="wrap"><h2>See it in action</h2><div class="shots">{shots}</div></div></section>

<section class="sec band" id="privacy"><div class="wrap band-in"><div><h2>Private by default</h2>
<p class="lede">A keyboard sees everything you type. SmarType is built so it doesn't have to keep any of it.</p>
<a class="link" href="privacy.html">Read the privacy policy {icon("chevron_right", "ic sm")}</a></div>
<div class="promises">{prom}</div></div></section>

<section class="sec"><div class="wrap split"><div>{art("art_empty_languages", 300)}</div><div>
<h2>English and Hindi, <em>one key apart</em></h2>
<p class="lede">Add the languages you type in and switch with the globe key. Suggestions follow the language you're in.</p></div></div></section>

<section class="sec"><div class="wrap split rev"><div>{art("art_signin", 300)}</div><div>
<h2>Try the AI <em>for free</em></h2>
<p class="lede">Sign in with Google to get free AI tries for rewrite, translate and format. Typing, suggestions and voice work without an account.</p></div></div></section>

<section class="sec closing"><div class="wrap"><h2>Coming soon to <em>Google Play</em></h2>
<p class="lede">Questions in the meantime? <a href="help.html">Help</a> has the answers, or <a href="contact.html">write to us</a>.</p></div></section>
"""
    return page("index.html", "SmarType: the AI keyboard for Android", "An Android keyboard with AI that fixes, translates and tidies your words, in every app.", body)


DRAFT = ('<div class="draft"><b>Draft.</b> This text was drafted from how the app works today and has not been approved yet. '
         "It must be reviewed by SmarType (and a lawyer) before the app is published.</div>")


def doc(name, title, description, h1, updated, sections, draft=False):
    toc = "".join(f'<li><a href="#{E(sid)}">{E(t)}</a></li>' for sid, t, _ in sections)
    body = "".join(f'<section id="{E(sid)}"><h2>{E(t)}</h2>{content}</section>' for sid, t, content in sections)
    return page(name, title, description,
                f'<div class="wrap doc">{DRAFT if draft else ""}<h1>{E(h1)}</h1><p class="meta">Last updated: {E(updated)}</p>'
                f'<nav class="toc" aria-label="On this page"><ol>{toc}</ol></nav>{body}</div>', current=name)


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
                f'<div class="wrap doc"><h1>Help</h1><p class="lede">Quick answers. Still stuck? <a href="contact.html">Contact us</a>.</p>{groups}</div>', current="help.html")


def contact():
    return page("contact.html", "Contact · SmarType", "How to reach SmarType.",
                f'<div class="wrap doc contact">{art("art_done", 200)}<h1>Contact us</h1>'
                f'<p class="lede">Questions, feedback or a problem? Write to <a href="mailto:{SUPPORT}">{SUPPORT}</a>. We usually reply within two working days.</p>'
                '<p>To delete your account, write from the email address you sign in with. For billing, Google Play handles payments and refunds.</p></div>')


def notfound():
    return page("404.html", "Page not found · SmarType", "This page doesn't exist.",
                f'<div class="wrap doc contact">{art("art_empty_notes", 200)}<h1>Page not found</h1><p class="lede"><a href="index.html">Go to the home page</a>.</p></div>')


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
