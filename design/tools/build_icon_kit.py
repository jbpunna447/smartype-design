"""Builds the SmarType icon kit into assets/brand from the approved logo (src/brand_marks.py).

Android vector drawables can't use masks, so the voice bars and every cut-out are computed as real path geometry
with skia-pathops. The SVG masters use the same paths, so Android and the SVGs draw exactly the same shapes.
PNGs (Play Store icon, favicons, lockups) are rendered from the SVG masters with headless Chrome.

Needs: fontTools, skia-pathops, uharfbuzz, Google Chrome, and the Google Sans Flex variable font (OFL) from
github.com/google/fonts/tree/main/ofl/googlesansflex for the wordmark and badge text.

    python tools/build_icon_kit.py --font path/to/GoogleSansFlex[ROND,opsz,slnt,wdth,wght].ttf
"""
import argparse
import io
import os
import shutil
import subprocess
import sys
import tempfile

import pathops
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import brand_marks as bm  # noqa: E402
from brand_glyphs import GLYPH_S  # noqa: E402

OUT = os.path.join(ROOT, "assets", "brand")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


# ---------- geometry ----------

def path_from_d(d, transform=(1, 0, 0, 1, 0, 0)):
    p = pathops.Path()
    parse_path(d, TransformPen(p.getPen(), transform))
    return p


def rounded_rect(x, y, w, h, r):
    k = .5523 * r
    d = (f"M{x + r},{y} H{x + w - r} C{x + w - r + k},{y} {x + w},{y + r - k} {x + w},{y + r} V{y + h - r} "
         f"C{x + w},{y + h - r + k} {x + w - r + k},{y + h} {x + w - r},{y + h} H{x + r} C{x + r - k},{y + h} {x},{y + h - r + k} {x},{y + h - r} "
         f"V{y + r} C{x},{y + r - k} {x + r - k},{y} {x + r},{y} Z")
    return path_from_d(d)


def op(a, b, kind):
    return pathops.op(a, b, kind, fix_winding=True)


def d_of(p):
    pen = SVGPathPen(None, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip(".") or "0")
    p.draw(pen)
    return pen.getCommands()


def transformed(p, t):
    out = pathops.Path()
    p.draw(TransformPen(out.getPen(), t))
    return out


def erode(p, amount):
    """p shrunk by `amount` all round."""
    edge = pathops.Path(p)
    edge.stroke(2 * amount, pathops.LineCap.BUTT_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    edge.convertConicsToQuads()
    return op(p, edge, pathops.PathOp.DIFFERENCE)


def logo_shapes():
    w, gh, d = GLYPH_S[bm.S_KEY]
    k = bm.S_H / gh
    s = path_from_d(d, (k, 0, 0, k, bm.S_CX - w * k / 2, bm.S_CY - bm.S_H / 2))
    inner = erode(s, bm.EDGE)
    bars = pathops.Path()
    bw = bm.S_H * .75
    for i in range(4):
        x = bm.S_CX - bw / 2 + .4 + i * 2 * bm.SLOT
        y = bm.S_CY + bm.S_H * .1
        bars = op(bars, rounded_rect(x, y, bm.SLOT, bm.S_H / 2, 0.0001), pathops.PathOp.UNION)
    cuts = op(bars, inner, pathops.PathOp.INTERSECTION)
    s_voice = op(s, cuts, pathops.PathOp.DIFFERENCE)
    sc = bm.SPARK_SCALE
    sx = bm.S_CX + bm.SPARK_DX - 10.5 * sc
    sy = bm.S_CY + bm.SPARK_DY - 11 * sc
    spark = path_from_d(bm.SPARK_PATH, (sc, 0, 0, sc, sx, sy))
    face = rounded_rect(31, 29, 46, 46, 11)
    lip = rounded_rect(31, 31.5, 46, 46, 11)
    key = op(face, lip, pathops.PathOp.UNION)
    # A light S cut out of a solid key looks bolder than the same S in Ink on white, so the cut-outs are thinned
    # by MONO_THIN on each side to match the colour icon's weight.
    s_thin = erode(s, bm.MONO_THIN)
    mono = op(op(key, op(s_thin, cuts, pathops.PathOp.DIFFERENCE), pathops.PathOp.DIFFERENCE), spark, pathops.PathOp.DIFFERENCE)
    mono_solid = op(op(key, s_thin, pathops.PathOp.DIFFERENCE), spark, pathops.PathOp.DIFFERENCE)
    spark_box = (sx + 3.5 * sc, sy + 2 * sc, sx + 21.4 * sc, sy + 18 * sc)
    return dict(s=s, s_voice=s_voice, spark=spark, face=face, lip=lip, mono=mono, mono_solid=mono_solid, spark_box=spark_box)


# ---------- text (wordmark and badges) ----------

class Typeset:
    """Outlines text in Google Sans Flex at an axis location, shaped with HarfBuzz (kerning included)."""

    def __init__(self, font_path, location):
        f = instantiateVariableFont(TTFont(font_path), location)
        buf = io.BytesIO()
        f.save(buf)
        self.ttf = TTFont(io.BytesIO(buf.getvalue()))
        self.upem = self.ttf["head"].unitsPerEm
        self.cap = self.ttf["OS/2"].sCapHeight
        self.hbfont = hb.Font(hb.Face(hb.Blob(buf.getvalue())))
        self.gs = self.ttf.getGlyphSet()
        self.order = self.ttf.getGlyphOrder()

    def glyphs(self, text):
        b = hb.Buffer()
        b.add_str(text)
        b.guess_segment_properties()
        hb.shape(self.hbfont, b, {"kern": True, "liga": True})
        x = 0
        out = []
        for info, pos in zip(b.glyph_infos, b.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset, pos.y_offset))
            x += pos.x_advance
        return out, x

    def paths(self, text, size, x0=0, baseline=0):
        """One pathops.Path per glyph, scaled so the em is `size`, with the baseline at y=baseline (y down)."""
        k = size / self.upem
        gl, adv = self.glyphs(text)
        res = []
        for name, gx, gy in gl:
            p = pathops.Path()
            self.gs[name].draw(TransformPen(p.getPen(), (k, 0, 0, -k, x0 + gx * k, baseline - gy * k)))
            res.append(p)
        return res, adv * k


