"""Play Store phone screenshots: 1080 × 1920 (9:16), one panoramic scene across all eight.

Each screenshot has a big outcome-led headline, the moment zoomed in (before → after) floating over a slab of the
real UI, and the key character reacting. Soft brand-gradient shapes run across the frame edges, so the set reads as
one strip in the store. Light and dark frames alternate for rhythm. No device frame (Google advises against it).

The UI slabs come from the real-size mockups in screens.py; before upload, each is replaced by a capture of the
shipped app, cropped to the same window (see `crop`)."""
from brand_marks import BG_STOPS, INK, SPARK_PATH, SPARK_STOPS
from illustration_concepts import _id, _spark
from illustration_set import character
from screens import S

W, H = 1080, 1920
LIGHT, DARK = "#F5FAFB", "#0B1416"
AI = [(0, "#2AA8E0"), (1, "#4BDCA4")]


def _stops(stops):
    return ", ".join(f"{c} {o * 100:.0f}%" for o, c in stops)


def _key(mode, px, look=(0, 0)):
    """The key character as a small SVG, px wide."""
    p = _id("pk")
    return f'<svg width="{px}" height="{px}" viewBox="0 0 100 100" aria-hidden="true">{character(10, 8, 80, mode, p, look)}</svg>'


def _sparkle(px, stops=SPARK_STOPS):
    p = _id("ps")
    return f'<svg width="{px}" height="{px}" viewBox="-12 -12 24 24" aria-hidden="true">{_spark(p, 22, stops)}</svg>'


def _bubble(text, cls="", style=""):
    return f'<div class="pl-bub {cls}" style="{style}">{text}</div>'


SQUIGGLE = ('<svg class="sq" viewBox="0 0 120 8" preserveAspectRatio="none" aria-hidden="true"><path d="M0 4 q5 -5 10 0 t10 0 t10 0 t10 0 t10 0 t10 0 t10 0 t10 0 t10 0 t10 0 t10 0 t10 0" '
            'fill="none" stroke="#E5395B" stroke-width="2.5"/></svg>')

