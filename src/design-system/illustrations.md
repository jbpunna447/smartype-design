# Illustrations

The soft clay 3D icon set that replaces the app's generic drawn illustrations. Every image is generated with Gemini from the shared style below, in a dark and a light version, then exported by the design team to the sizes in "Delivery".

## Where art goes

| # | Name | Screen | Replaces in code | Size in app |
| --- | --- | --- | --- | --- |
| 1 | `art_onb_welcome` | Onboarding page 1, Welcome | `WelcomeIllustration()` in `app/onboarding/OnboardingScreen.kt` | 240 dp |
| 2 | `art_onb_suggestions` | Onboarding page 2, Smart predictions | `SuggestionsIllustration()` | 240 dp |
| 3 | `art_onb_privacy` | Onboarding page 3, Privacy and data | `PrivacyIllustration()` | 240 dp |
| 4 | `art_onb_customize` | Onboarding page 4, Customizable experience | `CustomizationIllustration()` | 240 dp |
| 5 | `art_signin` | Sign-in screen hero | the plain mark at the top of `app/auth/AuthScreen.kt` | 200 dp |
| 6 | `art_ai_premium` | SmarType AI screen hero | the gradient medallion in `app/settings/ai/SmarTypeAiScreen.kt` | 200 dp |
| 7 | `art_subscription` | Premium subscriptions hero | top of `app/ui/SubscriptionScreen.kt` | 200 dp |
| 8 | `art_empty_languages` | No keyboard languages | `SmarTypeEmptyState` in `KeyboardLanguagesScreen.kt` | 160 dp |
| 9 | `art_empty_search` | No languages found (search) | `SmarTypeEmptyState` in `AddKeyboardScreen.kt` | 160 dp |
| 10 | `art_empty_themes` | No custom themes yet | custom themes list (`settings__custom_theme__list_empty`) | 160 dp |
| 11 | `art_empty_dictionary` | Empty user dictionary | `settings__udm__no_words_in_dictionary` | 160 dp |
| 12 | `art_empty_notes` | No saved notes | Quick Notes "Saved notes" empty card | 160 dp |
| 13 | `art_empty_styles` | No custom writing styles | Writing styles "Your styles" empty card | 160 dp |
| 14 | `art_empty_extension` | Extension not found | `SmarTypeEmptyState` in `app/ext/ExtensionNotFoundScreen.kt` | 160 dp |

Not illustrated: anything inside the keyboard (Clipboard empty, Emoji history), settings rows, dialogs, error banners. They keep icons.

## The SmarType key

The recurring character is a single **graphite keycap with a teal spark**, not the logo. The logo's spark is sky blue and a teal version is planned; until then the art uses a plain key so the set stays teal and doesn't need regenerating when the logo changes.

## Shared style

Soft clay 3D icons on a **transparent background**: one image per illustration that works on dark, light and AMOLED, on the page and on cards. Gemini can't export real transparency, so each image is generated on a flat green screen and the background is removed afterwards (see Delivery).

The objects must read on both grounds: graphite keycaps get a lighter top face and rim so they stand out on dark, and the white clay keeps a soft shading so it stands out on light.

```
Style: soft 3D clay icon render. Smooth, rounded, slightly inflated shapes with generous rounded edges and a soft-touch matte finish like premium vinyl or silicone. Perfectly smooth and flawless surfaces: no fingerprints, no tool marks, no seams, no grain, no handmade or sculpted texture. Soft diffused studio light from the top left with gentle ambient occlusion on the objects. Colours: graphite clay keycaps (#33474B sides, a lighter grey top face, a lighter rounded rim, and a soft rim light along the keycap edges so they stand out on a dark background), soft white clay (#E9F3F5) for secondary objects with gentle grey shading, and one teal clay accent (#2FB8C6). Background: a perfectly flat, evenly lit solid chroma green (#00B140) for background removal, with no shadow on the background, no gradient, no floor and no reflections; keep the objects free of green tint. No text, no letters, no numbers, no logos, no people, no hands, no device frames, no other colours. Square 1:1, 2048 x 2048, one centred subject filling about 55% of the frame, generous empty space around it.
```

## Prompts

**1 · art_onb_welcome**
```
A single oversized keyboard keycap floating just above the ground, tilted slightly toward the viewer. A small rounded four-point teal clay spark hovers above its top right corner and casts teal light onto the key's top surface. Two smaller blank keycaps float out of focus behind it at different depths.
```