# ---------- Android vector drawables ----------

def _gradient(kind, stops, **attrs):
    a = " ".join(f'android:{k}="{v:.2f}"' if isinstance(v, float) else f'android:{k}="{v}"' for k, v in attrs.items())
    items = "".join(f'\n                <item android:offset="{o}" android:color="{c}"/>' for o, c in stops)
    return (f'\n        <aapt:attr name="android:fillColor">\n            <gradient android:type="{kind}" {a}>{items}\n            </gradient>\n        </aapt:attr>')


def vpath(d, color=None, gradient=None):
    if gradient:
        return f'    <path android:pathData="{d}">{gradient}\n    </path>\n'
    return f'    <path android:fillColor="{color}" android:pathData="{d}"/>\n'


def vector(body, size=108, viewport=108, comment=""):
    head = '<?xml version="1.0" encoding="utf-8"?>\n'
    if comment:
        head += f"<!-- {comment} -->\n"
    return (head + '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n    xmlns:aapt="http://schemas.android.com/aapt"\n'
            f'    android:width="{size}dp"\n    android:height="{size}dp"\n    android:viewportWidth="{viewport}"\n    android:viewportHeight="{viewport}">\n'
            + body + "</vector>\n")


def argb(hex6, alpha):
    return "#%02X%s" % (round(alpha * 255), hex6.lstrip("#").upper())


FULL = "M0,0H108V108H0Z"
CIRCLE = "M54,18A36,36 0 1,1 54,90A36,36 0 1,1 54,18Z"


def background_body():
    lin = _gradient("linear", [(o, c) for o, c in bm.BG_STOPS], startX=18.0, startY=18.0, endX=90.0, endY=90.0)
    rad = _gradient("radial", [(0, argb("#FFFFFF", .45)), (1, argb("#FFFFFF", 0))], centerX=34.0, centerY=26.0, gradientRadius=46.0)
    return vpath(FULL, gradient=lin) + vpath(FULL, gradient=rad)


def foreground_body(sh, extra=""):
    face = _gradient("linear", [(0, "#FFFFFF"), (1, "#EDF3F5")], startX=54.0, startY=29.0, endX=54.0, endY=75.0)
    x0, y0, x1, y1 = sh["spark_box"]
    sp = _gradient("linear", bm.SPARK_STOPS, startX=x0, startY=y0, endX=x1, endY=y1)
    spl = _gradient("radial", [(0, argb("#FFFFFF", .25)), (1, argb("#FFFFFF", 0))], centerX=x0, centerY=y0, gradientRadius=(x1 - x0) * .9)
    return (vpath(d_of(sh["lip"]), bm.LIP) + vpath(d_of(sh["face"]), gradient=face) + vpath(d_of(sh["s_voice"]), bm.INK) +
            vpath(d_of(sh["spark"]), gradient=sp) + vpath(d_of(sh["spark"]), gradient=spl) + extra)


