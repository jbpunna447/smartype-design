SmarType is a calm, keyboard-first Android app. The app is dark by default, built on Material 3 with a teal accent, set in Google Sans Flex, and saves its boldest moments (3D artwork and the AI gradient) for the few places that matter. This system writes down the app as it looks today (its colours, radii and type scale come straight from the code), so new screens and fixes stay consistent with it. It is not a redesign. These rules apply to the SmarType app and to the app-owned panels inside the keyboard. The keyboard keys themselves follow the user's chosen keyboard theme.

## Principles

- **Calm first.** Neutral surfaces, one accent, generous spacing. If a screen needs a second accent colour, it probably needs fewer things on it.
- **Dark by default, light as an equal.** Design every screen in `dark` first, then check `light` and `amoled`. Never ship a screen that only works in one.
- **The keyboard is the product.** Settings exist to make typing better. Lead with what the user does (type, rewrite, dictate), not with configuration.
- **AI only when asked.** The spark ✦ and the AI gradient appear only on things that send text to AI after a tap. Nothing else gets them.
- **One bold moment per screen.** A 3D illustration or the AI gradient, not both, and never on a dense settings screen.
- **Reference: Gboard.** Familiar Google patterns: Material 3 components, a plain settings list, no surprises. SmarType differs in its teal identity and its AI.

## Writing

- Speak to the user as "you". Sentence case for everything: titles, buttons, chips. ("Open keyboard settings", not "Open Keyboard Settings".)
- Name things by what people recognise: "keyboard languages", not "subtypes"; "Sign in with Google", not "Firebase Authentication".
- Buttons say exactly what happens: "Turn on SmarType", "Replace", "Insert". The confirmation echoes it: "Replaced · Undo".
- Errors say what went wrong and what to do, with no blame and no internal terms. Write "AI can't run on this device right now. Your text wasn't sent." Never write "App verification failed. Update SmarType and try again."
- No emoji in interface text. The only glyph that carries meaning is ✦ for AI. Style chips may show their own emoji because that is the content.
- Numbers as digits ("3 styles", "Step 1 of 3"). Times as "11:31", relative dates as "Yesterday".

## Colour

- Build screens from the Material 3 roles in this system. Page: `background`. Groups and cards: `surface-container-low`, then `surface-container` and `surface-container-high` for raised layers. Text: `on-surface`; secondary text: `on-surface-variant`.
- `primary` is the single accent: the main button, selected states, links, the focus ring. Text on it is `on-primary`.
- Use `primary-container` with `on-primary-container` for soft emphasis (tonal buttons, the current step, info banners).
- `secondary` means success only ("Keyboard ready", "Saved"). `tertiary-container` is for neutral badges ("Free plan").
- `error` is for errors and destructive actions, always with a word or icon, never colour alone.
- The AI gradient (`ai-gradient-start` to `ai-gradient-end`, text `on-ai-gradient`) is reserved for AI actions: Rewrite, Translate, voice Done, Premium upgrade. The keyboard keeps its own gradient (`brand-cyan` to `brand-teal`).
- `amoled` keeps every role from `dark` and sets `background`, `surface` and the container steps to near-black.
- Every text pair here has been checked: at least 4.5:1 in all three themes. `outline` on `background` is 4.2:1 in light: use it for control borders (3:1 needed), not for text.

## Type

- One family: Google Sans Flex (variable). Hierarchy comes from size and weight, never from a second typeface. Until the font ships in the app, the fallback is DM Sans.
- Screen title: `title-large` in the small top app bar, `headline-large` when the bar is expanded. Section headers: `title-small` in `primary`.
- Row titles: `title-medium`; row summaries: `body-medium` in `on-surface-variant`.
- Buttons: `label-large`. Chips: `label-medium`. Badges and step labels: `label-small`, the smallest text allowed.
- Onboarding headlines: `display-small` or `headline-medium`, never larger on a phone.
- Non-Latin scripts (Devanagari and others) fall back to the system Noto fonts; keep line heights from the style so mixed lines don't jump.

