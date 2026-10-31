# Component audit

Cards, list rows, chips, sheets, dialogs, feedback and keyboard panels as they are in the code today (main @ c3d86d39c), and the steps to reach Components → Card, ListRow, Chip, Sheet and KeyboardPanel.

## What's in the code

| Area | Today | Uses |
| --- | --- | --- |
| Cards | `FlorisInfoCard`, `FlorisErrorCard`, `FlorisWarningCard`, `FlorisSimpleCard` (`lib/compose/FlorisCards.kt`) and `SmarTypeSurfaceCard` (`lib/compose/SmarTypeAppSurface.kt`), plus 8 raw `Card` calls | 20, 19, 5, 5, 24, 8 |
| Rows | `SettingsListItem` (Material `ListItem`), JetPref `Preference` / `SwitchPreference` / `ListPreference`, `SmarTypeSettingsGroup`, `SmarTypeSectionHeader` | 50 ListItem, 158 / 57 / 36 prefs, 5, 21 |
| Chips | `FlorisChip` (12 dp), `SmarTypeStatusChip` (full pill), Material `FilterChip` (8 dp), `SuggestionChip`, `InputChip`, AI panel chips (999 dp) | 21, 13, 5, 1, 1 |
| Sheets | `SmarTypeSheet`, `SmarTypeSelectionBottomSheet`, raw `ModalBottomSheet` | 22, 3 |
| Dialogs | raw `AlertDialog`, `SmarTypeConfirmationDialog`, `FlorisConfirmDeleteDialog`, `FlorisUnsavedChangesDialog` | 11, 8, 3, 1 |
| Feedback | Android toasts (`Toast.makeText`, `showShortToast`, `showLongToast`); no snackbars | 93 calls in 32 files |
| Keyboard panels | `KeyboardPanelHeader`, `KeyboardPanelCard`, `KeyboardPanelButton`, `KeyboardPanelActionRow` (`ime/ui/KeyboardPanel.kt`) | all panels |
| Corner literals | `RoundedCornerShape` with 3, 4, 5, 6, 10 and 999 dp outside the token scale | 16 places |

## Problems

1. **Two card families** with different paddings and colours (`FlorisCards` and `SmarTypeSurfaceCard`) on neighbouring screens.
2. **Home and Settings list rows differently.** Home shows each row as its own card with gaps; Settings uses one grouped card with dividers.
3. **Rows without summaries next to rows with them** ("Keyboard", "Smartbar", "Typing", "Gestures" have none; review finding S2).
4. **Four chip shapes:** 8, 12, full pill and 999 dp, sometimes on the same screen (Writing styles and the AI panel).
5. **Status shown as chips that look tappable** (`SmarTypeStatusChip` pills for "Free plan", "Keyboard ready").
6. **Confirmations are inconsistent:** removing a language uses a bottom sheet, deleting a note uses a dialog, signing out has no confirmation style of its own.
7. **93 toasts.** They disappear, can't be undone, appear on top of other apps, and include the misleading "Sign in before restoring or purchasing premium" (review O4, V2).
8. **Keyboard panel header** puts the only way back (a ↵ icon) at the top left, where it looks like Enter (review A10). The AI panel repeats the user's text in a quote box (A11).
9. **Corner sizes outside the scale** (3, 4, 5, 6, 10, 999 dp) in Writing styles, tips, the plan card bar, the AI overlay and the theme editor.

## Changes, in order

1. Add `SmarTypeCard` and `SmarTypeBanner`; make the `FlorisCards` functions and `SmarTypeSurfaceCard` call them.
2. Restyle `SmarTypeSettingsGroup` and `SmarTypeSectionHeader` to the ListRow spec; render JetPref rows and `SettingsListItem` through `SmarTypeListRow`. Add summaries to the four bare Typing rows.
3. Move Home's list to one grouped List group.
4. Add `SmarTypeChip` and `SmarTypeBadge`; swap `SmarTypeStatusChip` to a badge, then `FlorisChip`, `FilterChip` and the AI panel chips to chips.
5. Add `SmarTypeDialog`; route every confirmation through it, including removing a language.
6. Add a snackbar host to the app scaffold; replace in-app toasts with snackbars or banners, starting with the auth and subscription messages.
7. Rework `KeyboardPanelHeader` and `KeyboardPanelActionRow` into the KeyboardPanel frame: `arrow_back` and the panel name in the header, the panel replacing the smartbar and the keys, a selection hint instead of the source quote, Back returns to the keys.
8. Replace corner literals with shape tokens (`radius-xs` for the small ones, `radius-sm` for chips).

Steps 1 to 6 are presentation only. Step 7 touches keyboard navigation (Back handling in `KeyboardPanelBackStack`), so it needs a device test. Nothing here changes how text is replaced in other apps.