def adaptive(fg, bg="@drawable/ic_launcher_background", mono="@drawable/ic_launcher_monochrome"):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
            f'    <background android:drawable="{bg}"/>\n    <foreground android:drawable="{fg}"/>\n    <monochrome android:drawable="{mono}"/>\n</adaptive-icon>\n')


def badge(ts, label, fill):
    """A pill with outlined text under the key, inside the 72 × 72 visible area (and the circle mask)."""
    size = 6.2
    glyph_paths, adv = ts.paths(label, size)
    cap = ts.cap * size / ts.upem
    w = adv + 6
    x, y, h = 54 - w / 2, 80.5, 7.4
    pill = rounded_rect(x, y, w, h, h / 2)
    text = pathops.Path()
    for p in glyph_paths:
        text = op(text, transformed(p, (1, 0, 0, 1, x + 3, y + h / 2 + cap / 2)), pathops.PathOp.UNION)
    return vpath(d_of(pill), fill) + vpath(d_of(text), "#FFFFFF")


# ---------- SVG masters ----------

def svg_doc(body, view, w, h, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{view}">'
            f'<defs>{defs}</defs>{body}</svg>\n')


def svg_grad(gid, stops, x1, y1, x2, y2):
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" gradientUnits="userSpaceOnUse">{st}</linearGradient>'


def svg_light(gid, cx, cy, r, a):
    return (f'<radialGradient id="{gid}" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#fff" stop-opacity="{a}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')


def icon_svg_parts(sh, p="", inverse=False):
    """inverse=True: the deep background, for use on the brand gradient and other bright colours."""
    x0, y0, x1, y1 = sh["spark_box"]
    stops, light = (bm.INVERSE_STOPS, .18) if inverse else (bm.BG_STOPS, .45)
    defs = (svg_grad(p + "bg", stops, 18, 18, 90, 90) + svg_light(p + "bgl", 34, 26, 46, light) +
            svg_grad(p + "face", [(0, "#FFFFFF"), (1, "#EDF3F5")], 54, 29, 54, 75) +
            svg_grad(p + "sp", bm.SPARK_STOPS, x0, y0, x1, y1) + svg_light(p + "spl", x0, y0, (x1 - x0) * .9, .25))
    bg = f'<rect width="108" height="108" fill="url(#{p}bg)"/><rect width="108" height="108" fill="url(#{p}bgl)"/>'
    fg = (f'<path fill="{bm.LIP}" d="{d_of(sh["lip"])}"/><path fill="url(#{p}face)" d="{d_of(sh["face"])}"/>'
          f'<path fill="{bm.INK}" d="{d_of(sh["s_voice"])}"/><path fill="url(#{p}sp)" d="{d_of(sh["spark"])}"/>'
          f'<path fill="url(#{p}spl)" d="{d_of(sh["spark"])}"/>')
    return defs, bg, fg


def icon_svg(sh, shape="square", size=512):
    """The full icon on the visible 72 × 72: 'square' (full bleed, for Play and maskable), 'rounded' (favicon)."""
    defs, bg, fg = icon_svg_parts(sh)
    if shape == "rounded":
        defs += '<clipPath id="r"><rect x="18" y="18" width="72" height="72" rx="16"/></clipPath>'
        return svg_doc(f'<g clip-path="url(#r)">{bg}{fg}</g>', "18 18 72 72", size, size, defs)
    return svg_doc(bg + fg, "18 18 72 72", size, size, defs)


# ---------- rendering ----------

