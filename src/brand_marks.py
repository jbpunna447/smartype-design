"""Logo directions for the brand review, drawn as vectors on Android's 108 × 108 adaptive-icon canvas.

Each direction has a background, a foreground and a monochrome (themed icon) layer, like ic_launcher.xml.
Colours are the shipped brand colours (res/values/colors_signature_brand.xml)."""

INK = "#08323B"
PORCELAIN = "#F7F9FA"
GRAPHITE = "#0D1114"
GLACIER = "#67CEE5"
SEAGLASS = "#69D4BD"

# The shipped monogram (ic_smartype_foreground.xml), in its own 0..85 coordinates: x 15..70, y 18..89. Only "Today"
# uses it: it isn't symmetric (smaller, offset top bowl; ends cut at different angles; small flats in the spine).
S_PATH = ("M62,27 C58,21 51,18 43,18 C29,18 20,26 20,37 C20,48 28,54 42,57 L47,58 C54,60 58,63 58,68 C58,74 52,78 44,78 "
          "C35,78 29,74 26,67 L15,71 C19,82 29,89 44,89 C60,89 70,81 70,68 C70,57 62,51 48,48 L42,47 C35,45 32,42 32,37 "
          "C32,32 36,29 43,29 C49,29 54,32 57,37 Z")
STAR_PATH = "M74,13 L77,20 L84,23 L77,26 L74,33 L71,26 L64,23 L71,20 Z"


# The new S: two evenly round bowls drawn as ellipses, the top one deliberately smaller (rx 19, ry 15 at (50, 32))
# than the bottom one (rx 22, ry 18 at (50, 65)), as in the original S; the spark fills the space the smaller top
# leaves. The bowls meet level at (50, 47); each end stops 30° past the side of its bowl. Even stroke, round ends.
# Box with the stroke: x 21.5..78.5, y 10.5..89.5 (57 × 79), centred on (50, 50).
S2_PATH = "M66.45,24.50 A19,15 0 1 0 50,47 A22,18 0 1 1 30.95,74.00"
S2_WEIGHT = 13


def _s_drawn(cx, cy, h, fill):
    """The hand-drawn two-ellipse S (kept for the comparison on the brand page)."""
    k = h / 79
    tx = cx - 50 * k
    ty = cy - 50 * k
    return (f'<path fill="none" stroke="{fill}" stroke-width="{S2_WEIGHT}" stroke-linecap="round" stroke-linejoin="round" '
            f'transform="translate({tx:.2f} {ty:.2f}) scale({k:.4f})" d="{S2_PATH}"/>')


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


# A · Keycap: a white key with a light lip, the S as its legend. The AI version adds the spark as the key's
# corner legend, the way a real key shows its long-press symbol.
LIP = "#C3D5DA"
TEAL = "#0B727B"
SPARK_PATH = ("M10.5 4c.55 4.3 2.7 6.45 7 7-4.3.55-6.45 2.7-7 7-.55-4.3-2.7-6.45-7-7 4.3-.55 6.45-2.7 7-7Z"
              "M18.5 2c.28 1.75 1.13 2.6 2.88 2.88-1.75.28-2.6 1.13-2.88 2.88-.28-1.75-1.13-2.6-2.88-2.88C17.37 4.6 18.22 3.75 18.5 2Z")


def key_bg(gid):
    return f'<defs>{_grad(gid)}</defs><rect width="108" height="108" fill="url(#{gid})"/>'


# Stronger icon backgrounds: a wider hue shift (blue → cyan → mint) in the same family, with an optional soft light.
BG_STOPS = {
    "soft": [(0, GLACIER), (1, SEAGLASS)],
    "vivid": [(0, "#1E9BD7"), (.5, "#22C3CF"), (1, "#4BDCA4")],
    "deep": [(0, "#1663B8"), (.5, "#1BAFC8"), (1, "#40D9A0")],
    "spark": [(0, "#1257A8"), (.5, "#0E8DA6"), (1, "#119A76")],
}


