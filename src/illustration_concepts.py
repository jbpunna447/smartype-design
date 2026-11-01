"""Shared drawing helpers for the illustrations: ids, gradients, the spark, the key, the glow, the shadow and the
animated SVG wrapper (with a still frame for reduced motion)."""
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
