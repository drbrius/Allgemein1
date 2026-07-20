# -*- coding: utf-8 -*-
"""Business Plan — Gold Refinery & High-Security Gold Vault, Frauenfeld.
English luxury edition. PDF generator (ReportLab)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, NextPageTemplate
)
from reportlab.graphics.shapes import Drawing, Rect, String, Polygon

# ---------------------------------------------------------------- palette
INK = colors.HexColor("#2B2822")      # warm near-black text
GOLD = colors.HexColor("#A8863B")     # antique gold
GOLD_BRIGHT = colors.HexColor("#C9A959")
CREAM = colors.HexColor("#FBF8F1")    # page tint
DARKBG = colors.HexColor("#171511")   # cover ground
HAIR = colors.HexColor("#D9D0BC")     # hairlines
MUTE = colors.HexColor("#6E675A")     # secondary text
ZEBRA = colors.HexColor("#F4EFE3")

PAGE_W, PAGE_H = A4
OUT = "Business_Plan_Gold_Refinery_Frauenfeld.pdf"

styles = getSampleStyleSheet()

def st(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    styles.add(ParagraphStyle(name, parent=base, **kw))

st("Body", fontName="Times-Roman", fontSize=10.2, leading=14.6, alignment=TA_JUSTIFY,
   textColor=INK, spaceAfter=6)
st("Lead", parent=styles["Body"], fontName="Times-Italic", fontSize=10.6, leading=15.5,
   textColor=MUTE)
st("H1x", fontName="Times-Bold", fontSize=16.5, leading=21, textColor=INK,
   spaceBefore=4, spaceAfter=2)
st("H1n", fontName="Times-Roman", fontSize=9.5, leading=12, textColor=GOLD,
   spaceBefore=10, spaceAfter=1)
st("H2x", fontName="Times-Bold", fontSize=11.5, leading=15, textColor=GOLD,
   spaceBefore=11, spaceAfter=4)
st("Bullet2", parent=styles["Body"], leftIndent=13, bulletIndent=2, spaceAfter=3)
st("Small", fontName="Times-Roman", fontSize=8, leading=11, textColor=MUTE)
st("TblCell", fontName="Helvetica", fontSize=8.2, leading=11, textColor=INK)
st("TblCellB", fontName="Helvetica-Bold", fontSize=8.2, leading=11, textColor=INK)
st("TblHead", fontName="Helvetica-Bold", fontSize=7.6, leading=10, textColor=GOLD)


def spaced(cv, cx, y, text, font, size, track, color, align="c"):
    """Letter-spaced canvas text, centred (or l/r aligned) at cx."""
    w = stringWidth(text, font, size) + track * max(len(text) - 1, 0)
    if align == "c":
        x = cx - w / 2.0
    elif align == "r":
        x = cx - w
    else:
        x = cx
    t = cv.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(track)
    t.setFillColor(color)
    t.textOut(text)
    cv.drawText(t)


def page_bg(cv):
    cv.setFillColor(CREAM)
    cv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)


def header_footer(cv, doc):
    cv.saveState()
    page_bg(cv)
    # header
    spaced(cv, 20*mm, PAGE_H-13.5*mm, "AURUM HELVETIA", "Helvetica-Bold", 7, 1.6, GOLD, "l")
    spaced(cv, PAGE_W-20*mm, PAGE_H-13.5*mm, "CONFIDENTIAL", "Helvetica", 7, 1.6, MUTE, "r")
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(0.5)
    cv.line(20*mm, PAGE_H-16*mm, PAGE_W-20*mm, PAGE_H-16*mm)
    # footer
    cv.setStrokeColor(HAIR)
    cv.setLineWidth(0.5)
    cv.line(20*mm, 14.5*mm, PAGE_W-20*mm, 14.5*mm)
    spaced(cv, PAGE_W/2, 10.5*mm,
           "GOLD REFINERY · HIGH-SECURITY VAULT · FRAUENFELD, SWITZERLAND",
           "Helvetica", 6.3, 1.3, MUTE, "c")
    cv.setFont("Times-Roman", 8.5)
    cv.setFillColor(INK)
    cv.drawRightString(PAGE_W-20*mm, 9.8*mm, f"{doc.page}")
    cv.restoreState()


def cover(cv, doc):
    cv.saveState()
    cv.setFillColor(DARKBG)
    cv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # double frame
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1.1)
    cv.rect(10*mm, 10*mm, PAGE_W-20*mm, PAGE_H-20*mm)
    cv.setLineWidth(0.4)
    cv.rect(12.5*mm, 12.5*mm, PAGE_W-25*mm, PAGE_H-25*mm)
    cx = PAGE_W/2

    spaced(cv, cx, PAGE_H-38*mm, "AURUM  HELVETIA", "Times-Roman", 15, 4.5, GOLD_BRIGHT)
    spaced(cv, cx, PAGE_H-45.5*mm, "ZURICH  ·  FRAUENFELD", "Helvetica", 6.5, 2.5, MUTE)

    # ornament
    def flourish(y):
        cv.setStrokeColor(GOLD)
        cv.setLineWidth(0.5)
        cv.line(cx-32*mm, y, cx-4*mm, y)
        cv.line(cx+4*mm, y, cx+32*mm, y)
        cv.setFillColor(GOLD)
        p = cv.beginPath()
        p.moveTo(cx, y+1.6*mm); p.lineTo(cx+1.6*mm, y)
        p.lineTo(cx, y-1.6*mm); p.lineTo(cx-1.6*mm, y); p.close()
        cv.drawPath(p, stroke=0, fill=1)

    flourish(PAGE_H-58*mm)
    spaced(cv, cx, PAGE_H-72*mm, "BUSINESS  PLAN", "Helvetica", 9, 4.0, colors.HexColor("#EDE6D6"))

    cv.setFillColor(GOLD_BRIGHT)
    cv.setFont("Times-Roman", 27)
    cv.drawCentredString(cx, PAGE_H-88*mm, "Gold Refinery")
    cv.drawCentredString(cx, PAGE_H-101*mm, "High-Security Gold Vault")
    cv.drawCentredString(cx, PAGE_H-114*mm, "Security House")

    spaced(cv, cx, PAGE_H-126*mm,
           "PLOT 61522  ·  FRAUENFELD  ·  CANTON OF THURGAU  ·  SWITZERLAND",
           "Helvetica", 7, 1.8, colors.HexColor("#BFB49B"))
    flourish(PAGE_H-134*mm)

    # gold bar emblem
    y0 = PAGE_H-168*mm
    cv.setFillColor(GOLD)
    cv.setStrokeColor(GOLD_BRIGHT)
    cv.setLineWidth(0.9)
    p = cv.beginPath()
    p.moveTo(cx-26*mm, y0); p.lineTo(cx+26*mm, y0)
    p.lineTo(cx+20.5*mm, y0+12.5*mm); p.lineTo(cx-20.5*mm, y0+12.5*mm); p.close()
    cv.drawPath(p, stroke=1, fill=1)
    spaced(cv, cx, y0+4.9*mm, "999.9  FINE  GOLD", "Helvetica-Bold", 6.5, 1.8, DARKBG)

    # metadata block
    meta = [
        ("PROJECT", "AURUM HELVETIA — Refining & Vaulting Centre, Frauenfeld"),
        ("PROPERTY", "Plot No. 61522 · E-GRID CH607729208032 · 6,434 m²"),
        ("ZONING", "Employment Zone (A) · PiN Overlay · Noise Sensitivity IV"),
        ("LAND ACQUISITION", "CHF 13,000,000 (as offered)"),
        ("TOTAL INVESTMENT", "CHF 70 million (indicative)"),
    ]
    y = 78*mm
    for label, value in meta:
        spaced(cv, cx, y, label, "Helvetica-Bold", 6.2, 1.9, GOLD)
        cv.setFont("Times-Roman", 9.5)
        cv.setFillColor(colors.HexColor("#EDE6D6"))
        cv.drawCentredString(cx, y-4.6*mm, value)
        y -= 11.5*mm
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(0.5)
    cv.line(cx-32*mm, 24.5*mm, cx+32*mm, 24.5*mm)
    spaced(cv, cx, 19.5*mm, "JULY 2026  ·  VERSION 2.0  ·  STRICTLY CONFIDENTIAL",
           "Helvetica", 6.5, 1.9, MUTE)
    cv.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                         topMargin=24*mm, bottomMargin=20*mm,
                         title="Business Plan — Gold Refinery & High-Security Gold Vault, Frauenfeld",
                         author="AURUM HELVETIA AG (in formation)")
        f = Frame(20*mm, 19*mm, PAGE_W-40*mm, PAGE_H-43*mm, id="main")
        fc = Frame(25*mm, 20*mm, PAGE_W-50*mm, PAGE_H-40*mm, id="cover")
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[fc], onPage=cover),
            PageTemplate(id="Std", frames=[f], onPage=header_footer),
        ])


def P(txt, style="Body"):
    return Paragraph(txt, styles[style])

def B(txt):
    return Paragraph(f'<font color="#A8863B">•</font>&nbsp;&nbsp;{txt}', styles["Bullet2"])

def H1(numeral, title):
    out = []
    if numeral:
        out.append(Paragraph(f"SECTION {numeral}", styles["H1n"]))
    else:
        out.append(Spacer(1, 10))
    out.append(Paragraph(title, styles["H1x"]))
    out.append(HRFlowable(width=22*mm, thickness=1.1, color=GOLD, spaceBefore=2, spaceAfter=9,
                          hAlign="LEFT"))
    return out

def tbl(data, widths, aligns=None, bold_last=False):
    rows = []
    for ri, row in enumerate(data):
        cells = []
        for ci, cell in enumerate(row):
            if ri == 0:
                s, txt = "TblHead", str(cell).upper()
            else:
                txt = str(cell)
                s = "TblCellB" if (bold_last and ri == len(data)-1) or txt.startswith("**") else "TblCell"
                txt = txt.lstrip("*")
            cells.append(Paragraph(txt, styles[s]))
        rows.append(cells)
    t = Table(rows, colWidths=widths, repeatRows=1)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, GOLD),
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, GOLD),
        ("LINEBELOW", (0, 1), (-1, -2), 0.35, HAIR),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if bold_last:
        style += [("LINEABOVE", (0, -1), (-1, -1), 0.9, GOLD),
                  ("BACKGROUND", (0, -1), (-1, -1), ZEBRA)]
    if aligns:
        for ci, a in enumerate(aligns):
            if a == "R":
                style.append(("ALIGN", (ci, 0), (ci, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t


def site_plan():
    """Schematic site plan (not to scale) — luxury palette."""
    W, H = 170*mm, 106*mm
    d = Drawing(W, H)
    plot_fill = colors.HexColor("#F1ECDD")
    d.add(Rect(6*mm, 8*mm, 158*mm, 90*mm, strokeColor=INK, strokeWidth=1.2,
               fillColor=plot_fill))
    d.add(String(6*mm, 100*mm, "PLOT 61522  ·  6,434 m²  (schematic, not to scale)",
                 fontName="Helvetica-Bold", fontSize=7.5, fillColor=GOLD))
    # access road
    d.add(Rect(6*mm, 0, 158*mm, 6*mm, strokeColor=None, fillColor=colors.HexColor("#DDD6C6")))
    d.add(String(52*mm, 1.9*mm, "Access road (Langfeld / Ost- / Juchstrasse district)",
                 fontName="Helvetica", fontSize=6, fillColor=MUTE))
    # national-highway building line strip
    d.add(Rect(146*mm, 8*mm, 18*mm, 90*mm, strokeColor=colors.HexColor("#9A5A4A"),
               strokeWidth=0.7, fillColor=colors.HexColor("#EFE0D8")))
    for i, s in enumerate(["Highway", "building", "line", "(107 m,", "keep clear)"]):
        d.add(String(148*mm, (88-3.6*i)*mm, s, fontName="Helvetica", fontSize=5.8,
                     fillColor=colors.HexColor("#9A5A4A")))
    # perimeter
    d.add(Rect(10*mm, 11*mm, 132*mm, 84*mm, strokeColor=GOLD, strokeWidth=1.1,
               fillColor=None, strokeDashArray=[3, 2]))
    d.add(String(12*mm, 91.5*mm, "Security perimeter — 3 m barrier, intrusion detection, video analytics",
                 fontName="Helvetica", fontSize=6, fillColor=GOLD))
    # refinery
    d.add(Rect(16*mm, 46*mm, 66*mm, 42*mm, strokeColor=INK, strokeWidth=1,
               fillColor=colors.HexColor("#E9DDBB")))
    d.add(String(19*mm, 81*mm, "REFINERY", fontName="Helvetica-Bold", fontSize=8, fillColor=INK))
    d.add(String(19*mm, 76.5*mm, "Melting · separation · electrolysis", fontName="Helvetica", fontSize=6, fillColor=INK))
    d.add(String(19*mm, 73*mm, "Assay laboratory · off-gas treatment · casting", fontName="Helvetica", fontSize=6, fillColor=INK))
    d.add(String(19*mm, 69.5*mm, "approx. 1,400 m² footprint, two storeys", fontName="Helvetica", fontSize=6, fillColor=INK))
    # vault
    d.add(Rect(96*mm, 56*mm, 40*mm, 32*mm, strokeColor=INK, strokeWidth=1.6,
               fillColor=colors.HexColor("#DBD3C0")))
    d.add(String(99*mm, 81*mm, "GOLD VAULT", fontName="Helvetica-Bold", fontSize=7.5, fillColor=INK))
    d.add(String(99*mm, 77*mm, "Strongroom to EN 1143-1", fontName="Helvetica", fontSize=6, fillColor=INK))
    d.add(String(99*mm, 73.5*mm, "two levels (one below grade)", fontName="Helvetica", fontSize=6, fillColor=INK))
    d.add(String(99*mm, 70*mm, "approx. 450 m² footprint", fontName="Helvetica", fontSize=6, fillColor=INK))
    # transfer lock
    d.add(Rect(82*mm, 62*mm, 14*mm, 12*mm, strokeColor=INK, strokeWidth=0.8,
               fillColor=colors.HexColor("#EFE8D5")))
    d.add(String(83.2*mm, 67.5*mm, "Value", fontName="Helvetica", fontSize=5.5, fillColor=INK))
    d.add(String(83.2*mm, 64.5*mm, "airlock", fontName="Helvetica", fontSize=5.5, fillColor=INK))
    # logistics
    d.add(Rect(96*mm, 30*mm, 40*mm, 20*mm, strokeColor=INK, strokeWidth=1,
               fillColor=colors.HexColor("#E3E0D2")))
    d.add(String(99*mm, 43*mm, "LOGISTICS / CIT AIRLOCK", fontName="Helvetica-Bold", fontSize=6, fillColor=INK))
    d.add(String(99*mm, 39.5*mm, "enclosed lock for armoured vehicles,", fontName="Helvetica", fontSize=5.5, fillColor=INK))
    d.add(String(99*mm, 36.5*mm, "doré intake / fine-gold dispatch", fontName="Helvetica", fontSize=5.5, fillColor=INK))
    # parking
    d.add(Rect(16*mm, 28*mm, 40*mm, 12*mm, strokeColor=MUTE, strokeWidth=0.7,
               fillColor=colors.HexColor("#EFEBDF")))
    d.add(String(18*mm, 33*mm, "Staff & visitor parking (outer zone)", fontName="Helvetica", fontSize=5.5, fillColor=MUTE))
    # security house
    d.add(Rect(62*mm, 11*mm, 26*mm, 14*mm, strokeColor=INK, strokeWidth=1,
               fillColor=colors.HexColor("#D8DEE3")))
    d.add(String(64*mm, 19.5*mm, "SECURITY HOUSE", fontName="Helvetica-Bold", fontSize=6, fillColor=INK))
    d.add(String(64*mm, 16*mm, "24/7 control room,", fontName="Helvetica", fontSize=5.5, fillColor=INK))
    d.add(String(64*mm, 13*mm, "personnel & vehicle locks", fontName="Helvetica", fontSize=5.5, fillColor=INK))
    # north arrow
    d.add(Polygon([158*mm, 14*mm, 156*mm, 9*mm, 160*mm, 9*mm],
                  strokeColor=INK, fillColor=INK))
    d.add(String(156.6*mm, 15.5*mm, "N", fontName="Helvetica-Bold", fontSize=7, fillColor=INK))
    return d


story = [NextPageTemplate("Std"), Spacer(1, 10), PageBreak()]

# ---------------------------------------------------------------- Contents
story += H1("", "Contents")
toc = [
    ("I", "Executive Summary"), ("II", "Site & Property (PLR Cadastre Analysis)"),
    ("III", "Regulatory Framework"), ("IV", "Architecture & Site Concept"),
    ("V", "Refinery — Technology & Capacity"), ("VI", "Gold Vault — High-Security Storage"),
    ("VII", "Security House & Security Concept"), ("VIII", "Capital Expenditure"),
    ("IX", "Revenue Model & Financial Plan"), ("X", "Organisation & People"),
    ("XI", "Timeline & Project Phases"), ("XII", "Risk Analysis"),
    ("XIII", "Appendix — PLR Cadastre Extract & Disclaimer"),
]
rows = [[Paragraph(f'<font color="#A8863B">{n}</font>', styles["TblCellB"]),
         Paragraph(t, styles["TblCell"])] for n, t in toc]
t = Table(rows, colWidths=[14*mm, 150*mm])
t.setStyle(TableStyle([
    ("LINEBELOW", (0, 0), (-1, -1), 0.35, HAIR),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ("LEFTPADDING", (0, 0), (-1, -1), 2),
]))
story.append(t)
story.append(Spacer(1, 10))
story.append(P("All financial figures are stated in Swiss francs (CHF). The figures presented are indicative "
               "planning values derived from empirical benchmarks; they are to be substantiated in the detailed "
               "design phase through tenders, expert opinions and preliminary rulings by the authorities.", "Small"))
story.append(PageBreak())

# ---------------------------------------------------------------- I Executive Summary
story += H1("I", "Executive Summary")
story.append(P(
    "AURUM HELVETIA AG (in formation) intends to develop an integrated <b>precious-metals refining and "
    "vaulting centre</b> on plot 61522 in Frauenfeld, Canton of Thurgau, Switzerland. The project comprises "
    "three buildings: a <b>gold refinery</b> with a build-out capacity of approximately 100 tonnes of gold "
    "equivalent per annum, a <b>high-security gold vault</b> (strongroom of the highest resistance grades "
    "under EN 1143-1) with a storage capacity of up to 200 tonnes, and a <b>Security House</b> serving as the "
    "permanently manned control room and the sole controlled point of access to the estate."))
story.append(P(
    "The site is exceptionally well suited. The 6,434 m² plot lies entirely within the <b>Employment Zone "
    "(Arbeitszone A)</b> with <b>noise sensitivity level IV</b> — the only category in which heavy industrial "
    "operations are permissible. The plot is free of groundwater protection zones and carries no entry in the "
    "register of contaminated sites. Its immediate proximity to the A7 national motorway (Zurich–Konstanz) "
    "allows fast, predictable valuables transport; Zurich Airport lies approximately 40 minutes away."))
story.append(P("Key parameters", "H2x"))
for x in [
    "Land acquisition: CHF 13.0 million (6,434 m², equivalent to roughly CHF 2,020 per m²).",
    "Total investment: approximately CHF 70 million including land, construction, process plant and security systems.",
    "Financing: 40 per cent equity (CHF 28 million), 60 per cent debt (CHF 42 million).",
    "Revenue target at full operation (plan year 3): approximately CHF 33 million; EBITDA margin of about 50 per cent.",
    "Break-even at pre-tax profit level in the second operating year; payback within eight to ten years.",
    "Business lines: toll refining (doré, recycling, bullion), vaulting and storage, logistics and certification services.",
    "Target accreditations: licences under the Swiss Precious Metals Control Act, SRO/AMLA affiliation, "
    "and LBMA Good Delivery in the medium term.",
]:
    story.append(B(x))
story.append(P(
    "Switzerland refines a substantial share of the world's traded gold, yet existing capacity is concentrated "
    "at a handful of locations (principally Ticino, Valais and Neuchâtel). A modern, compactly planned site in "
    "eastern Switzerland with an integrated high-security vault addresses the growing demand for <b>traceable, "
    "responsibly refined gold</b> and for <b>bank-independent physical storage</b> serving institutional and "
    "private clients alike."))
story.append(PageBreak())

# ---------------------------------------------------------------- II Site
story += H1("II", "Site & Property (PLR Cadastre Analysis)")
story.append(P(
    "This section is based on the official extract from the Cadastre of Public-Law Restrictions on Landownership "
    "(PLR / ÖREB cadastre) dated 20 July 2026, extract number 94e6ede8-6f45-4c08-8312-848c71110089, issued by "
    "the Office for Geoinformation of the Canton of Thurgau."))
story.append(tbl([
    ["Attribute", "Finding", "Assessment for the project"],
    ["Property", "Plot No. 61522, freehold, E-GRID CH607729208032, municipality of Frauenfeld (BFS 8500)", "Unambiguously identified freehold within the building zone"],
    ["Area", "6,434 m²", "Sufficient for refinery, vault, Security House, logistics and reserves"],
    ["Land-use zone", "Employment Zone (A), 100% — overlaid by the Zone for High-Footfall Uses (PiN), 100%", "Industrial-commercial use conforms to zoning; PiN overlay opens options (e.g. client hall, showroom)"],
    ["Noise sensitivity", "Sensitivity level IV, 100%", "Heavy industrial operations permitted — ideal for a melting and refining plant with 24/7 utilities"],
    ["Building-line plan", "Building-line plan in legal force, 100% of plot", "Building placement to be coordinated with the municipality along the building lines"],
    ["National-highway building line", "Building line in force over 107 m", "Strip along the A7 to be kept free of structures, or FEDRO consent required; treated as open space in the site concept"],
    ["Groundwater protection", "No protection zones or areas on the plot", "No elevated permitting risk for chemical and process areas"],
    ["Contaminated sites", "No entry in the register (KbS)", "No identifiable legacy-contamination cost risk (residual risk covered by due diligence)"],
    ["Other topics", "Watercourse space / forest distance: no data or not affected", "No project-relevant constraints apparent"],
], [30*mm, 62*mm, 72*mm]))
story.append(P("Location & market appraisal", "H2x"))
story.append(P(
    "The plot lies in the Langfeld / Ost- / Juchstrasse development district of eastern Frauenfeld, immediately "
    "at the A7 motorway junction. For an operation with daily valuables transport, direct motorway access is a "
    "decisive security and efficiency factor: short, variable routes without forced stops through town centres. "
    "As the cantonal capital, Frauenfeld offers qualified labour, proximity to the cantonal police, and — within "
    "the greater Zurich/Winterthur area — a deep recruiting pool for chemistry, metallurgy, security and "
    "compliance professionals."))
story.append(P(
    "The purchase price of <b>CHF 13.0 million</b> corresponds to roughly <b>CHF 2,020 per m²</b>. For fully "
    "serviced, uncontaminated employment-zone land with motorway access on the Winterthur–Frauenfeld axis this "
    "sits at the upper yet defensible end of the market; the zoning profile (sensitivity level IV, PiN overlay) "
    "and the plot's clean planning status justify a premium over ordinary commercial land."))
story.append(PageBreak())

# ---------------------------------------------------------------- III Regulatory
story += H1("III", "Regulatory Framework")
story.append(P(
    "Operating a gold refinery with a vault is comprehensively regulated in Switzerland. The following licences "
    "and framework conditions determine the project and are managed as the critical path in the timeline "
    "(Section XI):"))
story.append(tbl([
    ["Domain", "Legal basis", "Requirement / measure"],
    ["Precious-metals control", "Precious Metals Control Act (PMCA/EMKG, SR 941.31) and ordinance", "Melter's licence and trade-assayer licence from the Central Office for Precious Metals Control (FOCBS); prerequisite for producing fine gold with official hallmarking"],
    ["Anti-money-laundering", "AMLA (SR 955.0), AMLO", "Professional trading in bank precious metals requires SRO affiliation or FINMA supervision; build-up of a compliance system (KYC, provenance evidence, transaction monitoring)"],
    ["Responsible sourcing", "LBMA Responsible Gold Guidance, OECD Due Diligence Guidance", "Supply-chain due diligence from day one; LBMA Good Delivery accreditation in the medium term (requires inter alia three years of operation, minimum production, assaying competence)"],
    ["Environment / air", "EPA, Ordinance on Air Pollution Control (OAPC/LRV)", "Off-gas scrubbing and filtration for melting and wet-chemical processes; emissions declaration and acceptance measurements"],
    ["Chemicals / major accidents", "ChemA, ChemO, Major Accidents Ordinance (MAO/StFV)", "Storage and handling concept for acids and process gases; staying below or controlling threshold quantities, MAO summary report"],
    ["Water protection", "WPA, WPO", "Wastewater neutralisation with metals recovery; indirect-discharge permit from the canton"],
    ["Occupational safety", "Employment Act, accident-insurance law / Suva (EKAS) directives", "Safety and health-protection concept, explosion protection, PPE, occupational-medical care"],
    ["Building law", "Planning and Building Act of Thurgau, Frauenfeld building code (DBU 65), 1987 zoning plan incl. special building rules", "Ordinary building-permit procedure; early preliminary application; coordination of building lines (municipality, and FEDRO for the national-highway strip)"],
    ["Insurance", "Market standard (Lloyd's et al.)", "All-risk / specie cover for storage and transport; the insurers' technical acceptance of the strongroom is a condition of cover"],
], [30*mm, 52*mm, 82*mm]))
story.append(P(
    "<b>Assessment:</b> none of these requirements stands in the way of the project at the chosen site. Zoning "
    "conformity and sensitivity level IV materially reduce objection risk; the critical timelines are the "
    "building-permit procedure (including FEDRO coordination) and the PMCA licences."))
story.append(PageBreak())

# ---------------------------------------------------------------- IV Architecture
story += H1("IV", "Architecture & Site Concept")
story.append(P(
    "The site concept follows the principle of <b>security through structure</b>: a single controlled access "
    "through the Security House; strictly separated flows for staff, visitors, valuables transport and "
    "materials; security zones layered from the outside in; and the vault as the innermost, fully protected "
    "core with no façade facing public space. The 107-metre national-highway building-line strip remains free "
    "of structures and is used as landscaped retention space."))
story.append(Spacer(1, 4))
story.append(site_plan())
story.append(PageBreak())
story.append(P("Schedule of areas (principal usable areas, indicative)", "H2x"))
story.append(tbl([
    ["Building", "Use", "Area (m²)"],
    ["Refinery (two storeys, c. 1,400 m² footprint)", "Melt shop and casting, wet-chemical separation, electrolysis, sampling and assay laboratory, off-gas and wastewater plant, workshop, changing rooms, offices, utilities", "2,600 GFA"],
    ["Gold vault (two levels, one below grade)", "Strongroom chambers with client segregation, airlocks, counting and inspection rooms, safe-deposit section (option), autonomous utilities", "900 GFA"],
    ["Security House (two storeys)", "24/7 control room, personnel and vehicle locks, reception and identification, security-staff facilities, redundant server room", "350 GFA"],
    ["Logistics / CIT airlock", "Enclosed lock for armoured vehicles, covered handling, direct link to refinery and vault", "300 GFA"],
    ["External works", "Manoeuvring and parking areas, perimeter zone, landscaped retention areas (incl. building-line strip)", "c. 3,800"],
], [50*mm, 84*mm, 30*mm], aligns=[None, None, "R"]))
story.append(P("Architectural principles", "H2x"))
for x in [
    "Compact, sparsely fenestrated volumes in fair-faced concrete with a suspended metal façade; daylight "
    "through shed-type roof lights in non-critical areas.",
    "The refinery as a flexible industrial hall (8 × 8 m grid) with crane runway and a heavily serviced "
    "utilities spine; expansion reserve for a second electrolysis line built in.",
    "The vault in massive construction (special reinforced-concrete mix with aggregates of enhanced "
    "breakthrough resistance), fully earth-covered lower level, largely blind façades; externally not "
    "recognisable as a bullion store.",
    "The Security House as the estate's public face: representative yet defensible — reception, "
    "identification and single-person interlocks in one building.",
    "Sustainability: photovoltaics across all roofs (target above 500 kWp), furnace waste-heat recovery "
    "for building heating, rainwater retention within the building-line strip; Minergie standard targeted "
    "for the administrative areas.",
]:
    story.append(B(x))
story.append(PageBreak())

# ---------------------------------------------------------------- V Refinery
story += H1("V", "Refinery — Technology & Capacity")
story.append(P(
    "The refinery is designed as a modern toll refinery for gold and silver, focused on three input streams: "
    "doré bars from mine production of demonstrably responsible origin; recycling material (old gold, "
    "production scrap, electronic-scrap concentrates); and the re-melting and upgrading of bullion "
    "(Good Delivery conversion, format changes)."))
story.append(P("Process chain", "H2x"))
story.append(tbl([
    ["Stage", "Method", "Purpose"],
    ["Intake & sampling", "Goods receipt in the CIT airlock, weighing, drill/melt sampling, X-ray fluorescence and fire assay in the in-house laboratory", "Binding determination of content as settlement basis"],
    ["Melting & homogenising", "Induction furnaces with enclosed extraction", "Homogeneous feedstock, sampling, removal of impurities"],
    ["Pre-refining", "Miller process (in-melt chlorination) for high throughput", "Rapid upgrade to c. 99.5% Au; silver and base metals report to the slag/chloride phase"],
    ["Fine refining", "Wohlwill electrolysis; complementary wet-chemical separation (aqua regia) for complex feeds", "Fine gold 999.9; recovery of silver and platinum-group metals from anode slimes"],
    ["Casting & minting", "Bar casting (1 kg – 12.5 kg), minting line for small bars of 1 g – 100 g", "Marketable end products with serial number, certificate and official hallmark"],
    ["Environmental stage", "Multi-stage gas scrubbing (chlorine/NOx), filtration, wastewater neutralisation with metals recovery", "Compliance with air and water ordinances; recovery of value metals from all side streams"],
], [30*mm, 72*mm, 62*mm]))
story.append(P("Capacity & ramp-up", "H2x"))
for x in [
    "Technical build-out capacity of approximately 100 tonnes of gold equivalent per annum on a two-shift "
    "basis; expandable to 150 tonnes via a third shift and a second electrolysis line.",
    "Ramp-up path: around 15 tonnes in plan year 1 (commissioning, trial runs, first clients), 40 tonnes "
    "in year 2, 60 tonnes in year 3, thereafter 70–80 tonnes.",
    "The assay laboratory (fire assay and spectrometry) operates as its own profit centre for third-party "
    "and umpire analyses.",
    "Quality objective: fine gold 999.9 with seamless batch traceability from input lot to bar — a central "
    "selling proposition towards banks and wholesale clients.",
]:
    story.append(B(x))
story.append(P(
    "<b>Security and environmental advantage of the site:</b> noise sensitivity level IV permits continuous "
    "operation of furnaces and ventilation; the absence of groundwater-protection overlays considerably "
    "simplifies permitting of the wet-chemical processes. Major-accident prevention (chlorine for the Miller "
    "process, acid storage) is addressed through enclosed systems, gas-warning installations and separate, "
    "bunded storage rooms with neutralisation reserves."))
story.append(PageBreak())

# ---------------------------------------------------------------- VI Vault
story += H1("VI", "Gold Vault — High-Security Storage")
story.append(P(
    "The vault is conceived as a profit centre in its own right: physical storage for banks, asset managers, "
    "family offices, bullion dealers and — within the scope of the PiN zoning overlay — selected private "
    "clients. Designation of the facility as a bonded warehouse (open customs warehouse) will be examined in "
    "order to serve international clients."))
story.append(P("Structural & technical design", "H2x"))
for x in [
    "Strongroom to EN 1143-1, targeting the highest insurable resistance grades on the market (grades X to "
    "XIII with EX and CD supplements against explosives and core-drill attack); final classification to be "
    "agreed with the specie insurers.",
    "Two vault levels: the fully earth-covered basement as the main store with pallet logistics for large "
    "bars; the ground-floor level for client segregates, counting and inspection rooms and an optional "
    "safe-deposit section.",
    "Monolithic reinforced-concrete envelope of enhanced breakthrough resistance, externally discreet — no "
    "visible indication of a bullion store; access exclusively through airlocks from within the estate.",
    "Autonomous services: independent power, cooling and communications, standby generator, redundant "
    "alarm-transmission paths.",
    "Capacity: up to 200 tonnes of gold depending on configuration, plus silver and pallet storage in the "
    "logistics wing.",
]:
    story.append(B(x))
story.append(P("Operating model & revenues", "H2x"))
story.append(tbl([
    ["Service", "Target clients", "Pricing model (indicative)"],
    ["Segregated (allocated) storage", "Banks, funds, family offices", "0.10 – 0.20% p.a. of stored value, audit access included"],
    ["Pooled bar storage", "Dealers, refining clients", "0.08 – 0.12% p.a., combinable with refining contracts"],
    ["Safe-deposit boxes (option, PiN-conforming)", "Private clients, SMEs", "Fixed prices by box size, access via the Security House"],
    ["Handling & logistics", "All segments", "In/out fees, counting and inspection, CIT handling"],
], [46*mm, 48*mm, 70*mm]))
story.append(P(
    "Combining refinery and vault on one site is a structural competitive advantage: freshly refined fine gold "
    "can be placed into storage without external transport (“mint to vault”), lowering insurance and transport "
    "cost and enabling a closed chain of security and evidence from melt lot to storage position."))
story.append(PageBreak())

# ---------------------------------------------------------------- VII Security
story += H1("VII", "Security House & Security Concept")
story.append(P(
    "The security concept follows the internationally established <b>layered-defence (“onion-skin”) principle</b> "
    "with five graduated zones and a consistent four-eyes organisation. It is coordinated with the Thurgau "
    "cantonal police, the insurers and an accredited certification body, and is audited periodically."))
story.append(tbl([
    ["Zone", "Scope", "Measures (extract)"],
    ["0 — Surroundings", "Public space, approach", "Discreet external appearance, traffic-calmed approach, long-range video analytics, licence-plate recognition at the access"],
    ["1 — Perimeter", "Property boundary", "3 m fence/wall system with anti-climb and anti-dig protection, detection sensors (fence, ground, thermal), certified vehicle-restraint systems (bollards/barriers) at the entrance"],
    ["2 — Estate", "Outdoor areas within the perimeter", "Gap-free video coverage with analytics, lighting concept, guided routing with single-person interlocks, drone detection"],
    ["3 — Buildings", "Refinery, logistics, Security House", "Burglar-resistant envelope (resistance classes RC5/RC6 at critical openings), personnel and vehicle locks, multi-factor access (badge + biometrics + PIN), intruder alarm to EN 50131 grade 4"],
    ["4 — Core", "Strongroom, fine-gold store", "Vault doors and chambers to EN 1143-1 (highest grades), time-delayed multi-person opening, seismic and structure-borne-sound detection, separate alarm loops, access only under the four-eyes rule with logged release by the control room"],
], [26*mm, 40*mm, 98*mm]))
story.append(P("The Security House — heart of the operation", "H2x"))
for x in [
    "Permanently manned control room (24/7, minimum two operators) with redundant connection to a "
    "certified alarm-receiving centre and the cantonal police.",
    "Sole point of access for people and vehicles: identification, visitor management, single-person "
    "interlocks, weapons and metal detection, separated waiting areas.",
    "Command of all valuables transports: notification, slot allocation, route and window coordination "
    "with the CIT partners; no transport without a confirmed slot.",
    "Crisis and emergency organisation: intervention concept agreed with the police, sabotage and fire "
    "scenarios, business-continuity plan, annual exercises.",
    "Data-protection-compliant video archiving (revised Swiss DPA), tamper-proof logging of access and "
    "events.",
]:
    story.append(B(x))
story.append(P(
    "<b>Personnel security:</b> all employees undergo background screening (debt-enforcement and criminal "
    "records, references); security-critical functions are re-screened periodically. Segregation of duties "
    "(production / vault / compliance / security) and rotating responsibilities reduce insider risk. Details of "
    "resistance times, intervention times and alarm philosophy are deliberately confined to the confidential "
    "security specification."))
story.append(PageBreak())

# ---------------------------------------------------------------- VIII Capex
story += H1("VIII", "Capital Expenditure")
story.append(P(
    "The investment estimate is based on cost benchmarks of comparable industrial and high-security buildings "
    "(accuracy ± 20 per cent, price basis 2026) and is to be verified through contractor tenders in the "
    "preliminary-design phase."))
story.append(tbl([
    ["Item", "Assumption / basis", "CHF m"],
    ["Land acquisition, plot 61522", "6,434 m² as offered", "13.00"],
    ["Acquisition costs", "Transfer tax, notary, land register (c. 2.3%)", "0.30"],
    ["Refinery building", "2,600 m² GFA, heavily serviced industrial build, c. CHF 4,800/m²", "12.50"],
    ["Gold vault", "900 m² GFA specialist construction incl. strongrooms, c. CHF 12,800/m²", "11.50"],
    ["Security House", "350 m² GFA incl. interlock systems", "1.80"],
    ["Logistics/CIT airlock, externals, perimeter", "Vehicle lock, fence and detection systems, bollards, manoeuvring areas", "2.60"],
    ["Process plant & furnaces", "Induction furnaces, Miller line, Wohlwill electrolysis, separation, casting/minting, off-gas and wastewater plant", "14.00"],
    ["Security systems", "Intruder alarm grade 4, video/analytics, access/biometrics, control-room technology, redundancies", "4.20"],
    ["Laboratory & operating equipment", "Assaying (fire assay, spectrometry), IT/ERP, track-and-trace", "2.20"],
    ["Design, permits, professional fees", "c. 12% of construction and plant cost", "3.40"],
    ["Contingency", "c. 7% reserve", "4.50"],
    ["**Total investment", "", "**70.00"],
], [54*mm, 84*mm, 22*mm], aligns=[None, None, "R"], bold_last=True))
story.append(P("Financing", "H2x"))
story.append(tbl([
    ["Source", "Share", "CHF m", "Notes"],
    ["Equity (founders, anchor investors)", "40%", "28.0", "Subscribed in two tranches (acquisition/design, construction)"],
    ["Mortgage / investment loan", "50%", "35.0", "Secured on land and buildings; interest assumption 2.8%"],
    ["Supplier / lease financing of plant", "10%", "7.0", "Furnace and electrolysis technology"],
], [58*mm, 16*mm, 20*mm, 62*mm], aligns=[None, "R", "R", None]))
story.append(P(
    "The land acquisition (CHF 13.0 million) is funded entirely from the first equity tranche so that the "
    "unencumbered plot is available as collateral for the construction phase."))
story.append(PageBreak())

# ---------------------------------------------------------------- IX Financial plan
story += H1("IX", "Revenue Model & Financial Plan")
story.append(P("Revenue streams at full operation (plan year 3)", "H2x"))
story.append(tbl([
    ["Revenue stream", "Volume assumptions", "CHF m"],
    ["Toll refining, gold & silver", "60 t throughput × avg. CHF 0.40/g refining income", "24.0"],
    ["Recycling / separation margin", "Additional income from complex feeds and by-metals (Ag, PGM)", "3.5"],
    ["Vaulting / storage", "Avg. 40 t stored × avg. 0.12% p.a. on stored value (assumption CHF 90/g)", "4.3"],
    ["Ancillary income", "Analytics, certificates, logistics/handling, minting orders", "1.2"],
    ["**Total revenue, plan year 3", "", "**33.0"],
], [54*mm, 84*mm, 22*mm], aligns=[None, None, "R"], bold_last=True))
story.append(P("Five-year plan (indicative, CHF m)", "H2x"))
story.append(tbl([
    ["Item", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
    ["Refining throughput (t)", "15", "40", "60", "70", "78"],
    ["Revenue", "8.0", "19.5", "33.0", "38.5", "42.0"],
    ["Operating costs (incl. staff, energy, insurance)", "9.5", "13.7", "16.5", "18.7", "20.1"],
    ["EBITDA", "-1.5", "5.8", "16.5", "19.8", "21.9"],
    ["Depreciation", "3.3", "3.5", "3.5", "3.5", "3.5"],
    ["Finance cost", "1.2", "1.2", "1.2", "1.1", "1.0"],
    ["**Profit before tax (EBT)", "**-6.0", "**1.1", "**11.8", "**15.2", "**17.4"],
], [65*mm, 19*mm, 19*mm, 19*mm, 19*mm, 19*mm],
    aligns=[None, "R", "R", "R", "R", "R"]))
story.append(P("Key planning assumptions", "H2x"))
for x in [
    "Conservative gold-price assumption of CHF 90,000 per kg for valuing stored holdings; the revenue "
    "model is predominantly volume-driven rather than price-driven (fee business, no proprietary trading "
    "with open positions).",
    "Headcount growth from 28 full-time equivalents in year 1 to 58 in year 3; average full cost of "
    "CHF 120,000 per position.",
    "Insurance premiums (specie / all-risk) calculated at 0.9 – 1.4 per cent of average stored value, "
    "declining with claims history and certification progress.",
    "Working capital remains modest, as client material is refined and stored in third-party ownership "
    "(toll processing); metal accounts are squared daily.",
    "Combined cantonal and federal tax rate of roughly 13.5 per cent in Thurgau — attractive by "
    "international comparison.",
    "Break-even at EBT level in year 2; cumulative free cash flow positive from year 5; project payback "
    "including land within eight to ten years.",
]:
    story.append(B(x))
story.append(PageBreak())

# ---------------------------------------------------------------- X Organisation
story += H1("X", "Organisation & People")
story.append(tbl([
    ["Unit", "Responsibilities", "FTE Yr 1", "FTE Yr 3"],
    ["Executive board & staff", "CEO, CFO, legal/compliance (AML desk), HR", "4", "6"],
    ["Refinery production", "Melt shop, separation, electrolysis, casting (two-shift)", "10", "22"],
    ["Laboratory / quality", "Assaying, QA, certification, track-and-trace", "3", "6"],
    ["Security / control room", "24/7 control room, interlock operation, CIT coordination", "8", "14"],
    ["Vault / logistics", "In/out storage, client segregates, inventories", "2", "6"],
    ["Sales & client management", "Mining, banking and recycling clients, vaulting sales", "1", "4"],
    ["**Total", "", "**28", "**58"],
], [44*mm, 80*mm, 18*mm, 18*mm], aligns=[None, None, "R", "R"], bold_last=True))
story.append(P(
    "Key hires are the refinery operations manager (metallurgy, experience at a Good Delivery refinery), the "
    "head of security (police, armed-forces or CIT-industry background) and the AML compliance officer. For "
    "the 24/7 control room a blended model of in-house staff and a contractually bound, certified security "
    "provider is under review; authority over alarm and release processes remains in-house in every case."))
story.append(P("Legal form & governance", "H2x"))
for x in [
    "Swiss stock corporation (AG) domiciled in Frauenfeld; board of directors with independent members "
    "covering finance, law and security.",
    "Internal control system from day one; annual external audits of finance, AML, security and "
    "environment.",
    "Four-eyes principle across all value-relevant processes; no single-person access to core zones.",
]:
    story.append(B(x))
story.append(Spacer(1, 8))
story += H1("XI", "Timeline & Project Phases")
story.append(tbl([
    ["Phase", "Period", "Milestones"],
    ["0 — Securing & due diligence", "Q3 – Q4 2026", "Purchase deed for plot 61522, technical and legal due diligence, preliminary planning application, incorporation, first equity tranche"],
    ["1 — Design & permitting", "Q1 2027 – Q2 2028", "Preliminary and detailed design (SIA phases 31/32), environmental and major-accident dossiers, building application, FEDRO building-line coordination, PMCA licence applications, insurers' acceptance concept"],
    ["2 — Construction", "Q3 2028 – Q4 2029", "Excavation and shell (vault first), fit-out, installation of process and security systems, factory acceptance tests"],
    ["3 — Commissioning", "Q1 – Q3 2030", "Cold and hot commissioning, emissions measurements, melter's and trade-assayer licences active, insurers' vault acceptance, first client lots"],
    ["4 — Ramp-up & accreditation", "from Q4 2030", "Two-shift operation, SRO audit, building the LBMA track record (Good Delivery targeted after three operating years)"],
], [38*mm, 30*mm, 96*mm]))
story.append(PageBreak())

# ---------------------------------------------------------------- XII Risks
story += H1("XII", "Risk Analysis")
story.append(tbl([
    ["Risk", "P*", "I*", "Mitigation"],
    ["Building-permit delay / objections", "medium", "medium", "Zoning conformity (Employment Zone, level IV) minimises grounds for objection; early preliminary application; transparent communication with city and neighbours"],
    ["Conditions from the highway building line (FEDRO)", "medium", "low", "Site concept keeps the strip clear; early alignment with FEDRO"],
    ["PMCA / AML licences delayed", "low", "high", "Experienced compliance counsel, complete applications, screened key personnel recruited before filing"],
    ["Construction cost overrun", "medium", "medium", "7% contingency, general-contractor award with cost ceiling, phased fit-out"],
    ["Market risk: refining margins under pressure", "medium", "medium", "Differentiation through traceability, eastern-Switzerland location advantage, combined refining-plus-storage offer; multi-year anchor contracts"],
    ["Security incident (robbery, burglary, insider)", "low", "very high", "Layered zone concept, highest vault grades, four-eyes principle, personnel screening, insurance cover, intervention agreement with the cantonal police"],
    ["Environmental / major-accident event", "low", "high", "Enclosed processes, gas-warning and neutralisation systems, MAO summary report, regular drills"],
    ["Supply-chain reputation risk", "medium", "high", "OECD-conformant due diligence, acceptance of audited provenance only, external responsible-sourcing audit from year one"],
    ["Interest-rate / financing risk", "medium", "medium", "Long-term fixed rates, staggered equity tranches, covenant headroom"],
], [44*mm, 15*mm, 16*mm, 89*mm]))
story.append(P("*P = probability of occurrence, I = impact", "Small"))
story.append(P(
    "Overall assessment: the project carries a risk profile typical of high-security industrial ventures, yet "
    "one that is well controllable through the choice of site, zoning conformity and a rigorous security "
    "architecture. No single identified risk is capable of preventing the project."))
story.append(Spacer(1, 8))
story += H1("XIII", "Appendix — PLR Cadastre Extract & Disclaimer")
story.append(tbl([
    ["PLR cadastre extract (official)", "Entry"],
    ["Extract number / date", "94e6ede8-6f45-4c08-8312-848c71110089 / 20 July 2026"],
    ["Property", "Plot No. 61522, freehold, municipality of Frauenfeld (BFS 8500)"],
    ["E-GRID", "CH607729208032"],
    ["Area", "6,434 m² (official cadastral survey as at 16 July 2026)"],
    ["PLR topics affecting the plot", "Land-use planning: Employment Zone (A) 100%, Zone for High-Footfall Uses (PiN) 100% · building-line plan 100% · national-highway building lines: line in force, 107 m · noise sensitivity level IV, 100%"],
    ["Not affected (selection)", "Groundwater protection zones and areas, register of contaminated sites, special design plans, planning zones, forest topics"],
    ["Principal legal bases", "Spatial Planning Act (SR 700), Thurgau Planning and Building Act and ordinance (RB 700/700.1), Frauenfeld building code DBU 65, 1987 zoning plan (No. 548) incl. special building rules, Langfeld/Ost-/Juchstrasse zoning plan (No. 88, 2009), National Highways Act and ordinance, Noise Abatement Ordinance"],
    ["Responsible cadastre office", "Office for Geoinformation, Canton of Thurgau, Staubeggstrasse 3, 8510 Frauenfeld"],
], [52*mm, 112*mm]))
story.append(Spacer(1, 6))
story.append(P(
    "<b>Disclaimer:</b> this business plan is a project study intended solely for internal decision-making and "
    "for discussions with qualified investors, banks, authorities and insurers. All cost, revenue and schedule "
    "figures are indicative planning values (accuracy ± 20 per cent) and replace neither tenders nor expert "
    "opinions nor official rulings. The PLR cadastre extract is of purely informative character and creates no "
    "rights or obligations; the legally enacted documents prevail. Statements on security measures are "
    "deliberately generic; operationally relevant details are confined to the confidential security "
    "specification.", "Small"))

doc = Doc(OUT)
doc.build(story)
print("OK:", OUT)
