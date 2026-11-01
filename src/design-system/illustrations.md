# Illustrations

One character across the app: the SmarType key, alive. It comes from the logo (the S lifts off the app icon's key and becomes the first letter typed), and it does what SmarType does: it watches you type, spots a typo, fixes it with the spark, translates and listens.

## The character

- **Body:** the brand key: white face, light grey lip (`#C3D5DA`), corners at 24% of its size. No arms, no legs, no S.
- **Face:** two Ink eyes with a white catchlight, a smile, mint cheeks (`#4BDCA4` at 45%).
- **The spark:** its idea and its tool (the brand spark). On light surfaces the deep spark gradient; on dark surfaces the AI gradient.
- **Props** are brand shapes: white cards and message bubbles, AI-gradient chips and badges, the globe, a magnifier, a puzzle piece.
- **Glow:** a soft disc in the brand gradient behind each scene.

## Expressions

| Expression | Eyes | Brows | Mouth | Used for |
| --- | --- | --- | --- | --- |
| Watching | Open, following the action | — | Smile | Typing, empty notes, languages |
| Surprised | Wide | Raised | Small round | Spotting a typo, Premium, themes |
| Curious | Open | One raised | Small, sideways | No results, empty styles, missing extension |
| Focused | Squinting | Angled down | Small, sideways | Fixing, SmarType AI |
| Happy | ^ ^ | — | Big smile | Fixed, all set, free tries |
| Asleep | Closed | — | Small round | Empty dictionary |

## The set

Heroes are drawn for 200 dp, empty states for 160 dp. See the Illustrations page for each one animated, on light and dark, and `assets/illustrations/README.md` for the files.

| Name | Screen | Replaces in code | Moment |
| --- | --- | --- | --- |
| `art_welcome` | Setup, first page | `WelcomeIllustration()` in `app/onboarding/OnboardingScreen.kt` | The S lifts off the logo and becomes the first letter; the key watches the message, spots "runing", throws the spark, cheers at "running" |
| `art_signin` | Setup, sign in | The plain mark at the top of `app/auth/AuthScreen.kt` | Three free tries pop out of a little box; the key watches, then cheers |
| `art_done` | Setup, You're all set | New (the setup's last page) | The key hops; a check pops; confetti falls |
| `art_premium` | Premium | Top of `app/ui/SubscriptionScreen.kt` | The key on a stage, sparks orbiting |
| `art_ai` | SmarType AI | The gradient medallion in `app/settings/ai/SmarTypeAiScreen.kt` | Messy lines snap into a neat card as the key focuses |
| `art_empty_notes` | Notes in the app, no notes | Quick Notes "Saved notes" empty card | A blank note with a blinking caret; the key watches |
| `art_empty_styles` | Writing styles, none of your own | Writing styles "No custom styles created yet" card | Two style chips and an empty slot with a plus; the key is curious |
| `art_empty_search` | Add language, no results | `SmarTypeEmptyState` in `AddKeyboardScreen.kt` | A magnifier sweeps; a question mark pops |
| `art_empty_languages` | Keyboard languages, none | `SmarTypeEmptyState` in `KeyboardLanguagesScreen.kt` | A globe turns; letters in three scripts pop out. With the new Languages flow the list is never empty (the language in use is always saved), so this is a fallback only |
| `art_empty_themes` | Themes, no custom themes | Custom themes list (`settings__custom_theme__list_empty`) | Swatches circle the key and tint its face |
| `art_empty_dictionary` | User dictionary, empty | `settings__udm__no_words_in_dictionary` | The key naps against an empty book |
| `art_extension` | Extension not found | `SmarTypeEmptyState` in `app/ext/ExtensionNotFoundScreen.kt` | A puzzle with a missing piece; the key is puzzled |

## Motion

- Springy: squash and stretch on hops; a blink every 4 s; loops of 3–9 s.
- Reduced motion: show the still, frozen at the illustration's key moment (never a blank first frame).

## Dark surfaces

Anything drawn straight onto the background in Ink (voice bars, the magnifier) turns light (`#E3EEF0`); the spark switches to the AI gradient. Shapes on white cards and the key stay as they are. The `-dark` files already do this.

## Not illustrated

Anything inside the keyboard (Clipboard empty, emoji history), settings rows, dialogs and banners. They keep icons.
