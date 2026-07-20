# -*- coding: utf-8 -*-
"""Businessplan Goldraffinerie & Gold-Bunker Frauenfeld — PDF-Generator (ReportLab)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF

GOLD = colors.HexColor("#8B6914")
GOLD_LIGHT = colors.HexColor("#C9A227")
DARK = colors.HexColor("#1A1A1A")
GREY = colors.HexColor("#555555")
BG = colors.HexColor("#F5EFD9")
TABLE_HEAD = colors.HexColor("#3B3323")

PAGE_W, PAGE_H = A4
OUT = "Businessplan_Goldraffinerie_Frauenfeld.pdf"

styles = getSampleStyleSheet()

def st(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    s = ParagraphStyle(name, parent=base, **kw)
    styles.add(s)
    return s

st("Body", fontName="Helvetica", fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY,
   textColor=DARK, spaceAfter=5)
st("BodyC", parent=styles["Body"], alignment=TA_CENTER)
st("H1x", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=GOLD,
   spaceBefore=14, spaceAfter=7)
st("H2x", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=DARK,
   spaceBefore=10, spaceAfter=4)
st("Bullet2", parent=styles["Body"], leftIndent=12, bulletIndent=2, spaceAfter=2.5)
st("Small", fontName="Helvetica", fontSize=7.5, leading=10, textColor=GREY)
st("TblCell", fontName="Helvetica", fontSize=8.5, leading=11, textColor=DARK)
st("TblCellB", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=DARK)
st("TblHead", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
st("CoverTitle", fontName="Helvetica-Bold", fontSize=26, leading=32,
   textColor=DARK, alignment=TA_CENTER)
st("CoverSub", fontName="Helvetica", fontSize=13, leading=18, textColor=GREY,
   alignment=TA_CENTER)
st("CoverMeta", fontName="Helvetica", fontSize=10, leading=15, textColor=DARK,
   alignment=TA_CENTER)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.6)
    canvas.line(20*mm, PAGE_H-14*mm, PAGE_W-20*mm, PAGE_H-14*mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(20*mm, PAGE_H-12.2*mm,
                      "Businessplan  ·  Goldraffinerie & Hochsicherheits-Bunker  ·  Parzelle 61522, Frauenfeld TG")
    canvas.drawRightString(PAGE_W-20*mm, PAGE_H-12.2*mm, "VERTRAULICH")
    canvas.line(20*mm, 13*mm, PAGE_W-20*mm, 13*mm)
    canvas.drawString(20*mm, 9.5*mm, "Projektstudie AURUM HELVETIA  ·  Stand: Juli 2026")
    canvas.drawRightString(PAGE_W-20*mm, 9.5*mm, f"Seite {doc.page}")
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H-18*mm, PAGE_W, 18*mm, stroke=0, fill=1)
    canvas.rect(0, 0, PAGE_W, 12*mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(20*mm, PAGE_H-12*mm, "PROJEKTSTUDIE  ·  AURUM HELVETIA AG (i. G.)")
    canvas.drawRightString(PAGE_W-20*mm, PAGE_H-12*mm, "VERTRAULICH")
    # Goldbarren-Symbol
    cx = PAGE_W/2
    y0 = 42*mm
    canvas.setFillColor(GOLD_LIGHT)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    p = canvas.beginPath()
    p.moveTo(cx-28*mm, y0); p.lineTo(cx+28*mm, y0)
    p.lineTo(cx+22*mm, y0+14*mm); p.lineTo(cx-22*mm, y0+14*mm); p.close()
    canvas.drawPath(p, stroke=1, fill=1)
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(cx, y0+5.5*mm, "999.9  FINE  GOLD")
    canvas.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                         topMargin=22*mm, bottomMargin=18*mm,
                         title="Businessplan Goldraffinerie & Gold-Bunker Frauenfeld",
                         author="AURUM HELVETIA AG (i. G.)")
        f = Frame(20*mm, 18*mm, PAGE_W-40*mm, PAGE_H-40*mm, id="main")
        fc = Frame(25*mm, 20*mm, PAGE_W-50*mm, PAGE_H-40*mm, id="cover")
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[fc], onPage=cover),
            PageTemplate(id="Std", frames=[f], onPage=header_footer),
        ])


def P(txt, style="Body"):
    return Paragraph(txt, styles[style])

def B(txt):
    return Paragraph(f"•  {txt}", styles["Bullet2"])

def tbl(data, widths, aligns=None, bold_last=False, head=True):
    rows = []
    for ri, row in enumerate(data):
        cells = []
        for ci, cell in enumerate(row):
            if ri == 0 and head:
                s = "TblHead"
            elif bold_last and ri == len(data)-1:
                s = "TblCellB"
            else:
                s = "TblCellB" if (ci == 0 and isinstance(cell, str) and cell.startswith("**")) else "TblCell"
            txt = cell.lstrip("*") if isinstance(cell, str) else str(cell)
            cells.append(Paragraph(txt, styles[s]))
        rows.append(cells)
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F4EA")]),
    ]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD))
    if bold_last:
        style.append(("BACKGROUND", (0, len(data)-1), (-1, len(data)-1), colors.HexColor("#EFE6C8")))
    if aligns:
        for ci, a in enumerate(aligns):
            if a == "R":
                style.append(("ALIGN", (ci, 0), (ci, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t


def site_plan():
    """Schematischer Arealplan (nicht massstäblich)."""
    W, H = 170*mm, 108*mm
    d = Drawing(W, H)
    # Parzelle
    d.add(Rect(6*mm, 8*mm, 158*mm, 92*mm, strokeColor=DARK, strokeWidth=1.4,
               fillColor=colors.HexColor("#EDF3E4")))
    d.add(String(8*mm, 102*mm, "Parzelle 61522 · 6'434 m² (Schema, nicht massstäblich)",
                 fontName="Helvetica-Bold", fontSize=8, fillColor=DARK))
    # Strasse unten
    d.add(Rect(6*mm, 0, 158*mm, 6*mm, strokeColor=None, fillColor=colors.HexColor("#C8C8C8")))
    d.add(String(66*mm, 1.8*mm, "Erschliessungsstrasse (Gebiet Langfeld / Ost- / Juchstrasse)",
                 fontName="Helvetica", fontSize=6.5, fillColor=DARK))
    # Baulinienbereich Nationalstrasse (rechts)
    d.add(Rect(146*mm, 8*mm, 18*mm, 92*mm, strokeColor=colors.HexColor("#B03030"),
               strokeWidth=0.8, fillColor=colors.HexColor("#F6DADA")))
    d.add(String(148*mm, 88*mm, "Baulinie", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#B03030")))
    d.add(String(148*mm, 84.5*mm, "N-Strasse", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#B03030")))
    d.add(String(148*mm, 81*mm, "(107 m,", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#B03030")))
    d.add(String(148*mm, 77.5*mm, "freihalten)", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#B03030")))
    # Perimeter
    d.add(Rect(10*mm, 11*mm, 132*mm, 86*mm, strokeColor=GOLD, strokeWidth=1.2,
               fillColor=None, strokeDashArray=[3, 2]))
    d.add(String(12*mm, 93.5*mm, "Sicherheitsperimeter (Zaun 3 m, Detektion, Videoanalyse)",
                 fontName="Helvetica", fontSize=6.5, fillColor=GOLD))
    # Security House am Zugang
    d.add(Rect(62*mm, 11*mm, 26*mm, 14*mm, strokeColor=DARK, strokeWidth=1,
               fillColor=colors.HexColor("#D8E4F0")))
    d.add(String(64*mm, 19.5*mm, "SECURITY HOUSE", fontName="Helvetica-Bold", fontSize=6, fillColor=DARK))
    d.add(String(64*mm, 16*mm, "Leitstelle 24/7,", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    d.add(String(64*mm, 13*mm, "Personen-/Fzg.-Schleuse", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    # Raffinerie
    d.add(Rect(16*mm, 46*mm, 66*mm, 44*mm, strokeColor=DARK, strokeWidth=1,
               fillColor=colors.HexColor("#F3E3B8")))
    d.add(String(19*mm, 83*mm, "RAFFINERIE", fontName="Helvetica-Bold", fontSize=8, fillColor=DARK))
    d.add(String(19*mm, 78.5*mm, "Schmelze · Scheidung · Elektrolyse", fontName="Helvetica", fontSize=6, fillColor=DARK))
    d.add(String(19*mm, 75*mm, "Labor · Abluftreinigung · Giesserei", fontName="Helvetica", fontSize=6, fillColor=DARK))
    d.add(String(19*mm, 71.5*mm, "ca. 1'400 m² Grundfläche, 2 Geschosse", fontName="Helvetica", fontSize=6, fillColor=DARK))
    # Bunker
    d.add(Rect(96*mm, 56*mm, 40*mm, 34*mm, strokeColor=DARK, strokeWidth=1.6,
               fillColor=colors.HexColor("#D9D2C0")))
    d.add(String(99*mm, 83*mm, "GOLD-BUNKER", fontName="Helvetica-Bold", fontSize=7.5, fillColor=DARK))
    d.add(String(99*mm, 79*mm, "Tresoranlage EN 1143-1", fontName="Helvetica", fontSize=6, fillColor=DARK))
    d.add(String(99*mm, 75.5*mm, "2 Ebenen (davon 1 UG)", fontName="Helvetica", fontSize=6, fillColor=DARK))
    d.add(String(99*mm, 72*mm, "ca. 450 m² Grundfläche", fontName="Helvetica", fontSize=6, fillColor=DARK))
    # Verbindungstrakt
    d.add(Rect(82*mm, 62*mm, 14*mm, 12*mm, strokeColor=DARK, strokeWidth=0.8,
               fillColor=colors.HexColor("#E8E0CC")))
    d.add(String(83*mm, 67.5*mm, "Wert-", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    d.add(String(83*mm, 64.5*mm, "schleuse", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    # LKW-Schleuse / Logistik
    d.add(Rect(96*mm, 30*mm, 40*mm, 20*mm, strokeColor=DARK, strokeWidth=1,
               fillColor=colors.HexColor("#E2E9DC")))
    d.add(String(99*mm, 43*mm, "LOGISTIK / WTU-SCHLEUSE", fontName="Helvetica-Bold", fontSize=6, fillColor=DARK))
    d.add(String(99*mm, 39.5*mm, "geschlossene Fahrzeugschleuse,", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    d.add(String(99*mm, 36.5*mm, "Anlieferung Doré / Auslieferung", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    # Parkierung
    d.add(Rect(16*mm, 28*mm, 40*mm, 12*mm, strokeColor=GREY, strokeWidth=0.7,
               fillColor=colors.HexColor("#EFEFEF")))
    d.add(String(18*mm, 33*mm, "Parkierung Personal/Besucher (aussen)", fontName="Helvetica", fontSize=5.5, fillColor=DARK))
    # Nordpfeil
    d.add(Polygon([158*mm, 14*mm, 156*mm, 9*mm, 160*mm, 9*mm],
                  strokeColor=DARK, fillColor=DARK))
    d.add(String(156.6*mm, 15.5*mm, "N", fontName="Helvetica-Bold", fontSize=7, fillColor=DARK))
    return d


story = []

# ---------------------------------------------------------------- Deckblatt
story.append(Spacer(1, 30*mm))
story.append(P("BUSINESSPLAN", "CoverSub"))
story.append(Spacer(1, 4*mm))
story.append(P("Goldraffinerie<br/>Hochsicherheits-Goldbunker<br/>Security House", "CoverTitle"))
story.append(Spacer(1, 8*mm))
story.append(P("Parzelle 61522 · Frauenfeld · Kanton Thurgau · Schweiz", "CoverSub"))
story.append(Spacer(1, 42*mm))
meta = [
    ["Projekt", "AURUM HELVETIA — Raffinations- und Wertlagerzentrum Frauenfeld"],
    ["Grundstück", "Parzelle Nr. 61522, E-GRID CH607729208032, 6'434 m²"],
    ["Zone", "Arbeitszone (A) / Zone für publikumsintensive Nutzungen (PiN), ES IV"],
    ["Landerwerb", "CHF 13'000'000 (gemäss Angebot)"],
    ["Gesamtinvestition", "CHF 70.0 Mio. (indikativ)"],
    ["Stand", "20. Juli 2026 · Version 1.0 · VERTRAULICH"],
]
t = Table([[Paragraph(f"<b>{a}</b>", styles["TblCell"]), Paragraph(b, styles["TblCell"])] for a, b in meta],
          colWidths=[38*mm, 106*mm])
t.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, GOLD),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3E9C8")),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(PageBreak())

# ---------------------------------------------------------------- Inhalt
story.append(P("Inhalt", "H1x"))
toc = [
    ("1", "Executive Summary"), ("2", "Standort und Grundstück (ÖREB-Analyse)"),
    ("3", "Regulatorischer Rahmen"), ("4", "Architektur- und Nutzungskonzept"),
    ("5", "Raffinerie: Technologie und Kapazität"), ("6", "Gold-Bunker: Hochsicherheits-Wertlager"),
    ("7", "Security House und Sicherheitskonzept"), ("8", "Investitionsrechnung"),
    ("9", "Ertragsmodell und Finanzplan"), ("10", "Organisation und Personal"),
    ("11", "Terminplan und Projektphasen"), ("12", "Risikoanalyse"),
    ("13", "Anhang: ÖREB-Kernauszug und Disclaimer"),
]
for n, ti in toc:
    story.append(P(f"<b>{n}.</b>&nbsp;&nbsp;{ti}", "Body"))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=0.6, color=GOLD))
story.append(Spacer(1, 6))
story.append(P("Alle Finanzangaben in Schweizer Franken (CHF). Bei den dargestellten Zahlen handelt es sich um "
               "indikative Planwerte auf Basis von Erfahrungs- und Richtwerten; sie sind im Rahmen der "
               "Detailplanung durch Offerten, Gutachten und behördliche Vorabklärungen zu erhärten.", "Small"))
story.append(PageBreak())

# ---------------------------------------------------------------- 1 Executive Summary
story.append(P("1.  Executive Summary", "H1x"))
story.append(P(
    "Die AURUM HELVETIA AG (in Gründung) plant auf der Parzelle 61522 in Frauenfeld (Kanton Thurgau) die "
    "Errichtung eines integrierten <b>Edelmetall-Raffinations- und Wertlagerzentrums</b>. Das Projekt umfasst "
    "drei Baukörper: eine <b>Goldraffinerie</b> mit einer Ausbaukapazität von rund 100 Tonnen Gold-Äquivalent "
    "pro Jahr, einen <b>Hochsicherheits-Goldbunker</b> (Tresoranlage der höchsten Widerstandsklassen nach "
    "EN 1143-1) mit einer Einlagerungskapazität von bis zu 200 Tonnen sowie ein <b>Security House</b> als "
    "permanent besetzte Sicherheitsleitstelle und einzigen kontrollierten Zugangspunkt des Areals."))
story.append(P(
    "Der Standort ist aussergewöhnlich gut geeignet: Das 6'434 m² grosse Grundstück liegt vollständig in der "
    "<b>Arbeitszone (A)</b> mit <b>Lärmempfindlichkeitsstufe IV</b> — der einzigen Stufe, in der stark störende "
    "(industrielle) Betriebe zulässig sind. Es bestehen weder Grundwasserschutzzonen noch Einträge im Kataster "
    "der belasteten Standorte. Die unmittelbare Nähe zur Nationalstrasse A7 (Zürich–Konstanz) ermöglicht "
    "schnelle, planbare Werttransporte; die Distanz zum Flughafen Zürich beträgt rund 40 Minuten."))
story.append(P("Eckwerte des Vorhabens:", "H2x"))
for x in [
    "Landerwerb: CHF 13.0 Mio. (6'434 m², entspricht rund CHF 2'020/m²).",
    "Gesamtinvestition: rund CHF 70 Mio. inkl. Land, Bau, Prozess- und Sicherheitstechnik.",
    "Finanzierung: 40 % Eigenkapital (CHF 28 Mio.), 60 % Fremdkapital (CHF 42 Mio.).",
    "Umsatzziel im Vollbetrieb (Planjahr 3): rund CHF 33 Mio.; EBITDA-Marge rund 50 %.",
    "Break-even auf Stufe EBT im zweiten Betriebsjahr; Amortisation innert 8–10 Jahren.",
    "Geschäftsfelder: Lohnraffination (Doré, Recycling, Bankengold), Vaulting/Wertlagerung, "
    "Logistik- und Zertifizierungsdienstleistungen.",
    "Zielzertifizierungen: Bewilligungen nach Edelmetallkontrollgesetz, SRO/GwG-Anschluss, "
    "mittelfristig LBMA Good Delivery.",
]:
    story.append(B(x))
story.append(P(
    "Die Schweiz raffiniert heute einen erheblichen Teil des weltweit gehandelten Goldes; die bestehenden "
    "Kapazitäten konzentrieren sich auf wenige Standorte (v. a. Tessin, Wallis, Neuenburg). Ein moderner, "
    "kompakt geplanter Standort in der Ostschweiz mit integriertem Hochsicherheitslager adressiert die "
    "wachsende Nachfrage nach <b>rückverfolgbarem, verantwortungsvoll raffiniertem Gold</b> sowie nach "
    "<b>bankenunabhängiger physischer Lagerung</b> für institutionelle und private Kunden."))

story.append(PageBreak())

# ---------------------------------------------------------------- 2 Standort
story.append(P("2.  Standort und Grundstück (ÖREB-Analyse)", "H1x"))
story.append(P(
    "Grundlage dieses Kapitels ist der amtliche Auszug aus dem Kataster der öffentlich-rechtlichen "
    "Eigentumsbeschränkungen (ÖREB-Kataster) vom 20.07.2026, Auszugsnummer 94e6ede8-6f45-4c08-8312-848c71110089, "
    "erstellt durch das Amt für Geoinformation des Kantons Thurgau."))
story.append(tbl([
    ["Merkmal", "Befund", "Bewertung für das Projekt"],
    ["Grundstück", "Nr. 61522, Liegenschaft, E-GRID CH607729208032, Gemeinde Frauenfeld (BFS 8500)", "Eindeutig identifiziert, Liegenschaft im Baugebiet"],
    ["Fläche", "6'434 m²", "Ausreichend für Raffinerie, Bunker, Security House, Logistik und Reserven"],
    ["Nutzungszone", "Arbeitszone (A), 100 % — überlagert mit Zone für publikumsintensive Nutzungen (PiN), 100 %", "Industriell-gewerbliche Nutzung zonenkonform; PiN eröffnet Optionen (z. B. Schalterhalle/Showroom)"],
    ["Lärmempfindlichkeit", "Empfindlichkeitsstufe IV, 100 %", "Stark störende Betriebe zulässig — ideal für Schmelz- und Raffinationsbetrieb mit 24/7-Technik"],
    ["Baulinienplan", "Baulinienplan rechtskräftig, 100 % der Parzelle", "Gebäudestellung entlang der Baulinien zu koordinieren (Gemeinde)"],
    ["Baulinien Nationalstrasse", "Baulinie in Kraft über 107 m", "Streifen entlang A7 von Hochbauten freihalten bzw. ASTRA-Zustimmung nötig; im Arealkonzept als Freifläche berücksichtigt"],
    ["Grundwasserschutz", "Keine Schutzzonen/-areale auf der Parzelle", "Kein erhöhtes Auflagenrisiko für Chemie-/Prozessbereiche"],
    ["Belastete Standorte", "Kein Eintrag im KbS", "Kein Altlasten-Kostenrisiko erkennbar (Restrisiko via Due Diligence prüfen)"],
    ["Weitere Themen", "Gewässerraum/Waldabstand: keine Daten bzw. nicht betroffen", "Keine projektrelevanten Einschränkungen ersichtlich"],
], [30*mm, 62*mm, 78*mm]))
story.append(P("Lage- und Markteinschätzung", "H2x"))
story.append(P(
    "Die Parzelle liegt im Entwicklungsgebiet Langfeld-/Ost-/Juchstrasse in Frauenfeld Ost, unmittelbar am "
    "Anschluss an die A7. Für einen Betrieb mit täglichen Werttransporten ist die direkte "
    "Autobahnanbindung ein zentraler Sicherheits- und Effizienzfaktor: kurze, variierbare Routen, keine "
    "Ortsdurchfahrten mit Zwangshalten. Frauenfeld bietet als Kantonshauptstadt qualifizierte Arbeitskräfte, "
    "Nähe zu Polizeistützpunkten (Kantonspolizei Thurgau) und im Grossraum Zürich/Winterthur ein "
    "Rekrutierungsfeld für Fachpersonal (Chemie, Metallurgie, Sicherheit, Compliance)."))
story.append(P(
    "Der Kaufpreis von <b>CHF 13.0 Mio.</b> entspricht rund <b>CHF 2'020/m²</b>. Für voll erschlossenes, "
    "unbelastetes Arbeitszonenland mit Autobahnanschluss in der Achse Winterthur–Frauenfeld liegt dieser Wert "
    "im oberen, aber vertretbaren Marktbereich; die Zonierung (ES IV, PiN-Überlagerung) und die planungs- "
    "rechtliche «Sauberkeit» des Grundstücks rechtfertigen eine Prämie gegenüber gewöhnlichem Gewerbeland."))

story.append(PageBreak())

# ---------------------------------------------------------------- 3 Regulatorik
story.append(P("3.  Regulatorischer Rahmen", "H1x"))
story.append(P(
    "Der Betrieb einer Goldraffinerie mit Wertlager ist in der Schweiz umfassend reguliert. Die folgenden "
    "Bewilligungen und Rahmenbedingungen sind projektbestimmend und werden in der Terminplanung (Kap. 11) "
    "als kritischer Pfad geführt:"))
story.append(tbl([
    ["Bereich", "Grundlage", "Anforderung / Massnahme"],
    ["Edelmetallkontrolle", "Edelmetallkontrollgesetz (EMKG, SR 941.31) und Verordnung", "Schmelzbewilligung sowie Bewilligung als Handelsprüfer beim Zentralamt für Edelmetallkontrolle (BAZG); Voraussetzung für Feingold-Produktion mit amtlicher Stempelung"],
    ["Geldwäscherei", "GwG (SR 955.0), GwV", "Der gewerbsmässige Handel mit Bankedelmetallen erfordert Anschluss an eine SRO bzw. FINMA-Unterstellung; Aufbau eines Compliance-Systems (KYC, Herkunftsnachweis, Transaktionsmonitoring)"],
    ["Verantwortungsvolle Beschaffung", "LBMA Responsible Gold Guidance, OECD Due Diligence Guidance", "Lieferketten-Sorgfaltsprüfung ab Tag 1; mittelfristig Akkreditierung LBMA Good Delivery (Voraussetzung u. a. 3 Jahre Betrieb, Mindestproduktion, Assaying-Kompetenz)"],
    ["Umwelt / Luft", "USG, Luftreinhalte-Verordnung (LRV)", "Abluftreinigung (Wäscher, Filter) für Schmelze und nasschemische Prozesse; Emissionserklärung und Abnahmemessungen"],
    ["Chemikalien / Störfall", "ChemG, ChemV, Störfallverordnung (StFV)", "Lager- und Einsatzkonzept für Säuren und Prozessgase; Unterschreitung bzw. Beherrschung der Mengenschwellen, Kurzbericht nach StFV"],
    ["Gewässerschutz", "GSchG, GSchV", "Abwasserneutralisation und Metallrückgewinnung; Indirekteinleiter-Bewilligung des Kantons"],
    ["Arbeitssicherheit", "ArG, UVG / Suva-Richtlinien (EKAS)", "Sicherheits- und Gesundheitsschutzkonzept, Explosionsschutz, PSA, betriebsärztliche Betreuung"],
    ["Baurecht", "PBG/PBV TG, Baureglement Frauenfeld (DBU 65), Zonenplan 1987 inkl. Sonderbauvorschriften", "Ordentliches Baubewilligungsverfahren; frühzeitige Bauvoranfrage; Abstimmung Baulinien (Gemeinde und ASTRA für den Nationalstrassen-Baulinienbereich)"],
    ["Versicherung", "Marktstandard (Lloyd's u. a.)", "All-Risk-/Specie-Deckung für Lager und Transporte; versicherungstechnische Abnahme der Tresoranlage als Voraussetzung der Deckungszusage"],
], [34*mm, 50*mm, 86*mm]))
story.append(P(
    "<b>Einschätzung:</b> Keine der Anforderungen steht dem Projekt am gewählten Standort entgegen. "
    "Zonenkonformität und ES IV reduzieren das Einspracherisiko wesentlich; die kritischen Zeitpfade sind das "
    "Baubewilligungsverfahren (inkl. ASTRA-Koordination) und die EMKG-Bewilligungen."))

story.append(PageBreak())

# ---------------------------------------------------------------- 4 Architektur
story.append(P("4.  Architektur- und Nutzungskonzept", "H1x"))
story.append(P(
    "Das Arealkonzept folgt dem Prinzip <b>«Sicherheit durch Struktur»</b>: ein einziger kontrollierter "
    "Zugang über das Security House, klar getrennte Verkehrsflüsse (Personal / Besucher / Werttransport / "
    "Material), gestaffelte Sicherheitszonen von aussen nach innen und der Bunker als innerster, allseitig "
    "geschützter Kern ohne direkte Aussenfassade zum öffentlichen Raum. Der Baulinienbereich entlang der "
    "Nationalstrasse (107 m) bleibt von Hochbauten frei und wird als Grün-/Sickerfläche genutzt."))
story.append(Spacer(1, 4))
story.append(site_plan())
story.append(PageBreak())
story.append(P("Raumprogramm (Hauptnutzflächen, indikativ)", "H2x"))
story.append(tbl([
    ["Baukörper", "Nutzung", "Fläche (m²)"],
    ["Raffinerie (2 Geschosse, ca. 1'400 m² Grundfläche)", "Schmelzerei/Giesserei, nasschemische Scheidung, Elektrolyse, Probenahme/Labor (Assaying), Abluft-/Abwassertechnik, Werkstatt, Garderoben, Büros, Technikzentrale", "2'600 BGF"],
    ["Gold-Bunker (2 Ebenen, davon 1 Untergeschoss)", "Tresorkammern (Kunden-Segregation), Schleusen, Zähl- und Prüfräume, Schliessfachbereich (Option), Technik autark", "900 BGF"],
    ["Security House (2 Geschosse)", "Leitstelle 24/7, Personen- und Fahrzeugschleuse, Empfang/Identifikation, Sozialräume Sicherheitsdienst, Serverraum (redundant)", "350 BGF"],
    ["Logistik-/WTU-Schleuse", "Geschlossene Fahrzeugschleuse für gepanzerte Fahrzeuge, Umschlag unter Dach, direkte Anbindung an Raffinerie und Bunker", "300 BGF"],
    ["Aussenanlagen", "Rangier- und Parkierflächen, Perimeterzone, Grün-/Retentionsflächen (inkl. Baulinienstreifen)", "ca. 3'800"],
], [52*mm, 88*mm, 30*mm], aligns=[None, None, "R"]))
story.append(P("Architektonische Leitlinien", "H2x"))
for x in [
    "Kompakte, fensterarme Volumen in Sichtbeton mit vorgehängter Metallfassade; Tageslicht über "
    "shedartige Oblichter in nicht sicherheitskritischen Bereichen.",
    "Raffinerie als flexibler Hallenbau (Raster 8 × 8 m) mit Kranbahn und installationsstarker "
    "Technikzone; Erweiterungsreserve für eine zweite Elektrolyse-Linie eingeplant.",
    "Bunker in Massivbauweise (Stahlbeton-Spezialrezeptur mit Zuschlagstoffen erhöhter "
    "Durchbruchhemmung), vollständig erdüberschüttete Sohlebene, weitgehend öffnungslose Fassaden; "
    "nach aussen nicht als Wertlager erkennbar.",
    "Security House als «Gesicht» des Areals: repräsentativ, aber wehrhaft — Empfang, Identifikation "
    "und Vereinzelung in einem Baukörper.",
    "Nachhaltigkeit: PV-Anlage auf allen Dachflächen (Ziel > 500 kWp), Abwärmenutzung der Schmelzöfen "
    "für Gebäudeheizung, Regenwasser-Retention im Baulinienstreifen; Zielstandard Minergie (Verwaltungsteile).",
]:
    story.append(B(x))

story.append(PageBreak())

# ---------------------------------------------------------------- 5 Raffinerie
story.append(P("5.  Raffinerie: Technologie und Kapazität", "H1x"))
story.append(P(
    "Die Raffinerie wird als moderne Lohnraffinerie («toll refining») für Gold und Silber ausgelegt, mit "
    "Fokus auf drei Inputströme: Doré-Barren aus Minenproduktion (nachweislich verantwortungsvolle Herkunft), "
    "Recyclingmaterial (Altgold, Produktionsabfälle, Elektronikschrott-Konzentrate) sowie Umschmelzung und "
    "Feinung von Bankengold (Good-Delivery-Umarbeitung, Formatwechsel)."))
story.append(P("Prozesskette", "H2x"))
story.append(tbl([
    ["Stufe", "Verfahren", "Zweck"],
    ["Eingang & Probenahme", "Wareneingang in der WTU-Schleuse, Verwiegung, Bohr-/Schmelzprobe, Röntgenfluoreszenz- und Feuerassay im eigenen Labor", "Verbindliche Gehaltsbestimmung als Abrechnungsbasis («settlement»)"],
    ["Schmelzen & Homogenisieren", "Induktionsöfen mit gekapselter Absaugung", "Homogenes Vormaterial, Probenehmen, Entfernen von Verunreinigungen"],
    ["Vorraffination", "Miller-Prozess (Chlorierung in der Schmelze) für hohe Durchsätze", "Schnelle Anhebung auf ca. 99.5 % Au; Silber/Basismetalle in die Schlacken-/Chloridphase"],
    ["Feinraffination", "Wohlwill-Elektrolyse; ergänzend nasschemische Scheidung (Königswasser) für komplexe Vorstoffe", "Feingold 999.9; Rückgewinnung von Silber und Platingruppenmetallen aus Anodenschlämmen"],
    ["Giessen & Prägen", "Barrengiesserei (Guss 1 kg – 12.5 kg), Prägelinie für Kleinbarren 1 g – 100 g", "Marktfähige Endprodukte mit Seriennummer, Zertifikat und amtlicher Punzierung"],
    ["Umweltstufe", "Mehrstufige Abgaswäscher (Chlor-/NOx-Wäsche), Filtration, Abwasserneutralisation mit Metallrückgewinnung", "Einhaltung LRV/GSchV; Rückgewinnung von Wertmetallen aus allen Nebenströmen"],
], [30*mm, 76*mm, 64*mm]))
story.append(P("Kapazität und Auslastungspfad", "H2x"))
for x in [
    "Technische Ausbaukapazität: rund 100 t Gold-Äquivalent pro Jahr (2-Schicht-Betrieb, "
    "Erweiterung auf 150 t durch dritte Schicht und zweite Elektrolyse-Linie möglich).",
    "Auslastungspfad: Planjahr 1 rund 15 t (Inbetriebnahme, Testläufe, Erstkunden), Planjahr 2 "
    "rund 40 t, Planjahr 3 rund 60 t, danach 70–80 t.",
    "Labor mit Feuerassay und Spektrometrie als eigenes Profitcenter (Fremdanalytik, Schiedsanalysen).",
    "Qualitätsziel: Feingold 999.9 mit lückenloser Chargenrückverfolgung (Track-and-Trace bis zum "
    "Inputlos) — zentrales Verkaufsargument gegenüber Banken und Grosshändlern.",
]:
    story.append(B(x))
story.append(P(
    "<b>Sicherheits- und Umweltvorteil des Standorts:</b> Die Lärmempfindlichkeitsstufe IV erlaubt "
    "durchgehenden Betrieb der Öfen und Lüftungsanlagen; die fehlende Grundwasserschutz-Überlagerung "
    "vereinfacht die Bewilligung der nasschemischen Prozesse erheblich. Die Störfallvorsorge (Chlorgas des "
    "Miller-Prozesses, Säurelager) wird durch gekapselte Systeme, Gaswarnanlagen und getrennte, "
    "auffangwannengesicherte Lagerräume mit Neutralisationsvorhalt adressiert."))

story.append(PageBreak())

# ---------------------------------------------------------------- 6 Bunker
story.append(P("6.  Gold-Bunker: Hochsicherheits-Wertlager", "H1x"))
story.append(P(
    "Der Bunker ist als eigenständiges Profitcenter konzipiert: physische Lagerung («vaulting») für Banken, "
    "Vermögensverwalter, Family Offices, Edelmetallhändler und — im Rahmen der PiN-Zonierung — ausgewählte "
    "Privatkunden. Die Anlage wird zoll- und mehrwertsteuerlich als offenes Zolllager (OZL) geprüft, um "
    "internationale Kunden bedienen zu können."))
story.append(P("Bauliche und technische Auslegung", "H2x"))
for x in [
    "Tresoranlage nach EN 1143-1, Zielwiderstandsgrad der höchsten am Markt versicherbaren Klassen "
    "(Grad X bis XIII, mit EX- und CD-Zusatz gegen Sprengstoff- und Kernbohrangriffe); definitive "
    "Klassifizierung in Abstimmung mit den Specie-Versicherern.",
    "Zwei Tresorebenen: Untergeschoss vollständig erdüberdeckt (Hauptlager, Palettenlogistik für "
    "Grossbarren), Erdgeschossebene für Kundensegregate, Zähl-/Prüfräume und optionalen Schliessfachbereich.",
    "Monolithische Stahlbetonhülle mit erhöhter Durchbruchhemmung, aussenliegend unauffällig (keine "
    "sichtbare Kennzeichnung als Wertlager), Zugänge ausschliesslich über Schleusen aus dem Inneren des Areals.",
    "Autarke Technik: unabhängige Strom-, Kühl- und Kommunikationsversorgung, Netzersatzanlage, "
    "redundante Alarmübertragungswege.",
    "Kapazität: bis zu 200 t Gold (belegungsabhängig), zuzüglich Silber-/Palettenlager im Logistiktrakt.",
]:
    story.append(B(x))
story.append(P("Betriebsmodell und Erlöse", "H2x"))
story.append(tbl([
    ["Dienstleistung", "Zielkunden", "Preismodell (indikativ)"],
    ["Segregierte Lagerung (allocated)", "Banken, Fonds, Family Offices", "0.10 – 0.20 % p. a. des Lagerwerts, inkl. Audit-Zugang"],
    ["Sammellagerung Barrenbestand", "Händler, Raffinationskunden", "0.08 – 0.12 % p. a., kombinierbar mit Raffinationsverträgen"],
    ["Schliessfächer (Option, PiN-konform)", "Private, KMU", "Fixpreise nach Fachgrösse, Zugang über Security House"],
    ["Handling & Logistik", "Alle Segmente", "Ein-/Auslagerungsgebühren, Zählen/Prüfen, Umschlag WTU"],
], [48*mm, 52*mm, 70*mm]))
story.append(P(
    "Die Kombination von Raffinerie und Lager am selben Standort ist ein struktureller Wettbewerbsvorteil: "
    "Frisch raffiniertes Feingold kann ohne externen Transport direkt eingelagert werden («mint-to-vault»), "
    "was Versicherungs- und Transportkosten senkt und ein geschlossenes Sicherheits- und "
    "Nachweissystem vom Schmelzlos bis zum Lagerplatz ermöglicht."))

story.append(PageBreak())

# ---------------------------------------------------------------- 7 Sicherheit
story.append(P("7.  Security House und Sicherheitskonzept", "H1x"))
story.append(P(
    "Das Sicherheitskonzept folgt dem international etablierten <b>Zwiebelschalen-Prinzip</b> mit fünf "
    "gestaffelten Zonen und durchgängiger Vier-Augen-Organisation. Es wird mit Kantonspolizei Thurgau, "
    "Versicherern und einer akkreditierten Zertifizierungsstelle abgestimmt und periodisch auditiert."))
story.append(tbl([
    ["Zone", "Bereich", "Massnahmen (Auszug)"],
    ["0 — Umfeld", "Öffentlicher Raum, Zufahrt", "Unauffällige Aussenwirkung, verkehrsberuhigte Zufahrt, Weitbereichs-Videoanalyse, Kennzeichenerfassung an der Zufahrt"],
    ["1 — Perimeter", "Grundstücksgrenze", "Zaun-/Mauersystem 3 m mit Übersteig- und Untergrabschutz, Detektionssensorik (Zaun, Boden, Thermik), Fahrzeugrückhaltesysteme (zertifizierte Poller/Barrieren) an der Einfahrt"],
    ["2 — Areal", "Aussenflächen innerhalb Perimeter", "Lückenlose Videoüberwachung mit Analytik, Beleuchtungskonzept, Wegeführung mit Vereinzelung, Drohnendetektion"],
    ["3 — Gebäude", "Raffinerie, Logistik, Security House", "Einbruchhemmende Hülle (Widerstandsklassen RC5/RC6 an kritischen Öffnungen), Personen- und Fahrzeugschleusen, Mehrfaktor-Zutritt (Ausweis + Biometrie + PIN), EMA nach EN 50131 Grad 4"],
    ["4 — Kernzone", "Tresoranlage, Feingoldlager", "Tresortüren und -kammern EN 1143-1 (höchste Grade), zeitverzögerte Mehrpersonen-Öffnung, seismische und körperschallbasierte Detektion, separate Alarmlinien, Zutritt nur im Vier-Augen-Prinzip mit protokollierter Freigabe durch die Leitstelle"],
], [24*mm, 42*mm, 104*mm]))
story.append(P("Security House (Herzstück des Betriebs)", "H2x"))
for x in [
    "Permanent besetzte Leitstelle (24/7, mindestens zwei Operatoren), redundante Aufschaltung auf eine "
    "zertifizierte Alarmempfangsstelle und die Kantonspolizei.",
    "Einziger Zugangspunkt für Personen und Fahrzeuge: Identifikation, Besucherverwaltung, "
    "Vereinzelungsschleusen, Waffen-/Metalldetektion, getrennte Warteräume.",
    "Führung sämtlicher Werttransporte: Avisierung, Slot-Vergabe, Routen- und Fensterkoordination mit "
    "den WTU-Partnern; kein Transport ohne bestätigten Slot.",
    "Krisen- und Notfallorganisation: Interventionskonzept mit der Polizei, Sabotage- und "
    "Brandfallszenarien, Business-Continuity-Plan, jährliche Übungen.",
    "Datenschutzkonforme Videoarchivierung (revDSG), Zutritts- und Ereignisprotokollierung mit "
    "manipulationssicherer Speicherung.",
]:
    story.append(B(x))
story.append(P(
    "<b>Personelle Sicherheit:</b> Alle Mitarbeitenden durchlaufen eine Personensicherheitsprüfung "
    "(Betreibungs-/Strafregister, Referenzen), sicherheitskritische Funktionen zusätzlich periodische "
    "Re-Checks. Funktionstrennung (Produktion / Lager / Compliance / Sicherheit) und rotierende "
    "Zuständigkeiten reduzieren Innentäter-Risiken. Details zu Widerstandszeiten, Interventionszeiten und "
    "Alarmphilosophie werden bewusst nur im vertraulichen Sicherheitspflichtenheft geführt."))

story.append(PageBreak())

# ---------------------------------------------------------------- 8 Investition
story.append(P("8.  Investitionsrechnung", "H1x"))
story.append(P(
    "Die Investitionsschätzung basiert auf Kostenkennwerten vergleichbarer Industrie- und "
    "Hochsicherheitsbauten (Genauigkeit ± 20 %, Preisbasis 2026). Sie ist in der Vorprojektphase durch "
    "Unternehmerofferten zu verifizieren."))
story.append(tbl([
    ["Position", "Annahme / Basis", "CHF Mio."],
    ["Landerwerb Parzelle 61522", "6'434 m² gemäss Angebot", "13.00"],
    ["Erwerbsnebenkosten", "Handänderungssteuer, Notariat, Grundbuch (ca. 2.3 %)", "0.30"],
    ["Raffineriegebäude", "2'600 m² BGF, hochinstallierter Industriebau, ca. CHF 4'800/m²", "12.50"],
    ["Gold-Bunker", "900 m² BGF Spezialbau inkl. Tresorkammern, ca. CHF 12'800/m²", "11.50"],
    ["Security House", "350 m² BGF inkl. Schleusenanlagen", "1.80"],
    ["Logistik-/WTU-Schleuse, Umgebung, Perimeter", "Fahrzeugschleuse, Zaun-/Detektionssystem, Poller, Rangierflächen", "2.60"],
    ["Prozess- und Ofentechnik", "Induktionsöfen, Miller-Linie, Wohlwill-Elektrolyse, Scheidung, Giesserei/Prägung, Abluft/Abwasser", "14.00"],
    ["Sicherheitstechnik", "EMA Grad 4, Video/Analytik, Zutritt/Biometrie, Leitstellentechnik, Redundanzen", "4.20"],
    ["Labor- und Betriebseinrichtung", "Assaying (Feuerprobe, Spektrometrie), IT/ERP, Track-and-Trace", "2.20"],
    ["Planung, Bewilligungen, Honorare", "ca. 12 % der Bau-/Anlagekosten", "3.40"],
    ["Unvorhergesehenes", "ca. 7 % Reserve", "4.50"],
    ["**Gesamtinvestition", "", "**70.00"],
], [56*mm, 84*mm, 24*mm], aligns=[None, None, "R"], bold_last=True))
story.append(P("Finanzierung", "H2x"))
story.append(tbl([
    ["Quelle", "Anteil", "CHF Mio.", "Bemerkung"],
    ["Eigenkapital (Gründer, Ankerinvestoren)", "40 %", "28.0", "Zeichnung in zwei Tranchen (Kauf/Planung, Bau)"],
    ["Hypothekar-/Investitionskredit", "50 %", "35.0", "Besichert durch Land und Gebäude; Zinsannahme 2.8 %"],
    ["Lieferanten-/Leasingfinanzierung Anlagen", "10 %", "7.0", "Ofen- und Elektrolysetechnik", ],
], [62*mm, 18*mm, 22*mm, 62*mm], aligns=[None, "R", "R", None]))
story.append(P(
    "Der Landerwerb (CHF 13.0 Mio.) wird vollständig aus der ersten Eigenkapitaltranche finanziert, damit das "
    "Grundstück unbelastet als Kreditsicherheit für die Bauphase zur Verfügung steht."))

story.append(PageBreak())

# ---------------------------------------------------------------- 9 Finanzplan
story.append(P("9.  Ertragsmodell und Finanzplan", "H1x"))
story.append(P("Erlösquellen im Vollbetrieb (Planjahr 3)", "H2x"))
story.append(tbl([
    ["Erlösquelle", "Mengengerüst", "CHF Mio."],
    ["Lohnraffination Gold/Silber", "60 t Durchsatz × Ø CHF 0.40/g Raffinationsertrag", "24.0"],
    ["Recycling-/Scheidgutmarge", "Mehrertrag aus komplexen Vorstoffen und Nebenmetallen (Ag, PGM)", "3.5"],
    ["Vaulting / Lagerung", "Ø 40 t eingelagert × Ø 0.12 % p. a. auf Lagerwert (Annahme CHF 90/g)", "4.3"],
    ["Nebenerlöse", "Analytik, Zertifikate, Logistik/Handling, Prägeaufträge", "1.2"],
    ["**Gesamtumsatz Planjahr 3", "", "**33.0"],
], [56*mm, 84*mm, 24*mm], aligns=[None, None, "R"], bold_last=True))
story.append(P("Fünfjahresplan (indikativ, CHF Mio.)", "H2x"))
story.append(tbl([
    ["Position", "Jahr 1", "Jahr 2", "Jahr 3", "Jahr 4", "Jahr 5"],
    ["Durchsatz Raffination (t)", "15", "40", "60", "70", "78"],
    ["Umsatz", "8.0", "19.5", "33.0", "38.5", "42.0"],
    ["Betriebsaufwand (inkl. Personal, Energie, Versicherung)", "9.5", "13.7", "16.5", "18.7", "20.1"],
    ["EBITDA", "-1.5", "5.8", "16.5", "19.8", "21.9"],
    ["Abschreibungen", "3.3", "3.5", "3.5", "3.5", "3.5"],
    ["Finanzaufwand", "1.2", "1.2", "1.2", "1.1", "1.0"],
    ["**Ergebnis vor Steuern (EBT)", "**-6.0", "**1.1", "**11.8", "**15.2", "**17.4"],
], [66*mm, 19*mm, 19*mm, 19*mm, 19*mm, 19*mm],
    aligns=[None, "R", "R", "R", "R", "R"]))
story.append(P("Wesentliche Planannahmen", "H2x"))
for x in [
    "Goldpreisannahme konservativ CHF 90'000/kg für die Bewertung der Lagerbestände; das Erlösmodell "
    "ist überwiegend mengen-, nicht preisgetrieben (Gebührengeschäft, kein Eigenhandel mit offenen Positionen).",
    "Personalaufbau von 28 Vollzeitstellen (Jahr 1) auf 58 (Jahr 3); durchschnittliche Vollkosten "
    "CHF 120'000 pro Stelle.",
    "Versicherungsprämien (Specie/All-Risk) mit 0.9 – 1.4 % des durchschnittlichen Lagerwerts "
    "kalkuliert; sinkend mit Schadenshistorie und Zertifizierungsfortschritt.",
    "Working Capital bleibt gering, da Kundenmaterial im Fremdeigentum raffiniert und gelagert wird "
    "(Lohnveredelung); Metallkonti werden täglich glattgestellt.",
    "Steuersatz Kanton Thurgau/Bund kombiniert rund 13.5 % — im internationalen Vergleich attraktiv.",
    "Break-even auf Stufe EBT im Jahr 2; kumulativ positiver freier Cashflow ab Jahr 5; "
    "Projektamortisation (inkl. Land) innert 8 – 10 Jahren.",
]:
    story.append(B(x))

story.append(PageBreak())

# ---------------------------------------------------------------- 10 Organisation
story.append(P("10.  Organisation und Personal", "H1x"))
story.append(tbl([
    ["Bereich", "Aufgaben", "VZÄ Jahr 1", "VZÄ Jahr 3"],
    ["Geschäftsleitung & Stab", "CEO, CFO, Recht/Compliance (GwG-Fachstelle), HR", "4", "6"],
    ["Produktion Raffinerie", "Schmelzerei, Scheidung, Elektrolyse, Giesserei (2-Schicht)", "10", "22"],
    ["Labor / Qualität", "Assaying, QS, Zertifizierung, Track-and-Trace", "3", "6"],
    ["Sicherheit / Leitstelle", "24/7-Leitstelle, Schleusenbetrieb, Werttransport-Koordination", "8", "14"],
    ["Lager / Logistik (Bunker)", "Ein-/Auslagerung, Kundensegregate, Inventuren", "2", "6"],
    ["Vertrieb & Kundenmanagement", "Minen-, Banken- und Recyclingkunden, Vaulting-Vertrieb", "1", "4"],
    ["**Total", "", "**28", "**58"],
], [44*mm, 84*mm, 18*mm, 18*mm], aligns=[None, None, "R", "R"], bold_last=True))
story.append(P(
    "Schlüsselrekrutierungen sind der Raffineriebetriebsleiter (Metallurgie, Erfahrung in einer "
    "Good-Delivery-Raffinerie), der Leiter Sicherheit (Hintergrund Polizei/Armee/WTU-Industrie) und der "
    "GwG-Compliance-Officer. Für die 24/7-Leitstelle wird ein Mischmodell aus eigenem Personal und einem "
    "vertraglich gebundenen, zertifizierten Sicherheitsdienstleister geprüft; die Hoheit über Alarm- und "
    "Freigabeprozesse verbleibt in jedem Fall intern."))
story.append(P("Rechtsform und Governance", "H2x"))
for x in [
    "Aktiengesellschaft nach schweizerischem Recht, Sitz Frauenfeld; Verwaltungsrat mit unabhängigen "
    "Mitgliedern (Finanz, Recht, Sicherheit).",
    "Internes Kontrollsystem ab Tag 1; jährliche externe Audits (Finanz, GwG, Sicherheit, Umwelt).",
    "Vier-Augen-Prinzip in allen wertrelevanten Prozessen; kein Einzelzugriff auf Kernzonen.",
]:
    story.append(B(x))

story.append(Spacer(1, 6))
story.append(P("11.  Terminplan und Projektphasen", "H1x"))
story.append(tbl([
    ["Phase", "Zeitraum", "Meilensteine"],
    ["0 — Sicherung & Due Diligence", "Q3 – Q4 2026", "Kaufvertrag/Beurkundung Parzelle 61522, technische und rechtliche Due Diligence, Bauvoranfrage, Gründung AG, EK-Tranche 1"],
    ["1 — Planung & Bewilligung", "Q1 2027 – Q2 2028", "Vorprojekt/Bauprojekt (SIA-Phasen 31/32), Umwelt- und Störfallnachweise, Baugesuch, ASTRA-Abstimmung Baulinie, EMKG-Gesuche, Versicherer-Abnahmekonzept"],
    ["2 — Realisierung", "Q3 2028 – Q4 2029", "Aushub/Rohbau (Bunker zuerst), Ausbau, Montage Prozess- und Sicherheitstechnik, Werksabnahmen"],
    ["3 — Inbetriebnahme", "Q1 – Q3 2030", "Kalt-/Warm-Inbetriebnahme, Emissionsmessungen, Schmelz- und Handelsprüferbewilligung aktiv, Versicherungsabnahme Tresor, Erstkunden-Chargen"],
    ["4 — Hochlauf & Zertifizierung", "ab Q4 2030", "2-Schicht-Betrieb, SRO-Audit, Aufbau LBMA-Track-Record (Ziel Good Delivery nach 3 Betriebsjahren)"],
], [40*mm, 32*mm, 92*mm]))

story.append(PageBreak())

# ---------------------------------------------------------------- 12 Risiken
story.append(P("12.  Risikoanalyse", "H1x"))
story.append(tbl([
    ["Risiko", "E*", "A*", "Gegenmassnahmen"],
    ["Verzögerung Baubewilligung / Einsprachen", "mittel", "mittel", "Zonenkonformität (Arbeitszone, ES IV) minimiert Angriffsflächen; frühe Bauvoranfrage; transparente Information von Stadt und Nachbarschaft"],
    ["Auflagen Baulinie Nationalstrasse (ASTRA)", "mittel", "tief", "Arealkonzept hält Baulinienstreifen frei; frühzeitige Vorabstimmung mit ASTRA"],
    ["EMKG-/GwG-Bewilligungen verzögert", "tief", "hoch", "Erfahrene Compliance-Beratung, vollständige Gesuche, Rekrutierung geprüfter Schlüsselpersonen vor Gesuchstellung"],
    ["Baukostenüberschreitung", "mittel", "mittel", "Reserveposition 7 %, GU-/TU-Vergabe mit Kostendach, Etappierung der Ausbauten"],
    ["Marktrisiko: Raffinationsmargen unter Druck", "mittel", "mittel", "Differenzierung über Rückverfolgbarkeit, Ostschweizer Standortvorteil, Kombiangebot Raffination + Lagerung; Mehrjahresverträge mit Ankerkunden"],
    ["Sicherheitsereignis (Überfall, Einbruch, Innentäter)", "tief", "sehr hoch", "Gestaffeltes Zonenkonzept, höchste Tresorklassen, Vier-Augen-Prinzip, Personalprüfungen, Versicherungsdeckung, Interventionsvereinbarung mit Kantonspolizei"],
    ["Umwelt-/Störfallereignis", "tief", "hoch", "Gekapselte Prozesse, Gaswarn- und Neutralisationssysteme, StFV-Kurzbericht, regelmässige Übungen"],
    ["Reputationsrisiko Lieferkette", "mittel", "hoch", "OECD-konforme Sorgfaltsprüfung, Annahme nur auditierter Herkünfte, externes Responsible-Sourcing-Audit ab Jahr 1"],
    ["Zins-/Finanzierungsrisiko", "mittel", "mittel", "Langfristige Zinsbindung, gestaffelte EK-Tranchen, Covenant-Puffer"],
], [46*mm, 14*mm, 16*mm, 88*mm]))
story.append(P("*E = Eintretenswahrscheinlichkeit, A = Auswirkung", "Small"))
story.append(P(
    "Gesamtbeurteilung: Das Projekt weist ein für Hochsicherheits-Industrieprojekte typisches, aber durch "
    "Standortwahl, Zonenkonformität und konsequente Sicherheitsarchitektur gut beherrschbares Risikoprofil "
    "auf. Kein identifiziertes Einzelrisiko ist projektverhindernd."))

story.append(Spacer(1, 8))
story.append(P("13.  Anhang: ÖREB-Kernauszug und Disclaimer", "H1x"))
story.append(tbl([
    ["ÖREB-Auszug (amtlich)", "Angabe"],
    ["Auszugsnummer / Datum", "94e6ede8-6f45-4c08-8312-848c71110089 / 20.07.2026"],
    ["Grundstück", "Nr. 61522, Liegenschaft, Gemeinde Frauenfeld (BFS 8500)"],
    ["E-GRID", "CH607729208032"],
    ["Fläche", "6'434 m² (Stand amtliche Vermessung 16.07.2026)"],
    ["Betroffene ÖREB-Themen", "Nutzungsplanung: Arbeitszone (A) 100 %, Zone für publikumsintensive Nutzungen (PiN) 100 % · Baulinienplan 100 % · Baulinien Nationalstrassen: Baulinie in Kraft, 107 m · Lärmempfindlichkeitsstufe IV, 100 %"],
    ["Nicht betroffen (Auswahl)", "Grundwasserschutzzonen und -areale, Kataster der belasteten Standorte, Gestaltungsplan, Planungszonen, Wald-Themen"],
    ["Massgebliche Rechtsgrundlagen", "RPG (SR 700), PBG/PBV TG (RB 700/700.1), Baureglement Frauenfeld DBU 65, Zonenplan 1987 (Nr. 548) inkl. Sonderbauvorschriften, Zonenplan Langfeld-/Ost-/Juchstrasse (Nr. 88, 2009), NSG/NSV, LSV"],
    ["Katasterverantwortliche Stelle", "Amt für Geoinformation Kanton Thurgau, Staubeggstrasse 3, 8510 Frauenfeld"],
], [52*mm, 112*mm], head=True))
story.append(Spacer(1, 6))
story.append(P(
    "<b>Disclaimer:</b> Dieser Businessplan ist eine Projektstudie und dient ausschliesslich der internen "
    "Entscheidungsvorbereitung sowie Gesprächen mit qualifizierten Investoren, Banken, Behörden und "
    "Versicherern. Sämtliche Kosten-, Erlös- und Terminangaben sind indikative Planwerte (Genauigkeit "
    "± 20 %) und ersetzen weder Offerten noch Gutachten oder behördliche Auskünfte. Der ÖREB-Auszug hat rein "
    "informativen Charakter und begründet keine Rechte und Pflichten; massgeblich sind die rechtskräftig "
    "verabschiedeten Dokumente. Angaben zu Sicherheitsmassnahmen sind bewusst generisch gehalten; "
    "einsatzrelevante Details werden ausschliesslich im vertraulichen Sicherheitspflichtenheft geführt.", "Small"))

doc = Doc(OUT)

from reportlab.platypus import NextPageTemplate
final_story = [NextPageTemplate("Std")] + story
doc.build(final_story)
print("OK:", OUT)
