/* Deal CRM — Formulare zum Anlegen und Bearbeiten */
(function (global) {
  "use strict";

  var S = global.Store, U = global.UI, D = global.CRMData;

  function kontaktOptionen() {
    return S.state.kontakte.map(function (k) {
      return { value: k.id, label: S.kontaktName(k) + (k.firma ? " · " + k.firma : "") };
    });
  }

  function dealOptionen() {
    return S.state.deals.map(function (d) {
      return { value: d.id, label: d.titel + " · " + S.kategorie(d.kategorie).label };
    });
  }

  function stageOptionen() {
    return D.STAGES.map(function (s) { return { value: s.id, label: s.label }; });
  }

  function kategorieOptionen() {
    return D.KATEGORIEN.map(function (k) { return { value: k.id, label: k.label }; });
  }

  /* ---------------- Deal ---------------- */

  /* Fachfelder der gewählten Kategorie — wird bei Kategoriewechsel neu gezeichnet */
  function kategorieFelder(kat, details) {
    var k = S.kategorie(kat);
    return '<div class="section-title">' + U.esc(k.label) + "</div>" +
      k.felder.map(function (f) {
        var wert = details && details[f.k] !== undefined ? details[f.k] : "";
        var name = "detail_" + f.k;
        if (f.typ === "select") {
          return U.feld(f.label, U.select(name, wert, f.optionen, "— keine Angabe —"));
        }
        return U.feld(f.label, U.input(name, wert, {
          typ: f.typ === "number" ? "number" : "text",
          platzhalter: f.platzhalter || ""
        }));
      }).join("");
  }

  function dealForm(id, onSaved) {
    var d = id ? S.deal(id) : null;
    var v = d || {
      titel: "", kategorie: "immobilie", volumen: "", menge: "", einheit: "",
      ertragJahr: "", marge: "", ort: "", land: "Deutschland",
      stage: "recherche", wahrscheinlichkeit: 10, quelle: D.QUELLEN[0], kontaktId: "",
      betreuer: S.state.einstellungen.nutzer, notizen: "", tags: [], details: {}
    };
    var kat = S.kategorie(v.kategorie);

    var body =
      '<div class="form-grid">' +
        '<div class="section-title">Deal</div>' +
        U.feld("Bezeichnung *", U.input("titel", v.titel, { platzhalter: "z. B. Goldbarren-Tranche LBMA 250 kg" }), true) +
        U.feld("Kategorie", U.select("kategorie", v.kategorie, kategorieOptionen())) +
        U.feld("Phase", U.select("stage", v.stage, stageOptionen())) +
        U.feld("Ort / Standort", U.input("ort", v.ort, { platzhalter: "Zürich" })) +
        U.feld("Land", U.input("land", v.land)) +

        '<div class="section-title">Kaufmännisches</div>' +
        U.feldRaw('<span id="lbl-volumen">' + U.esc(kat.volumenLabel) + "</span> *",
          U.input("volumen", v.volumen, { typ: "number", min: 0, schritt: 1000 })) +
        U.feld("Erwartete Marge / Provision (€)", U.input("marge", v.marge, { typ: "number", min: 0, schritt: 500 })) +
        U.feldRaw('<span id="lbl-menge">' + U.esc(kat.mengeLabel) + "</span>",
          U.input("menge", v.menge, { typ: "number", min: 0, schritt: "any" })) +
        U.feld("Einheit", '<span id="einheit-wrap">' +
          U.select("einheit", v.einheit, kat.mengeEinheiten, "— ohne —") + "</span>") +
        '<div class="full" id="ertrag-wrap">' +
          (kat.ertragLabel
            ? U.feld(kat.ertragLabel, U.input("ertragJahr", v.ertragJahr, { typ: "number", min: 0, schritt: 100 }))
            : "") +
        "</div>" +
        '<div class="full"><div id="kennzahl-vorschau" class="hint"></div></div>' +

        '<div id="kategorie-felder" class="full" style="display:contents">' +
          kategorieFelder(v.kategorie, v.details) +
        "</div>" +

        '<div class="section-title">Zuordnung</div>' +
        U.feld("Wahrscheinlichkeit (%)", U.input("wahrscheinlichkeit", v.wahrscheinlichkeit, { typ: "number", min: 0 })) +
        U.feld("Quelle", U.select("quelle", v.quelle, D.QUELLEN)) +
        U.feld("Betreuer", U.select("betreuer", v.betreuer, D.TEAM_NAMEN)) +
        U.feld("Gegenpartei / Kontakt", U.select("kontaktId", v.kontaktId, kontaktOptionen(), "— kein Kontakt —")) +
        U.feld("Schlagwörter (Komma-getrennt)", U.input("tags", (v.tags || []).join(", "), { platzhalter: "Tranche, Compliance" }), true) +
        U.feld("Notizen", U.textarea("notizen", v.notizen, "Stand der Gespräche, Besonderheiten, nächste Schritte …"), true) +
      "</div>";

    U.modal({
      titel: d ? "Deal bearbeiten" : "Neuer Deal",
      body: body,
      okLabel: d ? "Änderungen speichern" : "Deal anlegen",
      onOpen: function (dialog) {
        var katSel = dialog.querySelector('[name="kategorie"]');
        var stageSel = dialog.querySelector('[name="stage"]');
        var probIn = dialog.querySelector('[name="wahrscheinlichkeit"]');
        var out = dialog.querySelector("#kennzahl-vorschau");

        function feldWert(name) {
          var el = dialog.querySelector('[name="' + name + '"]');
          return el ? Number(el.value) || 0 : 0;
        }

        function vorschau() {
          var k = S.kategorie(katSel.value);
          var volumen = feldWert("volumen");
          var mengeWert = feldWert("menge");
          var ertrag = feldWert("ertragJahr");
          var marge = feldWert("marge");
          var einheitEl = dialog.querySelector('[name="einheit"]');
          var einheit = einheitEl ? einheitEl.value : "";
          var teile = [];
          if (volumen && mengeWert) {
            teile.push("Preis je " + U.esc(einheit || k.mengeLabel) + " <b>" + U.eur(volumen / mengeWert) + "</b>");
          }
          if (volumen && ertrag) {
            teile.push("Faktor <b>" + U.dez(volumen / ertrag) + "</b>");
            teile.push("Rendite <b>" + U.dez((ertrag / volumen) * 100) + " %</b>");
          }
          if (volumen && marge) teile.push("Marge <b>" + U.dez((marge / volumen) * 100) + " %</b>");
          out.innerHTML = teile.length ? teile.join(" · ")
            : "Volumen, Menge und Marge eingeben — Kennzahlen werden automatisch berechnet.";
        }

        /* Kategoriewechsel: Labels, Einheiten, Ertragsfeld und Fachfelder austauschen */
        katSel.addEventListener("change", function () {
          var k = S.kategorie(katSel.value);
          dialog.querySelector("#lbl-volumen").textContent = k.volumenLabel;
          dialog.querySelector("#lbl-menge").textContent = k.mengeLabel;
          dialog.querySelector("#einheit-wrap").innerHTML =
            U.select("einheit", k.mengeEinheiten[0], k.mengeEinheiten, "— ohne —");

          var ertragWrap = dialog.querySelector("#ertrag-wrap");
          var bisher = dialog.querySelector('[name="ertragJahr"]');
          var bisherWert = bisher ? bisher.value : "";
          ertragWrap.innerHTML = k.ertragLabel
            ? U.feld(k.ertragLabel, U.input("ertragJahr", bisherWert, { typ: "number", min: 0, schritt: 100 }))
            : "";

          dialog.querySelector("#kategorie-felder").innerHTML = kategorieFelder(katSel.value, {});
          dialog.querySelectorAll('[name="menge"], [name="volumen"], [name="marge"], [name="ertragJahr"], [name="einheit"]')
            .forEach(function (el) { el.addEventListener("input", vorschau); el.addEventListener("change", vorschau); });
          vorschau();
        });

        stageSel.addEventListener("change", function () {
          probIn.value = S.stage(stageSel.value).prob;
        });

        dialog.querySelectorAll('[name="menge"], [name="volumen"], [name="marge"], [name="ertragJahr"], [name="einheit"]')
          .forEach(function (el) { el.addEventListener("input", vorschau); el.addEventListener("change", vorschau); });
        vorschau();
      },
      onOk: function (dialog) {
        var w = U.formWerte(dialog);
        var fehler = [];
        if (!w.titel) fehler.push("titel");
        if (!w.volumen || Number(w.volumen) <= 0) fehler.push("volumen");
        if (fehler.length) {
          U.markiereFehler(dialog, fehler);
          U.toast("Bitte Bezeichnung und Volumen ausfüllen.", "err");
          return false;
        }

        var details = {};
        Object.keys(w).forEach(function (key) {
          if (key.indexOf("detail_") === 0 && w[key] !== "") {
            var roh = w[key];
            var zahl = Number(roh);
            details[key.slice(7)] = roh !== "" && !isNaN(zahl) && /^[0-9.,]+$/.test(roh) ? zahl : roh;
          }
        });

        var daten = {
          titel: w.titel, kategorie: w.kategorie,
          volumen: Number(w.volumen) || 0,
          menge: Number(w.menge) || 0,
          einheit: w.einheit || "",
          ertragJahr: Number(w.ertragJahr) || 0,
          marge: Number(w.marge) || 0,
          ort: w.ort, land: w.land,
          stage: w.stage, quelle: w.quelle, kontaktId: w.kontaktId, betreuer: w.betreuer,
          wahrscheinlichkeit: Math.min(100, Math.max(0, Number(w.wahrscheinlichkeit) || 0)),
          notizen: w.notizen,
          tags: w.tags ? w.tags.split(",").map(function (t) { return t.trim(); }).filter(Boolean) : [],
          details: details
        };
        if (d) daten.id = d.id;
        var gespeichert = S.saveDeal(daten);
        U.toast(d ? "Deal aktualisiert." : "Deal angelegt.", "ok");
        if (onSaved) onSaved(gespeichert);
      }
    });
  }

  /* ---------------- Kontakt ---------------- */
  function kontaktForm(id, onSaved) {
    var k = id ? S.kontakt(id) : null;
    var v = k || {
      vorname: "", nachname: "", typ: "verkaeufer", firma: "", email: "", telefon: "",
      strasse: "", plz: "", ort: "", land: "Deutschland", notizen: "", tags: []
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
        U.feld("Land", U.input("land", v.land)) +
        U.feld("Schlagwörter (Komma-getrennt)", U.input("tags", (v.tags || []).join(", "))) +
        U.feld("Notizen", U.textarea("notizen", v.notizen, "Gesprächsnotizen, Präferenzen, Compliance-Hinweise …"), true) +
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
          email: w.email, telefon: w.telefon, strasse: w.strasse, plz: w.plz,
          ort: w.ort, land: w.land, notizen: w.notizen,
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
      dealId: "", kontaktId: "", notiz: ""
    }, vorbelegung || {});

    var body =
      '<div class="form-grid">' +
        U.feld("Aufgabe *", U.input("titel", v.titel, { platzhalter: "z. B. SBLC-Entwurf prüfen" }), true) +
        U.feld("Art", U.select("typ", v.typ, D.AUFGABENTYPEN.map(function (a) {
          return { value: a.id, label: a.label };
        }))) +
        U.feld("Fällig am", U.input("faellig", v.faellig, { typ: "date" })) +
        U.feld("Priorität", U.select("prioritaet", v.prioritaet, D.PRIORITAETEN.map(function (p) {
          return { value: p.id, label: p.label };
        }))) +
        U.feld("Deal", U.select("dealId", v.dealId, dealOptionen(), "— kein Deal —")) +
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
          dealId: w.dealId, kontaktId: w.kontaktId, notiz: w.notiz
        };
        if (t) { daten.id = t.id; daten.erledigt = t.erledigt; }
        var gespeichert = S.saveAufgabe(daten);
        U.toast(t ? "Aufgabe aktualisiert." : "Aufgabe angelegt.", "ok");
        if (onSaved) onSaved(gespeichert);
      }
    });
  }

  /* ---------------- Protokoll ---------------- */
  function schrittZeile(schritt, index) {
    var s = schritt || { text: "", verantwortlich: "", faellig: "" };
    return '<div class="schritt-row" data-index="' + index + '">' +
      '<input type="text" data-s="text" value="' + U.esc(s.text) + '" placeholder="Maßnahme">' +
      U.select("", s.verantwortlich, D.TEAM_NAMEN.concat(["extern"]), "verantwortlich")
        .replace('name=""', 'data-s="verantwortlich"') +
      '<input type="date" data-s="faellig" value="' + U.esc(s.faellig || "") + '">' +
      '<button type="button" class="btn btn-sm btn-icon btn-ghost" data-schritt-weg="' + index + '" title="Zeile entfernen">' +
        U.icon("close", 14) + "</button>" +
      "</div>";
  }

  function protokollForm(id, vorbelegung, onSaved) {
    var p = id ? S.protokoll(id) : null;
    var e = S.state.einstellungen;
    var v = p || Object.assign({
      datum: S.heuteISO(), uhrzeit: "10:00", dauer: 30, kanal: "telefon",
      betreff: "", dealId: "", kontaktId: "",
      teilnehmer: "", verfasser: e.assistenz || e.nutzer, freigeber: e.nutzer,
      status: "entwurf", vertraulich: false,
      themen: "", ergebnisse: "", offenePunkte: "",
      naechsteSchritte: []
    }, vorbelegung || {});

    /* Teilnehmer aus dem verknüpften Kontakt vorbelegen */
    if (!p && !v.teilnehmer) {
      var k0 = v.kontaktId ? S.kontakt(v.kontaktId) : null;
      v.teilnehmer = e.nutzer + " (" + e.firma + ")" +
        (k0 ? ", " + S.kontaktName(k0) + (k0.firma ? " (" + k0.firma + ")" : "") : "");
    }

    var schritte = (v.naechsteSchritte || []).slice();
    if (!schritte.length) schritte.push({ text: "", verantwortlich: "", faellig: "" });

    var body =
      '<div class="form-grid">' +
        '<div class="section-title">Kopfdaten' + (p ? " · " + U.esc(p.nummer) : "") + "</div>" +
        U.feld("Betreff *", U.input("betreff", v.betreff, { platzhalter: "z. B. Abstimmung Goldtranche — Preisbindung" }), true) +
        U.feld("Datum", U.input("datum", v.datum, { typ: "date" })) +
        U.feld("Uhrzeit", U.input("uhrzeit", v.uhrzeit, { typ: "text", platzhalter: "10:30" })) +
        U.feld("Dauer (Minuten)", U.input("dauer", v.dauer, { typ: "number", min: 0, schritt: 5 })) +
        U.feld("Art des Gesprächs", U.select("kanal", v.kanal, D.KANAELE.map(function (k) {
          return { value: k.id, label: k.label };
        }))) +
        U.feld("Deal", U.select("dealId", v.dealId, dealOptionen(), "— kein Deal —")) +
        U.feld("Kontakt", U.select("kontaktId", v.kontaktId, kontaktOptionen(), "— kein Kontakt —")) +
        U.feld("Teilnehmer", U.textarea("teilnehmer", v.teilnehmer, "Name (Firma), Name (Firma) …"), true) +
        U.feld("Protokollführung", U.select("verfasser", v.verfasser, D.TEAM_NAMEN)) +
        U.feld("Freigabe durch", U.select("freigeber", v.freigeber, D.TEAM_NAMEN, "— offen —")) +

        '<div class="section-title">Inhalt</div>' +
        '<div class="full" style="display:flex;justify-content:flex-end;margin-bottom:-0.4rem">' +
          '<button type="button" class="btn btn-sm" id="vorlage-btn">Gliederung einfügen</button></div>' +
        U.feld("Besprochene Punkte *", U.textarea("themen", v.themen, "Was wurde besprochen?"), true) +
        U.feld("Ergebnisse und Vereinbarungen", U.textarea("ergebnisse", v.ergebnisse, "Was wurde vereinbart?"), true) +
        U.feld("Offene Punkte / Risiken", U.textarea("offenePunkte", v.offenePunkte, ""), true) +

        '<div class="section-title">Nächste Schritte</div>' +
        '<div class="full"><div id="schritte">' +
          schritte.map(function (s, i) { return schrittZeile(s, i); }).join("") +
        "</div>" +
        '<button type="button" class="btn btn-sm" id="schritt-add" style="margin-top:0.5rem">' +
          U.icon("plus", 14) + " Weitere Maßnahme</button></div>" +

        '<div class="section-title">Status</div>' +
        U.feld("Status", U.select("status", v.status, D.PROTOKOLL_STATUS.map(function (s) {
          return { value: s.id, label: s.label };
        }))) +
        '<label class="field"><span>Kennzeichnung</span>' +
          '<label class="check"><input type="checkbox" name="vertraulich"' + (v.vertraulich ? " checked" : "") +
          "> vertraulich</label></label>" +
        '<label class="field full"><span>Übernahme</span>' +
          '<label class="check"><input type="checkbox" name="aufgabenErzeugen"' +
          (S.state.einstellungen.aufgabenAusProtokoll ? " checked" : "") +
          "> Aus den nächsten Schritten Aufgaben anlegen</label></label>" +
      "</div>";

    U.modal({
      titel: p ? "Protokoll bearbeiten" : "Neues Protokoll " + S.naechsteNummer(),
      body: body,
      okLabel: p ? "Änderungen speichern" : "Protokoll anlegen",
      onOpen: function (dialog) {
        var host = dialog.querySelector("#schritte");

        function bindeEntfernen() {
          host.querySelectorAll("[data-schritt-weg]").forEach(function (b) {
            b.onclick = function () {
              if (host.children.length > 1) b.closest(".schritt-row").remove();
              else host.querySelectorAll("[data-s]").forEach(function (el) { el.value = ""; });
            };
          });
        }
        bindeEntfernen();

        dialog.querySelector("#schritt-add").addEventListener("click", function () {
          var wrap = document.createElement("div");
          wrap.innerHTML = schrittZeile(null, host.children.length);
          host.appendChild(wrap.firstChild);
          bindeEntfernen();
          var neu = host.lastElementChild.querySelector('[data-s="text"]');
          if (neu) neu.focus();
        });

        dialog.querySelector("#vorlage-btn").addEventListener("click", function () {
          var ta = dialog.querySelector('[name="themen"]');
          if (!ta.value.trim()) ta.value = D.PROTOKOLL_VORLAGE;
          else ta.value += "\n\n" + D.PROTOKOLL_VORLAGE;
          ta.focus();
        });

        /* Kontaktwechsel ergänzt die Teilnehmerliste */
        dialog.querySelector('[name="kontaktId"]').addEventListener("change", function (ev) {
          var k = ev.target.value ? S.kontakt(ev.target.value) : null;
          if (!k) return;
          var ta = dialog.querySelector('[name="teilnehmer"]');
          var name = S.kontaktName(k) + (k.firma ? " (" + k.firma + ")" : "");
          if (ta.value.indexOf(S.kontaktName(k)) === -1) {
            ta.value = ta.value.trim() ? ta.value.trim() + ", " + name : name;
          }
        });
      },
      onOk: function (dialog) {
        var w = U.formWerte(dialog);
        var fehler = [];
        if (!w.betreff) fehler.push("betreff");
        if (!w.themen) fehler.push("themen");
        if (fehler.length) {
          U.markiereFehler(dialog, fehler);
          U.toast("Betreff und besprochene Punkte sind Pflichtfelder.", "err");
          return false;
        }

        var schritteNeu = [];
        dialog.querySelectorAll("#schritte .schritt-row").forEach(function (row, i) {
          var text = row.querySelector('[data-s="text"]').value.trim();
          if (!text) return;
          var alt = (v.naechsteSchritte || [])[i];
          schritteNeu.push({
            text: text,
            verantwortlich: row.querySelector('[data-s="verantwortlich"]').value,
            faellig: row.querySelector('[data-s="faellig"]').value,
            uebernommen: alt && alt.text === text ? !!alt.uebernommen : false
          });
        });

        var daten = {
          betreff: w.betreff, datum: w.datum, uhrzeit: w.uhrzeit,
          dauer: Number(w.dauer) || 0, kanal: w.kanal,
          dealId: w.dealId, kontaktId: w.kontaktId,
          teilnehmer: w.teilnehmer, verfasser: w.verfasser, freigeber: w.freigeber,
          themen: w.themen, ergebnisse: w.ergebnisse, offenePunkte: w.offenePunkte,
          naechsteSchritte: schritteNeu,
          status: w.status, vertraulich: !!w.vertraulich
        };
        if (p) daten.id = p.id;

        var r = S.saveProtokoll(daten, !!w.aufgabenErzeugen);
        U.toast(
          (p ? "Protokoll aktualisiert." : "Protokoll " + r.protokoll.nummer + " angelegt.") +
          (r.aufgaben ? " " + r.aufgaben + " Aufgabe(n) erzeugt." : ""), "ok");
        if (onSaved) onSaved(r.protokoll);
      }
    });
  }

  /* ---------------- Notiz / Aktivität ---------------- */
  function notizForm(dealId, kontaktId, onSaved) {
    var body =
      '<div class="form-grid">' +
        U.feld("Art", U.select("typ", "note", [
          { value: "note", label: "Notiz" },
          { value: "anruf", label: "Telefonat" },
          { value: "email", label: "E-Mail" },
          { value: "termin", label: "Termin" }
        ])) +
        U.feld("Datum", U.input("wann", S.heuteISO(), { typ: "date" })) +
        U.feld("Eintrag *", U.textarea("text", "", "Was ist passiert?"), true) +
      "</div>" +
      '<p class="hint">Für ausführliche Gesprächsnotizen mit Teilnehmern und Maßnahmen ' +
      "eignet sich ein Protokoll besser.</p>";

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
        S.log(w.typ, w.text, dealId, kontaktId);
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
    deal: dealForm,
    kontakt: kontaktForm,
    aufgabe: aufgabeForm,
    protokoll: protokollForm,
    notiz: notizForm
  };
})(window);
