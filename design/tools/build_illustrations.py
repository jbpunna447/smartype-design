"""Exports the illustration set (src/illustration_set.py) into assets/illustrations.

For each illustration: an animated SVG for light and dark surfaces, a still SVG frozen at its key moment (for
reduced motion), and still PNGs at 3x. Needs Google Chrome for the PNGs.

    python tools/build_illustrations.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from illustration_set import SET, STILL_AT  # noqa: E402
from mascot_cast import CAST_PRESETS, render_mascot_svg  # noqa: E402

OUT = os.path.join(ROOT, "assets", "illustrations")
CAST_OUT = os.path.join(ROOT, "assets", "illustrations-cast")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = '<style>@import url("https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&amp;display=swap");</style>'
# Dark surfaces: ink drawn straight onto the background turns light, and the spark uses the AI gradient.
DARK_VARS = "--ill-ink:#E3EEF0;--sp0:#2AA8E0;--sp1:#3CC4C1;--sp2:#4BDCA4"


def standalone(svg, dark=False, still_at=None):
    """A self-contained SVG file: xmlns, the font, dark variables on the root, and an optional frozen frame."""
    svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    if dark:
        svg = svg.replace("<svg ", f'<svg style="{DARK_VARS}" ', 1)
    cls = re.search(r'<svg[^>]* class="([^"]+)"', svg).group(1)
    extra = FONTS
    if still_at is not None:
        extra += f"<style>.{cls} * {{ animation-play-state: paused !important; animation-delay: -{still_at}s !important; }}</style>"
    return re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + extra, svg, count=1) + "\n"


def render(svg_text, path, px):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "p.html")
        with open(page, "w") as fh:
            fh.write('<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&display=swap">'
                     f'</head><body style="margin:0;background:transparent">{svg_text}</body></html>')
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        "--virtual-time-budget=1500", f"--window-size={px},{px}", f"--screenshot={path}", "file://" + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_cast_illustrations():
    for sub in ("svg", "still"):
        shutil.rmtree(os.path.join(CAST_OUT, sub), ignore_errors=True)
        os.makedirs(os.path.join(CAST_OUT, sub))
    for slug, _title, _subtitle, _spec, still_at in CAST_PRESETS:
        uid = f"cast-{slug}"
        for dark, suffix in ((False, ""), (True, "-dark")):
            svg_raw = render_mascot_svg(200, preset=slug, uid=uid)
            with open(os.path.join(CAST_OUT, f"svg/{slug}{suffix}.svg"), "w") as fh:
                fh.write(standalone(svg_raw, dark))
            with open(os.path.join(CAST_OUT, f"still/{slug}{suffix}.svg"), "w") as fh:
                fh.write(standalone(svg_raw, dark, still_at))
    print("illustrations-cast written to", CAST_OUT)
    return CAST_OUT


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if "--cast-only" in args:
        build_cast_illustrations()
        return
    for sub in ("svg", "still", "png"):
        shutil.rmtree(os.path.join(OUT, sub), ignore_errors=True)
        os.makedirs(os.path.join(OUT, sub))
    for name, title, where, dp, fn, kind in SET:
        t = STILL_AT[name]
        for dark, suffix in ((False, ""), (True, "-dark")):
            with open(os.path.join(OUT, f"svg/{name}{suffix}.svg"), "w") as fh:
                fh.write(standalone(fn(dp), dark))
            still = standalone(fn(dp), dark, t)
            with open(os.path.join(OUT, f"still/{name}{suffix}.svg"), "w") as fh:
                fh.write(still)
            render(standalone(fn(dp * 3), dark, t), os.path.join(OUT, f"png/{name}{suffix}@3x.png"), dp * 3)
    print("illustrations written to", OUT)
    build_cast_illustrations()


if __name__ == "__main__":
    main()