# Each frame: screen id, theme, headline (with one <em> accent), crop (y0, y1 in dp: the content plus 24 dp of air on top,
# down to the keyboard's bottom edge, never the nav bar; the slab sits flush with the frame's bottom edge),
# extras (HTML placed absolutely), alt text (<= 140 characters).
FRAMES = [
    dict(sid="ai-open", theme="light", head="Fix any message <em>in one tap</em>", crop=(332, 776),
         extras=(_bubble('im <span class="typo">runing' + SQUIGGLE + '</span> late sry', "before", "left:290px;top:500px;transform:rotate(-3deg)") +
                 f'<div class="pl-arrow" style="left:560px;top:640px">↓</div>' +
                 f'<div style="position:absolute;left:66px;top:510px">{_key("surprised", 230, (.04, -.02))}</div>' +
                 f'<div style="position:absolute;left:830px;top:470px">{_sparkle(120)}</div>'),
         alt="SmarType fixing a typo-filled message, im runing late sry, into I'm running late for the meeting, sorry."),
    dict(sid="tr-open", theme="light", head="Type in English. <em>Send it in Hindi.</em>", crop=(332, 776),
         extras=(_bubble("Running late, sorry!", "", "left:80px;top:470px") +
                 f'<div class="pl-badge" style="left:700px;top:470px">文A</div>' +
                 _bubble("देर हो रही है, माफ़ करना!", "ai", "right:80px;top:640px")),
         alt="SmarType translating Running late, sorry from English into Hindi, with English, Hindi and Telugu to choose from"),
    dict(sid="vo-listen", theme="dark", head="Just speak. <em>It's tidied up.</em>", crop=(332, 776),
         extras=(_bubble("um so like I'm on my way, be there in ten", "raw", "left:80px;top:420px;max-width:920px") +
                 f'<div class="pl-arrow dark" style="left:620px;top:545px">↓</div>' +
                 _bubble("On my way, be there in 10!", "ai", "right:80px;top:625px") +
                 f'<div style="position:absolute;left:70px;top:570px">{_key("asleep", 170)}</div>'),
         alt="Voice typing in SmarType: rambling speech turned into a clean message, On my way, be there in 10!"),
    dict(sid="fm-open", theme="light", head="Rough notes, <em>neat lists</em>", crop=(356, 776),
         extras=(_bubble("need: tickets, hotel for 2 nights, cab, dinner sat", "note", "left:70px;top:470px;transform:rotate(-2deg)") +
                 f'<div style="position:absolute;right:70px;top:440px">{_key("happy", 190)}</div>'),
         alt="SmarType turning a run-on list into tidy bullet points: train tickets, hotel for 2 nights, cab, dinner"),
    dict(sid="nt-changed", theme="light", head="Notes that <em>AI can polish</em>", crop=(24, 520),
         extras=(_bubble("add that I'll pay the rent on Friday", "ask", "left:80px;top:430px;max-width:600px") +
                 f'<div style="position:absolute;right:80px;top:410px">{_key("focus", 190, (-.03, .02))}</div>'),
         alt="A SmarType note changed by AI after asking, add that I'll pay the rent on Friday, with Undo and Insert"),
    dict(sid="cb-open", theme="light", head="Copied it? <em>Paste in one tap.</em>", crop=(332, 776),
         extras=(_bubble("Order #48213 confirmed for Friday", "", "left:80px;top:480px;transform:rotate(-2deg);max-width:600px") +
                 f'<div style="position:absolute;right:90px;top:470px">{_key("watch", 190, (-.04, .03))}</div>'),
         alt="The SmarType clipboard in the keyboard with pinned and recent clips, ready to paste"),
    dict(sid="lg-globe", theme="dark", head="English and Hindi, <em>one key apart</em>", crop=(332, 776),
         extras=(_bubble("See you tomorrow", "", "left:80px;top:460px") + _bubble("कल मिलते हैं", "ai", "right:80px;top:610px") +
                 '<div class="pl-globe" style="left:420px;top:590px"><svg aria-hidden="true"><use href="#ms-language"/></svg></div>'),
         alt="Switching the SmarType keyboard between English and Hindi with the globe key"),
    dict(sid="privacy", theme="dark", head="Your typing <em>stays on your phone</em>", graphic=True,
         extras=(f'<div style="position:absolute;left:250px;top:470px">{_key("happy", 250)}</div>'
                 '<div class="pl-lock" style="left:560px;top:490px"><svg aria-hidden="true"><use href="#ms-lock"/></svg></div>'
                 + "".join(f'<div class="pl-promise" style="top:{860 + i * 330}px"><div class="ic"><svg aria-hidden="true"><use href="#{ref}"/></svg></div>'
                           f'<div><b>{t}</b><span>{d}</span></div></div>'
                           for i, (ref, t, d) in enumerate([("ms-keyboard", "Typing stays on your phone", "Suggestions are learned on the device"),
                                                            ("br-spark", "AI sees only what you send", "Only when you tap Rewrite, Translate or Format"),
                                                            ("ms-lock", "Passwords stay private", "No AI, no voice, nothing learned in password fields")]))),
         alt="SmarType privacy: typing stays on the phone, AI sees only what you send, password fields stay private"),
]


# Every UI slab uses the same scale, so text in the app reads the same size in each screenshot.
SLAB_K = 2.6


