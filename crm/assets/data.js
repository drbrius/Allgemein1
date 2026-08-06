/* OffMarket CRM — Stammdaten, Icons und Demo-Datensatz */
(function (global) {
  "use strict";

  var STAGES = [
    { id: "recherche",   label: "Recherche",       color: "#94a3b8", prob: 10 },
    { id: "erstkontakt", label: "Erstkontakt",     color: "#38bdf8", prob: 20 },
    { id: "gespraech",   label: "Besichtigung",    color: "#818cf8", prob: 40 },
    { id: "angebot",     label: "Angebot / LOI",   color: "#a78bfa", prob: 60 },
    { id: "verhandlung", label: "Verhandlung",     color: "#fb923c", prob: 75 },
    { id: "notar",       label: "Notartermin",     color: "#eab308", prob: 90 },
    { id: "gewonnen",    label: "Angekauft",       color: "#22c55e", prob: 100 },
    { id: "verloren",    label: "Verloren",        color: "#ef4444", prob: 0 }
  ];

  var OBJEKTARTEN = [
    "Mehrfamilienhaus",
    "Wohn- und Geschäftshaus",
    "Eigentumswohnung",
    "Einfamilienhaus",
    "Grundstück",
    "Gewerbeimmobilie",
    "Pflegeimmobilie"
  ];

  var KONTAKTTYPEN = [
    { id: "eigentuemer", label: "Eigentümer",  cls: "pill-accent" },
    { id: "makler",      label: "Makler",      cls: "pill-sky" },
    { id: "tippgeber",   label: "Tippgeber",   cls: "pill-violet" },
    { id: "investor",    label: "Investor",    cls: "pill-green" },
    { id: "verwalter",   label: "Verwalter",   cls: "pill-amber" },
    { id: "sonstige",    label: "Sonstige",    cls: "" }
  ];

  var QUELLEN = [
    "Direktansprache",
    "Tippgeber",
    "Eigentümeranschreiben",
    "Netzwerk",
    "Makler",
    "Zwangsversteigerung",
    "Portal-Recherche"
  ];

  var ZUSTAENDE = ["Neuwertig", "Gepflegt", "Renovierungsbedarf", "Sanierungsbedarf", "Entkernt"];

  var AUFGABENTYPEN = [
    { id: "anruf",  label: "Anruf",       icon: "phone" },
    { id: "email",  label: "E-Mail",      icon: "mail" },
    { id: "termin", label: "Termin",      icon: "calendar" },
    { id: "brief",  label: "Anschreiben", icon: "file" },
    { id: "todo",   label: "To-do",       icon: "check" }
  ];

  var PRIORITAETEN = [
    { id: "hoch",     label: "Hoch",     cls: "pill-red" },
    { id: "mittel",   label: "Mittel",   cls: "pill-amber" },
    { id: "niedrig",  label: "Niedrig",  cls: "" }
  ];

  var TEAM = ["Anna Berger", "Jonas Weiss", "Mira Kohl", "Sven Faber"];

  /* Inline-SVG-Icons (24er Grid, currentColor) */
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
    note:      '<path d="M4 4h16v12l-4 4H4z"/><path d="M20 16h-4v4"/>'
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

  function seed() {
    var kontakte = [
      { id: "k1", vorname: "Helga",    nachname: "Brandt",     typ: "eigentuemer", firma: "",                          email: "h.brandt@web.de",            telefon: "+49 341 2298431",  strasse: "Lindenauer Markt 8", plz: "04177", ort: "Leipzig",   notizen: "Erbengemeinschaft, verkauft ungern über Makler.", tags: ["Erbfall"], createdAt: daysAgo(190) },
      { id: "k2", vorname: "Ralf",     nachname: "Osterhage",  typ: "eigentuemer", firma: "Osterhage GbR",             email: "info@osterhage-gbr.de",      telefon: "+49 511 4478120",  strasse: "Podbielskistr. 144", plz: "30177", ort: "Hannover",  notizen: "Portfolio-Abverkauf über 2 Jahre geplant.",       tags: ["Portfolio"], createdAt: daysAgo(163) },
      { id: "k3", vorname: "Sabine",   nachname: "Kruse",      typ: "tippgeber",   firma: "Kruse Hausverwaltung",      email: "s.kruse@kruse-hv.de",        telefon: "+49 40 87654321",  strasse: "Eppendorfer Weg 12", plz: "20259", ort: "Hamburg",   notizen: "Liefert regelmäßig Tipps, 1 % Provision vereinbart.", tags: ["Top-Quelle"], createdAt: daysAgo(410) },
      { id: "k4", vorname: "Dr. Peter", nachname: "Lang",      typ: "investor",    firma: "Lang Family Office",        email: "p.lang@lang-fo.de",          telefon: "+49 89 21098765",  strasse: "Maximilianstr. 35",  plz: "80539", ort: "München",   notizen: "Sucht MFH ab 3 Mio. €, Faktor bis 22.",           tags: ["Kapital"], createdAt: daysAgo(240) },
      { id: "k5", vorname: "Yasemin",  nachname: "Aydin",      typ: "eigentuemer", firma: "",                          email: "y.aydin@gmx.de",             telefon: "+49 221 3390055",  strasse: "Venloer Str. 301",   plz: "50823", ort: "Köln",      notizen: "Altersbedingter Verkauf, wünscht Wohnrecht.",     tags: ["Wohnrecht"], createdAt: daysAgo(96) },
      { id: "k6", vorname: "Markus",   nachname: "Stollberg",  typ: "makler",      firma: "Stollberg Immobilien",      email: "ms@stollberg-immo.de",       telefon: "+49 351 4471290",  strasse: "Königstr. 4",        plz: "01097", ort: "Dresden",   notizen: "Bietet Objekte vor Portalveröffentlichung an.",   tags: [], createdAt: daysAgo(300) },
      { id: "k7", vorname: "Christine", nachname: "Vogt",      typ: "eigentuemer", firma: "",                          email: "chr.vogt@t-online.de",       telefon: "+49 561 7788321",  strasse: "Wilhelmshöher Allee 190", plz: "34121", ort: "Kassel", notizen: "Scheidungsverkauf, Zeitdruck.",                  tags: ["Zeitdruck"], createdAt: daysAgo(48) },
      { id: "k8", vorname: "Torsten",  nachname: "Meiwald",    typ: "verwalter",   firma: "MW Property Management",    email: "t.meiwald@mw-pm.de",         telefon: "+49 30 55442210",  strasse: "Frankfurter Allee 62", plz: "10247", ort: "Berlin",  notizen: "Verwaltet 14 Objekte, kennt verkaufswillige Eigentümer.", tags: ["Netzwerk"], createdAt: daysAgo(220) },
      { id: "k9", vorname: "Andrea",   nachname: "Pohl",       typ: "eigentuemer", firma: "Pohl Verwaltungs UG",       email: "a.pohl@pohl-ug.de",          telefon: "+49 391 2234567",  strasse: "Hegelstr. 22",       plz: "39104", ort: "Magdeburg", notizen: "Verkauft nur komplett, kein Teilverkauf.",        tags: [], createdAt: daysAgo(130) },
      { id: "k10", vorname: "Bernd",   nachname: "Schuhmacher", typ: "tippgeber",  firma: "Handwerk Schuhmacher",      email: "b.schuhmacher@hs-bau.de",    telefon: "+49 231 9987412",  strasse: "Rheinische Str. 77", plz: "44137", ort: "Dortmund",  notizen: "Handwerker, bekommt Sanierungsobjekte früh mit.", tags: [], createdAt: daysAgo(75) }
    ];

    var o = [
      ["Gründerzeit-MFH Lindenau", "Merseburger Str. 88", "04177", "Leipzig", "Mehrfamilienhaus", 1908, 1240, 620, 16, 1980000, 118800, "Renovierungsbedarf", "verhandlung", "Tippgeber", "k1", "Anna Berger", "Kaufpreis von 2,15 Mio. auf 1,98 Mio. verhandelt. DD läuft.", ["Erbfall", "Value-Add"], 24],
      ["Wohn-/Geschäftshaus List", "Podbielskistr. 144", "30177", "Hannover", "Wohn- und Geschäftshaus", 1964, 980, 410, 11, 2450000, 142000, "Gepflegt", "angebot", "Direktansprache", "k2", "Jonas Weiss", "LOI versendet, Rückmeldung bis Monatsende zugesagt.", ["Portfolio"], 12],
      ["MFH Eppendorf", "Eppendorfer Weg 118", "20259", "Hamburg", "Mehrfamilienhaus", 1952, 760, 330, 10, 3150000, 138000, "Gepflegt", "gespraech", "Tippgeber", "k3", "Anna Berger", "Besichtigung mit Statiker durchgeführt, Dach 2019 neu.", ["Top-Lage"], 7],
      ["Zinshaus Ehrenfeld", "Venloer Str. 301", "50823", "Köln", "Mehrfamilienhaus", 1928, 645, 280, 9, 2290000, 109500, "Renovierungsbedarf", "erstkontakt", "Eigentümeranschreiben", "k5", "Mira Kohl", "Eigentümerin möchte lebenslanges Wohnrecht im DG.", ["Wohnrecht"], 19],
      ["Sanierungsobjekt Neustadt", "Rothenburger Str. 19", "01099", "Dresden", "Mehrfamilienhaus", 1897, 890, 340, 12, 1450000, 61200, "Sanierungsbedarf", "gespraech", "Makler", "k6", "Sven Faber", "Denkmalschutz, KfW-Förderung prüfen.", ["Denkmal", "Value-Add"], 31],
      ["EFH Wilhelmshöhe", "Wilhelmshöher Allee 190", "34121", "Kassel", "Einfamilienhaus", 1979, 186, 720, 1, 495000, 0, "Gepflegt", "notar", "Netzwerk", "k7", "Mira Kohl", "Notartermin bestätigt, Finanzierung steht.", ["Zeitdruck"], 3],
      ["Baugrundstück Rothensee", "Barleber Chaussee 4", "39126", "Magdeburg", "Grundstück", 0, 0, 2400, 0, 380000, 0, "Entkernt", "recherche", "Portal-Recherche", "k9", "Sven Faber", "B-Plan erlaubt 3 Vollgeschosse, Bodengutachten fehlt.", ["Neubau"], 44],
      ["MFH Kreuzviertel", "Rheinische Str. 77", "44137", "Dortmund", "Mehrfamilienhaus", 1958, 540, 260, 8, 1120000, 68400, "Renovierungsbedarf", "erstkontakt", "Tippgeber", "k10", "Jonas Weiss", "Eigentümer erreicht, Rückruf in KW 34 vereinbart.", [], 9],
      ["Gewerbehof Friedrichshain", "Frankfurter Allee 62", "10247", "Berlin", "Gewerbeimmobilie", 1971, 2100, 1350, 6, 5900000, 372000, "Gepflegt", "verhandlung", "Netzwerk", "k8", "Anna Berger", "Mieterausbau 2024 abgeschlossen, WAULT 6,2 Jahre.", ["Core+"], 5],
      ["ETW-Paket Südvorstadt", "Karl-Liebknecht-Str. 62", "04275", "Leipzig", "Eigentumswohnung", 1996, 312, 0, 5, 845000, 44400, "Neuwertig", "gewonnen", "Makler", "k6", "Jonas Weiss", "Ankauf notariell beurkundet, Übergabe zum 01.10.", ["Abgeschlossen"], 21],
      ["MFH Gohlis", "Georg-Schumann-Str. 210", "04159", "Leipzig", "Mehrfamilienhaus", 1935, 720, 300, 10, 1690000, 92400, "Gepflegt", "gewonnen", "Direktansprache", "k1", "Anna Berger", "Ankauf abgeschlossen, Verwaltung übergeben.", ["Abgeschlossen"], 88],
      ["Pflegeheim Nordstadt", "Hegelstr. 22", "39104", "Magdeburg", "Pflegeimmobilie", 2004, 3100, 1900, 84, 8400000, 546000, "Gepflegt", "angebot", "Netzwerk", "k9", "Sven Faber", "Betreiberbonität geprüft, Pachtvertrag bis 2039.", ["Betreiber"], 14],
      ["MFH Südstadt", "Hildesheimer Str. 45", "30169", "Hannover", "Mehrfamilienhaus", 1962, 610, 250, 9, 1780000, 88800, "Renovierungsbedarf", "verloren", "Direktansprache", "k2", "Jonas Weiss", "An Bieter mit höherem Gebot verloren (1,95 Mio.).", ["Verloren"], 36],
      ["Wohnanlage Prohlis", "Georg-Palitzsch-Str. 12", "01239", "Dresden", "Mehrfamilienhaus", 1984, 1560, 900, 24, 2340000, 175200, "Gepflegt", "recherche", "Zwangsversteigerung", "k6", "Sven Faber", "Termin Amtsgericht am 12.11., Verkehrswert 2,6 Mio.", ["ZVG"], 2],
      ["Stadthaus Altstadt", "Königstr. 4", "01097", "Dresden", "Wohn- und Geschäftshaus", 1911, 430, 190, 6, 1395000, 74400, "Gepflegt", "gespraech", "Makler", "k6", "Mira Kohl", "Zweitbesichtigung mit Architekt geplant.", ["Denkmal"], 11]
    ];

    /* Spaltenreihenfolge der Rohdaten oben */
    var COL = {
      titel: 0, strasse: 1, plz: 2, ort: 3, typ: 4, baujahr: 5, wohnflaeche: 6,
      grundstueck: 7, einheiten: 8, kaufpreis: 9, mieteJahr: 10, zustand: 11,
      stage: 12, quelle: 13, kontaktId: 14, betreuer: 15, notizen: 16, tags: 17, alter: 18
    };

    var objekte = o.map(function (r, i) {
      var stage = r[COL.stage];
      var st = STAGES.filter(function (s) { return s.id === stage; })[0];
      return {
        id: "o" + (i + 1),
        titel: r[COL.titel], strasse: r[COL.strasse], plz: r[COL.plz], ort: r[COL.ort],
        typ: r[COL.typ], baujahr: r[COL.baujahr],
        wohnflaeche: r[COL.wohnflaeche], grundstueck: r[COL.grundstueck], einheiten: r[COL.einheiten],
        kaufpreis: r[COL.kaufpreis], mieteJahr: r[COL.mieteJahr], zustand: r[COL.zustand],
        stage: stage, quelle: r[COL.quelle], kontaktId: r[COL.kontaktId], betreuer: r[COL.betreuer],
        wahrscheinlichkeit: st ? st.prob : 10,
        notizen: r[COL.notizen], tags: r[COL.tags] || [],
        /* Erfassungsdatum über ein halbes Jahr streuen, damit Verlaufscharts aussagekräftig sind */
        createdAt: daysAgo(r[COL.alter] + 5 + ((i * 37) % 160)),
        updatedAt: daysAgo(r[COL.alter])
      };
    });

    var aufgaben = [
      { id: "t1", titel: "Kaufpreisangebot mit Eigentümerin final abstimmen", typ: "anruf",  faellig: dayIn(-2), prioritaet: "hoch",    erledigt: false, objektId: "o1",  kontaktId: "k1",  notiz: "Zielpreis 1,95 Mio." },
      { id: "t2", titel: "Grundbuchauszug anfordern",                          typ: "todo",   faellig: dayIn(-1), prioritaet: "mittel",  erledigt: false, objektId: "o2",  kontaktId: "",    notiz: "" },
      { id: "t3", titel: "Zweitbesichtigung mit Architekt",                    typ: "termin", faellig: dayIn(0),  prioritaet: "hoch",    erledigt: false, objektId: "o15", kontaktId: "k6",  notiz: "10:00 Uhr vor Ort" },
      { id: "t4", titel: "LOI-Rückmeldung nachfassen",                         typ: "email",  faellig: dayIn(0),  prioritaet: "hoch",    erledigt: false, objektId: "o2",  kontaktId: "k2",  notiz: "" },
      { id: "t5", titel: "Mieterliste und Nebenkostenabrechnung anfordern",    typ: "email",  faellig: dayIn(1),  prioritaet: "mittel",  erledigt: false, objektId: "o3",  kontaktId: "k3",  notiz: "" },
      { id: "t6", titel: "Notartermin vorbereiten (Entwurf prüfen)",           typ: "todo",   faellig: dayIn(2),  prioritaet: "hoch",    erledigt: false, objektId: "o6",  kontaktId: "k7",  notiz: "Entwurf liegt vor" },
      { id: "t7", titel: "Bodengutachten beauftragen",                         typ: "todo",   faellig: dayIn(4),  prioritaet: "niedrig", erledigt: false, objektId: "o7",  kontaktId: "",    notiz: "" },
      { id: "t8", titel: "Eigentümer Rückruf KW 34",                           typ: "anruf",  faellig: dayIn(5),  prioritaet: "mittel",  erledigt: false, objektId: "o8",  kontaktId: "k10", notiz: "" },
      { id: "t9", titel: "Anschreiben-Serie Ehrenfeld versenden (40 Stk.)",    typ: "brief",  faellig: dayIn(6),  prioritaet: "mittel",  erledigt: false, objektId: "",    kontaktId: "",    notiz: "Zielgebiet 50823" },
      { id: "t10", titel: "Betreiberbonität final dokumentieren",              typ: "todo",   faellig: dayIn(8),  prioritaet: "mittel",  erledigt: false, objektId: "o12", kontaktId: "k9",  notiz: "" },
      { id: "t11", titel: "ZVG-Termin Amtsgericht vormerken",                  typ: "termin", faellig: dayIn(12), prioritaet: "hoch",    erledigt: false, objektId: "o14", kontaktId: "",    notiz: "12.11., 09:30 Uhr" },
      { id: "t12", titel: "Finanzierungsanfrage an Hausbank",                  typ: "email",  faellig: dayIn(-4), prioritaet: "hoch",    erledigt: true,  objektId: "o9",  kontaktId: "",    notiz: "" },
      { id: "t13", titel: "Exposé für Investorenkreis erstellen",              typ: "todo",   faellig: dayIn(-6), prioritaet: "niedrig", erledigt: true,  objektId: "o10", kontaktId: "k4",  notiz: "" },
      { id: "t14", titel: "Tippgeberprovision abrechnen",                      typ: "todo",   faellig: dayIn(3),  prioritaet: "niedrig", erledigt: false, objektId: "o11", kontaktId: "k3",  notiz: "1 % vom Kaufpreis" }
    ];

    var aktivitaeten = [
      { id: "a1", ts: daysAgo(1),  typ: "stage",   text: "Phase auf „Verhandlung“ geändert", objektId: "o1",  kontaktId: "" },
      { id: "a2", ts: daysAgo(2),  typ: "anruf",   text: "Telefonat mit Frau Brandt: Preisvorstellung 2,05 Mio.", objektId: "o1", kontaktId: "k1" },
      { id: "a3", ts: daysAgo(3),  typ: "email",   text: "LOI an Osterhage GbR versendet", objektId: "o2", kontaktId: "k2" },
      { id: "a4", ts: daysAgo(5),  typ: "termin",  text: "Besichtigung Eppendorfer Weg mit Statiker", objektId: "o3", kontaktId: "k3" },
      { id: "a5", ts: daysAgo(6),  typ: "note",    text: "Dachsanierung 2019 dokumentiert, Rechnung liegt vor", objektId: "o3", kontaktId: "" },
      { id: "a6", ts: daysAgo(8),  typ: "stage",   text: "Phase auf „Notartermin“ geändert", objektId: "o6", kontaktId: "" },
      { id: "a7", ts: daysAgo(11), typ: "anruf",   text: "Erstkontakt Frau Aydin — grundsätzliches Interesse", objektId: "o4", kontaktId: "k5" },
      { id: "a8", ts: daysAgo(14), typ: "create",  text: "Objekt angelegt", objektId: "o14", kontaktId: "" },
      { id: "a9", ts: daysAgo(18), typ: "stage",   text: "Phase auf „Angekauft“ geändert", objektId: "o10", kontaktId: "" },
      { id: "a10", ts: daysAgo(21), typ: "note",   text: "Absage erhalten — höheres Gebot eines Mitbewerbers", objektId: "o13", kontaktId: "k2" }
    ];

    return { objekte: objekte, kontakte: kontakte, aufgaben: aufgaben, aktivitaeten: aktivitaeten };
  }

  global.CRMData = {
    STAGES: STAGES,
    OBJEKTARTEN: OBJEKTARTEN,
    KONTAKTTYPEN: KONTAKTTYPEN,
    QUELLEN: QUELLEN,
    ZUSTAENDE: ZUSTAENDE,
    AUFGABENTYPEN: AUFGABENTYPEN,
    PRIORITAETEN: PRIORITAETEN,
    TEAM: TEAM,
    ICONS: ICONS,
    seed: seed
  };
})(window);
