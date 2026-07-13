# CalcMate – Multilingual Online Calculators

A modern, free calculator website inspired by [rechneronline.de](https://rechneronline.de/) — no login, no dependencies, no build step. Just static HTML, CSS and vanilla JavaScript.

## Features

- **7 calculators**: basic calculator (with keypad, parentheses and percent), percentage calculator (3 modes), VAT calculator (net ↔ gross), rule of three (direct and inverse), slope calculator (length + height → percent, angle, slope length, with triangle diagram), BMI calculator, compound interest calculator
- **4 languages** on separate, fully translated URLs: [`/de/`](de/), [`/en/`](en/), [`/fr/`](fr/), [`/it/`](it/)
- **Light, minimal design**: responsive layout, flat white theme, no external fonts or trackers
- **SEO optimised**:
  - Unique `<title>` and meta description per language
  - `hreflang` alternate links (incl. `x-default`) on every page and in the sitemap
  - Canonical URLs, Open Graph tags
  - JSON-LD structured data (`WebApplication` + `FAQPage`) per language
  - `sitemap.xml` and `robots.txt`
- **Localised details**: decimal comma on DE/FR/IT keypads, country-specific default VAT rates (DE 19 %, EN 20 %, FR 20 %, IT 22 %), locale-aware number formatting via `Intl.NumberFormat`
- The root page (`/`) redirects visitors to their browser language (or their last choice) and doubles as a language chooser.

## Structure

```
index.html        Language landing page (auto-redirect + chooser)
de/index.html     German version
en/index.html     English version
fr/index.html     French version
it/index.html     Italian version
assets/style.css  Shared styles (light + dark theme)
assets/app.js     Shared calculator logic (safe expression parser, no eval)
assets/favicon.svg
sitemap.xml
robots.txt
```

## Hosting

The site is pure static files — host it anywhere (GitHub Pages, Netlify, any web server).

The absolute URLs used for SEO (canonical, hreflang, sitemap) currently point to
`https://drbrius.github.io/Allgemein1/`. If you deploy under a different domain,
do a search &amp; replace of that base URL across `*.html`, `sitemap.xml` and `robots.txt`.

To enable GitHub Pages: repository **Settings → Pages → Deploy from branch**, select the branch and `/ (root)`.

## Development

No build step. Open `index.html` in a browser, or serve locally:

```
python3 -m http.server
```
