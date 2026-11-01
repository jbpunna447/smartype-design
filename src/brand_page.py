"""The brand review page: today's marks, three logo directions, one spark, colour and the wordmark."""
import html

from brand_marks import DIRECTIONS, GLACIER, GRAPHITE, INK, PORCELAIN, S2_PATH, S2_WEIGHT, S_PATH, SEAGLASS, SPARK_PATH, icon, notification

E = html.escape

AI_LOGO = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-label="AI logo today"><defs><linearGradient id="ail{s}" x2="24" y2="24" gradientUnits="userSpaceOnUse">'
           '<stop stop-color="#67CEE5"/><stop offset="1" stop-color="#69D4BD"/></linearGradient></defs><circle cx="12" cy="12" r="12" fill="url(#ail{s})"/>'
           '<path fill="#08323B" d="M11.55 10.18 14.88 12l-3.33 1.83-1.82 3.33-1.83-3.33L4.57 12l3.33-1.82 1.83-3.33 1.82 3.33Z'
           'M16.16 6.59l1.69.93-1.69.93-.93 1.69-.92-1.69-1.7-.93 1.7-.93.92-1.69.93 1.69Z'
           'M16.16 15.56l1.69.92-1.69.93-.93 1.7-.92-1.7-1.7-.93 1.7-.92.92-1.7.93 1.7Z"/></svg>')
SPARK = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="{c}" aria-label="Spark"><path d="M10.5 4c.55 4.3 2.7 6.45 7 7-4.3.55-6.45 2.7-7 7-.55-4.3-2.7-6.45-7-7 4.3-.55 6.45-2.7 7-7Z"/>'
         '<path d="M18.5 2c.28 1.75 1.13 2.6 2.88 2.88-1.75.28-2.6 1.13-2.88 2.88-.28-1.75-1.13-2.6-2.88-2.88C17.37 4.6 18.22 3.75 18.5 2Z"/></svg>')
STAR = '<svg width="{s}" height="{s}" viewBox="64 13 20 20" aria-label="Star in the app icon"><path fill="{c}" d="M74,13 L77,20 L84,23 L77,26 L74,33 L71,26 L64,23 L71,20 Z"/></svg>'


def _fig(inner, cap):
    return f'<figure class="bk-fig"><div class="bk-art">{inner}</div><figcaption>{cap}</figcaption></figure>'


def _home(key, dark):
    """A home-screen row: the icon among neutral placeholders, at launcher size (56 px icon in a 72 px cell)."""
    others = [("Phone", "#5f8f6b"), ("Photos", "#c98b53"), ("Camera", "#6b7a8c")]
    cells = [f'<div class="bk-app">{icon(key, 56, "circle")}<span>SmarType</span></div>']
    cells += [f'<div class="bk-app"><i style="background:{c}"></i><span>{n}</span></div>' for n, c in others]
    return f'<div class="bk-home{" dark" if dark else ""}">' + "".join(cells) + "</div>"


def _direction(key, title, idea, good, risks, pick=False):
    name = DIRECTIONS[key][0]
    sizes = "".join(f'<div class="bk-sz">{icon(key, s, m)}<span>{lbl}</span></div>' for s, m, lbl in
                    [(96, "squircle", "Samsung"), (96, "rounded", "Rounded"), (48, "circle", "48 dp"), (32, "circle", "32"), (24, "circle", "24")])
    themed = (f'<div class="bk-sz">{icon(key, 56, "circle", mono=True)}<span>Themed, light</span></div>'
              f'<div class="bk-sz">{icon(key, 56, "circle", mono=True, mono_bg="#1E2B2E", mono_fg="#A9D7DE")}<span>Themed, dark</span></div>'
              f'<div class="bk-sz"><span class="bk-status">{notification(key, 24)}{notification(key, 18)}</span><span>Status bar</span></div>')
    badge = ' <span class="tag ready">Recommended</span>' if pick else ""
    return (f'<section class="bk-dir{" pick" if pick else ""}" id="dir-{key}"><div class="bk-hero">{icon(key, 192, "circle")}</div><div class="bk-body">'
            f'<h3>{E(name)}{badge}</h3><p class="bk-idea">{E(title)}</p><p>{E(idea)}</p>'
            f'<div class="bk-row">{sizes}</div><div class="bk-row">{themed}</div><div class="bk-homes">{_home(key, False)}{_home(key, True)}</div>'
            '<div class="bk-pc"><div><h4>Works</h4><ul>' + "".join(f"<li>{E(x)}</li>" for x in good) + '</ul></div><div><h4>Watch out</h4><ul>' +
            "".join(f"<li>{E(x)}</li>" for x in risks) + "</ul></div></div></div></section>")


