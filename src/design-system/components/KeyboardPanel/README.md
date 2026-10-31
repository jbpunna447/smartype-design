# KeyboardPanel

The frame every app-owned panel inside the keyboard uses (AI, Translate, Clipboard, Notes, Voice, More actions), so they open, read and close the same way.

## Anatomy

1. **Header, 48 dp:** on the left, the toolbar button that opened the panel turns into a **keyboard icon** in the same position (✦ becomes the keyboard icon for AI); tapping it returns to the keys. Then the title in `title-small`, an optional status badge, and at most one icon action on the right (Translate, Settings).
2. **Selection hint (AI and Translate, only when text is selected):** `label-small` in secondary text: "Selected text only". With no selection nothing shows; the whole message is the obvious default. This replaces the quote box that repeated the user's text.
3. **Body:** one vertical scroll region with 12 dp padding: chips, the result, or a list.
4. **Dock, pinned at the bottom:** only actions on the panel's content, at most two (Copy and Replace, or Try again). Navigation never sits here. The main action uses the AI style only when it applies an AI result (Replace, Insert).

## Behaviour

- The AI panel runs as soon as it opens: tapping ✦ is the action, there is no Rewrite button. One request returns every pinned style; results stay in memory for that text, so switching chips is instant. An empty field sends nothing.

- The keyboard icon (where the opening button was) and system Back both return to the letter keys. Back never hides the whole keyboard from a panel.
- The panel keeps its height when content changes (loading, result, error) so the keys below don't jump.
- Loading: the result area shows a skeleton; the main action shows a spinner.
- Unavailable or error: one banner explaining what happened and what still works. No action that can't work is shown.
- After Replace or Insert, the panel closes and the suggestion row shows "Replaced · Undo" for 6 seconds.

## Colours and shape

- Colours come from the active keyboard theme through `KeyboardPanelColors` (background, surface, surfaceRaised, border, secondaryText, accent, accentStart/End, onAccent, error), as the code does today. The preview above uses app colours to stand in for a theme.
- Type, spacing, corners and states come from this system: panel corners `radius-lg` (`PanelShape`, 16 dp), actions `radius-md` (`ActionShape`, 14 dp), chips `radius-sm`. No 999 dp pills.
- Inline elements only: no popups, dialogs or dropdown windows from the keyboard.

## Replaces

`KeyboardPanelHeader` (the ↵ back icon becomes the keyboard-icon toggle), `KeyboardPanelActionRow`, `KeyboardPanelButton` defaults (gradient becomes opt-in), the AI panel's source preview box, and Translate's gradient Close button.

## What the consumer provides

`title`, optional `badge`, optional header `action`, optional selection hint, `content`, and up to two dock actions with their style. The keyboard-icon toggle is always added by the frame.
