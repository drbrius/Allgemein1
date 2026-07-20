#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSG Sales — Switzerland Expansion & Real Estate Investment Platform
Confidential Business Plan — luxury-styled PDF generator (ReportLab).
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, PageBreak, NextPageTemplate, KeepTogether, Flowable,
    HRFlowable,
)

# ----------------------------------------------------------------------------
# Assets & palette
# ----------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.environ.get("PSG_OUT", os.path.join(HERE, "PSG-Sales-Switzerland-Business-Plan.pdf"))

pdfmetrics.registerFont(TTFont("Cormorant", os.path.join(FONTS, "CormorantGaramondRegular.ttf")))
pdfmetrics.registerFont(TTFont("Cormorant-Md", os.path.join(FONTS, "CormorantGaramondMedium.ttf")))
pdfmetrics.registerFont(TTFont("Cormorant-Sb", os.path.join(FONTS, "CormorantGaramondSemiBold.ttf")))
pdfmetrics.registerFont(TTFont("Cormorant-Bd", os.path.join(FONTS, "CormorantGaramondBold.ttf")))
pdfmetrics.registerFont(TTFont("Cormorant-It", os.path.join(FONTS, "CormorantGaramondMediumItalic.ttf")))
pdfmetrics.registerFont(TTFont("Mont-Lt", os.path.join(FONTS, "MontserratLight.ttf")))
pdfmetrics.registerFont(TTFont("Mont", os.path.join(FONTS, "MontserratRegular.ttf")))
pdfmetrics.registerFont(TTFont("Mont-Md", os.path.join(FONTS, "MontserratMedium.ttf")))
pdfmetrics.registerFont(TTFont("Mont-Sb", os.path.join(FONTS, "MontserratSemiBold.ttf")))

pdfmetrics.registerFontFamily("Mont", normal="Mont", bold="Mont-Sb",
                              italic="Mont", boldItalic="Mont-Sb")
pdfmetrics.registerFontFamily("Mont-Lt", normal="Mont-Lt", bold="Mont-Md",
                              italic="Mont-Lt", boldItalic="Mont-Md")
pdfmetrics.registerFontFamily("Cormorant-Md", normal="Cormorant-Md", bold="Cormorant-Bd",
                              italic="Cormorant-It", boldItalic="Cormorant-Bd")
pdfmetrics.registerFontFamily("Cormorant-Sb", normal="Cormorant-Sb", bold="Cormorant-Bd",
                              italic="Cormorant-It", boldItalic="Cormorant-Bd")

NAVY      = HexColor("#141D2B")   # midnight
NAVY_2    = HexColor("#1D2A3D")
GOLD      = HexColor("#B08D4F")   # champagne gold
GOLD_SOFT = HexColor("#C7AB77")
GOLD_PALE = HexColor("#E8DCC4")
PAPER     = HexColor("#FCFBF7")   # warm white page
CREAM     = HexColor("#F6F2E9")   # tinted panels / alt rows
CHARCOAL  = HexColor("#39404C")   # body text
SLATE     = HexColor("#6E7683")   # muted text
HAIR      = HexColor("#E2DCCE")   # hairlines
WHITE     = HexColor("#FFFFFF")
MIST      = HexColor("#93A0B4")   # muted text on navy

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 2.35 * cm, 2.35 * cm, 2.7 * cm, 2.5 * cm
TEXT_W = PAGE_W - ML - MR

DOC_DATE = "July 2026"

# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------

def chf(n):
    """Swiss-style thousands: 1'850'000"""
    return format(int(round(n)), ",").replace(",", "’")


def tracked(canvas_obj, text, font, size, color, x, y, tracking=2.0, align="left"):
    canvas_obj.saveState()
    w = pdfmetrics.stringWidth(text, font, size) + tracking * max(len(text) - 1, 0)
    if align == "center":
        x = x - w / 2.0
    elif align == "right":
        x = x - w
    t = canvas_obj.beginText(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(tracking)
    t.textOut(text)
    canvas_obj.drawText(t)
    canvas_obj.restoreState()


class Track(Flowable):
    """In-flow letter-spaced caps label."""

    def __init__(self, text, font="Mont-Sb", size=7.5, color=GOLD,
                 tracking=2.4, align="left", space_after=0):
        super().__init__()
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.tracking = tracking
        self.align = align
        self.space_after = space_after

    def wrap(self, availWidth, availHeight):
        self.availWidth = availWidth
        return availWidth, self.size + 2 + self.space_after

    def draw(self):
        x = 0
        if self.align == "center":
            x = self.availWidth / 2.0
        elif self.align == "right":
            x = self.availWidth
        tracked(self.canv, self.text, self.font, self.size, self.color,
                x, self.space_after + 1, self.tracking, self.align)


class StructureChart(Flowable):
    """Elegant vertical group-structure schematic."""

    BOX_W, BOX_H, GAP = 262, 36, 21

    def __init__(self, width):
        super().__init__()
        self.width = width
        self.height = 4 * self.BOX_H + 3 * self.GAP + 6

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def _box(self, c, cx, top_y, title, sub, dark=False):
        x = cx - self.BOX_W / 2.0
        y = top_y - self.BOX_H
        c.setLineWidth(0.8)
        c.setStrokeColor(GOLD)
        c.setFillColor(NAVY if dark else CREAM)
        c.rect(x, y, self.BOX_W, self.BOX_H, fill=1, stroke=1)
        tracked(c, title, "Mont-Sb", 7.4, GOLD_SOFT if dark else NAVY,
                cx, y + self.BOX_H - 15, 1.6, "center")
        c.setFont("Mont-Lt", 6.6)
        c.setFillColor(MIST if dark else SLATE)
        c.drawCentredString(cx, y + 7, sub)
        return y

    def draw(self):
        c = self.canv
        cx = self.width / 2.0
        top = self.height - 2
        y = self._box(c, cx, top, "PSG SALES",
                      "Group parent · capital & investment committee", dark=True)
        for title, sub in [
            ("PSG SWITZERLAND AG", "Swiss holding · European petroleum sales & trading · Zug"),
            ("PSG IMMOBILIEN AG", "Real estate acquisition, development, renovation & resale"),
            ("PROJECT ENTITIES", "Per-project ring-fencing of larger developments"),
        ]:
            c.setStrokeColor(GOLD)
            c.setLineWidth(0.8)
            c.line(cx, y, cx, y - self.GAP)
            c.setFont("Mont-Lt", 6.2)
            c.setFillColor(GOLD)
            c.drawString(cx + 6, y - self.GAP / 2.0 - 2, "100%")
            y = self._box(c, cx, y - self.GAP, title, sub)


class Anchor(Flowable):
    """Records the page number a section starts on (for the contents page)."""

    def __init__(self, key, registry):
        super().__init__()
        self.key = key
        self.registry = registry
        self.width = self.height = 0

    def wrap(self, availWidth, availHeight):
        return 0, 0

    def draw(self):
        self.registry[self.key] = self.canv.getPageNumber()


# ----------------------------------------------------------------------------
# Paragraph styles
# ----------------------------------------------------------------------------
S = {}
S["body"] = ParagraphStyle("body", fontName="Mont", fontSize=8.8, leading=14.8,
                           textColor=CHARCOAL, alignment=TA_JUSTIFY, spaceAfter=7)
S["bodyL"] = ParagraphStyle("bodyL", parent=S["body"], alignment=TA_LEFT)
S["lead"] = ParagraphStyle("lead", fontName="Cormorant-Md", fontSize=13.2, leading=19,
                           textColor=NAVY_2, alignment=TA_LEFT, spaceAfter=11)
S["h1"] = ParagraphStyle("h1", fontName="Cormorant-Sb", fontSize=25, leading=29,
                         textColor=NAVY, spaceAfter=2)
S["h2"] = ParagraphStyle("h2", fontName="Cormorant-Sb", fontSize=14.5, leading=18,
                         textColor=NAVY, spaceBefore=13, spaceAfter=5)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], alignment=TA_LEFT,
                             leftIndent=13, firstLineIndent=-13, spaceAfter=4.5)
