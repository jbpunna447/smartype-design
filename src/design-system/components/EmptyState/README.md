# EmptyState

What a screen shows when it has nothing yet (`SmarTypeEmptyState`): an illustration of the key character, a title, one line of help and at most one action.

## Anatomy

- Illustration: 160 dp from the set (`art_empty_*`), decorative, no content description. The glow is part of the art. Animated, with the still when animations are off; the `-dark` version on dark surfaces.
- Title: `headline-small` in `on-surface`, 16 dp below the art. Says what's missing in plain words: "No saved notes yet".
- Message: `body-medium` in `on-surface-variant`, one or two lines, says how to get started.
- Action (optional): one `Tonal` button, Medium, that starts the thing ("Add a language", "New draft").
- Centred horizontally and vertically in the empty area, `space-8` padding around.
- When the screen already has a bottom action ("Add keyboard language"), the empty state has no button of its own: one action per screen.
- Hide the screen's intro or helper text while the list is empty. The empty state is the only content.

## Rules

- Use an empty state only when a list is truly empty, not while it loads. While loading, keep the layout and show a progress indicator.
- Search with no results: art `art_empty_search`, title "No languages found", the query in the message, no action (the user is already typing).
- Never show an empty state that contradicts the screen: if the keyboard is typing in English, the languages list isn't empty (review finding L1).
- Inside the keyboard (Clipboard, Emoji history, the Notes panel) use an icon and one line instead; no illustrations in the keyboard.

## Replaces

The current `SmarTypeEmptyState` layout, the Quick Notes "Saved notes" empty card and the Writing styles "No custom styles created yet" card.

## What the consumer provides

`art` (one of the `art_empty_*` drawables), `title`, `message`, optional `actionLabel` and `onAction`.
