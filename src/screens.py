"""Every new screen, built from components.py at real size. Keys are referenced from flows.py."""
from components import (abtn, appbar, banner, chat, chips, device, dock, esc, group, ic, ime, kbanner, keys, lrow,
                        panel, result, smartbar, snackbar, suggestions, voicebar, ann)

TYPED = "im running late for the meet sorry"


def _kb(panel_html=None, sugg=None, **kk):
    """The keyboard: smartbar, suggestion row and keys; an open panel replaces all three."""
    if panel_html:
        return ime(panel_html)
    return ime(smartbar(), sugg if sugg is not None else suggestions(), keys(**kk))


S = {}

# ---------- the bar above the keys ----------
S["kb-typing"] = device(chat(text="Running late for the meet") + _kb(sugg=suggestions(["meet", "meeting", "meetings"])), ime=True)
S["kb-empty"] = device(chat() + _kb(), ime=True)
S["kb-wide"] = device(chat(text="See you at 4") + ime(smartbar(emoji=True), suggestions(["4", "4pm", "4:00"]), keys(utility="language", space="English · हिन्दी")), width=412, ime=True)

# ---------- AI rewrite ----------
S["ai-open"] = device(chat(text=TYPED) + _kb(panel_html=panel(
    "Rewrite",
    chips([("Fix grammar", "sel"), "Polite", "Professional", "Shorter"]) + result("Fix grammar", "I'm running late for the meeting, sorry.", "Show changes"),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai")))), ime=True)
S["ai-free"] = device(chat(text=TYPED) + _kb(panel_html=panel(
    "Rewrite", chips([("Fix grammar", "sel"), "Polite", "Professional", "Shorter"], annotate=False) +
    kbanner("info", "Pick a style, then tap Rewrite.", "Free plan: 4 tries left. One tap rewrites in all your styles."),
    badge="4 left", dock=dock(("Rewrite", "ai")))), ime=True)
S["ai-loading"] = device(chat(text=TYPED) + _kb(panel_html=panel(
    "Rewrite", chips([("Fix grammar", "sel"), "Polite", "Professional", "Shorter"], annotate=False) + result("Writing your options…", "", skel=True),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai"), annotate=False))), ime=True)
S["ai-error"] = device(chat(text=TYPED) + _kb(panel_html=panel(
    "Rewrite", kbanner("err", "Couldn't rewrite this.", "Your text wasn't changed.", act="Try again"), badge="4 left")), ime=True)
S["ai-empty"] = device(chat() + _kb(panel_html=panel(
    "Rewrite", kbanner("info", "Type something first.", "Then tap ✦ to see it in different styles.", icon="info"))), ime=True)
S["ai-replaced"] = device(chat(text="I'm running late for the meeting, sorry.") + _kb(sugg=suggestions(snack=("Replaced with Fix grammar", "Undo"))), ime=True)

# ---------- translate ----------
S["tr-open"] = device(chat(text=TYPED) + _kb(panel_html=panel(
    "Translate", chips(["English", ("Hindi", "sel"), "Telugu", ("+ More", "more")]) + result("English → Hindi", "माफ़ करना, मुझे मीटिंग के लिए देर हो रही है।"),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai")))), ime=True)
_langs = "".join(
    f'<div class="s-item"{ann("Language row", "Radius 12 dp; tap translates; pin toggles a chip", "keyboard key surface", "keep") if i == 0 else ""}>'
    f'<div class="tx"><b>{n}</b><small>{s}</small></div>{ic("keep", fill=p, size=20)}</div>'
    for i, (n, s, p) in enumerate([("हिन्दी Hindi", "Pinned", True), ("తెలుగు Telugu", "Pinned", True), ("Español Spanish", "Recent", False)]))
S["tr-more"] = device(chat(text=TYPED) + _kb(panel_html=panel(
    "All languages", f'<div class="s-item" style="background:var(--kb-bg-var)">{ic("search", size=20)}<div class="tx" style="color:var(--kb-on-var)">Search languages</div></div><div class="s-list">{_langs}</div>')), ime=True)

# ---------- format ----------
S["fm-open"] = device(chat(title="Mail", msgs=(), text="need: train tickets, hotel for 2 nights, cab from airport, dinner booking sat") + _kb(panel_html=panel(
    "Format", chips([("Bullets", "sel"), "Numbered", "Table", "Summarise"]) +
    result("Bullets", "• Train tickets<br>• Hotel for 2 nights<br>• Cab from the airport<br>• Dinner on Saturday").replace('class="x"', 'class="x" style="font-size:14px;line-height:20px"'),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai")))), ime=True)
S["fm-short"] = device(chat(title="Mail", msgs=(), text="see you soon") + _kb(panel_html=panel(
    "Format", chips(["Bullets", "Numbered", "Table", ("Summarise", "dis")], annotate=False) +
    kbanner("info", "Too short to summarise.", "Summarise needs at least 100 characters.", icon="info"), badge="4 left")), ime=True)

# ---------- voice ----------
S["vo-listen"] = device(chat() + ime(voicebar("listening"), suggestions(), keys(dim=True)), ime=True)
S["vo-pause"] = device(chat() + ime(voicebar("listening"), suggestions(hint="Still listening"), keys(dim=True, annotate=False)), ime=True)
S["vo-trans"] = device(chat() + ime(voicebar("transcribing"), suggestions(annotate=False), keys(dim=True, annotate=False)), ime=True)
S["vo-inserted"] = device(chat(text="मैं दस मिनट में पहुँच रहा हूँ") + _kb(sugg=suggestions(snack=("Inserted 6 words", "Undo"))), ime=True)
S["vo-denied"] = device(chat() + ime(voicebar("denied"), suggestions(annotate=False), keys(annotate=False)), ime=True)

# ---------- clipboard ----------
_clips = [("Office Wi-Fi: Lake-5G", "Pinned", True), ("https://maps.app/meet-point", "2 min ago", False),
          ("Order #48213 confirmed for Friday", "1 h ago", False), ("Thanks, see you there!", "Yesterday", False)]
_cl = "".join(f'<div class="s-item"{ann("Clip", "Radius 12 dp; padding 10 × 12 dp; tap pastes, long-press pins or deletes", "keyboard key surface", "keep (pinned)") if i == 0 else ""}><div class="tx"><b>{esc(t)}</b><small>{esc(m)}</small></div>{ic("keep", fill=True, size=20) if p else ""}</div>'
              for i, (t, m, p) in enumerate(_clips))
S["cb-open"] = device(chat() + _kb(panel_html=panel(
    "Clipboard", f'<div class="s-list">{_cl}</div>', action=f'<div class="s-btn" style="width:40px;flex-basis:40px">{ic("more_vert")}</div>')), ime=True)

# ---------- notes ----------
_notes = [("Leave request to Arjun", "Hi Arjun, I'd like to take Friday off… · 10 min ago"),
          ("Reply to landlord", "Thanks for fixing the tap. About the… · Yesterday"),
          ("Trip packing list", "Charger, passport, the blue jacket… · Mon")]
_nl = "".join(f'<div class="s-item"{ann("Note row", "Radius 12 dp; title 14 sp medium, preview 12 sp", "keyboard key surface") if i == 0 else ""}><div class="tx"><b>{esc(t)}</b><small>{esc(p)}</small></div></div>' for i, (t, p) in enumerate(_notes))
S["nt-list"] = device(chat(title="Mail", msgs=(), placeholder="Compose email") + _kb(panel_html=panel(
    "Notes", f'<div class="s-b out" style="flex:0 0 48px"{ann("New note", "Height 48 dp; radius 14 dp; 1.5 dp border", "keyboard primary", "add")}>{ic("add", size=20)}New note</div><div class="s-list">{_nl}</div>')), ime=True)
def _ovhead(title, status=None):
    st = f"<small>{esc(status)}</small>" if status else ""
    return (f'<div class="s-ovhead"{ann("Overlay header", "Height 56 dp; title title-medium 16 sp; status 12 sp", "surface-container-high; on-surface")}>'
            f'<div class="t">{esc(title)}{st}</div>'
            f'<div class="s-btn" style="color:var(--on-surface-variant)"{ann("More", "Copy, Share, Delete, All notes", None, "more_vert")}>{ic("more_vert")}</div>'
            f'<div class="s-btn" style="color:var(--on-surface-variant)"{ann("Close", "Saves and closes; back to the app", None, "close")}>{ic("close")}</div></div>')


def _aibox(text=None, focus=False, placeholder="Ask AI to change this note", can_send=False):
    q = esc(text) + '<span class="s-caret"></span>' if text else esc(placeholder)
    return (f'<div class="s-aibox{" focus" if focus else ""}"{ann("Ask AI box", "Height 44 dp; radius 22 dp; free-text instruction; send 36 dp", "surface-container-highest; focus ring primary", "spark, send")}>'
            f'<span class="spk">{ic("spark", size=20)}</span><span class="q">{q}</span>'
            f'<span class="s-send{"" if can_send else " dis"}">{ic("send", size=20)}</span></div>')


def _foot(words):
    return (f'<div class="s-ovtools"{ann("Note footer", "Height 56 dp; word count 12 sp; Insert on the right", "surface-container-high")}>'
            f'<span class="s-wc">{words} words</span><div class="s-sp"></div>'
            f'<div class="s-ins"{ann("Insert", "Height 40 dp; radius 14 dp; puts the note into the app at the cursor", "ai-gradient; on-ai-gradient")}>Insert</div></div>')


def _note(head, body, bottom):
    return device(
        '<div class="s-host" style="position:relative">'
        '<div class="s-hbar"><span class="s-av">R</span>Ravi</div><div class="s-msgs"></div><div class="s-field"><span class="ph">Message</span></div>'
        '<div class="s-ovscrim"></div>'
        f'<div class="s-overlay"{ann("Note overlay", "Floats over the app, above the keyboard; 8 dp margins; radius 24 dp", "surface-container-high; on-surface")}>{head}'
        f'<div class="s-ovbody">{body}</div>{bottom}</div></div>' + _kb(), ime=True)


_MSG0 = "hey ravi the tap is fixed thanks a lot. can u send the rent receipt"
_MSG1 = 'Hey Ravi, the tap\'s fixed, thanks a lot! <span class="s-hl">I\'ll pay the rent on Friday.</span> Can you send me the receipt?'


def _sugg(*labels):
    return (f'<div class="s-ochips one"{ann("AI suggestions", "Chips 32 dp, picked from what the note looks like (a list, a message…); one tap = one AI use", "outline-variant; on-surface-variant", "spark")}>' +
            "".join(f'<span class="s-achip">{ic("spark", size=16)}{esc(t)}</span>' for t in labels) + "</div>")


S["nt-new"] = _note(_ovhead("New note"),
                    f'<div class="s-ovtext sm"{ann("Note text", "Opens with the cursor here and the keyboard up: just start typing or tap the Mic", "on-surface")}><span class="s-caret"></span>'
                    '<span style="color:var(--on-surface-variant)">Write anything: a list, a message, something to keep</span></div>'
                    f'<div class="s-ochips"><span class="s-achip ctx"{ann("Paste chip", "Only when something is copied; one tap pastes it into the note", "primary-container; on-primary-container", "content_paste")}>{ic("content_paste", size=18)}Paste “Order #48213 confirmed for Friday…”</span></div>',
                    _aibox(placeholder="Ask AI to write something"))
S["nt-grocery"] = _note(_ovhead("Groceries", "Saved 18:02"),
                        '<div class="s-list-note">milk<br>eggs<br>onions<br>atta 5kg<br>tomatoes<br>dish soap<br>bread<span class="s-caret"></span></div>' +
                        _sugg("Group by aisle", "Add quantities", "Make it a checklist"),
                        _aibox() + _foot(9))
S["nt-ask"] = _note(_ovhead("Ravi", "Saved 11:30"),
                    f'<div class="s-ovtext sm">{esc(_MSG0)}</div>' + _sugg("Fix grammar", "More casual", "Shorter"),
                    _aibox("add that I'll pay the rent on Friday", focus=True, can_send=True))
S["nt-changed"] = _note(_ovhead("Ravi", "Saved 11:31"),
                        f'<div class="s-ovtext sm"{ann("Changed text", "AI edits the note in place; what changed is tinted for a few seconds", "primary at 22%")}>{_MSG1}</div>'
                        f'<div class="s-osnack"{ann("Undo message", "Inside the overlay; 6 s", "inverse-surface; action inverse-primary", "undo")}><span>Changed by AI</span><b>Undo</b></div>',
                        _aibox() + _foot(20))

# ---------- languages (app) ----------
_help = '<div class="s-help">The keyboard switches between these with the 🌐 key. The first one is the default.</div>'
_drag = ic("drag_indicator")
S["lg-fresh"] = device(appbar("Languages") + '<div class="s-scroll">' + _help + group(
    lrow("English (US)", "QWERTY · default", '<span class="s-abadge info">In use</span>', annotate=("Language row", "Min height 72 dp; title-medium 16 sp; summary body-medium 14 sp", "on-surface; on-surface-variant"))) +
    abtn("Add language", "fill", "m", icon="add", full=True, annotate=("Add language", "Filled, medium, 48 dp; radius 14 dp; full width", "primary; on-primary", "add")) + "</div>", app=True)
_sugg = "".join(lrow(n, s, ic("chevron_right"), annotate=("Suggested language", "Min height 72 dp", "surface-container-low", "chevron_right") if i == 0 else None)
                for i, (n, s) in enumerate([("हिन्दी Hindi", "Device language"), ("తెలుగు Telugu", "Common in India"), ("தமிழ் Tamil", "Common in India"), ("বাংলা Bengali", "Common in India")]))
S["lg-add"] = device(appbar("Add language") + '<div class="s-scroll">' +
                     f'<div class="s-search"{ann("Search field", "Height 56 dp; radius 28 dp", "surface-container-high; on-surface-variant", "search")}>{ic("search")}Search languages</div>'
                     + '<div class="s-sech">Suggested for you</div>' + group(_sugg, annotate=False) + '<div class="s-sech">All languages</div>' +
                     group(lrow("English", "15 regions", ic("chevron_right")), annotate=False) + "</div>", app=True)
S["lg-added"] = device(appbar("Languages") + '<div class="s-scroll">' + _help + group(
    lrow("English (US)", "QWERTY · default", _drag, annotate=("Language row", "Drag handle on the right; first row is the default", "on-surface-variant", "drag_indicator")),
    lrow("हिन्दी Hindi", "Devanagari keys", _drag)) + abtn("Add language", "fill", "m", icon="add", full=True) +
    snackbar("Hindi added. Tap 🌐 to switch.", "Undo") + "</div>", app=True)
S["lg-details"] = device(appbar("Languages") + '<div class="s-scroll">' + _help + group(lrow("English (US)", "QWERTY · default", _drag), lrow("हिन्दी Hindi", "Devanagari keys", _drag), annotate=False) +
                         '<div class="s-scrim"></div>' +
                         f'<div class="s-sheet"{ann("Bottom sheet", "Top radius 24 dp; drag handle 32 × 4 dp", "surface-container")}><div class="s-handle"></div><h4>हिन्दी Hindi</h4><div class="sub">Devanagari keys</div>'
                         f'<div class="s-srow"{ann("Sheet row", "Min height 56 dp; body-large 16 sp")}>{ic("check")}<span style="flex:1">Make default</span></div>'
                         f'<div class="s-srow danger"{ann("Remove", "Opens a confirmation dialog", "error", "delete")}>{ic("delete")}<span style="flex:1">Remove Hindi</span></div></div></div>', app=True)
S["lg-remove"] = device(appbar("Languages") + '<div class="s-scroll">' + _help + group(lrow("English (US)", "QWERTY · default", _drag), lrow("हिन्दी Hindi", "Devanagari keys", _drag), annotate=False) +
                        '<div class="s-scrim"></div>' +
                        f'<div class="s-dialog"{ann("Dialog", "Radius 24 dp; padding 24 dp; title headline-small 24 sp", "surface-container-high; actions primary, destructive error")}><h4>Remove Hindi (India)?</h4>'
                        '<p>You can add it again from Add language.</p><div class="acts"><span>Cancel</span><span class="danger">Remove</span></div></div></div>', app=True)
S["lg-globe"] = device(chat(text="See you tomorrow") + ime(smartbar(annotate=False), suggestions(["tomorrow", "tomorrow!", "today"], annotate=False), keys(utility="language", space="English · हिन्दी", annotate=False)) +
                       f'<div class="s-pop"{ann("Language list", "Long-press on 🌐 or space. Width 200 dp; rows 48 dp; radius 16 dp", "keyboard popup surface")}>'
                       '<div class="on">English (US) <span>✓</span></div><div>हिन्दी Hindi</div><div class="sep">Other keyboards…</div></div>', ime=True)
S["lg-hindi-v1"] = device(chat(text="kal milte") + ime(smartbar(annotate=False), suggestions(annotate=False), keys(utility="language", space="हिन्दी", deva=True, annotate=False)), ime=True)
S["lg-layout-later"] = device(appbar("Add language") + '<div class="s-scroll"><div class="s-scrim"></div>' +
                              '<div class="s-sheet"><div class="s-handle"></div><h4>Hindi · choose a layout</h4><div class="sub">You can change this later.</div>'
                              '<div class="s-srow"><span class="s-radio on"></span><div>Type in English letters<small>“namaste” → नमस्ते. QWERTY keys.</small></div></div>'
                              '<div class="s-srow"><span class="s-radio"></span><div>Devanagari keys<small>Hindi letters on the keys.</small></div></div>'
                              + abtn("Add Hindi", "fill", "m", full=True) + "</div></div>", app=True)
S["lg-hindi-later"] = device(chat(text="kal milte") + ime(smartbar(annotate=False), suggestions(["मिलते", "मिलते हैं", "milte"], annotate=False), keys(utility="language", space="हिन्दी", annotate=False)), ime=True)

# ---------- errors and Premium (app) ----------
S["er-home"] = device(appbar("SmarType", back=False) + '<div class="s-scroll">' +
                      f'<div class="s-card"{ann("Plan card", "Hero card: radius 16 dp; padding 16 dp", "surface-container")}><h5>Free plan</h5><p>3 of 5 free AI tries left.</p></div>' +
                      banner("warn", "Premium isn't available on this phone right now", "Google Play couldn't confirm this device. Typing, themes and your settings still work.", act="Learn more") + "</div>", app=True)
S["er-premium"] = device(appbar("Premium") + '<div class="s-scroll">' +
                         banner("warn", "Plans can't load on this phone", "Google Play couldn't confirm this device, so purchases are turned off. Trying again won't fix this.", act="What can I do?") +
                         '<div class="s-card"><h5>Monthly · ₹120</h5><p>Unavailable on this phone</p></div><div class="s-card"><h5>Yearly · ₹999</h5><p>Unavailable on this phone</p></div></div>', app=True)
S["er-ai"] = device(chat(text="im running late") + _kb(panel_html=panel(
    "Rewrite", kbanner("warn", "AI can't run on this phone right now", "Google Play couldn't confirm the device. Your text wasn't sent. Typing, suggestions and voice still work.")))
    , ime=True)
S["er-signedin"] = device(appbar("SmarType", back=False) + '<div class="s-scroll">' +
                          '<div class="s-card"><h5>Free plan</h5><p>5 free AI tries.</p></div>' + snackbar("Signed in as priya…@gmail.com") + "</div>", app=True)
S["er-signin-fail"] = device('<div class="s-onb"><div class="s-skip">Not now</div>' +
                             banner("err", "Couldn't sign in", "Check your connection and try again. You can also skip and sign in later from Settings.").replace('class="s-banner err"', 'class="s-banner err" style="margin:24px 0 16px"') +
                             '<div style="margin-top:auto"></div>' + abtn("Try again", "fill", "l", annotate=("Main action", "Filled, large, 56 dp; full width; 16 dp gutters", "primary; on-primary")) +
                             abtn("Skip for now", "txt", "m") + '<div style="height:16px"></div></div>', app=True)

# ---------- setup (app) ----------
def _art_svg(name, dp=200):
    from illustration_set import SET
    fn = {n: f for n, t, w, d, f, k in SET}[name]
    return (f'<div class="s-art"' + ann("Illustration", f"{dp} × {dp} dp; animated, with a still frame for reduced motion (assets/illustrations)", None, None) + f'>{fn(dp)}</div>')
S["su-welcome"] = device('<div class="s-onb"><div class="s-skip"' + ann("Skip", "Text button, 48 dp tall", "primary") + '>Skip</div>' + _art_svg("art_welcome") +
                         '<h3' + ann("Headline", "headline-medium 28/36 sp") + '>Type, fix and translate in one keyboard</h3><p class="l">Smart suggestions, a clean keyboard, and AI that fixes your message in one tap.</p>'
                         '<div class="s-dots"' + ann("Page dots", "8 dp dots; current 24 dp wide", "primary; outline-variant") + '><i class="on"></i><i></i></div>' +
                         abtn("Next", "fill", "l", annotate=("Main action", "Filled, large, 56 dp; full width", "primary; on-primary")) + '<div style="height:16px"></div></div>', app=True)
_pv = "".join(f'<div class="s-pv"{ann("Privacy line", "Icon tile 40 dp, radius 12 dp; title 16 sp; text 14 sp", "primary-container; on-primary-container", i) if k == 0 else ""}><span class="ico">{ic(i)}</span><div><b>{t}</b><span>{s}</span></div></div>'
              for k, (i, t, s) in enumerate([("keyboard", "Typing stays on your phone", "Suggestions are learned on the device."),
                                             ("spark", "AI only sees what you send", "Only when you tap Rewrite, Translate or Format."),
                                             ("lock", "Password fields stay private", "No AI, no voice and nothing learned in password fields.")]))
S["su-privacy"] = device('<div class="s-onb"><div class="s-skip">Skip</div><h3 style="margin-top:16px">Private by default</h3>' + _pv +
                         '<div style="font:500 14px/20px var(--font-sans);color:var(--primary);padding:12px 0">Read the privacy policy</div>'
                         '<div class="s-dots"><i></i><i class="on"></i></div>' + abtn("Set up keyboard", "fill", "l") + '<div style="height:16px"></div></div>', app=True)

_LOGO = '<img src="{root}assets/art/logo.png" alt="" width="20" height="20" style="border-radius:5px;display:block">'
def _sys1(other="Gboard"):
    """Android's on-screen keyboard list. `other` is the phone's current keyboard (see the setup flow: device-aware name)."""
    return (f'<div class="s-sys" aria-hidden="true"{ann("Picture of Android settings", "Decorative and animated, not a control; tapping it does the same as Open settings. Rows 40 dp; radius 12 dp; 1 dp outline; the first row names the keyboard this phone uses now", "sys-picture (light: surface-container-lowest, dark: surface-container-high); outline-variant; switch primary")}>'
            f'<div class="bar">{ic("arrow_back", size=20)}On-screen keyboard</div>'
            f'<div class="row">{ic("keyboard", size=20)}<span class="n">{other}</span><span class="s-tog on"></span></div>'
            f'<div class="row hi" style="position:relative">{_LOGO}<span class="n">SmarType</span><span class="s-tog anim"></span>'
            '<span class="s-tap" style="right:20px;top:6px"></span></div></div>')


def _sys2(other="Gboard"):
    """Android's keyboard picker, with the phone's current keyboard first."""
    return (f'<div class="s-sys" aria-hidden="true"{ann("Picture of the keyboard picker", "Decorative and animated, not a control; tapping it does the same as Choose keyboard. Same surface as the settings picture", "sys-picture; outline-variant; radio primary")}>'
            '<div class="bar">Choose input method</div>'
            f'<div class="row"><span class="s-rad out"></span><span class="n">{other}</span></div>'
            f'<div class="row hi" style="position:relative"><span class="s-rad anim"></span><span class="n">SmarType</span>'
            '<span class="s-tap" style="left:11px;top:6px"></span></div></div>')


def _step1(other="Gboard"):
    return device('<div class="s-onb"><div class="s-steps"' + ann("Progress", "3 bars, 4 dp tall, gap 4 dp", "primary; outline-variant") + '><i class="on"></i><i></i><i></i></div>'
                  '<h3>Turn on SmarType</h3><p class="l" style="margin-bottom:24px">Two quick steps in Android settings.</p>'
                  f'<div class="s-step"{ann("Active step card", "Radius 16 dp; padding 16 dp; action inside the card", "surface-container-low")}><div class="h">1 · Allow SmarType<span class="s-abadge neu"{ann("Status badge", "24 dp; radius 8 dp; not a switch", "tertiary-container")}>Not on yet</span></div>'
                  '<p>Android asks you to allow a new keyboard once.</p>' + _sys1(other) + abtn("Open settings", "fill", "m") + '</div>'
                  '<div class="s-step dim"><div class="h">2 · Choose SmarType<span class="s-abadge neu">Next</span></div><p>Pick it as the keyboard you type with.</p></div></div>', app=True)


S["su-step1"] = _step1("Gboard")
S["su-step1-samsung"] = _step1("Samsung Keyboard")
S["su-step2"] = device('<div class="s-onb"><div class="s-steps"><i class="on"></i><i class="on"></i><i></i></div><h3>Turn on SmarType</h3><p class="l" style="margin-bottom:24px">Two quick steps in Android settings.</p>'
                       f'<div class="s-step dim"><div class="h">1 · Allow SmarType<span class="s-abadge ok"{ann("Done badge", "24 dp; radius 8 dp", "secondary-container; on-secondary-container")}>On ✓</span></div></div>'
                       '<div class="s-step"><div class="h">2 · Choose SmarType<span class="s-abadge neu">Not yet</span></div><p>Pick it as the keyboard you type with.</p>' + _sys2() + abtn("Choose keyboard", "fill", "m") + '</div></div>', app=True)
S["su-try"] = device('<div class="s-onb" style="padding-bottom:0"><div class="s-steps"><i class="on"></i><i class="on"></i><i class="on"></i></div><h3>Try it</h3>'
                     '<p class="l">Type anything, or fix this one:</p>'
                     f'<div class="s-tryf"{ann("Test field", "Min height 56 dp; radius 16 dp", "surface-container-high")}>{TYPED}<span class="s-caret"></span></div>'
                     + banner("info", "Tap ✦ above the keys to fix it", "").replace('class="s-banner info"', 'class="s-banner info" style="margin:0"') +
                     '<div style="margin-top:auto;align-self:flex-end;font:500 14px/20px var(--font-sans);color:var(--primary);padding:12px 0">Done</div></div>' +
                     ime(smartbar(annotate=False), suggestions(annotate=False), keys(annotate=False)), app=True, ime=True)
S["su-signin"] = device('<div class="s-onb"><div class="s-skip">Not now</div>' + _art_svg("art_signin") +
                        '<h3>Try AI for free</h3><p class="l">Sign in to get free AI tries for rewrite, translate and format, and to keep Premium on all your phones.</p><div style="margin-top:auto"></div>'
                        f'<div class="s-gbtn"{ann("Google sign-in button", "56 dp; radius 14 dp; 1 dp border; Google G 20 dp (brand mark)", "outline; on-surface", "Google G (ic_google_g_icon)")}>{ic("google", size=20)}Continue with Google</div>'
                        '<div style="text-align:center;font:400 14px/20px var(--font-sans);color:var(--on-surface-variant);padding:12px 0 16px">Typing works without an account.</div></div>', app=True)
S["su-done"] = device('<div class="s-onb">' + _art_svg("art_done") + '<h3>You\'re all set</h3><p class="l">Signed in as priya…@gmail.com</p><div style="margin-top:auto"></div>' +
                      abtn("Go to SmarType", "fill", "l") + '<div style="height:16px"></div></div>', app=True)

# ---------- settings, Home and Writing styles (app) ----------
S["st-settings"] = device(appbar("Settings") + '<div class="s-scroll">' +
    f'<div class="s-search"{ann("Settings search", "Height 56 dp; radius 28 dp", "surface-container-high", "search")}>{ic("search")}Search settings</div>' +
    '<div class="s-sech">Typing and input</div>' + group(
        lrow("Keyboard", "Height, number row, key sounds", ic("chevron_right"), annotate=("Row with summary", "Min height 72 dp; every row in a group has a summary", "on-surface; on-surface-variant", "chevron_right")),
        lrow("Smartbar", "Buttons and suggestions", ic("chevron_right")),
        lrow("Typing", "Autocorrect, suggestions, capitalisation", ic("chevron_right")),
        lrow("Gestures", "Swipe typing, cursor control", ic("chevron_right"))) +
    '<div style="height:12px"></div>' + banner("info", "Tip", "The smartbar now keeps the same buttons. Change what's in ⋯ in Smartbar.", act="Got it").replace('class="s-banner info"', 'class="s-banner info"' + ann("Inline tip", "Banner under the group it describes; never floats over rows", "primary-container")) +
    '<div class="s-sech">Look and feel</div>' + group(lrow("Themes", "Keyboard colours and key shapes", ic("chevron_right")), lrow("App look", "Light, dark, AMOLED", ic("chevron_right")), annotate=False) + "</div>", app=True)
_pin = lambda n, s: lrow(n, s, ic("drag_indicator"))
S["st-styles"] = device(appbar("Writing styles") + '<div class="s-scroll">' +
    '<div class="s-help">On your keyboard: up to 4, in this order. Drag to reorder.</div>' +
    '<div class="s-sech">On your keyboard · 4 of 4</div>' + group(
        lrow("Polite", "Pinned", ic("drag_indicator"), annotate=("Pinned style", "Drag handle; the first pinned style shows first", "on-surface-variant", "drag_indicator")),
        _pin("Professional", "Pinned"), _pin("Casual", "Pinned"), _pin("Shorter", "Pinned")) +
    '<div class="s-sech">Everyday</div>' + group(
        lrow("Social", None, ic("keep"), one=True, annotate=("Unpinned style", "Tap the pin to put it on the keyboard", "on-surface-variant", "keep")),
        lrow("Emojify", None, ic("keep"), one=True), lrow("Neutral", None, ic("keep"), one=True), annotate=False) +
    '<div class="s-sech">Your styles</div>' + abtn("Add style", "ton", "m", icon="add", full=True, annotate=("Add style", "Tonal, medium, 48 dp", "primary-container; on-primary-container", "add")).replace("margin: 16px 16px 0", "") + "</div>", app=True)
S["st-home"] = device(appbar("SmarType", back=False) + '<div class="s-scroll">' +
    f'<div class="s-card"{ann("Plan card", "Hero card: plan, renewal date and one action", "surface-container")}><h5>Premium</h5><p>Renews 12 Nov · ₹999 a year</p>'
    '<div style="font:500 14px/20px var(--font-sans);color:var(--primary);margin-top:12px">Manage in Google Play</div></div>' +
    f'<div class="s-tryf" style="margin:0 16px 12px"{ann("Try field", "Min height 56 dp; radius 16 dp; opens the keyboard", "surface-container-high")}><span style="color:var(--on-surface-variant)">Try your keyboard</span></div>' +
    group(lrow("Themes", "SmarType Night", ic("chevron_right")), lrow("Writing styles", "4 on your keyboard", ic("chevron_right")),
          lrow("Languages", "English, हिन्दी", ic("chevron_right")), lrow("Settings", None, ic("chevron_right"), one=True)) +
    '<div class="s-sech">Help</div>' + group(lrow("Guides", None, ic("chevron_right"), one=True), lrow("Contact support", None, ic("chevron_right"), one=True),
          lrow("Share SmarType", None, ic("chevron_right"), one=True), annotate=False) + "</div>", app=True)

# ---------- More panel (⋯), long-press names ----------
def _tile(icon, label, on=False, a=""):
    return f'<div class="s-tile{" on" if on else ""}"{a}><div class="c">{ic(icon, fill=on, size=20)}</div><span>{esc(label)}</span></div>'


_more = ('<div class="s-more">'
         f'<div class="g"{ann("Group label", "label-small 12/16 sp; 8 dp above, 4 dp below; read by TalkBack as a heading", "keyboard on-surface-variant")}>Editing</div><div class="s-tiles">' +
         _tile("undo", "Undo", a=ann("Action tile", "84 × 68 dp cell (4 columns at 360 dp); pill 56 × 36 dp, radius 18 dp; icon 20 dp; label 12/16 sp, one line", "pill keyboard key surface; icon on-surface-variant; label on-background", "undo")) +
         _tile("redo", "Redo") + _tile("select_all", "Select all") + _tile("arrow_range", "Move cursor") +
         _tile("content_copy", "Copy") + _tile("content_cut", "Cut") + _tile("content_paste", "Paste") + '</div>'
         '<div class="g">Keyboard</div><div class="s-tiles">' +
         _tile("spellcheck", "Autocorrect", on=True, a=ann("Toggle tile, on", "Same size; filled pill and filled icon when on; TalkBack says \"Autocorrect, switch, on\"", "pill keyboard primary; icon on-primary", "spellcheck")) +
         _tile("front_hand", "One-handed") + _tile("domino_mask", "Incognito") + _tile("language", "Language") + '</div>'
         '<div class="g">Go to</div><div class="s-tiles">' + _tile("mood", "Emoji") + _tile("settings", "Settings") + '</div></div>')
_edit_btn = f'<div class="s-ptext"{ann("Edit (was the floating Reorder button)", "Text button in the header; 48 dp tall; label-large 14 sp", "keyboard primary")}>Edit</div>'
S["kb-more"] = device(chat() + _kb(panel_html=panel("More", _more, action=_edit_btn)), ime=True)


def _erow(icon, label, a=""):
    return f'<div class="s-erow"{a}>{ic("drag_indicator")}{ic(icon, size=20)}<span class="n">{esc(label)}</span></div>'


_edit = ('<div class="s-more">'
         f'<div class="s-ehint">Drag to change the order. The smartbar\'s own buttons stay where they are.</div>'
         '<div class="g">Editing</div>' +
         _erow("undo", "Undo", ann("Reorder row", "48 dp; drag handle 24 dp; icon 20 dp; long-press anywhere on the row to drag; TalkBack actions Move up and Move down", "keyboard on-background; handle on-surface-variant", "drag_indicator")) +
         _erow("redo", "Redo") + _erow("select_all", "Select all") + _erow("arrow_range", "Move cursor") + _erow("content_copy", "Copy") + '</div>')
S["kb-more-edit"] = device(chat() + _kb(panel_html=panel("Edit More", _edit, action='<div class="s-ptext">Done</div>')), ime=True)

_sb_tip = smartbar().replace('title="Format">', 'title="Format"><span class="s-tip"' +
                             ann("Name on long-press", "32 dp tall; radius 8 dp; 12 dp side padding; 2 dp above the bar; shows while held, 1.5 s after release", "keyboard on-background fill; keyboard background text") + '>Format</span>', 1)
S["kb-tip"] = device(chat(text="Running late for the meet") + ime(_sb_tip, suggestions(["meet", "meeting", "meetings"], annotate=False), keys(annotate=False)), ime=True)

# ---------- autocorrect ----------
_ac_row = ('<div class="s-row48 s-sugg"' + ann("Suggestion row after an autocorrect", "Same 48 dp row; the original word comes first with an undo arrow; tap it to put it back", "original word keyboard on-surface-variant, dotted underline") +
           f'><span class="orig">{ic("undo", size=16)}<s>teh</s></span><span class="b">the</span><span>then</span></div>')
S["ac-done"] = device(chat(text="See you at the ") + ime(smartbar(annotate=False), _ac_row, keys(annotate=False)), ime=True)


# ---------- TalkBack focus order ----------
def _focus(html, items):
    """Adds numbered TalkBack focus markers (drawn by spec.js) to a screen. items: [(css selector, label)]."""
    import json
    data = json.dumps([[s, l] for s, l in items]).replace("'", "&#39;")
    return html.replace('<div class="s-dev', f'<div data-focus=\'{data}\' class="s-dev', 1)


_bar = ".s-ime > .s-row48:first-child > .s-btn"
S["tb-keyboard"] = _focus(S["kb-typing"], [
    (f"{_bar}:nth-child(1)", "1"), (f"{_bar}:nth-child(2)", "2"), (f"{_bar}:nth-child(3)", "3"), (f"{_bar}:nth-child(4)", "4"),
    (f"{_bar}:nth-child(5)", "5"), (f"{_bar}:nth-child(6)", "6"), (f"{_bar}:nth-child(8)", "7"),
    (".s-sugg span:nth-child(1)", "8"), (".s-sugg span:nth-child(2)", "9"), (".s-sugg span:nth-child(3)", "10"),
    (".s-keys", "Keys: touch to explore, lift to type"),
])
S["tb-panel"] = _focus(S["ai-open"], [
    (".s-phead .s-btn", "1"), (".s-phead .t", "2"), (".s-phead .s-badge", "3"),
    (".s-chips .s-chip:nth-child(1)", "4"), (".s-chips .s-chip:nth-child(2)", "5"), (".s-chips .s-chip:nth-child(3)", "6"), (".s-chips .s-chip:nth-child(4)", "7"),
    (".s-res", "8"), (".s-res .m span:nth-child(2)", "9"), (".s-dock .s-b:nth-child(1)", "10"), (".s-dock .s-b:nth-child(2)", "11"),
])
S["tb-more"] = _focus(S["kb-more"], [
    (".s-phead .s-btn", "1"), (".s-phead .t", "2"), (".s-phead .s-ptext", "3"), (".s-more > .g", "4"),
    (".s-more .s-tile:nth-child(1)", "5"), (".s-more .s-tile:nth-child(2)", "6"), (".s-more .s-tile:nth-child(3)", "7"), (".s-more .s-tile:nth-child(4)", "8"),
])
