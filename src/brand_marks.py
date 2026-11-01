"""Logo directions for the brand review, drawn as vectors on Android's 108 × 108 adaptive-icon canvas.

Each direction has a background, a foreground and a monochrome (themed icon) layer, like ic_launcher.xml.
Colours are the shipped brand colours (res/values/colors_signature_brand.xml)."""

INK = "#08323B"
PORCELAIN = "#F7F9FA"
GRAPHITE = "#0D1114"
GLACIER = "#67CEE5"
SEAGLASS = "#69D4BD"

# The shipped monogram (ic_smartype_foreground.xml), in its own 0..85 coordinates: x 15..70, y 18..89.
S_PATH = ("M62,27 C58,21 51,18 43,18 C29,18 20,26 20,37 C20,48 28,54 42,57 L47,58 C54,60 58,63 58,68 C58,74 52,78 44,78 "
          "C35,78 29,74 26,67 L15,71 C19,82 29,89 44,89 C60,89 70,81 70,68 C70,57 62,51 48,48 L42,47 C35,45 32,42 32,37 "
          "C32,32 36,29 43,29 C49,29 54,32 57,37 Z")
STAR_PATH = "M74,13 L77,20 L84,23 L77,26 L74,33 L71,26 L64,23 L71,20 Z"


def _s(cx, cy, h, fill):
    """The monogram centred on (cx, cy), h units tall."""
    k = h / 71
    tx = cx - 42.5 * k
    ty = cy - 53.5 * k
    return f'<path fill="{fill}" transform="translate({tx:.2f} {ty:.2f}) scale({k:.4f})" d="{S_PATH}"/>'


def _grad(gid):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="108" y2="108" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{GLACIER}"/><stop offset="1" stop-color="{SEAGLASS}"/></linearGradient>')


# Each layer function returns SVG content on the 108 canvas. gid keeps gradient ids unique per drawing.
def today_bg(gid):
    return f'<rect width="108" height="108" fill="{GRAPHITE}"/>'


def today_fg(gid):
    return (f'<defs><linearGradient id="{gid}s" x1="64" y1="13" x2="84" y2="33" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{GLACIER}"/><stop offset="1" stop-color="{SEAGLASS}"/></linearGradient></defs>'
            f'<g transform="translate(23 20) scale(.68)"><path fill="{PORCELAIN}" d="{S_PATH}"/><path fill="url(#{gid}s)" d="{STAR_PATH}"/></g>')


def today_mono(gid):
    return f'<g transform="translate(23 20) scale(.68)" fill="MONO"><path d="{S_PATH}"/><path d="{STAR_PATH}"/></g>'


# A · Keycap: a flat key with the S as its legend.
def key_bg(gid):
    return f'<defs>{_grad(gid)}</defs><rect width="108" height="108" fill="url(#{gid})"/>'


def key_fg(gid):
    return ('<rect x="31" y="33" width="46" height="46" rx="11" fill="#0B4F57" opacity=".55"/>'
            f'<rect x="31" y="28" width="46" height="46" rx="11" fill="{PORCELAIN}"/>' + _s(54, 51, 30, INK))


def key_mono(gid):
    return ('<mask id="%sm"><rect width="108" height="108" fill="#000"/><rect x="31" y="28" width="46" height="51" rx="11" fill="#fff"/>' % gid +
            _s(54, 51, 30, "#000") + '</mask><rect width="108" height="108" fill="MONO" mask="url(#%sm)"/>' % gid)


# B · Caret: the S followed by a text cursor, as if it had just been typed.
def caret_bg(gid):
    return f'<rect width="108" height="108" fill="{GRAPHITE}"/>'


def caret_fg(gid):
    return (f'<defs>{_grad(gid)}</defs>' + _s(46, 54, 44, PORCELAIN) +
            f'<rect x="71" y="33" width="5" height="42" rx="2.5" fill="url(#{gid})"/>')


def caret_mono(gid):
    return _s(46, 54, 44, "MONO") + '<rect x="71" y="33" width="5" height="42" rx="2.5" fill="MONO"/>'


# C · Talk key: a key with a speech tail, for typing and speaking.
_BUBBLE = "M42,28 H66 A11,11 0 0 1 77,39 V63 A11,11 0 0 1 66,74 H46 L33,82 L35,71 A11,11 0 0 1 31,63 V39 A11,11 0 0 1 42,28 Z"


def talk_bg(gid):
    return f'<defs>{_grad(gid)}</defs><rect width="108" height="108" fill="url(#{gid})"/>'


def talk_fg(gid):
    return f'<path fill="{PORCELAIN}" d="{_BUBBLE}"/>' + _s(54, 51, 30, INK)


def talk_mono(gid):
    return ('<mask id="%sm"><rect width="108" height="108" fill="#000"/><path fill="#fff" d="%s"/>' % (gid, _BUBBLE) +
            _s(54, 51, 30, "#000") + '</mask><rect width="108" height="108" fill="MONO" mask="url(#%sm)"/>' % gid)


DIRECTIONS = {
    "today": ("Today", today_bg, today_fg, today_mono),
    "key": ("A · Keycap", key_bg, key_fg, key_mono),
    "caret": ("B · Caret", caret_bg, caret_fg, caret_mono),
    "talk": ("C · Talk key", talk_bg, talk_fg, talk_mono),
}

# Launcher masks in the 108 canvas: Android shows the middle 72 × 72.
MASKS = {
    "circle": '<circle cx="54" cy="54" r="36"/>',
    "squircle": '<path d="M54,18 C84,18 90,24 90,54 C90,84 84,90 54,90 C24,90 18,84 18,54 C18,24 24,18 54,18 Z"/>',
    "rounded": '<rect x="18" y="18" width="72" height="72" rx="16"/>',
}

_n = [0]


def icon(key, size, mask="circle", mono=False, mono_bg="#D7E6EA", mono_fg="#22474F"):
    """The launcher icon for a direction at `size` px. mono=True draws Android's themed icon (tinted monochrome layer)."""
    _n[0] += 1
    gid = f"b{key}{_n[0]}"
    _, bg, fg, mn = DIRECTIONS[key]
    if mono:
        body = f'<rect width="108" height="108" fill="{mono_bg}"/><g style="color:{mono_fg}">' + mn(gid).replace("MONO", mono_fg) + "</g>"
    else:
        body = bg(gid + "g") + fg(gid)
    return (f'<svg width="{size}" height="{size}" viewBox="18 18 72 72" role="img" aria-label="{DIRECTIONS[key][0]} icon">'
            f'<defs><clipPath id="{gid}c">{MASKS[mask]}</clipPath></defs><g clip-path="url(#{gid}c)">{body}</g></svg>')


def notification(key, size=24, color="currentColor"):
    """The status-bar icon: the monochrome layer alone, cropped to the safe zone."""
    _n[0] += 1
    gid = f"n{key}{_n[0]}"
    return (f'<svg width="{size}" height="{size}" viewBox="21 21 66 66" aria-hidden="true">' +
            DIRECTIONS[key][3](gid).replace("MONO", color) + "</svg>")