def _bg(stops, glow):
    def bg(gid):
        st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in BG_STOPS[stops])
        out = (f'<defs><linearGradient id="{gid}" x1="18" y1="18" x2="90" y2="90" gradientUnits="userSpaceOnUse">{st}</linearGradient>')
        if glow:
            out += (f'<radialGradient id="{gid}r" cx="34" cy="26" r="46" gradientUnits="userSpaceOnUse">'
                    '<stop stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
        out += f'</defs><rect width="108" height="108" fill="url(#{gid})"/>'
        if glow:
            out += f'<rect width="108" height="108" fill="url(#{gid}r)"/>'
        return out
    return bg


def _keycap(gid):
    return (f'<defs><linearGradient id="{gid}k" x1="0" y1="29" x2="0" y2="75" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDF3F5"/></linearGradient></defs>'
            f'<rect x="31" y="31.5" width="46" height="46" rx="11" fill="{LIP}"/>'
            f'<rect x="31" y="29" width="46" height="46" rx="11" fill="url(#{gid}k)"/>')


def key_fg(gid):
    return _keycap(gid) + _s(54, 52, 30, INK)


def key_mono(gid):
    return ('<mask id="%sm"><rect width="108" height="108" fill="#000"/><rect x="31" y="29" width="46" height="48.5" rx="11" fill="#fff"/>' % gid +
            _s(54, 52, 30, "#000") + '</mask><rect width="108" height="108" fill="MONO" mask="url(#%sm)"/>' % gid)


# The S sits a little down-left on the key's top face; the spark sits up in the key's top-right corner, a short gap
# after the S's top tip (the end of the stroke when the S is written backwards).
KS_H, KS_K = 29, .7
KS_CX, KS_CY = 51, 54
_SPARK_DX, _SPARK_DY = 13.5, -14


def _spark(fill, gid=None):
    scx, scy = KS_CX + _SPARK_DX, KS_CY + _SPARK_DY
    tx, ty = scx - 10.5 * KS_K, scy - 11 * KS_K
    path = f'transform="translate({tx:.2f} {ty:.2f}) scale({KS_K})" d="{SPARK_PATH}"'
    if fill != "gradient":
        return f'<path fill="{fill}" {path}/>'
    # The background's vivid gradient and light, laid over the spark's own box.
    x0, y0, x1, y1 = tx + 3.5 * KS_K, ty + 2 * KS_K, tx + 21.4 * KS_K, ty + 18 * KS_K
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in BG_STOPS["spark"])
    return (f'<defs><linearGradient id="{gid}sp" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" gradientUnits="userSpaceOnUse">{st}</linearGradient>'
            f'<radialGradient id="{gid}spl" cx="{x0:.2f}" cy="{y0:.2f}" r="{(x1 - x0) * .9:.2f}" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>'
            f'<path fill="url(#{gid}sp)" {path}/><path fill="url(#{gid}spl)" {path}/>')


def _s(cx, cy, h, fill):
    """The logo S: Google Sans Flex at weight 700, roundness 100, centred on (cx, cy), h units tall."""
    return _sfont("w700r100", cx, cy, h, fill)


def _sfont(key, cx, cy, h, fill):
    """The Google Sans Flex S (brand_glyphs.GLYPH_S[key]) centred on (cx, cy), h units tall."""
    from brand_glyphs import GLYPH_S
    w, gh, d = GLYPH_S[key]
    k = h / gh
    return f'<path fill="{fill}" transform="translate({cx - w * k / 2:.2f} {cy - h / 2:.2f}) scale({k:.5f})" d="{d}"/>'


def _voice_mask(gid, cx, cy, h, style):
    """Voice variants: 'bars' cuts the whole lower half of the S into a level meter; 'fade' cuts only its left end,
    with gaps that widen towards the tail, like sound trailing off."""
    w = h * .75
    if style == "bars":
        cuts = "".join(f'<rect x="{cx - w / 2 + i * 2.1:.2f}" y="{cy + h * .04:.2f}" width=".75" height="{h / 2:.2f}" fill="#000"/>' for i in range(11))
    else:
        cuts = "".join(f'<rect x="{cx - w / 2 + 6.6 - i * 2.2:.2f}" y="{cy + h * .12:.2f}" width="{.5 + i * .3:.2f}" height="{h / 2:.2f}" fill="#000"/>' for i in range(4))
    return f'<mask id="{gid}v"><rect width="108" height="108" fill="#fff"/>{cuts}</mask>'


