# ListRow

The row every settings and list screen is built from (`SmarTypeListRow`), always inside a `SmarTypeListGroup` under a section header.

## Anatomy

- Group: fill `surface-container-low`, corners `radius-lg`, no gap between rows, a 1 dp `outline-variant` divider between them.
- Section header above each group: `title-small` in `primary`, 8 dp above the group, `space-6` above the header.
- Row: minimum 56 dp tall (72 dp with a summary), 12 by 16 dp padding, 16 dp gap between parts.
- Leading (optional): a 40 dp icon tile (`primary-container`, `radius-sm`), an avatar (`radius-full`), or a drag handle. Use the same leading type for every row in a group.
- Text: title `title-medium`, summary `body-medium` in `on-surface-variant`, at most 2 lines.
- Trailing (one of): chevron `›` (opens a screen), switch, value text, badge, or nothing.

## Rules

- Every row in "Typing and input" and similar groups has a summary that names what's inside ("Autocorrect, suggestions, capitalisation"). No bare titles in a group where others have summaries.
- A row with a switch toggles when the whole row is tapped, not just the switch.
- Disabled rows keep their layout, dim title and summary to `disabled-content`, and the summary says why ("Sign in to turn this on").
- Destructive rows ("Sign out", "Delete all notes") use `error` for the title, sit last in their group, and always confirm with a dialog.
- Reorderable rows (languages, pinned styles) show a drag handle as the leading part and lift with `state-dragged` while moving.
- Home uses the same grouped rows as Settings. It doesn't show each row as its own card.

## Replaces

`SettingsListItem` (Material `ListItem`), the JetPref `Preference`, `SwitchPreference` and `ListPreference` row visuals, `SmarTypeSettingsGroup` and `SmarTypeSectionHeader` (kept, restyled), and the separate cards on Home.

## What the consumer provides

`title`, optional `summary`, `leading`, `trailing` (chevron, switch with state, value, badge), `onClick`, `enabled`, and for disabled rows the reason text.
