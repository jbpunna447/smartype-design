# Sheet

Bottom sheets (`SmarTypeSheet`) for choosing and editing, dialogs (`SmarTypeDialog`) for confirming, and snackbars (`SmarTypeSnackbar`) for telling the user what just happened.

## When to use which

| Need | Use | Example |
| --- | --- | --- |
| Pick from options, edit a few fields | Bottom sheet | Choose a layout for Hindi, Day and night schedule, theme details |
| Confirm something that can't be undone | Dialog | Remove a language, delete a note, sign out |
| Confirm something that can be undone | Snackbar with Undo, no dialog | Removed a style chip, deleted a draft |
| Report the result of an action | Snackbar | "Copied", "Saved", "Language added" |
| A fact that stays true | Banner (see Card) | "Sign in to use AI" |

## Bottom sheet

- Fill `surface-container`, top corners `radius-xl`, drag handle, `elevation-2` in light, scrim at `scrim-opacity`.
- Title `title-large`; content uses List groups in `surface-container-high`; at most one button at the bottom (Tonal or Filled), full width.
- Swipe down, tap the scrim or press Back to close without changes. If there are unsaved edits, ask first.

## Dialog

- Fill `surface-container-high`, corners `radius-xl`, 24 dp padding, width 280 to 312 dp.
- Title `headline-small` as a question ("Remove Hindi (India)?"); body `body-medium` says what happens next.
- Actions: Text buttons, right-aligned, Cancel first, the confirming verb last. A destructive verb is red (`Danger` text style). Never "OK" or "Yes".
- Confirmations are always dialogs. Today removing a language uses a bottom sheet and other deletes use dialogs: make them all dialogs.

## Snackbar

- Fill `inverse-surface`, text `inverse-on-surface`, action in `inverse-primary`, corners `radius-md`, 16 dp above the bottom bar.
- One line, past tense, optional single action ("Undo", "View"). Shows for 4 seconds, 10 with an action.
- In the app, snackbars replace Android toasts. Toasts are only for messages from outside the app's screens (the keyboard service, the floating bubble), and even there prefer an inline message in the panel.

## Replaces

`SmarTypeSheet`, `SmarTypeSelectionBottomSheet`, the raw `ModalBottomSheet` in `FlorisCopyToClipboardActivity`, the 11 raw `AlertDialog` calls, `SmarTypeConfirmationDialog`, `FlorisConfirmDeleteDialog`, `FlorisUnsavedChangesDialog`, and most of the 93 toast calls in 32 files.

## What the consumer provides

Sheet: `title`, `content`, optional primary action, `onDismiss`. Dialog: `title`, `message`, `confirmLabel`, `destructive`, `onConfirm`, `onCancel`. Snackbar: `message`, optional `actionLabel` and handler.
