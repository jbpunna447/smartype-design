# SmarType design

What changes in the SmarType keyboard app, and why. This repository holds design work only; the app's code lives in its own repository and is not changed here.

## The site

`site/` is a static website. Start at `site/index.html`.

- **Flows** (`site/flows/`): one page per flow, each with the problem, today's screens next to the new ones, what changes, done-when, and a developer section (code, decisions, risky areas). Flows marked **New feature** explain what to build instead.
- **Real-size specs:** new screens are HTML drawn at 1 px = 1 dp on a 360 × 800 dp phone, from the design-system tokens and the SmarType Night and Day keyboard themes. "Show measurements" draws the sizes; "Spec" under each screen lists every element's size, component, tokens and icon. Add `?measure=1` to a flow page's address to open it with measurements on.
- **Backlog:** review findings that aren't designed yet.
- **Design system:** principles, components, tokens, and **Icons** (Material Symbols Rounded).
- **Downloads:** app icon, illustrations, icons (SVG and Android vector drawables).

## Layout

```
site/                built website (deploy this folder)
src/flows.py         content of every flow page
src/screens.py       every new screen, built from src/components.py
src/components.py    real-size mockup components with spec annotations
src/spec.css, spec.js, site.css
src/design-system/   design system docs, component previews, tokens.json
assets/screens/today/  screenshots of today's app (from the UX review)
assets/icons/        Material Symbols Rounded 0.48.0 (Apache 2.0) and the brand spark
assets/brand/, assets/illustrations/
archive/             earlier working pages (fix specs, audit, review); not published
notes/               owner decisions
tools/build_site.py  builds site/
```

## Change a page

Edit the content in `src/`, then rebuild:

```
pip install markdown
python3 tools/build_site.py
```

## Deploy on Vercel

Framework preset "Other", no build command, root directory `site`.
