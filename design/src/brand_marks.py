"""The SmarType logo, drawn as vectors on Android's 108 × 108 adaptive-icon canvas.

The logo has a background, a foreground and a monochrome (themed icon) layer, like ic_launcher.xml. "today" is the
icon the app ships now (ic_smartype_foreground.xml), kept only to show what the logo replaces."""

INK = "#08323B"
PORCELAIN = "#F7F9FA"
GRAPHITE = "#0D1114"
LIP = "#C3D5DA"

# Background: vivid blue → cyan → mint at 135°, with a soft white light from the top left.
BG_STOPS = [(0, "#1E9BD7"), (.5, "#22C3CF"), (1, "#4BDCA4")]
# Inverse icon background, for the brand gradient and other bright colours, where the normal icon blends in:
# the same hues, deep (ink blue → deep teal → deep green), with a fainter light.
INVERSE_STOPS = [(0, "#0B3A66"), (.5, "#0A4B5A"), (1, "#0C5A47")]
# The spark on light surfaces: a deeper version of the same colours, so it stays visible on white.
SPARK_STOPS = [(0, "#1257A8"), (.5, "#0E8DA6"), (1, "#119A76")]
# The AI gradient in the app (tokens ai-gradient-start / ai-gradient-end), with Ink on top.
AI_STOPS = [(0, "#2AA8E0"), (1, "#4BDCA4")]

# The one spark (assets/icons/brand/spark.svg), on a 24-unit grid: a big four-point star and a small one.
SPARK_PATH = ("M10.5 4c.55 4.3 2.7 6.45 7 7-4.3.55-6.45 2.7-7 7-.55-4.3-2.7-6.45-7-7 4.3-.55 6.45-2.7 7-7Z"
              "M18.5 2c.28 1.75 1.13 2.6 2.88 2.88-1.75.28-2.6 1.13-2.88 2.88-.28-1.75-1.13-2.6-2.88-2.88C17.37 4.6 18.22 3.75 18.5 2Z")

# Today's icon: the monogram and a straight-edged star (ic_smartype_foreground.xml).
TODAY_S = ("M62,27 C58,21 51,18 43,18 C29,18 20,26 20,37 C20,48 28,54 42,57 L47,58 C54,60 58,63 58,68 C58,74 52,78 44,78 "
           "C35,78 29,74 26,67 L15,71 C19,82 29,89 44,89 C60,89 70,81 70,68 C70,57 62,51 48,48 L42,47 C35,45 32,42 32,37 "
           "C32,32 36,29 43,29 C49,29 54,32 57,37 Z")
TODAY_STAR = "M74,13 L77,20 L84,23 L77,26 L74,33 L71,26 L64,23 L71,20 Z"

# Layout on the key's top face (x 31..77, y 29..75): the S a little down-left, the spark up in the top-right corner,
# just after the S's top tip. The S is the Google Sans Flex S at weight 700, roundness 100 (brand_glyphs.GLYPH_S).
S_KEY = "w700r100"
S_CX, S_CY, S_H = 51, 54, 29
SPARK_SCALE = .7
SPARK_DX, SPARK_DY = 13.5, -14
# Voice bars: four slots of equal width with equal bars between them, cut only inside the stroke; a rim of EDGE
# units is left along the S's outline so the letter keeps its shape.
EDGE = .9
SLOT = 1.1
# Themed and status-bar icons: the S cut out of the key is thinned by this much on each side, because a light shape
# on a dark one looks bolder than the same shape dark on light.
MONO_THIN = .4


def _stops(stops):
    return "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)


def _light(gid, cx, cy, r, alpha):
    return (f'<radialGradient id="{gid}" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#fff" stop-opacity="{alpha}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')


def background(gid, inverse=False):
    stops, light = (INVERSE_STOPS, .18) if inverse else (BG_STOPS, .45)
    return (f'<defs><linearGradient id="{gid}" x1="18" y1="18" x2="90" y2="90" gradientUnits="userSpaceOnUse">{_stops(stops)}</linearGradient>'
            f'{_light(gid + "r", 34, 26, 46, light)}</defs>'
            f'<rect width="108" height="108" fill="url(#{gid})"/><rect width="108" height="108" fill="url(#{gid}r)"/>')


