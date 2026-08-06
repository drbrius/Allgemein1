/* OffMarket CRM — Datenhaltung (localStorage), CRUD und Kennzahlen */
(function (global) {
  "use strict";

  var KEY = "offmarket-crm-v1";
  var D = global.CRMData;

  var state = {
    objekte: [], kontakte: [], aufgaben: [], aktivitaeten: [],
    einstellungen: {
      firma: "OffMarket Partners",
      nutzer: "Anna Berger",
      waehrung: "EUR",
      theme: "auto",
      zielFaktor: 20
    }
  };

  var listeners = [];

  /* ---------- Persistenz ---------- */
  function load() {
    var raw = null;
    try { raw = localStorage.getItem(KEY); } catch (e) { /* Speicher gesperrt */ }
    if (raw) {
      try {
        var parsed = JSON.parse(raw);
        state.objekte = parsed.objekte || [];
        state.kontakte = parsed.kontakte || [];
        state.aufgaben = parsed.aufgaben || [];
        state.aktivitaeten = parsed.aktivitaeten || [];
        state.einstellungen = Object.assign(state.einstellungen, parsed.einstellungen || {});
        return;
      } catch (e) { /* defekter Datensatz → Demo laden */ }
    }
    resetDemo(true);
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignorieren */ }
  }

  function resetDemo(silent) {
    var s = D.seed();
    state.objekte = s.objekte;
    state.kontakte = s.kontakte;
    state.aufgaben = s.aufgaben;
    state.aktivitaeten = s.aktivitaeten;
    save();
    if (!silent) emit();
  }

  function clearAll() {
    state.objekte = [];
    state.kontakte = [];
    state.aufgaben = [];
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

  function isOffen(ob) { return ob.stage !== "gewonnen" && ob.stage !== "verloren"; }

  function faktor(ob) {
    return ob.mieteJahr > 0 ? ob.kaufpreis / ob.mieteJahr : 0;
  }
  function rendite(ob) {
    return ob.kaufpreis > 0 && ob.mieteJahr > 0 ? (ob.mieteJahr / ob.kaufpreis) * 100 : 0;
  }
  function preisProQm(ob) {
    return ob.wohnflaeche > 0 ? ob.kaufpreis / ob.wohnflaeche : 0;
  }
  function gewichtet(ob) {
    return ob.kaufpreis * (Number(ob.wahrscheinlichkeit) || 0) / 100;
  }

  function kontakt(id) {
    return state.kontakte.filter(function (k) { return k.id === id; })[0] || null;
  }
  function objekt(id) {
    return state.objekte.filter(function (o) { return o.id === id; })[0] || null;
  }
  function kontaktName(k) {
    if (!k) return "";
    return (k.vorname + " " + k.nachname).trim();
  }

  /* ---------- Aktivitäten ---------- */
  function log(typ, text, objektId, kontaktId) {
    state.aktivitaeten.unshift({
      id: uid("a"), ts: new Date().toISOString(), typ: typ,
      text: text, objektId: objektId || "", kontaktId: kontaktId || ""
    });
    if (state.aktivitaeten.length > 400) state.aktivitaeten.length = 400;
  }

  function aktivitaetenFuer(filter) {
    return state.aktivitaeten.filter(function (a) {
      if (filter.objektId) return a.objektId === filter.objektId;
      if (filter.kontaktId) return a.kontaktId === filter.kontaktId;
      return true;
    });
  }

  /* ---------- CRUD Objekte ---------- */
  function saveObjekt(data) {
    var now = new Date().toISOString();
    if (data.id) {
      var vorhanden = objekt(data.id);
      if (!vorhanden) return null;
      var alteStage = vorhanden.stage;
      Object.assign(vorhanden, data, { updatedAt: now });
      if (alteStage !== vorhanden.stage) {
        log("stage", "Phase auf „" + stage(vorhanden.stage).label + "“ geändert", vorhanden.id);
      } else {
        log("edit", "Objektdaten aktualisiert", vorhanden.id);
      }
      save(); emit();
      return vorhanden;
    }
    var neu = Object.assign({
      id: uid("o"), tags: [], notizen: "", createdAt: now, updatedAt: now
    }, data);
    state.objekte.unshift(neu);
    log("create", "Objekt angelegt", neu.id, neu.kontaktId);
    save(); emit();
    return neu;
  }

  function setStage(id, stageId) {
    var ob = objekt(id);
    if (!ob || ob.stage === stageId) return;
    ob.stage = stageId;
    ob.wahrscheinlichkeit = stage(stageId).prob;
    ob.updatedAt = new Date().toISOString();
    log("stage", "Phase auf „" + stage(stageId).label + "“ geändert", id);
    save(); emit();
  }

  function deleteObjekt(id) {
    var ob = objekt(id);
    if (!ob) return null;
    var index = state.objekte.indexOf(ob);
    state.objekte.splice(index, 1);
    state.aufgaben.forEach(function (t) { if (t.objektId === id) t.objektId = ""; });
    save(); emit();
    return { eintrag: ob, index: index };
  }

  function restoreObjekt(snapshot) {
    if (!snapshot) return;
    state.objekte.splice(snapshot.index, 0, snapshot.eintrag);
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
    state.objekte.forEach(function (o) { if (o.kontaktId === id) o.kontaktId = ""; });
    state.aufgaben.forEach(function (t) { if (t.kontaktId === id) t.kontaktId = ""; });
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
      id: uid("t"), erledigt: false, objektId: "", kontaktId: "", notiz: "",
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
    if (t.erledigt) log("task", "Aufgabe erledigt: " + t.titel, t.objektId, t.kontaktId);
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

  function aufgabenFuer(objektId, kontaktId) {
    return state.aufgaben.filter(function (t) {
      return (objektId && t.objektId === objektId) || (kontaktId && t.kontaktId === kontaktId);
    });
  }

  /* ---------- Einstellungen ---------- */
  function setEinstellung(key, value) {
    state.einstellungen[key] = value;
    save();
  }

  /* ---------- Kennzahlen ---------- */
  function heuteISO() { return new Date().toISOString().slice(0, 10); }

  function kpis() {
    var offen = state.objekte.filter(isOffen);
    var gewonnen = state.objekte.filter(function (o) { return o.stage === "gewonnen"; });
    var verloren = state.objekte.filter(function (o) { return o.stage === "verloren"; });
    var volumen = offen.reduce(function (s, o) { return s + (o.kaufpreis || 0); }, 0);
    var forecast = offen.reduce(function (s, o) { return s + gewichtet(o); }, 0);
    var mitMiete = offen.filter(function (o) { return o.mieteJahr > 0; });
    var avgFaktor = mitMiete.length
      ? mitMiete.reduce(function (s, o) { return s + faktor(o); }, 0) / mitMiete.length
      : 0;
    var entschieden = gewonnen.length + verloren.length;
    var heute = heuteISO();
    var offeneAufgaben = state.aufgaben.filter(function (t) { return !t.erledigt; });

    return {
      objekteGesamt: state.objekte.length,
      aktiveDeals: offen.length,
      volumen: volumen,
      forecast: forecast,
      avgFaktor: avgFaktor,
      gewonnen: gewonnen.length,
      verloren: verloren.length,
      ankaufsvolumen: gewonnen.reduce(function (s, o) { return s + (o.kaufpreis || 0); }, 0),
      quote: entschieden ? (gewonnen.length / entschieden) * 100 : 0,
      kontakte: state.kontakte.length,
      aufgabenOffen: offeneAufgaben.length,
      aufgabenHeute: offeneAufgaben.filter(function (t) { return t.faellig === heute; }).length,
      aufgabenUeberfaellig: offeneAufgaben.filter(function (t) { return t.faellig && t.faellig < heute; }).length,
      neu30Tage: state.objekte.filter(function (o) {
        return (Date.now() - new Date(o.createdAt).getTime()) < 30 * 864e5;
      }).length
    };
  }

  function proStage() {
    return D.STAGES.map(function (s) {
      var liste = state.objekte.filter(function (o) { return o.stage === s.id; });
      return {
        stage: s,
        anzahl: liste.length,
        volumen: liste.reduce(function (sum, o) { return sum + (o.kaufpreis || 0); }, 0),
        objekte: liste
      };
    });
  }

  function gruppiereNach(feld) {
    var map = {};
    state.objekte.forEach(function (o) {
      var key = o[feld] || "Ohne Angabe";
      if (!map[key]) map[key] = { key: key, anzahl: 0, volumen: 0 };
      map[key].anzahl++;
      map[key].volumen += o.kaufpreis || 0;
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
      var liste = state.objekte.filter(function (o) {
        var t = new Date(o.createdAt).getTime();
        return t >= d.getTime() && t < next.getTime();
      });
      out.push({
        label: d.toLocaleDateString("de-DE", { month: "short" }),
        anzahl: liste.length,
        volumen: liste.reduce(function (s, o) { return s + (o.kaufpreis || 0); }, 0)
      });
    }
    return out;
  }

  /* ---------- Import / Export ---------- */
  function exportJSON() {
    return JSON.stringify({
      exportiert: new Date().toISOString(),
      version: 1,
      objekte: state.objekte,
      kontakte: state.kontakte,
      aufgaben: state.aufgaben,
      aktivitaeten: state.aktivitaeten,
      einstellungen: state.einstellungen
    }, null, 2);
  }

  function importJSON(text) {
    var parsed = JSON.parse(text);
    if (!parsed || typeof parsed !== "object") throw new Error("Ungültiges Format");
    if (!Array.isArray(parsed.objekte) && !Array.isArray(parsed.kontakte)) {
      throw new Error("Keine CRM-Daten gefunden");
    }
    state.objekte = parsed.objekte || [];
    state.kontakte = parsed.kontakte || [];
    state.aufgaben = parsed.aufgaben || [];
    state.aktivitaeten = parsed.aktivitaeten || [];
    if (parsed.einstellungen) Object.assign(state.einstellungen, parsed.einstellungen);
    save(); emit();
    return {
      objekte: state.objekte.length,
      kontakte: state.kontakte.length,
      aufgaben: state.aufgaben.length
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
    uid: uid, stage: stage, isOffen: isOffen,
    faktor: faktor, rendite: rendite, preisProQm: preisProQm, gewichtet: gewichtet,
    kontakt: kontakt, objekt: objekt, kontaktName: kontaktName,
    log: log, aktivitaetenFuer: aktivitaetenFuer,
    saveObjekt: saveObjekt, setStage: setStage, deleteObjekt: deleteObjekt, restoreObjekt: restoreObjekt,
    saveKontakt: saveKontakt, deleteKontakt: deleteKontakt, restoreKontakt: restoreKontakt,
    saveAufgabe: saveAufgabe, toggleAufgabe: toggleAufgabe, deleteAufgabe: deleteAufgabe,
    restoreAufgabe: restoreAufgabe, aufgabenFuer: aufgabenFuer,
    setEinstellung: setEinstellung,
    kpis: kpis, proStage: proStage, gruppiereNach: gruppiereNach, neuProMonat: neuProMonat,
    heuteISO: heuteISO,
    exportJSON: exportJSON, importJSON: importJSON, toCSV: toCSV
  };
})(window);
