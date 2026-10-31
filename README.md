# SmarType design

UX review, fix specs, design system, brand and illustrations for the SmarType keyboard app. This repository holds design work only; the app's code lives in its own repository and is not changed here.

## The site

`site/` is a static website, ready to open or deploy. Start at `site/index.html` (the hand-off), then read `site/audit.html`.

| Page | What it is |
| --- | --- |
| `index.html` | Hand-off: the fixes, build order, risky areas, open decisions, downloads |
| `audit.html` | What was checked against the app code and corrected |
| `fix-1b.html` | Smartbar, voice and keyboard panels |
| `fix-1.html` | AI panel behaviour |
| `fix-2.html` | Languages |
| `fix-4.html` | Error messages |
| `fix-5.html` | Setup and onboarding |
| `design-system/` | Principles, components, tokens |
| `review.html` | End-to-end UX review, 47 findings |
| `specs.html`, `brand.html`, `art.html` | Earlier pages, each with a note on what's superseded |

## Layout

```
site/            built website (deploy this folder)
src/pages/       source of the hand-off, audit and fix pages
src/earlier/     the review, specs, brand kit and art pages
src/design-system/  design system docs, component previews, tokens
assets/brand/    app icon and logo files
assets/illustrations/  clay illustrations (WebP per density, masters, sources)
notes/           owner decisions
tools/build_site.py  builds site/ from src/ and assets/
```

## Change a page

Edit the file in `src/`, then rebuild:

```
pip install markdown
python3 tools/build_site.py
```

## Deploy on Vercel

Import this repository, choose the framework preset "Other", leave the build command empty, and set the root directory to `site`.
