"""Builders for the real-size spec mockups (1 CSS px = 1 dp).

Every annotated element gets data attributes that spec.js turns into the
measurement overlay and the element table under each screen:
  data-el  element name      data-c  component      data-t  tokens      data-i  icon
"""
import html
import os
import re

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/icons")


def esc(s):
    return html.escape(s, quote=True)


def ann(name=None, comp=None, tok=None, icon=None):
    out = ""
    if name:
        out += f' data-el="{esc(name)}"'
    if comp:
        out += f' data-c="{esc(comp)}"'
    if tok:
        out += f' data-t="{esc(tok)}"'
    if icon:
        out += f' data-i="{esc(icon)}"'
    return out


def sprite():
    """All icons as SVG symbols: Material Symbols Rounded (ms-*) and the brand spark (br-spark)."""
    syms = []
    ms = os.path.join(ICON_DIR, "material-symbols-rounded")
    for f in sorted(os.listdir(ms)):
        if not f.endswith(".svg"):
            continue
        s = open(os.path.join(ms, f)).read()
        inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
        syms.append(f'<symbol id="ms-{f[:-4]}" viewBox="0 -960 960 960">{inner}</symbol>')
    s = open(os.path.join(ICON_DIR, "brand/spark.svg")).read()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    syms.append(f'<symbol id="br-spark" viewBox="0 0 24 24">{inner}</symbol>')
    g = open(os.path.join(ICON_DIR, "brand/google-g.svg")).read()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", g, re.S).group(1)
    syms.append(f'<symbol id="br-google" viewBox="0 0 21 20">{inner}</symbol>')
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(syms) + "</svg>"


def ic(name, fill=False, size=24):
    cls = "s-ic" + ("" if size == 24 else f" s{size}")
    ref = "br-spark" if name == "spark" else ("br-google" if name == "google" else f"ms-{name}{'-fill' if fill else ''}")
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{ref}"/></svg>'


# ---------- frame ----------

def device(body, app=False, width=360, ime=False):
    style = f' style="--w:{width}px"' if width != 360 else ""
    nav = '<div class="s-gnav kb"><i></i></div>' if ime else '<div class="s-gnav"><i></i></div>'
    return (f'<div class="s-dev{" app" if app else ""}"{style}{ann("Screen", f"Phone, {width} × 800 dp")}>'
            f'<div class="s-status"><span>9:41</span><span>▾ ▴ ▮</span></div>{body}{nav}</div>')


def chat(title="Priya", msgs=("Are you joining at 4?",), text=None, placeholder="Message", caret=True, field_ann=True):
    bubbles = "".join(f'<div class="s-bub">{esc(m)}</div>' for m in msgs)
    content = (esc(text) if text else f'<span class="ph">{esc(placeholder)}</span>') + ('<span class="s-caret"></span>' if caret else "")
    fa = ann("Text field (the other app)", "Not ours: the app the user types into") if field_ann else ""
    return (f'<div class="s-host"><div class="s-hbar"><span class="s-av">{title[0]}</span>{esc(title)}</div>'
            f'<div class="s-msgs">{bubbles}</div><div class="s-field"{fa}>{content}</div></div>')


# ---------- keyboard ----------

SMARTBAR = [
    ("spark", "Rewrite", True), ("translate", "Translate", True), ("format_list_bulleted", "Format", True),
    ("content_paste", "Clipboard", False), ("sticky_note_2", "Notes", False), ("mood", "Emoji", False),
    ("more_horiz", "More", False),
]


