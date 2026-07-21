#!/usr/bin/env python3
"""CalcMate static site generator.

Usage: python3 tools/build.py

Regenerates the per-language hub pages (de/, en/, fr/, it/), one page per
calculator per language, and sitemap.xml. All translatable content lives in
tools/content_<lang>.py; the shared page structure lives here. The generated
pages are plain static HTML — the site itself still has no build dependency,
this script only needs to be re-run when content changes.
"""

import importlib
import json
import os
import sys

BASE = "https://drbrius.github.io/Allgemein1"
LANGS = ["de", "en", "fr", "it"]
LANG_NAMES = {"de": "Deutsch", "en": "English", "fr": "Français", "it": "Italiano"}
LASTMOD = "2026-07-21"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORDER = [
    "calculator", "percentage", "vat", "discount", "rule3", "slope",
    "bmi", "interest", "loan", "fuel", "tip", "date",
]

ICONS = {
    "calculator": "🧮", "percentage": "％", "vat": "🧾", "discount": "🏷️",
    "rule3": "⚖️", "slope": "📐", "bmi": "❤️", "interest": "📈",
    "loan": "🏦", "fuel": "⛽", "tip": "🪙", "date": "📅",
}

RELATED = {
    "calculator": ["percentage", "rule3", "vat"],
    "percentage": ["discount", "vat", "rule3"],
    "vat": ["percentage", "discount", "loan"],
    "discount": ["percentage", "vat", "tip"],
    "rule3": ["percentage", "fuel", "calculator"],
    "slope": ["rule3", "percentage", "calculator"],
    "bmi": ["date", "percentage", "calculator"],
    "interest": ["loan", "percentage", "vat"],
    "loan": ["interest", "vat", "percentage"],
    "fuel": ["rule3", "percentage", "discount"],
    "tip": ["percentage", "discount", "calculator"],
    "date": ["calculator", "rule3", "bmi"],
}

sys.path.insert(0, os.path.join(ROOT, "tools"))
MODULES = {lang: importlib.import_module("content_" + lang) for lang in LANGS}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def url(lang, key=None):
    if key is None:
        return "%s/%s/" % (BASE, lang)
    return "%s/%s/%s/" % (BASE, lang, MODULES[lang].CALCS[key]["slug"])


def ld(data):
    return ('  <script type="application/ld+json">\n%s\n  </script>'
            % json.dumps(data, ensure_ascii=False, indent=2))


def faq_ld(faqs):
    return ld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    })


def hreflang_links(key=None):
    lines = []
    for lang in LANGS:
        lines.append('  <link rel="alternate" hreflang="%s" href="%s">' % (lang, url(lang, key)))
    xdef = (BASE + "/") if key is None else url("en", key)
    lines.append('  <link rel="alternate" hreflang="x-default" href="%s">' % xdef)
    return "\n".join(lines)


def head(lang, key, title, desc, canon, assets, extra_ld):
    og_title = title.replace("&amp;", "&")
    parts = [
        "<!DOCTYPE html>",
        '<html lang="%s">' % lang,
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        "  <title>%s</title>" % title,
        '  <meta name="description" content="%s">' % esc(desc),
        '  <link rel="canonical" href="%s">' % canon,
        hreflang_links(key),
        '  <meta property="og:type" content="website">',
        '  <meta property="og:title" content="%s">' % esc(og_title),
        '  <meta property="og:description" content="%s">' % esc(desc),
        '  <meta property="og:url" content="%s">' % canon,
        '  <meta property="og:locale" content="%s">' % lang,
        '  <meta name="theme-color" content="#4f6df5">',
        '  <link rel="icon" href="%s/favicon.svg" type="image/svg+xml">' % assets,
        '  <link rel="stylesheet" href="%s/style.css">' % assets,
    ]
    parts.extend(extra_ld)
    parts.append("</head>")
    return "\n".join(parts)


def header(lang, key):
    logo_href = "./" if key is None else "../"
    items = []
    for l in LANGS:
        if l == lang:
            items.append('        <li><a href="./" hreflang="%s" aria-current="true">%s</a></li>'
                         % (l, l.upper()))
        else:
            href = ("../%s/" % l) if key is None else ("../../%s/%s/" % (l, MODULES[l].CALCS[key]["slug"]))
            items.append('        <li><a href="%s" hreflang="%s" lang="%s">%s</a></li>'
                         % (href, l, l, l.upper()))
    return """<body>
  <header class="site-header">
    <div class="wrap">
      <a class="logo" href="%s"><span class="logo-mark">∑</span>CalcMate</a>
      <ul class="lang-switch">
%s
      </ul>
    </div>
  </header>""" % (logo_href, "\n".join(items))


def footer(lang, key, nav_label):
    site = MODULES[lang].SITE
    links = []
    for l in LANGS:
        if l == lang:
            links.append('        <a href="./" hreflang="%s" aria-current="true">%s</a>'
                         % (l, LANG_NAMES[l]))
        else:
            href = ("../%s/" % l) if key is None else ("../../%s/%s/" % (l, MODULES[l].CALCS[key]["slug"]))
            links.append('        <a href="%s" hreflang="%s" lang="%s">%s</a>'
                         % (href, l, l, LANG_NAMES[l]))
    return """  <footer class="site-footer">
    <div class="wrap">
      <nav aria-label="%s">
%s
      </nav>
      <p>%s</p>
    </div>
  </footer>""" % (nav_label, "\n".join(links), site["footer"])