def _swatch(name, hexv, use, dark_text=False):
    return (f'<div class="bk-sw"><i style="background:{hexv}"></i><b>{E(name)}</b><code>{hexv}</code><span>{E(use)}</span></div>')


def _wordmark(tshare=False, size=44, color=INK):
    t = f'<span class="bk-t">T</span>' if tshare else "T"
    return f'<span class="bk-wm" style="font-size:{size}px;color:{color}">Smar{t}ype</span>'


def _s_compare():
    old = (f'<svg width="200" height="200" style="background:#fff;border-radius:16px" viewBox="0 8 85 90" aria-label="Today\'s S over itself turned 180 degrees"><path d="{S_PATH}" fill="{INK}"/>'
           f'<path d="{S_PATH}" fill="none" stroke="#e5395b" stroke-width=".7" transform="rotate(180 42.5 53.5)"/></svg>')
    new = (f'<svg width="200" height="200" style="background:#fff;border-radius:16px" viewBox="5 5 90 90" aria-label="New S with its two construction ellipses">'
           '<ellipse cx="50" cy="32" rx="19" ry="15" fill="none" stroke="#e5395b" stroke-width=".6" stroke-dasharray="1.5 1"/>'
           '<ellipse cx="50" cy="65" rx="22" ry="18" fill="none" stroke="#e5395b" stroke-width=".6" stroke-dasharray="1.5 1"/>'
           f'<path d="{S2_PATH}" fill="none" stroke="{INK}" stroke-width="{S2_WEIGHT}" stroke-linecap="round"/>'
           f'<path d="{S2_PATH}" fill="none" stroke="#fff" stroke-width=".5"/></svg>')
    return ('<div class="bk-figs">' + _fig(old, "<b>Today.</b> In red, the same S turned 180°: the top bowl is smaller and sits further left, "
                                            "the two ends are cut at different angles, and short straight joins leave small kinks in the spine.") +
            _fig(new, "<b>New.</b> Each bowl is an even ellipse (red), so the curves are smooth and the stroke is one even weight with round ends. "
                      "The top bowl is deliberately smaller than the bottom one, as in the original S: it keeps the S from looking top-heavy and leaves room for the spark.") + "</div>")


def _ai_strip():
    sp = f'<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{SPARK_PATH}"/></svg>'
    return ('<div class="bk-strip">'
            f'<div>{icon("keyai", 72, "squircle")}<span>App icon</span></div>'
            f'<div><span class="bk-aib">{sp}</span><span>Smartbar AI button</span></div>'
            f'<div><span class="bk-chip">{sp}Fix grammar</span><span>Selected style</span></div>'
            '<div><span class="bk-pill">Replace</span><span>Main AI action</span></div>'
            '<div><span class="tag new">Premium</span><span>AI and Premium tags</span></div></div>'
            '<p>One spark shape everywhere (the path in spark.svg) and one blue → mint family. In the app, AI actions use '
            '<code>ai-gradient-start #2AA8E0</code> → <code>ai-gradient-end #4BDCA4</code> with Ink on top (5.1:1 and 7.9:1). '
            'On the white key, the spark uses a deeper version of the same colours so it stays visible. The three-star circle (ic_ai_logo) is retired.</p>')


