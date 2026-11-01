"""The brand page: the SmarType logo, how it's built, the one spark, colour, the wordmark and what it replaces."""
import html

from components import ic
from brand_marks import (AI_STOPS, BG_STOPS, GRAPHITE, INK, LIP, PORCELAIN, SPARK_PATH, SPARK_STOPS, ai_badge, icon,
                         notification, spark_mark)

E = html.escape

OLD_AI_LOGO = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-label="Old AI logo"><defs><linearGradient id="oail{s}" x2="24" y2="24" gradientUnits="userSpaceOnUse">'
               '<stop stop-color="#67CEE5"/><stop offset="1" stop-color="#69D4BD"/></linearGradient></defs><circle cx="12" cy="12" r="12" fill="url(#oail{s})"/>'
               '<path fill="#08323B" d="M11.55 10.18 14.88 12l-3.33 1.83-1.82 3.33-1.83-3.33L4.57 12l3.33-1.82 1.83-3.33 1.82 3.33Z'
               'M16.16 6.59l1.69.93-1.69.93-.93 1.69-.92-1.69-1.7-.93 1.7-.93.92-1.69.93 1.69Z'
               'M16.16 15.56l1.69.92-1.69.93-.93 1.7-.92-1.7-1.7-.93 1.7-.92.92-1.7.93 1.7Z"/></svg>')


def _sz(inner, label):
    return f'<div class="bk-sz">{inner}<span>{E(label)}</span></div>'


def _home(dark):
    others = [("Phone", "#5f8f6b"), ("Photos", "#c98b53"), ("Camera", "#6b7a8c")]
    cells = [f'<div class="bk-app">{icon(56, "circle")}<span>SmarType</span></div>']
    cells += [f'<div class="bk-app"><i style="background:{c}"></i><span>{n}</span></div>' for n, c in others]
    return f'<div class="bk-home{" dark" if dark else ""}">' + "".join(cells) + "</div>"


def _grad_css(stops, angle=135):
    return f"linear-gradient({angle}deg, " + ", ".join(f"{c} {o * 100:.0f}%" for o, c in stops) + ")"


def _swatch(name, css, code, use):
    return f'<div class="bk-sw"><i style="background:{css}"></i><b>{E(name)}</b><code>{E(code)}</code><span>{E(use)}</span></div>'


def _spark_inline(size=20):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{SPARK_PATH}"/></svg>'


def _logo():
    sizes = "".join(_sz(icon(s, m), lbl) for s, m, lbl in
                    [(96, "squircle", "Samsung"), (96, "rounded", "Rounded"), (48, "circle", "48 dp"), (32, "circle", "32"), (24, "circle", "24")])
    themed = (_sz(icon(56, mono=True), "Themed, light") + _sz(icon(56, mono=True, mono_bg="#1E2B2E", mono_fg="#A9D7DE"), "Themed, dark") +
              _sz(f'<span class="bk-status">{notification(24)}{notification(18)}</span>', "Status bar"))
    return ('<section class="bk-dir pick"><div class="bk-hero">' + icon(192, "circle") + '</div><div class="bk-body">'
            '<p class="bk-idea">A key: the S is its legend, the spark is its second function.</p>'
            '<p>A white keycap on a vivid blue → cyan → mint gradient. The S has voice bars cut inside its tail, and the AI spark sits in the key\'s '
            'top-right corner, where real keys show what a long-press gives you. Typing, voice and AI in one mark.</p>'
            f'<div class="bk-row">{sizes}</div><div class="bk-row">{themed}</div><div class="bk-homes">{_home(False)}{_home(True)}</div></div></section>')


def _construction():
    rows = [
        ("Canvas", "Android adaptive icon: 108 × 108; launchers show the middle 72 × 72 in their own shape"),
        ("Background", "Linear 135°: #1E9BD7 → #22C3CF (50%) → #4BDCA4, over the visible 72 × 72. Soft light: radial white from (34, 26), radius 46, 45% → 0%"),
        ("Key", "Top face x 31–77, y 29–75 (46 × 46), corner radius 11, white → #EDF3F5 top to bottom. Lip: the same shape 2.5 lower, #C3D5DA"),
        ("S", "Google Sans Flex, weight 700, roundness 100, optical size 144, converted to a vector path (OFL). 29 tall, centred at (51, 54), Ink #08323B"),
        ("Voice bars", "Four slots 1.1 wide with 1.1 bars between them, in the S's tail, starting 10% below its centre. A 0.9 rim is kept along the S's outline"),
        ("Spark", "The one spark (spark.svg) at 70%: its big star centred 13.5 right and 14 above the S's centre. Deep gradient #1257A8 → #0E8DA6 → #119A76 with a faint light"),
        ("Themed icon", "The key's silhouette with the S, voice bars and spark cut out; Android tints it"),
        ("Status bar icon (24 dp)", "Same silhouette with a solid S: the bars would vanish at that size"),
    ]
    return ('<div class="tbl"><table><thead><tr><th>Part</th><th>Spec (units of the 108 canvas)</th></tr></thead><tbody>' +
            "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in rows) + "</tbody></table></div>"
            '<div class="note" style="margin-top:14px"><b>Everything is vector.</b> Key, lip, S, bars, spark and gradients are vector shapes. '
            'Only the 512 px Play Store icon and store art are exported as PNG, from the same vectors.</div>')


