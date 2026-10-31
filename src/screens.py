"""Every new screen, built from components.py at real size. Keys are referenced from flows.py."""
from components import (abtn, appbar, banner, chat, chips, device, dock, esc, group, ic, ime, kbanner, keys, lrow,
                        panel, result, smartbar, snackbar, suggestions, voicebar, ann)

TYPED = "im running late for the meet sorry"


def _kb(active=None, panel_html=None, sugg=None, **kk):
    rows = [smartbar(active=active)]
    if panel_html:
        rows.append(panel_html)
    else:
        rows.append(sugg if sugg is not None else suggestions())
        rows.append(keys(**kk))
    return ime(*rows)


S = {}

# ---------- the bar above the keys ----------
S["kb-typing"] = device(chat(text="Running late for the meet") + _kb(sugg=suggestions(["meet", "meeting", "meetings"])), ime=True)
S["kb-empty"] = device(chat() + _kb(), ime=True)
S["kb-wide"] = device(chat(text="See you at 4") + ime(smartbar(emoji=True), suggestions(["4", "4pm", "4:00"]), keys(utility="language", space="English · हिन्दी")), width=412, ime=True)

# ---------- AI rewrite ----------
S["ai-open"] = device(chat(text=TYPED) + _kb(active="Rewrite", panel_html=panel(
    "Rewrite",
    chips([("Fix grammar", "sel"), "Polite", "Professional", "Shorter"]) + result("Fix grammar", "I'm running late for the meeting, sorry.", "Show changes"),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai")))), ime=True)
S["ai-loading"] = device(chat(text=TYPED) + _kb(active="Rewrite", panel_html=panel(
    "Rewrite", chips([("Fix grammar", "sel"), "Polite", "Professional", "Shorter"], annotate=False) + result("Writing your options…", "", skel=True),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai"), annotate=False))), ime=True)
S["ai-error"] = device(chat(text=TYPED) + _kb(active="Rewrite", panel_html=panel(
    "Rewrite", kbanner("err", "Couldn't rewrite this.", "Your text wasn't changed.", act="Try again"), badge="4 left")), ime=True)
S["ai-empty"] = device(chat() + _kb(active="Rewrite", panel_html=panel(
    "Rewrite", kbanner("info", "Type something first.", "Then tap ✦ to see it in different styles.", icon="info"))), ime=True)
S["ai-replaced"] = device(chat(text="I'm running late for the meeting, sorry.") + _kb(sugg=suggestions(snack=("Replaced with Fix grammar", "Undo"))), ime=True)

# ---------- translate ----------
S["tr-open"] = device(chat(text=TYPED) + _kb(active="Translate", panel_html=panel(
    "Translate", chips(["English", ("Hindi", "sel"), "Telugu", ("+ More", "more")]) + result("English → Hindi", "माफ़ करना, मुझे मीटिंग के लिए देर हो रही है।"),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai")))), ime=True)
_langs = "".join(
    f'<div class="s-item"{ann("Language row", "Radius 12 dp; tap translates; pin toggles a chip", "keyboard key surface", "keep") if i == 0 else ""}>'
    f'<div class="tx"><b>{n}</b><small>{s}</small></div>{ic("keep", fill=p, size=20)}</div>'
    for i, (n, s, p) in enumerate([("हिन्दी Hindi", "Pinned", True), ("తెలుగు Telugu", "Pinned", True), ("Español Spanish", "Recent", False)]))
S["tr-more"] = device(chat(text=TYPED) + _kb(active="Translate", panel_html=panel(
    "All languages", f'<div class="s-item" style="background:var(--kb-bg-var)">{ic("search", size=20)}<div class="tx" style="color:var(--kb-on-var)">Search languages</div></div><div class="s-list">{_langs}</div>')), ime=True)

# ---------- format ----------
S["fm-open"] = device(chat(title="Mail", msgs=(), text="need: train tickets, hotel for 2 nights, cab from airport, dinner booking sat") + _kb(active="Format", panel_html=panel(
    "Format", chips([("Bullets", "sel"), "Numbered", "Table", "Summarise"]) +
    result("Bullets", "• Train tickets<br>• Hotel for 2 nights<br>• Cab from the airport<br>• Dinner on Saturday").replace('class="x"', 'class="x" style="font-size:14px;line-height:20px"'),
    badge="4 left", dock=dock(("Copy", "q"), ("Replace", "ai")))), ime=True)
S["fm-short"] = device(chat(title="Mail", msgs=(), text="see you soon") + _kb(active="Format", panel_html=panel(
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
S["cb-open"] = device(chat() + _kb(active="Clipboard", panel_html=panel(
    "Clipboard", f'<div class="s-list">{_cl}</div>', action=f'<div class="s-btn" style="width:40px;flex-basis:40px">{ic("more_vert")}</div>')), ime=True)

# ---------- notes ----------
_notes = [("Leave request to Arjun", "Hi Arjun, I'd like to take Friday off… · 10 min ago"),
          ("Reply to landlord", "Thanks for fixing the tap. About the… · Yesterday"),
          ("Trip packing list", "Charger, passport, the blue jacket… · Mon")]
_nl = "".join(f'<div class="s-item"{ann("Note row", "Radius 12 dp; title 14 sp medium, preview 12 sp", "keyboard key surface") if i == 0 else ""}><div class="tx"><b>{esc(t)}</b><small>{esc(p)}</small></div></div>' for i, (t, p) in enumerate(_notes))
S["nt-list"] = device(chat(title="Mail", msgs=(), placeholder="Compose email") + _kb(active="Notes", panel_html=panel(
    "Notes", f'<div class="s-b out" style="flex:0 0 48px"{ann("New note", "Height 48 dp; radius 14 dp; 1.5 dp border", "keyboard primary", "add")}>{ic("add", size=20)}New note</div><div class="s-list">{_nl}</div>')), ime=True)
_edhead = (f'<div class="s-phead"{ann("Editor header", "Height 48 dp; status 12 sp", "keyboard background")}><div class="s-btn" style="color:var(--kb-on)">{ic("arrow_back")}</div>'
           f'<div class="t">Leave request to Arjun</div><span class="meta">Saved 11:31</span><div class="s-btn" style="width:40px;flex-basis:40px"{ann("More", "Copy, Share, Delete", None, "more_vert")}>{ic("more_vert")}</div></div>')
_edbar = (f'<div class="s-edbar"{ann("Note tools", "Height 48 dp; AI action buttons + Insert", "keyboard background")}>' +
          "".join(f'<div class="s-btn ai"><div class="c">{ic(n)}</div></div>' for n in ("spark", "translate", "format_list_bulleted", "mic")) +
          f'<div class="s-sp"></div><div class="s-ins"{ann("Insert", "Height 40 dp in a 48 dp row; radius 14 dp", "ai-gradient; on-ai-gradient")}>Insert</div></div>')
S["nt-editor"] = device(chat(title="Mail", msgs=(), placeholder="Compose email", caret=False, field_ann=False) +
                        f'<div class="s-editor"{ann("Note editor", "Opens over the keyboard; keys type into the note", "keyboard theme colours")}>{_edhead}'
                        f'<div class="s-edtext"{ann("Note text", "Radius 12 dp; padding 12 dp; body-large 16/24 sp", "keyboard key surface")}>Hi Arjun,<br>I\'d like to take Friday off for a family function. I\'ve handed the report to Meena<span class="s-caret"></span></div>'
                        f'{_edbar}{keys(annotate=False)}</div>', ime=True)

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
S["er-ai"] = device(chat(text="im running late") + _kb(active="Rewrite", panel_html=panel(
    "Rewrite", kbanner("warn", "AI can't run on this phone right now", "Google Play couldn't confirm the device. Your text wasn't sent. Typing, suggestions and voice still work.")))
    , ime=True)
S["er-signedin"] = device(appbar("SmarType", back=False) + '<div class="s-scroll">' +
                          '<div class="s-card"><h5>Free plan</h5><p>5 free AI tries.</p></div>' + snackbar("Signed in as priya…@gmail.com") + "</div>", app=True)
S["er-signin-fail"] = device('<div class="s-onb"><div class="s-skip">Not now</div>' +
                             banner("err", "Couldn't sign in", "Check your connection and try again. You can also skip and sign in later from Settings.").replace('class="s-banner err"', 'class="s-banner err" style="margin:24px 0 16px"') +
                             '<div style="margin-top:auto"></div>' + abtn("Try again", "fill", "l", annotate=("Main action", "Filled, large, 56 dp; full width; 16 dp gutters", "primary; on-primary")) +
                             abtn("Skip for now", "txt", "m") + '<div style="height:16px"></div></div>', app=True)

# ---------- setup (app) ----------
_art = '<img class="s-art" src="{root}assets/art/{name}.webp" alt=""' + ann("Illustration", "200 × 200 dp; WebP from assets/illustrations") + ">"
S["su-welcome"] = device('<div class="s-onb"><div class="s-skip"' + ann("Skip", "Text button, 48 dp tall", "primary") + '>Skip</div>' + _art.format(root="{root}", name="art_onb_suggestions") +
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
S["su-step1"] = device('<div class="s-onb"><div class="s-steps"' + ann("Progress", "3 bars, 4 dp tall, gap 4 dp", "primary; outline-variant") + '><i class="on"></i><i></i><i></i></div>'
                       '<h3>Turn on SmarType</h3><p class="l" style="margin-bottom:24px">Two quick steps in Android settings.</p>'
                       f'<div class="s-step"{ann("Active step card", "Radius 16 dp; padding 16 dp; action inside the card", "surface-container-low")}><div class="h">1 · Allow SmarType<span class="s-abadge neu"{ann("Status badge", "24 dp; radius 8 dp; not a switch", "tertiary-container")}>Not on yet</span></div>'
                       '<p>Android asks you to allow a new keyboard once.</p>' + abtn("Open settings", "fill", "m") + '</div>'
                       '<div class="s-step dim"><div class="h">2 · Choose SmarType<span class="s-abadge neu">Next</span></div><p>Pick it as the keyboard you type with.</p></div></div>', app=True)
S["su-step2"] = device('<div class="s-onb"><div class="s-steps"><i class="on"></i><i class="on"></i><i></i></div><h3>Turn on SmarType</h3><p class="l" style="margin-bottom:24px">Two quick steps in Android settings.</p>'
                       f'<div class="s-step dim"><div class="h">1 · Allow SmarType<span class="s-abadge ok"{ann("Done badge", "24 dp; radius 8 dp", "secondary-container; on-secondary-container")}>On ✓</span></div></div>'
                       '<div class="s-step"><div class="h">2 · Choose SmarType<span class="s-abadge neu">Not yet</span></div><p>Pick it as the keyboard you type with.</p>' + abtn("Choose keyboard", "fill", "m") + '</div></div>', app=True)
S["su-try"] = device('<div class="s-onb" style="padding-bottom:0"><div class="s-steps"><i class="on"></i><i class="on"></i><i class="on"></i></div><h3>Try it</h3>'
                     '<p class="l">Type anything, or fix this one:</p>'
                     f'<div class="s-tryf"{ann("Test field", "Min height 56 dp; radius 16 dp", "surface-container-high")}>{TYPED}<span class="s-caret"></span></div>'
                     + banner("info", "Tap ✦ above the keys to fix it", "").replace('class="s-banner info"', 'class="s-banner info" style="margin:0"') +
                     '<div style="margin-top:auto;align-self:flex-end;font:500 14px/20px var(--font-sans);color:var(--primary);padding:12px 0">Done</div></div>' +
                     ime(smartbar(annotate=False), suggestions(annotate=False), keys(annotate=False)), app=True, ime=True)
S["su-signin"] = device('<div class="s-onb"><div class="s-skip">Not now</div>' + _art.format(root="{root}", name="art_signin") +
                        '<h3>Try AI for free</h3><p class="l">Sign in to get free AI tries for rewrite, translate and format, and to keep Premium on all your phones.</p><div style="margin-top:auto"></div>'
                        f'<div class="s-gbtn"{ann("Google sign-in button", "56 dp; radius 14 dp; 1 dp border; Google G 20 dp (brand mark)", "outline; on-surface", "Google G (ic_google_g_icon)")}>{ic("google", size=20)}Continue with Google</div>'
                        '<div style="text-align:center;font:400 14px/20px var(--font-sans);color:var(--on-surface-variant);padding:12px 0 16px">Typing works without an account.</div></div>', app=True)
S["su-done"] = device('<div class="s-onb"><h3 style="margin-top:48px">You\'re all set</h3><p class="l">Signed in as priya…@gmail.com</p><div style="margin-top:auto"></div>' +
                      abtn("Go to SmarType", "fill", "l") + '<div style="height:16px"></div></div>', app=True)