def _backdrop(i, theme):
    """A slice of one long scene: soft gradient blobs whose centres sit on frame edges, so shapes carry across."""
    base = LIGHT if theme == "light" else DARK
    op = .30 if theme == "light" else .38
    blobs = ""
    for j in range(len(FRAMES) + 1):
        cy = 380 if j % 2 else 1560
        blobs += f'<circle cx="{j * W}" cy="{cy}" r="520" fill="url(#bg{i})" opacity="{op}"/>'
        blobs += f'<circle cx="{j * W + 540}" cy="{1920 - cy + 200}" r="240" fill="url(#bg{i})" opacity="{op * .6:.2f}"/>'
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in BG_STOPS)
    return (f'<svg class="pl-bg" width="{W}" height="{H}" viewBox="{i * W} 0 {W} {H}" aria-hidden="true">'
            f'<defs><radialGradient id="bg{i}"><stop offset="0" stop-color="#22C3CF"/><stop offset=".55" stop-color="#1E9BD7" stop-opacity=".7"/>'
            f'<stop offset="1" stop-color="#4BDCA4" stop-opacity="0"/></radialGradient><linearGradient id="bgl{i}" x1="0" x2="1">{stops}</linearGradient></defs>'
            f'<rect x="{i * W}" width="{W}" height="{H}" fill="{base}"/>{blobs}</svg>')


def frame_html(i, root=""):
    f = FRAMES[i]
    slab = ""
    if not f.get("graphic"):
        y0, y1 = f["crop"]
        k = SLAB_K
        sw, sh = 360 * k, (y1 - y0) * k
        f = dict(f, top=round(H - sh))  # flush with the bottom edge; only the top corners are rounded
        dev = S[f["sid"]].replace("{root}", root)
        slab = (f'<div class="pl-slab" style="left:{(W - sw) / 2:.0f}px;top:{f["top"]}px;width:{sw:.0f}px;height:{sh:.0f}px">'
                f'<div class="pl-dev" style="transform: translateY({-y0 * k:.0f}px) scale({k})">{dev}</div></div>')
    tone = "ink" if f["theme"] == "light" else "porcelain"
    brand = f'<img class="pl-brand" src="{root}assets/brand/lockup-{tone}.svg" alt="SmarType">'
    return (f'<div class="pl {f["theme"]}" role="img" aria-label="{f["alt"]}">{_backdrop(i, f["theme"])}{brand}'
            f'<h1 class="pl-head">{f["head"]}</h1>{slab}{f["extras"]}</div>')


