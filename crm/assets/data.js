/* Deal CRM — Stammdaten, Kategorien, Icons und Demo-Datensatz */
(function (global) {
  "use strict";

  /* ---------------- Phasen ---------------- */
  var STAGES = [
    { id: "recherche",   label: "Recherche",        color: "#94a3b8", prob: 10 },
    { id: "erstkontakt", label: "Erstkontakt",      color: "#38bdf8", prob: 20 },
    { id: "pruefung",    label: "Prüfung / DD",     color: "#818cf8", prob: 40 },
    { id: "angebot",     label: "Angebot / LOI",    color: "#a78bfa", prob: 60 },
    { id: "verhandlung", label: "Verhandlung",      color: "#fb923c", prob: 75 },
    { id: "closing",     label: "Vertrag / Closing", color: "#eab308", prob: 90 },
    { id: "gewonnen",    label: "Abgeschlossen",    color: "#22c55e", prob: 100 },
    { id: "verloren",    label: "Verloren",         color: "#ef4444", prob: 0 }
  ];

  /* ---------------- Deal-Kategorien ----------------
     Jede Kategorie bringt eigene Fachfelder mit, die im Formular und in der
     Detailansicht dynamisch ergänzt werden (gespeichert unter deal.details). */
  var KATEGORIEN = [
    {
      id: "immobilie", label: "Immobilien", icon: "building", farbe: "#4f6df5",
      volumenLabel: "Kaufpreis (€)",
      mengeLabel: "Fläche", mengeEinheiten: ["m²", "ha"],
      ertragLabel: "Jahresmiete IST (€)",
      felder: [
        { k: "objektart", label: "Objektart", typ: "select", optionen: ["Mehrfamilienhaus", "Wohn- und Geschäftshaus", "Eigentumswohnung", "Einfamilienhaus", "Grundstück", "Gewerbeimmobilie", "Pflegeimmobilie", "Hotel"] },
        { k: "wohneinheiten", label: "Einheiten", typ: "number" },
        { k: "baujahr", label: "Baujahr", typ: "number" },
        { k: "zustand", label: "Zustand", typ: "select", optionen: ["Neuwertig", "Gepflegt", "Renovierungsbedarf", "Sanierungsbedarf", "Entkernt"] },
        { k: "grundstueck", label: "Grundstück (m²)", typ: "number" }
      ]
    },
    {
      id: "edelmetall", label: "Edelmetalle", icon: "coins", farbe: "#d4a017",
      volumenLabel: "Transaktionsvolumen (€)",
      mengeLabel: "Menge", mengeEinheiten: ["kg", "t", "oz (Feinunzen)", "Barren", "Münzen"],
      ertragLabel: "",
      felder: [
        { k: "metall", label: "Metall", typ: "select", optionen: ["Gold", "Silber", "Platin", "Palladium", "Rhodium"] },
        { k: "reinheit", label: "Feingehalt", typ: "text", platzhalter: "z. B. 999,9" },
        { k: "form", label: "Form", typ: "select", optionen: ["Barren (LBMA Good Delivery)", "Barren (non-LBMA)", "Münzen", "Granulat", "Doré", "Schmuckscheidgut"] },
        { k: "lagerort", label: "Lager- / Verwahrort", typ: "text", platzhalter: "Zollfreilager Zürich" },
        { k: "zertifikat", label: "Assay / Zertifikat", typ: "text" },
        { k: "lieferung", label: "Übergabe", typ: "select", optionen: ["Abholung Zollfreilager", "Versicherter Transport", "Loco London", "Serial-Number-Ledger", "Sichtprüfung vor Ort"] }
      ]
    },
    {
      id: "energie", label: "Energie & Öl", icon: "droplet", farbe: "#0f766e",
      volumenLabel: "Kontraktwert (€)",
      mengeLabel: "Menge", mengeEinheiten: ["Barrel", "t", "m³", "MWh", "Liter", "t/Monat"],
      ertragLabel: "",
      felder: [
        { k: "produkt", label: "Produkt", typ: "select", optionen: ["Brent Crude", "WTI", "Diesel EN590", "Jet A-1 / JP54", "Heizöl", "LNG", "LPG", "Bitumen", "Strom"] },
        { k: "incoterm", label: "Incoterm", typ: "select", optionen: ["FOB", "CIF", "CFR", "DAP", "EXW", "TTO (Tank-to-Tank)", "TTV (Tank-to-Vessel)"] },
        { k: "verladeort", label: "Verlade- / Lieferort", typ: "text", platzhalter: "Rotterdam ARA" },
        { k: "laufzeit", label: "Vertragslaufzeit", typ: "text", platzhalter: "12 Monate rollierend" },
        { k: "zahlung", label: "Zahlungsinstrument", typ: "select", optionen: ["SBLC", "DLC / LC at sight", "MT103 TT", "Escrow", "Vorkasse", "Cash against Documents"] },
        { k: "inspektion", label: "Inspektion", typ: "text", platzhalter: "SGS / Saybolt" }
      ]
    },
    {
      id: "krypto", label: "Krypto & Digital Assets", icon: "bitcoin", farbe: "#f7931a",
      volumenLabel: "Transaktionsvolumen (€)",
      mengeLabel: "Menge", mengeEinheiten: ["BTC", "ETH", "USDT", "USDC", "SOL", "Token"],
      ertragLabel: "Staking-Ertrag p. a. (€)",
      felder: [
        { k: "asset", label: "Asset", typ: "text", platzhalter: "BTC" },
        { k: "netzwerk", label: "Netzwerk / Chain", typ: "text", platzhalter: "Bitcoin, Ethereum, Tron …" },
        { k: "discount", label: "Discount zum Spot (%)", typ: "number" },
        { k: "verwahrung", label: "Verwahrung", typ: "select", optionen: ["OTC-Desk", "Qualified Custodian", "Multisig-Wallet", "Exchange", "Cold Storage"] },
        { k: "settlement", label: "Settlement", typ: "select", optionen: ["Escrow", "T+0 OTC", "Bank-Escrow", "Atomic Swap", "Tranchenweise"] },
        { k: "kyc", label: "KYC / AML-Status", typ: "select", optionen: ["offen", "Unterlagen angefordert", "in Prüfung", "abgeschlossen", "abgelehnt"] },
        { k: "sof", label: "Herkunftsnachweis (SoF)", typ: "text" }
      ]
    },
    {
      id: "rohstoff", label: "Rohstoffe & Waren", icon: "box", farbe: "#7c5cf0",
      volumenLabel: "Kontraktwert (€)",
      mengeLabel: "Menge", mengeEinheiten: ["t", "kg", "Container", "m³", "Sack", "t/Monat"],
      ertragLabel: "",
      felder: [
        { k: "produkt", label: "Produkt", typ: "text", platzhalter: "Kupferkathoden Grade A" },
        { k: "qualitaet", label: "Spezifikation / Qualität", typ: "text", platzhalter: "LME Grade A, 99,99 %" },
        { k: "incoterm", label: "Incoterm", typ: "select", optionen: ["FOB", "CIF", "CFR", "DAP", "EXW", "FCA"] },
        { k: "lieferort", label: "Lieferort", typ: "text" },
        { k: "rhythmus", label: "Lieferrhythmus", typ: "text", platzhalter: "monatlich, 12 Tranchen" },
        { k: "zahlung", label: "Zahlungsinstrument", typ: "select", optionen: ["SBLC", "DLC / LC at sight", "MT103 TT", "Escrow", "Cash against Documents"] }
      ]
    },
    {
      id: "beteiligung", label: "Unternehmensbeteiligung", icon: "briefcase", farbe: "#0d8bd9",
      volumenLabel: "Kaufpreis (€)",
      mengeLabel: "Anteil", mengeEinheiten: ["%", "Anteile"],
      ertragLabel: "EBITDA p. a. (€)",
      felder: [
        { k: "branche", label: "Branche", typ: "text" },
        { k: "umsatz", label: "Jahresumsatz (€)", typ: "number" },
        { k: "mitarbeiter", label: "Mitarbeitende", typ: "number" },
        { k: "struktur", label: "Struktur", typ: "select", optionen: ["Share Deal", "Asset Deal", "Mehrheit", "Minderheit", "Earn-out-Modell"] },
        { k: "anlass", label: "Anlass", typ: "select", optionen: ["Nachfolge", "Wachstumsfinanzierung", "Distressed", "Carve-out", "Exit"] }
      ]
    },
    {
      id: "fahrzeug", label: "Fahrzeuge & Maschinen", icon: "truck", farbe: "#e0453c",
      volumenLabel: "Kaufpreis (€)",
      mengeLabel: "Stückzahl", mengeEinheiten: ["Stück", "Flotte", "Posten"],
      ertragLabel: "Leasingertrag p. a. (€)",
      felder: [
        { k: "hersteller", label: "Hersteller / Modell", typ: "text" },
        { k: "baujahr", label: "Baujahr", typ: "number" },
        { k: "zustand", label: "Zustand", typ: "select", optionen: ["Neu", "Gebraucht – top", "Gebraucht", "Reparaturbedarf", "Ersatzteilträger"] },
        { k: "standort", label: "Standort", typ: "text" },
        { k: "papiere", label: "Papiere / Zulassung", typ: "text" }
      ]
    },
    {
      id: "kunst", label: "Kunst & Sammlerstücke", icon: "palette", farbe: "#be185d",
      volumenLabel: "Kaufpreis (€)",
      mengeLabel: "Stückzahl", mengeEinheiten: ["Stück", "Konvolut", "Lot"],
      ertragLabel: "",
      felder: [
        { k: "kuenstler", label: "Künstler / Marke", typ: "text" },
        { k: "werk", label: "Werk / Objekt", typ: "text" },
        { k: "jahr", label: "Entstehungsjahr", typ: "number" },
        { k: "provenienz", label: "Provenienz", typ: "text" },
        { k: "zertifikat", label: "Echtheitszertifikat", typ: "text" }
      ]
    },
    {
      id: "sonstiges", label: "Sonstiges", icon: "star", farbe: "#6b7385",
      volumenLabel: "Volumen (€)",
      mengeLabel: "Menge", mengeEinheiten: ["Einheiten", "Stück", "Posten"],
      ertragLabel: "Laufender Ertrag p. a. (€)",
      felder: [
        { k: "beschreibung", label: "Kurzbeschreibung", typ: "text" }
      ]
    }
  ];

  var KONTAKTTYPEN = [
    { id: "verkaeufer",   label: "Verkäufer / Eigentümer", cls: "pill-accent" },
    { id: "kaeufer",      label: "Käufer / Investor",      cls: "pill-green" },
    { id: "vermittler",   label: "Vermittler / Broker",    cls: "pill-sky" },
    { id: "tippgeber",    label: "Tippgeber",              cls: "pill-violet" },
    { id: "dienstleister", label: "Dienstleister",         cls: "pill-amber" },
    { id: "sonstige",     label: "Sonstige",               cls: "" }
  ];

  var QUELLEN = [
    "Direktansprache",
    "Tippgeber",
    "Netzwerk",
    "Broker / Makler",
    "Bestandskunde",
    "Messe / Konferenz",
    "Empfehlung",
    "Plattform / Portal",
    "Ausschreibung / Auktion"
  ];

  var AUFGABENTYPEN = [
    { id: "anruf",  label: "Anruf",       icon: "phone" },
    { id: "email",  label: "E-Mail",      icon: "mail" },
    { id: "termin", label: "Termin",      icon: "calendar" },
    { id: "dokument", label: "Dokument",  icon: "file" },
    { id: "pruefung", label: "Prüfung",   icon: "search" },
    { id: "todo",   label: "To-do",       icon: "check" }
  ];

  var PRIORITAETEN = [
    { id: "hoch",    label: "Hoch",    cls: "pill-red" },
    { id: "mittel",  label: "Mittel",  cls: "pill-amber" },
    { id: "niedrig", label: "Niedrig", cls: "" }
  ];

  /* ---------------- Protokolle ---------------- */
  var KANAELE = [
    { id: "telefon",  label: "Telefonat",     icon: "phone" },
    { id: "video",    label: "Videokonferenz", icon: "video" },
    { id: "vorort",   label: "Vor-Ort-Termin", icon: "pin" },
    { id: "messe",    label: "Messe / Event",  icon: "users" },
    { id: "email",    label: "E-Mail-Verkehr", icon: "mail" },
    { id: "intern",   label: "Interne Besprechung", icon: "note" }
  ];

  var PROTOKOLL_STATUS = [
    { id: "entwurf",    label: "Entwurf",    cls: "pill-amber" },
    { id: "final",      label: "Final",      cls: "pill-sky" },
    { id: "freigegeben", label: "Freigegeben", cls: "pill-green" }
  ];

  var PROTOKOLL_VORLAGE =
    "1. Anlass und Ausgangslage\n   – \n\n" +
    "2. Besprochene Punkte\n   – \n   – \n\n" +
    "3. Offene Punkte / Risiken\n   – ";

  var TEAM = [
    { name: "Anna Berger",  rolle: "Partnerin" },
    { name: "Jonas Weiss",  rolle: "Deal Manager" },
    { name: "Mira Kohl",    rolle: "Deal Managerin" },
    { name: "Sven Faber",   rolle: "Analyst" },
    { name: "Lena Sommer",  rolle: "Assistenz" }
  ];

  var TEAM_NAMEN = TEAM.map(function (t) { return t.name; });

  /* ---------------- Icons (24er Grid, currentColor) ---------------- */
  var ICONS = {
    dashboard: '<path d="M4 13h6V4H4v9Zm0 7h6v-5H4v5Zm10 0h6v-9h-6v9Zm0-16v5h6V4h-6Z"/>',
    building:  '<path d="M4 21V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16M14 21V9h5a1 1 0 0 1 1 1v11M3 21h18M7 8h3M7 12h3M7 16h3M17 13h1M17 17h1"/>',
    kanban:    '<path d="M4 4h4v12H4zM10 4h4v7h-4zM16 4h4v16h-4z"/>',
    users:     '<path d="M16 20v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M9.5 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7ZM21 20v-1a4 4 0 0 0-3-3.87M16.5 4.13a4 4 0 0 1 0 7.75"/>',
    check:     '<path d="m4 12 5 5L20 6"/>',
    chart:     '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    settings:  '<path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.1A1.7 1.7 0 0 0 8.9 19.3a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.1A1.7 1.7 0 0 0 4.7 8.9a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.55V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.55 1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9v.1a1.7 1.7 0 0 0 1.55 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>',
    search:    '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    plus:      '<path d="M12 5v14M5 12h14"/>',
    edit:      '<path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    trash:     '<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v5M14 11v5"/>',
    phone:     '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    mail:      '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
    calendar:  '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
    file:      '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/>',
    protokoll: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M8.5 13h7M8.5 17h4"/>',
    pin:       '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
    euro:      '<path d="M17 5.5A6.5 6.5 0 0 0 7.2 9M17 18.5A6.5 6.5 0 0 1 7.2 15M4 10.5h8M4 13.5h8"/>',
    flame:     '<path d="M12 22a7 7 0 0 0 7-7c0-5-4-6-4-10-3 1-5 3.5-5 6 0 1.5-1 2-1.5 1.2C7 11 6.5 9.8 6.5 9A7.6 7.6 0 0 0 5 15a7 7 0 0 0 7 7Z"/>',
    clock:     '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    download:  '<path d="M12 3v12M7 11l5 5 5-5M4 21h16"/>',
    upload:    '<path d="M12 21V9M7 13l5-5 5 5M4 3h16"/>',
    close:     '<path d="M6 6l12 12M18 6 6 18"/>',
    menu:      '<path d="M4 7h16M4 12h16M4 17h16"/>',
    sun:       '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon:      '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/>',
    back:      '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    star:      '<path d="m12 3 2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-3-5.3 3 1.1-6L3.4 9.4l6-.8L12 3Z"/>',
    note:      '<path d="M4 4h16v12l-4 4H4z"/><path d="M20 16h-4v4"/>',
    coins:     '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v5c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 11v5c0 1.7 3.6 3 8 3s8-1.3 8-3v-5"/>',
    droplet:   '<path d="M12 3s6 6.2 6 10a6 6 0 0 1-12 0c0-3.8 6-10 6-10Z"/>',
    bitcoin:   '<circle cx="12" cy="12" r="9"/><path d="M9.5 8h4a2 2 0 1 1 0 4h-4Zm0 4h4.5a2 2 0 1 1 0 4H9.5Zm0-4V6.5m0 11V16m3-9.5V6.5m0 11V16"/>',
    box:       '<path d="m12 3 8 4.2v9.6L12 21l-8-4.2V7.2Z"/><path d="M4 7.2 12 11.5l8-4.3M12 11.5V21"/>',
    briefcase: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 12h18"/>',
    truck:     '<path d="M3 16V6h11v10M14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>',
    palette:   '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 2-.9 2-2 0-.5-.2-1-.6-1.3-.3-.4-.5-.8-.5-1.2 0-1 .8-1.8 1.8-1.8H16a5 5 0 0 0 5-5c0-3.9-4-6.7-9-6.7Z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7.5" r="1"/><circle cx="14.5" cy="7.5" r="1"/>',
    video:     '<rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 10 6-3v10l-6-3z"/>',
    print:     '<path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2M6 14h12v7H6z"/>',
    copy:      '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    lock:      '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    arrowRight: '<path d="M5 12h14M13 6l6 6-6 6"/>'
  };

  /* ---------------- Demo-Daten ---------------- */
  function daysAgo(n) {
    var d = new Date();
    d.setHours(9, 0, 0, 0);
    d.setDate(d.getDate() - n);
    return d.toISOString();
  }
  function dayIn(n) {
    var d = new Date();
    d.setHours(9, 0, 0, 0);
    d.setDate(d.getDate() + n);
    return d.toISOString().slice(0, 10);
  }
  function dateAgo(n) {
    var d = new Date();
    d.setDate(d.getDate() - n);
    return d.toISOString().slice(0, 10);
  }

  function seed() {
    var kontakte = [
      { id: "k1",  vorname: "Helga",    nachname: "Brandt",      typ: "verkaeufer",   firma: "",                            email: "h.brandt@web.de",          telefon: "+49 341 2298431",  strasse: "Lindenauer Markt 8",  plz: "04177", ort: "Leipzig",    land: "Deutschland", notizen: "Erbengemeinschaft, verkauft ungern über Makler.",            tags: ["Erbfall"],     createdAt: daysAgo(190) },
      { id: "k2",  vorname: "Ralf",     nachname: "Osterhage",   typ: "verkaeufer",   firma: "Osterhage GbR",               email: "info@osterhage-gbr.de",    telefon: "+49 511 4478120",  strasse: "Podbielskistr. 144",  plz: "30177", ort: "Hannover",   land: "Deutschland", notizen: "Portfolio-Abverkauf über zwei Jahre geplant.",               tags: ["Portfolio"],   createdAt: daysAgo(163) },
      { id: "k3",  vorname: "Sabine",   nachname: "Kruse",       typ: "tippgeber",    firma: "Kruse Hausverwaltung",        email: "s.kruse@kruse-hv.de",      telefon: "+49 40 87654321",  strasse: "Eppendorfer Weg 12",  plz: "20259", ort: "Hamburg",    land: "Deutschland", notizen: "Liefert regelmäßig Tipps, 1 % Provision vereinbart.",        tags: ["Top-Quelle"],  createdAt: daysAgo(410) },
      { id: "k4",  vorname: "Dr. Peter", nachname: "Lang",       typ: "kaeufer",      firma: "Lang Family Office",          email: "p.lang@lang-fo.de",        telefon: "+49 89 21098765",  strasse: "Maximilianstr. 35",   plz: "80539", ort: "München",    land: "Deutschland", notizen: "Sucht Sachwerte ab 3 Mio. €, auch Edelmetall-Tranchen.",     tags: ["Kapital"],     createdAt: daysAgo(240) },
      { id: "k5",  vorname: "Marc",     nachname: "Baumgartner", typ: "vermittler",   firma: "Helvetic Metals AG",          email: "m.baumgartner@helvetic-metals.ch", telefon: "+41 44 5520188", strasse: "Bahnhofstrasse 24", plz: "8001", ort: "Zürich",  land: "Schweiz",     notizen: "Zugang zu LBMA-Raffinerie und Zollfreilager Zürich.",        tags: ["LBMA"],        createdAt: daysAgo(120) },
      { id: "k6",  vorname: "Amina",    nachname: "Osei",        typ: "verkaeufer",   firma: "Accra Gold Traders Ltd.",     email: "a.osei@accragold.gh",      telefon: "+233 30 2761100",  strasse: "Independence Ave 14", plz: "GA-107", ort: "Accra",     land: "Ghana",       notizen: "Doré-Gold, Herkunftsnachweise noch unvollständig.",          tags: ["Compliance"],  createdAt: daysAgo(64) },
      { id: "k7",  vorname: "Hendrik",  nachname: "van Dijk",    typ: "vermittler",   firma: "Rotterdam Fuel Brokers B.V.", email: "h.vandijk@rfb.nl",         telefon: "+31 10 4433221",  strasse: "Wilhelminakade 90",   plz: "3072", ort: "Rotterdam",  land: "Niederlande", notizen: "Mandat für EN590 und Jet A-1, arbeitet nur mit SBLC.",       tags: ["ARA"],         createdAt: daysAgo(98) },
      { id: "k8",  vorname: "Yuki",     nachname: "Tanaka",      typ: "kaeufer",      firma: "Meridian OTC Desk",           email: "y.tanaka@meridian-otc.io", telefon: "+65 6221 4400",    strasse: "Marina Bvd 10",       plz: "018983", ort: "Singapur",  land: "Singapur",    notizen: "Nimmt BTC-Blöcke ab 50 BTC, Settlement über Bank-Escrow.",   tags: ["OTC"],         createdAt: daysAgo(76) },
      { id: "k9",  vorname: "Elena",    nachname: "Petrova",     typ: "verkaeufer",   firma: "Baltic Commodities OÜ",       email: "e.petrova@balticcom.ee",   telefon: "+372 6 401200",    strasse: "Narva mnt 5",         plz: "10117", ort: "Tallinn",    land: "Estland",     notizen: "Kupferkathoden und Weizen, Lieferungen über Muuga.",         tags: [],              createdAt: daysAgo(142) },
      { id: "k10", vorname: "Bernd",    nachname: "Schuhmacher", typ: "tippgeber",    firma: "Handwerk Schuhmacher",        email: "b.schuhmacher@hs-bau.de",  telefon: "+49 231 9987412",  strasse: "Rheinische Str. 77",  plz: "44137", ort: "Dortmund",   land: "Deutschland", notizen: "Bekommt Sanierungsobjekte und Maschinenposten früh mit.",    tags: [],              createdAt: daysAgo(75) },
      { id: "k11", vorname: "Dr. Clara", nachname: "Ritter",     typ: "dienstleister", firma: "Ritter & Kollegen Notariat", email: "c.ritter@ritter-notar.de", telefon: "+49 30 88997700",  strasse: "Kurfürstendamm 61",   plz: "10707", ort: "Berlin",     land: "Deutschland", notizen: "Beurkundungen und Anderkonto-Abwicklung.",                   tags: ["Notariat"],    createdAt: daysAgo(300) },
      { id: "k12", vorname: "Thomas",   nachname: "Mendel",      typ: "verkaeufer",   firma: "Mendel Metallbau GmbH",       email: "t.mendel@mendel-metallbau.de", telefon: "+49 761 5540033", strasse: "Tullastr. 18",    plz: "79108", ort: "Freiburg",   land: "Deutschland", notizen: "Nachfolgeregelung, kein familieninterner Nachfolger.",       tags: ["Nachfolge"],   createdAt: daysAgo(88) },
      { id: "k13", vorname: "Sofia",    nachname: "Marchetti",   typ: "kaeufer",      firma: "Marchetti Collezione",        email: "s.marchetti@collezione.it", telefon: "+39 02 76001122", strasse: "Via Montenapoleone 8", plz: "20121", ort: "Mailand",  land: "Italien",     notizen: "Sammelt Uhren und Zeitgenössisches, zahlt bar.",             tags: ["Sammler"],     createdAt: daysAgo(52) },
      { id: "k14", vorname: "Lars",     nachname: "Hovland",     typ: "vermittler",   firma: "Nordic Energy Partners AS",   email: "l.hovland@nordicenergy.no", telefon: "+47 22 118800",   strasse: "Aker Brygge 12",      plz: "0250", ort: "Oslo",       land: "Norwegen",    notizen: "LNG-Spotladungen, direkter Zugang zum Terminal.",            tags: ["LNG"],         createdAt: daysAgo(41) }
    ];

    /* [titel, kategorie, volumen, menge, einheit, ertragJahr, marge, ort, land, stage, quelle, kontaktId, betreuer, notizen, tags, details, alterTage] */
    var rows = [
      ["Gründerzeit-MFH Lindenau", "immobilie", 1980000, 1240, "m²", 118800, 0, "Leipzig", "Deutschland", "verhandlung", "Tippgeber", "k1", "Anna Berger",
        "Kaufpreis von 2,15 Mio. auf 1,98 Mio. verhandelt, Due Diligence läuft.", ["Erbfall", "Value-Add"],
        { objektart: "Mehrfamilienhaus", wohneinheiten: 16, baujahr: 1908, zustand: "Renovierungsbedarf", grundstueck: 620 }, 2],

      ["Wohn-/Geschäftshaus List", "immobilie", 2450000, 980, "m²", 142000, 0, "Hannover", "Deutschland", "angebot", "Direktansprache", "k2", "Jonas Weiss",
        "LOI versendet, Rückmeldung bis Monatsende zugesagt.", ["Portfolio"],
        { objektart: "Wohn- und Geschäftshaus", wohneinheiten: 11, baujahr: 1964, zustand: "Gepflegt", grundstueck: 410 }, 5],

      ["Gewerbehof Friedrichshain", "immobilie", 5900000, 2100, "m²", 372000, 0, "Berlin", "Deutschland", "verhandlung", "Netzwerk", "k11", "Anna Berger",
        "Mieterausbau 2024 abgeschlossen, WAULT 6,2 Jahre.", ["Core+"],
        { objektart: "Gewerbeimmobilie", wohneinheiten: 6, baujahr: 1971, zustand: "Gepflegt", grundstueck: 1350 }, 4],

      ["Pflegeheim Nordstadt", "immobilie", 8400000, 3100, "m²", 546000, 0, "Magdeburg", "Deutschland", "pruefung", "Broker / Makler", "k2", "Sven Faber",
        "Betreiberbonität geprüft, Pachtvertrag bis 2039.", ["Betreiber"],
        { objektart: "Pflegeimmobilie", wohneinheiten: 84, baujahr: 2004, zustand: "Gepflegt", grundstueck: 1900 }, 9],

      ["Goldbarren-Tranche LBMA 250 kg", "edelmetall", 18750000, 250, "kg", 0, 281000, "Zürich", "Schweiz", "verhandlung", "Netzwerk", "k5", "Anna Berger",
        "Raffinerie bestätigt Verfügbarkeit, Serial-Number-Liste liegt vor. Käuferseite: Lang Family Office.", ["LBMA", "Tranche"],
        { metall: "Gold", reinheit: "999,9", form: "Barren (LBMA Good Delivery)", lagerort: "Zollfreilager Zürich", zertifikat: "Assay der Raffinerie, Serial Ledger", lieferung: "Abholung Zollfreilager" }, 1],

      ["Silbergranulat 5 t", "edelmetall", 4500000, 5000, "kg", 0, 90000, "Frankfurt am Main", "Deutschland", "angebot", "Bestandskunde", "k5", "Mira Kohl",
        "Abnahme in fünf Monatstranchen, Preisbindung an LBMA-Fixing.", ["Tranche"],
        { metall: "Silber", reinheit: "999", form: "Granulat", lagerort: "Scheideanstalt Pforzheim", zertifikat: "Werkszeugnis", lieferung: "Versicherter Transport" }, 7],

      ["Doré-Gold Accra 50 kg", "edelmetall", 3400000, 50, "kg", 0, 136000, "Accra", "Ghana", "pruefung", "Empfehlung", "k6", "Sven Faber",
        "Compliance-Prüfung läuft: Minenlizenz und Exportpapiere unvollständig. Ohne vollständige LBMA-konforme Herkunftskette kein Ankauf.", ["Compliance", "Risiko"],
        { metall: "Gold", reinheit: "ca. 850 (Doré)", form: "Doré", lagerort: "Raffinerie Accra", zertifikat: "ausstehend", lieferung: "Versicherter Transport" }, 6],

      ["Diesel EN590 CIF Rotterdam", "energie", 31000000, 50000, "t/Monat", 0, 310000, "Rotterdam", "Niederlande", "verhandlung", "Broker / Makler", "k7", "Jonas Weiss",
        "12-Monats-Kontrakt, erste Tranche 50.000 t. SBLC-Entwurf beim Käufer.", ["Kontrakt", "ARA"],
        { produkt: "Diesel EN590", incoterm: "CIF", verladeort: "Rotterdam ARA", laufzeit: "12 Monate rollierend", zahlung: "SBLC", inspektion: "SGS bei Löschung" }, 3],

      ["Jet A-1 FOB Houston", "energie", 36000000, 500000, "Barrel", 0, 288000, "Houston", "USA", "erstkontakt", "Netzwerk", "k7", "Jonas Weiss",
        "Angebot über Vermittlerkette erhalten — Endverkäufer noch nicht verifiziert. POP-Dokumente angefordert.", ["Prüfen"],
        { produkt: "Jet A-1 / JP54", incoterm: "FOB", verladeort: "Houston", laufzeit: "Spot", zahlung: "DLC / LC at sight", inspektion: "Saybolt" }, 11],

      ["LNG-Spotladung Q4", "energie", 28000000, 65000, "t", 0, 420000, "Oslo", "Norwegen", "pruefung", "Messe / Konferenz", "k14", "Mira Kohl",
        "Terminal-Slot für November reserviert, Abnehmer aus Süddeutschland geprüft.", ["Spot"],
        { produkt: "LNG", incoterm: "DAP", verladeort: "Terminal Øygarden", laufzeit: "Einmalladung", zahlung: "Escrow", inspektion: "Bureau Veritas" }, 8],

      ["BTC-Block 120 BTC (OTC)", "krypto", 11040000, 120, "BTC", 0, 198000, "Singapur", "Singapur", "closing", "Netzwerk", "k8", "Anna Berger",
        "1,8 % Discount zum Spot, Settlement in drei Tranchen über Bank-Escrow. KYC des Verkäufers abgeschlossen.", ["OTC", "Tranche"],
        { asset: "BTC", netzwerk: "Bitcoin", discount: 1.8, verwahrung: "Qualified Custodian", settlement: "Bank-Escrow", kyc: "abgeschlossen", sof: "Mining-Nachweis 2019–2023" }, 1],

      ["ETH-Staking-Portfolio 4.000 ETH", "krypto", 12400000, 4000, "ETH", 446000, 124000, "Zug", "Schweiz", "pruefung", "Empfehlung", "k8", "Sven Faber",
        "Bestehende Validator-Infrastruktur wird mitübertragen, Ertrag aktuell 3,6 % p. a.", ["Yield"],
        { asset: "ETH", netzwerk: "Ethereum", discount: 0.5, verwahrung: "Multisig-Wallet", settlement: "Tranchenweise", kyc: "in Prüfung", sof: "Exchange-Historie" }, 10],

      ["USDT-Fiat-Ramp 5 Mio.", "krypto", 5000000, 5000000, "USDT", 0, 75000, "Dubai", "VAE", "erstkontakt", "Plattform / Portal", "k8", "Mira Kohl",
        "Anfrage über Plattform, Gegenpartei noch nicht verifiziert — erhöhte Sorgfaltspflicht.", ["AML"],
        { asset: "USDT", netzwerk: "Tron (TRC-20)", discount: 0.8, verwahrung: "OTC-Desk", settlement: "Escrow", kyc: "Unterlagen angefordert", sof: "offen" }, 14],

      ["Kupferkathoden Grade A 2.000 t", "rohstoff", 16800000, 2000, "t", 0, 252000, "Hamburg", "Deutschland", "angebot", "Direktansprache", "k9", "Jonas Weiss",
        "LME-Referenzpreis plus Prämie, Lieferung in vier Tranchen CIF Hamburg.", ["LME"],
        { produkt: "Kupferkathoden Grade A", qualitaet: "LME Grade A, 99,99 %", incoterm: "CIF", lieferort: "Hamburg", rhythmus: "4 Tranchen à 500 t", zahlung: "DLC / LC at sight" }, 6],

      ["Zucker ICUMSA 45, 12.500 t", "rohstoff", 6500000, 12500, "t", 0, 97500, "Santos", "Brasilien", "recherche", "Plattform / Portal", "k9", "Sven Faber",
        "Angebot aus Vermittlerkette, Ursprungsnachweis und Tankinspektion offen.", ["Prüfen"],
        { produkt: "Zucker ICUMSA 45", qualitaet: "ICUMSA 45, brasilianischer Ursprung", incoterm: "FOB", lieferort: "Santos", rhythmus: "Spot", zahlung: "SBLC" }, 16],

      ["Weizen Mahlqualität 25.000 t", "rohstoff", 6000000, 25000, "t", 0, 90000, "Tallinn", "Estland", "verloren", "Netzwerk", "k9", "Mira Kohl",
        "An Mitbewerber verloren, Preis lag 4 % unter unserem Angebot.", ["Verloren"],
        { produkt: "Weizen Mahlqualität", qualitaet: "Protein 12,5 %", incoterm: "FOB", lieferort: "Muuga", rhythmus: "2 Tranchen", zahlung: "MT103 TT" }, 22],

      ["Mendel Metallbau GmbH", "beteiligung", 4200000, 100, "%", 780000, 0, "Freiburg", "Deutschland", "pruefung", "Empfehlung", "k12", "Anna Berger",
        "Nachfolgeregelung, Altgesellschafter bleibt 12 Monate an Bord. Financial DD beauftragt.", ["Nachfolge", "Share Deal"],
        { branche: "Metallverarbeitung", umsatz: 9400000, mitarbeiter: 48, struktur: "Share Deal", anlass: "Nachfolge" }, 3],

      ["LKW-Flotte 24 Sattelzugmaschinen", "fahrzeug", 1680000, 24, "Stück", 0, 84000, "Dortmund", "Deutschland", "angebot", "Tippgeber", "k10", "Sven Faber",
        "Flottenauflösung eines Spediteurs, Gutachten für 6 Fahrzeuge liegt vor.", ["Flotte"],
        { hersteller: "Mercedes-Benz Actros / MAN TGX", baujahr: 2019, zustand: "Gebraucht – top", standort: "Dortmund", papiere: "vollständig, Wartungshefte lückenlos" }, 12],

      ["Uhrenkonvolut 14 Stück", "kunst", 2300000, 14, "Konvolut", 0, 230000, "Mailand", "Italien", "gewonnen", "Bestandskunde", "k13", "Mira Kohl",
        "Ankauf abgeschlossen, Übergabe im Tresor der Bank erfolgt.", ["Abgeschlossen"],
        { kuenstler: "Patek Philippe, Rolex, A. Lange & Söhne", werk: "Konvolut aus Privatsammlung", jahr: 1998, provenienz: "Einzeleigentum seit Erstkauf, Belege vorhanden", zertifikat: "Papiere und Boxen vollständig" }, 19],

      ["MFH Gohlis", "immobilie", 1690000, 720, "m²", 92400, 0, "Leipzig", "Deutschland", "gewonnen", "Direktansprache", "k1", "Anna Berger",
        "Ankauf abgeschlossen, Verwaltung übergeben.", ["Abgeschlossen"],
        { objektart: "Mehrfamilienhaus", wohneinheiten: 10, baujahr: 1935, zustand: "Gepflegt", grundstueck: 300 }, 28],

      ["Goldmünzen-Posten 1.500 oz", "edelmetall", 4050000, 1500, "oz (Feinunzen)", 0, 60750, "Wien", "Österreich", "recherche", "Messe / Konferenz", "k5", "Mira Kohl",
        "Privatverkauf aus Nachlass, Stückliste angefordert.", ["Nachlass"],
        { metall: "Gold", reinheit: "999,9", form: "Münzen", lagerort: "Bankschließfach Wien", zertifikat: "Münzen in Originalverpackung", lieferung: "Sichtprüfung vor Ort" }, 13]
    ];

    var C = { titel: 0, kategorie: 1, volumen: 2, menge: 3, einheit: 4, ertragJahr: 5, marge: 6,
              ort: 7, land: 8, stage: 9, quelle: 10, kontaktId: 11, betreuer: 12, notizen: 13,
              tags: 14, details: 15, alter: 16 };

    var deals = rows.map(function (r, i) {
      var st = STAGES.filter(function (s) { return s.id === r[C.stage]; })[0];
      return {
        id: "d" + (i + 1),
        titel: r[C.titel],
        kategorie: r[C.kategorie],
        volumen: r[C.volumen],
        menge: r[C.menge],
        einheit: r[C.einheit],
        ertragJahr: r[C.ertragJahr],
        marge: r[C.marge],
        ort: r[C.ort],
        land: r[C.land],
        stage: r[C.stage],
        wahrscheinlichkeit: st ? st.prob : 10,
        quelle: r[C.quelle],
        kontaktId: r[C.kontaktId],
        betreuer: r[C.betreuer],
        notizen: r[C.notizen],
        tags: r[C.tags] || [],
        details: r[C.details] || {},
        createdAt: daysAgo(r[C.alter] + 5 + ((i * 31) % 170)),
        updatedAt: daysAgo(r[C.alter])
      };
    });

    var aufgaben = [
      { id: "t1",  titel: "Serial-Number-Liste mit Raffinerie abgleichen",     typ: "pruefung", faellig: dayIn(-2), prioritaet: "hoch",    erledigt: false, dealId: "d5",  kontaktId: "k5",  notiz: "250 Barren, Abgleich mit Assay" },
      { id: "t2",  titel: "SBLC-Entwurf an Käufer freigeben",                  typ: "dokument", faellig: dayIn(-1), prioritaet: "hoch",    erledigt: false, dealId: "d8",  kontaktId: "k7",  notiz: "" },
      { id: "t3",  titel: "Escrow-Agent für BTC-Settlement beauftragen",        typ: "todo",     faellig: dayIn(0),  prioritaet: "hoch",    erledigt: false, dealId: "d11", kontaktId: "k8",  notiz: "Tranche 1: 40 BTC" },
      { id: "t4",  titel: "LOI-Rückmeldung nachfassen",                        typ: "email",    faellig: dayIn(0),  prioritaet: "hoch",    erledigt: false, dealId: "d2",  kontaktId: "k2",  notiz: "" },
      { id: "t5",  titel: "Exportlizenz und Minenpapiere anfordern",            typ: "dokument", faellig: dayIn(1),  prioritaet: "hoch",    erledigt: false, dealId: "d7",  kontaktId: "k6",  notiz: "ohne Papiere kein Ankauf" },
      { id: "t6",  titel: "Financial Due Diligence Kick-off",                  typ: "termin",   faellig: dayIn(2),  prioritaet: "mittel",  erledigt: false, dealId: "d17", kontaktId: "k12", notiz: "10:00 Uhr, Freiburg" },
      { id: "t7",  titel: "Mieterliste und Nebenkostenabrechnung anfordern",    typ: "email",    faellig: dayIn(3),  prioritaet: "mittel",  erledigt: false, dealId: "d1",  kontaktId: "k1",  notiz: "" },
      { id: "t8",  titel: "POP-Dokumente des Endverkäufers prüfen",             typ: "pruefung", faellig: dayIn(4),  prioritaet: "hoch",    erledigt: false, dealId: "d9",  kontaktId: "k7",  notiz: "Vermittlerkette verifizieren" },
      { id: "t9",  titel: "AML-Prüfung Gegenpartei USDT-Ramp",                 typ: "pruefung", faellig: dayIn(5),  prioritaet: "hoch",    erledigt: false, dealId: "d13", kontaktId: "k8",  notiz: "" },
      { id: "t10", titel: "Terminal-Slot Q4 schriftlich bestätigen",            typ: "email",    faellig: dayIn(6),  prioritaet: "mittel",  erledigt: false, dealId: "d10", kontaktId: "k14", notiz: "" },
      { id: "t11", titel: "Gutachten für sechs Sattelzugmaschinen einholen",    typ: "todo",     faellig: dayIn(8),  prioritaet: "niedrig", erledigt: false, dealId: "d18", kontaktId: "k10", notiz: "" },
      { id: "t12", titel: "Stückliste Goldmünzen anfordern",                    typ: "email",    faellig: dayIn(9),  prioritaet: "niedrig", erledigt: false, dealId: "d21", kontaktId: "k5",  notiz: "" },
      { id: "t13", titel: "Notartermin koordinieren",                           typ: "termin",   faellig: dayIn(-4), prioritaet: "hoch",    erledigt: true,  dealId: "d3",  kontaktId: "k11", notiz: "" },
      { id: "t14", titel: "Tippgeberprovision abrechnen",                       typ: "todo",     faellig: dayIn(-6), prioritaet: "niedrig", erledigt: true,  dealId: "d20", kontaktId: "k3",  notiz: "1 % vom Kaufpreis" },
      { id: "t15", titel: "Protokoll der Käuferbesprechung finalisieren",       typ: "dokument", faellig: dayIn(1),  prioritaet: "mittel",  erledigt: false, dealId: "d5",  kontaktId: "k4",  notiz: "Freigabe durch Anna Berger" }
    ];

    var protokolle = [
      {
        id: "p1", nummer: "P-2026-0001", datum: dateAgo(1), uhrzeit: "10:30", dauer: 45,
        kanal: "video", betreff: "Abstimmung Goldtranche 250 kg — Preisbindung und Übergabe",
        dealId: "d5", kontaktId: "k5",
        teilnehmer: "Anna Berger (OffMarket), Marc Baumgartner (Helvetic Metals AG), Dr. Peter Lang (Lang Family Office)",
        verfasser: "Lena Sommer", freigeber: "Anna Berger", status: "freigegeben", vertraulich: true,
        themen:
          "1. Verfügbarkeit und Herkunft\n" +
          "   – Raffinerie bestätigt 250 kg in Good-Delivery-Barren, Serial-Number-Liste liegt vor.\n" +
          "   – Lagerung im Zollfreilager Zürich, Bestandsnachweis vom Vortag vorgelegt.\n\n" +
          "2. Preisbildung\n" +
          "   – Bindung an LBMA-Nachmittagsfixing am Tag der Zahlung, Aufschlag 0,9 %.\n" +
          "   – Käuferseite fordert Fixierung des Aufschlags für 30 Tage.\n\n" +
          "3. Übergabe und Versicherung\n" +
          "   – Übergabe im Zollfreilager, Umlagerung auf das Konto des Käufers.\n" +
          "   – Transportversicherung entfällt bei Umlagerung im Lager.",
        ergebnisse:
          "– Aufschlag von 0,9 % wird für 30 Tage fixiert, danach Neuverhandlung.\n" +
          "– Übergabe erfolgt als Umlagerung im Zollfreilager Zürich, Kosten trägt der Verkäufer.\n" +
          "– Käufer akzeptiert Serial-Number-Ledger als Nachweis, zusätzliche Sichtprüfung wird vereinbart.",
        offenePunkte:
          "– Assay-Zertifikat für vier Barren aus älterer Charge fehlt noch.\n" +
          "– Termin für die Sichtprüfung im Lager ist noch nicht bestätigt.",
        naechsteSchritte: [
          { text: "Fehlende Assay-Zertifikate bei der Raffinerie anfordern", verantwortlich: "Marc Baumgartner", faellig: dayIn(2) },
          { text: "Sichtprüfung im Zollfreilager terminieren", verantwortlich: "Lena Sommer", faellig: dayIn(4) },
          { text: "Kaufvertragsentwurf mit fixiertem Aufschlag versenden", verantwortlich: "Anna Berger", faellig: dayIn(5) }
        ],
        createdAt: daysAgo(1), updatedAt: daysAgo(1)
      },
      {
        id: "p2", nummer: "P-2026-0002", datum: dateAgo(3), uhrzeit: "14:00", dauer: 60,
        kanal: "telefon", betreff: "EN590-Kontrakt — Zahlungsinstrument und Tranchenplanung",
        dealId: "d8", kontaktId: "k7",
        teilnehmer: "Jonas Weiss (OffMarket), Hendrik van Dijk (Rotterdam Fuel Brokers B.V.)",
        verfasser: "Lena Sommer", freigeber: "", status: "final", vertraulich: false,
        themen:
          "1. Vertragsstruktur\n" +
          "   – 12-Monats-Kontrakt über 50.000 t je Monat, CIF Rotterdam.\n" +
          "   – Erste Tranche soll als Testlieferung mit reduziertem Volumen laufen.\n\n" +
          "2. Zahlungsinstrument\n" +
          "   – Verkäuferseite besteht auf SBLC einer Prime Bank.\n" +
          "   – Unser Vorschlag: DLC at sight für die Testtranche, danach SBLC.\n\n" +
          "3. Inspektion\n" +
          "   – SGS-Inspektion bei Löschung, Kosten werden geteilt.",
        ergebnisse:
          "– Testtranche über 20.000 t wird mit DLC at sight abgewickelt.\n" +
          "– Ab der zweiten Tranche gilt SBLC, Entwurf kommt von der Verkäuferseite.\n" +
          "– SGS-Inspektion bei Löschung vereinbart, Kostenteilung 50/50.",
        offenePunkte:
          "– Bankbestätigung für die DLC steht aus.\n" +
          "– Endverkäufer wurde bisher nicht offengelegt.",
        naechsteSchritte: [
          { text: "SBLC-Entwurf prüfen und an Käufer freigeben", verantwortlich: "Jonas Weiss", faellig: dayIn(-1) },
          { text: "Offenlegung des Endverkäufers einfordern", verantwortlich: "Jonas Weiss", faellig: dayIn(3) }
        ],
        createdAt: daysAgo(3), updatedAt: daysAgo(3)
      },
      {
        id: "p3", nummer: "P-2026-0003", datum: dateAgo(6), uhrzeit: "09:15", dauer: 30,
        kanal: "video", betreff: "BTC-Block 120 BTC — Settlement in Tranchen",
        dealId: "d11", kontaktId: "k8",
        teilnehmer: "Anna Berger (OffMarket), Yuki Tanaka (Meridian OTC Desk)",
        verfasser: "Lena Sommer", freigeber: "Anna Berger", status: "freigegeben", vertraulich: true,
        themen:
          "1. Settlement-Struktur\n" +
          "   – Drei Tranchen à 40 BTC über Bank-Escrow.\n" +
          "   – Preisfixierung je Tranche zum Zeitpunkt der Freigabe.\n\n" +
          "2. Compliance\n" +
          "   – KYC des Verkäufers abgeschlossen, Source-of-Funds dokumentiert.\n" +
          "   – Mining-Nachweise für die Jahre 2019 bis 2023 liegen vor.",
        ergebnisse:
          "– Settlement in drei Tranchen à 40 BTC bestätigt, Discount 1,8 % zum Spot.\n" +
          "– Escrow-Agent wird von unserer Seite beauftragt, Gebühren teilen sich beide Seiten.\n" +
          "– Erste Tranche soll innerhalb von zehn Tagen abgewickelt sein.",
        offenePunkte:
          "– Wallet-Adressen für die Tranchen zwei und drei fehlen noch.",
        naechsteSchritte: [
          { text: "Escrow-Agent beauftragen und Vertrag zeichnen", verantwortlich: "Anna Berger", faellig: dayIn(0) },
          { text: "Wallet-Adressen für Tranche 2 und 3 anfordern", verantwortlich: "Lena Sommer", faellig: dayIn(2) }
        ],
        createdAt: daysAgo(6), updatedAt: daysAgo(6)
      },
      {
        id: "p4", nummer: "P-2026-0004", datum: dateAgo(8), uhrzeit: "16:00", dauer: 50,
        kanal: "vorort", betreff: "Besichtigung Gründerzeit-MFH Lindenau mit Statiker",
        dealId: "d1", kontaktId: "k1",
        teilnehmer: "Anna Berger (OffMarket), Helga Brandt (Eigentümerin), Ing. Kaltenbach (Statik)",
        verfasser: "Lena Sommer", freigeber: "", status: "entwurf", vertraulich: false,
        themen:
          "1. Bauzustand\n" +
          "   – Dachstuhl trocken, Sanierung 2019 dokumentiert.\n" +
          "   – Feuchtigkeit im Kellergeschoss im Bereich der Nordwand.\n\n" +
          "2. Mietsituation\n" +
          "   – 16 Einheiten, zwei Wohnungen leerstehend, Mietniveau unter Marktmiete.\n\n" +
          "3. Preisvorstellung\n" +
          "   – Eigentümerin nennt 2,05 Mio. €, wir bieten 1,95 Mio. €.",
        ergebnisse:
          "– Einigung auf 1,98 Mio. € vorbehaltlich der Kellerabdichtung.\n" +
          "– Statiker schätzt Abdichtungskosten auf 45.000 bis 60.000 €.\n" +
          "– Eigentümerin stellt Mieterliste und Nebenkostenabrechnungen bereit.",
        offenePunkte:
          "– Kostenvoranschlag für die Abdichtung fehlt.\n" +
          "– Grundbuchauszug noch nicht angefordert.",
        naechsteSchritte: [
          { text: "Kostenvoranschlag Kellerabdichtung einholen", verantwortlich: "Sven Faber", faellig: dayIn(1) },
          { text: "Mieterliste und Nebenkostenabrechnung anfordern", verantwortlich: "Lena Sommer", faellig: dayIn(3) }
        ],
        createdAt: daysAgo(8), updatedAt: daysAgo(8)
      },
      {
        id: "p5", nummer: "P-2026-0005", datum: dateAgo(11), uhrzeit: "11:00", dauer: 40,
        kanal: "intern", betreff: "Interne Risikobesprechung Doré-Gold Accra",
        dealId: "d7", kontaktId: "",
        teilnehmer: "Anna Berger, Sven Faber, Lena Sommer",
        verfasser: "Lena Sommer", freigeber: "Anna Berger", status: "freigegeben", vertraulich: true,
        themen:
          "1. Compliance-Lage\n" +
          "   – Minenlizenz liegt nur als Kopie vor, Exportpapiere unvollständig.\n" +
          "   – Herkunftskette nicht LBMA-konform dokumentierbar.\n\n" +
          "2. Risikobewertung\n" +
          "   – Reputations- und Rechtsrisiko wird als hoch eingestuft.\n" +
          "   – Marge von 4 % rechtfertigt das Risiko in der aktuellen Form nicht.",
        ergebnisse:
          "– Deal bleibt in der Phase Prüfung, kein Angebot ohne vollständige Papiere.\n" +
          "– Frist von 30 Tagen für die Nachreichung, danach Absage.\n" +
          "– Externe Compliance-Kanzlei wird nur bei vollständigen Unterlagen eingeschaltet.",
        offenePunkte:
          "– Original der Minenlizenz und vollständige Exportdokumentation.",
        naechsteSchritte: [
          { text: "Frist von 30 Tagen schriftlich mitteilen", verantwortlich: "Sven Faber", faellig: dayIn(1) },
          { text: "Exportlizenz und Minenpapiere anfordern", verantwortlich: "Lena Sommer", faellig: dayIn(1) }
        ],
        createdAt: daysAgo(11), updatedAt: daysAgo(11)
      }
    ];

    var aktivitaeten = [
      { id: "a1",  ts: daysAgo(1),  typ: "protokoll", text: "Protokoll P-2026-0001 freigegeben: Abstimmung Goldtranche 250 kg", dealId: "d5",  kontaktId: "k5" },
      { id: "a2",  ts: daysAgo(1),  typ: "stage",     text: "Phase auf „Verhandlung“ geändert",                                  dealId: "d5",  kontaktId: "" },
      { id: "a3",  ts: daysAgo(2),  typ: "anruf",     text: "Telefonat mit Frau Brandt: Einigung auf 1,98 Mio. €",              dealId: "d1",  kontaktId: "k1" },
      { id: "a4",  ts: daysAgo(3),  typ: "protokoll", text: "Protokoll P-2026-0002 erstellt: EN590-Kontrakt",                    dealId: "d8",  kontaktId: "k7" },
      { id: "a5",  ts: daysAgo(4),  typ: "email",     text: "LOI an Osterhage GbR versendet",                                    dealId: "d2",  kontaktId: "k2" },
      { id: "a6",  ts: daysAgo(6),  typ: "protokoll", text: "Protokoll P-2026-0003 freigegeben: BTC-Block Settlement",           dealId: "d11", kontaktId: "k8" },
      { id: "a7",  ts: daysAgo(7),  typ: "stage",     text: "Phase auf „Vertrag / Closing“ geändert",                            dealId: "d11", kontaktId: "" },
      { id: "a8",  ts: daysAgo(8),  typ: "termin",    text: "Besichtigung Lindenau mit Statiker durchgeführt",                   dealId: "d1",  kontaktId: "k1" },
      { id: "a9",  ts: daysAgo(11), typ: "protokoll", text: "Protokoll P-2026-0005 freigegeben: Risikobesprechung Doré-Gold",    dealId: "d7",  kontaktId: "" },
      { id: "a10", ts: daysAgo(14), typ: "note",      text: "Gegenpartei USDT-Ramp nicht verifiziert — erhöhte Sorgfaltspflicht", dealId: "d13", kontaktId: "k8" },
      { id: "a11", ts: daysAgo(19), typ: "stage",     text: "Phase auf „Abgeschlossen“ geändert",                                dealId: "d19", kontaktId: "" },
      { id: "a12", ts: daysAgo(22), typ: "note",      text: "Absage erhalten — Mitbewerber 4 % günstiger",                       dealId: "d16", kontaktId: "k9" }
    ];

    return { deals: deals, kontakte: kontakte, aufgaben: aufgaben, protokolle: protokolle, aktivitaeten: aktivitaeten };
  }

  global.CRMData = {
    STAGES: STAGES,
    KATEGORIEN: KATEGORIEN,
    KONTAKTTYPEN: KONTAKTTYPEN,
    QUELLEN: QUELLEN,
    AUFGABENTYPEN: AUFGABENTYPEN,
    PRIORITAETEN: PRIORITAETEN,
    KANAELE: KANAELE,
    PROTOKOLL_STATUS: PROTOKOLL_STATUS,
    PROTOKOLL_VORLAGE: PROTOKOLL_VORLAGE,
    TEAM: TEAM,
    TEAM_NAMEN: TEAM_NAMEN,
    ICONS: ICONS,
    seed: seed
  };
})(window);
