"""Renders the Play Store screenshots (site/store/frame-*.html, written by build_site.py) to 1080 × 1920 PNGs
without transparency, into assets/store/en. Run build_site.py first, then this, then build_site.py again.

    python tools/build_store.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import store  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(ROOT, "assets", "store", "en")


def main():
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    for i, f in enumerate(store.FRAMES):
        sid = f["sid"]
        page = os.path.join(ROOT, "site", "store", f"frame-{i + 1:02d}.html")
        png = os.path.join(OUT, f"{i + 1:02d}-{sid}.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--virtual-time-budget=3000", f"--window-size={store.W},{store.H}", f"--screenshot={png}", "file://" + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Play wants a 24-bit PNG with no alpha.
        Image.open(png).convert("RGB").save(png, optimize=True)
    for key, title, desc, fn, alt in store.FEATURES:
        page = os.path.join(ROOT, "site", "store", f"feature-{key}.html")
        png = os.path.join(OUT, f"feature-{key}.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--virtual-time-budget=3000", f"--window-size={store.FW},{store.FH}", f"--screenshot={png}", "file://" + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        Image.open(png).convert("RGB").save(png, optimize=True)
    with open(os.path.join(OUT, "alt-text.txt"), "w") as fh:
        fh.write("".join(f"{i + 1:02d}-{f['sid']}.png\t{f['alt']}\n" for i, f in enumerate(store.FRAMES)))
        fh.write("".join(f"feature-{key}.png\t{alt}\n" for key, title, desc, fn, alt in store.FEATURES))
    print("screenshots written to", OUT)


if __name__ == "__main__":
    main()