def _keycap(gid):
    return (f'<defs><linearGradient id="{gid}k" x1="0" y1="29" x2="0" y2="75" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDF3F5"/></linearGradient></defs>'
            f'<rect x="31" y="31.5" width="46" height="46" rx="11" fill="{LIP}"/>'
            f'<rect x="31" y="29" width="46" height="46" rx="11" fill="url(#{gid}k)"/>')


def _glyph(cx, cy, h, fill):
    from brand_glyphs import GLYPH_S
    w, gh, d = GLYPH_S[S_KEY]
    k = h / gh
    return f'<path fill="{fill}" transform="translate({cx - w * k / 2:.2f} {cy - h / 2:.2f}) scale({k:.5f})" d="{d}"/>'


def _glyph_edge(amount, colour):
    """A stroke of `amount` on each side of the S's outline: drawn in white inside a mask, it thins the S."""
    from brand_glyphs import GLYPH_S
    w, gh, d = GLYPH_S[S_KEY]
    k = S_H / gh
    return (f'<path fill="none" stroke="{colour}" stroke-width="{2 * amount / k:.1f}" stroke-linejoin="round" '
            f'transform="translate({S_CX - w * k / 2:.2f} {S_CY - S_H / 2:.2f}) scale({k:.5f})" d="{d}"/>')


def _inner_mask(gid):
    """White where the S is at least EDGE inside its outline."""
    from brand_glyphs import GLYPH_S
    w, gh, d = GLYPH_S[S_KEY]
    k = S_H / gh
    t = f'translate({S_CX - w * k / 2:.2f} {S_CY - S_H / 2:.2f}) scale({k:.5f})'
    return (f'<mask id="{gid}i"><g transform="{t}"><path fill="#fff" d="{d}"/>'
            f'<path fill="none" stroke="#000" stroke-width="{2 * EDGE / k:.1f}" stroke-linejoin="round" d="{d}"/></g></mask>')


def _bars(fill):
    w = S_H * .75
    return "".join(f'<rect x="{S_CX - w / 2 + .4 + i * 2 * SLOT:.2f}" y="{S_CY + S_H * .1:.2f}" width="{SLOT}" height="{S_H / 2:.2f}" fill="{fill}"/>'
                   for i in range(4))


def _s_voice(gid, fill):
    return (_inner_mask(gid) +
            f'<mask id="{gid}v"><rect width="108" height="108" fill="#fff"/><g mask="url(#{gid}i)">{_bars("#000")}</g></mask>'
            f'<g mask="url(#{gid}v)">' + _glyph(S_CX, S_CY, S_H, fill) + "</g>")


def spark(fill, gid, x, y, scale, light=True):
    """The spark with its 24-unit box at (x, y). fill is a colour, or a list of gradient stops laid over the spark."""
    path = f'transform="translate({x:.2f} {y:.2f}) scale({scale})" d="{SPARK_PATH}"'
    if isinstance(fill, str):
        return f'<path fill="{fill}" {path}/>'
    x0, y0, x1, y1 = x + 3.5 * scale, y + 2 * scale, x + 21.4 * scale, y + 18 * scale
    out = (f'<defs><linearGradient id="{gid}sp" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" gradientUnits="userSpaceOnUse">{_stops(fill)}</linearGradient>'
           + (_light(gid + "spl", x0, y0, (x1 - x0) * .9, .25) if light else "") + f'</defs><path fill="url(#{gid}sp)" {path}/>')
    if light:
        out += f'<path fill="url(#{gid}spl)" {path}/>'
    return out


def _key_spark(fill, gid=""):
    cx, cy = S_CX + SPARK_DX, S_CY + SPARK_DY
    return spark(fill, gid, cx - 10.5 * SPARK_SCALE, cy - 11 * SPARK_SCALE, SPARK_SCALE)