def _spark_system(root):
    smartbar = ('<span class="bk-kb">' + f'<span class="bk-aib">{_spark_inline()}</span>'
                f'<span class="bk-aib">{ic("translate", size=20)}</span><span class="bk-aib">{ic("format_list_bulleted", size=20)}</span></span>')
    places = (
        _sz(icon(72, "squircle"), "App icon: spark on the key") +
        _sz(ai_badge(72), "AI logo (replaces ic_ai_logo)") +
        _sz(smartbar, "Smartbar: Rewrite, Translate, Format") +
        _sz(f'<span class="bk-chip">{_spark_inline(16)}Fix grammar</span>', "Selected style") +
        _sz('<span class="bk-pill">Replace</span>', "Main AI action") +
        _sz(f'<span class="bk-prem">{_spark_inline(14)}Premium</span>', "Premium badge") +
        _sz(f'<span class="bk-inl">{spark_mark(20)}<span>AI writing</span></span>', "On light: spark alone") +
        _sz(f'<span class="bk-inl dark">{spark_mark(20, on_dark=True)}<span>AI writing</span></span>', "On dark: spark alone"))
    rules = [
        ("Shape", "Always spark.svg: a big four-point star with curved sides and a small one at its top right. Never rotated, stretched or redrawn."),
        ("On the AI gradient", "Ink #08323B. Used by the smartbar's AI buttons, the AI logo, selected style chips and the Premium badge."),
        ("Alone on light surfaces", "The deep gradient #1257A8 → #0E8DA6 → #119A76: the logo's key, AI labels and headings, the website."),
        ("Alone on dark surfaces", "The AI gradient #2AA8E0 → #4BDCA4."),
        ("Size", "At least 12 dp. In a round badge, the spark is 55% of the badge (20 dp in the 36 dp smartbar button)."),
        ("Space", "Keep a quarter of the spark's width clear around it."),
        ("Meaning", "AI only. The AI gradient marks every AI action (Translate, Format and Mic keep their own icons on it); the spark marks AI writing and the brand. Clipboard, Notes and Emoji never use either."),
    ]
    retired = "".join(_sz(x, lbl) for x, lbl in [
        ('<svg width="40" height="40" viewBox="64 13 20 20" aria-hidden="true"><path fill="#69D4BD" d="M74,13 L77,20 L84,23 L77,26 L74,33 L71,26 L64,23 L71,20 Z"/></svg>', "Straight star (old icon)"),
        (OLD_AI_LOGO.format(s=40), "Three stars (ic_ai_logo)"),
        (f'<img src="{root}assets/art/keycap-3d.png" alt="" width="40" height="40" style="border-radius:9px">', "Glowing star (3D keycap)"),
    ])
    return ('<div class="bk-strip">' + places + "</div>"
            '<div class="tbl" style="margin-top:16px"><table><thead><tr><th>Rule</th><th>Spec</th></tr></thead><tbody>' +
            "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in rules) + "</tbody></table></div>"
            '<h3 style="margin-top:22px">Retired</h3><div class="bk-row">' + retired + "</div>")


def _colour():
    return ('<div class="bk-sws">' +
            _swatch("Icon background", _grad_css(BG_STOPS), "#1E9BD7 → #22C3CF → #4BDCA4", "App icon, splash, store art, website hero") +
            _swatch("Spark on light", _grad_css(SPARK_STOPS), "#1257A8 → #0E8DA6 → #119A76", "The spark alone on white or light surfaces") +
            _swatch("AI gradient", _grad_css(AI_STOPS), "#2AA8E0 → #4BDCA4", "AI actions in the app (ai-gradient tokens); the spark on dark") +
            _swatch("Ink", INK, INK, "The S; text and the spark on the AI gradient") +
            _swatch("Porcelain", PORCELAIN, PORCELAIN, "Light surfaces") +
            _swatch("Graphite", GRAPHITE, GRAPHITE, "Dark surfaces, dark splash") +
            _swatch("Lip", LIP, LIP, "The key's lip") +
            _swatch("Teal (UI primary)", "#0B727B", "#0B727B", "Buttons and links in the app, light theme") + "</div>")


