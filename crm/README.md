# OffMarket CRM

Ein schlankes CRM für **Off-Market-Deals aller Anlageklassen** — Immobilien, Edelmetalle,
Energie und Öl, Krypto, Rohstoffe, Unternehmensbeteiligungen, Fahrzeuge und Maschinen sowie
Kunst und Sammlerstücke. Mit Deal-Pipeline, Kontakten, Aufgaben, **Gesprächsprotokollen** und
Auswertungen. Reines Frontend — statisches HTML, CSS und Vanilla JavaScript, kein Build-Schritt,
keine Abhängigkeiten, kein Server.

Aufrufen: [`/crm/`](./) — z. B. lokal über `python3 -m http.server` und dann
<http://localhost:8000/crm/>.

## Funktionsumfang

| Bereich | Inhalt |
| --- | --- |
| **Übersicht** | KPI-Kacheln (aktive Deals, Pipeline-Volumen, erwartete Marge, Abschlussquote), Pipeline nach Phase, Volumen nach Anlageklasse, Top-Deals, heutige Aufgaben, letzte Protokolle, Aktivitätenverlauf |
| **Pipeline** | Kanban über acht Phasen (Recherche → Erstkontakt → Prüfung/DD → Angebot/LOI → Verhandlung → Vertrag/Closing → Abgeschlossen / Verloren) mit Drag & Drop und Spaltensummen |
| **Deals** | Sortierbare Tabelle mit Volltextsuche und Filtern (Kategorie, Phase, Betreuer, nur offene), CSV-Export der gefilterten Auswahl |
| **Deal-Detail** | Phasenwechsel per Klick, Kennzahlen, kategoriespezifische Fachdaten, Notizen, Protokolle, Aufgaben, Aktivitäten-Timeline, Gegenpartei mit Telefon- und Mail-Link |
| **Protokolle** | Gesprächsprotokolle mit fortlaufender Nummer, Statusworkflow, Maßnahmenliste, druckbarer Dokumentansicht und Textexport — siehe unten |
| **Kontakte** | Verkäufer, Käufer, Vermittler, Tippgeber und Dienstleister mit verknüpften Deals und Protokollen |
| **Aufgaben** | Gruppiert nach überfällig / heute / diese Woche / später / erledigt, mit Priorität, Typ und Bezug zu Deal, Kontakt und Protokoll |
| **Auswertungen** | Funnel nach Phase, Volumen nach Anlageklasse (Donut) und Land, Anlageklassen im Vergleich, Quellen- und Team-Performance, Protokolle und neue Deals je Monat, Druckansicht |
| **Einstellungen** | Profil, Standard-Protokollführung, Design (hell/dunkel/System), JSON-Export und -Import, CSV-Exporte, Demo-Datensatz, Daten löschen |

Weitere Details: globale Suche über Deals, Kontakte, Protokolle und Aufgaben (<kbd>/</kbd>),
Tastenkürzel <kbd>N</kbd> für einen neuen Deal und <kbd>P</kbd> für ein neues Protokoll,
Undo-Toasts nach dem Löschen, responsives Layout mit Mobil-Navigation, helles und dunkles Design.

## Anlageklassen und Fachfelder

Jede Kategorie bringt eigene Fachfelder mit, die im Formular und in der Detailansicht
automatisch erscheinen (gespeichert unter `deal.details`). Auch die Beschriftungen passen sich
an — aus „Kaufpreis“ wird bei Rohstoffen „Kontraktwert“, aus „Fläche“ wird „Menge“.

| Kategorie | Beispiele für Fachfelder |
| --- | --- |
| Immobilien | Objektart, Einheiten, Baujahr, Zustand, Grundstück, Jahresmiete |
| Edelmetalle | Metall, Feingehalt, Form (LBMA-Barren, Münzen, Doré …), Lagerort, Assay, Übergabe |
| Energie & Öl | Produkt (Brent, EN590, Jet A-1, LNG …), Incoterm, Verladeort, Laufzeit, Zahlungsinstrument, Inspektion |
| Krypto & Digital Assets | Asset, Netzwerk, Discount zum Spot, Verwahrung, Settlement, KYC/AML-Status, Herkunftsnachweis |
| Rohstoffe & Waren | Produkt, Spezifikation, Incoterm, Lieferort, Lieferrhythmus, Zahlungsinstrument |
| Unternehmensbeteiligung | Branche, Umsatz, Mitarbeitende, Struktur (Share/Asset Deal), Anlass |
| Fahrzeuge & Maschinen | Hersteller/Modell, Baujahr, Zustand, Standort, Papiere |
| Kunst & Sammlerstücke | Künstler/Marke, Werk, Entstehungsjahr, Provenienz, Echtheitszertifikat |

## Kennzahlen

