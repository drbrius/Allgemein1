/* OffMarket CRM — Formulare zum Anlegen und Bearbeiten */
(function (global) {
  "use strict";

  var S = global.Store, U = global.UI, D = global.CRMData;

  function kontaktOptionen() {
    return S.state.kontakte.map(function (k) {
      return { value: k.id, label: S.kontaktName(k) + (k.firma ? " · " + k.firma : "") };
    });
  }

  function objektOptionen() {
    return S.state.objekte.map(function (o) {
      return { value: o.id, label: o.titel + " · " + o.ort };
    });
  }

  function stageOptionen() {
    return D.STAGES.map(function (s) { return { value: s.id, label: s.label }; });
  }

  /* ---------------- Objekt ---------------- */
  function objektForm(id, onSaved) {
    var o = id ? S.objekt(id) : null;
    var v = o || {
      titel: "", strasse: "", plz: "", ort: "", typ: D.OBJEKTARTEN[0], baujahr: "",
      wohnflaeche: "", grundstueck: "", einheiten: "", kaufpreis: "", mieteJahr: "",
      zustand: D.ZUSTAENDE[1], stage: "recherche", quelle: D.QUELLEN[0], kontaktId: "",
      betreuer: S.state.einstellungen.nutzer, wahrscheinlichkeit: 10, notizen: "", tags: []
    };

    var body =
      '<div class="form-grid">' +
        '<div class="section-title">Objekt</div>' +
        U.feld("Bezeichnung *", U.input("titel", v.titel, { platzhalter: "z. B. Gründerzeit-MFH Lindenau" }), true) +
        U.feld("Straße und Hausnummer", U.input("strasse", v.strasse), true) +
        U.feld("PLZ", U.input("plz", v.plz, { platzhalter: "04177" })) +
        U.feld("Ort *", U.input("ort", v.ort)) +
        U.feld("Objektart", U.select("typ", v.typ, D.OBJEKTARTEN)) +
        U.feld("Zustand", U.select("zustand", v.zustand, D.ZUSTAENDE)) +

        '<div class="section-title">Eckdaten</div>' +
        U.feld("Baujahr", U.input("baujahr", v.baujahr, { typ: "number", min: 0 })) +
        U.feld("Einheiten", U.input("einheiten", v.einheiten, { typ: "number", min: 0 })) +
        U.feld("Wohn-/Nutzfläche (m²)", U.input("wohnflaeche", v.wohnflaeche, { typ: "number", min: 0 })) +
        U.feld("Grundstück (m²)", U.input("grundstueck", v.grundstueck, { typ: "number", min: 0 })) +
        U.feld("Kaufpreis (€) *", U.input("kaufpreis", v.kaufpreis, { typ: "number", min: 0, schritt: 1000 })) +
        U.feld("Jahresmiete IST (€)", U.input("mieteJahr", v.mieteJahr, { typ: "number", min: 0, schritt: 100 })) +
        '<div class="full"><div id="kennzahl-vorschau" class="hint"></div></div>' +

        '<div class="section-title">Akquise</div>' +
        U.feld("Phase", U.select("stage", v.stage, stageOptionen())) +
        U.feld("Wahrscheinlichkeit (%)", U.input("wahrscheinlichkeit", v.wahrscheinlichkeit, { typ: "number", min: 0 })) +
        U.feld("Quelle", U.select("quelle", v.quelle, D.QUELLEN)) +
        U.feld("Betreuer", U.select("betreuer", v.betreuer, D.TEAM)) +
        U.feld("Eigentümer / Kontakt", U.select("kontaktId", v.kontaktId, kontaktOptionen(), "— kein Kontakt —"), true) +
        U.feld("Schlagwörter (Komma-getrennt)", U.input("tags", (v.tags || []).join(", "), { platzhalter: "Value-Add, Denkmal" }), true) +
        U.feld("Notizen", U.textarea("notizen", v.notizen, "Gesprächsstand, Besonderheiten, nächste Schritte …"), true) +
      "</div>";

    U.modal({
      titel: o ? "Objekt bearbeiten" : "Neues Objekt",
      body: body,
      okLabel: o ? "Änderungen speichern" : "Objekt anlegen",
      onOpen: function (dialog) {
        var kp = dialog.querySelector('[name="kaufpreis"]');
        var mi = dialog.querySelector('[name="mieteJahr"]');
        var wf = dialog.querySelector('[name="wohnflaeche"]');
        var stageSel = dialog.querySelector('[name="stage"]');
        var probIn = dialog.querySelector('[name="wahrscheinlichkeit"]');
        var out = dialog.querySelector("#kennzahl-vorschau");

        function aktualisiere() {
          var preis = Number(kp.value) || 0;
          var miete = Number(mi.value) || 0;
          var flaeche = Number(wf.value) || 0;
          var teile = [];
          if (preis && miete) {
            teile.push("Faktor <b>" + U.dez(preis / miete) + "</b>");
            teile.push("Bruttorendite <b>" + U.dez((miete / preis) * 100) + " %</b>");
          }
          if (preis && flaeche) teile.push("Preis/m² <b>" + U.eur(preis / flaeche) + "</b>");
          out.innerHTML = teile.length ? teile.join(" · ") : "Kaufpreis und Jahresmiete eingeben für Faktor und Rendite.";
        }
        [kp, mi, wf].forEach(function (el) { el.addEventListener("input", aktualisiere); });
        stageSel.addEventListener("change", function () {
          probIn.value = S.stage(stageSel.value).prob;
        });
        aktualisiere();
      },
      onOk: function (dialog) {
        var w = U.formWerte(dialog);
        var fehler = [];
        if (!w.titel) fehler.push("titel");
        if (!w.ort) fehler.push("ort");
        if (!w.kaufpreis || Number(w.kaufpreis) <= 0) fehler.push("kaufpreis");
        if (fehler.length) {
          U.markiereFehler(dialog, fehler);
          U.toast("Bitte Bezeichnung, Ort und Kaufpreis ausfüllen.", "err");
          return false;
        }
        var daten = {
          titel: w.titel, strasse: w.strasse, plz: w.plz, ort: w.ort,
          typ: w.typ, zustand: w.zustand,
          baujahr: Number(w.baujahr) || 0,
          einheiten: Number(w.einheiten) || 0,
          wohnflaeche: Number(w.wohnflaeche) || 0,
          grundstueck: Number(w.grundstueck) || 0,
          kaufpreis: Number(w.kaufpreis) || 0,
          mieteJahr: Number(w.mieteJahr) || 0,
          stage: w.stage, quelle: w.quelle, kontaktId: w.kontaktId, betreuer: w.betreuer,
          wahrscheinlichkeit: Math.min(100, Math.max(0, Number(w.wahrscheinlichkeit) || 0)),
          notizen: w.notizen,
          tags: w.tags ? w.tags.split(",").map(function (t) { return t.trim(); }).filter(Boolean) : []
        };
        if (o) daten.id = o.id;
        var gespeichert = S.saveObjekt(daten);
        U.toast(o ? "Objekt aktualisiert." : "Objekt angelegt.", "ok");
        if (onSaved) onSaved(gespeichert);
      }
    });
  }

  /* ---------------- Kontakt ---------------- */
  function kontaktForm(id, onSaved) {
    var k = id ? S.kontakt(id) : null;
    var v = k || {
      vorname: "", nachname: "", typ: "eigentuemer", firma: "", email: "", telefon: "",
      strasse: "", plz: "", ort: "", notizen: "", tags: []
    };

    var body =
      '<div class="form-grid">' +
        U.feld("Vorname", U.input("vorname", v.vorname)) +
        U.feld("Nachname *", U.input("nachname", v.nachname)) +
        U.feld("Rolle", U.select("typ", v.typ, D.KONTAKTTYPEN.map(function (t) {
          return { value: t.id, label: t.label };
        }))) +
        U.feld("Firma", U.input("firma", v.firma)) +
        U.feld("E-Mail", U.input("email", v.email, { typ: "email" })) +
        U.feld("Telefon", U.input("telefon", v.telefon, { typ: "tel" })) +
        U.feld("Straße", U.input("strasse", v.strasse), true) +
        U.feld("PLZ", U.input("plz", v.plz)) +
        U.feld("Ort", U.input("ort", v.ort)) +
        U.feld("Schlagwörter (Komma-getrennt)", U.input("tags", (v.tags || []).join(", ")), true) +
        U.feld("Notizen", U.textarea("notizen", v.notizen, "Gesprächsnotizen, Präferenzen …"), true) +
      "</div>";

    U.modal({
      titel: k ? "Kontakt bearbeiten" : "Neuer Kontakt",
      body: body,
      okLabel: k ? "Änderungen speichern" : "Kontakt anlegen",
      onOk: function (dialog) {
        var w = U.formWerte(dialog);
        if (!w.nachname) {
          U.markiereFehler(dialog, ["nachname"]);
          U.toast("Bitte einen Nachnamen angeben.", "err");
          return false;
        }
        var daten = {
          vorname: w.vorname, nachname: w.nachname, typ: w.typ, firma: w.firma,
          email: w.email, telefon: w.telefon, strasse: w.strasse, plz: w.plz, ort: w.ort,
          notizen: w.notizen,
          tags: w.tags ? w.tags.split(",").map(function (t) { return t.trim(); }).filter(Boolean) : []
        };
        if (k) daten.id = k.id;
        var gespeichert = S.saveKontakt(daten);
        U.toast(k ? "Kontakt aktualisiert." : "Kontakt angelegt.", "ok");
        if (onSaved) onSaved(gespeichert);
      }
    });
  }

  /* ---------------- Aufgabe ---------------- */
  function aufgabeForm(id, vorbelegung, onSaved) {
    var t = id ? S.state.aufgaben.filter(function (x) { return x.id === id; })[0] : null;
    var v = t || Object.assign({
      titel: "", typ: "anruf", faellig: S.heuteISO(), prioritaet: "mittel",
      objektId: "", kontaktId: "", notiz: ""
    }, vorbelegung || {});

    var body =
      '<div class="form-grid">' +
        U.feld("Aufgabe *", U.input("titel", v.titel, { platzhalter: "z. B. Eigentümer zurückrufen" }), true) +
        U.feld("Art", U.select("typ", v.typ, D.AUFGABENTYPEN.map(function (a) {
          return { value: a.id, label: a.label };
        }))) +
        U.feld("Fällig am", U.input("faellig", v.faellig, { typ: "date" })) +
        U.feld("Priorität", U.select("prioritaet", v.prioritaet, D.PRIORITAETEN.map(function (p) {
          return { value: p.id, label: p.label };
        }))) +
        U.feld("Objekt", U.select("objektId", v.objektId, objektOptionen(), "— kein Objekt —")) +
        U.feld("Kontakt", U.select("kontaktId", v.kontaktId, kontaktOptionen(), "— kein Kontakt —"), true) +
        U.feld("Notiz", U.textarea("notiz", v.notiz, ""), true) +
      "</div>";

    U.modal({
      titel: t ? "Aufgabe bearbeiten" : "Neue Aufgabe",
      body: body,
      okLabel: t ? "Änderungen speichern" : "Aufgabe anlegen",
      onOk: function (dialog) {
        var w = U.formWerte(dialog);
        if (!w.titel) {
          U.markiereFehler(dialog, ["titel"]);
          U.toast("Bitte einen Titel angeben.", "err");
          return false;
        }
        var daten = {
          titel: w.titel, typ: w.typ, faellig: w.faellig, prioritaet: w.prioritaet,
          objektId: w.objektId, kontaktId: w.kontaktId, notiz: w.notiz
        };
        if (t) { daten.id = t.id; daten.erledigt = t.erledigt; }
        var gespeichert = S.saveAufgabe(daten);
        U.toast(t ? "Aufgabe aktualisiert." : "Aufgabe angelegt.", "ok");
        if (onSaved) onSaved(gespeichert);
      }
    });
  }

  /* ---------------- Notiz / Aktivität ---------------- */
  function notizForm(objektId, kontaktId, onSaved) {
    var body =
      '<div class="form-grid">' +
        U.feld("Art", U.select("typ", "note", [
          { value: "note", label: "Notiz" },
          { value: "anruf", label: "Telefonat" },
          { value: "email", label: "E-Mail" },
          { value: "termin", label: "Termin / Besichtigung" }
        ])) +
        U.feld("Datum", U.input("wann", S.heuteISO(), { typ: "date" })) +
        U.feld("Eintrag *", U.textarea("text", "", "Was wurde besprochen?"), true) +
      "</div>";

    U.modal({
      titel: "Aktivität festhalten",
      body: body,
      okLabel: "Eintragen",
      onOk: function (dialog) {
        var w = U.formWerte(dialog);
        if (!w.text) {
          U.markiereFehler(dialog, ["text"]);
          return false;
        }
        S.log(w.typ, w.text, objektId, kontaktId);
        if (w.wann && w.wann !== S.heuteISO()) {
          S.state.aktivitaeten[0].ts = new Date(w.wann + "T12:00:00").toISOString();
          S.state.aktivitaeten.sort(function (a, b) { return new Date(b.ts) - new Date(a.ts); });
        }
        S.save(); S.emit();
        U.toast("Aktivität gespeichert.", "ok");
        if (onSaved) onSaved();
      }
    });
  }

  global.Forms = {
    objekt: objektForm,
    kontakt: kontaktForm,
    aufgabe: aufgabeForm,
    notiz: notizForm
  };
})(window);
