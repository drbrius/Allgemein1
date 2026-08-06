/* OffMarket CRM — Ansichten */
(function (global) {
  "use strict";

  var S = global.Store, U = global.UI, D = global.CRMData, F = global.Forms;

  /* Filterzustand bleibt zwischen den Renderings erhalten */
  var filter = {
    objekte: { q: "", typ: "", stage: "", betreuer: "", sort: "updatedAt", dir: -1, nurOffen: false },
    kontakte: { q: "", typ: "" },
    aufgaben: { modus: "offen", betreuer: "" }
  };

  function leer(titel, text, aktionHtml) {
    return '<div class="empty"><div class="big">' + U.icon("search", 28) + "</div>" +
      "<h3>" + U.esc(titel) + "</h3><p>" + U.esc(text) + "</p>" + (aktionHtml || "") + "</div>";
  }

  function kontaktTyp(id) {
    return D.KONTAKTTYPEN.filter(function (t) { return t.id === id; })[0] || D.KONTAKTTYPEN[5];
  }

  function prio(id) {
    return D.PRIORITAETEN.filter(function (p) { return p.id === id; })[0] || D.PRIORITAETEN[2];
  }

  function aufgabenTyp(id) {
    return D.AUFGABENTYPEN.filter(function (a) { return a.id === id; })[0] || D.AUFGABENTYPEN[4];
  }

  function objektLink(o) {
    return '<a href="#/objekt/' + o.id + '">' + U.esc(o.titel) + "</a>";
  }

  /* =====================================================================
     Dashboard
     ===================================================================== */
  function dashboard() {
    var k = S.kpis();
    var stufen = S.proStage().filter(function (p) { return p.stage.id !== "verloren"; });
    var heute = S.heuteISO();

    var faellige = S.state.aufgaben
      .filter(function (t) { return !t.erledigt && t.faellig && t.faellig <= heute; })
      .sort(function (a, b) { return a.faellig < b.faellig ? -1 : 1; })
      .slice(0, 6);

    var topDeals = S.state.objekte.filter(S.isOffen)
      .sort(function (a, b) { return S.gewichtet(b) - S.gewichtet(a); })
      .slice(0, 6);

    var aktivitaeten = S.state.aktivitaeten.slice(0, 7);

    var kpiCards = [
      { label: "Aktive Deals", icon: "flame", value: U.num(k.aktiveDeals),
        foot: U.num(k.neu30Tage) + " neu in 30 Tagen" },
      { label: "Pipeline-Volumen", icon: "euro", value: U.eurKurz(k.volumen),
        foot: "gewichtet " + U.eurKurz(k.forecast) },
      { label: "Ø Ankaufsfaktor", icon: "chart", value: k.avgFaktor ? U.dez(k.avgFaktor) : "—",
        foot: "Zielfaktor ≤ " + U.num(S.state.einstellungen.zielFaktor) },
      { label: "Abschlussquote", icon: "check", value: U.dez(k.quote) + " %",
        foot: k.gewonnen + " angekauft · " + k.verloren + " verloren" }
    ].map(function (c) {
      return '<div class="card kpi"><div class="label">' + U.icon(c.icon, 15) + U.esc(c.label) + "</div>" +
        '<div class="value">' + c.value + "</div>" +
        '<div class="foot">' + U.esc(c.foot) + "</div></div>";
    }).join("");

    var pipelineBalken = U.balken(stufen.map(function (p) {
      return { label: p.stage.label, wert: p.volumen, farbe: p.stage.color };
    }), U.eurKurz);

    var aufgabenListe = faellige.length ? faellige.map(function (t) {
      var f = U.faelligText(t.faellig);
      var ob = t.objektId ? S.objekt(t.objektId) : null;
      return '<div class="task-row" data-task="' + t.id + '">' +
        '<input type="checkbox" data-toggle="' + t.id + '" aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(t.titel) + "</div>" +
          '<div class="m"><span class="' + f.cls + '">' + U.esc(f.text) + "</span>" +
          (ob ? '<span class="faint">·</span><a href="#/objekt/' + ob.id + '">' + U.esc(ob.titel) + "</a>" : "") +
          '<span class="pill ' + prio(t.prioritaet).cls + '">' + prio(t.prioritaet).label + "</span></div>" +
        "</div></div>";
    }).join("") : '<p class="muted" style="font-size:0.87rem;padding:0.6rem 0">Keine offenen Aufgaben für heute. 🎉</p>';

    var deals = topDeals.length ? '<div class="table-wrap"><table class="data compact"><thead><tr>' +
      "<th>Objekt</th><th>Phase</th><th class=\"num\">Kaufpreis</th><th class=\"num\">Faktor</th><th class=\"num\">Gewichtet</th>" +
      "</tr></thead><tbody>" + topDeals.map(function (o) {
        return "<tr>" +
          '<td><div class="cell-title">' + objektLink(o) + '</div><div class="cell-sub">' + U.esc(o.ort + " · " + o.typ) + "</div></td>" +
          "<td>" + U.stagePill(o.stage) + "</td>" +
          '<td class="num">' + U.eur(o.kaufpreis) + "</td>" +
          '<td class="num">' + (S.faktor(o) ? U.dez(S.faktor(o)) : "—") + "</td>" +
          '<td class="num">' + U.eurKurz(S.gewichtet(o)) + "</td>" +
          "</tr>";
      }).join("") + "</tbody></table></div>"
      : leer("Noch keine aktiven Deals", "Lege dein erstes Objekt an, um die Pipeline zu füllen.",
             '<button class="btn btn-primary" data-neu="objekt">Objekt anlegen</button>');

    var timeline = aktivitaeten.length ? '<div class="timeline">' + aktivitaeten.map(function (a, i) {
      var ob = a.objektId ? S.objekt(a.objektId) : null;
      return '<div class="tl-item"><div class="tl-rail"><div class="tl-dot">' +
        U.icon(a.typ === "anruf" ? "phone" : a.typ === "email" ? "mail" : a.typ === "termin" ? "calendar" :
               a.typ === "stage" ? "kanban" : a.typ === "create" ? "plus" : "note", 13) +
        "</div>" + (i < aktivitaeten.length - 1 ? '<div class="tl-line"></div>' : "") + "</div>" +
        '<div class="tl-body"><div class="txt">' + U.esc(a.text) + "</div>" +
        '<div class="ts">' + U.datumZeit(a.ts) + (ob ? " · " + objektLink(ob) : "") + "</div></div></div>";
    }).join("") + "</div>" : '<p class="muted" style="font-size:0.87rem">Noch keine Aktivitäten erfasst.</p>';

    var monate = S.neuProMonat(6);

    return {
      html:
        '<div class="page-head"><div><h1>Übersicht</h1>' +
          "<p>Guten Tag, " + U.esc(S.state.einstellungen.nutzer.split(" ")[0]) + " — " +
          k.aufgabenUeberfaellig + " überfällige, " + k.aufgabenHeute + " heutige Aufgaben.</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-neu="aufgabe">' + U.icon("plus", 15) + " Aufgabe</button>" +
            '<button class="btn btn-primary" data-neu="objekt">' + U.icon("plus", 15) + " Neues Objekt</button>" +
          "</div></div>" +
        '<div class="stack">' +
          '<div class="grid grid-kpi">' + kpiCards + "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Pipeline nach Phase</h2>' +
              '<span class="sub">' + U.eurKurz(k.volumen) + " offen</span>" +
              '<div class="actions"><a class="btn btn-sm" href="#/pipeline">Kanban öffnen</a></div></div>' +
              '<div class="card-body">' + pipelineBalken + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Heute zu erledigen</h2>' +
              '<div class="actions"><a class="btn btn-sm" href="#/aufgaben">Alle Aufgaben</a></div></div>' +
              '<div class="card-body tight" style="padding:0 1rem">' + aufgabenListe + "</div></div>" +
          "</div>" +
          '<div class="card"><div class="card-head"><h2>Top-Deals nach gewichtetem Volumen</h2>' +
            '<div class="actions"><a class="btn btn-sm" href="#/objekte">Alle Objekte</a></div></div>' + deals + "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Letzte Aktivitäten</h2></div>' +
              '<div class="card-body">' + timeline + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Neu erfasste Objekte je Monat</h2>' +
              '<span class="sub">letzte 6 Monate</span></div>' +
              '<div class="card-body">' + U.saeulen(monate.map(function (m) {
                return { label: m.label, wert: m.anzahl };
              })) + "</div></div>" +
          "</div>" +
        "</div>",
      mount: function (root) {
        root.querySelectorAll("[data-toggle]").forEach(function (cb) {
          cb.addEventListener("change", function () {
            S.toggleAufgabe(cb.getAttribute("data-toggle"));
            U.toast("Aufgabe erledigt.", "ok");
          });
        });
      }
    };
  }

  /* =====================================================================
     Objekte (Liste)
     ===================================================================== */
  function gefilterteObjekte() {
    var f = filter.objekte;
    var q = f.q.toLowerCase();
    var liste = S.state.objekte.filter(function (o) {
      if (f.typ && o.typ !== f.typ) return false;
      if (f.stage && o.stage !== f.stage) return false;
      if (f.betreuer && o.betreuer !== f.betreuer) return false;
      if (f.nurOffen && !S.isOffen(o)) return false;
      if (!q) return true;
      var kt = o.kontaktId ? S.kontaktName(S.kontakt(o.kontaktId)) : "";
      return (o.titel + " " + o.strasse + " " + o.plz + " " + o.ort + " " + o.typ + " " +
              (o.tags || []).join(" ") + " " + kt + " " + o.notizen).toLowerCase().indexOf(q) !== -1;
    });

    var key = f.sort;
    liste.sort(function (a, b) {
      var va, vb;
      if (key === "faktor") { va = S.faktor(a); vb = S.faktor(b); }
      else if (key === "rendite") { va = S.rendite(a); vb = S.rendite(b); }
      else if (key === "stage") {
        va = D.STAGES.findIndex(function (s) { return s.id === a.stage; });
        vb = D.STAGES.findIndex(function (s) { return s.id === b.stage; });
      } else { va = a[key]; vb = b[key]; }
      if (typeof va === "string" || typeof vb === "string") {
        return String(va || "").localeCompare(String(vb || ""), "de") * f.dir;
      }
      return ((va || 0) - (vb || 0)) * f.dir;
    });
    return liste;
  }

  function objekte() {
    var f = filter.objekte;
    var liste = gefilterteObjekte();

    function th(key, label, klasse) {
      var aktiv = f.sort === key;
      return '<th class="sortable ' + (klasse || "") + (aktiv ? " sorted" : "") + '" data-sort="' + key + '">' +
        U.esc(label) + ' <span class="arrow">' + (aktiv ? (f.dir === 1 ? "▲" : "▼") : "↕") + "</span></th>";
    }

    var zeilen = liste.map(function (o) {
      var kt = o.kontaktId ? S.kontakt(o.kontaktId) : null;
      return '<tr data-open="' + o.id + '">' +
        '<td><div class="cell-title">' + U.esc(o.titel) + "</div>" +
          '<div class="cell-sub">' + U.esc([o.strasse, (o.plz + " " + o.ort).trim()].filter(Boolean).join(", ")) + "</div></td>" +
        "<td>" + U.esc(o.typ) + '<div class="cell-sub">' + (o.einheiten ? o.einheiten + " Einh." : "—") + "</div></td>" +
        "<td>" + U.stagePill(o.stage) + "</td>" +
        '<td class="num">' + U.eur(o.kaufpreis) + "</td>" +
        '<td class="num">' + (o.mieteJahr ? U.eur(o.mieteJahr) : "—") + "</td>" +
        '<td class="num">' + (S.faktor(o) ? U.dez(S.faktor(o)) : "—") +
          '<div class="cell-sub">' + (S.rendite(o) ? U.dez(S.rendite(o)) + " %" : "—") + "</div></td>" +
        "<td>" + (kt ? '<a href="#/kontakt/' + kt.id + '">' + U.esc(S.kontaktName(kt)) + "</a>" : '<span class="faint">—</span>') + "</td>" +
        '<td class="nowrap muted">' + U.relativ(o.updatedAt) + "</td>" +
        '<td><div class="row-actions">' +
          '<button class="btn btn-sm btn-icon" data-edit="' + o.id + '" title="Bearbeiten">' + U.icon("edit", 15) + "</button>" +
          '<button class="btn btn-sm btn-icon btn-danger" data-del="' + o.id + '" title="Löschen">' + U.icon("trash", 15) + "</button>" +
        "</div></td></tr>";
    }).join("");

    var summe = liste.reduce(function (s, o) { return s + (o.kaufpreis || 0); }, 0);

    var tabelle = liste.length
      ? '<div class="table-wrap"><table class="data"><thead><tr>' +
          th("titel", "Objekt") + th("typ", "Art") + th("stage", "Phase") +
          th("kaufpreis", "Kaufpreis", "num") + th("mieteJahr", "Miete p. a.", "num") +
          th("faktor", "Faktor · Rendite", "num") +
          "<th>Eigentümer</th>" + th("updatedAt", "Geändert") + "<th></th>" +
        "</tr></thead><tbody>" + zeilen + "</tbody></table></div>"
      : leer("Keine Objekte gefunden", "Passe die Filter an oder lege ein neues Objekt an.",
             '<button class="btn btn-primary" data-neu="objekt">Objekt anlegen</button>');

    return {
      html:
        '<div class="page-head"><div><h1>Objekte</h1>' +
          "<p>" + U.num(liste.length) + " von " + U.num(S.state.objekte.length) +
          " Objekten · Volumen " + U.eurKurz(summe) + "</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-csv="objekte">' + U.icon("download", 15) + " CSV</button>" +
            '<button class="btn btn-primary" data-neu="objekt">' + U.icon("plus", 15) + " Neues Objekt</button>" +
          "</div></div>" +
        '<div class="card"><div class="toolbar">' +
          '<div class="grow"><input type="search" id="f-q" placeholder="Suchen nach Titel, Adresse, Tag …" value="' + U.esc(f.q) + '"></div>' +
          U.select("f-typ", f.typ, D.OBJEKTARTEN, "Alle Objektarten") +
          U.select("f-stage", f.stage, D.STAGES.map(function (s) { return { value: s.id, label: s.label }; }), "Alle Phasen") +
          U.select("f-betreuer", f.betreuer, D.TEAM, "Ganzes Team") +
          '<label class="check"><input type="checkbox" id="f-offen"' + (f.nurOffen ? " checked" : "") + "> nur offene</label>" +
          (f.q || f.typ || f.stage || f.betreuer || f.nurOffen
            ? '<button class="btn btn-sm btn-ghost" id="f-reset">Filter zurücksetzen</button>' : "") +
        "</div>" + tabelle + "</div>",
      mount: function (root) {
        var q = root.querySelector("#f-q");
        q.addEventListener("input", function () {
          filter.objekte.q = q.value;
          global.App.render({ fokus: "#f-q" });
        });
        root.querySelector('[name="f-typ"]').addEventListener("change", function (e) {
          filter.objekte.typ = e.target.value; global.App.render();
        });
        root.querySelector('[name="f-stage"]').addEventListener("change", function (e) {
          filter.objekte.stage = e.target.value; global.App.render();
        });
        root.querySelector('[name="f-betreuer"]').addEventListener("change", function (e) {
          filter.objekte.betreuer = e.target.value; global.App.render();
        });
        root.querySelector("#f-offen").addEventListener("change", function (e) {
          filter.objekte.nurOffen = e.target.checked; global.App.render();
        });
        var reset = root.querySelector("#f-reset");
        if (reset) reset.addEventListener("click", function () {
          filter.objekte = { q: "", typ: "", stage: "", betreuer: "", sort: "updatedAt", dir: -1, nurOffen: false };
          global.App.render();
        });
        root.querySelectorAll("th.sortable").forEach(function (el) {
          el.addEventListener("click", function () {
            var key = el.getAttribute("data-sort");
            if (filter.objekte.sort === key) filter.objekte.dir *= -1;
            else { filter.objekte.sort = key; filter.objekte.dir = key === "titel" || key === "typ" ? 1 : -1; }
            global.App.render();
          });
        });
        root.querySelectorAll("tr[data-open]").forEach(function (tr) {
          tr.addEventListener("click", function (e) {
            if (e.target.closest("button") || e.target.closest("a")) return;
            location.hash = "#/objekt/" + tr.getAttribute("data-open");
          });
        });
        root.querySelectorAll("[data-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.objekt(b.getAttribute("data-edit")); });
        });
        root.querySelectorAll("[data-del]").forEach(function (b) {
          b.addEventListener("click", function () { loescheObjekt(b.getAttribute("data-del")); });
        });
      }
    };
  }

  function loescheObjekt(id, danach) {
    var o = S.objekt(id);
    if (!o) return;
    U.frage("Objekt löschen?", "„" + o.titel + "“ wird aus dem CRM entfernt.", function () {
      var snapshot = S.deleteObjekt(id);
      U.toast("Objekt gelöscht.", "warn", {
        label: "Rückgängig",
        run: function () { S.restoreObjekt(snapshot); U.toast("Wiederhergestellt.", "ok"); }
      });
      if (danach) danach();
    });
  }

  /* =====================================================================
     Objekt-Detail
     ===================================================================== */
  function objektDetail(id) {
    var o = S.objekt(id);
    if (!o) {
      return { html: leer("Objekt nicht gefunden", "Der Eintrag wurde möglicherweise gelöscht.",
        '<a class="btn btn-primary" href="#/objekte">Zur Objektliste</a>'), mount: function () {} };
    }
    var kt = o.kontaktId ? S.kontakt(o.kontaktId) : null;
    var aufgaben = S.aufgabenFuer(o.id, null).sort(function (a, b) {
      return (a.erledigt - b.erledigt) || String(a.faellig).localeCompare(String(b.faellig));
    });
    var aktivitaeten = S.aktivitaetenFuer({ objektId: o.id });

    var fakten = [
      ["Kaufpreis", U.eur(o.kaufpreis)],
      ["Jahresmiete IST", o.mieteJahr ? U.eur(o.mieteJahr) : "—"],
      ["Faktor", S.faktor(o) ? U.dez(S.faktor(o)) : "—"],
      ["Bruttorendite", S.rendite(o) ? U.dez(S.rendite(o)) + " %" : "—"],
      ["Preis je m²", S.preisProQm(o) ? U.eur(S.preisProQm(o)) : "—"],
      ["Fläche", o.wohnflaeche ? U.num(o.wohnflaeche) + " m²" : "—"],
      ["Grundstück", o.grundstueck ? U.num(o.grundstueck) + " m²" : "—"],
      ["Einheiten", o.einheiten ? U.num(o.einheiten) : "—"],
      ["Baujahr", o.baujahr || "—"],
      ["Zustand", o.zustand || "—"],
      ["Quelle", o.quelle || "—"],
      ["Gewichtet", U.eur(S.gewichtet(o))]
    ].map(function (f) {
      return '<div class="fact"><div class="k">' + U.esc(f[0]) + '</div><div class="v">' + f[1] + "</div></div>";
    }).join("");

    var stageBar = '<div class="stage-bar">' + D.STAGES.map(function (s) {
      var on = s.id === o.stage;
      return '<button data-stage="' + s.id + '" class="' + (on ? "on" : "") + '"' +
        (on ? ' style="background:' + s.color + '"' : "") + ">" + U.esc(s.label) + "</button>";
    }).join("") + "</div>";

    var aufgabenHtml = aufgaben.length ? aufgaben.map(function (t) {
      var f = U.faelligText(t.faellig);
      return '<div class="task-row' + (t.erledigt ? " done" : "") + '">' +
        '<input type="checkbox" data-toggle="' + t.id + '"' + (t.erledigt ? " checked" : "") + ' aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(t.titel) + "</div>" +
        '<div class="m"><span class="' + (t.erledigt ? "faint" : f.cls) + '">' +
          (t.erledigt ? "erledigt" : U.esc(f.text)) + "</span>" +
          '<span class="tag">' + aufgabenTyp(t.typ).label + "</span></div></div>" +
        '<button class="btn btn-sm btn-icon btn-ghost" data-task-edit="' + t.id + '">' + U.icon("edit", 14) + "</button>" +
        "</div>";
    }).join("") : '<p class="muted" style="font-size:0.87rem">Keine Aufgaben zu diesem Objekt.</p>';

    var timeline = aktivitaeten.length ? '<div class="timeline">' + aktivitaeten.map(function (a, i) {
      return '<div class="tl-item"><div class="tl-rail"><div class="tl-dot">' +
        U.icon(a.typ === "anruf" ? "phone" : a.typ === "email" ? "mail" : a.typ === "termin" ? "calendar" :
               a.typ === "stage" ? "kanban" : a.typ === "create" ? "plus" : "note", 13) + "</div>" +
        (i < aktivitaeten.length - 1 ? '<div class="tl-line"></div>' : "") + "</div>" +
        '<div class="tl-body"><div class="txt">' + U.esc(a.text) + "</div>" +
        '<div class="ts">' + U.datumZeit(a.ts) + "</div></div></div>";
    }).join("") + "</div>" : '<p class="muted" style="font-size:0.87rem">Noch keine Aktivitäten.</p>';

    var kontaktKarte = kt
      ? '<div class="row" style="gap:0.6rem"><span class="avatar">' + U.esc(U.initialen(S.kontaktName(kt))) + "</span>" +
        '<div><div class="cell-title"><a href="#/kontakt/' + kt.id + '">' + U.esc(S.kontaktName(kt)) + "</a></div>" +
        '<div class="cell-sub">' + U.esc(kt.firma || kontaktTyp(kt.typ).label) + "</div></div></div>" +
        '<div class="divider"></div>' +
        (kt.telefon ? '<div class="row" style="font-size:0.86rem">' + U.icon("phone", 14) +
          '<a href="tel:' + U.esc(kt.telefon.replace(/\s/g, "")) + '">' + U.esc(kt.telefon) + "</a></div>" : "") +
        (kt.email ? '<div class="row" style="font-size:0.86rem;margin-top:0.35rem">' + U.icon("mail", 14) +
          '<a href="mailto:' + U.esc(kt.email) + '">' + U.esc(kt.email) + "</a></div>" : "")
      : '<p class="muted" style="font-size:0.87rem">Kein Eigentümer verknüpft. ' +
        '<button class="btn btn-sm" data-edit-objekt="1">Jetzt zuordnen</button></p>';

    return {
      html:
        '<div class="breadcrumb"><a href="#/objekte">Objekte</a> › ' + U.esc(o.titel) + "</div>" +
        '<div class="page-head"><div>' +
          "<h1>" + U.esc(o.titel) + "</h1>" +
          '<p>' + U.icon("pin", 14) + " " + U.esc([o.strasse, (o.plz + " " + o.ort).trim()].filter(Boolean).join(", ")) +
          " · " + U.esc(o.typ) + " · Betreuer " + U.esc(o.betreuer || "—") + "</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-neu-aktivitaet="1">' + U.icon("note", 15) + " Aktivität</button>" +
            '<button class="btn" data-neu-aufgabe="1">' + U.icon("check", 15) + " Aufgabe</button>" +
            '<button class="btn" data-edit-objekt="1">' + U.icon("edit", 15) + " Bearbeiten</button>" +
            '<button class="btn btn-danger btn-icon" data-del-objekt="1" title="Löschen">' + U.icon("trash", 15) + "</button>" +
          "</div></div>" +
        '<div class="detail-grid">' +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Phase</h2>' +
              '<span class="sub">Wahrscheinlichkeit ' + U.num(o.wahrscheinlichkeit) + " %</span></div>" +
              '<div class="card-body">' + stageBar + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Kennzahlen</h2></div>' +
              '<div class="card-body"><div class="facts">' + fakten + "</div></div></div>" +
            '<div class="card"><div class="card-head"><h2>Notizen</h2>' +
              '<div class="actions"><button class="btn btn-sm" data-edit-objekt="1">Bearbeiten</button></div></div>' +
              '<div class="card-body"><p style="font-size:0.9rem;white-space:pre-wrap">' +
              (o.notizen ? U.esc(o.notizen) : '<span class="muted">Keine Notizen hinterlegt.</span>') + "</p></div></div>" +
            '<div class="card"><div class="card-head"><h2>Aufgaben</h2>' +
              '<div class="actions"><button class="btn btn-sm" data-neu-aufgabe="1">' + U.icon("plus", 14) + " Aufgabe</button></div></div>" +
              '<div class="card-body" style="padding:0 1rem">' + aufgabenHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Verlauf</h2>' +
              '<div class="actions"><button class="btn btn-sm" data-neu-aktivitaet="1">' + U.icon("plus", 14) + " Eintrag</button></div></div>" +
              '<div class="card-body">' + timeline + "</div></div>" +
          "</div>" +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Eigentümer</h2></div>' +
              '<div class="card-body">' + kontaktKarte + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Merkmale</h2></div>' +
              '<div class="card-body"><div class="row">' +
                (o.tags && o.tags.length
                  ? o.tags.map(function (t) { return '<span class="tag">' + U.esc(t) + "</span>"; }).join("")
                  : '<span class="muted" style="font-size:0.86rem">Keine Schlagwörter</span>') +
              "</div>" +
              '<div class="divider"></div>' +
              '<div style="font-size:0.82rem" class="muted">Angelegt ' + U.datum(o.createdAt) +
              "<br>Zuletzt geändert " + U.datum(o.updatedAt) + " (" + U.relativ(o.updatedAt) + ")</div>" +
              "</div></div>" +
          "</div>" +
        "</div>",
      mount: function (root) {
        root.querySelectorAll("[data-stage]").forEach(function (b) {
          b.addEventListener("click", function () {
            S.setStage(o.id, b.getAttribute("data-stage"));
            U.toast("Phase aktualisiert.", "ok");
          });
        });
        root.querySelectorAll("[data-edit-objekt]").forEach(function (b) {
          b.addEventListener("click", function () { F.objekt(o.id); });
        });
        root.querySelectorAll("[data-neu-aufgabe]").forEach(function (b) {
          b.addEventListener("click", function () {
            F.aufgabe(null, { objektId: o.id, kontaktId: o.kontaktId || "" });
          });
        });
        root.querySelectorAll("[data-neu-aktivitaet]").forEach(function (b) {
          b.addEventListener("click", function () { F.notiz(o.id, o.kontaktId || ""); });
        });
        root.querySelectorAll("[data-task-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.aufgabe(b.getAttribute("data-task-edit")); });
        });
        root.querySelectorAll("[data-toggle]").forEach(function (cb) {
          cb.addEventListener("change", function () { S.toggleAufgabe(cb.getAttribute("data-toggle")); });
        });
        var del = root.querySelector("[data-del-objekt]");
        if (del) del.addEventListener("click", function () {
          loescheObjekt(o.id, function () { location.hash = "#/objekte"; });
        });
      }
    };
  }

  /* =====================================================================
     Pipeline (Kanban)
     ===================================================================== */
  function pipeline() {
    var spalten = S.proStage();

    var html = spalten.map(function (p) {
      var karten = p.objekte
        .sort(function (a, b) { return b.kaufpreis - a.kaufpreis; })
        .map(function (o) {
          var kt = o.kontaktId ? S.kontakt(o.kontaktId) : null;
          return '<article class="kcard" draggable="true" data-id="' + o.id + '">' +
            '<div class="t">' + U.esc(o.titel) + "</div>" +
            '<div class="a">' + U.esc((o.plz ? o.plz + " " : "") + o.ort) + "</div>" +
            '<div class="meta"><span class="price">' + U.eurKurz(o.kaufpreis) + "</span>" +
              (S.faktor(o) ? '<span class="tag">F ' + U.dez(S.faktor(o)) + "</span>" : "") +
              (kt ? '<span class="tag">' + U.esc(U.initialen(S.kontaktName(kt))) + "</span>" : "") +
            "</div></article>";
        }).join("");

      return '<section class="kcol" data-stage="' + p.stage.id + '">' +
        '<div class="kcol-head"><span class="dot" style="background:' + p.stage.color + '"></span>' +
          U.esc(p.stage.label) + '<span class="n">' + p.anzahl + "</span></div>" +
        '<div class="kcol-sum">' + U.eurKurz(p.volumen) + "</div>" +
        '<div class="kcol-body">' + (karten || '<div class="kempty">Hierher ziehen</div>') + "</div>" +
        "</section>";
    }).join("");

    var k = S.kpis();

    return {
      html:
        '<div class="page-head"><div><h1>Pipeline</h1>' +
          "<p>" + U.num(k.aktiveDeals) + " aktive Deals · " + U.eurKurz(k.volumen) +
          " Volumen · gewichtet " + U.eurKurz(k.forecast) + "</p></div>" +
          '<div class="actions"><button class="btn btn-primary" data-neu="objekt">' +
            U.icon("plus", 15) + " Neues Objekt</button></div></div>" +
        '<div class="kanban">' + html + "</div>",
      mount: function (root) {
        var gezogen = null;

        root.querySelectorAll(".kcard").forEach(function (card) {
          card.addEventListener("dragstart", function (e) {
            gezogen = card.getAttribute("data-id");
            card.classList.add("dragging");
            e.dataTransfer.effectAllowed = "move";
            try { e.dataTransfer.setData("text/plain", gezogen); } catch (err) { /* ältere Browser */ }
          });
          card.addEventListener("dragend", function () {
            card.classList.remove("dragging");
            gezogen = null;
          });
          card.addEventListener("click", function () {
            location.hash = "#/objekt/" + card.getAttribute("data-id");
          });
        });

        root.querySelectorAll(".kcol").forEach(function (col) {
          col.addEventListener("dragover", function (e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
            col.classList.add("dragover");
          });
          col.addEventListener("dragleave", function () { col.classList.remove("dragover"); });
          col.addEventListener("drop", function (e) {
            e.preventDefault();
            col.classList.remove("dragover");
            var id = gezogen || e.dataTransfer.getData("text/plain");
            if (!id) return;
            var neueStage = col.getAttribute("data-stage");
            var o = S.objekt(id);
            if (!o || o.stage === neueStage) return;
            S.setStage(id, neueStage);
            U.toast("„" + o.titel + "“ → " + S.stage(neueStage).label, "ok");
          });
        });
      }
    };
  }

  /* =====================================================================
     Kontakte
     ===================================================================== */
  function kontakte() {
    var f = filter.kontakte;
    var q = f.q.toLowerCase();
    var liste = S.state.kontakte.filter(function (k) {
      if (f.typ && k.typ !== f.typ) return false;
      if (!q) return true;
      return (S.kontaktName(k) + " " + k.firma + " " + k.email + " " + k.telefon + " " + k.ort + " " +
              (k.tags || []).join(" ")).toLowerCase().indexOf(q) !== -1;
    }).sort(function (a, b) { return S.kontaktName(a).localeCompare(S.kontaktName(b), "de"); });

    var zeilen = liste.map(function (k) {
      var objekteAnzahl = S.state.objekte.filter(function (o) { return o.kontaktId === k.id; });
      var volumen = objekteAnzahl.reduce(function (s, o) { return s + (o.kaufpreis || 0); }, 0);
      var t = kontaktTyp(k.typ);
      return '<tr data-open="' + k.id + '">' +
        '<td><div class="row" style="gap:0.55rem;flex-wrap:nowrap">' +
          '<span class="avatar">' + U.esc(U.initialen(S.kontaktName(k))) + "</span>" +
          '<div><div class="cell-title">' + U.esc(S.kontaktName(k)) + "</div>" +
          '<div class="cell-sub">' + U.esc(k.firma || "—") + "</div></div></div></td>" +
        '<td><span class="pill ' + t.cls + '">' + U.esc(t.label) + "</span></td>" +
        "<td>" + (k.telefon ? '<a href="tel:' + U.esc(k.telefon.replace(/\s/g, "")) + '">' + U.esc(k.telefon) + "</a>" : '<span class="faint">—</span>') +
          '<div class="cell-sub">' + (k.email ? '<a href="mailto:' + U.esc(k.email) + '">' + U.esc(k.email) + "</a>" : "—") + "</div></td>" +
        "<td>" + U.esc(k.ort || "—") + "</td>" +
        '<td class="num">' + objekteAnzahl.length + "</td>" +
        '<td class="num">' + (volumen ? U.eurKurz(volumen) : "—") + "</td>" +
        '<td><div class="row-actions">' +
          '<button class="btn btn-sm btn-icon" data-edit="' + k.id + '" title="Bearbeiten">' + U.icon("edit", 15) + "</button>" +
          '<button class="btn btn-sm btn-icon btn-danger" data-del="' + k.id + '" title="Löschen">' + U.icon("trash", 15) + "</button>" +
        "</div></td></tr>";
    }).join("");

    var tabelle = liste.length
      ? '<div class="table-wrap"><table class="data"><thead><tr>' +
        "<th>Name</th><th>Rolle</th><th>Kontakt</th><th>Ort</th>" +
        '<th class="num">Objekte</th><th class="num">Volumen</th><th></th>' +
        "</tr></thead><tbody>" + zeilen + "</tbody></table></div>"
      : leer("Keine Kontakte gefunden", "Passe die Suche an oder lege einen neuen Kontakt an.",
             '<button class="btn btn-primary" data-neu="kontakt">Kontakt anlegen</button>');

    return {
      html:
        '<div class="page-head"><div><h1>Kontakte</h1>' +
          "<p>" + U.num(liste.length) + " von " + U.num(S.state.kontakte.length) + " Kontakten</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-csv="kontakte">' + U.icon("download", 15) + " CSV</button>" +
            '<button class="btn btn-primary" data-neu="kontakt">' + U.icon("plus", 15) + " Neuer Kontakt</button>" +
          "</div></div>" +
        '<div class="card"><div class="toolbar">' +
          '<div class="grow"><input type="search" id="k-q" placeholder="Name, Firma, Telefon, Ort …" value="' + U.esc(f.q) + '"></div>' +
          U.select("k-typ", f.typ, D.KONTAKTTYPEN.map(function (t) { return { value: t.id, label: t.label }; }), "Alle Rollen") +
        "</div>" + tabelle + "</div>",
      mount: function (root) {
        var q = root.querySelector("#k-q");
        q.addEventListener("input", function () {
          filter.kontakte.q = q.value;
          global.App.render({ fokus: "#k-q" });
        });
        root.querySelector('[name="k-typ"]').addEventListener("change", function (e) {
          filter.kontakte.typ = e.target.value; global.App.render();
        });
        root.querySelectorAll("tr[data-open]").forEach(function (tr) {
          tr.addEventListener("click", function (e) {
            if (e.target.closest("button") || e.target.closest("a")) return;
            location.hash = "#/kontakt/" + tr.getAttribute("data-open");
          });
        });
        root.querySelectorAll("[data-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.kontakt(b.getAttribute("data-edit")); });
        });
        root.querySelectorAll("[data-del]").forEach(function (b) {
          b.addEventListener("click", function () { loescheKontakt(b.getAttribute("data-del")); });
        });
      }
    };
  }

  function loescheKontakt(id, danach) {
    var k = S.kontakt(id);
    if (!k) return;
    U.frage("Kontakt löschen?", S.kontaktName(k) + " wird entfernt. Verknüpfte Objekte bleiben erhalten.", function () {
      var snapshot = S.deleteKontakt(id);
      U.toast("Kontakt gelöscht.", "warn", {
        label: "Rückgängig",
        run: function () { S.restoreKontakt(snapshot); U.toast("Wiederhergestellt.", "ok"); }
      });
      if (danach) danach();
    });
  }

  /* =====================================================================
     Kontakt-Detail
     ===================================================================== */
  function kontaktDetail(id) {
    var k = S.kontakt(id);
    if (!k) {
      return { html: leer("Kontakt nicht gefunden", "Der Eintrag wurde möglicherweise gelöscht.",
        '<a class="btn btn-primary" href="#/kontakte">Zur Kontaktliste</a>'), mount: function () {} };
    }
    var t = kontaktTyp(k.typ);
    var objekteListe = S.state.objekte.filter(function (o) { return o.kontaktId === k.id; });
    var volumen = objekteListe.reduce(function (s, o) { return s + (o.kaufpreis || 0); }, 0);
    var aufgaben = S.aufgabenFuer(null, k.id);
    var aktivitaeten = S.aktivitaetenFuer({ kontaktId: k.id });

    var objekteHtml = objekteListe.length
      ? '<ul class="list-plain">' + objekteListe.map(function (o) {
          return '<li><div class="grow"><div class="cell-title">' + objektLink(o) + "</div>" +
            '<div class="cell-sub">' + U.esc(o.ort + " · " + o.typ) + "</div></div>" +
            U.stagePill(o.stage) + '<span class="mono nowrap">' + U.eurKurz(o.kaufpreis) + "</span></li>";
        }).join("") + "</ul>"
      : '<p class="muted" style="font-size:0.87rem">Keine Objekte verknüpft.</p>';

    var aufgabenHtml = aufgaben.length ? aufgaben.map(function (a) {
      var f = U.faelligText(a.faellig);
      return '<div class="task-row' + (a.erledigt ? " done" : "") + '">' +
        '<input type="checkbox" data-toggle="' + a.id + '"' + (a.erledigt ? " checked" : "") + ' aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(a.titel) + "</div>" +
        '<div class="m"><span class="' + (a.erledigt ? "faint" : f.cls) + '">' +
        (a.erledigt ? "erledigt" : U.esc(f.text)) + "</span></div></div></div>";
    }).join("") : '<p class="muted" style="font-size:0.87rem">Keine Aufgaben.</p>';

    var timeline = aktivitaeten.length ? '<div class="timeline">' + aktivitaeten.map(function (a, i) {
      return '<div class="tl-item"><div class="tl-rail"><div class="tl-dot">' +
        U.icon(a.typ === "anruf" ? "phone" : a.typ === "email" ? "mail" : a.typ === "termin" ? "calendar" : "note", 13) +
        "</div>" + (i < aktivitaeten.length - 1 ? '<div class="tl-line"></div>' : "") + "</div>" +
        '<div class="tl-body"><div class="txt">' + U.esc(a.text) + "</div>" +
        '<div class="ts">' + U.datumZeit(a.ts) + "</div></div></div>";
    }).join("") + "</div>" : '<p class="muted" style="font-size:0.87rem">Noch keine Aktivitäten.</p>';

    return {
      html:
        '<div class="breadcrumb"><a href="#/kontakte">Kontakte</a> › ' + U.esc(S.kontaktName(k)) + "</div>" +
        '<div class="page-head"><div class="row" style="gap:0.8rem;flex-wrap:nowrap">' +
          '<span class="avatar" style="width:44px;height:44px;font-size:1rem">' + U.esc(U.initialen(S.kontaktName(k))) + "</span>" +
          "<div><h1>" + U.esc(S.kontaktName(k)) + "</h1>" +
          '<p><span class="pill ' + t.cls + '">' + U.esc(t.label) + "</span> " +
          U.esc(k.firma ? " · " + k.firma : "") + U.esc(k.ort ? " · " + k.ort : "") + "</p></div></div>" +
          '<div class="actions">' +
            '<button class="btn" data-neu-aktivitaet="1">' + U.icon("note", 15) + " Aktivität</button>" +
            '<button class="btn" data-neu-aufgabe="1">' + U.icon("check", 15) + " Aufgabe</button>" +
            '<button class="btn" data-edit-kontakt="1">' + U.icon("edit", 15) + " Bearbeiten</button>" +
            '<button class="btn btn-danger btn-icon" data-del-kontakt="1" title="Löschen">' + U.icon("trash", 15) + "</button>" +
          "</div></div>" +
        '<div class="detail-grid">' +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Verknüpfte Objekte</h2>' +
              '<span class="sub">' + objekteListe.length + " · " + U.eurKurz(volumen) + "</span></div>" +
              '<div class="card-body">' + objekteHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Notizen</h2></div>' +
              '<div class="card-body"><p style="font-size:0.9rem;white-space:pre-wrap">' +
              (k.notizen ? U.esc(k.notizen) : '<span class="muted">Keine Notizen hinterlegt.</span>') + "</p></div></div>" +
            '<div class="card"><div class="card-head"><h2>Aufgaben</h2></div>' +
              '<div class="card-body" style="padding:0 1rem">' + aufgabenHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Verlauf</h2></div>' +
              '<div class="card-body">' + timeline + "</div></div>" +
          "</div>" +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Kontaktdaten</h2></div><div class="card-body">' +
              '<ul class="list-plain" style="font-size:0.87rem">' +
                (k.telefon ? "<li>" + U.icon("phone", 15) + '<a class="grow" href="tel:' + U.esc(k.telefon.replace(/\s/g, "")) + '">' + U.esc(k.telefon) + "</a></li>" : "") +
                (k.email ? "<li>" + U.icon("mail", 15) + '<a class="grow" href="mailto:' + U.esc(k.email) + '">' + U.esc(k.email) + "</a></li>" : "") +
                ((k.strasse || k.ort) ? "<li>" + U.icon("pin", 15) + '<span class="grow">' +
                  U.esc([k.strasse, (k.plz + " " + k.ort).trim()].filter(Boolean).join(", ")) + "</span></li>" : "") +
                "<li>" + U.icon("clock", 15) + '<span class="grow muted">Kontakt seit ' + U.datum(k.createdAt) + "</span></li>" +
              "</ul></div></div>" +
            '<div class="card"><div class="card-head"><h2>Merkmale</h2></div><div class="card-body"><div class="row">' +
              (k.tags && k.tags.length
                ? k.tags.map(function (x) { return '<span class="tag">' + U.esc(x) + "</span>"; }).join("")
                : '<span class="muted" style="font-size:0.86rem">Keine Schlagwörter</span>') +
            "</div></div></div>" +
          "</div>" +
        "</div>",
      mount: function (root) {
        root.querySelectorAll("[data-edit-kontakt]").forEach(function (b) {
          b.addEventListener("click", function () { F.kontakt(k.id); });
        });
        root.querySelectorAll("[data-neu-aufgabe]").forEach(function (b) {
          b.addEventListener("click", function () { F.aufgabe(null, { kontaktId: k.id }); });
        });
        root.querySelectorAll("[data-neu-aktivitaet]").forEach(function (b) {
          b.addEventListener("click", function () { F.notiz("", k.id); });
        });
        root.querySelectorAll("[data-toggle]").forEach(function (cb) {
          cb.addEventListener("change", function () { S.toggleAufgabe(cb.getAttribute("data-toggle")); });
        });
        var del = root.querySelector("[data-del-kontakt]");
        if (del) del.addEventListener("click", function () {
          loescheKontakt(k.id, function () { location.hash = "#/kontakte"; });
        });
      }
    };
  }

  /* =====================================================================
     Aufgaben
     ===================================================================== */
  function aufgaben() {
    var f = filter.aufgaben;
    var heute = S.heuteISO();
    var alle = S.state.aufgaben.slice().sort(function (a, b) {
      return String(a.faellig || "9999").localeCompare(String(b.faellig || "9999"));
    });

    var sichtbar = alle.filter(function (t) {
      if (f.modus === "offen") return !t.erledigt;
      if (f.modus === "ueberfaellig") return !t.erledigt && t.faellig && t.faellig < heute;
      if (f.modus === "erledigt") return t.erledigt;
      return true;
    });

    function gruppe(titel, liste, klasse) {
      if (!liste.length) return "";
      return '<div class="card"><div class="card-head"><h2 class="' + (klasse || "") + '">' + U.esc(titel) + "</h2>" +
        '<span class="sub">' + liste.length + "</span></div>" +
        '<div class="card-body" style="padding:0 1rem">' + liste.map(zeile).join("") + "</div></div>";
    }

    function zeile(t) {
      var fl = U.faelligText(t.faellig);
      var ob = t.objektId ? S.objekt(t.objektId) : null;
      var kt = t.kontaktId ? S.kontakt(t.kontaktId) : null;
      return '<div class="task-row' + (t.erledigt ? " done" : "") + '">' +
        '<input type="checkbox" data-toggle="' + t.id + '"' + (t.erledigt ? " checked" : "") + ' aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(t.titel) + "</div>" +
          '<div class="m">' +
            '<span class="tag">' + U.esc(aufgabenTyp(t.typ).label) + "</span>" +
            '<span class="' + (t.erledigt ? "faint" : fl.cls) + '">' + (t.erledigt ? "erledigt" : U.esc(fl.text)) + "</span>" +
            '<span class="pill ' + prio(t.prioritaet).cls + '">' + prio(t.prioritaet).label + "</span>" +
            (ob ? '<a href="#/objekt/' + ob.id + '">' + U.esc(ob.titel) + "</a>" : "") +
            (kt ? '<a href="#/kontakt/' + kt.id + '">' + U.esc(S.kontaktName(kt)) + "</a>" : "") +
            (t.notiz ? '<span class="faint">' + U.esc(t.notiz) + "</span>" : "") +
          "</div></div>" +
        '<button class="btn btn-sm btn-icon btn-ghost" data-task-edit="' + t.id + '" title="Bearbeiten">' + U.icon("edit", 14) + "</button>" +
        '<button class="btn btn-sm btn-icon btn-ghost" data-task-del="' + t.id + '" title="Löschen">' + U.icon("trash", 14) + "</button>" +
        "</div>";
    }

    var ueberfaellig = sichtbar.filter(function (t) { return !t.erledigt && t.faellig && t.faellig < heute; });
    var heuteListe   = sichtbar.filter(function (t) { return !t.erledigt && t.faellig === heute; });
    var woche        = sichtbar.filter(function (t) {
      var d = U.tageBis(t.faellig);
      return !t.erledigt && d !== null && d > 0 && d <= 7;
    });
    var spaeter      = sichtbar.filter(function (t) {
      var d = U.tageBis(t.faellig);
      return !t.erledigt && (d === null || d > 7);
    });
    var erledigt     = sichtbar.filter(function (t) { return t.erledigt; });

    var inhalt = sichtbar.length
      ? gruppe("Überfällig", ueberfaellig, "overdue") +
        gruppe("Heute", heuteListe, "due-today") +
        gruppe("Diese Woche", woche) +
        gruppe("Später", spaeter) +
        gruppe("Erledigt", erledigt)
      : leer("Keine Aufgaben", "In dieser Ansicht gibt es nichts zu tun.",
             '<button class="btn btn-primary" data-neu="aufgabe">Aufgabe anlegen</button>');

    var tabs = [
      { id: "offen", label: "Offen" },
      { id: "ueberfaellig", label: "Überfällig" },
      { id: "erledigt", label: "Erledigt" },
      { id: "alle", label: "Alle" }
    ].map(function (t) {
      return '<button class="btn btn-sm' + (f.modus === t.id ? " btn-primary" : "") + '" data-modus="' + t.id + '">' +
        U.esc(t.label) + "</button>";
    }).join("");

    return {
      html:
        '<div class="page-head"><div><h1>Aufgaben</h1>' +
          "<p>" + sichtbar.length + " Einträge in dieser Ansicht</p></div>" +
          '<div class="actions"><button class="btn btn-primary" data-neu="aufgabe">' +
            U.icon("plus", 15) + " Neue Aufgabe</button></div></div>" +
        '<div class="row" style="margin-bottom:1rem">' + tabs + "</div>" +
        '<div class="stack">' + inhalt + "</div>",
      mount: function (root) {
        root.querySelectorAll("[data-modus]").forEach(function (b) {
          b.addEventListener("click", function () {
            filter.aufgaben.modus = b.getAttribute("data-modus");
            global.App.render();
          });
        });
        root.querySelectorAll("[data-toggle]").forEach(function (cb) {
          cb.addEventListener("change", function () { S.toggleAufgabe(cb.getAttribute("data-toggle")); });
        });
        root.querySelectorAll("[data-task-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.aufgabe(b.getAttribute("data-task-edit")); });
        });
        root.querySelectorAll("[data-task-del]").forEach(function (b) {
          b.addEventListener("click", function () {
            var snapshot = S.deleteAufgabe(b.getAttribute("data-task-del"));
            U.toast("Aufgabe gelöscht.", "warn", {
              label: "Rückgängig",
              run: function () { S.restoreAufgabe(snapshot); }
            });
          });
        });
      }
    };
  }

  /* =====================================================================
     Berichte
     ===================================================================== */
  function berichte() {
    var k = S.kpis();
    var stufen = S.proStage();

    var trichterStufen = stufen
      .filter(function (p) { return p.stage.id !== "verloren"; })
      .map(function (p) { return { label: p.stage.label, wert: p.anzahl, farbe: p.stage.color }; });

    var palette = ["#4f6df5", "#22c55e", "#f59e0b", "#a78bfa", "#0ea5e9", "#ef4444", "#14b8a6", "#94a3b8"];

    var nachArt = S.gruppiereNach("typ").map(function (g, i) {
      return { label: g.key, wert: g.volumen, farbe: palette[i % palette.length] };
    });

    var nachOrt = S.gruppiereNach("ort").slice(0, 8).map(function (g, i) {
      return { label: g.key, wert: g.volumen, farbe: palette[i % palette.length] };
    });

    /* Quellen-Auswertung */
    var quellen = {};
    S.state.objekte.forEach(function (o) {
      var q = o.quelle || "Ohne Angabe";
      if (!quellen[q]) quellen[q] = { key: q, anzahl: 0, volumen: 0, gewonnen: 0, verloren: 0 };
      quellen[q].anzahl++;
      quellen[q].volumen += o.kaufpreis || 0;
      if (o.stage === "gewonnen") quellen[q].gewonnen++;
      if (o.stage === "verloren") quellen[q].verloren++;
    });
    var quellenListe = Object.keys(quellen).map(function (q) { return quellen[q]; })
      .sort(function (a, b) { return b.volumen - a.volumen; });

    var quellenTabelle = '<div class="table-wrap"><table class="data"><thead><tr>' +
      '<th>Quelle</th><th class="num">Objekte</th><th class="num">Volumen</th>' +
      '<th class="num">Angekauft</th><th class="num">Quote</th></tr></thead><tbody>' +
      quellenListe.map(function (q) {
        var entschieden = q.gewonnen + q.verloren;
        return "<tr><td>" + U.esc(q.key) + "</td>" +
          '<td class="num">' + q.anzahl + "</td>" +
          '<td class="num">' + U.eurKurz(q.volumen) + "</td>" +
          '<td class="num">' + q.gewonnen + "</td>" +
          '<td class="num">' + (entschieden ? U.dez((q.gewonnen / entschieden) * 100) + " %" : "—") + "</td></tr>";
      }).join("") + "</tbody></table></div>";

    /* Team-Auswertung */
    var team = {};
    S.state.objekte.forEach(function (o) {
      var b = o.betreuer || "Nicht zugeordnet";
      if (!team[b]) team[b] = { key: b, aktiv: 0, volumen: 0, gewichtet: 0, gewonnen: 0 };
      if (S.isOffen(o)) {
        team[b].aktiv++;
        team[b].volumen += o.kaufpreis || 0;
        team[b].gewichtet += S.gewichtet(o);
      }
      if (o.stage === "gewonnen") team[b].gewonnen++;
    });
    var teamListe = Object.keys(team).map(function (t) { return team[t]; })
      .sort(function (a, b) { return b.gewichtet - a.gewichtet; });

    var teamTabelle = '<div class="table-wrap"><table class="data"><thead><tr>' +
      '<th>Betreuer</th><th class="num">Aktive Deals</th><th class="num">Volumen</th>' +
      '<th class="num">Gewichtet</th><th class="num">Angekauft</th></tr></thead><tbody>' +
      teamListe.map(function (t) {
        return '<tr><td><div class="row" style="gap:0.5rem;flex-wrap:nowrap"><span class="avatar" style="width:26px;height:26px;font-size:0.68rem">' +
          U.esc(U.initialen(t.key)) + "</span>" + U.esc(t.key) + "</div></td>" +
          '<td class="num">' + t.aktiv + "</td>" +
          '<td class="num">' + U.eurKurz(t.volumen) + "</td>" +
          '<td class="num">' + U.eurKurz(t.gewichtet) + "</td>" +
          '<td class="num">' + t.gewonnen + "</td></tr>";
      }).join("") + "</tbody></table></div>";

    var monate = S.neuProMonat(12);

    return {
      html:
        '<div class="page-head"><div><h1>Auswertungen</h1>' +
          "<p>Kennzahlen über " + U.num(k.objekteGesamt) + " Objekte und " + U.num(k.kontakte) + " Kontakte</p></div>" +
          '<div class="actions"><button class="btn" onclick="window.print()">Drucken</button></div></div>' +
        '<div class="stack">' +
          '<div class="grid grid-kpi">' +
            '<div class="card kpi"><div class="label">' + U.icon("euro", 15) + "Ankaufsvolumen</div>" +
              '<div class="value">' + U.eurKurz(k.ankaufsvolumen) + '</div><div class="foot">' + k.gewonnen + " abgeschlossene Ankäufe</div></div>" +
            '<div class="card kpi"><div class="label">' + U.icon("chart", 15) + "Forecast (gewichtet)</div>" +
              '<div class="value">' + U.eurKurz(k.forecast) + '</div><div class="foot">aus ' + k.aktiveDeals + " aktiven Deals</div></div>" +
            '<div class="card kpi"><div class="label">' + U.icon("check", 15) + "Abschlussquote</div>" +
              '<div class="value">' + U.dez(k.quote) + ' %</div><div class="foot">' + k.gewonnen + " von " + (k.gewonnen + k.verloren) + " entschieden</div></div>" +
            '<div class="card kpi"><div class="label">' + U.icon("clock", 15) + "Offene Aufgaben</div>" +
              '<div class="value">' + k.aufgabenOffen + '</div><div class="foot">' + k.aufgabenUeberfaellig + " überfällig</div></div>" +
          "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Funnel nach Phase</h2><span class="sub">Anzahl Objekte</span></div>' +
              '<div class="card-body">' + U.trichter(trichterStufen) + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Volumen nach Objektart</h2></div>' +
              '<div class="card-body">' + U.donut(nachArt, U.eurKurz) + "</div></div>" +
          "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Volumen nach Standort</h2></div>' +
              '<div class="card-body">' + (nachOrt.length ? U.balken(nachOrt, U.eurKurz) : '<p class="muted">Keine Daten</p>') + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Neue Objekte je Monat</h2><span class="sub">12 Monate</span></div>' +
              '<div class="card-body">' + U.saeulen(monate.map(function (m) { return { label: m.label, wert: m.anzahl }; })) + "</div></div>" +
          "</div>" +
          '<div class="card"><div class="card-head"><h2>Quellen-Performance</h2></div>' + quellenTabelle + "</div>" +
          '<div class="card"><div class="card-head"><h2>Team-Performance</h2></div>' + teamTabelle + "</div>" +
        "</div>",
      mount: function () {}
    };
  }

  /* =====================================================================
     Einstellungen
     ===================================================================== */
  function einstellungen() {
    var e = S.state.einstellungen;
    var groesse = 0;
    try { groesse = (localStorage.getItem("offmarket-crm-v1") || "").length; } catch (err) { /* ignorieren */ }

    return {
      html:
        '<div class="page-head"><div><h1>Einstellungen</h1>' +
          "<p>Profil, Darstellung und Datenverwaltung</p></div></div>" +
        '<div class="grid grid-2">' +
          '<div class="card"><div class="card-head"><h2>Profil</h2></div><div class="card-body">' +
            '<div class="form-grid">' +
              U.feld("Unternehmen", U.input("firma", e.firma), true) +
              U.feld("Angemeldet als", U.select("nutzer", e.nutzer, D.TEAM)) +
              U.feld("Zielfaktor (max.)", U.input("zielFaktor", e.zielFaktor, { typ: "number", min: 1 })) +
            "</div>" +
            '<div class="divider"></div>' +
            '<button class="btn btn-primary" id="profil-speichern">Speichern</button>' +
          "</div></div>" +
          '<div class="card"><div class="card-head"><h2>Darstellung</h2></div><div class="card-body">' +
            '<p class="muted" style="font-size:0.87rem;margin-bottom:0.7rem">Das Design folgt standardmäßig deiner Systemeinstellung.</p>' +
            '<div class="row">' +
              '<button class="btn' + (e.theme === "light" ? " btn-primary" : "") + '" data-theme-set="light">' + U.icon("sun", 15) + " Hell</button>" +
              '<button class="btn' + (e.theme === "dark" ? " btn-primary" : "") + '" data-theme-set="dark">' + U.icon("moon", 15) + " Dunkel</button>" +
              '<button class="btn' + ((e.theme || "auto") === "auto" ? " btn-primary" : "") + '" data-theme-set="auto">System</button>' +
            "</div></div></div>" +
          '<div class="card span-2"><div class="card-head"><h2>Daten</h2>' +
            '<span class="sub">' + U.num(S.state.objekte.length) + " Objekte · " + U.num(S.state.kontakte.length) +
            " Kontakte · " + U.num(S.state.aufgaben.length) + " Aufgaben · " + U.num(Math.round(groesse / 1024)) + " KB</span></div>" +
            '<div class="card-body">' +
              '<p class="muted" style="font-size:0.87rem;margin-bottom:0.8rem">' +
              "Alle Daten liegen ausschließlich lokal im Browser (localStorage). Für ein Backup oder den Wechsel des Geräts nutze den JSON-Export.</p>" +
              '<div class="row">' +
                '<button class="btn" id="export-json">' + U.icon("download", 15) + " JSON-Export</button>" +
                '<button class="btn" id="import-json">' + U.icon("upload", 15) + " JSON-Import</button>" +
                '<button class="btn" data-csv="objekte">' + U.icon("download", 15) + " Objekte als CSV</button>" +
                '<button class="btn" data-csv="kontakte">' + U.icon("download", 15) + " Kontakte als CSV</button>" +
                '<input type="file" id="import-file" accept="application/json,.json" hidden>' +
              "</div>" +
              '<div class="divider"></div>' +
              '<div class="row">' +
                '<button class="btn" id="demo-laden">Demo-Datensatz laden</button>' +
                '<button class="btn btn-danger" id="alles-loeschen">Alle Daten löschen</button>' +
              "</div>" +
            "</div></div>" +
          '<div class="card span-2"><div class="card-head"><h2>Tastenkürzel</h2></div><div class="card-body">' +
            '<ul class="list-plain" style="font-size:0.87rem">' +
              "<li><kbd>/</kbd><span class=\"grow\">Suche fokussieren</span></li>" +
              "<li><kbd>N</kbd><span class=\"grow\">Neues Objekt anlegen</span></li>" +
              "<li><kbd>Esc</kbd><span class=\"grow\">Dialog schließen</span></li>" +
            "</ul></div></div>" +
        "</div>",
      mount: function (root) {
        root.querySelector("#profil-speichern").addEventListener("click", function () {
          S.setEinstellung("firma", root.querySelector('[name="firma"]').value.trim() || "OffMarket Partners");
          S.setEinstellung("nutzer", root.querySelector('[name="nutzer"]').value);
          S.setEinstellung("zielFaktor", Number(root.querySelector('[name="zielFaktor"]').value) || 20);
          U.toast("Einstellungen gespeichert.", "ok");
          global.App.render();
        });
        root.querySelectorAll("[data-theme-set]").forEach(function (b) {
          b.addEventListener("click", function () {
            global.App.setTheme(b.getAttribute("data-theme-set"));
          });
        });
        root.querySelector("#export-json").addEventListener("click", function () {
          U.download("offmarket-crm-" + S.heuteISO() + ".json", S.exportJSON(), "application/json");
          U.toast("Export erstellt.", "ok");
        });
        var fileInput = root.querySelector("#import-file");
        root.querySelector("#import-json").addEventListener("click", function () { fileInput.click(); });
        fileInput.addEventListener("change", function () {
          var datei = fileInput.files[0];
          if (!datei) return;
          var reader = new FileReader();
          reader.onload = function () {
            try {
              var r = S.importJSON(String(reader.result));
              U.toast(r.objekte + " Objekte, " + r.kontakte + " Kontakte importiert.", "ok");
              global.App.render();
            } catch (err) {
              U.toast("Import fehlgeschlagen: " + err.message, "err");
            }
          };
          reader.readAsText(datei);
        });
        root.querySelector("#demo-laden").addEventListener("click", function () {
          U.frage("Demo-Daten laden?", "Der aktuelle Datenbestand wird durch den Demo-Datensatz ersetzt.", function () {
            S.resetDemo();
            U.toast("Demo-Datensatz geladen.", "ok");
            global.App.render();
          }, "Laden");
        });
        root.querySelector("#alles-loeschen").addEventListener("click", function () {
          U.frage("Wirklich alle Daten löschen?", "Objekte, Kontakte, Aufgaben und Verlauf werden unwiderruflich entfernt.", function () {
            S.clearAll();
            U.toast("Alle Daten gelöscht.", "warn");
            global.App.render();
          });
        });
      }
    };
  }

  /* =====================================================================
     Globale Suche
     ===================================================================== */
  function suche(q) {
    var s = q.toLowerCase();
    var objekteTreffer = S.state.objekte.filter(function (o) {
      return (o.titel + " " + o.strasse + " " + o.ort + " " + o.plz + " " + o.typ + " " +
              (o.tags || []).join(" ")).toLowerCase().indexOf(s) !== -1;
    });
    var kontakteTreffer = S.state.kontakte.filter(function (k) {
      return (S.kontaktName(k) + " " + k.firma + " " + k.email + " " + k.telefon + " " + k.ort)
        .toLowerCase().indexOf(s) !== -1;
    });
    var aufgabenTreffer = S.state.aufgaben.filter(function (t) {
      return (t.titel + " " + t.notiz).toLowerCase().indexOf(s) !== -1;
    });

    var gesamt = objekteTreffer.length + kontakteTreffer.length + aufgabenTreffer.length;

    function block(titel, items, renderer) {
      if (!items.length) return "";
      return '<div class="card"><div class="card-head"><h2>' + U.esc(titel) + "</h2>" +
        '<span class="sub">' + items.length + "</span></div>" +
        '<div class="card-body"><ul class="list-plain">' + items.slice(0, 12).map(renderer).join("") + "</ul></div></div>";
    }

    return {
      html:
        '<div class="page-head"><div><h1>Suche</h1><p>' + gesamt + ' Treffer für „' + U.esc(q) + "“</p></div></div>" +
        (gesamt ? '<div class="stack">' +
          block("Objekte", objekteTreffer, function (o) {
            return '<li><div class="grow"><div class="cell-title">' + objektLink(o) + "</div>" +
              '<div class="cell-sub">' + U.esc(o.ort + " · " + o.typ) + "</div></div>" +
              U.stagePill(o.stage) + '<span class="mono nowrap">' + U.eurKurz(o.kaufpreis) + "</span></li>";
          }) +
          block("Kontakte", kontakteTreffer, function (k) {
            return '<li><span class="avatar">' + U.esc(U.initialen(S.kontaktName(k))) + "</span>" +
              '<div class="grow"><div class="cell-title"><a href="#/kontakt/' + k.id + '">' + U.esc(S.kontaktName(k)) + "</a></div>" +
              '<div class="cell-sub">' + U.esc(k.firma || kontaktTyp(k.typ).label) + "</div></div></li>";
          }) +
          block("Aufgaben", aufgabenTreffer, function (t) {
            var f = U.faelligText(t.faellig);
            return '<li><div class="grow"><div class="cell-title">' + U.esc(t.titel) + "</div>" +
              '<div class="cell-sub ' + f.cls + '">' + U.esc(f.text) + "</div></div></li>";
          }) + "</div>"
          : leer("Keine Treffer", "Für „" + q + "“ wurde nichts gefunden.", "")),
      mount: function () {}
    };
  }

  global.Views = {
    dashboard: dashboard,
    objekte: objekte,
    objektDetail: objektDetail,
    pipeline: pipeline,
    kontakte: kontakte,
    kontaktDetail: kontaktDetail,
    aufgaben: aufgaben,
    berichte: berichte,
    einstellungen: einstellungen,
    suche: suche,
    gefilterteObjekte: gefilterteObjekte
  };
})(window);
