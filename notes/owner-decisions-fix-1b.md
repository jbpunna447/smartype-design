# Fix 1b: owner notes (1 Nov 2026)

Decisions from the owner for Fix 1b. Designed in site/fix-1b.html; later decisions are recorded on that page and in site/audit.html.

## 1. Smartbar and suggestion bar
- Two separate bars. The smartbar sits on top. The suggestion bar is its own row below it. The smartbar never turns into suggestions.
- Smartbar, left to right: AI ✦, Translate, Clipboard, Notes, Emoji (if it fits), ⋯ menu, and the Mic pinned far right.
- AI, Translate, and Mic get today's AI-button treatment. Clipboard, Notes, and Emoji are plain icons.
- ⋯ opens the settings menu (themes, autocorrect, and so on; this is the existing More panel).
- Proposed, not yet confirmed: Emoji comes before ⋯, so ⋯ stays fixed next to the Mic. Emoji is the first to drop into ⋯ on narrow widths, then Notes. The suggestion bar collapses when it has nothing to show.

## 2. Voice listening mode (replaces the system voice window, D1)
- Tapping the Mic turns the smartbar into: 🗑 Delete · ● timer · live waveform · language (Auto-detect by default) · ➤ Send.
- Delete discards the recording before transcription.
- Send: the bar shows "Transcribing…", then pastes the text at the cursor.
- The default language is set in Settings, as Auto-detect.
- Open for the devs: transcribe on the device (SpeechRecognizer) or in the cloud (Functions plus quota, a risky area, needs the owner's plan review).

## 3. AI panel: AI | Translate as tabs
- Remove the shown input text (the quote box / word-count line).
- Tapping ✦ runs Fix grammar first. That is the first, selected chip.
- Other chips follow: Polite, Professional, the other defaults, and the user's custom prompts.
- The "N left" badge stays at the top.
- AI and Translate are a tab switch in the same panel. Whichever one you enter from, you can switch to the other.
- Translate uses chips like AI does, not a dropdown. English is the first chip, followed by the user's pinned favourite languages (Hindi, …), plus a "More languages" option. Fallback if chips get too complex: a dropdown.
- Same layout, chip row, result area, and keyboard-return button position in both tabs (fixes B5).

## 4. Clipboard and Notes split apart
- Today one pad icon opens a panel with two tabs, Clipboard and Quick Notes. Split them into two smartbar buttons.
- Clipboard: the standard clipboard panel, reached directly from the smartbar. Clipboard history is on by default for everyone (#517 may already do this; verify on the latest build).
- Every panel (AI, Translate, Clipboard, Notes) has the same "back to keyboard" button in the same place.

## 5. Notes as a drafting playground (like Gmail's "Help me write")
- Tapping Notes opens a list: "+ New draft" at the top, then the saved notes (most recent first, with a one-line preview and the time).
- Opening or creating a note brings up an editor over the keyboard that behaves like a text field. You can type into it with the keyboard or dictate with the Mic (the same listening mode as section 2).
- The editor has an ✦ AI button that runs the same chips (Fix grammar, Polite, Professional, custom prompts) and Translate on the note, with Replace and Undo.
- The note saves automatically, so you can come back and keep adding to a draft over time.
- One tap on "Insert" puts the note into the app's text field. The note stays saved.
- Improve on the current Quick Notes, don't rebuild from scratch.