def _wordmarks(root):
    def img(name, h, alt="SmarType"):
        return f'<img src="{root}assets/brand/{name}.svg" alt="{alt}" height="{h}" style="display:block;max-width:100%">'
    return (f'<div class="bk-words"><div class="bk-wcard">{img("wordmark-ink", 40)}<span>Wordmark: in the app and at small sizes</span></div>'
            f'<div class="bk-wcard">{img("wordmark-ink-gradient-t", 40)}<span>The T in the gradient (one letter shared by Smart and Type): website and store art</span></div>'
            f'<div class="bk-wcard dark">{img("wordmark-porcelain-gradient-t", 40)}<span>On graphite</span></div>'
            f'<div class="bk-wcard">{img("lockup-ink", 46)}<span>Lockup: icon height = 1.6 × the cap height; gap = half the icon</span></div>'
            f'<div class="bk-wcard dark">{img("lockup-porcelain", 46)}<span>Lockup on graphite</span></div></div>')


def brand_body(root):
    keycap = f'<img src="{root}assets/art/keycap-3d.png" alt="" width="64" height="64" style="border-radius:14px">'
    replaces = "".join(_sz(x, lbl) for x, lbl in [
        (icon(64, which="today"), "App icon today"), (keycap, "3D keycap (earlier kit)"), (OLD_AI_LOGO.format(s=64), "AI logo today")])
    return (
        '<h1>Brand</h1><p class="lede">One SmarType mark from the Play Store down to the status bar, one spark for AI, '
        'and one colour family from the app icon to every AI button.</p>'
        '<h2>The logo</h2>' + _logo() +
        '<h2>How it\'s built</h2>' + _construction() +
        '<h2>One spark</h2><p>The same spark everywhere SmarType means AI, in two forms: in Ink on the AI gradient, or alone in a gradient. '
        'Nothing else in the product uses a star.</p>' + _spark_system(root) +
        '<h2>Colour</h2>' + _colour() +
        '<h2>Wordmark</h2><p>Google Sans Flex at weight 600, the standard (not rounded) style, with the font\'s own S, outlined. '
        'It stays separate from the logo: the two only appear together in the lockup. The app still bundles DM Sans; moving the app to Google Sans Flex goes with this.</p>' + _wordmarks(root) +
        '<h2>What it replaces</h2><div class="bk-row">' + replaces + "</div>"
        '<p>Today there are three different marks and four different stars. All of them are replaced by the logo and the one spark above.</p>'
        '<h2>Icon kit</h2><p>Built from these vectors by <code>tools/build_icon_kit.py</code>. '
        '<a href="downloads/smartype-brand-assets.zip" download>Download smartype-brand-assets.zip</a> (with a README on where each file goes in the app).</p>'
        '<div class="tbl"><table><thead><tr><th>File</th><th>What it is</th></tr></thead><tbody>'
        '<tr><td><code>android/drawable/ic_launcher_background.xml</code>, <code>ic_launcher_foreground.xml</code>, <code>ic_launcher_monochrome.xml</code></td><td>Adaptive icon layers and the themed icon, as vector drawables</td></tr>'
        '<tr><td><code>android/drawable/ic_launcher_foreground_debug.xml</code>, <code>…_beta.xml</code></td><td>The foreground with a DEV or BETA badge</td></tr>'
        '<tr><td><code>android/mipmap-anydpi-v26/ic_launcher*.xml</code></td><td>Adaptive icons for release, debug and beta, with round versions</td></tr>'
        '<tr><td><code>android/drawable/ic_stat_smartype.xml</code></td><td>Status-bar icon, 24 dp, white, solid S</td></tr>'
        '<tr><td><code>android/drawable/ic_smartype_splash.xml</code></td><td>Splash icon: the icon in a circle of two thirds of the canvas</td></tr>'
        '<tr><td><code>png/play-store-icon-512.png</code></td><td>Play Store icon, 512 × 512, 32-bit PNG, full square</td></tr>'
        '<tr><td><code>web/</code></td><td>favicon.svg, favicon-16/32, apple-touch-icon, icon-192/512, maskable 512, site.webmanifest</td></tr>'
        '<tr><td><code>svg/</code></td><td>Icon masters (full, rounded, each layer), wordmark (ink, porcelain, gradient T) and lockups, all outlined</td></tr>'
        '<tr><td><code>png/lockup-*.png</code>, <code>icon-rounded-1024.png</code></td><td>Lockups and a large icon for documents and slides</td></tr>'
        '</tbody></table></div>'
    )
