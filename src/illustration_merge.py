"""The merged concept: the key, alive and in action. The brand key is the character, and it performs the product's
moments: it comes out of the logo (the S squashes into its smile), fixes a typo, translates, and listens.
Each scene is an animated SVG (CSS motion) with a still frame for reduced motion."""
from brand_marks import INK, _s_voice
from illustration_concepts import FONT, _glow, _id, _key, _shadow, _spark, _svg

AI = [(0, "#2AA8E0"), (1, "#4BDCA4")]


def _face(x, y, s, p, look=True, eyes_cls="eyes"):
    """Eyes and smile for a key at (x, y), size s. The eyes sit in a group that can look around and blink."""
    ex1, ex2, ey = x + .36 * s, x + .64 * s, y + .40 * s
    rx, ry = .06 * s, .085 * s
    eyes = (f'<g class="{eyes_cls}"><g class="blink"><ellipse cx="{ex1:.1f}" cy="{ey:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{INK}"/>'
            f'<ellipse cx="{ex2:.1f}" cy="{ey:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{INK}"/></g></g>')
    smile = (f'<path class="smile" d="M{x + .40 * s:.1f} {y + .58 * s:.1f} q{.10 * s:.1f} {.11 * s:.1f} {.20 * s:.1f} 0" fill="none" stroke="{INK}" '
             f'stroke-width="{.05 * s:.1f}" stroke-linecap="round" pathLength="1"/>')
    cheeks = (f'<g class="cheeks"><ellipse cx="{x + .25 * s:.1f}" cy="{y + .56 * s:.1f}" rx="{.07 * s:.1f}" ry="{.04 * s:.1f}" fill="#4BDCA4" opacity=".45"/>'
              f'<ellipse cx="{x + .75 * s:.1f}" cy="{y + .56 * s:.1f}" rx="{.07 * s:.1f}" ry="{.04 * s:.1f}" fill="#4BDCA4" opacity=".45"/></g>')
    return eyes + smile + cheeks


def _logo_s(x, y, s, gid):
    """The logo's S with its voice bars, on a key at (x, y), size s, exactly as on the app icon."""
    k = s / 46
    return f'<g transform="translate({x - 31 * k:.2f} {y - 29 * k:.2f}) scale({k:.4f})">{_s_voice(gid, INK)}</g>'


def _bubble(x, y, w, h, tail="left"):
    t = (f"l-12 11 l2 -11" if tail == "left" else "l12 11 l-2 -11")
    tx = x + 26 if tail == "left" else x + w - 26
    return (f'<path d="M{x + 14} {y} h{w - 28} a14 14 0 0 1 14 14 v{h - 28} a14 14 0 0 1 -14 14 H{tx} {t} H{x + 14} '
            f'a14 14 0 0 1 -14 -14 v-{h - 28} a14 14 0 0 1 14 -14 z" fill="#FFFFFF"/>')


# ---------- 1 · From logo to friend ----------