STYLE = f"""
.pl {{ width: {W}px; height: {H}px; position: relative; overflow: hidden; font-family: "Google Sans Flex", "DM Sans", sans-serif; }}
.pl-bg {{ position: absolute; inset: 0; }}
.pl-brand {{ position: absolute; left: 72px; top: 62px; height: 58px; }}
.pl-head {{ position: absolute; left: 72px; right: 72px; top: 168px; margin: 0; font-weight: 700; font-size: 92px; line-height: 1.04;
  letter-spacing: -.025em; color: {INK}; text-wrap: balance; }}
.pl.dark .pl-head {{ color: #F2F8F9; }}
.pl-head em {{ font-style: normal; background: linear-gradient(120deg, {_stops(SPARK_STOPS)}); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.pl.dark .pl-head em {{ background-image: linear-gradient(120deg, {_stops(AI)}); }}
.pl-slab {{ position: absolute; overflow: hidden; border-radius: 56px 56px 0 0; box-shadow: 0 40px 90px rgba(8,50,59,.22), 0 0 0 1px rgba(8,50,59,.06); }}
.pl.dark .pl-slab {{ box-shadow: 0 40px 90px rgba(0,0,0,.5), 0 0 0 1px rgba(255,255,255,.08); }}
.pl-dev {{ width: 360px; transform-origin: 0 0; }}
.pl .s-dev {{ border-radius: 0; box-shadow: none; }}
.pl .s-status, .pl .s-gnav {{ visibility: hidden; }}
.pl-bub {{ position: absolute; z-index: 3; max-width: 760px; padding: 26px 38px; border-radius: 44px; background: #FFFFFF; color: {INK};
  font-size: 46px; font-weight: 600; line-height: 1.2; box-shadow: 0 20px 50px rgba(8,50,59,.18); }}
.pl-bub.ai {{ background: linear-gradient(120deg, {_stops(AI)}); }}
.pl-bub.raw {{ background: rgba(255,255,255,.12); color: #C6D6DA; font-weight: 500; font-style: italic; box-shadow: none; border: 2px dashed rgba(255,255,255,.3); }}
.pl-bub.note {{ background: #FFF8E6; border-radius: 22px; font-weight: 500; max-width: 600px; }}
.pl-bub.ask {{ background: #FFFFFF; border: 3px solid #2AA8E0; }}
.pl-bub.before {{ font-weight: 500; }}
.pl-bub .typo {{ position: relative; display: inline-block; }}
.pl-bub .sq {{ position: absolute; left: 0; right: 0; bottom: -10px; width: 100%; height: 12px; }}
.pl-arrow {{ position: absolute; z-index: 3; font-size: 84px; font-weight: 700; color: #1E9BD7; }}
.pl-arrow.dark {{ color: #4BDCA4; }}
.pl-badge {{ position: absolute; z-index: 4; width: 120px; height: 120px; border-radius: 60px; display: grid; place-items: center;
  background: linear-gradient(135deg, {_stops(AI)}); color: {INK}; font-size: 46px; font-weight: 700; box-shadow: 0 16px 40px rgba(8,50,59,.25); }}
.pl-globe {{ position: absolute; z-index: 4; width: 130px; height: 130px; border-radius: 65px; background: linear-gradient(135deg, {_stops(AI)}) ; box-shadow: 0 16px 40px rgba(0,0,0,.35); }}
.pl-globe {{ display: grid; place-items: center; color: {INK}; }} .pl-globe svg {{ width: 76px; height: 76px; fill: currentColor; }}
.pl-lock {{ position: absolute; z-index: 3; width: 210px; height: 210px; border-radius: 105px; display: grid; place-items: center;
  background: linear-gradient(135deg, {_stops(AI)}); color: {INK}; box-shadow: 0 24px 60px rgba(0,0,0,.45); }}
.pl-lock svg {{ width: 120px; height: 120px; fill: currentColor; }}
.pl-promise {{ position: absolute; left: 72px; right: 72px; height: 280px; box-sizing: border-box; display: flex; align-items: center; gap: 40px; padding: 0 48px;
  border-radius: 48px; background: rgba(255,255,255,.07); border: 2px solid rgba(255,255,255,.12); color: #F2F8F9; }}
.pl-promise .ic {{ flex: 0 0 140px; height: 140px; border-radius: 40px; display: grid; place-items: center; background: linear-gradient(135deg, {_stops(AI)}); color: {INK}; }}
.pl-promise .ic svg {{ width: 76px; height: 76px; fill: currentColor; }}
.pl-promise b {{ display: block; font-size: 52px; line-height: 1.1; font-weight: 700; letter-spacing: -.01em; }}
.pl-promise span {{ display: block; margin-top: 12px; font-size: 36px; line-height: 1.25; color: #B5CACF; }}
.pl > div[style*="position:absolute"] svg {{ display: block; filter: drop-shadow(0 16px 30px rgba(8,50,59,.22)); }}
"""


# ---------- feature graphic: 1024 × 500 ----------
# Google: focal point in the centre, nothing important near the edges (Play may crop or overlay them, and a promo
# video's play button sits on top), vibrant colours, branding that extends the icon rather than repeats it, no device
# imagery and no "Best", "#1" or "Free". Every option carries the SmarType lockup in the centre safe area.
FW, FH = 1024, 500


def _fb(text, cls="", style=""):
    return f'<div class="fg-b {cls}" style="{style}">{text}</div>'


def _typo(word):
    return f'<span class="typo">{word}{SQUIGGLE}</span>'


def _voice(style):
    bars = "".join(f'<i style="height:{h}px"></i>' for h in (14, 26, 40, 22, 34, 18, 30))
    return f'<div class="fg-voice" style="{style}"><svg aria-hidden="true"><use href="#ms-mic"/></svg><span>{bars}</span></div>'