Aus Volumen, Menge, laufendem Ertrag und erwarteter Marge werden automatisch abgeleitet:

- **Preis je Einheit** = Volumen ÷ Menge (€/kg, €/Barrel, €/BTC, €/m² …)
- **Marge in %** = erwartete Marge ÷ Volumen
- **Faktor** = Volumen ÷ Jahresertrag (Miete, EBITDA, Staking-Ertrag)
- **Rendite** = Jahresertrag ÷ Volumen
- **Gewichtetes Volumen / gewichtete Marge** = Wert × Abschlusswahrscheinlichkeit der Phase

## Protokolle

Das Protokollmodul ist für die Assistenz gedacht, die Gespräche nach dem Termin dokumentiert.

- **Kopfdaten**: fortlaufende Nummer (`P-2026-0001`), Datum, Uhrzeit, Dauer, Gesprächsart
  (Telefonat, Videokonferenz, Vor-Ort-Termin, Messe, E-Mail, interne Besprechung), Bezug zu
  Deal und Kontakt, Teilnehmerliste, Protokollführung und Freigabe.
- **Inhalt**: besprochene Punkte, Ergebnisse und Vereinbarungen, offene Punkte — auf Wunsch
  über die Schaltfläche „Gliederung einfügen“ mit einer vorbereiteten Struktur.
- **Nächste Schritte**: beliebig viele Maßnahmen mit Verantwortlichem und Termin. Per
  Häkchen werden daraus **automatisch Aufgaben**, die im Aufgabenmodul und beim Deal
  auftauchen und auf das Protokoll zurückverweisen. Bereits übernommene Maßnahmen werden
  markiert und nicht doppelt angelegt.
- **Statusworkflow**: Entwurf → Final → Freigegeben; Freigaben landen im Aktivitätenverlauf
  des Deals. Protokolle lassen sich als vertraulich kennzeichnen.
- **Ausgabe**: druckbare Dokumentansicht mit Briefkopf und Unterschriftszeilen
  („Drucken / PDF“), Textexport in die Zwischenablage sowie CSV-Export aller Protokolle.

## Datenhaltung

Alle Daten liegen ausschließlich im **localStorage** des Browsers (Schlüssel
`offmarket-crm-v2`) — nichts wird übertragen, es gibt keine Anmeldung und kein Backend.
Beim ersten Start wird ein Demo-Datensatz mit 21 Deals aus acht Anlageklassen, 14 Kontakten,
15 Aufgaben und 5 Protokollen geladen.

Ein Datenbestand der früheren, rein immobilienbezogenen Version (`offmarket-crm-v1`) wird beim
ersten Start **automatisch migriert**: Objekte werden zu Deals der Kategorie „Immobilien“,
Kaufpreis zu Volumen, Jahresmiete zu Ertrag, objektspezifische Angaben wandern in die
Fachfelder; Kontaktrollen und Phasen werden auf das neue Schema abgebildet.

Für Backup oder Gerätewechsel: **Einstellungen → JSON-Export** bzw. **JSON-Import**.

## Struktur

```
crm/
  index.html          Layout-Shell (Sidebar, Topbar, Container)
  assets/
    crm.css           Design-Tokens, Layout, Komponenten, Protokoll-Dokument, Druckansicht
    data.js           Phasen, Anlageklassen samt Fachfeldern, Rollen, Icons, Demo-Datensatz
    store.js          Zustand, localStorage-Persistenz inkl. Migration, CRUD, Kennzahlen, Export
    ui.js             Formatierung (de-DE), Modal, Toasts, SVG-Diagramme, Zwischenablage
    forms.js          Formulare für Deal (kategorieabhängig), Kontakt, Aufgabe, Protokoll, Notiz
    views.js          Die elf Ansichten
    app.js            Hash-Router, Navigation, Theme, Tastenkürzel, CSV-Exporte
    favicon.svg
```

Die Skripte laden als klassische `<script>`-Tags in fester Reihenfolge und kommunizieren über
die globalen Objekte `CRMData`, `Store`, `UI`, `Forms`, `Views` und `App` — dadurch läuft die
Anwendung auch direkt per `file://`, ohne Modul-Bundler.

## Routen

`#/dashboard` · `#/pipeline` · `#/deals` · `#/deal/<id>` · `#/kontakte` · `#/kontakt/<id>` ·
`#/protokolle` · `#/protokoll/<id>` · `#/aufgaben` · `#/berichte` · `#/einstellungen` ·
`#/suche/<begriff>`

## Hosting

Statische Dateien — deploybar auf Vercel, Netlify, GitHub Pages oder jedem Webserver.
Bei einem Deployment des Repository-Roots ist das CRM unter `/crm/` erreichbar; soll es unter
der Domain-Wurzel liegen, genügt es, den Ordnerinhalt ins Root zu legen (es gibt keine
absoluten Pfade).