def origin(size=240):
    """The app icon's key comes alive: the S squashes into a smile, eyes pop open, the spark jumps up as an idea."""
    p = _id("or")
    T = "5.6s"
    style = (f"@keyframes {p}s {{ 0%,22% {{ opacity: 1; transform: none; }} 34%,84% {{ opacity: 0; transform: translateY(14px) scale(.9,.12); }} 96%,100% {{ opacity: 1; transform: none; }} }}"
             f" @keyframes {p}e {{ 0%,28% {{ transform: scale(0); }} 36% {{ transform: scale(1.25); }} 40%,82% {{ transform: scale(1); }} 88%,100% {{ transform: scale(0); }} }}"
             f" @keyframes {p}m {{ 0%,30% {{ stroke-dashoffset: 1; }} 42%,82% {{ stroke-dashoffset: 0; }} 88%,100% {{ stroke-dashoffset: 1; }} }}"
             f" @keyframes {p}c {{ 0%,40% {{ opacity: 0; }} 48%,80% {{ opacity: 1; }} 86%,100% {{ opacity: 0; }} }}"
             f" @keyframes {p}sp {{ 0%,24% {{ transform: translate(0,0) scale(1) rotate(0); }} 36% {{ transform: translate(14px,-30px) scale(1.5) rotate(25deg); }}"
             f" 44%,80% {{ transform: translate(12px,-26px) scale(1.3) rotate(0); }} 92%,100% {{ transform: translate(0,0) scale(1) rotate(0); }} }}"
             f" @keyframes {p}hop {{ 0%,44%,74%,100% {{ transform: none; }} 50% {{ transform: translateY(2px) scale(1.05,.94); }} 58% {{ transform: translateY(-12px) scale(.98,1.03); }} 66% {{ transform: translateY(0) scale(1.03,.97); }} }}"
             f" @keyframes {p}b {{ 0%,68%,74%,100% {{ transform: scaleY(1); }} 71% {{ transform: scaleY(.1); }} }}"
             f" .{p} .s {{ animation: {p}s {T} cubic-bezier(.5,0,.3,1) infinite; transform-origin: 50% 100%; }}"
             f" .{p} .eyes {{ animation: {p}e {T} infinite; }} .{p} .blink {{ animation: {p}b {T} infinite; }}"
             f" .{p} .smile {{ stroke-dasharray: 1; animation: {p}m {T} infinite; }} .{p} .cheeks {{ animation: {p}c {T} infinite; }}"
             f" .{p} .sp {{ animation: {p}sp {T} cubic-bezier(.3,1.4,.5,1) infinite; }} .{p} .hop {{ animation: {p}hop {T} infinite; transform-origin: 50% 100%; }}")
    x, y, s = 54, 58, 92
    body = (_glow(100, 104, 90, p + "g") + _shadow(100, 166, 46, 7, p + "sh") +
            f'<g class="hop">{_key(x, y, s, p + "k")}<g class="s">{_logo_s(x, y, s, p + "ls")}</g>{_face(x, y, s, p)}'
            f'<g transform="translate({x + .728 * s:.1f} {y + .239 * s:.1f})"><g class="sp">{_spark(p + "sp", .365 * s)}</g></g></g>')
    return _svg(p, style, body, size, "The SmarType key comes alive")


# ---------- 2 · Fixing ----------

def fixing(size=240):
    """The key reads a typo, winds up, throws the spark, and smiles when the message is fixed."""
    p = _id("fx")
    T = "4.8s"
    style = (f"@keyframes {p}look {{ 0%,10% {{ transform: none; }} 16%,40% {{ transform: translate(3px,-3px); }} 62%,100% {{ transform: none; }} }}"
             f" @keyframes {p}wind {{ 0%,22%,40%,56%,72%,100% {{ transform: none; }} 28% {{ transform: translateY(3px) scale(1.06,.92); }}"
             f" 34% {{ transform: translateY(-6px) scale(.97,1.04) rotate(-4deg); }} 62% {{ transform: translateY(-10px); }} }}"
             f" @keyframes {p}fly {{ 0%,30% {{ offset-distance: 0%; opacity: 1; transform: scale(1); }} 44% {{ offset-distance: 100%; opacity: 1; transform: scale(1.3) rotate(90deg); }}"
             f" 48%,92% {{ offset-distance: 100%; opacity: 0; transform: scale(.3); }} 100% {{ offset-distance: 0%; opacity: 1; transform: scale(1); }} }}"
             f" @keyframes {p}out {{ 0%,44% {{ opacity: 1; }} 50%,92% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}"
             f" @keyframes {p}in {{ 0%,46% {{ opacity: 0; transform: translateY(3px); }} 54%,92% {{ opacity: 1; transform: none; }} 100% {{ opacity: 0; }} }}"
             f" @keyframes {p}burst {{ 0%,44% {{ opacity: 0; transform: scale(.3); }} 50% {{ opacity: .8; transform: scale(1); }} 62%,100% {{ opacity: 0; transform: scale(1.6); }} }}"
             f" @keyframes {p}grin {{ 0%,52% {{ transform: none; }} 58%,88% {{ transform: scale(1.25,1.35); }} 96%,100% {{ transform: none; }} }}"
             f" .{p} .eyes {{ animation: {p}look {T} infinite; }} .{p} .wind {{ animation: {p}wind {T} cubic-bezier(.4,0,.2,1) infinite; transform-origin: 50% 100%; }}"
             f" .{p} .fly {{ offset-path: path('M58 92 C 70 40, 120 30, 150 52'); offset-rotate: 0deg; animation: {p}fly {T} cubic-bezier(.4,0,.2,1) infinite; }}"
             f" .{p} .out {{ animation: {p}out {T} infinite; }} .{p} .in {{ animation: {p}in {T} infinite; }}"
             f" .{p} .burst {{ animation: {p}burst {T} infinite; }} .{p} .smile {{ animation: {p}grin {T} infinite; }}")
    x, y, s = 26, 104, 70
    bubble = (f'<g transform="translate(0 -6)">{_bubble(54, 34, 138, 52, "left")}'
              f'<g class="out"><text x="68" y="66" font-size="14" font-weight="500" fill="{INK}" {FONT}>runing late sry</text>'
              '<path d="M68 70 q2.5 2.5 5 0 t5 0 t5 0 t5 0 t5 0 t5 0 t5 0 t5 0 t2 0" fill="none" stroke="#E5395B" stroke-width="1.5" stroke-linecap="round"/></g>'
              f'<g class="in"><text x="68" y="66" font-size="13" font-weight="600" fill="{INK}" {FONT}>Running late, sorry!</text></g>'
              f'<g transform="translate(150 52)"><g class="burst"><circle r="14" fill="none" stroke="#2AA8E0" stroke-width="2"/></g></g></g>')
    body = (_glow(110, 110, 88, p + "g") + _shadow(x + s / 2, 186, 34, 6, p + "sh") + bubble +
            f'<g class="wind">{_key(x, y, s, p + "k")}{_face(x, y, s, p)}</g>' + f'<g class="fly">{_spark(p + "sp", 24)}</g>')
    return _svg(p, style, body, size, "The SmarType key fixing a typo")