def i18n_script(lang, assets):
    site = MODULES[lang].SITE
    return """  <script>
    window.CALC_I18N = %s;
  </script>
  <script src="%s/app.js"></script>
</body>
</html>""" % (json.dumps(site["i18n"], ensure_ascii=False), assets)


def faq_section(site, faqs):
    out = ['    <section class="faq" aria-labelledby="faq-title">',
           '      <h2 id="faq-title">%s</h2>' % site["faq_title"]]
    for q, a in faqs:
        out.append("      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>"
                   % (q, a))
    out.append("    </section>")
    return "\n".join(out)


def hub_page(lang):
    m = MODULES[lang]
    site = m.SITE
    canon = url(lang)

    app = ld({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": site["app_name"],
        "url": canon,
        "applicationCategory": "UtilityApplication",
        "operatingSystem": "Any",
        "inLanguage": lang,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": site["app_desc"],
    })
    items = ld({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": m.CALCS[key]["name"], "url": url(lang, key)}
            for i, key in enumerate(ORDER)
        ],
    })

    cards = []
    for key in ORDER:
        c = m.CALCS[key]
        cards.append(
            '      <a class="calc-card" href="%s/">\n'
            '        <span class="icon" aria-hidden="true">%s</span>\n'
            "        <h2>%s</h2>\n"
            "        <p>%s</p>\n"
            "      </a>" % (c["slug"], ICONS[key], c["name"], c["card"]))

    html = "\n".join([
        head(lang, None, site["title"], site["desc"], canon, "../assets",
             [app, items, faq_ld(site["hub_faqs"])]),
        header(lang, None),
        "",
        '  <main class="wrap">',
        '    <section class="hero">',
        "      <h1>%s</h1>" % site["hub_h1"],
        "      <p>%s</p>" % site["hub_intro"],
        "    </section>",
        "",
        '    <div class="card-grid">',
        "\n".join(cards),
        "    </div>",
        "",
        faq_section(site, site["hub_faqs"]),
        "  </main>",
        "",
        footer(lang, None, site["lang_nav_label"]),
        "",
        i18n_script(lang, "../assets"),
    ])
    return html


def calc_page(lang, key):
    m = MODULES[lang]
    site = m.SITE
    c = m.CALCS[key]
    canon = url(lang, key)

    breadcrumb = ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": site["home"], "item": url(lang)},
            {"@type": "ListItem", "position": 2, "name": c["name"], "item": canon},
        ],
    })
    app = ld({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "%s – CalcMate" % c["name"],
        "url": canon,
        "applicationCategory": "UtilityApplication",
        "operatingSystem": "Any",
        "inLanguage": lang,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": c["desc"],
    })

    chips = []
    for rel in RELATED[key]:
        r = m.CALCS[rel]
        chips.append('        <a href="../%s/">%s %s</a>' % (r["slug"], ICONS[rel], r["name"]))

    form = "\n".join("      " + line if line else "" for line in c["form"].strip().split("\n"))
    seo = "\n".join("      " + line if line else "" for line in c["seo"].strip().split("\n"))

    html = "\n".join([
        head(lang, key, c["title"], c["desc"], canon, "../../assets",
             [breadcrumb, app, faq_ld(c["faqs"])]),
        header(lang, key),
        "",
        '  <main class="wrap">',
        '    <nav class="breadcrumb" aria-label="Breadcrumb">',
        '      <a href="../">%s</a> › <span>%s</span>' % (site["home"], c["name"]),
        "    </nav>",
        "",
        '    <section class="calc-section">',
        '      <h1><span class="icon" aria-hidden="true">%s</span>%s</h1>' % (ICONS[key], c["h1"]),
        "      <p>%s</p>" % c["intro"],
        form,
        "    </section>",
        "",
        '    <article class="seo-text">',
        seo,
        "    </article>",
        "",
        faq_section(site, c["faqs"]),
        "",
        '    <section class="related">',
        "      <h2>%s</h2>" % site["related_title"],
        '      <nav class="calc-nav" aria-label="%s">' % site["related_title"],
        "\n".join(chips),
        "      </nav>",
        "    </section>",
        "  </main>",
        "",
        footer(lang, key, site["lang_nav_label"]),
        "",
        i18n_script(lang, "../../assets"),
    ])
    return html


def sitemap():
    def entry(loc, alternates):
        lines = ["  <url>", "    <loc>%s</loc>" % loc, "    <lastmod>%s</lastmod>" % LASTMOD]
        for hl, href in alternates:
            lines.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (hl, href))
        lines.append("  </url>")
        return "\n".join(lines)

    hub_alts = [(l, url(l)) for l in LANGS] + [("x-default", BASE + "/")]
    entries = [entry(BASE + "/", hub_alts)]
    for lang in LANGS:
        entries.append(entry(url(lang), hub_alts))
    for key in ORDER:
        alts = [(l, url(l, key)) for l in LANGS] + [("x-default", url("en", key))]
        for lang in LANGS:
            entries.append(entry(url(lang, key), alts))

    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        "\n".join(entries),
        "</urlset>",
    ]) + "\n"


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content if content.endswith("\n") else content + "\n")
    print("wrote %s" % path)


def main():
    for lang in LANGS:
        write("%s/index.html" % lang, hub_page(lang))
        for key in ORDER:
            write("%s/%s/index.html" % (lang, MODULES[lang].CALCS[key]["slug"]), calc_page(lang, key))
    write("sitemap.xml", sitemap())


if __name__ == "__main__":
    main()
