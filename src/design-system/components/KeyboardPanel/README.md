# KeyboardPanel

The frame every app-owned panel inside the keyboard uses (Rewrite, Translate, Format, Clipboard, Notes), so they open, read and close the same way. The real-size screens in the flow pages are the reference; open their Spec tables for exact sizes.

## Layout

- **The panel replaces the smartbar, the suggestion row and the keys:** 48 + 48 + 220 = 316 dp on a 360 × 800 dp phone. The keys area is 4 × the keyboard row base height (`FlorisImeSizing`). The keyboard's height doesn't change.
- **Header, 48 dp, in the smartbar's place:** `arrow_back` (48 dp touch target, 24 dp icon), the panel name in `title-medium` (16/24 sp), an optional uses-left badge (24 dp, radius 8 dp, `label-small`) and at most one icon action (`more_vert`). A 1 dp divider below.
- **Selection hint** (Rewrite, Translate, Format, only when part of the text is selected): "Selected text only" in `label-small`. No quote box.
- **Body:** 12 dp padding, 12 dp gap. Chips (32 dp, radius 12 dp, gap 8 dp, scroll horizontally), then the result card (radius 12 dp, padding 12 dp, text `body-large`), or a list.
- **Dock, 68 dp:** 8 dp top, 48 dp buttons, 12 dp bottom, 8 dp gap. Content actions only (Copy and Replace, or Insert). Navigation never sits here. An unavailable state has no dock.

## Behaviour

- Rewrite, Translate and Format run as soon as they open. Results stay in memory for that text until it changes or the keyboard closes, so switching chips or reopening a panel costs no new request. An empty field sends nothing.
- `arrow_back` in the header and system Back both bring back the keyboard with the smartbar. To go from Rewrite to Translate: ‹, then Translate. Back never hides the whole keyboard from a panel.
- The panel keeps its height when content changes (loading, result, error), so the keys and the app don't jump.
- Loading: a skeleton in the result card. Error or unavailable: one banner saying what happened and what still works; no action that can't work.
- After Replace or Insert, the panel closes and the suggestion row shows "Replaced · Undo" or "Inserted · Undo" for 6 seconds.

## Colours and shape

- Colours come from the active keyboard theme through `KeyboardPanelColors` (background, surface, surfaceRaised, border, secondaryText, accent, accentStart/End, onAccent, error). SmarType Night and Day values are in `floris_night.json` and `floris_day.json`.
- AI actions use the AI gradient (`ai-gradient-start` → `ai-gradient-end`, text `on-ai-gradient`).
- Corners: chips and cards `radius-sm` (12 dp), dock buttons `radius-md` (14 dp). No 999 dp pills.
- Inline elements only: no popups, dialogs or dropdown windows from the keyboard.
- Icons: Material Symbols Rounded, 24 dp. The spark is the only custom icon.

## Replaces

`KeyboardPanelHeader` (the ↵ back icon), `KeyboardPanelActionRow`, the `KeyboardPanelButton` gradient default, the AI panel's quote box, and Translate's bottom-left back button.

## What the consumer provides

`title`, optional `badge`, optional header `action`, optional selection hint, `content`, and up to two dock actions with their style. The back button is always added by the frame.