# ---------- 3 · Translating ----------

def translating(size=240):
    """The key reads a message left to right, then the bubble flips into Hindi."""
    p = _id("tr")
    T = "5.2s"
    style = (f"@keyframes {p}read {{ 0%,8% {{ transform: translate(-3px,-3px); }} 22% {{ transform: translate(3px,-3px); }} 30% {{ transform: translate(-3px,-3px); }}"
             f" 42% {{ transform: translate(3px,-3px); }} 52%,88% {{ transform: translate(0,-1px); }} 100% {{ transform: translate(-3px,-3px); }} }}"
             f" @keyframes {p}flip {{ 0%,44% {{ transform: scaleX(1); }} 50% {{ transform: scaleX(0); }} 56%,94% {{ transform: scaleX(1); }} 100% {{ transform: scaleX(1); }} }}"
             f" @keyframes {p}en {{ 0%,49% {{ opacity: 1; }} 50%,99% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}"
             f" @keyframes {p}hi {{ 0%,49% {{ opacity: 0; }} 50%,99% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}"
             f" @keyframes {p}tag {{ 0%,40% {{ transform: scale(1); }} 46% {{ transform: scale(1.25) rotate(-8deg); }} 54%,100% {{ transform: scale(1); }} }}"
             f" @keyframes {p}nod {{ 0%,52%,64%,100% {{ transform: none; }} 58% {{ transform: translateY(4px) scale(1.04,.95); }} }}"
             f" .{p} .eyes {{ animation: {p}read {T} ease-in-out infinite; }} .{p} .flip {{ animation: {p}flip {T} cubic-bezier(.5,0,.5,1) infinite; }}"
             f" .{p} .en {{ animation: {p}en {T} infinite; }} .{p} .hi {{ animation: {p}hi {T} infinite; }}"
             f" .{p} .tag {{ animation: {p}tag {T} infinite; }} .{p} .nod {{ animation: {p}nod {T} infinite; transform-origin: 50% 100%; }}")
    x, y, s = 104, 106, 70
    bubble = (f'<g class="flip">{_bubble(12, 30, 150, 52, "right")}'
              f'<g class="en"><text x="87" y="62" text-anchor="middle" font-size="15" font-weight="600" fill="{INK}" {FONT}>Running late!</text></g>'
              f'<g class="hi"><text x="87" y="62" text-anchor="middle" font-size="15" font-weight="600" fill="{INK}" {FONT}>देर हो रही है!</text></g></g>')
    tag = (f'<defs><linearGradient id="{p}ai" x1="0" y1="0" x2="1" y2="1">'
           + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in AI) + '</linearGradient></defs>'
           f'<g transform="translate(166 30)"><g class="tag"><circle r="16" fill="url(#{p}ai)"/>'
           f'<text y="5" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}" {FONT}>文A</text></g></g>')
    body = (_glow(100, 110, 88, p + "g") + _shadow(x + s / 2, 186, 34, 6, p + "sh") + bubble + tag +
            f'<g class="nod">{_key(x, y, s, p + "k")}{_face(x, y, s, p)}</g>')
    return _svg(p, style, body, size, "The SmarType key translating a message into Hindi")