def smartbar(emoji=False, annotate=True):
    btns = []
    for icon, label, ai in SMARTBAR:
        if label == "Emoji" and not emoji:
            continue
        cls = "s-btn " + ("ai" if ai else "plain")
        a = ""
        if annotate and label == "Rewrite":
            a = ann("AI action button", "Touch target 48 × 48 dp; circle 36 dp; icon 20 dp",
                    "ai-gradient-start → ai-gradient-end (135°); icon on-ai-gradient", "spark (brand)")
        elif annotate and label == "Clipboard":
            a = ann("Plain action button", "Touch target 48 × 48 dp; icon 24 dp", "icon: keyboard on-surface-variant", "content_paste")
        btns.append(f'<div class="{cls}" title="{label}"{a}><div class="c">{ic(icon, size=20 if ai else 24)}</div></div>')
    mic_a = ann("Mic button", "Same as an AI action button, pinned to the right", "ai-gradient", "mic") if annotate else ""
    btns.append('<div class="s-sp"></div>')
    btns.append(f'<div class="s-btn ai" title="Voice"{mic_a}><div class="c">{ic("mic", size=20)}</div></div>')
    a = ann("Smartbar", "Actions row of the stacked smartbar; height 48 dp; side padding 4 dp",
            "keyboard background") if annotate else ""
    return f'<div class="s-row48"{a}>' + "".join(btns) + "</div>"


def suggestions(words=None, hint=None, snack=None, annotate=True):
    if snack:
        txt, act = snack
        inner = f'<div class="s-snack"{ann("Undo message", "Height 36 dp in the 48 dp row; radius 8 dp; shows 6 s", "keyboard on-background fill; text keyboard background; action inverse-primary")}><span>{esc(txt)}</span><b>{esc(act)}</b></div>'
    elif hint:
        inner = f'<span class="hint">{esc(hint)}</span>'
    elif words:
        inner = "".join(f'<span class="{"b" if i == 1 else ""}">{esc(w)}</span>' for i, w in enumerate(words))
    else:
        inner = ""
    a = ann("Suggestion row", "Suggestion row of the stacked smartbar; height 48 dp, kept when empty",
            "text 16 sp keyboard on-background; centre slot weight 600; dividers keyboard line") if annotate else ""
    return f'<div class="s-row48 s-sugg"{a}>{inner}</div>'


QWERTY = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]


def keys(dim=False, space="", utility="mood", annotate=True, deva=False):
    rows = QWERTY if not deva else ["ौैाीूबहगदज", "ोेअिुपरकत", "ंमनवलसय"]
    r1 = "".join(f'<div class="s-k" style="grid-column:span 2">{c}</div>' for c in rows[0][:10])
    r2 = '<div style="grid-column:span 1"></div>' + "".join(f'<div class="s-k" style="grid-column:span 2">{c}</div>' for c in rows[1][:9])
    r3 = ('<div class="s-k fn" style="grid-column:span 3">⇧</div>' + "".join(f'<div class="s-k" style="grid-column:span 2">{c}</div>' for c in rows[2][:7])
          + '<div class="s-k fn" style="grid-column:span 3">⌫</div>')
    util = ic("language", size=20) if utility == "language" else ic("mood", size=20)
    r4 = (f'<div class="s-k fn" style="grid-column:span 3">?123</div><div class="s-k fn" style="grid-column:span 2">{util}</div>'
          f'<div class="s-k space" style="grid-column:span 10">{esc(space)}</div><div class="s-k fn" style="grid-column:span 2">.</div>'
          '<div class="s-k ent" style="grid-column:span 3">↵</div>')
    a = ann("Keys", "Unchanged. 4 rows × ~55 dp on a 360 × 800 dp phone (keyboard row base height); key radius 8 dp",
            "keyboard theme: key surface, on-surface") if annotate else ""
    return (f'<div class="s-keys{" dim" if dim else ""}"{a}>' + "".join(f'<div class="s-krow">{r}</div>' for r in (r1, r2, r3, r4)) + "</div>")


def ime(*parts):
    return '<div class="s-ime">' + "".join(parts) + "</div>"