def brand_body(root):
    keycap = f'<img src="{root}assets/art/logo.png" alt="3D keycap logo from the earlier kit" width="140" height="140" style="border-radius:28px">'
    today = (_fig(icon("today", 140, "circle"), "<b>App icon today.</b> White S and a small star on graphite. Clean, but a plain S in a circle is a common look, nothing says keyboard, and the star disappears below 48 px.") +
             _fig(keycap, "<b>3D keycap, earlier kit.</b> Says keyboard, but it's a raster render: glow, gloss and the striped S turn to noise at 48 px, and the themed-icon tracing is broken.") +
             _fig(AI_LOGO.format(s=140), "<b>AI logo in the app.</b> Three straight stars in a gradient circle (ic_ai_logo).") +
             _fig(SPARK.format(s=140, c="#0b727b"), "<b>Spark on the smartbar.</b> Two curved stars: the AI buttons in the new designs."))
    sparks = (f'<div class="bk-sparks"><div>{STAR.format(s=56, c=SEAGLASS)}<span>App icon star</span></div><div>{AI_LOGO.format(s=56)}<span>AI logo</span></div>'
              f'<div>{SPARK.format(s=56, c="#0b727b")}<span>Smartbar spark</span></div><div><img src="{root}assets/art/logo.png" alt="" width="56" height="56" style="border-radius:12px"><span>Keycap glow star</span></div></div>')
    dirs = (_direction("keyai", "A key: the S is its legend, the spark is its second function.",
                       "A white keycap with a thin light grey lip on a vivid blue → cyan → mint gradient with a soft light from the top left. On real keys the small symbol in the top corner is what a long-press gives you; here it's the AI spark, in a deeper version of the background's gradient, up in the key's top-right corner, so the icon says \"keyboard with AI built in\" in a keyboard's own language.",
                       ["Says \"keyboard\" at any size, and \"AI\" from 48 px up", "The spark is part of the key, not a sticker: different from the floating sparkles other AI apps use", "Written backwards, the S ends at its top tip and flows on into the spark: one movement, typing becoming AI", "Simple vector; the themed icon is the key's silhouette with the S and spark cut out"],
                       ["Below 32 px the spark becomes a dot; the S and the key still read", "Teal backgrounds are common for productivity apps"], pick=True) +
            _direction("caret", "The S, just typed: a text cursor after it.",
                       "Keeps today's graphite and white S, and replaces the floating star with a text cursor in the brand gradient.",
                       ["Keeps what people may already know from today's icon", "The cursor says typing; it can blink in the splash and on the website", "Strong contrast, reads well in a dark row of icons"],
                       ["At 24–32 px, S and cursor can read as \"SI\" or \"S1\"", "Still mostly a letter: says less about a keyboard than A"]) +
            _direction("talk", "A key that speaks: typing and voice in one shape.",
                       "The keycap gets a speech tail, for typing and speaking.",
                       ["Tells the voice story at a glance", "Friendly, distinct colour"],
                       ["A speech bubble reads as a messaging app (chat apps use bubbles)", "People may expect to send messages from it"]))
    variants = ('<div class="bk-row">' + "".join(
        f'<div class="bk-sz">{icon(k, 96, "circle")}{icon(k, 48, "circle")}<span>{lbl}</span></div>' for k, lbl in
        [("keyai", "Spark in the gradient (chosen)"), ("keyai_teal", "Spark in teal"), ("keyai_ink", "Spark in ink"), ("key", "No spark")]) + "</div>"
        '<p>The spark uses a deeper version of the background\'s gradient (#1257A8 → #0E8DA6 → #119A76) with a faint light, so it stands out on the white key and still belongs with the glow around it. It sits in the key\'s top-right corner, just after the S\'s top tip. Teal and ink are calmer alternatives; without the spark the icon says nothing about AI.</p>')
    colour = ('<div class="bk-sws">' +
              _swatch("Glacier", GLACIER, "Gradient start: icon background, AI actions") + _swatch("Seaglass", SEAGLASS, "Gradient end") +
              _swatch("Ink", INK, "Text on the gradient; the S on the key") + _swatch("Porcelain", PORCELAIN, "The key; light surfaces") +
              _swatch("Graphite", GRAPHITE, "Dark surfaces, dark splash") + _swatch("Teal (UI primary)", "#0B727B", "Buttons and links in the app, light theme") + "</div>")
    word = (f'<div class="bk-words"><div class="bk-wcard">{_wordmark()}<span>Plain: Google Sans Flex 600</span></div>'
            f'<div class="bk-wcard">{_wordmark(True)}<span>The T in the gradient: one letter shared by Smart and Type</span></div>'
            f'<div class="bk-wcard dark">{_wordmark(True, color=PORCELAIN)}<span>On graphite</span></div>'
            f'<div class="bk-wcard"><span class="bk-lock">{icon("keyai", 48, "squircle")}{_wordmark(False, 30)}</span><span>Lockup with icon A: icon height = 1.6 × the cap height; gap = half the icon</span></div></div>')
    return (
        '<h1>Brand review</h1><p class="lede">One SmarType mark that works from the Play Store down to the status bar, one spark for AI, and colours that match what the app already uses.</p>'
        '<h2>What we have today</h2><div class="bk-figs">' + today + '</div>'
        '<div class="note" style="margin-top:16px"><b>The problem.</b> Three different marks and four different sparks. The icon a user taps is not the logo in the brand kit, and neither looks like the AI symbol inside the app. The earlier kit also proposed moving the app to blue, but the shipped icon, the AI gradient and the app\'s teal are already one cyan–teal family; the blue keycap is the odd one out.</div>'
        '<h2>Where the mark has to work</h2><div class="tbl"><table><thead><tr><th>Place</th><th>Size</th><th>What it needs</th></tr></thead><tbody>'
        '<tr><td>Play Store listing</td><td>512 × 512 px</td><td>Recognisable next to Gboard, SwiftKey and Grammarly</td></tr>'
        '<tr><td>Home screen and app drawer</td><td>48–56 dp, any launcher shape</td><td>Survives circle, squircle and rounded masks</td></tr>'
        '<tr><td>Themed icons (Android 13+)</td><td>48 dp, one colour</td><td>A clear silhouette</td></tr>'
        '<tr><td>Keyboard picker and settings rows</td><td>24–32 dp</td><td>Still readable when small</td></tr>'
        '<tr><td>Status bar (voice, notes bubble)</td><td>24 dp, white only</td><td>A solid shape, no thin lines</td></tr>'
        '<tr><td>Splash, website, store art</td><td>Large</td><td>Room for motion (a key press, a blinking cursor)</td></tr>'
        '</tbody></table></div>'
        '<h2>Three directions</h2><p>Same colours and the same S for all three, so the comparison is about the idea. Shown at real launcher sizes, as themed icons and in the status bar.</p>' + dirs +
        '<h2>The S</h2>' + _s_compare() +
        '<h2>The spark on the key</h2>' + variants +
        '<h2>The background gradient</h2><div class="bk-row">' + "".join(
            f'<div class="bk-sz">{icon(k, 112, "circle")}{icon(k, 48, "circle")}<span>{lbl}</span></div>' for k, lbl in
            [("keyai_soft", "Soft: today's Glacier → Seaglass"), ("keyai_vivid", "Vivid"), ("keyai", "Vivid with light (chosen)"), ("keyai_deep", "Deep")]) + "</div>"
        '<p>Today\'s soft gradient reads as one flat colour. A wider shift, blue to cyan to mint, is how people recognise AI now, and it makes the white key stand out more, on light and dark home screens. The soft light from the top left gives the background depth, as if the key sits in a glow, while the key itself stays flat.</p>'
        '<div class="tbl"><table><thead><tr><th>Stop</th><th>Colour</th></tr></thead><tbody>'
        '<tr><td>Linear, 135°: 0% (top left)</td><td><code>#1E9BD7</code></td></tr><tr><td>50%</td><td><code>#22C3CF</code></td></tr><tr><td>100% (bottom right)</td><td><code>#4BDCA4</code></td></tr>'
        '<tr><td>Light: radial, centre at the top left of the visible icon, radius 64% of the icon</td><td><code>#FFFFFF</code> at 45% → 0%</td></tr>'
        '</tbody></table></div>'
        '<div class="note" style="margin-top:16px"><b>Everything is vector.</b> The key, its lip, the S, the spark and the gradients are vector paths (SVG here; Android vector drawables in the app), so they stay sharp at every size. The S is the drawn monogram from today\'s icon (ic_smartype_foreground.xml), not a font. Only the 512 px Play Store icon and store art are exported as PNG, from these vectors. The 3D keycap from the earlier kit and the illustrations are the only raster art; the keycap is retired.</div>'
        '<h2>One spark for AI</h2><p>Today: four different stars.</p>' + sparks + '<p style="margin-top:18px">New: the same spark and the same colours from the app icon to every AI action.</p>' + _ai_strip() +
        '<p>Keep one spark: the two curved stars already on the smartbar\'s AI buttons. It appears in two places only: as the corner legend on the logo\'s key, and on AI actions in the app (Rewrite, Translate, Format, voice tidy-up, Premium). Retire the three-star circle (ic_ai_logo) and the straight star on today\'s icon, so there is one spark, and it always means AI.</p>'
        '<h2>Colour</h2><p>Keep the shipped family. The icon, splash and store art use the vivid gradient with light above. Inside the app, AI actions move to the same blue → mint family (#2AA8E0 → #4BDCA4) with Ink icons and text; the teal tokens stay as they are.</p>' + colour +
        '<h2>Wordmark</h2><p>Set in Google Sans Flex, the typeface these designs use. The app still bundles DM Sans (res/font), so the switch the earlier kit proposed is part of this decision. The name\'s capital T is shared by \"Smart\" and \"Type\"; colouring it is optional.</p>' + word +
        '<h2>Your call</h2><div class="tbl"><table><thead><tr><th>Decision</th><th>Recommendation</th></tr></thead><tbody>'
        '<tr><td>Logo direction</td><td>A · Keycap with the AI spark</td></tr>'
        '<tr><td>Spark on the key</td><td>Chosen: deeper gradient #1257A8 → #0E8DA6 → #119A76, in the key\'s top-right corner just after the S\'s tip; S in ink</td></tr>'
        '<tr><td>Key depth</td><td>Lip 2.5 units of 108 (about 5% of the key), light grey #C3D5DA</td></tr>'
        '<tr><td>Icon background</td><td>Chosen: vivid gradient #1E9BD7 → #22C3CF → #4BDCA4 with a soft light</td></tr>'
        '<tr><td>AI buttons in the app</td><td>Move to the brand family: #2AA8E0 → #4BDCA4 with Ink (updated in tokens.json)</td></tr>'
        '<tr><td>The S</td><td>The new S: even, round bowls, a smaller top bowl balanced by the spark, round ends; in the logo, splash and lockup</td></tr>'
        '<tr><td>Wordmark: plain or the T in the gradient</td><td>The gradient T for the website and store art; plain for small sizes and in the app</td></tr>'
        '<tr><td>One spark, AI only</td><td>Yes: the smartbar spark, on the logo\'s key and on AI actions; nothing else uses a spark</td></tr>'
        '<tr><td>Colours</td><td>Keep the cyan–teal family; drop the earlier move to blue</td></tr>'
        '<tr><td>Typeface</td><td>Google Sans Flex for the wordmark and the app, replacing DM Sans (open licence, one variable file)</td></tr>'
        '</tbody></table></div>'
        '<h2>After you choose</h2><ul class="check">'
        '<li>Final vector icon: adaptive foreground, background and monochrome layers, legacy icons, 512 px Play icon, debug and beta badges.</li>'
        '<li>Notification icon, splash (with the key press or cursor animation), favicon and social image.</li>'
        '<li>Wordmark and lockup files (SVG, PNG), clear space and minimum sizes.</li>'
        '<li>A short brand page in the design system: logo, spark, colour, type, do and don\'t.</li>'
        '<li>Then the illustrations, store screenshots, feature graphic and website use it.</li></ul>'
    )