# ---------- 4 · Listening ----------

def listening(size=240):
    """The key closes its eyes and listens; its voice bars dance, then become words in a bubble."""
    p = _id("ls")
    T = "5s"
    bars = [(0, .55), (1, .9), (2, .6), (3, 1), (4, .7)]
    style = (f"@keyframes {p}bar {{ 0%,100% {{ transform: scaleY(.35); }} 50% {{ transform: scaleY(1); }} }}"
             f" @keyframes {p}bars {{ 0%,52% {{ opacity: 1; transform: none; }} 62%,92% {{ opacity: 0; transform: translate(30px,-34px) scale(.4); }} 100% {{ opacity: 1; transform: none; }} }}"
             f" @keyframes {p}text {{ 0%,58% {{ opacity: 0; transform: scale(.7); }} 66%,92% {{ opacity: 1; transform: none; }} 100% {{ opacity: 0; }} }}"
             f" @keyframes {p}shut {{ 0%,54% {{ opacity: 1; }} 58%,100% {{ opacity: 0; }} }} @keyframes {p}open {{ 0%,54% {{ opacity: 0; }} 58%,96% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}"
             f" @keyframes {p}sway {{ 0%,100% {{ transform: rotate(-3deg); }} 50% {{ transform: rotate(3deg); }} }}"
             f" .{p} .bar {{ animation: {p}bar .6s ease-in-out infinite; transform-origin: 50% 50%; }}"
             f" .{p} .bars {{ animation: {p}bars {T} cubic-bezier(.4,0,.2,1) infinite; }} .{p} .words {{ animation: {p}text {T} infinite; }}"
             f" .{p} .shut {{ animation: {p}shut {T} infinite; }} .{p} .eyes {{ animation: {p}open {T} infinite; }}"
             f" .{p} .sway {{ animation: {p}sway 1.2s ease-in-out infinite; transform-origin: 50% 100%; }}")
    x, y, s = 30, 100, 76
    closed = (f'<g class="shut" fill="none" stroke="{INK}" stroke-width="{.045 * s:.1f}" stroke-linecap="round">'
              f'<path d="M{x + .30 * s:.1f} {y + .40 * s:.1f} q{.06 * s:.1f} {.06 * s:.1f} {.12 * s:.1f} 0"/>'
              f'<path d="M{x + .58 * s:.1f} {y + .40 * s:.1f} q{.06 * s:.1f} {.06 * s:.1f} {.12 * s:.1f} 0"/></g>')
    barg = "".join(f'<rect class="bar" style="animation-delay:-{i * .13:.2f}s" x="{126 + i * 11}" y="{124 - 22 * h}" width="6" height="{44 * h:.1f}" rx="3" fill="{INK}"/>'
                   for i, h in bars)
    words = (f'<g class="words">{_bubble(70, 28, 120, 46, "left")}'
             f'<text x="130" y="57" text-anchor="middle" font-size="14" font-weight="600" fill="{INK}" {FONT}>On my way!</text></g>')
    body = (_glow(100, 110, 88, p + "g") + _shadow(x + s / 2, 186, 36, 6, p + "sh") + words + f'<g class="bars">{barg}</g>' +
            f'<g class="sway">{_key(x, y, s, p + "k")}{_face(x, y, s, p)}{closed}</g>')
    return _svg(p, style, body, size, "The SmarType key listening and turning speech into words")


SCENES = [
    ("origin", "From logo to friend", origin, "Welcome; splash to onboarding",
     "The app icon's key comes alive: the S squashes down into its smile, the eyes pop open and the spark jumps up as its idea. This is where the character comes from, so people link it to the logo."),
    ("fixing", "Fixing", fixing, "Welcome page 2, Rewrite tips, store art",
     "It reads the typo, winds up and throws the spark; the message is fixed and it grins."),
    ("translating", "Translating", translating, "Translate tips, Languages, store art",
     "Its eyes read the message left to right, then the bubble flips into Hindi with the translate badge."),
    ("listening", "Listening", listening, "Voice permission, voice tips, store art",
     "Eyes closed, swaying, its voice bars dance; they fly up and become words in a bubble."),
]
