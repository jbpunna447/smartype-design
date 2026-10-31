# Card

A flat container for one piece of content (`SmarTypeCard`), plus a `SmarTypeBanner` for a short status message with an optional action.

## Card

- Fill `surface-container-low`, corners `radius-lg`, padding `space-4`, no border, no shadow (`elevation-0`).
- `Raised` (fill `surface-container-high`) only for a card that sits inside another surface, such as a sheet.
- `Hero` (fill `surface-container`, 12 dp internal gap) for the one summary card at the top of a screen: the Home plan card, the SmarType AI status.
- Title `title-medium`, body `body-medium` in `on-surface-variant`. Actions inside a card are `Small` buttons, at most one `Tonal` plus one `Text`.
- A whole card can be tappable; then it has a pressed state layer and no separate button.
- Cards stack with a `space-3` gap. Settings lists don't use one card per row: use a List group.

## Banner

- For status the user should notice but not act on immediately: "Sign in to use AI", "SmarType is on", "AI can't run on this device right now".
- `Info`: `primary-container`. `Success`: `secondary-container`. `Warning`: `warning-container` with `on-warning-container`, for "something is limited, but nothing failed" (for example "Premium isn't available on this phone"). `Error`: `error-container`. Corners `radius-md`, padding 12 by 16 dp.
- Leading icon, bold first line (the fact), regular second line (what it means), optional text action on the right.
- One banner per screen, at the top of the content. It replaces toasts for anything that stays true.

## Replaces

`FlorisInfoCard`, `FlorisErrorCard`, `FlorisWarningCard`, `FlorisSimpleCard`, `SmarTypeSurfaceCard` and the 8 raw `Card` calls (Quick Notes, setup step cards).

## What the consumer provides

Card: `content`, optional `onClick`, `variant` (default, raised, hero). Banner: `kind` (info, success, error), `title`, optional `message`, optional `action` label and handler.
