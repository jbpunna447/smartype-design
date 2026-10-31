# Button audit

The app's buttons as they are in the code today (main @ c3d86d39c), and what changes to reach the single `SmarTypeButton` set in Components → Button.

## What's in the code

| Component | File | Uses | Style today |
| --- | --- | --- | --- |
| `FlorisButton` | `lib/compose/FlorisButtons.kt` | 13 | Filled primary, 48 dp min, 12 dp corners |
| `FlorisPrimaryButton` | `lib/compose/FlorisButtons.kt` | 3 (previews only) | Filled primary, 56 dp, 14 dp corners |
| `FlorisSecondaryButton` | `lib/compose/FlorisButtons.kt` | 2 (previews only) | Surface fill, 56 dp, 14 dp corners |
| `FlorisOutlinedButton` | `lib/compose/FlorisButtons.kt` | 15 | Outlined, 48 dp, 12 dp corners |
| `FlorisTextButton` | `lib/compose/FlorisButtons.kt` | 13 | Text, 48 dp, 12 dp corners |
| `FlorisIconButton` | `lib/compose/FlorisButtons.kt` | 25 | Icon button |
| `FlorisGoogleSignInButton`, `FlorisSkipButton` | `lib/compose/FlorisButtons.kt` | 4, 3 | Sign-in and skip |
| `GradientButton` + `Compact…`, `Circular…` | `lib/compose/GradientButton.kt` | 2 in screens | AI gradient, 56 or 48 dp, 14 or 12 dp corners |
| `SmarTypeAiActionButton` | `app/settings/ai/SmarTypeAiScreen.kt` | 2 | Gradient, or raw `OutlinedButton` |
| `KeyboardPanelButton` | `ime/ui/KeyboardPanel.kt` | 18 | Keyboard-theme colours, 14 dp corners; styles PRIMARY (gradient, the default), SECONDARY, TONAL, TEXT |
| `PrimaryButton`, `SecondaryButton` (panel scope) | `ime/ui/KeyboardPanel.kt` | 4, 4 | Wrappers over `KeyboardPanelButton` |
| Raw Material `Button`, `OutlinedButton`, `TextButton`, `FilledTonalButton` | 22 files | 9, 8, 21, 2 | Material defaults: full-pill shape, 40 dp height |

## Problems

1. **The AI gradient on a non-AI action.** "Add keyboard language" (`KeyboardLanguagesScreen.kt`) is a `GradientButton`.
2. **The gradient is the keyboard panel's default.** `KeyboardPanelButton` defaults to `PRIMARY`, so any call without a style becomes a gradient: Translate's "Close" and "Return to keyboard" both look like the main AI action.
3. **Raw Material buttons skip the shared ones** in Quick Notes, themes, the subtype editor, sheets and dialogs. They get Material's pill shape and 40 dp height, so they don't match the 14 dp, 48 dp buttons beside them.
4. **Two heights for the same job.** Bottom actions are 56 dp in onboarding and setup but 48 dp on the SmarType AI screen; the languages screen grows with text.
5. **Two corner sizes.** 12 dp (`FlorisButton`, outlined, text) and 14 dp (primary, gradient, panels) sit on the same screens.
6. **Unused variants.** `FlorisPrimaryButton` and `FlorisSecondaryButton` exist but only previews use them.
7. **Destructive styling is ad hoc.** Account's "Sign out" is a large outlined red button; dialogs use plain text buttons for "Remove".
8. **Side-by-side pairs.** Onboarding puts "Previous" and "Next" at 50/50 width, so the main action is half as wide as on every other screen.

## Changes, in order

1. Add `SmarTypeButton(variant, size)` in `lib/compose/` with the six variants. Keep the old functions as thin wrappers that call it, so nothing breaks while screens move over.
2. Change `KeyboardPanelButton`'s default style to `SECONDARY`; pass `PRIMARY` explicitly only for Rewrite, Translate and Insert.
3. Switch "Add keyboard language" to `Filled`.
4. Replace raw Material buttons screen by screen (22 files), starting with Quick Notes and the theme screens.
5. Make every bottom-of-screen action Large (56 dp); everything else Medium (48 dp).
6. Use 14 dp corners for every button.
7. Account "Sign out": a `Danger` text-style row at the bottom of the list, with a confirmation dialog.
8. Onboarding: full-width "Next"; "Back" becomes the system back gesture plus a small text button at the top.
9. Remove the unused `FlorisPrimaryButton` and `FlorisSecondaryButton` once nothing calls them.

These are presentation changes; no behaviour, route or test tag changes. Screens that touch sign-in or purchases (`AuthScreen`, `SubscriptionScreen`) only change the button's look, not what it does.
