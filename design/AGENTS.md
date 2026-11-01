# AGENTS.md (design)

Rules for work in `design/`: the design site, brand, illustrations and design system for SmarType.

## Commands
- Build the site: `python3 tools/build_site.py` (needs `markdown`). The built site goes to `site/` and is committed: Vercel serves it as is.
- Icon kit: `python3 tools/build_icon_kit.py --font <GoogleSansFlex[ROND,opsz,slnt,wdth,wght].ttf>` (needs fontTools, skia-pathops, uharfbuzz, Pillow, Chrome).
- Illustrations: `python3 tools/build_illustrations.py` (needs Chrome).
- Check: build the site, then look at changed pages at 375 px and in light and dark. No Gradle build and no device test.

## Rules
- Edit the sources (`src/`, `tools/`, `assets/`), never `site/` by hand; rebuild after every change.
- Icons: Material Symbols Rounded only (plus the brand spark and the Google G). No emoji or text symbols as icons; no triangle warning icon.
- Brand: one spark (`assets/icons/brand/spark.svg`); the logo and its rules are on the Brand page. Every mark is vector.
- Illustrations: the key character; anything drawn straight on the background uses `var(--ill-ink)` so it stays visible on dark.
- No personal data on the site: no real names, emails, tokens or device IDs. Use placeholders such as "Priya".
- Publishing happens from `main` through the `Publish design site` workflow (see the root `AGENTS.md`). It mirrors all of `design/` to a public repo: nothing here may be private.