def panel(title, body, badge=None, action=None, dock=None, back=True):
    b = ""
    if back:
        b = f'<div class="s-btn" style="color:var(--kb-on)"{ann("Back", "Touch target 48 dp; icon 24 dp; brings back the keyboard and the smartbar (same as system Back)", "keyboard on-background", "arrow_back")}>{ic("arrow_back")}</div>'
    head = (f'<div class="s-phead"{ann("Panel header", "Height 48 dp, in place of the smartbar; title-medium 16/24 sp; 1 dp divider", "keyboard background; divider keyboard line")}>'
            f'{b}<div class="t">{esc(title)}</div>')
    if badge:
        head += f'<span class="s-badge"{ann("Uses-left badge", "Height 24 dp; radius 8 dp; label-small 12 sp", "keyboard key surface; on-surface-variant")}>{esc(badge)}</span>'
    if action:
        head += action
    head += "</div>"
    d = dock or ""
    return (f'<div class="s-panel"{ann("Keyboard panel", "Replaces the smartbar, the suggestion row and the keys: 48 + 48 + 220 = 316 dp. Its header sits where the smartbar was.", "keyboard theme colours (KeyboardPanelColors)")}>'
            f'{head}<div class="s-pbody">{body}</div>{d}</div>')


def chips(items, annotate=True):
    out = []
    first_sel = first_un = True
    for it in items:
        label, kind = (it, "") if isinstance(it, str) else it
        a = ""
        if annotate and kind == "sel" and first_sel:
            a = ann("Selected chip", "Height 32 dp; radius 12 dp; padding 12 dp; label-medium 13 sp", "ai-gradient; on-ai-gradient")
            first_sel = False
        elif annotate and kind == "" and first_un:
            a = ann("Chip", "Height 32 dp; radius 12 dp; 1 dp border; gap 8 dp", "border keyboard line; text on-surface-variant")
            first_un = False
        out.append(f'<span class="s-chip {kind}"{a}>{esc(label)}</span>')
    return '<div class="s-chips">' + "".join(out) + "</div>"


def result(meta, text, right="", annotate=True, skel=False):
    a = ann("Result", "Radius 12 dp; padding 12 dp; meta label 12 sp; text body-large 16/24 sp", "keyboard key surface") if annotate else ""
    if skel:
        body = '<div class="s-skel" style="width:90%"></div><div class="s-skel" style="width:70%"></div>'
    else:
        body = f'<div class="x">{text}</div>'
    return f'<div class="s-res"{a}><div class="m"><span>{esc(meta)}</span><span>{esc(right)}</span></div>{body}</div>'


def dock(*btns, annotate=True):
    out = []
    for i, (label, kind) in enumerate(btns):
        a = ""
        if annotate and kind == "ai":
            a = ann("Main dock action", "Height 48 dp; radius 14 dp; label-large 14 sp", "ai-gradient; on-ai-gradient")
        elif annotate and kind == "q":
            a = ann("Second dock action", "Height 48 dp; radius 14 dp", "keyboard key surface; on-surface")
        out.append(f'<div class="s-b {kind}"{a}>{label}</div>')
    return f'<div class="s-dock"{ann("Dock", "Height 68 dp: 8 top + 48 + 12 bottom; gap 8 dp; content actions only") if annotate else ""}>' + "".join(out) + "</div>"


def kbanner(kind, title, text, act=None, icon=None):
    icon = icon or {"warn": "error", "err": "error", "info": "info"}[kind]
    a = ann({"warn": "Warning banner", "err": "Error banner", "info": "Info banner"}[kind], "Radius 14 dp; padding 12 × 16 dp; icon 24 dp; gap 12 dp",
            {"warn": "warning-container / on-warning-container (new token)", "err": "error-container / on-error-container", "info": "keyboard key surface"}[kind], icon)
    actx = f'<span class="act">{esc(act)}</span>' if act else ""
    return f'<div class="s-kbanner {kind}"{a}>{ic(icon)}<div><b>{esc(title)}</b>{esc(text)}{actx}</div></div>'


def wave():
    hs = [30, 55, 85, 60, 40, 75, 100, 65, 35, 50, 80, 45, 25, 60, 90, 55, 30, 20, 45, 70, 50, 30]
    return '<div class="s-wave">' + "".join(f'<b style="height:{h}%"></b>' for h in hs) + "</div>"