def foreground(gid):
    return _keycap(gid) + _s_voice(gid, INK) + _key_spark(SPARK_STOPS, gid)


def monochrome(gid, voice=True):
    """Themed icon: the key's silhouette with the S, its voice bars and the spark cut out. voice=False keeps the S
    solid, for the 24 dp status-bar icon where the bars would vanish."""
    bars = f'<g mask="url(#{gid}i)">{_bars("#fff")}</g>' if voice else ""
    return (_inner_mask(gid) +
            f'<mask id="{gid}m"><rect width="108" height="108" fill="#000"/><rect x="31" y="29" width="46" height="48.5" rx="11" fill="#fff"/>' +
            _glyph(S_CX, S_CY, S_H, "#000") + _glyph_edge(MONO_THIN, "#fff") + bars + _key_spark("#000") +
            f'</mask><rect width="108" height="108" fill="MONO" mask="url(#{gid}m)"/>')


def today(gid):
    return (f'<rect width="108" height="108" fill="{GRAPHITE}"/>'
            f'<defs><linearGradient id="{gid}s" x1="64" y1="13" x2="84" y2="33" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#67CEE5"/><stop offset="1" stop-color="#69D4BD"/></linearGradient></defs>'
            f'<g transform="translate(23 20) scale(.68)"><path fill="{PORCELAIN}" d="{TODAY_S}"/><path fill="url(#{gid}s)" d="{TODAY_STAR}"/></g>')


# Launcher masks in the 108 canvas: Android shows the middle 72 × 72.
MASKS = {
    "circle": '<circle cx="54" cy="54" r="36"/>',
    "squircle": '<path d="M54,18 C84,18 90,24 90,54 C90,84 84,90 54,90 C24,90 18,84 18,54 C18,24 24,18 54,18 Z"/>',
    "rounded": '<rect x="18" y="18" width="72" height="72" rx="16"/>',
}

_n = [0]


def _id(prefix):
    _n[0] += 1
    return f"{prefix}{_n[0]}"


def icon(size, mask="circle", mono=False, mono_bg="#D7E6EA", mono_fg="#22474F", which="logo", inverse=False):
    """The launcher icon at `size` px in a launcher mask. mono=True draws Android's themed icon."""
    gid = _id("b")
    if which == "today":
        body = today(gid)
    elif mono:
        body = f'<rect width="108" height="108" fill="{mono_bg}"/>' + monochrome(gid).replace("MONO", mono_fg)
    else:
        body = background(gid + "g", inverse) + foreground(gid)
    label = "Today's app icon" if which == "today" else "SmarType app icon"
    return (f'<svg width="{size}" height="{size}" viewBox="18 18 72 72" role="img" aria-label="{label}">'
            f'<defs><clipPath id="{gid}c">{MASKS[mask]}</clipPath></defs><g clip-path="url(#{gid}c)">{body}</g></svg>')


def notification(size=24, color="currentColor"):
    """The status-bar icon: the solid-S monochrome layer, cropped to the key."""
    return (f'<svg width="{size}" height="{size}" viewBox="28 26.5 52 52" aria-hidden="true">' +
            monochrome(_id("n"), voice=False).replace("MONO", color) + "</svg>")


def ai_badge(size):
    """The AI badge: the spark in Ink on the AI gradient. Same as the smartbar's AI button; replaces ic_ai_logo."""
    gid = _id("a")
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 36 36" role="img" aria-label="AI">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">{_stops(AI_STOPS)}</linearGradient></defs>'
            f'<circle cx="18" cy="18" r="18" fill="url(#{gid})"/>' + spark(INK, gid, 8, 8, 20 / 24) + "</svg>")


def spark_mark(size, on_dark=False):
    """The spark on its own: the deep gradient on light surfaces, the AI gradient on dark ones."""
    gid = _id("s")
    stops = AI_STOPS if on_dark else SPARK_STOPS
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" role="img" aria-label="AI">' + spark(stops, gid, 0, 0, 1, light=False) + "</svg>"
