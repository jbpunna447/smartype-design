"""Three illustration concepts, each drawn as an animated Welcome illustration (SVG with CSS motion).

A · Moments: tiny before → after scenes from the product. B · The key, alive: the brand key as a character.
C · Expressive playground: bold shapes, tumbling keys and words in many languages, springy motion."""
import math

from brand_marks import BG_STOPS, INK, LIP, SPARK_PATH, SPARK_STOPS

_n = [0]


def _id(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


def _stops(stops, alpha=1):
    return "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{alpha}"/>' for o, c in stops)


def _grad(gid, stops, x1, y1, x2, y2):
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="userSpaceOnUse">{_stops(stops)}</linearGradient>'


def _spark(gid, size, stops=SPARK_STOPS, fill=None):
    """The brand spark centred on (0, 0), `size` wide."""
    k = size / 24
    if fill:
        return f'<path fill="{fill}" transform="scale({k:.4f}) translate(-12 -11)" d="{SPARK_PATH}"/>'
    if stops is SPARK_STOPS:
        # Brand rule: the deep spark gradient on light surfaces; a dark surface swaps in the AI gradient via --sp0..2.
        st = "".join(f'<stop offset="{o}" style="stop-color: var(--sp{i}, {c})"/>' for i, (o, c) in enumerate(stops))
        g = f'<linearGradient id="{gid}" x1="{-9 * k:.2f}" y1="{-9 * k:.2f}" x2="{9 * k:.2f}" y2="{9 * k:.2f}" gradientUnits="userSpaceOnUse">{st}</linearGradient>'
    else:
        g = _grad(gid, stops, -9 * k, -9 * k, 9 * k, 9 * k)
    return (f'<defs>{g}</defs>'
            f'<path fill="url(#{gid})" transform="scale({k:.4f}) translate(-12 -11)" d="{SPARK_PATH}"/>')


def _key(x, y, size, gid, inner=""):
    r = size * .24
    lip = size * .06
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="{y}" x2="0" y2="{y + size}" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDF3F5"/></linearGradient></defs>'
            f'<rect x="{x}" y="{y + lip}" width="{size}" height="{size}" rx="{r}" fill="{LIP}"/>'
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="url(#{gid})"/>{inner}')


def _glow(cx, cy, r, gid, opacity=.3):
    return (f'<defs>{_grad(gid, BG_STOPS, cx - r, cy - r, cx + r, cy + r)}'
            f'<radialGradient id="{gid}f" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse"><stop stop-color="#fff" stop-opacity=".5"/>'
            f'<stop offset=".75" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></radialGradient>'
            f'<mask id="{gid}m"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid}f)"/></mask></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})" opacity="{opacity}" mask="url(#{gid}m)"/>')


def _shadow(cx, cy, rx, ry, gid, cls=""):
    return (f'<defs><radialGradient id="{gid}" cx="0" cy="0" r="1" gradientTransform="translate({cx} {cy}) scale({rx} {ry})">'
            f'<stop stop-color="{INK}" stop-opacity=".22"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>')


FONT = "font-family=\"'Google Sans Flex', 'DM Sans', system-ui, sans-serif\""
STILL = "@media (prefers-reduced-motion: reduce) {{ .{p} * {{ animation: none !important; }} }}"
# With a still time, reduced motion shows the illustration frozen at its key moment instead of its first frame.
STILL_AT = ("@media (prefers-reduced-motion: reduce) {{ .{p} * {{ animation-play-state: paused !important; "
            "animation-delay: -{t}s !important; }} }}")


def _svg(p, style, body, size, label, still=None):
    rm = STILL.format(p=p) if still is None else STILL_AT.format(p=p, t=still)
    return (f'<svg class="{p}" width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="{label}">'
            f'<style>.{p} [class] {{ transform-box: fill-box; transform-origin: center; }} {style} {rm}</style>{body}</svg>')


# ---------- A · Moments ----------

def moments(size=240):
    """A typo in a chat bubble; the spark leaves the smartbar's Rewrite button and the message is fixed."""
    p = _id("ma")
    style = (f"@keyframes {p}fly {{ 0%,28% {{ offset-distance: 0%; opacity: 0; transform: scale(.6); }} 32% {{ opacity: 1; }}"
             f" 46% {{ offset-distance: 100%; opacity: 1; transform: scale(1.15); }} 52%,100% {{ offset-distance: 100%; opacity: 0; transform: scale(.4); }} }}"
             f" @keyframes {p}out {{ 0%,46% {{ opacity: 1; }} 52%,92% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}"
             f" @keyframes {p}in {{ 0%,48% {{ opacity: 0; transform: translateY(3px); }} 56%,92% {{ opacity: 1; transform: none; }} 100% {{ opacity: 0; }} }}"
             f" @keyframes {p}tap {{ 0%,20% {{ transform: scale(1); }} 25% {{ transform: scale(.86); }} 30%,100% {{ transform: scale(1); }} }}"
             f" @keyframes {p}burst {{ 0%,46% {{ opacity: 0; transform: scale(.3); }} 52% {{ opacity: 1; transform: scale(1); }} 64%,100% {{ opacity: 0; transform: scale(1.5); }} }}"
             f" .{p} .fly {{ offset-path: path('M54 146 C 60 100, 140 110, 160 60'); animation: {p}fly 4.2s cubic-bezier(.4,0,.2,1) infinite; }}"
             f" .{p} .out {{ animation: {p}out 4.2s infinite; }} .{p} .in {{ animation: {p}in 4.2s infinite; }}"
             f" .{p} .tap {{ animation: {p}tap 4.2s infinite; }} .{p} .burst {{ animation: {p}burst 4.2s infinite; }}")
    bar = ('<rect x="16" y="124" width="168" height="44" rx="22" fill="#FFFFFF"/><rect x="16" y="166" width="168" height="4" rx="2" fill="' + LIP + '"/>'
           f'<defs>{_grad(p + "ai", [(0, "#2AA8E0"), (1, "#4BDCA4")], 36, 128, 72, 164)}</defs>'
           f'<g class="tap"><circle cx="54" cy="146" r="15" fill="url(#{p}ai)"/><g transform="translate(54 146)">{_spark(p + "s0", 16, fill=INK)}</g></g>'
           f'<circle cx="92" cy="146" r="15" fill="url(#{p}ai)" opacity=".85"/><text x="92" y="151" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}" {FONT}>文A</text>'
           f'<rect x="120" y="140" width="22" height="4" rx="2" fill="{LIP}"/><rect x="120" y="148" width="14" height="4" rx="2" fill="{LIP}"/>'
           f'<circle cx="164" cy="146" r="15" fill="url(#{p}ai)" opacity=".85"/>'
           f'<g fill="{INK}"><rect x="158" y="140" width="3" height="12" rx="1.5"/><rect x="163" y="136" width="3" height="20" rx="1.5"/><rect x="168" y="141" width="3" height="10" rx="1.5"/></g>')
    bubble = (f'<path d="M30 34 h140 a16 16 0 0 1 16 16 v22 a16 16 0 0 1 -16 16 h-112 l-14 12 l2 -12 h-16 a16 16 0 0 1 -16 -16 v-22 a16 16 0 0 1 16 -16 z" fill="#FFFFFF"/>'
              f'<g class="out"><text x="28" y="66" font-size="15" font-weight="500" fill="{INK}" {FONT}>im runing late sry</text>'
              '<path d="M58 70 q3 3 6 0 t6 0 t6 0 t6 0 t6 0 t6 0" fill="none" stroke="#E5395B" stroke-width="1.6" stroke-linecap="round"/></g>'
              f'<g class="in"><text x="28" y="66" font-size="15" font-weight="600" fill="{INK}" {FONT}>I\'m running late, sorry!</text></g>')
    burst = f'<g class="burst" transform="translate(160 56)"><circle r="14" fill="none" stroke="#2AA8E0" stroke-width="2" opacity=".6"/></g>'
    body = (_glow(100, 100, 92, p + "g") + bubble + bar + burst + f'<g class="fly">{_spark(p + "s1", 22)}</g>')
    return _svg(p, style, body, size, "A typo fixed by the AI spark")


# ---------- B · The key, alive ----------

def alive(size=240):
    """The brand key as a character: it hops, blinks, and its spark lights up like an idea."""
    p = _id("ka")
    style = (f"@keyframes {p}hop {{ 0%,100% {{ transform: translateY(0) scale(1,1); }} 12% {{ transform: translateY(2px) scale(1.06,.92); }}"
             f" 32% {{ transform: translateY(-16px) scale(.97,1.04); }} 50% {{ transform: translateY(0) scale(1.04,.95); }} 60% {{ transform: translateY(0) scale(1,1); }} }}"
             f" @keyframes {p}sh {{ 0%,100%,60% {{ transform: scale(1); opacity: 1; }} 32% {{ transform: scale(.7); opacity: .6; }} }}"
             f" @keyframes {p}blink {{ 0%,78%,86%,100% {{ transform: scaleY(1); }} 82% {{ transform: scaleY(.1); }} }}"
             f" @keyframes {p}idea {{ 0%,30% {{ opacity: 0; transform: translate(0,6px) scale(.4) rotate(-30deg); }} 42% {{ opacity: 1; transform: translate(0,0) scale(1.15) rotate(0); }}"
             f" 52%,88% {{ opacity: 1; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(.6); }} }}"
             f" @keyframes {p}hi {{ 0%,40% {{ opacity: 0; transform: scale(.5); }} 48% {{ opacity: 1; transform: scale(1.08); }} 54%,88% {{ opacity: 1; transform: scale(1); }} 96%,100% {{ opacity: 0; transform: scale(.8); }} }}"
             f" .{p} .hop {{ animation: {p}hop 3.6s cubic-bezier(.3,.7,.4,1) infinite; transform-origin: 50% 100%; }}"
             f" .{p} .sh {{ animation: {p}sh 3.6s infinite; }} .{p} .eye {{ animation: {p}blink 3.6s infinite; }}"
             f" .{p} .idea {{ animation: {p}idea 3.6s infinite; }} .{p} .hi {{ animation: {p}hi 3.6s infinite; }}")
    face = (f'<g fill="{INK}"><ellipse class="eye" cx="84" cy="112" rx="5" ry="7"/><ellipse class="eye" cx="112" cy="112" rx="5" ry="7"/></g>'
            f'<path d="M88 128 q10 9 20 0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            '<ellipse cx="74" cy="126" rx="6" ry="3.5" fill="#4BDCA4" opacity=".45"/><ellipse cx="122" cy="126" rx="6" ry="3.5" fill="#4BDCA4" opacity=".45"/>')
    body = (_glow(100, 104, 90, p + "g") + _shadow(98, 168, 42, 7, p + "sd", "sh") +
            f'<g class="hop">{_key(56, 82, 84, p + "k", face)}</g>'
            f'<g class="idea" transform="translate(150 66)">{_spark(p + "s", 34)}</g>'
            f'<g class="hi"><path d="M24 50 h46 a12 12 0 0 1 12 12 v10 a12 12 0 0 1 -12 12 h-24 l-10 9 l1 -9 h-13 a12 12 0 0 1 -12 -12 v-10 a12 12 0 0 1 12 -12 z" fill="#FFFFFF"/>'
            f'<text x="47" y="74" text-anchor="middle" font-size="16" font-weight="700" fill="{INK}" {FONT}>Hi!</text></g>')
    return _svg(p, style, body, size, "The SmarType key saying hi")


# ---------- C · Expressive playground ----------

def _cookie(cx, cy, r, waves=9, depth=.075):
    pts = []
    for i in range(181):
        t = 2 * math.pi * i / 180
        rr = r * (1 + depth * math.cos(waves * t))
        pts.append(f"{cx + rr * math.cos(t):.2f},{cy + rr * math.sin(t):.2f}")
    return "M" + " L".join(pts) + "Z"


def playground(size=240):
    """Bold shapes and words in many languages orbiting tumbling keys; everything springs."""
    p = _id("pg")
    words = [("hello", 0), ("नमस्ते", 90), ("hola", 180), ("வணக்கம்", 270)]
    style = (f"@keyframes {p}spin {{ to {{ transform: rotate(360deg); }} }} @keyframes {p}unspin {{ to {{ transform: rotate(-360deg); }} }}"
             f" @keyframes {p}bob {{ 0%,100% {{ transform: translateY(0) rotate(var(--r)); }} 50% {{ transform: translateY(-7px) rotate(calc(var(--r) * -1)); }} }}"
             f" @keyframes {p}pop {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.18) rotate(20deg); }} }}"
             f" .{p} .cookie {{ animation: {p}spin 24s linear infinite; }}"
             f" .{p} .orbit {{ animation: {p}spin 16s linear infinite; transform-box: view-box; transform-origin: 100px 100px; }}"
             f" .{p} .chip {{ animation: {p}unspin 16s linear infinite; }}"
             f" .{p} .bob {{ animation: {p}bob 2.4s cubic-bezier(.4,0,.2,1) infinite; }} .{p} .pop {{ animation: {p}pop 2.4s ease-in-out infinite; }}")
    chips = ""
    for w, ang in words:
        a = math.radians(ang - 90)
        x, y = 100 + 62 * math.cos(a), 100 + 62 * math.sin(a)
        wd = 12 + 7.5 * len(w) if w.isascii() else 58
        chips += (f'<g transform="translate({x:.1f} {y:.1f})"><g class="chip"><rect x="{-wd / 2:.1f}" y="-13" width="{wd:.1f}" height="26" rx="13" fill="#FFFFFF"/>'
                  f'<text y="4.5" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}" {FONT}>{w}</text></g></g>')
    keys = ""
    for i, (x, y, s, r, ch, d) in enumerate([(52, 82, 44, -12, "A", 0), (104, 70, 50, 8, "a", .3), (78, 116, 46, 4, "あ", .6)]):
        keys += (f'<g class="bob" style="--r:{r}deg; animation-delay:-{d}s">' +
                 _key(x, y, s, f"{p}k{i}", f'<text x="{x + s / 2}" y="{y + s * .66}" text-anchor="middle" font-size="{s * .5:.0f}" font-weight="700" fill="{INK}" {FONT}>{ch}</text>') + "</g>")
    body = (f'<defs>{_grad(p + "c", BG_STOPS, 30, 30, 170, 170)}</defs>'
            f'<g class="cookie"><path d="{_cookie(100, 100, 52)}" fill="url(#{p}c)" opacity=".9"/></g>' +
            f'<g class="orbit">{chips}</g>' + keys +
            f'<g transform="translate(150 70)"><g class="pop">{_spark(p + "s", 30)}</g></g>')
    return _svg(p, style, body, size, "Keys and words in many languages")


CONCEPTS = [
    ("moments", "A · Moments", moments,
     "Each illustration is a tiny before → after scene from the product: a typo fixed by the spark, a voice note turning into words, a message flipping into Hindi. The life comes from something happening, and it teaches what SmarType does while it delights.",
     ["Explains the product at a glance; doubles as a hint on what to tap", "Every scene reuses real UI (bubbles, smartbar, keys), so it stays true to the app",
      "Loops of 3–5 s work as Lottie files in the app and as video in the store"],
     ["Needs care to stay simple: one change per scene", "Text inside art must be localised or kept to universal content"]),
    ("alive", "B · The key, alive", alive,
     "The brand key becomes a small character: it hops, blinks and gets an idea (the spark). Each screen gives it a pose: waving hello, holding a note, searching with a magnifier, asleep on an empty list.",
     ["Most emotion and personality; memorable and easy to recognise", "One character carries the whole set, store art and website",
      "Empty states and errors feel friendly instead of blank"],
     ["Can feel childish if overdone: keep the face to two eyes and a smile", "Competes a little with the logo's key; the character has no S"]),
    ("playground", "C · Expressive playground", playground,
     "Bold, springy compositions in the spirit of Google's Material 3 Expressive: a big scalloped shape in the brand gradient, keys tumbling, words in English, Hindi, Spanish and Tamil orbiting, the spark popping.",
     ["Feels native to modern Android; energetic and premium", "Shows multilingual typing without words of explanation",
      "Easy to make a set: same parts, new arrangement"],
     ["More abstract: says less about what each screen does", "Lots of motion; needs a calm still frame for reduced motion"]),
]
