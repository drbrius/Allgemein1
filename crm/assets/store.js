/* Deal CRM — Datenhaltung (localStorage), CRUD und Kennzahlen */
(function (global) {
  "use strict";

  var KEY = "offmarket-crm-v2";
  var KEY_ALT = "offmarket-crm-v1";   /* Immobilien-Version, wird einmalig migriert */
  var D = global.CRMData;

  var state = {
    deals: [], kontakte: [], aufgaben: [], protokolle: [], aktivitaeten: [],
    einstellungen: {
      firma: "OffMarket Partners",
      nutzer: "Anna Berger",
      assistenz: "Lena Sommer",
      waehrung: "EUR",
      theme: "auto",
      zielMarge: 2,
      aufgabenAusProtokoll: true
    }
  };

  var listeners = [];

  /* ---------- Persistenz ---------- */
  function load() {
    var raw = null;
    try { raw = localStorage.getItem(KEY); } catch (e) { /* Speicher gesperrt */ }
    if (raw) {
      try {
        uebernehmen(JSON.parse(raw));
        return;
      } catch (e) { /* defekter Datensatz → weiter unten Demo laden */ }
    }

    var alt = null;
    try { alt = localStorage.getItem(KEY_ALT); } catch (e) { /* ignorieren */ }
    if (alt) {
      try {
        uebernehmen(migriereV1(JSON.parse(alt)));
        save();
        return;
      } catch (e) { /* Migration fehlgeschlagen → Demo laden */ }
    }

    resetDemo(true);
  }

  function uebernehmen(parsed) {
    state.deals = parsed.deals || [];
    state.kontakte = parsed.kontakte || [];
    state.aufgaben = parsed.aufgaben || [];
    state.protokolle = parsed.protokolle || [];
    state.aktivitaeten = parsed.aktivitaeten || [];
    state.einstellungen = Object.assign(state.einstellungen, parsed.einstellungen || {});
  }

  /* Immobilien-Datenbestand der ersten Version in das Deal-Modell überführen */
  function migriereV1(alt) {
    var typMap = {
      eigentuemer: "verkaeufer", makler: "vermittler", investor: "kaeufer",
      verwalter: "dienstleister", tippgeber: "tippgeber", sonstige: "sonstige"
    };
    var stageMap = { gespraech: "pruefung", notar: "closing" };

    return {
      deals: (alt.objekte || []).map(function (o) {
        return {
          id: o.id, titel: o.titel, kategorie: "immobilie",
          volumen: o.kaufpreis || 0,
          menge: o.wohnflaeche || 0, einheit: "m²",
          ertragJahr: o.mieteJahr || 0, marge: 0,
          ort: [o.strasse, (o.plz || "") + " " + (o.ort || "")].filter(function (t) { return String(t).trim(); }).join(", "),
          land: "Deutschland",
          stage: stageMap[o.stage] || o.stage,
          wahrscheinlichkeit: o.wahrscheinlichkeit,
          quelle: o.quelle, kontaktId: o.kontaktId, betreuer: o.betreuer,
          notizen: o.notizen, tags: o.tags || [],
          details: {
            objektart: o.typ, wohneinheiten: o.einheiten, baujahr: o.baujahr,
            zustand: o.zustand, grundstueck: o.grundstueck
          },
          createdAt: o.createdAt, updatedAt: o.updatedAt
        };
      }),
      kontakte: (alt.kontakte || []).map(function (k) {
        return Object.assign({}, k, { typ: typMap[k.typ] || "sonstige", land: "Deutschland" });
      }),
      aufgaben: (alt.aufgaben || []).map(function (t) {
        return Object.assign({}, t, { dealId: t.objektId || "" });
      }),
      protokolle: [],
      aktivitaeten: (alt.aktivitaeten || []).map(function (a) {
        return Object.assign({}, a, { dealId: a.objektId || "" });
      }),
      einstellungen: alt.einstellungen || {}
    };
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignorieren */ }
  }

  function resetDemo(silent) {
    var s = D.seed();
    state.deals = s.deals;
    state.kontakte = s.kontakte;
    state.aufgaben = s.aufgaben;
    state.protokolle = s.protokolle;
    state.aktivitaeten = s.aktivitaeten;
    save();
    if (!silent) emit();
  }

  function clearAll() {
    state.deals = [];
    state.kontakte = [];
    state.aufgaben = [];
    state.protokolle = [];
    state.aktivitaeten = [];
    save();
    emit();
  }

  function subscribe(fn) { listeners.push(fn); }
  function emit() { listeners.forEach(function (fn) { fn(); }); }

  /* ---------- Helfer ---------- */
  function uid(prefix) {
    return prefix + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  }

  function stage(id) {
    return D.STAGES.filter(function (s) { return s.id === id; })[0] || D.STAGES[0];
  }

  function kategorie(id) {
    return D.KATEGORIEN.filter(function (k) { return k.id === id; })[0] ||
      D.KATEGORIEN[D.KATEGORIEN.length - 1];
  }

  function isOffen(d) { return d.stage !== "gewonnen" && d.stage !== "verloren"; }

  function faktor(d) {
    return d.ertragJahr > 0 && d.volumen > 0 ? d.volumen / d.ertragJahr : 0;
  }
  function rendite(d) {
    return d.volumen > 0 && d.ertragJahr > 0 ? (d.ertragJahr / d.volumen) * 100 : 0;
  }
  function preisProEinheit(d) {
    return d.menge > 0 && d.volumen > 0 ? d.volumen / d.menge : 0;
  }
  function margeProzent(d) {
    return d.volumen > 0 && d.marge > 0 ? (d.marge / d.volumen) * 100 : 0;
  }
  function gewichtet(d) {
    return (d.volumen || 0) * (Number(d.wahrscheinlichkeit) || 0) / 100;
  }
  function gewichteteMarge(d) {
    return (d.marge || 0) * (Number(d.wahrscheinlichkeit) || 0) / 100;
  }

  function kontakt(id) {
    return state.kontakte.filter(function (k) { return k.id === id; })[0] || null;
  }
  function deal(id) {
    return state.deals.filter(function (d) { return d.id === id; })[0] || null;
  }
  function protokoll(id) {
    return state.protokolle.filter(function (p) { return p.id === id; })[0] || null;
  }
  function kontaktName(k) {
    if (!k) return "";
    return (k.vorname + " " + k.nachname).trim();
  }

  /* ---------- Aktivitäten ---------- */
  function log(typ, text, dealId, kontaktId) {
    state.aktivitaeten.unshift({
      id: uid("a"), ts: new Date().toISOString(), typ: typ,
      text: text, dealId: dealId || "", kontaktId: kontaktId || ""
    });
    if (state.aktivitaeten.length > 400) state.aktivitaeten.length = 400;
  }

  function aktivitaetenFuer(filter) {
    return state.aktivitaeten.filter(function (a) {
      if (filter.dealId) return a.dealId === filter.dealId;
      if (filter.kontaktId) return a.kontaktId === filter.kontaktId;
      return true;
    });
  }

  /* ---------- CRUD Deals ---------- */
  function saveDeal(data) {
    var now = new Date().toISOString();
    if (data.id) {
      var vorhanden = deal(data.id);
      if (!vorhanden) return null;
      var alteStage = vorhanden.stage;
      Object.assign(vorhanden, data, { updatedAt: now });
      if (alteStage !== vorhanden.stage) {
        log("stage", "Phase auf „" + stage(vorhanden.stage).label + "“ geändert", vorhanden.id);
      } else {
        log("edit", "Deal-Daten aktualisiert", vorhanden.id);
      }
      save(); emit();
      return vorhanden;
    }
    var neu = Object.assign({
      id: uid("d"), tags: [], details: {}, notizen: "", createdAt: now, updatedAt: now
    }, data);
    state.deals.unshift(neu);
    log("create", "Deal angelegt", neu.id, neu.kontaktId);
    save(); emit();
    return neu;
  }

  function setStage(id, stageId) {
    var d = deal(id);
    if (!d || d.stage === stageId) return;
    d.stage = stageId;
    d.wahrscheinlichkeit = stage(stageId).prob;
    d.updatedAt = new Date().toISOString();
    log("stage", "Phase auf „" + stage(stageId).label + "“ geändert", id);
    save(); emit();
  }

  function deleteDeal(id) {
    var d = deal(id);
    if (!d) return null;
    var index = state.deals.indexOf(d);
    state.deals.splice(index, 1);
    state.aufgaben.forEach(function (t) { if (t.dealId === id) t.dealId = ""; });
    state.protokolle.forEach(function (p) { if (p.dealId === id) p.dealId = ""; });
    save(); emit();
    return { eintrag: d, index: index };
  }

  function restoreDeal(snapshot) {
    if (!snapshot) return;
    state.deals.splice(snapshot.index, 0, snapshot.eintrag);
    save(); emit();
  }

  /* ---------- CRUD Kontakte ---------- */
  function saveKontakt(data) {
    if (data.id) {
      var vorhanden = kontakt(data.id);
      if (!vorhanden) return null;
      Object.assign(vorhanden, data);
      log("edit", "Kontaktdaten aktualisiert", "", vorhanden.id);
      save(); emit();
      return vorhanden;
    }
    var neu = Object.assign({
      id: uid("k"), tags: [], notizen: "", createdAt: new Date().toISOString()
    }, data);
    state.kontakte.unshift(neu);
    log("create", "Kontakt angelegt", "", neu.id);
    save(); emit();
    return neu;
  }

  function deleteKontakt(id) {
    var k = kontakt(id);
    if (!k) return null;
    var index = state.kontakte.indexOf(k);
    state.kontakte.splice(index, 1);
    state.deals.forEach(function (d) { if (d.kontaktId === id) d.kontaktId = ""; });
    state.aufgaben.forEach(function (t) { if (t.kontaktId === id) t.kontaktId = ""; });
    state.protokolle.forEach(function (p) { if (p.kontaktId === id) p.kontaktId = ""; });
    save(); emit();
    return { eintrag: k, index: index };
  }

  function restoreKontakt(snapshot) {
    if (!snapshot) return;
    state.kontakte.splice(snapshot.index, 0, snapshot.eintrag);
    save(); emit();
  }

  /* ---------- CRUD Aufgaben ---------- */
  function saveAufgabe(data) {
    if (data.id) {
      var vorhanden = state.aufgaben.filter(function (t) { return t.id === data.id; })[0];
      if (!vorhanden) return null;
      Object.assign(vorhanden, data);
      save(); emit();
      return vorhanden;
    }
    var neu = Object.assign({
      id: uid("t"), erledigt: false, dealId: "", kontaktId: "", notiz: "",
      createdAt: new Date().toISOString()
    }, data);
    state.aufgaben.unshift(neu);
    save(); emit();
    return neu;
  }

  function toggleAufgabe(id) {
    var t = state.aufgaben.filter(function (x) { return x.id === id; })[0];
    if (!t) return;
    t.erledigt = !t.erledigt;
    if (t.erledigt) log("task", "Aufgabe erledigt: " + t.titel, t.dealId, t.kontaktId);
    save(); emit();
  }

  function deleteAufgabe(id) {
    var t = state.aufgaben.filter(function (x) { return x.id === id; })[0];
    if (!t) return null;
    var index = state.aufgaben.indexOf(t);
    state.aufgaben.splice(index, 1);
    save(); emit();
    return { eintrag: t, index: index };
  }

  function restoreAufgabe(snapshot) {
    if (!snapshot) return;
    state.aufgaben.splice(snapshot.index, 0, snapshot.eintrag);
    save(); emit();
  }

  function aufgabenFuer(dealId, kontaktId) {
    return state.aufgaben.filter(function (t) {
      return (dealId && t.dealId === dealId) || (kontaktId && t.kontaktId === kontaktId);
    });
  }

  /* ---------- CRUD Protokolle ---------- */
  function naechsteNummer() {
    var jahr = new Date().getFullYear();
    var praefix = "P-" + jahr + "-";
    var hoechste = 0;
    state.protokolle.forEach(function (p) {
      if (p.nummer && p.nummer.indexOf(praefix) === 0) {
        var n = parseInt(p.nummer.slice(praefix.length), 10);
        if (!isNaN(n) && n > hoechste) hoechste = n;
      }
    });
    return praefix + String(hoechste + 1).padStart(4, "0");
  }

  function saveProtokoll(data, aufgabenErzeugen) {
    var now = new Date().toISOString();
    var p;
    if (data.id) {
      p = protokoll(data.id);
      if (!p) return null;
      var alterStatus = p.status;
      Object.assign(p, data, { updatedAt: now });
      if (alterStatus !== p.status && p.status !== "entwurf") {
        log("protokoll", "Protokoll " + p.nummer + " " +
          (p.status === "freigegeben" ? "freigegeben" : "finalisiert") + ": " + p.betreff, p.dealId, p.kontaktId);
      }
    } else {
      p = Object.assign({
        id: uid("p"),
        nummer: naechsteNummer(),
        status: "entwurf",
        vertraulich: false,
        naechsteSchritte: [],
        createdAt: now,
        updatedAt: now
      }, data);
      state.protokolle.unshift(p);
      log("protokoll", "Protokoll " + p.nummer + " erstellt: " + p.betreff, p.dealId, p.kontaktId);
    }

    var erzeugt = 0;
    if (aufgabenErzeugen) erzeugt = aufgabenAusProtokoll(p);

    save(); emit();
    return { protokoll: p, aufgaben: erzeugt };
  }

  /* Aus den nächsten Schritten eines Protokolls Aufgaben anlegen.
     Bereits übernommene Schritte werden anhand von uebernommen übersprungen. */
  function aufgabenAusProtokoll(p) {
    var erzeugt = 0;
    (p.naechsteSchritte || []).forEach(function (schritt) {
      if (!schritt.text || schritt.uebernommen) return;
      state.aufgaben.unshift({
        id: uid("t"),
        titel: schritt.text,
        typ: "todo",
        faellig: schritt.faellig || "",
        prioritaet: "mittel",
        erledigt: false,
        dealId: p.dealId || "",
        kontaktId: p.kontaktId || "",
        notiz: "aus Protokoll " + p.nummer +
          (schritt.verantwortlich ? " · verantwortlich: " + schritt.verantwortlich : ""),
        protokollId: p.id,
        createdAt: new Date().toISOString()
      });
      schritt.uebernommen = true;
      erzeugt++;
    });
    return erzeugt;
  }

  function setProtokollStatus(id, status) {
    var p = protokoll(id);
    if (!p || p.status === status) return;
    p.status = status;
    p.updatedAt = new Date().toISOString();
    log("protokoll", "Protokoll " + p.nummer + " → " +
      (D.PROTOKOLL_STATUS.filter(function (s) { return s.id === status; })[0] || {}).label,
      p.dealId, p.kontaktId);
    save(); emit();
  }

  function deleteProtokoll(id) {
    var p = protokoll(id);
    if (!p) return null;
    var index = state.protokolle.indexOf(p);
    state.protokolle.splice(index, 1);
    save(); emit();
    return { eintrag: p, index: index };
  }

  function restoreProtokoll(snapshot) {
    if (!snapshot) return;
    state.protokolle.splice(snapshot.index, 0, snapshot.eintrag);
    save(); emit();
  }

  function protokolleFuer(dealId, kontaktId) {
    return state.protokolle.filter(function (p) {
      return (dealId && p.dealId === dealId) || (kontaktId && p.kontaktId === kontaktId);
    }).sort(function (a, b) { return String(b.datum).localeCompare(String(a.datum)); });
  }

  /* Protokoll als reiner Text — für Zwischenablage, E-Mail oder Ablage */
  function protokollText(p) {
    var kanal = (D.KANAELE.filter(function (k) { return k.id === p.kanal; })[0] || {}).label || p.kanal;
    var d = p.dealId ? deal(p.dealId) : null;
    var k = p.kontaktId ? kontakt(p.kontaktId) : null;
    var zeilen = [];

    zeilen.push("GESPRÄCHSPROTOKOLL " + p.nummer);
    zeilen.push(state.einstellungen.firma);
    zeilen.push("");
    zeilen.push("Betreff:       " + p.betreff);
    zeilen.push("Datum:         " + p.datum + (p.uhrzeit ? ", " + p.uhrzeit + " Uhr" : "") +
      (p.dauer ? " (" + p.dauer + " Min.)" : ""));
    zeilen.push("Art:           " + kanal);
    if (d) zeilen.push("Deal:          " + d.titel + " (" + kategorie(d.kategorie).label + ")");
    if (k) zeilen.push("Kontakt:       " + kontaktName(k) + (k.firma ? ", " + k.firma : ""));
    zeilen.push("Teilnehmer:    " + (p.teilnehmer || "—"));
    zeilen.push("Protokoll:     " + (p.verfasser || "—"));
    if (p.freigeber) zeilen.push("Freigabe:      " + p.freigeber);
    if (p.vertraulich) zeilen.push("Hinweis:       VERTRAULICH");
    zeilen.push("");
    zeilen.push("BESPROCHENE PUNKTE");
    zeilen.push(p.themen || "—");
    zeilen.push("");
    zeilen.push("ERGEBNISSE UND VEREINBARUNGEN");
    zeilen.push(p.ergebnisse || "—");
    if (p.offenePunkte) {
      zeilen.push("");
      zeilen.push("OFFENE PUNKTE");
      zeilen.push(p.offenePunkte);
    }
    if ((p.naechsteSchritte || []).length) {
      zeilen.push("");
      zeilen.push("NÄCHSTE SCHRITTE");
      p.naechsteSchritte.forEach(function (s, i) {
        zeilen.push((i + 1) + ". " + s.text +
          (s.verantwortlich ? " — " + s.verantwortlich : "") +
          (s.faellig ? " — bis " + s.faellig : ""));
      });
    }
    zeilen.push("");
    zeilen.push("Erstellt am " + new Date(p.createdAt).toLocaleDateString("de-DE") +
      " · Status: " + (D.PROTOKOLL_STATUS.filter(function (s) { return s.id === p.status; })[0] || {}).label);
    return zeilen.join("\n");
  }

  /* ---------- Einstellungen ---------- */
  function setEinstellung(key, value) {
    state.einstellungen[key] = value;
    save();
  }

  /* ---------- Kennzahlen ---------- */
  function heuteISO() { return new Date().toISOString().slice(0, 10); }

  function kpis() {
    var offen = state.deals.filter(isOffen);
    var gewonnen = state.deals.filter(function (d) { return d.stage === "gewonnen"; });
    var verloren = state.deals.filter(function (d) { return d.stage === "verloren"; });
    var volumen = offen.reduce(function (s, d) { return s + (d.volumen || 0); }, 0);
    var forecast = offen.reduce(function (s, d) { return s + gewichtet(d); }, 0);
    var marge = offen.reduce(function (s, d) { return s + (d.marge || 0); }, 0);
    var margeGew = offen.reduce(function (s, d) { return s + gewichteteMarge(d); }, 0);
    var mitErtrag = offen.filter(function (d) { return d.ertragJahr > 0; });
    var avgFaktor = mitErtrag.length
      ? mitErtrag.reduce(function (s, d) { return s + faktor(d); }, 0) / mitErtrag.length
      : 0;
    var entschieden = gewonnen.length + verloren.length;
    var heute = heuteISO();
    var offeneAufgaben = state.aufgaben.filter(function (t) { return !t.erledigt; });

    return {
      dealsGesamt: state.deals.length,
      aktiveDeals: offen.length,
      volumen: volumen,
      forecast: forecast,
      marge: marge,
      margeGewichtet: margeGew,
      avgFaktor: avgFaktor,
      gewonnen: gewonnen.length,
      verloren: verloren.length,
      abschlussvolumen: gewonnen.reduce(function (s, d) { return s + (d.volumen || 0); }, 0),
      quote: entschieden ? (gewonnen.length / entschieden) * 100 : 0,
      kontakte: state.kontakte.length,
      protokolle: state.protokolle.length,
      protokolleEntwurf: state.protokolle.filter(function (p) { return p.status === "entwurf"; }).length,
      aufgabenOffen: offeneAufgaben.length,
      aufgabenHeute: offeneAufgaben.filter(function (t) { return t.faellig === heute; }).length,
      aufgabenUeberfaellig: offeneAufgaben.filter(function (t) { return t.faellig && t.faellig < heute; }).length,
      neu30Tage: state.deals.filter(function (d) {
        return (Date.now() - new Date(d.createdAt).getTime()) < 30 * 864e5;
      }).length
    };
  }

  function proStage() {
    return D.STAGES.map(function (s) {
      var liste = state.deals.filter(function (d) { return d.stage === s.id; });
      return {
        stage: s,
        anzahl: liste.length,
        volumen: liste.reduce(function (sum, d) { return sum + (d.volumen || 0); }, 0),
        deals: liste
      };
    });
  }

  function proKategorie() {
    return D.KATEGORIEN.map(function (k) {
      var liste = state.deals.filter(function (d) { return d.kategorie === k.id; });
      var offen = liste.filter(isOffen);
      return {
        kategorie: k,
        anzahl: liste.length,
        aktiv: offen.length,
        volumen: liste.reduce(function (s, d) { return s + (d.volumen || 0); }, 0),
        volumenOffen: offen.reduce(function (s, d) { return s + (d.volumen || 0); }, 0),
        marge: liste.reduce(function (s, d) { return s + (d.marge || 0); }, 0),
        gewonnen: liste.filter(function (d) { return d.stage === "gewonnen"; }).length,
        verloren: liste.filter(function (d) { return d.stage === "verloren"; }).length
      };
    }).filter(function (row) { return row.anzahl > 0; });
  }

  function gruppiereNach(feld) {
    var map = {};
    state.deals.forEach(function (d) {
      var key = d[feld] || "Ohne Angabe";
      if (!map[key]) map[key] = { key: key, anzahl: 0, volumen: 0, marge: 0 };
      map[key].anzahl++;
      map[key].volumen += d.volumen || 0;
      map[key].marge += d.marge || 0;
    });
    return Object.keys(map).map(function (k) { return map[k]; })
      .sort(function (a, b) { return b.volumen - a.volumen; });
  }

  function neuProMonat(monate) {
    var out = [];
    var jetzt = new Date();
    for (var i = monate - 1; i >= 0; i--) {
      var d = new Date(jetzt.getFullYear(), jetzt.getMonth() - i, 1);
      var next = new Date(d.getFullYear(), d.getMonth() + 1, 1);
      var liste = state.deals.filter(function (x) {
        var t = new Date(x.createdAt).getTime();
        return t >= d.getTime() && t < next.getTime();
      });
      out.push({
        label: d.toLocaleDateString("de-DE", { month: "short" }),
        anzahl: liste.length,
        volumen: liste.reduce(function (s, x) { return s + (x.volumen || 0); }, 0)
      });
    }
    return out;
  }

  function protokolleProMonat(monate) {
    var out = [];
    var jetzt = new Date();
    for (var i = monate - 1; i >= 0; i--) {
      var d = new Date(jetzt.getFullYear(), jetzt.getMonth() - i, 1);
      var next = new Date(d.getFullYear(), d.getMonth() + 1, 1);
      var anzahl = state.protokolle.filter(function (p) {
        var t = new Date(p.datum + "T12:00:00").getTime();
        return t >= d.getTime() && t < next.getTime();
      }).length;
      out.push({ label: d.toLocaleDateString("de-DE", { month: "short" }), anzahl: anzahl });
    }
    return out;
  }

  /* ---------- Import / Export ---------- */
  function exportJSON() {
    return JSON.stringify({
      exportiert: new Date().toISOString(),
      version: 2,
      deals: state.deals,
      kontakte: state.kontakte,
      aufgaben: state.aufgaben,
      protokolle: state.protokolle,
      aktivitaeten: state.aktivitaeten,
      einstellungen: state.einstellungen
    }, null, 2);
  }

  function importJSON(text) {
    var parsed = JSON.parse(text);
    if (!parsed || typeof parsed !== "object") throw new Error("Ungültiges Format");
    if (parsed.objekte && !parsed.deals) parsed = migriereV1(parsed);
    if (!Array.isArray(parsed.deals) && !Array.isArray(parsed.kontakte)) {
      throw new Error("Keine CRM-Daten gefunden");
    }
    uebernehmen(parsed);
    save(); emit();
    return {
      deals: state.deals.length,
      kontakte: state.kontakte.length,
      aufgaben: state.aufgaben.length,
      protokolle: state.protokolle.length
    };
  }

  function toCSV(rows, spalten) {
    var esc = function (v) {
      var s = v === null || v === undefined ? "" : String(v);
      return /[";\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    };
    var head = spalten.map(function (c) { return esc(c.label); }).join(";");
    var body = rows.map(function (r) {
      return spalten.map(function (c) { return esc(c.get(r)); }).join(";");
    });
    return "﻿" + [head].concat(body).join("\r\n");
  }

  global.Store = {
    state: state,
    load: load, save: save, emit: emit, subscribe: subscribe,
    resetDemo: resetDemo, clearAll: clearAll,
    uid: uid, stage: stage, kategorie: kategorie, isOffen: isOffen,
    faktor: faktor, rendite: rendite, preisProEinheit: preisProEinheit,
    margeProzent: margeProzent, gewichtet: gewichtet, gewichteteMarge: gewichteteMarge,
    kontakt: kontakt, deal: deal, protokoll: protokoll, kontaktName: kontaktName,
    log: log, aktivitaetenFuer: aktivitaetenFuer,
    saveDeal: saveDeal, setStage: setStage, deleteDeal: deleteDeal, restoreDeal: restoreDeal,
    saveKontakt: saveKontakt, deleteKontakt: deleteKontakt, restoreKontakt: restoreKontakt,
    saveAufgabe: saveAufgabe, toggleAufgabe: toggleAufgabe, deleteAufgabe: deleteAufgabe,
    restoreAufgabe: restoreAufgabe, aufgabenFuer: aufgabenFuer,
    saveProtokoll: saveProtokoll, setProtokollStatus: setProtokollStatus,
    deleteProtokoll: deleteProtokoll, restoreProtokoll: restoreProtokoll,
    protokolleFuer: protokolleFuer, protokollText: protokollText,
    aufgabenAusProtokoll: aufgabenAusProtokoll, naechsteNummer: naechsteNummer,
    setEinstellung: setEinstellung,
    kpis: kpis, proStage: proStage, proKategorie: proKategorie,
    gruppiereNach: gruppiereNach, neuProMonat: neuProMonat, protokolleProMonat: protokolleProMonat,
    heuteISO: heuteISO,
    exportJSON: exportJSON, importJSON: importJSON, toCSV: toCSV
  };
})(window);
