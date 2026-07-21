# CalcMate – Multilingual Online Calculators

A modern, free calculator website inspired by [rechneronline.de](https://rechneronline.de/) — no login, no dependencies, no runtime build step. Just static HTML, CSS and vanilla JavaScript.

## Features

- **12 calculators**, each on its own SEO-friendly URL per language:
  basic calculator (keypad, parentheses, percent), percentage (3 modes), VAT (net ↔ gross),
  discount, rule of three (direct and inverse), slope (percent/degrees, with triangle diagram),
  BMI, compound interest, loan (annuity payment, total cost, interest), fuel cost,
  tip & bill splitting, days between dates
- **4 languages** on separate, fully translated URLs with localised slugs:
  [`/de/`](de/), [`/en/`](en/), [`/fr/`](fr/), [`/it/`](it/) —
  e.g. `de/kreditrechner/`, `en/loan-calculator/`, `fr/calcul-pret/`, `it/calcolo-prestito/`
- **SEO optimised**:
  - One page per calculator per language (48 calculator pages + 4 hub pages), each with a
    unique `<title>`, meta description, intro, formula/explainer article and 3-question FAQ
  - `hreflang` alternate links per calculator cluster (incl. `x-default`), canonical URLs, Open Graph tags
  - JSON-LD structured data per page: `WebApplication`, `FAQPage`, `BreadcrumbList` (hubs add `ItemList`)
  - Internal linking: hub card grid + "related calculators" chips on every page
  - `sitemap.xml` (with `xhtml:link` alternates) and `robots.txt`
- **Localised details**: decimal comma on DE/FR/IT keypads, country-specific default VAT rates
  (DE 19 %, EN 20 %, FR 20 %, IT 22 %), locale-aware number formatting via `Intl.NumberFormat`
- The root page (`/`) redirects visitors to their browser language (or their last choice) and doubles as a language chooser.

## Structure

```
index.html            Language landing page (auto-redirect + chooser)
de|en|fr|it/          Language hubs (card grid linking to each calculator)
de|en|fr|it/<slug>/   One page per calculator (48 pages total)
assets/style.css      Shared styles
assets/app.js         Shared calculator logic (safe expression parser, no eval)
assets/favicon.svg
tools/build.py        Static site generator (page structure)
tools/content_*.py    Per-language content: titles, intros, forms, articles, FAQs
sitemap.xml
robots.txt
```

## Editing content / adding calculators

The generated pages are plain static files — the site itself needs no tooling. To change
content or add a calculator, edit `tools/content_<lang>.py` (and `tools/build.py` for
structure/order/related links), add the calculator's handler to `assets/app.js`, then run:

```
python3 tools/build.py
```

## Hosting

The site is pure static files — host it anywhere (GitHub Pages, Netlify, any web server).

The absolute URLs used for SEO (canonical, hreflang, sitemap) currently point to
`https://drbrius.github.io/Allgemein1/`. If you deploy under a different domain, change
`BASE` in `tools/build.py`, re-run the build, and update `robots.txt`.

To enable GitHub Pages: repository **Settings → Pages → Deploy from branch**, select the branch and `/ (root)`.

## Monetization checklist (owner actions)

1. **Custom domain** (~10–15 €/year): AdSense approval and rankings are much harder on a
   `github.io` subdomain. Buy a domain, point it at the host, change `BASE` in
   `tools/build.py`, rebuild, push.
2. **Google Search Console**: verify the domain, submit `sitemap.xml`. This gets all 53
   URLs indexed and shows which queries bring traffic.
3. **Google AdSense**: apply once the site is on its own domain. After approval, add the
   AdSense snippet to the generator's page template so it ships on every page, plus an
   `ads.txt` in the root.
4. **Bing Webmaster Tools**: same as Search Console, five minutes of work.
5. Optional later: affiliate widgets on the finance calculators (loan/interest) tend to
   out-earn display ads per visitor.

## Development

No build step needed to serve. Open `index.html` in a browser, or serve locally:

```
python3 -m http.server
```