def _keyfont(key, spark_fill=None, voice=False):
    def fg(gid):
        out = _keycap(gid)
        glyph = _sfont(key, KS_CX, KS_CY, KS_H, INK)
        if voice:
            out += _voice_mask(gid, KS_CX, KS_CY, KS_H, voice) + f'<g mask="url(#{gid}v)">{glyph}</g>'
        else:
            out += glyph
        return out + _spark(spark_fill or "gradient", gid)
    return fg


def _keyfont_mono(key):
    def mono(gid):
        return ('<mask id="%sm"><rect width="108" height="108" fill="#000"/><rect x="31" y="29" width="46" height="48.5" rx="11" fill="#fff"/>' % gid +
                _sfont(key, KS_CX, KS_CY, KS_H, "#000") + _spark("#000") + '</mask><rect width="108" height="108" fill="MONO" mask="url(#%sm)"/>' % gid)
    return mono


def _keyai(spark_fill):
    def fg(gid):
        return _keycap(gid) + _s(KS_CX, KS_CY, KS_H, INK) + _spark(spark_fill, gid)
    return fg


def keyai_mono(gid):
    return ('<mask id="%sm"><rect width="108" height="108" fill="#000"/><rect x="31" y="29" width="46" height="48.5" rx="11" fill="#fff"/>' % gid +
            _s(KS_CX, KS_CY, KS_H, "#000") + _spark("#000") + '</mask><rect width="108" height="108" fill="MONO" mask="url(#%sm)"/>' % gid)


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
    return f'<path fill="{PORCELAIN}" d="{_BUBBLE}"/>' + _s(54, 52, 30, INK)


def talk_mono(gid):
    return ('<mask id="%sm"><rect width="108" height="108" fill="#000"/><path fill="#fff" d="%s"/>' % (gid, _BUBBLE) +
            _s(54, 52, 30, "#000") + '</mask><rect width="108" height="108" fill="MONO" mask="url(#%sm)"/>' % gid)


DIRECTIONS = {
    "today": ("Today", today_bg, today_fg, today_mono),
    "keyai": ("A · Keycap with the AI spark", _bg("vivid", True), _keyai("gradient"), keyai_mono),
    "keyai_teal": ("Spark in teal", _bg("vivid", True), _keyai(TEAL), keyai_mono),
    "keyai_ink": ("Spark in ink", _bg("vivid", True), _keyai(INK), keyai_mono),
    "keyai_soft": ("Soft (today's colours)", key_bg, _keyai("gradient"), keyai_mono),
    "keyai_vivid": ("Vivid", _bg("vivid", False), _keyai("gradient"), keyai_mono),
    "keyai_deep": ("Deep", _bg("deep", False), _keyai("gradient"), keyai_mono),
    "f650": ("Google Sans Flex S · 650 round", _bg("vivid", True), _keyfont("w650r100"), _keyfont_mono("w650r100")),
    "f700": ("Google Sans Flex S · 700 round", _bg("vivid", True), _keyfont("w700r100"), _keyfont_mono("w700r100")),
    "f800": ("Google Sans Flex S · 800 round", _bg("vivid", True), _keyfont("w800r100"), _keyfont_mono("w800r100")),
    "f700sq": ("Google Sans Flex S · 700 square", _bg("vivid", True), _keyfont("w700r0"), _keyfont_mono("w700r0")),
    "f700bars": ("700 round, voice bars", _bg("vivid", True), _keyfont("w700r100", voice="bars"), _keyfont_mono("w700r100")),
    "f700fade": ("700 round, voice fade", _bg("vivid", True), _keyfont("w700r100", voice="fade"), _keyfont_mono("w700r100")),
    "key": ("Keycap without the spark", _bg("vivid", True), key_fg, key_mono),
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
