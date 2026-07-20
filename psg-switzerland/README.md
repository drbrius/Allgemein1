# PSG Sales — Switzerland Expansion Business Plan

Confidential business plan for the market entry of PSG Sales (Petroleum Sales
Group) into Switzerland and the build-up of a Swiss real estate investment and
development platform (distressed acquisitions, renovations and developments;
short-cycle 6–8 month projects and long-cycle ~24 month projects), led by
Robert Ramseier, Dipl. Architekt, as Principal for Switzerland.

- **Deliverable:** `PSG-Sales-Switzerland-Business-Plan.pdf` (A4, 19 pages)
- **Generator:** `generate_plan.py` (Python / ReportLab)

## Regenerating the PDF

The script expects a `fonts/` directory next to it containing these TTFs from
Google Fonts (both families are SIL Open Font License):

- Cormorant Garamond: Regular, Medium, SemiBold, Bold, Medium Italic
- Montserrat: Light, Regular, Medium, SemiBold

named `CormorantGaramondRegular.ttf`, `CormorantGaramondMedium.ttf`,
`CormorantGaramondSemiBold.ttf`, `CormorantGaramondBold.ttf`,
`CormorantGaramondMediumItalic.ttf`, `MontserratLight.ttf`,
`MontserratRegular.ttf`, `MontserratMedium.ttf`, `MontserratSemiBold.ttf`.

```bash
pip install reportlab
python3 generate_plan.py
```

All financial figures in the plan are illustrative planning estimates for
internal discussion — not forecasts, valuations or an offer. Swiss legal and
tax review (in particular Lex Koller) is required before any acquisition.