S["quote"] = ParagraphStyle("quote", fontName="Cormorant-It", fontSize=14.5, leading=20,
                            textColor=NAVY_2, alignment=TA_CENTER,
                            spaceBefore=6, spaceAfter=6)
S["cell"] = ParagraphStyle("cell", fontName="Mont", fontSize=8, leading=11.5,
                           textColor=CHARCOAL, alignment=TA_LEFT)
S["cellB"] = ParagraphStyle("cellB", parent=S["cell"], fontName="Mont-Md", textColor=NAVY)
S["cellR"] = ParagraphStyle("cellR", parent=S["cell"], alignment=TA_RIGHT)
S["cellBR"] = ParagraphStyle("cellBR", parent=S["cellB"], alignment=TA_RIGHT)
S["cellH"] = ParagraphStyle("cellH", fontName="Mont-Sb", fontSize=7, leading=10,
                            textColor=WHITE, alignment=TA_LEFT)
S["cellHR"] = ParagraphStyle("cellHR", parent=S["cellH"], alignment=TA_RIGHT)
S["note"] = ParagraphStyle("note", fontName="Mont", fontSize=7.3, leading=11.5,
                           textColor=SLATE, alignment=TA_LEFT, spaceBefore=5)
S["boxBody"] = ParagraphStyle("boxBody", parent=S["body"], fontSize=8.4, leading=13.6,
                              spaceAfter=5, alignment=TA_LEFT)
S["tocTitle"] = ParagraphStyle("tocTitle", fontName="Cormorant-Md", fontSize=13.5,
                               leading=17, textColor=NAVY)
S["tocPage"] = ParagraphStyle("tocPage", fontName="Mont", fontSize=8.5, leading=17,
                              textColor=GOLD, alignment=TA_RIGHT)
S["tocNum"] = ParagraphStyle("tocNum", fontName="Cormorant-Sb", fontSize=13.5,
                             leading=17, textColor=GOLD)


def bullet(text):
    return Paragraph(
        f'<font size="5.5" color="#B08D4F">&#9670;</font>&nbsp;&nbsp;{text}', S["bullet"])


def gold_rule(width=1.15 * cm, thickness=1.4, space_before=7, space_after=12):
    return HRFlowable(width=width, thickness=thickness, color=GOLD,
                      spaceBefore=space_before, spaceAfter=space_after,
                      hAlign="LEFT", lineCap="butt")


def hairline(space_before=8, space_after=8):
    return HRFlowable(width="100%", thickness=0.5, color=HAIR,
                      spaceBefore=space_before, spaceAfter=space_after, hAlign="LEFT")


def section_opener(num, title, anchor_key, registry, kicker="SECTION"):
    return [
        Anchor(anchor_key, registry),
        Track(f"{kicker} {num}", size=7.5, tracking=3.2),
        Spacer(1, 10),
        Paragraph(title, S["h1"]),
        gold_rule(),
    ]


def styled_table(header, rows, colWidths, right_cols=(), bold_rows=(),
                 header_right=(), total_row=None):
    data = []
    hcells = []
    for j, h in enumerate(header):
        st = S["cellHR"] if j in header_right else S["cellH"]
        hcells.append(Paragraph(h, st))
    data.append(hcells)
    for i, row in enumerate(rows):
        cells = []
        for j, v in enumerate(row):
            if i in bold_rows:
                st = S["cellBR"] if j in right_cols else S["cellB"]
            else:
                st = S["cellR"] if j in right_cols else S["cell"]
            cells.append(Paragraph(str(v), st))
        data.append(cells)
    t = Table(data, colWidths=colWidths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, GOLD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, CREAM]),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, HAIR),
        ("TOPPADDING", (0, 0), (-1, 0), 5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 4.6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    if total_row is not None:
        r = total_row + 1
        style += [
            ("LINEABOVE", (0, r), (-1, r), 0.9, GOLD),
            ("BACKGROUND", (0, r), (-1, r), GOLD_PALE),
            ("LINEBELOW", (0, r), (-1, r), 0.9, GOLD),
        ]
    t.setStyle(TableStyle(style))
    return t


def callout(label, paragraphs):
    inner = [Track(label, size=6.8, tracking=2.6, color=GOLD, space_after=2),
             Spacer(1, 5)]
    inner += [Paragraph(p, S["boxBody"]) for p in paragraphs]
    box = Table([[inner]], colWidths=[TEXT_W - 4])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ]))
    return box


def statement(text):
    return KeepTogether([
        Spacer(1, 4),
        HRFlowable(width=2.2 * cm, thickness=0.7, color=GOLD, hAlign="CENTER",
                   spaceBefore=0, spaceAfter=8),
        Paragraph(text, S["quote"]),
        HRFlowable(width=2.2 * cm, thickness=0.7, color=GOLD, hAlign="CENTER",
                   spaceBefore=8, spaceAfter=0),
    ])


# ----------------------------------------------------------------------------
# Page painters
# ----------------------------------------------------------------------------

def draw_frame(c, inset_outer=30, inset_inner=37):
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.3)
    c.rect(inset_outer, inset_outer, PAGE_W - 2 * inset_outer, PAGE_H - 2 * inset_outer)
    c.setLineWidth(0.5)
    c.rect(inset_inner, inset_inner, PAGE_W - 2 * inset_inner, PAGE_H - 2 * inset_inner)


def diamond(c, x, y, r=2.6, color=GOLD):
    c.saveState()
    c.setFillColor(color)
    c.setStrokeColor(color)
    p = c.beginPath()
    p.moveTo(x - r, y)
    p.lineTo(x, y + r)
    p.lineTo(x + r, y)
    p.lineTo(x, y - r)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def rule_with_diamond(c, cx, y, half=54):
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(cx - half, y, cx - 10, y)
    c.line(cx + 10, y, cx + half, y)
    diamond(c, cx, y)


def on_cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_frame(c)
    cx = PAGE_W / 2.0

    tracked(c, "P S G", "Cormorant-Sb", 40, GOLD_SOFT, cx, 690, 10, "center")
    tracked(c, "PETROLEUM SALES GROUP", "Mont-Lt", 8.5, MIST, cx, 668, 3.4, "center")
    rule_with_diamond(c, cx, 640)

    tracked(c, "CONFIDENTIAL BUSINESS PLAN", "Mont-Sb", 8, GOLD, cx, 555, 3.6, "center")
    c.setFillColor(WHITE)
    c.setFont("Cormorant-Sb", 31)
    c.drawCentredString(cx, 508, "Swiss Market Entry &")
    c.drawCentredString(cx, 471, "Real Estate Investment Platform")
    c.setFont("Cormorant-It", 13.5)
    c.setFillColor(GOLD_SOFT)
    c.drawCentredString(cx, 438, "Diversifying petroleum earnings into prime Swiss property")

    rule_with_diamond(c, cx, 380)
    tracked(c, "PREPARED UNDER THE DIRECTION OF", "Mont-Lt", 7, MIST, cx, 340, 2.8, "center")
    c.setFillColor(WHITE)
    c.setFont("Cormorant-Md", 19)
    c.drawCentredString(cx, 312, "Robert Ramseier")
    tracked(c, "DIPL. ARCHITEKT  ·  PRINCIPAL, SWITZERLAND", "Mont-Lt", 7.5, GOLD_SOFT,
            cx, 293, 2.4, "center")

    tracked(c, "ZURICH  ·  " + DOC_DATE.upper(), "Mont-Lt", 7, MIST, cx, 76, 2.6, "center")
    tracked(c, "STRICTLY PRIVATE & CONFIDENTIAL", "Mont-Lt", 6.4, MIST, cx, 60, 2.6, "center")
    c.restoreState()


