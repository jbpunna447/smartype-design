# Chip

Small selectable labels (`SmarTypeChip`) for filters and AI styles, and a non-interactive `SmarTypeBadge` for status.

## Chip

- 32 dp tall (48 dp touch target), 12 dp horizontal padding, corners `radius-sm`, label `label-medium`.
- Unselected: transparent with a 1 dp `outline` border, text `on-surface-variant`.
- Filter chips (app screens): selected uses `primary-container` fill, `on-primary-container` text and a leading `check` icon (18 dp). The tick, not colour alone, shows selection.
- AI style chips (Rewrite, Translate and Format panels): text only, no icons or emoji. Selected uses the AI gradient with `on-ai-gradient`; TalkBack says "selected". Only one is selected at a time, so the fill is enough.
- Icons in chips and badges come from Material Symbols Rounded only. No emoji, no text symbols.
- Chips in one row scroll horizontally; they never wrap in the keyboard. In app screens they wrap with an 8 dp gap.

## Badge

- 24 dp tall, 8 dp padding, corners `radius-xs`, `label-small`.
- `Success` (`secondary-container`), `Neutral` (`tertiary-container`), `Info` (`primary-container`), `Error` (`error-container`). Always words, optionally a leading icon.
- Badges never look tappable and never sit where a button would.

## Replaces

`FlorisChip` (12 dp), `SmarTypeStatusChip` (full pill), Material `FilterChip` (8 dp), `SuggestionChip`, `InputChip`, and the pill-shaped style chips in the AI panel (999 dp corners in `KeyboardPanel.kt`).

## What the consumer provides

Chip: `label`, `selected`, `onClick`, `kind` (filter or ai), `enabled`. Badge: `label`, `kind`, optional leading icon (Material Symbols Rounded, 16 dp).
