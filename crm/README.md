# OffMarket CRM

Ein schlankes CRM für die **Off-Market-Immobilienakquise**: Objekt-Pipeline, Eigentümer- und
Tippgeberkontakte, Aufgaben und Auswertungen. Reines Frontend — statisches HTML, CSS und
Vanilla JavaScript, kein Build-Schritt, keine Abhängigkeiten, kein Server.

Aufrufen: [`/crm/`](./) — z. B. lokal über `python3 -m http.server` und dann
<http://localhost:8000/crm/>.

## Funktionsumfang

| Bereich | Inhalt |
| --- | --- |
| **Übersicht** | KPI-Kacheln (aktive Deals, Pipeline-Volumen, Ø Ankaufsfaktor, Abschlussquote), Pipeline nach Phase, heute fällige Aufgaben, Top-Deals nach gewichtetem Volumen, Aktivitätenverlauf, neue Objekte je Monat |
| **Pipeline** | Kanban-Board über acht Phasen (Recherche → Erstkontakt → Besichtigung → Angebot/LOI → Verhandlung → Notartermin → Angekauft / Verloren) mit Drag & Drop, Spaltensummen |
| **Objekte** | Sortierbare Tabelle mit Volltextsuche und Filtern (Objektart, Phase, Betreuer, nur offene), CSV-Export der gefilterten Auswahl |
| **Objekt-Detail** | Phasenwechsel per Klick, Kennzahlen (Faktor, Bruttorendite, Preis je m², gewichtetes Volumen), Notizen, verknüpfte Aufgaben, Aktivitäten-Timeline, Eigentümerkarte mit Telefon-/Mail-Link |
| **Kontakte** | Eigentümer, Makler, Tippgeber, Investoren, Verwalter — inkl. Anzahl und Volumen der verknüpften Objekte |
| **Kontakt-Detail** | Stammdaten, verknüpfte Objekte, Aufgaben, Verlauf |
| **Aufgaben** | Gruppiert nach überfällig / heute / diese Woche / später / erledigt, mit Priorität, Typ und Verknüpfung zu Objekt und Kontakt |
| **Auswertungen** | Funnel nach Phase, Volumen nach Objektart (Donut) und Standort, Quellen-Performance mit Abschlussquote, Team-Performance, 12-Monats-Verlauf, Druckansicht |
| **Einstellungen** | Profil, Zielfaktor, Design (hell/dunkel/System), JSON-Export und -Import, CSV-Exporte, Demo-Datensatz, Daten löschen |

Weitere Details: globale Suche über Objekte, Kontakte und Aufgaben (<kbd>/</kbd>), Tastenkürzel
<kbd>N</kbd> für ein neues Objekt, Undo-Toasts nach dem Löschen, responsives Layout mit
Mobil-Navigation, helles und dunkles Design.

## Kennzahlen

Aus Kaufpreis und Jahresmiete (IST) werden automatisch abgeleitet:

- **Faktor** = Kaufpreis ÷ Jahresmiete
- **Bruttorendite** = Jahresmiete ÷ Kaufpreis × 100
- **Preis je m²** = Kaufpreis ÷ Wohn-/Nutzfläche
- **Gewichtetes Volumen** = Kaufpreis × Abschlusswahrscheinlichkeit (aus der Phase vorbelegt)

## Datenhaltung

Alle Daten liegen ausschließlich im **localStorage** des Browsers (Schlüssel
`offmarket-crm-v1`) — nichts wird übertragen, es gibt keine Anmeldung und kein Backend.
Beim ersten Start wird ein Demo-Datensatz mit 15 Objekten, 10 Kontakten und 14 Aufgaben geladen.

Für Backup oder Gerätewechsel: **Einstellungen → JSON-Export** bzw. **JSON-Import**.

## Struktur

```
crm/
  index.html          Layout-Shell (Sidebar, Topbar, Container)
  assets/
    crm.css           Design-Tokens, Layout, Komponenten (hell + dunkel)
    data.js           Stammdaten (Phasen, Objektarten, Rollen …), Icons, Demo-Datensatz
    store.js          Zustand, localStorage-Persistenz, CRUD, Kennzahlen, Import/Export
    ui.js             Formatierung (de-DE), Modal, Toasts, SVG-Diagramme
    forms.js          Formulare für Objekt, Kontakt, Aufgabe, Aktivität
    views.js          Die neun Ansichten
    app.js            Hash-Router, Navigation, Theme, Tastenkürzel, CSV-Export
    favicon.svg
```

Die Skripte laden als klassische `<script>`-Tags in fester Reihenfolge und kommunizieren über
die globalen Objekte `CRMData`, `Store`, `UI`, `Forms`, `Views` und `App` — dadurch läuft die
Anwendung auch direkt per `file://`, ohne Modul-Bundler.

## Routen

`#/dashboard` · `#/pipeline` · `#/objekte` · `#/objekt/<id>` · `#/kontakte` ·
`#/kontakt/<id>` · `#/aufgaben` · `#/berichte` · `#/einstellungen` · `#/suche/<begriff>`

## Hosting

Statische Dateien — deploybar auf Vercel, Netlify, GitHub Pages oder jedem Webserver.
Bei einem Deployment des Repository-Roots ist das CRM unter `/crm/` erreichbar; soll es unter
der Domain-Wurzel liegen, genügt es, den Ordnerinhalt ins Root zu legen (es gibt keine
absoluten Pfade).