def _logo(root, tone, style):
    return f'<img class="fg-logo" src="{root}assets/brand/lockup-{tone}.svg" alt="SmarType" style="{style}">'


def _feature_a(root):
    bg = "linear-gradient(135deg, " + _stops(BG_STOPS) + ")"
    return (f'<div class="fg" style="background:{bg}"><div class="fg-light"></div>'
            + _fb("im " + _typo("runing") + " late sry", "", "left:92px;top:96px;transform:rotate(-4deg)")
            + _fb("Running late, sorry!", "", "left:120px;top:190px;transform:rotate(2deg)")
            + _fb("देर हो रही है", "", "right:96px;top:100px;transform:rotate(3deg)")
            + _voice("right:132px;top:186px")
            + f'<div class="fg-at" style="left:{FW / 2 - 90:.0f}px;top:52px">{_key("happy", 180)}</div><div class="fg-at" style="left:{FW / 2 + 66:.0f}px;top:30px">{_sparkle(60)}</div>'
            + '<h1 class="fg-head" style="top:280px">Type it. Say it. <em class="w">Get it right.</em></h1>'
            + _logo(root, "on-gradient", f"left:{FW / 2 - 120:.0f}px;top:380px;height:45px") + "</div>")


def _feature_b(root):
    glow = f"radial-gradient(circle at 50% 42%, rgba(34,195,207,.55), rgba(30,155,215,.25) 28%, rgba(11,20,22,0) 55%)"
    return (f'<div class="fg" style="background:{glow}, #0B1416">'
            '<div class="fg-ring" style="left:332px;top:-28px;width:360px;height:360px"></div><div class="fg-ring" style="left:392px;top:32px;width:240px;height:240px;opacity:.5"></div>'
            + _fb("im " + _typo("runing") + " late sry", "glass trail-r", "left:96px;top:92px")
            + _fb("Running late, sorry!", "trail-r", "left:126px;top:196px")
            + _fb("देर हो रही है", "trail-l", "right:110px;top:100px")
            + _voice("right:140px;top:206px;background:#16262A")
            + f'<div class="fg-at" style="left:{FW / 2 - 85:.0f}px;top:58px">{_key("surprised", 170)}</div><div class="fg-at" style="left:{FW / 2 + 60:.0f}px;top:36px">{_sparkle(56, AI)}</div>'
            + '<h1 class="fg-head light" style="top:262px">Type it. Say it. <em class="g">Get it right.</em></h1>'
            + _logo(root, "porcelain", f"left:{FW / 2 - 120:.0f}px;top:370px;height:45px") + "</div>")


def _feature_c(root):
    bg = "linear-gradient(180deg, #1E9BD7 0%, #22C3CF 55%, #4BDCA4 100%)"
    rows = [10, 9, 9, 7]
    keys = ""
    for r, n in enumerate(rows):
        cells = "".join(f'<i class="{"sp" if (r == 3 and c == 3) else ""}"></i>' for c in range(n))
        keys += f'<div class="r r{r}">{cells}</div>'
    return (f'<div class="fg" style="background:{bg}"><div class="fg-light"></div>'
            f'<div class="fg-kb">{keys}</div>'
            + _logo(root, "on-gradient", f"left:{FW / 2 - 108:.0f}px;top:30px;height:40px")
            + '<h1 class="fg-head" style="top:82px;font-size:50px">Type it. Say it. <em class="w">Get it right.</em></h1>'
            + _fb("Running late, sorry!", "rise", "left:118px;top:186px;transform:rotate(-6deg)")
            + _fb("On my way!", "rise", "right:150px;top:176px;transform:rotate(5deg)")
            + _fb("कल मिलते हैं", "rise", "right:96px;top:262px;transform:rotate(-3deg)")
            + f'<div class="fg-at" style="left:{FW / 2 - 70:.0f}px;top:200px">{_key("happy", 140)}</div><div class="fg-at" style="left:{FW / 2 + 50:.0f}px;top:184px">{_sparkle(46)}</div>'
            + "</div>")