def voicebar(state="listening"):
    va = ann("Voice bar", "Replaces the smartbar row while recording; height 48 dp", "keyboard background")
    if state == "denied":
        return (f'<div class="s-row48"{va}><div class="s-btn" style="color:var(--kb-on)">{ic("close")}</div>'
                f'<div class="s-vmsg">Microphone is off<b>Allow</b></div></div>')
    dele = f'<div class="s-btn{" dis" if state == "transcribing" else ""}" style="color:var(--kb-on)"{ann("Delete recording", "Touch target 48 dp; discards without transcribing", "keyboard on-background", "delete")}>{ic("delete")}</div>'
    if state == "transcribing":
        mid = f'<div class="s-prog"{ann("Progress", "Height 32 dp; radius 16 dp; 3 dp indeterminate bar", "keyboard key surface; bar keyboard primary")}>Transcribing and tidying up… · Hindi</div>'
        return f'<div class="s-row48"{va}>{dele}{mid}</div>'
    rec = f'<div class="s-rec"{ann("Recording dot and timer", "Dot 8 dp; timer 13 sp monospace")}><i></i>0:07</div>'
    lang = f'<span class="s-lang"{ann("Language chip", "Height 32 dp; radius 12 dp; Auto-detect by default", "border keyboard line", "arrow_drop_down")}>Auto{ic("arrow_drop_down", size=20)}</span>'
    done = f'<div class="s-btn ai"{ann("Done", "AI action button; inserts the text", "ai-gradient", "check")}><div class="c">{ic("check", size=20)}</div></div>'
    return f'<div class="s-row48"{va}>{dele}{rec}{wave()}{lang}{done}</div>'


# ---------- SmarType app screens ----------

def appbar(title, back=True, actions=""):
    b = f'<div class="s-btn">{ic("arrow_back")}</div>' if back else ""
    return f'<div class="s-abar{"" if back else " nb"}"{ann("Top app bar", "Height 64 dp; title-large 22/28 sp", "background; on-surface", "arrow_back" if back else None)}>{b}<span style="flex:1">{esc(title)}</span>{actions}</div>'


def lrow(title, sub=None, trail="", one=False, annotate=None):
    a = ann(*annotate) if annotate else ""
    s = f"<small>{esc(sub)}</small>" if sub else ""
    return f'<div class="s-lrow{" one" if one else ""}"{a}><div class="tx">{title}{s}</div><span class="tr">{trail}</span></div>'


def group(*rows, annotate=True):
    a = ann("List group", "Radius 16 dp; side margin 16 dp; 1 dp dividers between rows", "surface-container-low; divider outline-variant") if annotate else ""
    return f'<div class="s-group"{a}>' + "".join(rows) + "</div>"


def abtn(label, kind="fill", size="m", icon=None, full=False, annotate=None):
    a = ann(*annotate) if annotate else ""
    i = ic(icon, size=18) if icon else ""
    return f'<div class="s-ab {kind} {size}{" full" if full else ""}"{a}>{i}{esc(label)}</div>'


def banner(kind, title, text, act=None):
    icon = {"warn": "error", "info": "info", "err": "error"}[kind]
    a = ann({"warn": "Warning banner", "info": "Info banner", "err": "Error banner"}[kind], "Radius 14 dp; padding 12 × 16 dp; icon 24 dp",
            {"warn": "warning-container / on-warning-container (new token)", "info": "primary-container / on-primary-container", "err": "error-container / on-error-container"}[kind], icon)
    actx = f'<span class="act">{esc(act)}</span>' if act else ""
    return f'<div class="s-banner {kind}"{a}>{ic(icon)}<div><b>{esc(title)}</b>{esc(text)}{actx}</div></div>'


def snackbar(text, act=None):
    a = ann("Snackbar", "Min height 48 dp; radius 14 dp; 16 dp from the edges; 4 s, 10 s with an action", "inverse-surface; inverse-on-surface; action inverse-primary")
    return f'<div class="s-snackbar"{a}><span>{esc(text)}</span>{f"<b>{esc(act)}</b>" if act else ""}</div>'