def on_body(c, doc):
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # header
    y = PAGE_H - 1.55 * cm
    tracked(c, "PSG SALES", "Mont-Sb", 6.8, GOLD, ML, y, 2.6, "left")
    tracked(c, "SWITZERLAND EXPANSION · 2026", "Mont-Lt", 6.8, SLATE,
            PAGE_W - MR, y, 2.2, "right")
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.5)
    c.line(ML, y - 8, PAGE_W - MR, y - 8)

    # footer
    fy = 1.45 * cm
    c.line(ML, fy + 12, PAGE_W - MR, fy + 12)
    tracked(c, "STRICTLY PRIVATE & CONFIDENTIAL", "Mont-Lt", 6.2, SLATE, ML, fy, 2.0, "left")
    diamond(c, PAGE_W / 2.0, fy + 2.4, 1.8, GOLD_SOFT)
    tracked(c, f"PAGE {c.getPageNumber():02d}", "Mont-Md", 6.6, GOLD,
            PAGE_W - MR, fy, 1.8, "right")
    c.restoreState()


def on_closing(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_frame(c)
    cx = PAGE_W / 2.0

    tracked(c, "P S G", "Cormorant-Sb", 34, GOLD_SOFT, cx, 610, 9, "center")
    tracked(c, "PETROLEUM SALES GROUP", "Mont-Lt", 7.5, MIST, cx, 590, 3.2, "center")
    rule_with_diamond(c, cx, 562)

    c.setFillColor(WHITE)
    c.setFont("Cormorant-It", 15.5)
    c.drawCentredString(cx, 508, "“Lasting value is built on stable ground.”")

    tracked(c, "CONTACT", "Mont-Sb", 7.5, GOLD, cx, 440, 3.4, "center")
    c.setFillColor(WHITE)
    c.setFont("Cormorant-Md", 17)
    c.drawCentredString(cx, 412, "Robert Ramseier, Dipl. Architekt")
    c.setFont("Mont-Lt", 8.5)
    c.setFillColor(MIST)
    c.drawCentredString(cx, 394, "Principal, PSG Switzerland AG (in formation)")
    c.drawCentredString(cx, 380, "Zurich, Switzerland")
    c.setFillColor(GOLD_SOFT)
    c.drawCentredString(cx, 360, "[ telephone ]   ·   [ e-mail ]   ·   [ registered address ]")

    rule_with_diamond(c, cx, 310)
    c.setFillColor(MIST)
    c.setFont("Mont-Lt", 6.8)
    c.drawCentredString(cx, 270, "This document is issued for discussion purposes only and does not constitute an offer,")
    c.drawCentredString(cx, 258, "solicitation or investment advice. All figures are illustrative estimates subject to due diligence,")
    c.drawCentredString(cx, 246, "financing, and legal and tax confirmation under Swiss law.")

    tracked(c, "ZURICH  ·  " + DOC_DATE.upper(), "Mont-Lt", 7, MIST, cx, 76, 2.6, "center")
    c.restoreState()


# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------
SECTIONS = [
    ("01", "Executive Summary", "exec"),
    ("02", "The Group & the Swiss Principal", "group"),
    ("03", "Why Switzerland", "why"),
    ("04", "Business Model & Corporate Structure", "model"),
    ("05", "Real Estate Investment Strategy", "strategy"),
    ("06", "Illustrative Project Economics", "economics"),
    ("07", "Capital & Financial Plan", "financial"),
    ("08", "Organisation & Governance", "org"),
    ("09", "Legal, Tax & Regulatory Framework", "legal"),
    ("10", "Risk Analysis & Mitigation", "risk"),
    ("11", "Implementation Roadmap", "roadmap"),
]


def make_story(pages):
    st = []
    st.append(NextPageTemplate("Body"))
    st.append(PageBreak())

    # ---------------- Notice page ----------------
    st += [
        Spacer(1, 26),
        Track("IMPORTANT NOTICE", size=7.5, tracking=3.2),
        Spacer(1, 10),
        Paragraph("Basis of Preparation", S["h1"]),
        gold_rule(),
        Paragraph(
            "This business plan has been prepared for the board and shareholders of the "
            "Petroleum Sales Group (“PSG Sales”, the “Group”) to set out the strategy, "
            "structure and capital requirements for the Group’s market entry into Switzerland "
            "and the establishment of a Swiss real estate investment and development platform.",
            S["body"]),
        Paragraph(
            "All financial figures in this document are illustrative planning estimates prepared "
            "for internal discussion. They are not forecasts, valuations or offers, and remain "
            "subject to project-level due diligence, financing terms, and confirmation by Swiss "
            "legal and tax counsel — in particular with respect to the Federal Act on the "
            "Acquisition of Real Estate by Persons Abroad (“Lex Koller”).",
            S["body"]),
        Paragraph(
            "This document is strictly private and confidential. It may not be reproduced or "
            "distributed, in whole or in part, without the prior written consent of PSG Sales.",
            S["body"]),
        Spacer(1, 16),
        styled_table(
            ["DOCUMENT", "DETAIL"],
            [
                ["Title", "Swiss Market Entry &amp; Real Estate Investment Platform"],
                ["Status", "Draft for discussion — Version 1.0"],
                ["Prepared by", "Robert Ramseier, Dipl. Architekt — Principal designate, Switzerland"],
                ["Issued for", "Board &amp; shareholders, Petroleum Sales Group"],
                ["Place / date", "Zurich, " + DOC_DATE],
                ["Classification", "Strictly private &amp; confidential"],
            ],
            [4.0 * cm, TEXT_W - 4.0 * cm],
        ),
    ]
    st.append(PageBreak())

    # ---------------- Contents ----------------
    st += [
        Spacer(1, 26),
        Track("CONTENTS", size=7.5, tracking=3.2),
        Spacer(1, 10),
        Paragraph("Table of Contents", S["h1"]),
        gold_rule(),
        Spacer(1, 6),
    ]
    toc_rows = []
    for num, title, key in SECTIONS:
        pg = pages.get(key, 0)
        toc_rows.append([
            Paragraph(num, S["tocNum"]),
            Paragraph(title, S["tocTitle"]),
            Paragraph(f"{pg:02d}", S["tocPage"]),
        ])
    toc = Table(toc_rows, colWidths=[1.3 * cm, TEXT_W - 1.3 * cm - 1.6 * cm, 1.6 * cm])
    toc.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, HAIR),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    st.append(toc)
    st.append(PageBreak())

    # ---------------- 01 Executive Summary ----------------
    st += section_opener("01", "Executive Summary", "exec", pages)
    st += [
        Paragraph(
            "PSG Sales, an international petroleum sales group, will establish a permanent "
            "presence in Switzerland and deploy part of its capital into a disciplined Swiss "
            "real estate investment and development programme — combining the stability of "
            "the Swiss market with the Group’s financial strength and an in-house architectural "
            "leadership.", S["lead"]),
        Paragraph(
            "The expansion has two mutually reinforcing pillars. First, PSG Switzerland AG will "
            "anchor the Group’s European petroleum sales and trading relationships from one of "
            "the world’s leading commodity-trading locations. Second, a dedicated real estate "
            "division will invest Group capital into distressed properties, under-valued building "
            "plots and repositioning opportunities in the Zurich–Zug–Lucerne economic corridor, "
            "creating value through renovation, development and resale.", S["body"]),
        Paragraph(
            "The platform is led on the ground by Robert Ramseier, a Swiss registered architect, "
            "acting as Principal for Switzerland. His mandate brings development management, "
            "architecture and design fully in-house — removing the external design margin and "
            "giving the Group direct control over cost, quality and permitting from the first "
            "site visit to the notarised resale.", S["body"]),
        Paragraph("Two investment tracks", S["h2"]),
        bullet("<b>Short-cycle projects (6–8 months):</b> acquisition of distressed or "
               "under-managed residential and mixed-use properties, high-quality renovation to "
               "Swiss finishing standards, and resale — targeting gross project margins of "
               "15–19% per cycle."),
        bullet("<b>Long-cycle projects (approx. 24 months):</b> acquisition of building plots and "
               "obsolete structures, in-house design and permitting (Baubewilligung), new "
               "construction or deep repositioning, and unit-by-unit sale as condominium ownership "
               "(Stockwerkeigentum) — targeting gross project margins of 22–28%."),
        Paragraph("Headline plan figures (illustrative)", S["h2"]),
        styled_table(
            ["KEY PARAMETER", "PLAN BASIS"],
            [
                ["Group equity commitment, Phase I", "CHF 25’000’000 over 24 months"],
                ["Senior bank financing (50–60% loan-to-cost)", "up to CHF 15’000’000"],
                ["Total deployment capacity", "≈ CHF 40’000’000"],
                ["Short-cycle projects, years 1–2", "6–8 completed renovations"],
                ["Long-cycle projects, years 1–2", "2 developments in permitting / construction"],
                ["Blended target return on Group equity", "14–18% p.a. after platform costs"],
            ],
            [8.6 * cm, TEXT_W - 8.6 * cm],
        ),
        statement("Petroleum earnings become Swiss bricks: recurring trading cash flow is converted "
                  "into appreciating, franc-denominated assets under the Group’s own design authority."),
    ]
    st.append(PageBreak())

    # ---------------- 02 Group & Principal ----------------
    st += section_opener("02", "The Group & the Swiss Principal", "group", pages)
    st += [
        Paragraph(
            "A capital-strong international petroleum group, joined by a Swiss architect-principal "
            "who converts local expertise into proprietary deal flow and in-house execution.",
            S["lead"]),
        Paragraph("PSG Sales — Petroleum Sales Group", S["h2"]),
        Paragraph(
            "PSG Sales is an international group active in the sale, distribution and trading of "
            "petroleum products, serving commercial and wholesale customers across its existing "
            "markets. The Group generates recurring trading cash flow and now seeks two things "
            "from its next expansion step: a European commercial platform in a first-class "
            "jurisdiction, and a durable store of value that diversifies Group earnings away from "
            "commodity-price cyclicality.", S["body"]),
        Paragraph(
            "Switzerland answers both requirements in a single move. Geneva and Zug rank among "
            "the world’s foremost commodity-trading hubs, and Swiss real estate is one of "
            "Europe’s most stable long-term asset classes. The Group’s expansion therefore "
            "pairs an operating presence with an investment programme, each strengthening the "
            "other: the trading entity gives substance and banking depth to the Swiss platform, "
            "while the property portfolio anchors Group capital in Swiss francs.", S["body"]),
        Paragraph("The Swiss Principal — Robert Ramseier, Dipl. Architekt", S["h2"]),
        Paragraph(
            "The Swiss platform will be led by Robert Ramseier, a registered architect practising "
            "in Switzerland, appointed as Principal for the Swiss market. His role is deliberately "
            "entrepreneurial: he originates acquisitions, leads design and permitting, directs "
            "construction and renovation, and manages resale — supported by the Group’s "
            "capital and investment committee.", S["body"]),
        bullet("<b>Origination.</b> Access to off-market and distressed situations through the "
               "professional network of a practising architect: estate liquidations, "
               "renovation-backlog properties, foreclosure auctions (Betreibungsamt) and plots "
               "with unused building reserves."),
        bullet("<b>Design authority.</b> Architectural concept, execution planning and interior "
               "design are produced in-house, aligning design ambition with investment discipline "
               "from day one."),
        bullet("<b>Permitting.</b> Direct handling of zoning analysis and building applications "
               "(Baugesuch / Baubewilligung) with communal and cantonal authorities — the "
               "decisive schedule risk in Swiss development."),
        bullet("<b>Execution.</b> Tendering and supervision of contractors, cost control to SIA "
               "norms, and quality assurance to the finishing standard the resale price depends on."),
        Spacer(1, 2),
        callout("THE IN-HOUSE ADVANTAGE", [
            "In a typical Swiss development, external architecture, planning and development fees "
            "absorb roughly 12–18% of construction cost, and coordination between owner, "
            "architect and contractor is the main source of delay. By holding development, "
            "architecture and design inside the platform, PSG retains this margin, compresses "
            "decision cycles, and ensures that every franc of capital expenditure is spent where "
            "it produces resale value.",
        ]),
    ]
    st.append(PageBreak())

    # ---------------- 03 Why Switzerland ----------------
    st += section_opener("03", "Why Switzerland", "why", pages)
    st += [
        Paragraph(
            "A scarce-supply property market inside one of the world’s most stable economies "
            "— and, at the same time, Europe’s natural home for commodity trading.",
            S["lead"]),
        Paragraph("Macro-economic foundation", S["h2"]),
        bullet("<b>Stability.</b> Triple-A sovereign standing, low inflation, an independent "
               "central bank and the Swiss franc’s safe-haven status protect invested capital "
               "in real terms."),
        bullet("<b>Growth of demand.</b> Sustained net immigration of qualified labour drives "
               "household formation, above all in the Zurich–Zug–Lucerne economic area."),
        bullet("<b>Scarcity of supply.</b> Rental vacancy stands near historic lows (around one "
               "percent nationally, far lower in the economic centres), while restrictive zoning "
               "and lengthy permitting keep new supply structurally behind demand."),
        bullet("<b>Financing environment.</b> Swiss interest rates are consistently the lowest in "
               "Europe, allowing conservative but accretive senior leverage on well-underwritten "
               "projects."),
        Paragraph("The opportunity in distressed and under-managed assets", S["h2"]),
        Paragraph(
            "Beneath the headline stability lies a persistent inefficiency: a large stock of "
            "post-war buildings with renovation backlogs, energy-standard deficits and outdated "
            "layouts, frequently held by private or estate owners without the capital or "
            "expertise to reposition them. Rising energy requirements and generational ownership "
            "changes are bringing these assets to market — often quietly, before a broker is "
            "engaged. For a buyer who can underwrite quickly and execute professionally, the "
            "spread between the neglected purchase and the finished sale is the most reliable "
            "profit pool in the Swiss market.", S["body"]),
        Paragraph("Target regions", S["h2"]),
        styled_table(
            ["REGION", "PROFILE", "PRIMARY TRACK"],
            [
                ["Zurich (city &amp; agglomeration)", "Deepest liquidity, strongest exit pricing, premium finishes rewarded", "Short-cycle renovation"],
                ["Zug", "Low-tax corporate hub, executive demand, scarce supply", "Both tracks · Group seat"],
                ["Aargau", "Commuter belt value entry, attractive plot pricing", "Short-cycle &amp; plots"],
                ["Lucerne", "Lake-region quality of life, robust condominium demand", "Long-cycle development"],
                ["Bern corridor", "Stable administrative demand, conservative pricing", "Opportunistic"],
            ],
            [3.8 * cm, TEXT_W - 3.8 * cm - 3.9 * cm, 3.9 * cm],
        ),
        Paragraph("The petroleum platform", S["h2"]),
        Paragraph(
            "In parallel, PSG Switzerland AG establishes the Group’s European petroleum sales "
            "office in one of the world’s foremost energy-trading communities, with unmatched "
            "access to trade-finance banks, logistics services and counterparties — commercial "
            "substance that also strengthens the real estate division’s standing with Swiss "
            "lenders.", S["body"]),
    ]
    st.append(PageBreak())

    # ---------------- 04 Business model ----------------
    st += section_opener("04", "Business Model & Corporate Structure", "model", pages)
    st += [
        Paragraph(
            "One Swiss holding, two divisions: petroleum sales as the operating anchor, real "
            "estate development as the value engine — with the entire property value chain "
            "held in-house.", S["lead"]),
        Paragraph("Corporate structure", S["h2"]),
        styled_table(
            ["ENTITY", "FORM", "PURPOSE"],
            [
                ["PSG Sales (Group)", "Existing parent", "Capital allocation, investment committee, consolidated reporting"],
                ["PSG Switzerland AG", "Swiss stock corporation (AG), seat in Zug", "Group holding &amp; European petroleum sales / trading office"],
                ["PSG Immobilien AG", "Swiss AG, subsidiary", "Real estate acquisition, development, renovation &amp; resale"],
                ["Project entities", "Per-project AG / co-ownership", "Ring-fencing of individual developments where size warrants"],
            ],
            [4.1 * cm, 4.6 * cm, TEXT_W - 4.1 * cm - 4.6 * cm],
        ),
        Spacer(1, 4),
        Paragraph(
            "Incorporation as an Aktiengesellschaft (minimum capital CHF 100’000, of which "
            "CHF 50’000 paid in) provides the governance depth Swiss banks and counterparties "
            "expect. The seat in Zug combines a competitive cantonal tax regime with proximity to "
            "the commodity-trading community; the real estate subsidiary operates group-wide "
            "across the target cantons.", S["body"]),
        Spacer(1, 8),
        StructureChart(TEXT_W),
        KeepTogether([
            Paragraph("The in-house value chain", S["h2"]),
            styled_table(
                ["STAGE", "IN-HOUSE CAPABILITY", "EXTERNAL PARTNERS"],
            [
                ["1 · Sourcing", "Architect network, auction monitoring, direct-owner approach", "Selected brokers, banks’ workout desks"],
                ["2 · Underwriting", "Design-led feasibility: zoning reserves, cost, exit pricing", "Valuers, structural engineers"],
                ["3 · Acquisition", "Negotiation & transaction management", "Notary, legal &amp; tax counsel"],
                ["4 · Design &amp; permitting", "Full architecture &amp; Baugesuch in-house", "Specialist planners (HVAC, fire, energy)"],
                ["5 · Construction", "Project &amp; cost management, site supervision", "General &amp; trade contractors (tendered)"],
                ["6 · Sale", "Product definition, staging &amp; pricing strategy", "Marketing brokers, notary"],
            ],
            [3.3 * cm, 6.7 * cm, TEXT_W - 3.3 * cm - 6.7 * cm],
            ),
        ]),
        Spacer(1, 4),
        Paragraph("Revenue model", S["h2"]),
        bullet("<b>Development profit</b> — the core: margin between all-in project cost and "
               "notarised resale proceeds on both tracks."),
        bullet("<b>Retained design margin</b> — architecture and development fees that would "
               "otherwise be paid to third parties remain within the platform (calculated at "
               "market rates for transparency in project accounting)."),
        bullet("<b>Interim income</b> — rental income from assets held during permitting, and "
               "selective retention of finished units where holding yields exceed recycling "
               "value."),
        bullet("<b>Petroleum contribution</b> — commercial margin of the Swiss trading office, "
               "which also carries the platform’s fixed costs."),
    ]
    st.append(PageBreak())

    # ---------------- 05 Strategy ----------------
    st += section_opener("05", "Real Estate Investment Strategy", "strategy", pages)
    st += [
        Paragraph(
            "Buy below intrinsic value, add value through design and execution, sell into "
            "scarcity — on two disciplined cycles.", S["lead"]),
        Paragraph("Acquisition criteria", S["h2"]),
        bullet("<b>Distressed or motivated situations:</b> renovation backlog, estate "
               "liquidations, foreclosure auctions, bank workouts, partition sales — priced "
               "below replacement or comparable value."),
        bullet("<b>Location quality first:</b> commuting distance to Zurich, Zug or Lucerne, "
               "public transport access, and micro-locations with proven resale liquidity."),
        bullet("<b>Value levers we control:</b> unused building reserves (Ausnützungsreserve), "
               "layout and standard deficits, energy retrofits, densification or conversion "
               "potential — value created by design, not by market timing."),
        bullet("<b>Size discipline:</b> CHF 1–4 million all-in for short-cycle assets; "
               "CHF 8–15 million total cost for long-cycle developments — large enough to "
               "matter, small enough to remain liquid."),
        Paragraph("Track A — Short-cycle renovation (6–8 months)", S["h2"]),
        styled_table(
            ["PHASE", "DURATION", "CONTENT"],
            [
                ["Acquire", "Month 0", "Distressed purchase, simultaneous design concept &amp; cost frame"],
                ["Renovate", "Months 1–5", "Permit-light refurbishment: kitchens, baths, surfaces, energy, layout"],
                ["Sell", "Months 5–8", "Staged marketing at renovated-comparable pricing; notarised exit"],
            ],
            [2.6 * cm, 2.9 * cm, TEXT_W - 2.6 * cm - 2.9 * cm],
        ),
        Spacer(1, 3),
        Paragraph(
            "Track A generates fast capital rotation — the same equity works up to twice a "
            "year — and builds the platform’s track record with banks, notaries and "
            "brokers. Works are scoped to remain within simplified permitting wherever possible, "
            "protecting the 6–8 month cycle.", S["body"]),
        Paragraph("Track B — Long-cycle development (≈ 24 months)", S["h2"]),
        styled_table(
            ["PHASE", "DURATION", "CONTENT"],
            [
                ["Acquire &amp; design", "Months 0–4", "Plot or obsolete structure; in-house concept to building application"],
                ["Permitting", "Months 4–10", "Baubewilligung incl. objection management; pre-sales launch"],
                ["Construct", "Months 10–22", "New build / deep reposition under in-house supervision"],
                ["Sell", "Months 16–24", "Condominium units (Stockwerkeigentum) sold off-plan &amp; on completion"],
            ],
            [3.4 * cm, 2.9 * cm, TEXT_W - 3.4 * cm - 2.9 * cm],
        ),
        Spacer(1, 3),
        Paragraph(
            "Track B carries the platform’s highest margins. Pre-selling 40–60% of units "
            "during permitting and construction de-risks the exit and reduces peak equity. The "
            "product is deliberately premium: intelligent floor plans, honest materials and "
            "energy-efficient building services — the segment where Swiss buyers pay for "
            "architectural quality.", S["body"]),
        callout("PORTFOLIO RHYTHM", [
            "Steady state from year two: three to four Track A rotations per year running "
            "alongside one to two Track B developments, so that short-cycle profits continuously "
            "fund long-cycle equity — a self-reinforcing pipeline with capital never idle.",
        ]),
        Paragraph("Underwriting guardrails", S["h2"]),
        Paragraph(
            "Discipline is codified, not discretionary. Every acquisition memorandum is tested "
            "against fixed limits before it reaches the investment committee:", S["body"]),
        styled_table(
            ["GUARDRAIL", "LIMIT"],
            [
                ["Senior leverage", "Maximum 60% of total project cost"],
                ["Underwritten gross margin", "Minimum 15% (Track A) · 20% (Track B)"],
                ["Exit stress test", "Profitable at 10% below underwritten exit pricing"],
                ["Single-project equity", "Maximum 25% of committed Group equity"],
                ["Pre-sales before construction (Track B)", "Minimum 40% of units notarised or reserved"],
                ["Geography", "Within one hour of Zurich, Zug or Lucerne"],
            ],
            [7.6 * cm, TEXT_W - 7.6 * cm],
        ),
    ]
    st.append(PageBreak())

    # ---------------- 06 Economics ----------------
    st += section_opener("06", "Illustrative Project Economics", "economics", pages)
    st += [
        Paragraph(
            "Two model projects, underwritten conservatively at today’s market levels. "
            "Figures are planning illustrations, not forecasts.", S["lead"]),
        Paragraph("Model A — Short-cycle renovation, Canton Aargau", S["h2"]),
        Paragraph(
            "A 1970s single-family house with renovation backlog, acquired from an estate below "
            "comparable value, renovated to contemporary standard in five months and resold to an "
            "owner-occupier.", S["body"]),
        styled_table(
            ["POSITION", "CHF"],
            [
                ["Acquisition price (incl. transaction costs)", chf(1_850_000)],
                ["Renovation capital expenditure", chf(380_000)],
                ["Carrying, financing &amp; sales costs", chf(115_000)],
                ["<b>Total project cost</b>", "<b>" + chf(2_345_000) + "</b>"],
                ["Resale price (renovated comparable)", chf(2_760_000)],
                ["<b>Gross project profit</b>", "<b>" + chf(415_000) + "</b>"],
            ],
            [TEXT_W - 4.2 * cm, 4.2 * cm],
            right_cols=(1,), bold_rows=(3, 5), total_row=5,
        ),
        Paragraph(
            "Margin on cost ≈ 17.7% over a 7-month cycle. With 50% senior financing, the "
            "return on equity employed is materially higher; two rotations of the same equity "
            "per year compound the effect.", S["note"]),
        Spacer(1, 8),
        Paragraph("Model B — Long-cycle development, Lucerne region", S["h2"]),
        Paragraph(
            "A building plot with an obsolete structure acquired off-market; in-house design and "
            "permitting of eight premium condominium units; construction over twelve months; "
            "units pre-sold from the permitting phase as Stockwerkeigentum.", S["body"]),
        styled_table(
            ["POSITION", "CHF"],
            [
                ["Plot acquisition (incl. transaction costs)", chf(3_300_000)],
                ["Construction cost, 8 units (tendered, incl. contingency)", chf(6_800_000)],
                ["Soft costs retained in-house (design, development, permits)", chf(950_000)],
                ["Financing &amp; sales costs", chf(650_000)],
                ["<b>Total project cost</b>", "<b>" + chf(11_700_000) + "</b>"],
                ["Sales revenue — 8 units, avg. " + chf(1_815_000), chf(14_520_000)],
                ["<b>Gross project profit</b>", "<b>" + chf(2_820_000) + "</b>"],
            ],
            [TEXT_W - 4.2 * cm, 4.2 * cm],
            right_cols=(1,), bold_rows=(4, 6), total_row=6,
        ),
        Paragraph(
            "Margin on cost ≈ 24.1% over 24 months. Because design and development are "
            "produced in-house, the soft-cost line is retained within the platform rather than "
            "paid away — raising the effective Group margin above the headline figure.",
            S["note"]),
        KeepTogether([
            Paragraph("Resilience of the models", S["h2"]),
            Paragraph(
                "Both models are underwritten to remain profitable under meaningful stress — the "
                "discount captured at acquisition is the margin of safety:", S["body"]),
            styled_table(
                ["SCENARIO", "MODEL A MARGIN", "MODEL B MARGIN"],
                [
                    ["Base case, as underwritten", "17.7%", "24.1%"],
                    ["Exit pricing − 5%", "11.8%", "17.9%"],
                    ["Exit pricing − 10%", "5.9%", "11.7%"],
                    ["Works cost + 10%", "15.8%", "17.3%"],
                ],
                [TEXT_W - 7.6 * cm, 3.8 * cm, 3.8 * cm],
                right_cols=(1, 2), header_right=(1, 2),
            ),
        ]),
        Spacer(1, 4),
        statement("Profit is engineered at acquisition and secured by execution — the market "
                  "is asked only to remain stable, not to rise."),
    ]
    st.append(PageBreak())

    # ---------------- 07 Financial plan ----------------
    st += section_opener("07", "Capital & Financial Plan", "financial", pages)
    st += [
        Paragraph(
            "CHF 25 million of Group equity, conservatively leveraged, deployed across a "
            "self-funding two-track pipeline.", S["lead"]),
        Paragraph("Phase I capital allocation (24 months)", S["h2"]),
        styled_table(
            ["ALLOCATION", "CHF", "%"],
            [
                ["Track A — short-cycle renovation programme", chf(9_000_000), "36%"],
                ["Track B — long-cycle developments (equity share)", chf(12_500_000), "50%"],
                ["Platform build-up, studio &amp; working capital", chf(2_000_000), "8%"],
                ["Strategic reserve / opportunity fund", chf(1_500_000), "6%"],
                ["<b>Total Group equity commitment</b>", "<b>" + chf(25_000_000) + "</b>", "<b>100%</b>"],
            ],
            [TEXT_W - 4.2 * cm - 2.0 * cm, 4.2 * cm, 2.0 * cm],
            right_cols=(1, 2), bold_rows=(4,), total_row=4,
        ),
        Spacer(1, 4),
        Paragraph(
            "Senior bank financing of 50–60% of project cost is added at asset level once the "
            "platform’s Swiss banking relationships are established, lifting total deployment "
            "capacity toward CHF 40 million. Leverage is used to enhance rotation, never to "
            "stretch underwriting.", S["body"]),
        Paragraph("Five-year outlook (illustrative, real estate division)", S["h2"]),
        styled_table(
            ["", "YEAR 1", "YEAR 2", "YEAR 3", "YEAR 4", "YEAR 5"],
            [
                ["Track A exits", "2", "4", "5", "6", "6"],
                ["Track B completions", "—", "1", "1", "2", "2"],
                ["Sales revenue, CHF m", "5.4", "21.8", "28.5", "41.0", "44.5"],
                ["Gross development profit, CHF m", "0.9", "4.1", "5.6", "8.3", "9.1"],
                ["Platform &amp; overhead costs, CHF m", "(1.1)", "(1.4)", "(1.7)", "(2.0)", "(2.1)"],
                ["<b>Division result before tax, CHF m</b>", "<b>(0.2)</b>", "<b>2.7</b>", "<b>3.9</b>", "<b>6.3</b>", "<b>7.0</b>"],
                ["Cumulative result, CHF m", "(0.2)", "2.5", "6.4", "12.7", "19.7"],
            ],
            [TEXT_W - 5 * 1.75 * cm, 1.75 * cm, 1.75 * cm, 1.75 * cm, 1.75 * cm, 1.75 * cm],
            right_cols=(1, 2, 3, 4, 5), bold_rows=(5,), header_right=(1, 2, 3, 4, 5), total_row=6,
        ),
        Paragraph(
            "Year 1 absorbs platform build-up ahead of the first exits; from year 2 the division "
            "is self-funding, with profits recycled into the pipeline. Petroleum trading results "
            "of PSG Switzerland AG are additive and not included above. All figures illustrative; "
            "no market appreciation assumed.", S["note"]),
        Spacer(1, 6),
        Paragraph("Funding & repatriation principles", S["h2"]),
        bullet("Group equity is drawn in tranches against approved acquisitions — never "
               "pre-funded idle."),
        bullet("Each project is ring-fenced; cross-collateralisation requires investment-committee "
               "approval."),
        bullet("Profits are recycled in Switzerland during the build-up phase; thereafter, annual "
               "distributions to the Group under the Swiss–home-jurisdiction double-tax treaty "
               "framework."),
    ]
    st.append(PageBreak())

    # ---------------- 08 Organisation ----------------
    st += section_opener("08", "Organisation & Governance", "org", pages)
    st += [
        Paragraph(
            "Entrepreneurial on the ground, institutionally governed above — clear mandates, "
            "clear approval limits.", S["lead"]),
        Paragraph("Governance architecture", S["h2"]),
        styled_table(
            ["LEVEL", "COMPOSITION", "MANDATE"],
            [
                ["Group board", "PSG Sales ownership &amp; executive", "Strategy, capital commitment, annual plan approval"],
                ["Investment committee", "Group CEO, Group CFO, Swiss Principal", "Approval of every acquisition, budget &amp; exit; quarterly review"],
                ["PSG Switzerland AG board", "Group representatives + Swiss member(s)", "Swiss statutory governance, banking, compliance"],
                ["Swiss Principal", "Robert Ramseier, Dipl. Architekt", "Origination, design, execution &amp; sale within approved budgets"],
            ],
            [3.4 * cm, 5.4 * cm, TEXT_W - 3.4 * cm - 5.4 * cm],
        ),
        Spacer(1, 4),
        Paragraph("Approval discipline", S["h2"]),
        bullet("Every acquisition requires a written underwriting memorandum — design "
               "concept, cost frame to SIA norms, exit comparables, sensitivity — approved by "
               "the investment committee before notarisation."),
        bullet("Budget overruns beyond a defined tolerance (5%) return to the committee; "
               "monthly project reporting on cost, schedule and sales status."),
        bullet("Dual signatures on all property transactions and payments above defined limits."),
        Paragraph("The Swiss team — lean by design", S["h2"]),
        styled_table(
            ["ROLE", "PHASE I", "FROM YEAR 2–3"],
            [
                ["Principal / lead architect", "R. Ramseier", "R. Ramseier"],
                ["Architecture &amp; design studio", "1–2 architects / draftspersons", "3–4 incl. interior design"],
                ["Project &amp; construction management", "1 (shared with Principal)", "2 dedicated"],
                ["Acquisitions &amp; sales", "Principal + external brokers", "1 dedicated manager"],
                ["Finance &amp; administration", "Fiduciary (outsourced)", "1 in-house controller"],
            ],
            [5.2 * cm, 5.2 * cm, TEXT_W - 5.2 * cm - 5.2 * cm],
        ),
        Spacer(1, 4),
        Paragraph(
            "Specialist engineering (structural, HVAC, energy, fire), legal, tax and notarial "
            "services remain external on a project basis — keeping fixed costs low while the "
            "value-defining disciplines of design, development and construction leadership stay "
            "in-house.", S["body"]),
    ]
    st.append(PageBreak())

    # ---------------- 09 Legal ----------------
    st += section_opener("09", "Legal, Tax & Regulatory Framework", "legal", pages)
    st += [
        Paragraph(
            "Swiss real estate rewards those who take its rules seriously. The platform is "
            "structured around them from the outset.", S["lead"]),
        callout("LEX KOLLER — THE DECISIVE STRUCTURING QUESTION", [
            "The Federal Act on the Acquisition of Real Estate by Persons Abroad (Lex Koller) "
            "restricts the acquisition of <b>residential</b> property by foreign nationals and "
            "foreign-controlled companies. For a foreign-controlled group, unrestricted "
            "acquisition is generally limited to <b>commercial-use property</b> (offices, retail, "
            "industrial, hotels), while residential acquisitions require either exemption, "
            "permit, or a compliant ownership structure.",
            "The plan therefore treats Lex Koller as a design parameter, not an afterthought: "
            "(i) formal legal opinion from specialised Swiss counsel before the first "
            "acquisition; (ii) a deal funnel that includes commercial and mixed-use assets which "
            "are outside the restriction; (iii) evaluation of Swiss co-investment and ownership "
            "structures for the residential programme — including the position of the Swiss "
            "Principal — strictly within the boundaries of the Act; and (iv) transaction-by-"
            "transaction confirmation with the competent cantonal authority where any doubt "
            "exists. Non-compliant structures are void under Swiss law — there is no "
            "commercial upside that justifies the risk.",
        ]),
        Spacer(1, 6),
        Paragraph("Corporate & tax framework", S["h2"]),
        bullet("<b>Incorporation:</b> AG under the Swiss Code of Obligations; notarial deed, "
               "commercial register entry, Swiss-resident board representation; share capital "
               "min. CHF 100’000."),
        bullet("<b>Corporate taxation:</b> combined federal / cantonal / communal rates of "
               "roughly 12–14% in Zug and comparable low-tax cantons."),
        bullet("<b>Property gains taxation:</b> cantonal real estate gains tax "
               "(Grundstückgewinnsteuer) applies on resale, with holding-period-dependent "
               "rates; frequent trading qualifies the platform as a professional property dealer "
               "(gewerbsmässiger Liegenschaftshändler) with corresponding income-tax "
               "treatment — modelled into every underwriting."),
        bullet("<b>Transaction taxes:</b> cantonal transfer taxes and notarial / land-register "
               "fees vary by canton and are included in acquisition cost at underwriting."),
        bullet("<b>VAT:</b> option for VAT on commercial lettings and correct input-tax treatment "
               "on construction cost, structured with the fiduciary from project one."),
        Paragraph("Planning & construction law", S["h2"]),
        bullet("Communal zoning plans (Bau- und Zonenordnung) define use and density; in-house "
               "zoning analysis is the first underwriting step for every asset."),
        bullet("Building permits are public procedures with neighbour objection rights "
               "(Einsprachen); schedule buffers and early neighbour engagement are standard "
               "practice in the plan."),
        bullet("Energy regulation (cantonal MuKEn standards) increasingly conditions renovations "
               "— a cost factor for unprepared sellers, and precisely the expertise premium "
               "this platform monetises."),
        bullet("Condominium creation (Stockwerkeigentum) is established by notarial deed with "
               "land-register entry — the standard exit vehicle for Track B."),
        Paragraph("Compliance", S["h2"]),
        Paragraph(
            "Anti-money-laundering diligence applies through the involved banks, notaries and, "
            "where applicable, financial intermediaries: documented source of funds from Group "
            "trading activity, know-your-counterparty checks on sellers and buyers, and payments "
            "exclusively through Swiss banking channels.", S["body"]),
        Paragraph("External advisory panel", S["h2"]),
        Paragraph(
            "A standing panel of Swiss advisors is appointed at incorporation and engaged on "
            "every transaction:", S["body"]),
        styled_table(
            ["ADVISOR", "MANDATE"],
            [
                ["Legal counsel — real estate &amp; Lex Koller", "Structuring opinion, transaction documents, permit appeals"],
                ["Tax &amp; fiduciary partner", "Corporate set-up, VAT and property-dealer taxation, accounting"],
                ["Cantonal notaries", "Deeds, land-register entries, condominium constitution"],
                ["Independent valuation partner", "Exit appraisals for every investment-committee submission"],
                ["Financing banks (2–3 relationships)", "Senior project facilities, interim finance, deposit banking"],
            ],
            [7.2 * cm, TEXT_W - 7.2 * cm],
        ),
    ]
    st.append(PageBreak())

    # ---------------- 10 Risk ----------------
    st += section_opener("10", "Risk Analysis & Mitigation", "risk", pages)
    st += [
        Paragraph(
            "Every material risk is either priced at acquisition, contracted away, or capped by "
            "structure.", S["lead"]),
        styled_table(
            ["RISK", "ASSESSMENT", "MITIGATION"],
            [
                ["Market correction during hold",
                 "Moderate probability, moderate impact on exit pricing",
                 "Profit underwritten at purchase, no appreciation assumed; short cycles limit exposure window; pre-sales on Track B; capacity to hold and let at sustainable yields"],
                ["Lex Koller / regulatory",
                 "Low probability if structured correctly; severe if ignored",
                 "Specialised counsel before first acquisition; commercial / mixed-use funnel; cantonal confirmation where any doubt; no structure at the edge of the Act"],
                ["Permitting delay &amp; objections",
                 "High probability of some delay on Track B",
                 "In-house permitting expertise; early authority &amp; neighbour dialogue; schedule buffers; Track A scoped for simplified procedures"],
                ["Construction cost overrun",
                 "Moderate probability",
                 "In-house cost planning to SIA norms; fixed-price / GMP tendering; 8–10% contingency; dual-signature change control"],
                ["Interest rate movement",
                 "Low–moderate; Swiss rates structurally low",
                 "Conservative 50–60% leverage; forward fixing on Track B; underwriting stressed at +150 bp"],
                ["Liquidity of exits",
                 "Low in target regions at target price points",
                 "Focus on liquid segments (family homes, 2.5–4.5-room condominiums); realistic pricing; broker network alongside in-house sales"],
                ["Key person (Principal)",
                 "Concentrated in build-up phase",
                 "Documented processes, deputising architect from year 1, key-person insurance, Group oversight of all files"],
                ["Currency (CHF vs. group currency)",
                 "Translation exposure for the Group",
                 "CHF assets funded substantially in CHF; natural hedge via Swiss cost base; hedging policy at Group treasury"],
            ],
            [3.1 * cm, 4.3 * cm, TEXT_W - 3.1 * cm - 4.3 * cm],
        ),
        Spacer(1, 8),
        statement("The plan’s first defence is the price paid; its second, the quality of "
                  "execution; its third, the balance sheet behind it."),
    ]
    st.append(PageBreak())

    # ---------------- 11 Roadmap ----------------
    st += section_opener("11", "Implementation Roadmap", "roadmap", pages)
    st += [
        Paragraph(
            "From board approval to a self-funding Swiss platform in eight quarters.", S["lead"]),
        styled_table(
            ["PHASE", "PERIOD", "MILESTONES"],
            [
                ["I · Foundation", "Q3–Q4 2026",
                 "Board approval &amp; capital commitment · Lex Koller opinion · incorporation of PSG Switzerland AG &amp; PSG Immobilien AG (Zug) · banking relationships · studio set-up · pipeline building"],
                ["II · First capital", "Q4 2026–Q1 2027",
                 "First 2 Track A acquisitions notarised · renovations under way · first Track B plot under exclusivity · petroleum sales office operational"],
                ["III · Proof", "Q2–Q3 2027",
                 "First Track A exits — track record established · Track B building application filed · senior financing lines confirmed · Track A rotations 3–4"],
                ["IV · Scale", "Q4 2027–2028",
                 "Track B permit &amp; construction start, pre-sales &gt; 40% · 4–5 Track A projects p.a. · second Track B acquisition · first profit distribution assessment"],
                ["V · Platform", "2029 onwards",
                 "Two Track B completions delivered · portfolio equity &gt; CHF 30 m · selective income-asset retention · evaluation of French-speaking market entry"],
            ],
            [2.9 * cm, 3.2 * cm, TEXT_W - 2.9 * cm - 3.2 * cm],
        ),
        Spacer(1, 8),
        Paragraph("Immediate next steps", S["h2"]),
        bullet("Group board resolution on the Phase I equity commitment of CHF 25 million."),
        bullet("Engagement of Swiss legal counsel for the Lex Koller opinion and incorporation "
               "mandate."),
        bullet("Appointment of Robert Ramseier as Principal and constitution of the investment "
               "committee."),
        bullet("Opening of Swiss banking relationships for the operating and project accounts."),
        bullet("Activation of the acquisition pipeline — first underwriting memoranda to the "
               "investment committee within 60 days of incorporation."),
        Spacer(1, 10),
        statement("Switzerland rewards patience, precision and presence. This plan brings all "
                  "three — with the Group’s capital behind them."),
    ]

    # closing dark page
    st.append(NextPageTemplate("Closing"))
    st.append(PageBreak())
    st.append(Spacer(1, 1))
    return st


# ----------------------------------------------------------------------------
# Build (two passes: record section pages, then final with TOC numbers)
# ----------------------------------------------------------------------------

def build(path, pages):
    doc = BaseDocTemplate(
        path, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title="PSG Sales — Swiss Market Entry & Real Estate Investment Platform",
        author="Robert Ramseier · PSG Sales",
        subject="Confidential Business Plan — Switzerland Expansion",
        creator="PSG Sales",
    )
    frame = Frame(ML, MB, TEXT_W, PAGE_H - MT - MB, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cover_frame = Frame(ML, MB, TEXT_W, PAGE_H - MT - MB, id="cover",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="Body", frames=[frame], onPage=on_body),
        PageTemplate(id="Closing", frames=[cover_frame], onPage=on_closing),
    ])
    doc.build(make_story(pages))


if __name__ == "__main__":
    registry = {}
    tmp = OUT + ".pass1.pdf"
    build(tmp, registry)          # pass 1: record real page numbers
    build(OUT, dict(registry))    # pass 2: final with TOC numbers
    os.remove(tmp)
    print("Wrote", OUT, "sections:", registry)
