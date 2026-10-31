# Button

One button component for the whole app, `SmarTypeButton`, in six variants and three sizes, so every call to action looks and behaves the same.

## Variants

| Variant | Use it for | Tokens | Today's code it replaces |
| --- | --- | --- | --- |
| `Filled` | The one main action on a screen: Turn on SmarType, Add keyboard language, Save, Continue. | `primary` / `on-primary` | `FlorisButton`, `FlorisPrimaryButton`, raw `Button` |
| `Ai` | Actions that send text to AI or sell AI: Rewrite, Translate, voice Done, Upgrade to Premium. Nothing else. | `ai-gradient-start` → `ai-gradient-end` / `on-ai-gradient` | `GradientButton`, `CompactGradientButton`, `CircularGradientButton`, the gradient branch of `SmarTypeAiActionButton` |
| `Tonal` | A useful second action: Copy, Try again, Keep talking, Manage subscription. | `primary-container` / `on-primary-container` | `FlorisSecondaryButton`, raw `FilledTonalButton` |
| `Outlined` | An alternative of equal weight beside a filled one, or a choice: Choose layout, Restore purchase. | `primary` text, `outline` border | `FlorisOutlinedButton`, raw `OutlinedButton` |
| `Text` | The low-emphasis way out: Skip, Not now, Cancel, dialog actions, Learn more. | `primary` | `FlorisTextButton`, `FlorisSkipButton`, raw `TextButton` |
| `Danger` | Confirming something that can't be undone (filled in a sheet, text style in a dialog): Remove, Delete, Sign out. | `error` / `on-error` | ad hoc red buttons (Account Sign out) |

## Sizes

- **Large, 56 dp:** only the full-width action pinned to the bottom of a task screen (onboarding, setup, subscription). Label `label-large` at 16 sp.
- **Medium, 48 dp:** the default everywhere else, including keyboard panels.
- **Small, 40 dp:** inline actions inside a card or banner. Its touch target still extends to 48 dp.
- Every size has a minimum height, not a fixed one, so text can grow at font scale 1.5.
- Corners: `radius-md` (14 dp) for all sizes. Never fully round.
- Icon: optional, 18 dp, before the label, with an 8 dp gap. The ✦ icon only on `Ai`.

## Rules

- At most **one** `Filled` or `Ai` button per screen or panel. Everything else steps down to `Tonal`, `Outlined` or `Text`.
- The AI gradient never appears on a button that doesn't involve AI. "Add keyboard language" is `Filled`.
- Task screens (onboarding, setup, sign-in, subscription) put their main action at the bottom, in thumb reach; never in the top bar.
- Bottom-of-screen actions: full width, 16 dp side gutter, 12 dp above the system navigation area. A second action goes below as `Text`, never side by side at 50/50.
- Dialogs: `Text` buttons, right-aligned, the confirming action last (rightmost). A destructive confirm uses the `Danger` text style.
- Labels are verbs in sentence case and say what happens: "Turn on SmarType", not "Next" or "OK" when a verb fits.
- Disabled: container `disabled-container`, label `disabled-content`. Show the reason next to it ("Sign in to use AI"). If the action can never work in this state, hide it instead.
- Loading: the button keeps its size, the label is replaced by a spinner and a short verb ("Saving"), and it doesn't accept taps.
- Pressed, hover and focus use the state layers (`state-pressed`, `state-hover`, `state-focus`). Focus adds a 2 dp `primary` ring.

## In the keyboard

`KeyboardPanelButton` stays, because its colours come from the keyboard theme. It follows the same variants, sizes, corners and rules. Its default style changes from the gradient (`PRIMARY`) to `SECONDARY`, so the gradient is opt-in and only on Rewrite, Translate and Insert.

## What the consumer provides

`text` (or a slot), `onClick`, `variant`, `size` (default medium), optional `icon`, `enabled`, `loading`, `fillMaxWidth`, and a `modifier` for test tags.