**2 · art_onb_suggestions**
```
Three small soft white clay rounded rectangles stacked in a gentle arc above a single keycap, like word suggestions rising from a key. The middle rectangle is slightly larger and has a thin teal clay edge; the other two are plain soft white clay. Tiny teal clay sparkles drift between them.
```

**3 · art_onb_privacy**
```
A smooth soft white clay shield standing upright, with a single keycap resting in front of it. The shield's edge has a soft teal light. A small closed padlock is embossed into the keycap's top surface instead of a letter. Quiet, safe, private.
```

**4 · art_onb_customize**
```
Four keycaps arranged in a loose fan, each with a different finish: matte graphite, frosted white glass, brushed dark metal, and graphite with a teal clay edge. A small teal clay spark sits between them. They look like a palette of themes to choose from.
```

**5 · art_signin**
```
A single keycap with a small soft white clay key ring loop attached at one corner, like a house key, resting at a slight angle. A teal clay spark glows where the ring meets the key. It feels like your key, safely kept.
```

**6 · art_ai_premium**
```
A single keycap at the centre with three small teal four-point sparks orbiting it on a thin, barely visible circular path. One spark is larger and in focus in front. Teal light reflects on the key's surface.
```

**7 · art_subscription**
```
A single keycap resting on a low soft white clay pedestal, with a soft teal halo of light rising from behind it, like a product on display. Calm and premium, not flashy.
```

**8 · art_empty_languages**
```
A small soft white clay globe with faint latitude lines, resting beside a single blank keycap. A tiny teal clay spark sits on the globe's surface. Lots of empty space.
```

**9 · art_empty_search**
```
A soft white clay magnifying glass lying on its side next to a single blank keycap, the lens catching a small teal clay highlight. Lots of empty space.
```

**10 · art_empty_themes**
```
A single blank keycap with a small soft white clay paint drop resting on its top, the drop catching a teal glow. Lots of empty space.
```

**11 · art_empty_dictionary**
```
A small closed soft white clay book lying flat, with a single blank keycap resting on its cover. A thin teal ribbon bookmark peeks out of the pages. Lots of empty space.
```

**12 · art_empty_notes**
```
Two thin soft white clay sheets, slightly fanned, leaning against a single blank keycap. The front sheet has a soft teal edge glow. Lots of empty space.
```

**13 · art_empty_styles**
```
A single blank keycap with a small soft white clay quill pen resting across it, the quill tip in teal clay. Lots of empty space.
```

**14 · art_empty_extension**
```
A single blank keycap next to a small soft white clay puzzle piece lying flat, the puzzle piece's edge in teal clay. Lots of empty space.
```

## Glow behind art

Every illustration sits on a soft teal glow drawn by the app, not baked into the image. It lifts white clay objects off the light background and adds depth on dark.

- A radial gradient centred behind the subject, about 70% of the art's width in radius, fading to fully transparent at the edge.
- Colour: `primary` of the current theme. Strength: **45%** in light, **15%** in dark, **20%** in AMOLED. Dark stays low so graphite keycaps keep their contrast against the background (the centre opacity).
- Drawn behind the image, inside the same box, so it moves and scales with it. Same glow for heroes and empty states.
- Turned off with "Remove animations"? No: the glow is static, so it stays.

## Checking a result

Keep an image only if all of these are true:

- One subject, centred, about 55% of the frame, nothing touching the edges.
- Only graphite, white and teal clay. No blue, purple, orange or gold, and no green tint on the objects.
- Surfaces are perfectly smooth: no fingerprints, tool marks, seams or grain.
- The background is one flat green with no shadow or gradient on it, so it cuts out cleanly.
- No text, letters or numbers anywhere, including on keycaps.
- After cut-out, it reads clearly on both `background` values (dark `#0B1416` and light `#F5FAFB`).

## Delivery

- Cut-out: the green background is removed with a chroma key, then the edges are cleaned and any green spill neutralised. A soft contact shadow (black, about 18% opacity) is added back under the subject so it doesn't float.
- Export as WebP with alpha (lossless edges, quality 90), square. Heroes (1 to 7): 720, 480 and 240 px. Empty states (8 to 14): 480, 320 and 160 px.
- One file per illustration, `<name>.webp`, in `drawable-nodpi/` (no separate night versions needed).
- Target under 100 KB per hero file and under 50 KB per empty-state file.
- In Compose, show art with `Image(painterResource(...), contentDescription = null)`: the art is decorative, the title beside it carries the meaning.
- Check every image on `background` in all three themes and on `surface-container` (cards) before shipping.