def _feature_d(root):
    vivid = "linear-gradient(135deg, " + _stops(BG_STOPS) + ")"
    return (f'<div class="fg" style="background:#D9E0E2">'
            f'<div class="fg-half" style="background:{vivid}"><div class="fg-light"></div></div>'
            + _logo(root, "on-gradient", f"left:{FW / 2 - 108:.0f}px;top:34px;height:40px")
            + _fb("im " + _typo("runing") + " late sry", "dull", "left:110px;top:150px;transform:rotate(-3deg)")
            + _fb("I'm running late, sorry!", "", "right:96px;top:150px;transform:rotate(2deg)")
            + f'<div class="fg-at" style="left:{FW / 2 - 80:.0f}px;top:140px">{_key("happy", 160)}</div><div class="fg-at fg-throw" style="left:{FW / 2 + 70:.0f}px;top:120px">{_sparkle(54)}</div>'
            + '<h1 class="fg-head" style="top:330px;font-size:52px">From typo to right, <em class="w">in one tap</em></h1></div>')


def _feature_e(root):
    bg = "linear-gradient(135deg, " + _stops(BG_STOPS) + ")"
    words = [("Hello", 150, 92, -6), ("नमस्ते", 300, 46, 4), ("Hola", 196, 196, 3), ("வணக்கம்", 96, 252, -4),
             ("こんにちは", 650, 52, -3), ("Bonjour", 790, 140, 5), ("你好", 650, 196, -5), ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", 760, 236, 3)]
    bubbles = "".join(_fb(w, "sm", f"left:{x}px;top:{y}px;transform:rotate({r}deg)") for w, x, y, r in words)
    return (f'<div class="fg" style="background:{bg}"><div class="fg-light"></div>'
            '<div class="fg-ring" style="left:362px;top:30px;width:300px;height:300px;border-color:rgba(255,255,255,.55)"></div>' + bubbles
            + f'<div class="fg-at" style="left:{FW / 2 - 80:.0f}px;top:92px">{_key("happy", 160)}</div><div class="fg-at" style="left:{FW / 2 + 56:.0f}px;top:74px">{_sparkle(52)}</div>'
            + '<h1 class="fg-head" style="top:336px;font-size:50px">Write it right, <em class="w">in your language</em></h1>'
            + _logo(root, "on-gradient", f"left:{FW / 2 - 96:.0f}px;top:410px;height:36px") + "</div>")


FEATURES = [
    ("a", "A · Moments", "The key in the centre, a typo fixed, Hindi and voice around it", _feature_a,
     "The SmarType key fixing a typo, translating into Hindi and turning speech into text, on the brand gradient"),
    ("b", "B · Spotlight", "Dark and premium: the brand gradient glows behind the key; bubbles float in with soft trails", _feature_b,
     "The SmarType key in a spotlight of the brand gradient, with a fixed typo, Hindi and voice floating around it"),
    ("c", "C · Keyboard horizon", "A big keyboard sweeps across the bottom; the key stands on it as words rise off the keys", _feature_c,
     "The SmarType key standing on a keyboard as messages in English and Hindi rise off the keys"),
    ("d", "D · Before and after", "Grey on the left with the typo, vivid on the right with the fix; the key throws the spark across", _feature_d,
     "A typo on a grey half turned into a correct message on a bright half by the SmarType key"),
    ("e", "E · Every language", "Greetings in eight scripts burst around the key", _feature_e,
     "The SmarType key surrounded by greetings in English, Hindi, Tamil, Punjabi, Spanish, French, Japanese and Chinese"),
]


FEATURE_STYLE = f"""
.fg {{ width: {FW}px; height: {FH}px; position: relative; overflow: hidden; font-family: "Google Sans Flex", "DM Sans", sans-serif; }}
.fg-light {{ position: absolute; inset: 0; background: radial-gradient(circle at 22% 8%, rgba(255,255,255,.5), rgba(255,255,255,0) 55%); pointer-events: none; }}
.fg-at {{ position: absolute; z-index: 4; }} .fg-at svg {{ display: block; filter: drop-shadow(0 18px 30px rgba(8,50,59,.3)); }}
.fg-head {{ position: absolute; z-index: 4; left: 0; right: 0; margin: 0; text-align: center; font-weight: 700; font-size: 56px; line-height: 1.05; letter-spacing: -.02em; color: {INK}; }}
.fg-head.light {{ color: #F2F8F9; }}
.fg-head em {{ font-style: normal; }} .fg-head em.w {{ color: #FFFFFF; text-shadow: 0 2px 18px rgba(8,50,59,.25); }}
.fg-head em.g {{ background: linear-gradient(120deg, {_stops(AI)}); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.fg-logo {{ position: absolute; z-index: 4; }}
.fg-b {{ position: absolute; z-index: 3; padding: 14px 22px; border-radius: 26px; background: #FFFFFF; color: {INK}; font-size: 26px; font-weight: 600;
  line-height: 1.2; white-space: nowrap; box-shadow: 0 12px 30px rgba(8,50,59,.2); }}
.fg-b.sm {{ font-size: 24px; padding: 11px 18px; }}
.fg-b.glass {{ background: rgba(255,255,255,.1); color: #E3EEF0; border: 1.5px solid rgba(255,255,255,.25); box-shadow: none; }}
.fg-b.dull {{ background: #F1F3F4; color: #6B7A7E; box-shadow: 0 8px 20px rgba(0,0,0,.08); }}
.fg-b.rise {{ box-shadow: 0 14px 34px rgba(8,50,59,.25); }}
.fg-b.trail-r::before, .fg-b.trail-l::before {{ content: ""; position: absolute; top: 50%; width: 90px; height: 3px; border-radius: 2px; }}
.fg-b.trail-r::before {{ right: 100%; margin-right: 10px; background: linear-gradient(90deg, rgba(75,220,164,0), rgba(75,220,164,.8)); }}
.fg-b.trail-l::before {{ left: 100%; margin-left: 10px; background: linear-gradient(270deg, rgba(42,168,224,0), rgba(42,168,224,.8)); }}
.fg-b .typo {{ position: relative; display: inline-block; }} .fg-b .sq {{ position: absolute; left: 0; right: 0; bottom: -7px; width: 100%; height: 8px; }}
.fg-voice {{ position: absolute; z-index: 3; display: flex; align-items: center; gap: 12px; padding: 12px 20px; border-radius: 30px; background: {INK}; color: #DFF6F2;
  box-shadow: 0 12px 30px rgba(8,50,59,.25); }}
.fg-voice svg {{ width: 28px; height: 28px; fill: currentColor; }} .fg-voice span {{ display: flex; align-items: center; gap: 5px; }}
.fg-voice i {{ display: block; width: 6px; border-radius: 3px; background: linear-gradient(180deg, #4BDCA4, #2AA8E0); }}
.fg-ring {{ position: absolute; border-radius: 50%; border: 2px dashed rgba(75,220,164,.45); }}
.fg-kb {{ position: absolute; left: -120px; right: -120px; top: 318px; height: 330px; transform: perspective(520px) rotateX(48deg); transform-origin: 50% 0;
  display: flex; flex-direction: column; gap: 14px; padding: 18px 40px; background: rgba(255,255,255,.28); border-radius: 30px; }}
.fg-kb .r {{ display: flex; gap: 14px; justify-content: center; }} .fg-kb i {{ display: block; width: 92px; height: 60px; border-radius: 14px; background: #FFFFFF;
  box-shadow: 0 6px 0 #C3D5DA; }} .fg-kb .r3 i.sp {{ width: 420px; }}
.fg-half {{ position: absolute; left: 512px; top: 0; bottom: 0; right: 0; clip-path: polygon(6% 0, 100% 0, 100% 100%, 0 100%); }}
.fg-throw svg {{ transform: rotate(20deg); }}
"""
