"""Steps and taps for the main tasks in each flow: (task, today, new, typing or speaking).
Counts are taps on the screen; typing and speaking are listed separately."""

TAPS = {
    "setup": [
        ("From install to a working keyboard", "4 × Next, privacy Next, sign-in choice, Open settings, switch, OK, back, Select, pick: 13 taps",
         "Next, Set up keyboard, Open settings, switch, OK, back, Choose keyboard, pick: 8 taps", "None"),
        ("Sign in", "Before setup, forced to decide", "Later, when it's worth it: Continue with Google, pick account: 2 taps", "None"),
        ("First try", "Not part of setup", "The keyboard is already up on Try it: tap ✦ to see AI work: 1 tap", "Typing"),
    ],
    "keyboard-bar": [
        ("Paste something you copied", "Pad icon → Clipboard (chooser) → the clip: 3 taps", "Clipboard → the clip: 2 taps", "None"),
        ("Pick a suggestion", "Suggestions sometimes replace the buttons", "The suggestion row is always in the same place: 1 tap", "Typing"),
        ("Reach a setting", "⋯ grid with unlabelled icons", "⋯ → a labelled item: 2 taps", "None"),
        ("Turn autocorrect off", "⋯ → guess which icon: 2 taps", "⋯ → Autocorrect (named, shows on): 2 taps", "None"),
        ("Reorder More", "⋯ → Reorder (covering a row) → drag", "⋯ → Edit → drag → Done", "None"),
        ("Find out what an icon does", "Not possible", "Long-press it: 1 press", "None"),
    ],
    "autocorrect": [
        ("Fix a typo", "Tap the suggestion: 1 tap, if noticed", "Nothing: it's corrected on space", "Typing"),
        ("Undo a wrong correction", "Backspace, if the user knows it", "Tap the put-back word: 1 tap (or Backspace)", "None"),
    ],
    "ai-rewrite": [
        ("Fix a message and send it (Premium)", "✦, pick a style, Rewrite, Replace: 4 taps", "✦, Replace: 2 taps", "Typing the message"),
        ("Fix a message (free)", "✦, pick a style, Rewrite, Replace: 4 taps", "✦, Rewrite, Replace: 3 taps", "Typing the message"),
        ("Try another style", "Chips disappear after a result: close, ✦, style, Rewrite: 4 taps", "Tap another chip: 1 tap, no new request", "None"),
        ("Undo a Replace", "Not possible", "Undo in the suggestion row: 1 tap", "None"),
    ],
    "translate": [
        ("Translate into your usual language and replace", "Translate, Replace: 2 taps (chips may be hidden)", "Translate, Replace: 2 taps", "None"),
        ("Translate into another language", "Translate, open the list, pick, Replace: 4 taps", "Translate, the language chip, Replace: 3 taps", "None"),
        ("Go from Rewrite to Translate", "Close, open the other panel: 2+ taps", "‹, Translate: 2 taps; results already fetched show at once", "None"),
    ],
    "format": [
        ("Turn text into bullets", "✦, Bullet points chip, Replace: 3 taps", "Format, Replace: 2 taps (Bullets is first, or the last used)", "None"),
        ("Make a table", "✦, Table chip, Replace: 3 taps", "Format, Table, Replace: 3 taps", "None"),
    ],
    "voice": [
        ("Dictate a message", "Mic, speak, wait, switch back to SmarType, fix punctuation by hand: 3+ taps and lots of editing",
         "Mic, speak, ✓: 2 taps; tidied up, ready to send", "Speaking"),
        ("Take a pause while speaking", "It stops after ~3 s; start again: +1 tap", "Keeps listening: 0 taps", "Speaking"),
        ("Throw a recording away", "—", "Delete: 1 tap", "None"),
    ],
    "clipboard": [
        ("Paste a recent clip", "Pad icon → Clipboard → the clip: 3 taps", "Clipboard → the clip: 2 taps", "None"),
        ("Pin a clip", "Long-press → Pin: 2 taps", "Long-press → Pin: 2 taps", "None"),
    ],
    "languages": [
        ("Add Hindi and switch to it", "Settings → Languages → Add → type \"hindi\" → pick: 4 taps + typing, and English is gone",
         "Languages → Add language → Hindi (suggested): 3 taps, no typing; then 🌐: 1 tap", "None"),
        ("Make a language the default", "Not possible", "Tap the row → Make default: 2 taps, or drag it to the top", "None"),
    ],
    "errors": [
        ("Find out why Premium isn't available", "Upgrade → error page → Retry (fails again): 3+ taps, no answer", "Read the banner on Home: 0 taps", "None"),
        ("After signing in", "Dismiss a wrong \"Sign in\" toast", "Nothing to do: a confirmation shows and goes", "None"),
    ],
    "talkback": [
        ("Type a word", "Likely not possible", "Per letter: slide to the key, lift", "Typing by touch"),
        ("Rewrite a message", "Not checked", "Find Rewrite, double-tap; find Replace, double-tap", "None"),
        ("Hear what changed", "Nothing", "Spoken automatically", "None"),
    ],
    "settings": [
        ("Change the keyboard's height", "Settings → guess between Keyboard and Typing (no summaries) → …", "Settings → Keyboard (its summary says Height): 2 taps; or search \"height\": 1 tap + typing", "Typing, only for search"),
        ("Put a style on the keyboard", "Find the style among 23 chips → pin → understand the 4 limit", "Writing styles → the style's pin: 2 taps", "None"),
        ("Manage the subscription", "Not on Home", "Home → Manage in Google Play: 1 tap", "None"),
    ],
}
