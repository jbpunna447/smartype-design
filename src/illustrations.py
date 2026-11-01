"""Flat vector illustrations built from the brand's own shapes: the white key with its lip, the spark, voice bars,
suggestion pills and a soft glow in the brand gradient. Each one works on light and dark surfaces."""
from brand_marks import BG_STOPS, INK, LIP, SPARK_PATH, SPARK_STOPS

_n = [0]


def _id(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


def _stops(stops, alpha=1):
    return "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{alpha}"/>' for o, c in stops)


def glow(cx, cy, r, gid):
    """A soft disc in the brand gradient behind the subject: it gives white shapes an edge on light surfaces."""
    return (f'<defs><linearGradient id="{gid}" x1="{cx - r}" y1="{cy - r}" x2="{cx + r}" y2="{cy + r}" gradientUnits="userSpaceOnUse">{_stops(BG_STOPS)}</linearGradient>'
            f'<radialGradient id="{gid}f" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse"><stop stop-color="#fff" stop-opacity=".55"/>'
            f'<stop offset=".7" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></radialGradient>'
            f'<mask id="{gid}m"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid}f)"/></mask></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})" opacity=".32" mask="url(#{gid}m)"/>')


def shadow(cx, cy, rx, ry, gid):
    return (f'<defs><radialGradient id="{gid}" cx="0" cy="0" r="1" gradientTransform="translate({cx} {cy}) scale({rx} {ry})">'
            f'<stop stop-color="{INK}" stop-opacity=".22"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>')


def key(x, y, size, gid, legend=""):
    """The brand key: white face, light lip below. `legend` is SVG drawn in the face's own units (0..size)."""
    r = size * .24
    lip = size * .055
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="{y}" x2="0" y2="{y + size}" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDF3F5"/></linearGradient></defs>'
            f'<rect x="{x}" y="{y + lip}" width="{size}" height="{size}" rx="{r}" fill="{LIP}"/>'
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="url(#{gid})"/>'
            f'<g transform="translate({x} {y})">{legend}</g>')


def spark(x, y, size, gid, stops=SPARK_STOPS):
    """The brand spark in its deep gradient, its 24-unit box scaled to `size` at (x, y)."""
    k = size / 24
    return (f'<defs><linearGradient id="{gid}" x1="{x + 3.5 * k}" y1="{y + 2 * k}" x2="{x + 21.4 * k}" y2="{y + 18 * k}" gradientUnits="userSpaceOnUse">'
            f'{_stops(stops)}</linearGradient></defs>'
            f'<path fill="url(#{gid})" transform="translate({x} {y}) scale({k:.4f})" d="{SPARK_PATH}"/>')


def pill(x, y, w, h, fill="#FFFFFF", stroke=None, gid=None):
    edge = ""
    if stroke == "gradient":
        edge = (f'<defs><linearGradient id="{gid}" x1="{x}" y1="{y}" x2="{x + w}" y2="{y + h}" gradientUnits="userSpaceOnUse">{_stops(BG_STOPS)}</linearGradient></defs>'
                f'<rect x="{x - 2}" y="{y - 2}" width="{w + 4}" height="{h + 4}" rx="{(h + 4) / 2}" fill="url(#{gid})"/>')
    return edge + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/><rect x="{x}" y="{y + h - 2}" width="{w}" height="2" rx="1" fill="{LIP}" opacity=".0"/>'


def line(x, y, w, colour=LIP, h=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{colour}"/>'


def svg(body, size):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-hidden="true">{body}</svg>'


# ---------- illustrations ----------

def welcome(size=200):
    """Setup, Welcome: suggestions rising from a key; the middle one is picked by AI."""
    legend = ('<g fill="none" stroke="#08323B" stroke-width="5" stroke-linecap="round">'
              '<path d="M26 30 v24"/><path d="M34 26 v32"/><path d="M42 32 v20"/></g>')  # voice bars as the key's legend
    body = (glow(100, 104, 86, _id("g")) + shadow(100, 170, 46, 7, _id("s")) +
            key(62, 92, 76, _id("k"), legend) + spark(110, 98, 22, _id("sp")) +
            pill(22, 52, 46, 20, "#FFFFFF") + pill(77, 36, 50, 22, "#FFFFFF", "gradient", _id("p")) + pill(136, 52, 46, 20, "#FFFFFF") +
            line(31, 60, 26) + line(87, 45, 30, INK) + line(145, 60, 26) + spark(120, 24, 16, _id("sp")))
    return svg(body, size)


def empty_notes(size=160):
    """Notes, no notes yet: a blank note waiting, with the spark ready to help."""
    body = (glow(100, 100, 78, _id("g")) + shadow(100, 168, 52, 7, _id("s")) +
            f'<rect x="58" y="42" width="92" height="114" rx="16" fill="{LIP}" transform="rotate(-6 104 99)"/>'
            f'<rect x="50" y="38" width="92" height="114" rx="16" fill="#FFFFFF"/>'
            + line(66, 62, 52, INK, 6) + line(66, 82, 60) + line(66, 98, 44) + line(66, 114, 54) +
            key(118, 112, 44, _id("k"), '<path d="M22 13 v18 M13 22 h18" stroke="#08323B" stroke-width="4.5" stroke-linecap="round"/>') +
            spark(132, 20, 26, _id("sp")))
    return svg(body, size)


ALL = {"art_welcome": welcome, "art_empty_notes": empty_notes}
