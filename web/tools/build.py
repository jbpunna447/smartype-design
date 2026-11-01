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
    """The one call to action: a keycap with the Play logo. A span while the app isn't on Play; swap for a link later."""
    return f'<span class="btn key {cls}" aria-disabled="true"><span class="play-chip">{PLAY}</span>{E(label)}</span>'


def art(name, size, cls=""):
    """An illustration that switches to its dark version with the system theme."""
    return (f'<picture class="art {cls}"><source media="(prefers-color-scheme: dark)" srcset="assets/art/{name}-dark.svg">'
            f'<img src="assets/art/{name}.svg" alt="" width="{size}" height="{size}" loading="lazy"></picture>')


# ---------- layout ----------

NAV = [("index.html#features", "Features"), ("index.html#privacy", "Privacy"), ("help.html", "Help")]


def page(name, title, description, body, current=None, extra=""):
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
<nav aria-label="Main">{links}</nav>{play_button("Coming soon", "sm")}</div></header>
<main id="main">{body}</main>
<footer class="foot"><div class="wrap foot-in">
<div><picture><source media="(prefers-color-scheme: dark)" srcset="assets/lockup-porcelain.svg"><img src="assets/lockup-ink.svg" alt="SmarType" height="26"></picture>
<p>The Android keyboard that helps you type, speak and get it right.</p></div>
<nav aria-label="Footer"><a href="help.html">Help</a><a href="contact.html">Contact</a><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms</a></nav>
<p class="copy">© {YEAR} SmarType</p></div></footer>{extra}</body></html>
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
    """The home page: a story told as you scroll. Text is typed in as each part appears (home.js); without JavaScript,
    or with reduced motion, every part shows its final text."""
    bubbles = [("बहुत-बहुत धन्यवाद!", "b2 ai", 1.1),
               ('<span class="wave"><i></i><i></i><i></i><i></i><i></i></span>Leaving now', "b3 dark", .8),
               ("• Milk<br>• Bread", "b4 note", 1.4)]
    floats = "".join(f'<div class="float {c}" data-depth="{d}" aria-hidden="true">{t}</div>' for t, c, d in bubbles)
    composer = (f'<div class="composer" data-depth=".25" aria-hidden="true"><div class="cm-top"><span class="cm-dot"></span>Message</div>'
                f'<div class="cm-field"><span class="cm-text">Can we reschedule to Friday?</span><i class="caret"></i></div>'
                f'<div class="cm-bar"><span class="cm-ai">{icon("spark", "ic")}</span><span class="cm-chip" data-k="pro">Professional</span>'
                f'<span class="cm-chip" data-k="hi">हिन्दी</span><span class="cm-chip">Shorter</span></div></div>')
    steps = [
        ("Type", "Type the way you always do. SmarType learns your words on your phone.", "keyboard"),
        ("Fix", "One tap on the spark fixes grammar, spelling and tone, right where you type.", "spark"),
        ("Translate", "Send it in Hindi, Telugu, Tamil and more, before you hit send.", "translate"),
        ("Speak", "Or just say it. It's tidied up, ready to send.", "mic"),
    ]
    # What each step changed, shown under its text.
    details = [
        '<span class="tag">' + icon("keyboard", "ic sm") + 'Learns your words, on your phone</span>',
        '<span class="diff"><s>u</s><b>you</b></span><span class="diff"><s>adress</s><b>address</b></span><span class="diff"><s>great,</s><b>Great!</b></span>',
        '<span class="tag">English</span>' + icon("chevron_right", "ic sm") + '<span class="tag on">हिन्दी</span><span class="tag">తెలుగు</span><span class="tag">தமிழ்</span>',
        '<span class="tag on"><span class="wave"><i></i><i></i><i></i><i></i><i></i></span>Speech to text, on your phone</span>',
    ]
    acc_html = "".join(f'<div class="acc-item{" on" if i == 0 else ""}" data-step="{i}" role="tab" tabindex="0" aria-selected="{"true" if i == 0 else "false"}">'
                       f'<div class="acc-bar" aria-hidden="true"><i class="acc-fill"></i></div>'
                       f'<div class="acc-head"><span class="acc-num">0{i + 1}</span>'
                       f'<h3 class="acc-title">{E(t)}</h3>'
                       f'<span class="acc-icon" aria-hidden="true">{icon(ic, "ic sm")}</span></div>'
                       f'<div class="acc-body"><div class="acc-body-in"><p>{E(d)}</p>'
                       f'<div class="step-detail">{details[i]}</div></div></div></div>' for i, (t, d, ic) in enumerate(steps))
    states = [("great, can u send the adress", "adress"), ("Great! Can you send me the address?", ""),
              ("बढ़िया! क्या तुम मुझे पता भेज सकते हो?", ""), ("Can't wait, see you on Saturday!", "")]
    state_html = "".join(f'<span class="st" data-typo="{E(w)}" hidden>{E(t)}</span>' for t, w in states)
    tones = {"Polite": "Would it be okay if I took Friday off? I'll make sure my work is covered.",
             "Professional": "I'd like to request leave on Friday. My tasks will be handed over before then.",
             "Casual": "Mind if I take Friday off? I'll sort my stuff before.",
             "Shorter": "Can I take Friday off?"}
    tone_chips = "".join(f'<button class="chip{" on" if i == 0 else ""}" type="button" aria-pressed="{"true" if i == 0 else "false"}" data-tone="{E(v)}">{E(k)}</button>'
                         for i, (k, v) in enumerate(tones.items()))
    cards = [
        ("c-translate", "translate", "Type in English.<br><em>Send it in Hindi.</em>", "Pick a language from the chips above your keys. The translation replaces your text, or copy it.",
         '<div class="mini"><div class="mb in">See you at dinner tonight!</div><div class="mb out" data-typeon>आज रात खाने पर मिलते हैं!</div>'
         '<div class="mchips"><span>English</span><span class="on">हिन्दी</span><span>తెలుగు</span><span>தமிழ்</span></div></div>'),
        ("c-voice", "mic", "Just speak.<br><em>It's tidied up.</em>", "Speech becomes text on your phone; SmarType adds the punctuation and drops the ums.",
         '<div class="mini voice"><div class="eq">' + "".join("<i></i>" for _ in range(28)) + '</div>'
         '<div class="raw">uh can you pick up, um, milk and bread on the way</div><div class="mb out">Can you pick up milk and bread on the way?</div></div>'),
        ("c-format", "format_list_bulleted", "Rough notes,<br><em>neat lists.</em>", "Bullets, numbered steps or a table, from whatever you typed.",
         '<div class="mini"><div class="raw">need tickets, hotel for 2 nights, cab from airport, dinner sat</div>'
         '<ul class="list"><li data-typeon>Train tickets</li><li data-typeon>Hotel for 2 nights</li><li data-typeon>Cab from the airport</li><li data-typeon>Dinner on Saturday</li></ul></div>'),
        ("c-notes", "sticky_note_2", "Notes that<br><em>AI can polish.</em>", "Jot a list or keep something you copied. Ask AI to add to it or change its tone; undo in one tap.",
         '<div class="mini"><div class="ask">' + icon("spark", "ic sm") + '<span data-typeon>add that I\'ll pay the rent on Friday</span></div>'
         '<div class="note">Hey Ravi, the tap\'s fixed, thanks a lot! <mark data-typeon>I\'ll pay the rent on Friday.</mark></div></div>'),
        ("c-clip", "content_paste", "Copied it?<br><em>Paste in one tap.</em>", "Recent and pinned clips sit right above your keys, and stay on your phone.",
         '<div class="mini"><div class="clip pin">Office Wi-Fi: Lake-5G ' + icon("keep", "ic sm") + '</div><div class="clip">Order #48213 confirmed for Friday</div>'
         '<div class="clip">maps.app/meet-point</div></div>'),
    ]
    card_html = "".join(f'<article class="card {c}"><div class="card-copy"><div class="card-ic">{icon(i)}</div><h3>{h}</h3><p>{E(d)}</p></div>'
                        f'<div class="card-vis">{v}</div></article>' for c, i, h, d, v in cards)
    hellos = [("Hello", "English"), ("नमस्ते", "Hindi"), ("నమస్కారం", "Telugu"), ("வணக்கம்", "Tamil"), ("নমস্কার", "Bengali"),
              ("ನಮಸ್ಕಾರ", "Kannada"), ("നമസ്കാരം", "Malayalam"), ("નમસ્તે", "Gujarati"), ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "Punjabi")]
    lang_names = "".join(f'<li data-hello="{E(h)}">{E(n)}</li>' for h, n in hellos)
    # Words that stay on the phone: they drift inside the ring and bounce off it (home.js).
    kept = ["Hi Mom", "meet at 6?", "PIN", "address", "love you", "bank OTP", "••••••", "salary", "doctor 4 pm", "Wi-Fi code"]
    kept_html = "".join(f'<span class="kw">{E(w)}</span>' for w in kept)
    stats = [("0", "keystrokes sent anywhere while you type"), ("0", "seconds of your voice leave your phone"), ("0", "words learned in password fields")]
    stat_html = "".join(f'<div class="stat" data-reveal><b>{n}</b><span>{E(t)}</span></div>' for n, t in stats)
    pw_offs = "".join(f'<span class="off">{icon("check_circle", "ic sm")}{E(t)}</span>' for t in ("AI off", "Voice off", "Learning off"))
    promises = [("keyboard", "Typing stays on your phone", "Suggestions, clipboard, notes and settings are stored only on your phone."),
                ("spark", "AI sees only what you send", "Text leaves your phone only when you tap Rewrite, Translate or Format, or finish a voice message, and it travels encrypted."),
                ("lock", "Never sold, never for ads", "We don't sell your data and we don't use what you type for advertising.")]
    prom = "".join(f'<li data-reveal><span class="pk">{icon(i)}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i, t, d in promises)
    body = f"""
<section class="hero2" id="top"><div class="glow g1" data-depth="-.3"></div><div class="glow g2" data-depth=".4"></div>
<div class="wrap hero2-in"><div class="hero2-copy">
<p class="kicker" data-reveal>The AI keyboard for Android</p>
<h1 data-type="hero">Type it.<br>Say it.<br><em>Get it right.</em></h1>
<p class="lede" data-reveal>SmarType fixes, translates and tidies your words, right where you type, in every app.</p>
<div class="cta" data-reveal>{play_button()}<a class="btn key alt" href="#features">See it work</a></div></div>
<div class="hero2-stage">{floats}<div class="hero2-art" data-depth=".12">{art("art_welcome", 360)}</div>{composer}</div></div>
<a class="scroll-cue" href="#features" aria-label="Scroll to the story"><span></span></a></section>

<section class="story" id="features"><div class="glow g-story" data-depth=".3"></div>
<div class="wrap story-head"><p class="kicker" data-reveal>How it works</p><h2 data-type>Watch it <em>work.</em></h2></div>
<div class="wrap story-in"><div class="accordion" role="tablist" aria-label="How SmarType works">{acc_html}</div>
<div class="story-stage" aria-hidden="true"><div class="phone"><div class="phone-chat"><div class="incoming">Party at our new place on Saturday!</div>
<div class="field"><span class="field-text">Great! Can you send me the address?</span><i class="caret"></i>{state_html}</div></div>
<div class="phone-bar"><span class="pb ai" data-for="1">{icon("spark", "ic")}</span><span class="pb ai" data-for="2">{icon("translate", "ic")}</span>
<span class="pb">{icon("format_list_bulleted", "ic")}</span><span class="pb">{icon("content_paste", "ic")}</span><span class="sp"></span>
<span class="pb ai" data-for="3">{icon("mic", "ic")}</span></div>
<div class="phone-keys">{"".join("<i></i>" for _ in range(30))}</div></div></div></div>
</section>

<section class="tone"><div class="glow g-tone" data-depth=".2"></div>
<div class="wrap"><p class="kicker" data-reveal>Styles</p><h2 data-type>Say it <em>your way.</em></h2>
<p class="lede" data-reveal>Same message, the tone you need. Tap a style, or make your own.</p>
<div class="tone-box" data-reveal><div class="tone-chips" role="group" aria-label="Writing styles"><span class="chip-pill" aria-hidden="true"></span>{tone_chips}</div>
<div class="tone-screen"><p class="tone-text" aria-live="polite"><span class="tone-words">{E(list(tones.values())[0])}</span><i class="caret" aria-hidden="true"></i></p></div></div>
</div></section>

<section class="stack"><div class="wrap"><p class="kicker" data-reveal>And more</p><h2 data-type>Everything <em>around it.</em></h2></div>
<div class="wrap cards">{card_html}<div class="stack-end" aria-hidden="true"></div></div></section>

<section class="langs"><div class="glow g-langs" data-depth=".25"></div>
<div class="wrap langs-in"><div><p class="kicker" data-reveal>Languages</p><h2 data-type>Your languages, <em>one key apart.</em></h2>
<p class="lede" data-reveal>Add the languages you type in and switch with the globe key.</p></div>
<div class="hello" data-reveal><div class="hello-card" aria-hidden="true"><span class="hello-word">Hello</span><i class="caret"></i></div>
<div class="hello-foot"><span class="globe" aria-hidden="true">{icon("language", "ic")}</span><ul class="lang-names">{lang_names}</ul></div></div></div>
</section>

<section class="vault" id="privacy"><div class="glow g3" data-depth=".25"></div>
<div class="wrap vault-head"><p class="kicker" data-reveal>Privacy</p><h2 data-type>Private <em>by default.</em></h2>
<p class="lede" data-reveal>A keyboard sees everything you type. SmarType is built so it doesn't have to keep any of it.</p></div>
<div class="wrap vault-grid">
<div class="orbit" aria-hidden="true"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
<div class="kept">{kept_html}</div><div class="core">{icon("lock")}<span>Your phone</span></div>
</div>
<div class="assure"><div class="stats">{stat_html}</div>
<div class="pw" data-reveal><div class="pw-field"><span class="pw-label">Password</span><span class="pw-dots">••••••••••</span>{icon("lock", "ic sm")}</div>
<div class="pw-offs">{pw_offs}</div><p>In password fields, SmarType turns itself down. Nothing is sent, spoken or learned.</p></div></div></div>
<div class="wrap"><ul class="vows">{prom}</ul>
<a class="link" href="privacy.html" data-reveal>Read the privacy policy {icon("chevron_right", "ic sm")}</a></div>
</section>

<section class="closing2"><div class="glow g-close" data-depth=".2"></div>
<div class="wrap split"><div class="close-art" data-reveal>{art("art_signin", 320)}</div><div>
<h2 data-type>Try the AI <em>for free.</em></h2>
<p class="lede" data-reveal>Sign in with Google to get free AI tries. Typing, suggestions and voice work without an account.</p>
<div class="cta" data-reveal>{play_button()}</div></div></div>
</section>
"""
    scripts = ('<script src="assets/js/gsap.min.js" defer></script><script src="assets/js/ScrollTrigger.min.js" defer></script>'
               '<script src="assets/js/home.js" defer></script>')
    return page("index.html", "SmarType: the AI keyboard for Android", "An Android keyboard with AI that fixes, translates and tidies your words, in every app.",
                body, extra=scripts)


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
    os.makedirs(os.path.join(OUT, "assets/js"))
    for f in ("gsap.min.js", "ScrollTrigger.min.js"):
        shutil.copy(os.path.join(WEB, "tools/vendor", f), os.path.join(OUT, "assets/js", f))
    shutil.copy(os.path.join(WEB, "tools/home.js"), os.path.join(OUT, "assets/js/home.js"))
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
