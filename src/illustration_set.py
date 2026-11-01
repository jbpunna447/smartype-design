"""The illustration set: the brand key as a character, in 12 moments. Shapes drawn straight onto the background in
Ink use var(--ill-ink), which a dark surface sets to a light ink so they stay visible. Heroes are drawn for 200 dp, empty states for
160 dp, all on a 200-unit canvas. Each loops (CSS motion) and has a still frame for reduced motion."""
import math

from brand_marks import INK, LIP, SPARK_PATH
from illustration_concepts import FONT, _glow, _id, _key, _shadow, _spark, _svg
from illustration_merge import AI, _bubble, hello

MINT = "#4BDCA4"
SKY = "#2AA8E0"


# ---------- the face: one function, every expression ----------

def face(x, y, s, mode="watch", look=(0, 0)):
    """The character's face on a key at (x, y), size s. mode: watch, happy, surprised, focus, curious, asleep.
    look shifts the eyes (units of the key's size). Open eyes blink (class 'blink')."""
    ex1, ex2, ey = x + .35 * s, x + .65 * s, y + .40 * s
    rx, ry = .07 * s, .095 * s
    dx, dy = look[0] * s, look[1] * s
    sw = .045 * s
    out = []
    if mode in ("watch", "surprised", "curious", "focus"):
        k = {"surprised": 1.25, "focus": 1}.get(mode, 1)
        sy = .45 if mode == "focus" else 1
        eyes = "".join(f'<ellipse cx="{ex + dx:.1f}" cy="{ey + dy:.1f}" rx="{rx * k:.1f}" ry="{ry * k * sy:.1f}" fill="{INK}"/>'
                       f'<circle cx="{ex + dx + rx * .35:.1f}" cy="{ey + dy - ry * .35 * sy:.1f}" r="{rx * .36:.1f}" fill="#fff"/>' for ex in (ex1, ex2))
        out.append(f'<g class="blink">{eyes}</g>')
    elif mode == "happy":
        out.append("".join(f'<path d="M{ex - rx:.1f} {ey + ry * .3:.1f} q{rx:.1f} {-ry * 1.4:.1f} {2 * rx:.1f} 0" fill="none" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
                           for ex in (ex1, ex2)))
    elif mode == "asleep":
        out.append("".join(f'<path d="M{ex - rx:.1f} {ey:.1f} q{rx:.1f} {ry * .9:.1f} {2 * rx:.1f} 0" fill="none" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
                           for ex in (ex1, ex2)))
    # eyebrows
    if mode == "surprised":
        out.append("".join(f'<path d="M{ex - rx * 1.1:.1f} {ey - ry * 2.1:.1f} q{rx * 1.1:.1f} {-ry * .5:.1f} {rx * 2.2:.1f} 0" fill="none" stroke="{INK}" stroke-width="{.035 * s:.1f}" stroke-linecap="round"/>'
                           for ex in (ex1, ex2)))
    elif mode == "curious":
        out.append(f'<path d="M{ex2 - rx * 1.1:.1f} {ey - ry * 2.1:.1f} q{rx * 1.1:.1f} {-ry * .6:.1f} {rx * 2.2:.1f} -{ry * .1:.1f}" fill="none" stroke="{INK}" stroke-width="{.035 * s:.1f}" stroke-linecap="round"/>'
                   f'<path d="M{ex1 - rx * 1.1:.1f} {ey - ry * 1.5:.1f} h{rx * 2.2:.1f}" fill="none" stroke="{INK}" stroke-width="{.035 * s:.1f}" stroke-linecap="round"/>')
    elif mode == "focus":
        out.append(f'<path d="M{ex1 - rx * 1.1:.1f} {ey - ry * 1.4:.1f} l{rx * 2.2:.1f} {ry * .5:.1f}" stroke="{INK}" stroke-width="{.035 * s:.1f}" stroke-linecap="round"/>'
                   f'<path d="M{ex2 + rx * 1.1:.1f} {ey - ry * 1.4:.1f} l-{rx * 2.2:.1f} {ry * .5:.1f}" stroke="{INK}" stroke-width="{.035 * s:.1f}" stroke-linecap="round"/>')
    # mouth
    mx, my = x + .5 * s, y + .62 * s
    if mode == "surprised":
        out.append(f'<ellipse cx="{mx:.1f}" cy="{my + .02 * s:.1f}" rx="{.045 * s:.1f}" ry="{.06 * s:.1f}" fill="{INK}"/>')
    elif mode == "happy":
        out.append(f'<path d="M{mx - .13 * s:.1f} {my - .03 * s:.1f} q{.13 * s:.1f} {.17 * s:.1f} {.26 * s:.1f} 0" fill="none" stroke="{INK}" stroke-width="{.05 * s:.1f}" stroke-linecap="round"/>')
    elif mode == "asleep":
        out.append(f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="{.03 * s:.1f}" ry="{.035 * s:.1f}" fill="{INK}"/>')
    elif mode in ("curious", "focus"):
        out.append(f'<path d="M{mx - .07 * s:.1f} {my:.1f} q{.07 * s:.1f} {.03 * s:.1f} {.14 * s:.1f} -{.02 * s:.1f}" fill="none" stroke="{INK}" stroke-width="{.045 * s:.1f}" stroke-linecap="round"/>')
    else:
        out.append(f'<path d="M{mx - .10 * s:.1f} {my - .02 * s:.1f} q{.10 * s:.1f} {.11 * s:.1f} {.20 * s:.1f} 0" fill="none" stroke="{INK}" stroke-width="{.05 * s:.1f}" stroke-linecap="round"/>')
    out.append("".join(f'<ellipse cx="{cx:.1f}" cy="{y + .58 * s:.1f}" rx="{.07 * s:.1f}" ry="{.04 * s:.1f}" fill="{MINT}" opacity=".45"/>' for cx in (x + .2 * s, x + .8 * s)))
    return "".join(out)


def character(x, y, s, mode, p, look=(0, 0), cls="body"):
    return f'<g class="{cls}">{_key(x, y, s, p + "k")}{face(x, y, s, mode, look)}</g>'


def scene(p, style, body, size, label, glow_at=(100, 104), still=0):
    common = (f"@keyframes {p}blink {{ 0%,92%,100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(.1); }} }}"
              f" .{p} .blink {{ animation: {p}blink 4s infinite; }}")
    return _svg(p, common + " " + style, _glow(glow_at[0], glow_at[1], 88, p + "g") + body, size, label, still)


def bob(p, name="body", amp=4, dur="3s"):
    return (f"@keyframes {p}{name} {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-{amp}px); }} }}"
            f" .{p} .{name} {{ animation: {p}{name} {dur} ease-in-out infinite; }}")


def hop(p, name="body", dur="2.4s"):
    return (f"@keyframes {p}{name} {{ 0%,60%,100% {{ transform: none; }} 10% {{ transform: translateY(2px) scale(1.05,.93); }}"
            f" 28% {{ transform: translateY(-14px) scale(.97,1.04); }} 46% {{ transform: translateY(0) scale(1.04,.95); }} }}"
            f" .{p} .{name} {{ animation: {p}{name} {dur} cubic-bezier(.3,.7,.4,1) infinite; transform-origin: 50% 100%; }}")


def _gradient(gid, stops, x1, y1, x2, y2):
    return (f'<defs><linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="userSpaceOnUse">'
            + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + "</linearGradient></defs>")


def _card(x, y, w, h, r=14, rot=0):
    t = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
    return (f'<g{t}><rect x="{x}" y="{y + 3}" width="{w}" height="{h}" rx="{r}" fill="{LIP}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FFFFFF"/></g>')


def _line(x, y, w, c=LIP, h=5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{c}"/>'


STILL_AT = {"art_welcome": 7.3, "art_signin": 3.2, "art_done": .8, "art_premium": 0, "art_ai": 3.2, "art_empty_notes": .2,
            "art_empty_styles": 0, "art_empty_search": 2.2, "art_empty_languages": 2.6, "art_empty_themes": 1.1,
            "art_empty_dictionary": 1.4, "art_extension": 0}


# ---------- heroes ----------

def signin(size=200):
    """Sign in: three free tries pop out of a little box, one by one; the key watches, then cheers."""
    p = _id("si")
    T = "4.8s"
    style = (" ".join(f"@keyframes {p}t{i} {{ 0%,{8 + i * 12}% {{ transform: translate(0,0) scale(.2); opacity: 0; }} {16 + i * 12}% {{ opacity: 1; }}"
                      f" {22 + i * 12}%,86% {{ transform: translate({dx}px,{dy}px) scale(1); opacity: 1; }} 94%,100% {{ transform: translate({dx}px,{dy}px) scale(.2); opacity: 0; }} }}"
                      f" .{p} .t{i} {{ animation: {p}t{i} {T} cubic-bezier(.3,1.5,.5,1) infinite; }}" for i, (dx, dy) in enumerate([(-34, -46), (0, -60), (34, -46)])) +
             f" @keyframes {p}lid {{ 0%,6% {{ transform: rotate(0); }} 12%,88% {{ transform: rotate(-28deg); }} 96%,100% {{ transform: rotate(0); }} }}"
             f" .{p} .lid {{ animation: {p}lid {T} cubic-bezier(.3,1.4,.5,1) infinite; transform-origin: 0% 100%; }}"
             f" @keyframes {p}w {{ 0%,48% {{ opacity: 1; }} 52%,92% {{ opacity: 0; }} 100% {{ opacity: 1; }} }} @keyframes {p}h {{ 0%,48% {{ opacity: 0; }} 52%,92% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}"
             f" .{p} .w {{ animation: {p}w {T} infinite; }} .{p} .h {{ animation: {p}h {T} infinite; }}" + " " + hop(p, "hopper", T))
    box = (_gradient(p + "bx", AI, 112, 120, 168, 170) +
           f'<rect x="114" y="132" width="52" height="38" rx="10" fill="url(#{p}bx)"/>'
           f'<g class="lid"><rect x="110" y="122" width="60" height="13" rx="6.5" fill="#FFFFFF"/></g>'
           f'<rect x="138" y="132" width="4" height="38" fill="#FFFFFF" opacity=".75"/>')
    tries = "".join(f'<g transform="translate(140 140)"><g class="t{i}"><circle r="15" fill="#FFFFFF"/><g>{_spark(p + f"s{i}", 18)}</g></g></g>' for i in range(3))
    x, y, s = 30, 98, 66
    body = (_shadow(100, 176, 70, 7, p + "sh") + tries + box +
            f'<g class="hopper">{_key(x, y, s, p + "k")}<g class="w">{face(x, y, s, "watch", (.03, -.03))}</g><g class="h">{face(x, y, s, "happy")}</g></g>')
    return scene(p, style, body, size, "Free AI tries pop out of a box; the key cheers", still=3.2)


def done(size=200):
    """You're all set: the key hops for joy; a check pops above it and little sparks fall like confetti."""
    p = _id("dn")
    T = "2.8s"
    conf = [(46, "#1E9BD7", 0), (70, MINT, .4), (128, SKY, .8), (152, "#22C3CF", .2), (100, MINT, 1.1), (34, "#22C3CF", 1.4), (166, "#1E9BD7", 1.7)]
    style = (hop(p, "body", T) +
             f" @keyframes {p}chk {{ 0%,100% {{ transform: translateY(0) scale(1); }} 28% {{ transform: translateY(-8px) scale(1.12); }} }}"
             f" .{p} .chk {{ animation: {p}chk {T} cubic-bezier(.3,.7,.4,1) infinite; }}"
             f" @keyframes {p}fall {{ 0% {{ transform: translateY(-30px) rotate(0); opacity: 0; }} 15% {{ opacity: 1; }} 100% {{ transform: translateY(150px) rotate(240deg); opacity: 0; }} }}"
             f" .{p} .cf {{ animation: {p}fall 3.2s linear infinite; }}")
    confetti = "".join(f'<rect class="cf" style="animation-delay:-{d}s" x="{cx}" y="24" width="7" height="4" rx="2" fill="{c}"/>' for cx, c, d in conf)
    check = (_gradient(p + "c", AI, 82, 18, 118, 54) +
             f'<g class="chk"><circle cx="100" cy="40" r="20" fill="url(#{p}c)"/><path d="M90 40 l7 7 l14 -14" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    x, y, s = 64, 82, 72
    body = (_shadow(100, 170, 40, 7, p + "sh") + confetti + check + character(x, y, s, "happy", p))
    return scene(p, style, body, size, "The key cheers: you're all set", still=0.8)


def premium(size=200):
    """Premium: the key on a small stage, three sparks orbiting it; it looks up, delighted."""
    p = _id("pr")
    style = (f"@keyframes {p}orb {{ to {{ transform: rotate(360deg); }} }} @keyframes {p}un {{ to {{ transform: rotate(-360deg); }} }}"
             f" .{p} .orb {{ animation: {p}orb 9s linear infinite; transform-box: view-box; transform-origin: 100px 108px; }}"
             f" .{p} .un {{ animation: {p}un 9s linear infinite; }}" + " " + bob(p, "body", 4, "3s"))
    orbit = "".join(f'<g transform="translate({100 + 66 * math.cos(math.radians(a)):.1f} {108 + 30 * math.sin(math.radians(a)):.1f})"><g class="un">{_spark(p + f"o{i}", 20 if i else 26)}</g></g>'
                    for i, a in enumerate((200, 320, 80)))
    stage = (_gradient(p + "st", AI, 52, 150, 148, 176) +
             f'<ellipse cx="100" cy="166" rx="50" ry="12" fill="url(#{p}st)"/><ellipse cx="100" cy="160" rx="50" ry="12" fill="#FFFFFF"/>'
             f'<ellipse cx="100" cy="108" rx="66" ry="30" fill="none" stroke="{SKY}" stroke-width="1.5" stroke-dasharray="3 5" opacity=".6"/>')
    x, y, s = 66, 82, 68
    body = stage + orbit + character(x, y, s, "surprised", p, (0, -.03))
    return scene(p, style, body, size, "The key on a stage with sparks orbiting: Premium", still=0)


def ai(size=200):
    """SmarType AI: the key focuses; messy lines on a card snap into neat, aligned lines with the spark."""
    p = _id("ai")
    T = "4s"
    lines = [(118, 64, 50, 84, 66, 56), (118, 80, 38, 84, 82, 70), (118, 96, 56, 84, 98, 44)]
    style = (" ".join(f"@keyframes {p}l{i} {{ 0%,30% {{ transform: translate({ox - nx}px,{oy - ny}px) rotate({(-1) ** i * 9}deg); }}"
                      f" 46%,88% {{ transform: none; }} 100% {{ transform: translate({ox - nx}px,{oy - ny}px) rotate({(-1) ** i * 9}deg); }} }}"
                      f" .{p} .l{i} {{ animation: {p}l{i} {T} cubic-bezier(.3,1.4,.5,1) infinite; }}" for i, (ox, oy, ow, nx, ny, nw) in enumerate(lines)) +
             f" @keyframes {p}sp {{ 0%,20% {{ transform: scale(.6) rotate(0); }} 34% {{ transform: scale(1.3) rotate(90deg); }} 46%,100% {{ transform: scale(1) rotate(90deg); }} }}"
             f" .{p} .sp {{ animation: {p}sp {T} cubic-bezier(.3,1.4,.5,1) infinite; }}"
             f" @keyframes {p}f {{ 0%,40% {{ opacity: 1; }} 46%,92% {{ opacity: 0; }} 100% {{ opacity: 1; }} }} @keyframes {p}h {{ 0%,40% {{ opacity: 0; }} 46%,92% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}"
             f" .{p} .f {{ animation: {p}f {T} infinite; }} .{p} .h {{ animation: {p}h {T} infinite; }}")
    card = _card(72, 46, 112, 70, 16) + "".join(
        f'<g class="l{i}"><rect x="{nx}" y="{ny}" width="{nw}" height="6" rx="3" fill="{INK if i == 0 else LIP}"/></g>' for i, (ox, oy, ow, nx, ny, nw) in enumerate(lines))
    x, y, s = 24, 104, 66
    body = (_shadow(57, 180, 32, 6, p + "sh") + card + f'<g transform="translate(176 46)"><g class="sp">{_spark(p + "s", 30)}</g></g>' +
            f'<g>{_key(x, y, s, p + "k")}<g class="f">{face(x, y, s, "focus", (.03, -.03))}</g><g class="h">{face(x, y, s, "happy")}</g></g>')
    return scene(p, style, body, size, "Messy lines snap into a neat card as the key focuses", still=3.2)


# ---------- empty states ----------

def notes(size=160):
    """No notes yet: a blank note with a blinking caret; the key watches, ready."""
    p = _id("nt")
    style = (f"@keyframes {p}car {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }} .{p} .car {{ animation: {p}car 1.1s steps(1) infinite; }}" + " " + bob(p, "body", 3, "3.4s"))
    note = _card(80, 34, 96, 118, 16, 4) + f'<rect class="car" x="96" y="58" width="3" height="18" rx="1.5" fill="{SKY}" transform="rotate(4 128 93)"/>'
    x, y, s = 26, 104, 62
    body = _shadow(100, 176, 70, 6, p + "sh") + note + character(x, y, s, "watch", p, (.04, -.03))
    return scene(p, style, body, size, "A blank note waiting, the key watching", still=0.2)


def styles(size=160):
    """No writing styles yet: two style chips float; an empty dashed chip with a plus pulses; the key is curious."""
    p = _id("st")
    style = (f"@keyframes {p}pul {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.08); }} }} .{p} .pul {{ animation: {p}pul 1.8s ease-in-out infinite; }}"
             + " " + bob(p, "c1", 4, "3s") + " " + bob(p, "c2", 5, "3.6s"))
    chips = (_gradient(p + "a", AI, 96, 40, 176, 64) +
             f'<g class="c1"><rect x="98" y="38" width="78" height="26" rx="13" fill="url(#{p}a)"/><text x="137" y="55.5" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}" {FONT}>Polite</text></g>'
             f'<g class="c2"><rect x="88" y="74" width="82" height="26" rx="13" fill="#FFFFFF"/><text x="129" y="91.5" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}" {FONT}>Casual</text></g>'
             f'<g class="pul"><rect x="104" y="112" width="70" height="26" rx="13" fill="none" stroke="{SKY}" stroke-width="2" stroke-dasharray="5 4"/>'
             f'<path d="M139 119 v12 M133 125 h12" stroke="{SKY}" stroke-width="2.5" stroke-linecap="round"/></g>')
    x, y, s = 22, 100, 64
    body = _shadow(54, 176, 32, 6, p + "sh") + chips + character(x, y, s, "curious", p, (.04, .01))
    return scene(p, style, body, size, "An empty style slot and a curious key", still=0)


def search(size=160):
    """No languages found: a magnifier sweeps left and right; the key's eyes follow; a question mark pops."""
    p = _id("se")
    T = "3.6s"
    style = (f"@keyframes {p}mag {{ 0%,100% {{ transform: translateX(-22px) rotate(-8deg); }} 50% {{ transform: translateX(22px) rotate(8deg); }} }}"
             f" .{p} .mag {{ animation: {p}mag {T} ease-in-out infinite; }}"
             f" @keyframes {p}eye {{ 0%,100% {{ transform: translateX(-3px); }} 50% {{ transform: translateX(3px); }} }} .{p} .blink {{ animation: {p}eye {T} ease-in-out infinite; }}"
             f" @keyframes {p}q {{ 0%,40% {{ opacity: 0; transform: translateY(6px) scale(.5); }} 50%,85% {{ opacity: 1; transform: none; }} 100% {{ opacity: 0; }} }}"
             f" .{p} .q {{ animation: {p}q {T} cubic-bezier(.3,1.5,.5,1) infinite; }}")
    mag = (f'<g transform="translate(100 56)"><g class="mag"><circle r="22" fill="#FFFFFF" fill-opacity=".7" stroke="var(--ill-ink, {INK})" stroke-width="6"/>'
           f'<path d="M16 16 l14 14" stroke="var(--ill-ink, {INK})" stroke-width="8" stroke-linecap="round"/><path d="M-9 -9 a12 12 0 0 1 10 -4" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></g></g>')
    q = f'<g class="q"><text x="146" y="104" font-size="26" font-weight="700" fill="{SKY}" {FONT}>?</text></g>'
    x, y, s = 66, 100, 64
    body = _shadow(98, 176, 34, 6, p + "sh") + mag + q + character(x, y, s, "curious", p, (0, -.02))
    return scene(p, style, body, size, "A magnifier searching, nothing found", still=2.2)


def languages(size=160):
    """No keyboard languages: a globe turns; letters from different scripts pop out of it; the key looks hopeful."""
    p = _id("lg")
    T = "4.5s"
    letters = [("Aa", -40, -30, 0), ("अ", 0, -48, 1.5), ("あ", 40, -30, 3)]
    style = (f"@keyframes {p}spin {{ to {{ transform: rotate(360deg); }} }} .{p} .mer {{ animation: {p}spin 6s linear infinite; }}" + " " +
             " ".join(f"@keyframes {p}p{i} {{ 0% {{ transform: translate(0,0) scale(.3); opacity: 0; }} 20% {{ opacity: 1; }} 60% {{ transform: translate({dx}px,{dy}px) scale(1); opacity: 1; }}"
                      f" 100% {{ transform: translate({dx}px,{dy - 10}px) scale(1); opacity: 0; }} }} .{p} .p{i} {{ animation: {p}p{i} {T} ease-out infinite; animation-delay: -{d}s; }}"
                      for i, (t, dx, dy, d) in enumerate(letters)))
    globe = (_gradient(p + "gl", AI, 116, 72, 168, 124) +
             f'<circle cx="142" cy="98" r="26" fill="url(#{p}gl)"/>'
             f'<g fill="none" stroke="{INK}" stroke-width="2.5" opacity=".8"><circle cx="142" cy="98" r="26"/><path d="M116 98 h52 M120 85 h44 M120 111 h44"/>'
             f'<g class="mer"><ellipse cx="142" cy="98" rx="11" ry="26"/></g></g>')
    pops = "".join(f'<g transform="translate(142 92)"><g class="p{i}"><rect x="-15" y="-12" width="30" height="24" rx="12" fill="#FFFFFF"/>'
                   f'<text y="5" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}" {FONT}>{t}</text></g></g>' for i, (t, *_ ) in enumerate(letters))
    x, y, s = 26, 102, 64
    body = _shadow(100, 176, 70, 6, p + "sh") + pops + globe + character(x, y, s, "watch", p, (.04, -.03))
    return scene(p, style, body, size, "A globe with letters from many scripts", still=2.6)


def themes(size=160):
    """No custom themes: colour swatches circle the key, and its face takes on each colour in turn; it's delighted."""
    p = _id("th")
    T = "4.5s"
    sw = [("#1E9BD7", 0), ("#22C3CF", 1.5), (MINT, 3)]
    style = (f"@keyframes {p}orb {{ to {{ transform: rotate(360deg); }} }} .{p} .orb {{ animation: {p}orb 9s linear infinite; transform-box: view-box; transform-origin: 98px 112px; }}"
             f" @keyframes {p}tint {{ 0%,100% {{ fill: #FFFFFF; }} 25% {{ fill: #DCF1FB; }} 50% {{ fill: #D9F7F5; }} 75% {{ fill: #DDF8EC; }} }}"
             f" .{p} .tint {{ animation: {p}tint {T} ease-in-out infinite; }}" + " " + bob(p, "body", 3, "3s"))
    swatches = "".join(f'<g transform="translate({98 + 58 * math.cos(math.radians(a)):.1f} {112 + 40 * math.sin(math.radians(a)):.1f})">'
                       f'<rect x="-11" y="-14" width="22" height="28" rx="7" fill="{c}" transform="rotate({a / 6:.0f})"/></g>' for (c, _), a in zip(sw, (200, 320, 80)))
    x, y, s = 66, 80, 64
    face_bg = f'<rect class="tint" x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * .24:.1f}" fill="#FFFFFF"/>'
    body = (_shadow(98, 168, 36, 6, p + "sh") + f'<g class="orb">{swatches}</g>' +
            f'<g class="body">{_key(x, y, s, p + "k")}{face_bg}{face(x, y, s, "surprised")}</g>')
    return scene(p, style, body, size, "Colour swatches circle the key and tint its face", still=1.1)


def dictionary(size=160):
    """Empty dictionary: the key naps against an open book with blank pages; little z's drift up."""
    p = _id("dc")
    style = (" ".join(f"@keyframes {p}z{i} {{ 0% {{ transform: translate(0,0) scale(.5); opacity: 0; }} 25% {{ opacity: 1; }} 100% {{ transform: translate({8 + i * 4}px,-34px) scale(1); opacity: 0; }} }}"
                      f" .{p} .z{i} {{ animation: {p}z{i} 3.6s ease-out infinite; animation-delay: -{i * 1.2}s; }}" for i in range(3)) +
             f" @keyframes {p}br {{ 0%,100% {{ transform: scale(1,1); }} 50% {{ transform: scale(1.02,.97); }} }} .{p} .body {{ animation: {p}br 3.6s ease-in-out infinite; transform-origin: 50% 100%; }}")
    book = (f'<path d="M96 146 q30 -12 44 0 v-64 q-14 -12 -44 0 z" fill="#FFFFFF"/><path d="M140 146 q14 -12 44 0 v-64 q-30 -12 -44 0 z" fill="#FFFFFF"/>'
            f'<path d="M96 150 q30 -12 44 0 q14 -12 44 0" fill="none" stroke="{LIP}" stroke-width="4"/><path d="M140 82 v64" stroke="{LIP}" stroke-width="2"/>'
            + "".join(_line(104 + (40 if j else 0), 96 + i * 12, 26, "#E4EDEF", 4) for i in range(3) for j in range(2)))
    zs = "".join(f'<g transform="translate({70 + i * 2} 86)"><g class="z{i}"><text font-size="{12 + i * 2}" font-weight="700" fill="{SKY}" {FONT}>z</text></g></g>' for i in range(3))
    x, y, s = 26, 98, 64
    body = _shadow(104, 172, 76, 6, p + "sh") + book + f'<g transform="rotate(-6 58 162)">{character(x, y, s, "asleep", p)}</g>' + zs
    return scene(p, style, body, size, "The key naps against an empty book", still=1.4)


def extension(size=160):
    """Extension not found: a puzzle with one piece missing; the empty slot glows; the key is puzzled."""
    p = _id("ex")
    style = (f"@keyframes {p}slot {{ 0%,100% {{ opacity: .5; }} 50% {{ opacity: 1; }} }} .{p} .slot {{ animation: {p}slot 1.8s ease-in-out infinite; }}"
             f" @keyframes {p}q {{ 0%,100% {{ transform: rotate(-10deg) translateY(0); }} 50% {{ transform: rotate(10deg) translateY(-4px); }} }} .{p} .q {{ animation: {p}q 2.4s ease-in-out infinite; }}")
    piece = "M0 0 h14 a6 6 0 1 1 12 0 h14 v14 a6 6 0 1 1 0 12 v14 h-14 a6 6 0 1 0 -12 0 h-14 v-14 a6 6 0 1 0 0 -12 z"
    grid = "".join(f'<path transform="translate({100 + c * 40} {44 + r * 40})" d="{piece}" fill="#FFFFFF" stroke="{LIP}" stroke-width="2"/>'
                   for r in range(2) for c in range(2) if (r, c) != (1, 1))
    slot = f'<path class="slot" transform="translate(140 84)" d="{piece}" fill="none" stroke="{SKY}" stroke-width="2.5" stroke-dasharray="5 4"/>'
    q = f'<g transform="translate(66 74)"><g class="q"><text font-size="24" font-weight="700" fill="{SKY}" {FONT}>?</text></g></g>'
    x, y, s = 22, 100, 64
    body = _shadow(100, 176, 72, 6, p + "sh") + grid + slot + q + character(x, y, s, "curious", p, (.05, -.02))
    return scene(p, style, body, size, "A puzzle with a missing piece; the key is puzzled", still=0)


SET = [
    ("art_welcome", "Welcome", "Setup, first page", 200, hello, "hero"),
    ("art_signin", "Sign in", "Setup, after the first try", 200, signin, "hero"),
    ("art_done", "You're all set", "Setup, last page", 200, done, "hero"),
    ("art_premium", "Premium", "Premium screen", 200, premium, "hero"),
    ("art_ai", "SmarType AI", "AI settings screen", 200, ai, "hero"),
    ("art_empty_notes", "No notes yet", "Notes list", 160, notes, "empty"),
    ("art_empty_styles", "No writing styles yet", "Writing styles", 160, styles, "empty"),
    ("art_empty_search", "No languages found", "Add language search", 160, search, "empty"),
    ("art_empty_languages", "No keyboard languages", "Keyboard languages", 160, languages, "empty"),
    ("art_empty_themes", "No custom themes", "Themes", 160, themes, "empty"),
    ("art_empty_dictionary", "Empty dictionary", "User dictionary", 160, dictionary, "empty"),
    ("art_extension", "Extension not found", "Extensions", 160, extension, "empty"),
]
