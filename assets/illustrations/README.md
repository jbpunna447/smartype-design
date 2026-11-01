# SmarType illustrations

The brand key as a character, in 12 moments. Built by `tools/build_illustrations.py` from `src/illustration_set.py`; don't edit the files by hand.

| File | What it is |
| --- | --- |
| `svg/<name>.svg`, `svg/<name>-dark.svg` | Animated (CSS), for light and dark surfaces |
| `still/<name>.svg`, `still/<name>-dark.svg` | Frozen at the key moment: use when the phone's "Remove animations" is on |
| `png/<name>@3x.png`, `png/<name>-dark@3x.png` | The still at 3x (600 px for heroes, 480 px for empty states), transparent background |

| Name | Screen | Size |
| --- | --- | --- |
| `art_welcome` | Setup, first page | 200 dp |
| `art_signin` | Setup, sign in | 200 dp |
| `art_done` | Setup, You're all set | 200 dp |
| `art_premium` | Premium | 200 dp |
| `art_ai` | SmarType AI settings | 200 dp |
| `art_empty_notes` | Notes, no notes yet | 160 dp |
| `art_empty_styles` | Writing styles, none yet | 160 dp |
| `art_empty_search` | Add language, no results | 160 dp |
| `art_empty_languages` | Keyboard languages, none | 160 dp |
| `art_empty_themes` | Themes, no custom themes | 160 dp |
| `art_empty_dictionary` | User dictionary, empty | 160 dp |
| `art_extension` | Extension not found | 160 dp |

## In the app

- Motion: convert the animated SVG to Lottie (for example with LottieFiles' SVG import, or rebuild in After Effects with the timings in `src/illustration_set.py`), and play it with Lottie Compose. When animations are off (`Settings.Global.ANIMATOR_DURATION_SCALE` is 0), show the still.
- Without Lottie, ship the still PNG or the still SVG converted to a vector drawable.
- Light and dark: use the `-dark` files on dark surfaces. In them, ink drawn straight onto the background turns light (`#E3EEF0`) and the spark uses the AI gradient.
- Text inside the art (the message bubbles) must be translated with the app. In Lottie, keep it as live text in Google Sans Flex.
- Never inside the keyboard. Empty states keep their words and button under the art.