def render_png(svg_text, out_path, w, h):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "p.html")
        with open(page, "w") as fh:
            fh.write(f'<!doctype html><html><body style="margin:0;background:transparent">{svg_text}</body></html>')
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        f"--window-size={w},{h}", f"--screenshot={out_path}", "file://" + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Play Console asks for a 32-bit PNG: always save with an alpha channel.
    from PIL import Image
    Image.open(out_path).convert("RGBA").save(out_path, optimize=True)


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True)
    args = ap.parse_args()

    for sub in ("android", "svg", "png", "web"):
        shutil.rmtree(os.path.join(OUT, sub), ignore_errors=True)
        os.makedirs(os.path.join(OUT, sub))
    sh = logo_shapes()
    badge_ts = Typeset(args.font, {"wght": 700, "ROND": 100, "opsz": 18})
    word_ts = Typeset(args.font, {"wght": 600, "ROND": 0, "opsz": 144})

    # Android
    a = "android/"
    write(a + "drawable/ic_launcher_background.xml", vector(background_body(), comment="SmarType app icon: background layer. Built by tools/build_icon_kit.py."))
    write(a + "drawable/ic_launcher_foreground.xml", vector(foreground_body(sh), comment="SmarType app icon: the key, the S with voice bars, the spark."))
    write(a + "drawable/ic_launcher_monochrome.xml", vector(vpath(d_of(sh["mono"]), "#FFFFFFFF"), comment="Themed icon (Android 13+): Android tints this layer."))
    write(a + "drawable/ic_launcher_foreground_debug.xml",
          vector(foreground_body(sh, badge(badge_ts, "DEV", "#C2410C")), comment="Debug builds: the foreground with a DEV badge."))
    write(a + "drawable/ic_launcher_foreground_beta.xml",
          vector(foreground_body(sh, badge(badge_ts, "BETA", bm.INK)), comment="Beta builds: the foreground with a BETA badge."))
    mono_note = transformed(sh["mono_solid"], (24 / 50, 0, 0, 24 / 50, -(54 - 25) * 24 / 50, -(53.25 - 25) * 24 / 50))
    write(a + "drawable/ic_stat_smartype.xml",
          vector(vpath(d_of(mono_note), "#FFFFFFFF"), size=24, viewport=24, comment="Status-bar icon: white silhouette, solid S (the voice bars would vanish at 24 dp)."))
    splash_bg = background_body()
    splash = (f'    <group>\n        <clip-path android:pathData="{CIRCLE}"/>\n' +
              "".join("    " + line + "\n" for line in splash_bg.rstrip("\n").split("\n")) + "    </group>\n" + foreground_body(sh))
    write(a + "drawable/ic_smartype_splash.xml",
          vector(splash, size=108, comment="Splash icon (SplashScreen windowSplashScreenAnimatedIcon): the icon in a circle of 2/3 of the canvas."))
    for v, fg in (("", "@drawable/ic_launcher_foreground"), ("_debug", "@drawable/ic_launcher_foreground_debug"), ("_beta", "@drawable/ic_launcher_foreground_beta")):
        write(a + f"mipmap-anydpi-v26/ic_launcher{v}.xml", adaptive(fg))
        write(a + f"mipmap-anydpi-v26/ic_launcher{v}_round.xml", adaptive(fg))

    # SVG masters
    defs, bg, fg = icon_svg_parts(sh)
    write("svg/icon-background.svg", svg_doc(bg, "0 0 108 108", 108, 108, defs))
    write("svg/icon-foreground.svg", svg_doc(fg, "0 0 108 108", 108, 108, defs))
    write("svg/icon-monochrome.svg", svg_doc(f'<path fill="#000" d="{d_of(sh["mono"])}"/>', "0 0 108 108", 108, 108))
    write("svg/icon-notification.svg", svg_doc(f'<path fill="#000" d="{d_of(mono_note)}"/>', "0 0 24 24", 24, 24))
    full = icon_svg(sh, "square")
    rounded = icon_svg(sh, "rounded")
    write("svg/icon.svg", full)
    write("svg/icon-rounded.svg", rounded)
    defs_i, bg_i, fg_i = icon_svg_parts(sh, "i", inverse=True)
    write("svg/icon-inverse-rounded.svg", svg_doc(f'<defs><clipPath id="ir"><rect x="18" y="18" width="72" height="72" rx="16"/></clipPath></defs>'
                                                  f'<g clip-path="url(#ir)">{bg_i}{fg_i}</g>', "18 18 72 72", 512, 512, defs_i))
    write("web/favicon.svg", icon_svg(sh, "rounded", 32))

    # Wordmark: Google Sans Flex 600, standard (not rounded), with the font's own S. It stays separate from the
    # logo; the two only meet in the lockup.
    cap = word_ts.cap * 100 / word_ts.upem
    glyphs, _ = word_ts.paths("SmarType", 100, 0, 0)
    names = [n for n, _, _ in word_ts.glyphs("SmarType")[0]]
    t_index = names.index(word_ts.ttf.getBestCmap()[ord("T")])
    word_all = pathops.Path()
    rest = pathops.Path()
    for i, p in enumerate(glyphs):
        word_all = op(word_all, p, pathops.PathOp.UNION)
        if i != t_index:
            rest = op(rest, p, pathops.PathOp.UNION)
    b = word_all.bounds
    view = f"{b[0]:.2f} {b[1]:.2f} {b[2] - b[0]:.2f} {b[3] - b[1]:.2f}"
    ww, wh = b[2] - b[0], b[3] - b[1]
    tb = glyphs[t_index].bounds
    tgrad = svg_grad("tg", bm.BG_STOPS, tb[0], tb[1], tb[2], tb[3])
    for name, colour in (("ink", bm.INK), ("porcelain", bm.PORCELAIN)):
        write(f"svg/wordmark-{name}.svg", svg_doc(f'<path fill="{colour}" d="{d_of(word_all)}"/>', view, round(ww * 4), round(wh * 4)))
        write(f"svg/wordmark-{name}-gradient-t.svg",
              svg_doc(f'<path fill="{colour}" d="{d_of(rest)}"/><path fill="url(#tg)" d="{d_of(glyphs[t_index])}"/>', view, round(ww * 4), round(wh * 4), tgrad))
    # Lockup: icon height = 1.6 × cap height; gap = 0.28 × the icon; icon centred on the cap height.
    ih = 1.6 * cap
    gap = ih * .28
    ix, iy = 0, -cap / 2 - ih / 2
    wx = ih + gap
    lb = (min(ix, wx + b[0]), min(iy, b[1]), max(ix + ih, wx + b[2]), max(iy + ih, b[3]))
    lview = f"{lb[0]:.2f} {lb[1]:.2f} {lb[2] - lb[0]:.2f} {lb[3] - lb[1]:.2f}"
    lw, lh = lb[2] - lb[0], lb[3] - lb[1]
    # ink and porcelain: the normal icon, for light and dark surfaces. on-gradient: the inverse icon with an Ink
    # wordmark, for the brand gradient and other bright colours.
    for name, colour, inverse in (("ink", bm.INK, False), ("porcelain", bm.PORCELAIN, False), ("on-gradient", bm.INK, True)):
        lock_defs, lbg, lfg = icon_svg_parts(sh, "l", inverse)
        lock_defs += '<clipPath id="lr"><rect x="18" y="18" width="72" height="72" rx="16"/></clipPath>'
        icon_g = f'<g transform="translate({ix:.2f} {iy:.2f}) scale({ih / 72:.5f}) translate(-18 -18)"><g clip-path="url(#lr)">{lbg}{lfg}</g></g>'
        body = icon_g + f'<g transform="translate({wx:.2f} 0)"><path fill="{colour}" d="{d_of(word_all)}"/></g>'
        txt = write(f"svg/lockup-{name}.svg", svg_doc(body, lview, round(lw * 4), round(lh * 4), lock_defs))
        render_png(open(txt).read(), os.path.join(OUT, f"png/lockup-{name}.png"), round(lw * 4), round(lh * 4))

    # PNGs
    jobs = [(full, "png/play-store-icon-512.png", 512), (rounded, "png/icon-rounded-1024.png", 1024), (rounded, "png/logo-480.png", 480),
            (full, "web/apple-touch-icon.png", 180), (rounded, "web/icon-192.png", 192), (rounded, "web/icon-512.png", 512),
            (full, "web/icon-maskable-512.png", 512), (rounded, "web/favicon-32.png", 32), (rounded, "web/favicon-16.png", 16)]
    for svg_text, rel, px in jobs:
        sized = svg_text.replace('width="512" height="512"', f'width="{px}" height="{px}"', 1)
        render_png(sized, os.path.join(OUT, rel), px, px)
    write("web/site.webmanifest",
          '{\n  "name": "SmarType",\n  "short_name": "SmarType",\n  "icons": [\n'
          '    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},\n'
          '    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},\n'
          '    {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}\n  ],\n'
          '  "theme_color": "#22C3CF",\n  "background_color": "#F7F9FA",\n  "display": "standalone"\n}\n')
    print("kit written to", OUT)


if __name__ == "__main__":
    main()