## Layout and spacing

- 4 dp grid. Side gutter `space-4` (16 dp), `space-5` on wide phones. Card padding `space-4`. Gap between cards `space-3`. Gap between sections `space-6`.
- Touch targets at least `space-12` (48 dp). Prefer min-heights over fixed heights so text can grow at large font sizes.
- One column on phones. Primary action at the bottom of task screens (onboarding, setup), at the top right for app bar actions.
- Test every screen at font scale 1.5 and at 320 dp width: nothing clips, text wraps.

## Shape and elevation

- Buttons `radius-md` (see Components → Button); chips and fields `radius-sm`; cards `radius-lg`; dialogs and sheet tops `radius-xl`. `radius-full` only for avatars, dots and switch thumbs, never for buttons.
- Dark and AMOLED show depth with tonal steps (`surface-container-*`), not shadows. Light uses `elevation-1` for menus and `elevation-2` for dialogs and sheets. Cards stay flat (`elevation-0`).
- Dividers: `outline-variant`, 1 dp, only between rows inside one group.

## States

- Pressed, hovered, focused and dragged states use a layer of the content colour at `state-pressed`, `state-hover`, `state-focus` and `state-dragged`.
- Disabled: content at `disabled-content`, container at `disabled-container`. A disabled control still says why nearby ("Sign in to use AI").
- Focus ring: 2 dp solid `primary`, offset 2 dp. It reaches at least 3:1 on every surface in every theme.
- Loading: keep the layout stable and show a progress indicator in place of the action; never blank the screen.

## Motion

- Short and purposeful: 100 ms for presses and toggles, 200 ms for panels and chips, 300 ms for screen transitions, using Material's emphasized easing.
- One orchestrated moment at most per screen (the welcome keycap rising, the AI result appearing). No looping decoration.
- With "Remove animations" on, cross-fade at 100 ms or cut.

## Illustration

- 3D artwork appears only on onboarding, empty states and celebration moments, never on settings or inside the keyboard.
- Style: soft clay 3D icons. Rounded, slightly inflated shapes with a smooth soft-touch matte finish, perfectly smooth (no fingerprints, tool marks or handmade texture). Graphite clay keycaps, soft white clay details and one teal clay accent, No text, no people, no device frames.
- Ship art with a transparent background: one image per illustration for every theme and surface. It must read on both the dark and the light `background`.
- The recurring subject is a plain graphite keycap with a teal spark, not the logo. The full list, prompts and export sizes are in the Illustrations section.
- Show art at 160 to 240 dp wide, ship it as WebP at 3x, under 80 KB each.

## Iconography

- Material Symbols Rounded, outlined, 24 dp, weight 400. Filled only for the selected state (bottom navigation, toggled tool).
- Icons sit in `on-surface-variant`, or `primary` when they show a selected or active state.
- The spark ✦ is the AI symbol. Use it only on AI entry points and AI actions.
- Every icon-only button has a content description. Decorative icons have none.

## Logo

- The SmarType mark is a graphite keycap with a frosted S (its lower half drawn as voice bars) and a glowing spark. Use the files in Logos; never redraw it.
- App icon: the keycap at 50% of a white adaptive-icon background. Themed icons use the monochrome S and spark.
- Keep clear space of at least 25% of the keycap's width. Don't recolour, crop or add effects. A teal version of the mark is planned; until then, use these files as they are.

## The keyboard

- The keys, key labels and keyboard background follow the user's keyboard theme (the built-in SmarType themes or their own). This system does not restyle them.
- App-owned keyboard panels (AI, Translate, Clipboard, Voice) take their colours from the active keyboard theme, as the code does today, and use this system's type, spacing, radii and states.
- Back, or an ABC key, from any panel always returns to the letter keys.
