# Chip

Small selectable labels (`SmarTypeChip`) for filters and AI styles, and a non-interactive `SmarTypeBadge` for status.

## Chip

- 32 dp tall (48 dp touch target), 12 dp horizontal padding, corners `radius-sm`, label `label-medium`.
- Unselected: transparent with a 1 dp `outline` border, text `on-surface-variant`.
- Selected: `primary-container` fill, `on-primary-container` text, a leading ✓. The tick, not colour alone, shows selection.
- AI style chips in the keyboard and Write: selected uses the AI gradient with `on-ai-gradient`. Each style keeps its own emoji, which is content. A style's emoji never changes to show state (today Grammar fix shows ✅ after use, which reads as "done").
- Chips in one row scroll horizontally; they never wrap in the keyboard. In app screens they wrap with an 8 dp gap.

## Badge

- 24 dp tall, 8 dp padding, corners `radius-xs`, `label-small`.
- `Success` (`secondary-container`), `Neutral` (`tertiary-container`), `Info` (`primary-container`), `Error` (`error-container`). Always words, optionally a leading glyph.
- Badges never look tappable and never sit where a button would.

## Replaces

`FlorisChip` (12 dp), `SmarTypeStatusChip` (full pill), Material `FilterChip` (8 dp), `SuggestionChip`, `InputChip`, and the pill-shaped style chips in the AI panel (999 dp corners in `KeyboardPanel.kt`).

## What the consumer provides

Chip: `label`, `selected`, `onClick`, optional `leadingEmoji`, `kind` (filter or ai), `enabled`. Badge: `label`, `kind`, optional glyph.
