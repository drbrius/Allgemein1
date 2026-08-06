/* Deal CRM — Ansichten */
(function (global) {
  "use strict";

  var S = global.Store, U = global.UI, D = global.CRMData, F = global.Forms;

  /* Filterzustand bleibt zwischen den Renderings erhalten */
  var filter = {
    deals: { q: "", kategorie: "", stage: "", betreuer: "", sort: "updatedAt", dir: -1, nurOffen: false },
    kontakte: { q: "", typ: "" },
    aufgaben: { modus: "offen" },
    protokolle: { q: "", status: "", kanal: "", dealId: "" }
  };

  function leer(titel, text, aktionHtml) {
    return '<div class="empty"><div class="big">' + U.icon("search", 28) + "</div>" +
      "<h3>" + U.esc(titel) + "</h3><p>" + U.esc(text) + "</p>" + (aktionHtml || "") + "</div>";
  }

  function kontaktTyp(id) {
    return D.KONTAKTTYPEN.filter(function (t) { return t.id === id; })[0] ||
      D.KONTAKTTYPEN[D.KONTAKTTYPEN.length - 1];
  }

  function prio(id) {
    return D.PRIORITAETEN.filter(function (p) { return p.id === id; })[0] || D.PRIORITAETEN[2];
  }

  function aufgabenTyp(id) {
    return D.AUFGABENTYPEN.filter(function (a) { return a.id === id; })[0] ||
      D.AUFGABENTYPEN[D.AUFGABENTYPEN.length - 1];
  }

  function kanal(id) {
    return D.KANAELE.filter(function (k) { return k.id === id; })[0] || D.KANAELE[0];
  }

  function dealLink(d) {
    return '<a href="#/deal/' + d.id + '">' + U.esc(d.titel) + "</a>";
  }

  function aktivitaetIcon(typ) {
    return typ === "anruf" ? "phone" : typ === "email" ? "mail" : typ === "termin" ? "calendar" :
      typ === "stage" ? "kanban" : typ === "create" ? "plus" : typ === "protokoll" ? "protokoll" :
      typ === "task" ? "check" : "note";
  }

  function timelineHtml(liste, mitDeal) {
    if (!liste.length) return '<p class="muted" style="font-size:0.87rem">Noch keine Aktivitäten.</p>';
    return '<div class="timeline">' + liste.map(function (a, i) {
      var d = mitDeal && a.dealId ? S.deal(a.dealId) : null;
      return '<div class="tl-item"><div class="tl-rail"><div class="tl-dot">' +
        U.icon(aktivitaetIcon(a.typ), 13) + "</div>" +
        (i < liste.length - 1 ? '<div class="tl-line"></div>' : "") + "</div>" +
        '<div class="tl-body"><div class="txt">' + U.esc(a.text) + "</div>" +
        '<div class="ts">' + U.datumZeit(a.ts) + (d ? " · " + dealLink(d) : "") + "</div></div></div>";
    }).join("") + "</div>";
  }

  /* Kompakte Protokollliste für Deal- und Kontaktdetails */
  function protokollListe(liste) {
    if (!liste.length) return '<p class="muted" style="font-size:0.87rem">Noch kein Protokoll erfasst.</p>';
    return '<ul class="list-plain">' + liste.map(function (p) {
      return '<li><div class="grow"><div class="cell-title">' +
        '<a href="#/protokoll/' + p.id + '">' + U.esc(p.betreff) + "</a></div>" +
        '<div class="cell-sub">' + U.esc(p.nummer) + " · " + U.datum(p.datum + "T12:00:00") +
        " · " + U.esc(kanal(p.kanal).label) + " · " + U.esc(p.verfasser || "") + "</div></div>" +
        U.statusPill(p.status) + "</li>";
    }).join("") + "</ul>";
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

    var topDeals = S.state.deals.filter(S.isOffen)
      .sort(function (a, b) { return S.gewichtet(b) - S.gewichtet(a); })
      .slice(0, 6);

    var letzteProtokolle = S.state.protokolle.slice()
      .sort(function (a, b) { return String(b.datum).localeCompare(String(a.datum)); })
      .slice(0, 5);

    var kpiCards = [
      { label: "Aktive Deals", icon: "flame", value: U.num(k.aktiveDeals),
        foot: U.num(k.neu30Tage) + " neu in 30 Tagen" },
      { label: "Pipeline-Volumen", icon: "euro", value: U.eurKurz(k.volumen),
        foot: "gewichtet " + U.eurKurz(k.forecast) },
      { label: "Erwartete Marge", icon: "chart", value: U.eurKurz(k.marge),
        foot: "gewichtet " + U.eurKurz(k.margeGewichtet) },
      { label: "Abschlussquote", icon: "check", value: U.dez(k.quote) + " %",
        foot: k.gewonnen + " abgeschlossen · " + k.verloren + " verloren" }
    ].map(function (c) {
      return '<div class="card kpi"><div class="label">' + U.icon(c.icon, 15) + U.esc(c.label) + "</div>" +
        '<div class="value">' + c.value + "</div>" +
        '<div class="foot">' + U.esc(c.foot) + "</div></div>";
    }).join("");

    var pipelineBalken = U.balken(stufen.map(function (p) {
      return { label: p.stage.label, wert: p.volumen, farbe: p.stage.color };
    }), U.eurKurz);

    var kategorien = S.proKategorie();
    var kategorieBalken = kategorien.length ? U.balken(kategorien.map(function (r) {
      return { label: r.kategorie.label, wert: r.volumen, farbe: r.kategorie.farbe };
    }), U.eurKurz) : '<p class="muted" style="font-size:0.87rem">Noch keine Deals erfasst.</p>';

    var aufgabenListe = faellige.length ? faellige.map(function (t) {
      var f = U.faelligText(t.faellig);
      var d = t.dealId ? S.deal(t.dealId) : null;
      return '<div class="task-row">' +
        '<input type="checkbox" data-toggle="' + t.id + '" aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(t.titel) + "</div>" +
          '<div class="m"><span class="' + f.cls + '">' + U.esc(f.text) + "</span>" +
          (d ? '<a href="#/deal/' + d.id + '">' + U.esc(d.titel) + "</a>" : "") +
          '<span class="pill ' + prio(t.prioritaet).cls + '">' + prio(t.prioritaet).label + "</span></div>" +
        "</div></div>";
    }).join("") : '<p class="muted" style="font-size:0.87rem;padding:0.6rem 0">Keine offenen Aufgaben für heute. 🎉</p>';

    var deals = topDeals.length ? '<div class="table-wrap"><table class="data compact"><thead><tr>' +
      '<th>Deal</th><th>Kategorie</th><th>Phase</th><th class="num">Volumen</th>' +
      '<th class="num">Marge</th><th class="num">Gewichtet</th>' +
      "</tr></thead><tbody>" + topDeals.map(function (d) {
        return "<tr>" +
          '<td><div class="cell-title">' + dealLink(d) + '</div><div class="cell-sub">' +
            U.esc([d.ort, d.land].filter(Boolean).join(", ")) + "</div></td>" +
          "<td>" + U.kategoriePill(d.kategorie) + "</td>" +
          "<td>" + U.stagePill(d.stage) + "</td>" +
          '<td class="num">' + U.eur(d.volumen) + "</td>" +
          '<td class="num">' + (d.marge ? U.eurKurz(d.marge) : "—") + "</td>" +
          '<td class="num">' + U.eurKurz(S.gewichtet(d)) + "</td>" +
          "</tr>";
      }).join("") + "</tbody></table></div>"
      : leer("Noch keine aktiven Deals", "Lege deinen ersten Deal an, um die Pipeline zu füllen.",
             '<button class="btn btn-primary" data-neu="deal">Deal anlegen</button>');

    var protokolleHtml = letzteProtokolle.length
      ? protokollListe(letzteProtokolle)
      : '<p class="muted" style="font-size:0.87rem">Noch keine Protokolle. ' +
        'Nach jedem Gespräch eines anlegen — die Maßnahmen werden automatisch zu Aufgaben.</p>';

    return {
      html:
        '<div class="page-head"><div><h1>Übersicht</h1>' +
          "<p>Guten Tag, " + U.esc(S.state.einstellungen.nutzer.split(" ")[0]) + " — " +
          k.aufgabenUeberfaellig + " überfällige, " + k.aufgabenHeute + " heutige Aufgaben" +
          (k.protokolleEntwurf ? ", " + k.protokolleEntwurf + " Protokoll-Entwürfe" : "") + ".</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-neu="protokoll">' + U.icon("protokoll", 15) + " Protokoll</button>" +
            '<button class="btn" data-neu="aufgabe">' + U.icon("plus", 15) + " Aufgabe</button>" +
            '<button class="btn btn-primary" data-neu="deal">' + U.icon("plus", 15) + " Neuer Deal</button>" +
          "</div></div>" +
        '<div class="stack">' +
          '<div class="grid grid-kpi">' + kpiCards + "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Pipeline nach Phase</h2>' +
              '<span class="sub">' + U.eurKurz(k.volumen) + " offen</span>" +
              '<div class="actions"><a class="btn btn-sm" href="#/pipeline">Kanban öffnen</a></div></div>' +
              '<div class="card-body">' + pipelineBalken + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Volumen nach Anlageklasse</h2>' +
              '<div class="actions"><a class="btn btn-sm" href="#/berichte">Auswertungen</a></div></div>' +
              '<div class="card-body">' + kategorieBalken + "</div></div>" +
          "</div>" +
          '<div class="card"><div class="card-head"><h2>Top-Deals nach gewichtetem Volumen</h2>' +
            '<div class="actions"><a class="btn btn-sm" href="#/deals">Alle Deals</a></div></div>' + deals + "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Heute zu erledigen</h2>' +
              '<div class="actions"><a class="btn btn-sm" href="#/aufgaben">Alle Aufgaben</a></div></div>' +
              '<div class="card-body" style="padding:0 1rem">' + aufgabenListe + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Letzte Protokolle</h2>' +
              '<div class="actions"><a class="btn btn-sm" href="#/protokolle">Alle Protokolle</a></div></div>' +
              '<div class="card-body">' + protokolleHtml + "</div></div>" +
          "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Letzte Aktivitäten</h2></div>' +
              '<div class="card-body">' + timelineHtml(S.state.aktivitaeten.slice(0, 7), true) + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Neue Deals je Monat</h2>' +
              '<span class="sub">letzte 6 Monate</span></div>' +
              '<div class="card-body">' + U.saeulen(S.neuProMonat(6).map(function (m) {
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
     Deals (Liste)
     ===================================================================== */
  function gefilterteDeals() {
    var f = filter.deals;
    var q = f.q.toLowerCase();
    var liste = S.state.deals.filter(function (d) {
      if (f.kategorie && d.kategorie !== f.kategorie) return false;
      if (f.stage && d.stage !== f.stage) return false;
      if (f.betreuer && d.betreuer !== f.betreuer) return false;
      if (f.nurOffen && !S.isOffen(d)) return false;
      if (!q) return true;
      var kt = d.kontaktId ? S.kontaktName(S.kontakt(d.kontaktId)) : "";
      var details = Object.keys(d.details || {}).map(function (x) { return d.details[x]; }).join(" ");
      return (d.titel + " " + d.ort + " " + d.land + " " + S.kategorie(d.kategorie).label + " " +
              (d.tags || []).join(" ") + " " + kt + " " + d.notizen + " " + details)
        .toLowerCase().indexOf(q) !== -1;
    });

    var key = f.sort;
    liste.sort(function (a, b) {
      var va, vb;
      if (key === "faktor") { va = S.faktor(a); vb = S.faktor(b); }
      else if (key === "margeProzent") { va = S.margeProzent(a); vb = S.margeProzent(b); }
      else if (key === "stage") {
        va = D.STAGES.findIndex(function (s) { return s.id === a.stage; });
        vb = D.STAGES.findIndex(function (s) { return s.id === b.stage; });
      } else if (key === "kategorie") {
        va = S.kategorie(a.kategorie).label; vb = S.kategorie(b.kategorie).label;
      } else { va = a[key]; vb = b[key]; }
      if (typeof va === "string" || typeof vb === "string") {
        return String(va || "").localeCompare(String(vb || ""), "de") * f.dir;
      }
      return ((va || 0) - (vb || 0)) * f.dir;
    });
    return liste;
  }

  function deals() {
    var f = filter.deals;
    var liste = gefilterteDeals();

    function th(key, label, klasse) {
      var aktiv = f.sort === key;
      return '<th class="sortable ' + (klasse || "") + (aktiv ? " sorted" : "") + '" data-sort="' + key + '">' +
        U.esc(label) + ' <span class="arrow">' + (aktiv ? (f.dir === 1 ? "▲" : "▼") : "↕") + "</span></th>";
    }

    var zeilen = liste.map(function (d) {
      var kt = d.kontaktId ? S.kontakt(d.kontaktId) : null;
      return '<tr data-open="' + d.id + '">' +
        '<td><div class="cell-title">' + U.esc(d.titel) + "</div>" +
          '<div class="cell-sub">' + U.esc([d.ort, d.land].filter(Boolean).join(", ")) + "</div></td>" +
        "<td>" + U.kategoriePill(d.kategorie) + "</td>" +
        "<td>" + U.stagePill(d.stage) + "</td>" +
        '<td class="num">' + U.eur(d.volumen) +
          '<div class="cell-sub">' + (d.menge ? U.menge(d.menge, d.einheit) : "—") + "</div></td>" +
        '<td class="num">' + (d.marge ? U.eurKurz(d.marge) : "—") +
          '<div class="cell-sub">' + (S.margeProzent(d) ? U.dez(S.margeProzent(d)) + " %" : "—") + "</div></td>" +
        '<td class="num">' + (S.faktor(d) ? U.dez(S.faktor(d)) : "—") +
          '<div class="cell-sub">' + (S.rendite(d) ? U.dez(S.rendite(d)) + " %" : "—") + "</div></td>" +
        "<td>" + (kt ? '<a href="#/kontakt/' + kt.id + '">' + U.esc(S.kontaktName(kt)) + "</a>" : '<span class="faint">—</span>') + "</td>" +
        '<td class="nowrap muted">' + U.relativ(d.updatedAt) + "</td>" +
        '<td><div class="row-actions">' +
          '<button class="btn btn-sm btn-icon" data-edit="' + d.id + '" title="Bearbeiten">' + U.icon("edit", 15) + "</button>" +
          '<button class="btn btn-sm btn-icon btn-danger" data-del="' + d.id + '" title="Löschen">' + U.icon("trash", 15) + "</button>" +
        "</div></td></tr>";
    }).join("");

    var summe = liste.reduce(function (s, d) { return s + (d.volumen || 0); }, 0);
    var margeSumme = liste.reduce(function (s, d) { return s + (d.marge || 0); }, 0);

    var tabelle = liste.length
      ? '<div class="table-wrap"><table class="data"><thead><tr>' +
          th("titel", "Deal") + th("kategorie", "Kategorie") + th("stage", "Phase") +
          th("volumen", "Volumen · Menge", "num") + th("marge", "Marge", "num") +
          th("faktor", "Faktor · Rendite", "num") +
          "<th>Gegenpartei</th>" + th("updatedAt", "Geändert") + "<th></th>" +
        "</tr></thead><tbody>" + zeilen + "</tbody></table></div>"
      : leer("Keine Deals gefunden", "Passe die Filter an oder lege einen neuen Deal an.",
             '<button class="btn btn-primary" data-neu="deal">Deal anlegen</button>');

    return {
      html:
        '<div class="page-head"><div><h1>Deals</h1>' +
          "<p>" + U.num(liste.length) + " von " + U.num(S.state.deals.length) +
          " Deals · Volumen " + U.eurKurz(summe) + " · Marge " + U.eurKurz(margeSumme) + "</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-csv="deals">' + U.icon("download", 15) + " CSV</button>" +
            '<button class="btn btn-primary" data-neu="deal">' + U.icon("plus", 15) + " Neuer Deal</button>" +
          "</div></div>" +
        '<div class="card"><div class="toolbar">' +
          '<div class="grow"><input type="search" id="f-q" placeholder="Suchen nach Titel, Ort, Produkt, Tag …" value="' + U.esc(f.q) + '"></div>' +
          U.select("f-kategorie", f.kategorie, D.KATEGORIEN.map(function (k) {
            return { value: k.id, label: k.label };
          }), "Alle Kategorien") +
          U.select("f-stage", f.stage, D.STAGES.map(function (s) { return { value: s.id, label: s.label }; }), "Alle Phasen") +
          U.select("f-betreuer", f.betreuer, D.TEAM_NAMEN, "Ganzes Team") +
          '<label class="check"><input type="checkbox" id="f-offen"' + (f.nurOffen ? " checked" : "") + "> nur offene</label>" +
          (f.q || f.kategorie || f.stage || f.betreuer || f.nurOffen
            ? '<button class="btn btn-sm btn-ghost" id="f-reset">Filter zurücksetzen</button>' : "") +
        "</div>" + tabelle + "</div>",
      mount: function (root) {
        var q = root.querySelector("#f-q");
        q.addEventListener("input", function () {
          filter.deals.q = q.value;
          global.App.render({ fokus: "#f-q" });
        });
        [["f-kategorie", "kategorie"], ["f-stage", "stage"], ["f-betreuer", "betreuer"]].forEach(function (paar) {
          root.querySelector('[name="' + paar[0] + '"]').addEventListener("change", function (e) {
            filter.deals[paar[1]] = e.target.value;
            global.App.render();
          });
        });
        root.querySelector("#f-offen").addEventListener("change", function (e) {
          filter.deals.nurOffen = e.target.checked; global.App.render();
        });
        var reset = root.querySelector("#f-reset");
        if (reset) reset.addEventListener("click", function () {
          filter.deals = { q: "", kategorie: "", stage: "", betreuer: "", sort: "updatedAt", dir: -1, nurOffen: false };
          global.App.render();
        });
        root.querySelectorAll("th.sortable").forEach(function (el) {
          el.addEventListener("click", function () {
            var key = el.getAttribute("data-sort");
            if (filter.deals.sort === key) filter.deals.dir *= -1;
            else { filter.deals.sort = key; filter.deals.dir = key === "titel" || key === "kategorie" ? 1 : -1; }
            global.App.render();
          });
        });
        root.querySelectorAll("tr[data-open]").forEach(function (tr) {
          tr.addEventListener("click", function (e) {
            if (e.target.closest("button") || e.target.closest("a")) return;
            location.hash = "#/deal/" + tr.getAttribute("data-open");
          });
        });
        root.querySelectorAll("[data-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.deal(b.getAttribute("data-edit")); });
        });
        root.querySelectorAll("[data-del]").forEach(function (b) {
          b.addEventListener("click", function () { loescheDeal(b.getAttribute("data-del")); });
        });
      }
    };
  }

  function loescheDeal(id, danach) {
    var d = S.deal(id);
    if (!d) return;
    U.frage("Deal löschen?", "„" + d.titel + "“ wird aus dem CRM entfernt.", function () {
      var snapshot = S.deleteDeal(id);
      U.toast("Deal gelöscht.", "warn", {
        label: "Rückgängig",
        run: function () { S.restoreDeal(snapshot); U.toast("Wiederhergestellt.", "ok"); }
      });
      if (danach) danach();
    });
  }

  /* =====================================================================
     Deal-Detail
     ===================================================================== */
  function dealDetail(id) {
    var d = S.deal(id);
    if (!d) {
      return { html: leer("Deal nicht gefunden", "Der Eintrag wurde möglicherweise gelöscht.",
        '<a class="btn btn-primary" href="#/deals">Zur Deal-Liste</a>'), mount: function () {} };
    }
    var kat = S.kategorie(d.kategorie);
    var kt = d.kontaktId ? S.kontakt(d.kontaktId) : null;
    var aufgaben = S.aufgabenFuer(d.id, null).sort(function (a, b) {
      return (a.erledigt - b.erledigt) || String(a.faellig).localeCompare(String(b.faellig));
    });
    var protokolle = S.protokolleFuer(d.id, null);

    var basisFakten = [
      [kat.volumenLabel.replace(" (€)", ""), U.eur(d.volumen)],
      [kat.mengeLabel, d.menge ? U.menge(d.menge, d.einheit) : "—"],
      ["Preis je " + (d.einheit || "Einheit"), S.preisProEinheit(d) ? U.eur(S.preisProEinheit(d)) : "—"],
      ["Erwartete Marge", d.marge ? U.eur(d.marge) + " (" + U.dez(S.margeProzent(d)) + " %)" : "—"],
      ["Gewichtetes Volumen", U.eur(S.gewichtet(d))],
      ["Gewichtete Marge", d.marge ? U.eur(S.gewichteteMarge(d)) : "—"]
    ];
    if (kat.ertragLabel && d.ertragJahr) {
      basisFakten.push([kat.ertragLabel.replace(" (€)", ""), U.eur(d.ertragJahr)]);
      basisFakten.push(["Faktor", U.dez(S.faktor(d))]);
      basisFakten.push(["Rendite", U.dez(S.rendite(d)) + " %"]);
    }
    basisFakten.push(["Quelle", d.quelle || "—"]);

    var faktenHtml = basisFakten.map(function (f) {
      return '<div class="fact"><div class="k">' + U.esc(f[0]) + '</div><div class="v">' + f[1] + "</div></div>";
    }).join("");

    var fachFelder = kat.felder.filter(function (f) {
      var w = d.details ? d.details[f.k] : undefined;
      return w !== undefined && w !== "" && w !== null;
    });
    var fachHtml = fachFelder.length
      ? '<div class="facts">' + fachFelder.map(function (f) {
          var w = d.details[f.k];
          if (f.typ === "number" && (f.k === "umsatz")) w = U.eur(w);
          else if (f.typ === "number") w = U.num(w);
          return '<div class="fact"><div class="k">' + U.esc(f.label) + '</div><div class="v">' + U.esc(w) + "</div></div>";
        }).join("") + "</div>"
      : '<p class="muted" style="font-size:0.87rem">Keine kategoriespezifischen Angaben erfasst.</p>';

    var stageBar = '<div class="stage-bar">' + D.STAGES.map(function (s) {
      var on = s.id === d.stage;
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
          '<span class="tag">' + aufgabenTyp(t.typ).label + "</span>" +
          (t.notiz ? '<span class="faint">' + U.esc(t.notiz) + "</span>" : "") + "</div></div>" +
        '<button class="btn btn-sm btn-icon btn-ghost" data-task-edit="' + t.id + '">' + U.icon("edit", 14) + "</button>" +
        "</div>";
    }).join("") : '<p class="muted" style="font-size:0.87rem">Keine Aufgaben zu diesem Deal.</p>';

    var kontaktKarte = kt
      ? '<div class="row" style="gap:0.6rem"><span class="avatar">' + U.esc(U.initialen(S.kontaktName(kt))) + "</span>" +
        '<div><div class="cell-title"><a href="#/kontakt/' + kt.id + '">' + U.esc(S.kontaktName(kt)) + "</a></div>" +
        '<div class="cell-sub">' + U.esc(kt.firma || kontaktTyp(kt.typ).label) + "</div></div></div>" +
        '<div class="divider"></div>' +
        (kt.telefon ? '<div class="row" style="font-size:0.86rem">' + U.icon("phone", 14) +
          '<a href="tel:' + U.esc(kt.telefon.replace(/\s/g, "")) + '">' + U.esc(kt.telefon) + "</a></div>" : "") +
        (kt.email ? '<div class="row" style="font-size:0.86rem;margin-top:0.35rem">' + U.icon("mail", 14) +
          '<a href="mailto:' + U.esc(kt.email) + '">' + U.esc(kt.email) + "</a></div>" : "") +
        (kt.ort ? '<div class="row" style="font-size:0.86rem;margin-top:0.35rem">' + U.icon("pin", 14) +
          U.esc([kt.ort, kt.land].filter(Boolean).join(", ")) + "</div>" : "")
      : '<p class="muted" style="font-size:0.87rem">Keine Gegenpartei verknüpft. ' +
        '<button class="btn btn-sm" data-edit-deal="1">Jetzt zuordnen</button></p>';

    return {
      html:
        '<div class="breadcrumb"><a href="#/deals">Deals</a> › ' + U.esc(d.titel) + "</div>" +
        '<div class="page-head"><div>' +
          "<h1>" + U.esc(d.titel) + "</h1>" +
          '<p>' + U.kategoriePill(d.kategorie, true) + " " +
          U.icon("pin", 14) + " " + U.esc([d.ort, d.land].filter(Boolean).join(", ")) +
          " · Betreuer " + U.esc(d.betreuer || "—") + "</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-neu-protokoll="1">' + U.icon("protokoll", 15) + " Protokoll</button>" +
            '<button class="btn" data-neu-aktivitaet="1">' + U.icon("note", 15) + " Aktivität</button>" +
            '<button class="btn" data-neu-aufgabe="1">' + U.icon("check", 15) + " Aufgabe</button>" +
            '<button class="btn" data-edit-deal="1">' + U.icon("edit", 15) + " Bearbeiten</button>" +
            '<button class="btn btn-danger btn-icon" data-del-deal="1" title="Löschen">' + U.icon("trash", 15) + "</button>" +
          "</div></div>" +
        '<div class="detail-grid">' +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Phase</h2>' +
              '<span class="sub">Wahrscheinlichkeit ' + U.num(d.wahrscheinlichkeit) + " %</span></div>" +
              '<div class="card-body">' + stageBar + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Kennzahlen</h2></div>' +
              '<div class="card-body"><div class="facts">' + faktenHtml + "</div></div></div>" +
            '<div class="card"><div class="card-head"><h2>' + U.esc(kat.label) + " — Fachdaten</h2>" +
              '<div class="actions"><button class="btn btn-sm" data-edit-deal="1">Bearbeiten</button></div></div>' +
              '<div class="card-body">' + fachHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Notizen</h2></div>' +
              '<div class="card-body"><p style="font-size:0.9rem;white-space:pre-wrap">' +
              (d.notizen ? U.esc(d.notizen) : '<span class="muted">Keine Notizen hinterlegt.</span>') + "</p></div></div>" +
            '<div class="card"><div class="card-head"><h2>Protokolle</h2>' +
              '<span class="sub">' + protokolle.length + "</span>" +
              '<div class="actions"><button class="btn btn-sm" data-neu-protokoll="1">' +
                U.icon("plus", 14) + " Protokoll</button></div></div>" +
              '<div class="card-body">' + protokollListe(protokolle) + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Aufgaben</h2>' +
              '<div class="actions"><button class="btn btn-sm" data-neu-aufgabe="1">' + U.icon("plus", 14) + " Aufgabe</button></div></div>" +
              '<div class="card-body" style="padding:0 1rem">' + aufgabenHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Verlauf</h2>' +
              '<div class="actions"><button class="btn btn-sm" data-neu-aktivitaet="1">' + U.icon("plus", 14) + " Eintrag</button></div></div>" +
              '<div class="card-body">' + timelineHtml(S.aktivitaetenFuer({ dealId: d.id }), false) + "</div></div>" +
          "</div>" +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Gegenpartei</h2></div>' +
              '<div class="card-body">' + kontaktKarte + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Merkmale</h2></div>' +
              '<div class="card-body"><div class="row">' +
                (d.tags && d.tags.length
                  ? d.tags.map(function (t) { return '<span class="tag">' + U.esc(t) + "</span>"; }).join("")
                  : '<span class="muted" style="font-size:0.86rem">Keine Schlagwörter</span>') +
              "</div>" +
              '<div class="divider"></div>' +
              '<div style="font-size:0.82rem" class="muted">Angelegt ' + U.datum(d.createdAt) +
              "<br>Zuletzt geändert " + U.datum(d.updatedAt) + " (" + U.relativ(d.updatedAt) + ")</div>" +
              "</div></div>" +
          "</div>" +
        "</div>",
      mount: function (root) {
        root.querySelectorAll("[data-stage]").forEach(function (b) {
          b.addEventListener("click", function () {
            S.setStage(d.id, b.getAttribute("data-stage"));
            U.toast("Phase aktualisiert.", "ok");
          });
        });
        root.querySelectorAll("[data-edit-deal]").forEach(function (b) {
          b.addEventListener("click", function () { F.deal(d.id); });
        });
        root.querySelectorAll("[data-neu-aufgabe]").forEach(function (b) {
          b.addEventListener("click", function () {
            F.aufgabe(null, { dealId: d.id, kontaktId: d.kontaktId || "" });
          });
        });
        root.querySelectorAll("[data-neu-protokoll]").forEach(function (b) {
          b.addEventListener("click", function () {
            F.protokoll(null, { dealId: d.id, kontaktId: d.kontaktId || "" }, function (p) {
              location.hash = "#/protokoll/" + p.id;
            });
          });
        });
        root.querySelectorAll("[data-neu-aktivitaet]").forEach(function (b) {
          b.addEventListener("click", function () { F.notiz(d.id, d.kontaktId || ""); });
        });
        root.querySelectorAll("[data-task-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.aufgabe(b.getAttribute("data-task-edit")); });
        });
        root.querySelectorAll("[data-toggle]").forEach(function (cb) {
          cb.addEventListener("change", function () { S.toggleAufgabe(cb.getAttribute("data-toggle")); });
        });
        var del = root.querySelector("[data-del-deal]");
        if (del) del.addEventListener("click", function () {
          loescheDeal(d.id, function () { location.hash = "#/deals"; });
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
      var karten = p.deals
        .sort(function (a, b) { return b.volumen - a.volumen; })
        .map(function (d) {
          var kat = S.kategorie(d.kategorie);
          return '<article class="kcard" draggable="true" data-id="' + d.id + '">' +
            '<div class="row" style="gap:0.35rem;flex-wrap:nowrap;color:' + kat.farbe + '">' +
              U.icon(kat.icon, 13) + '<span style="font-size:0.72rem;font-weight:650">' + U.esc(kat.label) + "</span></div>" +
            '<div class="t">' + U.esc(d.titel) + "</div>" +
            '<div class="a">' + U.esc([d.ort, d.land].filter(Boolean).join(", ")) + "</div>" +
            '<div class="meta"><span class="price">' + U.eurKurz(d.volumen) + "</span>" +
              (d.marge ? '<span class="tag">+' + U.eurKurz(d.marge) + "</span>" : "") +
              (d.menge ? '<span class="tag">' + U.esc(U.menge(d.menge, d.einheit)) + "</span>" : "") +
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
          " Volumen · gewichtete Marge " + U.eurKurz(k.margeGewichtet) + "</p></div>" +
          '<div class="actions"><button class="btn btn-primary" data-neu="deal">' +
            U.icon("plus", 15) + " Neuer Deal</button></div></div>" +
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
            location.hash = "#/deal/" + card.getAttribute("data-id");
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
            var d = S.deal(id);
            if (!d || d.stage === neueStage) return;
            S.setStage(id, neueStage);
            U.toast("„" + d.titel + "“ → " + S.stage(neueStage).label, "ok");
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
      return (S.kontaktName(k) + " " + k.firma + " " + k.email + " " + k.telefon + " " +
              k.ort + " " + (k.land || "") + " " + (k.tags || []).join(" "))
        .toLowerCase().indexOf(q) !== -1;
    }).sort(function (a, b) { return S.kontaktName(a).localeCompare(S.kontaktName(b), "de"); });

    var zeilen = liste.map(function (k) {
      var dealsDesKontakts = S.state.deals.filter(function (d) { return d.kontaktId === k.id; });
      var volumen = dealsDesKontakts.reduce(function (s, d) { return s + (d.volumen || 0); }, 0);
      var t = kontaktTyp(k.typ);
      return '<tr data-open="' + k.id + '">' +
        '<td><div class="row" style="gap:0.55rem;flex-wrap:nowrap">' +
          '<span class="avatar">' + U.esc(U.initialen(S.kontaktName(k))) + "</span>" +
          '<div><div class="cell-title">' + U.esc(S.kontaktName(k)) + "</div>" +
          '<div class="cell-sub">' + U.esc(k.firma || "—") + "</div></div></div></td>" +
        '<td><span class="pill ' + t.cls + '">' + U.esc(t.label) + "</span></td>" +
        "<td>" + (k.telefon ? '<a href="tel:' + U.esc(k.telefon.replace(/\s/g, "")) + '">' + U.esc(k.telefon) + "</a>" : '<span class="faint">—</span>') +
          '<div class="cell-sub">' + (k.email ? '<a href="mailto:' + U.esc(k.email) + '">' + U.esc(k.email) + "</a>" : "—") + "</div></td>" +
        "<td>" + U.esc(k.ort || "—") + '<div class="cell-sub">' + U.esc(k.land || "") + "</div></td>" +
        '<td class="num">' + dealsDesKontakts.length + "</td>" +
        '<td class="num">' + (volumen ? U.eurKurz(volumen) : "—") + "</td>" +
        '<td class="num">' + S.protokolleFuer(null, k.id).length + "</td>" +
        '<td><div class="row-actions">' +
          '<button class="btn btn-sm btn-icon" data-edit="' + k.id + '" title="Bearbeiten">' + U.icon("edit", 15) + "</button>" +
          '<button class="btn btn-sm btn-icon btn-danger" data-del="' + k.id + '" title="Löschen">' + U.icon("trash", 15) + "</button>" +
        "</div></td></tr>";
    }).join("");

    var tabelle = liste.length
      ? '<div class="table-wrap"><table class="data"><thead><tr>' +
        "<th>Name</th><th>Rolle</th><th>Kontakt</th><th>Standort</th>" +
        '<th class="num">Deals</th><th class="num">Volumen</th><th class="num">Protokolle</th><th></th>' +
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
    U.frage("Kontakt löschen?", S.kontaktName(k) + " wird entfernt. Verknüpfte Deals bleiben erhalten.", function () {
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
    var dealListe = S.state.deals.filter(function (d) { return d.kontaktId === k.id; });
    var volumen = dealListe.reduce(function (s, d) { return s + (d.volumen || 0); }, 0);
    var aufgaben = S.aufgabenFuer(null, k.id);
    var protokolle = S.protokolleFuer(null, k.id);

    var dealsHtml = dealListe.length
      ? '<ul class="list-plain">' + dealListe.map(function (d) {
          return '<li><div class="grow"><div class="cell-title">' + dealLink(d) + "</div>" +
            '<div class="cell-sub">' + U.esc(S.kategorie(d.kategorie).label + " · " + (d.ort || "")) + "</div></div>" +
            U.stagePill(d.stage) + '<span class="mono nowrap">' + U.eurKurz(d.volumen) + "</span></li>";
        }).join("") + "</ul>"
      : '<p class="muted" style="font-size:0.87rem">Keine Deals verknüpft.</p>';

    var aufgabenHtml = aufgaben.length ? aufgaben.map(function (a) {
      var f = U.faelligText(a.faellig);
      return '<div class="task-row' + (a.erledigt ? " done" : "") + '">' +
        '<input type="checkbox" data-toggle="' + a.id + '"' + (a.erledigt ? " checked" : "") + ' aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(a.titel) + "</div>" +
        '<div class="m"><span class="' + (a.erledigt ? "faint" : f.cls) + '">' +
        (a.erledigt ? "erledigt" : U.esc(f.text)) + "</span></div></div></div>";
    }).join("") : '<p class="muted" style="font-size:0.87rem">Keine Aufgaben.</p>';

    return {
      html:
        '<div class="breadcrumb"><a href="#/kontakte">Kontakte</a> › ' + U.esc(S.kontaktName(k)) + "</div>" +
        '<div class="page-head"><div class="row" style="gap:0.8rem;flex-wrap:nowrap">' +
          '<span class="avatar" style="width:44px;height:44px;font-size:1rem">' + U.esc(U.initialen(S.kontaktName(k))) + "</span>" +
          "<div><h1>" + U.esc(S.kontaktName(k)) + "</h1>" +
          '<p><span class="pill ' + t.cls + '">' + U.esc(t.label) + "</span> " +
          U.esc([k.firma, k.ort, k.land].filter(Boolean).join(" · ")) + "</p></div></div>" +
          '<div class="actions">' +
            '<button class="btn" data-neu-protokoll="1">' + U.icon("protokoll", 15) + " Protokoll</button>" +
            '<button class="btn" data-neu-aktivitaet="1">' + U.icon("note", 15) + " Aktivität</button>" +
            '<button class="btn" data-neu-aufgabe="1">' + U.icon("check", 15) + " Aufgabe</button>" +
            '<button class="btn" data-edit-kontakt="1">' + U.icon("edit", 15) + " Bearbeiten</button>" +
            '<button class="btn btn-danger btn-icon" data-del-kontakt="1" title="Löschen">' + U.icon("trash", 15) + "</button>" +
          "</div></div>" +
        '<div class="detail-grid">' +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Verknüpfte Deals</h2>' +
              '<span class="sub">' + dealListe.length + " · " + U.eurKurz(volumen) + "</span></div>" +
              '<div class="card-body">' + dealsHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Protokolle</h2>' +
              '<span class="sub">' + protokolle.length + "</span>" +
              '<div class="actions"><button class="btn btn-sm" data-neu-protokoll="1">' +
                U.icon("plus", 14) + " Protokoll</button></div></div>" +
              '<div class="card-body">' + protokollListe(protokolle) + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Notizen</h2></div>' +
              '<div class="card-body"><p style="font-size:0.9rem;white-space:pre-wrap">' +
              (k.notizen ? U.esc(k.notizen) : '<span class="muted">Keine Notizen hinterlegt.</span>') + "</p></div></div>" +
            '<div class="card"><div class="card-head"><h2>Aufgaben</h2></div>' +
              '<div class="card-body" style="padding:0 1rem">' + aufgabenHtml + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Verlauf</h2></div>' +
              '<div class="card-body">' + timelineHtml(S.aktivitaetenFuer({ kontaktId: k.id }), true) + "</div></div>" +
          "</div>" +
          '<div class="stack">' +
            '<div class="card"><div class="card-head"><h2>Kontaktdaten</h2></div><div class="card-body">' +
              '<ul class="list-plain" style="font-size:0.87rem">' +
                (k.telefon ? "<li>" + U.icon("phone", 15) + '<a class="grow" href="tel:' + U.esc(k.telefon.replace(/\s/g, "")) + '">' + U.esc(k.telefon) + "</a></li>" : "") +
                (k.email ? "<li>" + U.icon("mail", 15) + '<a class="grow" href="mailto:' + U.esc(k.email) + '">' + U.esc(k.email) + "</a></li>" : "") +
                ((k.strasse || k.ort) ? "<li>" + U.icon("pin", 15) + '<span class="grow">' +
                  U.esc([k.strasse, (k.plz + " " + k.ort).trim(), k.land].filter(Boolean).join(", ")) + "</span></li>" : "") +
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
        root.querySelectorAll("[data-neu-protokoll]").forEach(function (b) {
          b.addEventListener("click", function () {
            F.protokoll(null, { kontaktId: k.id, dealId: (dealListe[0] || {}).id || "" }, function (p) {
              location.hash = "#/protokoll/" + p.id;
            });
          });
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
     Protokolle (Liste)
     ===================================================================== */
  function gefilterteProtokolle() {
    var f = filter.protokolle;
    var q = f.q.toLowerCase();
    return S.state.protokolle.filter(function (p) {
      if (f.status && p.status !== f.status) return false;
      if (f.kanal && p.kanal !== f.kanal) return false;
      if (f.dealId && p.dealId !== f.dealId) return false;
      if (!q) return true;
      return (p.nummer + " " + p.betreff + " " + p.teilnehmer + " " + p.themen + " " +
              p.ergebnisse + " " + (p.offenePunkte || "") + " " + (p.verfasser || ""))
        .toLowerCase().indexOf(q) !== -1;
    }).sort(function (a, b) {
      return String(b.datum + b.uhrzeit).localeCompare(String(a.datum + a.uhrzeit));
    });
  }

  function protokolle() {
    var f = filter.protokolle;
    var liste = gefilterteProtokolle();

    var zeilen = liste.map(function (p) {
      var d = p.dealId ? S.deal(p.dealId) : null;
      var k = p.kontaktId ? S.kontakt(p.kontaktId) : null;
      var offeneSchritte = (p.naechsteSchritte || []).length;
      return '<tr data-open="' + p.id + '">' +
        '<td class="nowrap mono">' + U.esc(p.nummer) + "</td>" +
        '<td><div class="cell-title">' + U.esc(p.betreff) +
          (p.vertraulich ? ' <span class="pill pill-red">vertraulich</span>' : "") + "</div>" +
          '<div class="cell-sub">' + U.esc(p.teilnehmer || "") + "</div></td>" +
        "<td>" + (d ? '<a href="#/deal/' + d.id + '">' + U.esc(d.titel) + "</a>" :
          (k ? '<a href="#/kontakt/' + k.id + '">' + U.esc(S.kontaktName(k)) + "</a>" : '<span class="faint">intern</span>')) + "</td>" +
        '<td class="nowrap">' + U.icon(kanal(p.kanal).icon, 14) + " " + U.esc(kanal(p.kanal).label) + "</td>" +
        '<td class="nowrap">' + U.datum(p.datum + "T12:00:00") +
          '<div class="cell-sub">' + U.esc(p.uhrzeit || "") + (p.dauer ? " · " + p.dauer + " Min." : "") + "</div></td>" +
        "<td>" + U.esc(p.verfasser || "—") + "</td>" +
        '<td class="num">' + (offeneSchritte || "—") + "</td>" +
        "<td>" + U.statusPill(p.status) + "</td>" +
        '<td><div class="row-actions">' +
          '<button class="btn btn-sm btn-icon" data-edit="' + p.id + '" title="Bearbeiten">' + U.icon("edit", 15) + "</button>" +
          '<button class="btn btn-sm btn-icon btn-danger" data-del="' + p.id + '" title="Löschen">' + U.icon("trash", 15) + "</button>" +
        "</div></td></tr>";
    }).join("");

    var tabelle = liste.length
      ? '<div class="table-wrap"><table class="data"><thead><tr>' +
        "<th>Nummer</th><th>Betreff</th><th>Bezug</th><th>Art</th><th>Datum</th>" +
        '<th>Protokollführung</th><th class="num">Maßnahmen</th><th>Status</th><th></th>' +
        "</tr></thead><tbody>" + zeilen + "</tbody></table></div>"
      : leer("Keine Protokolle gefunden",
             "Halte Gespräche direkt nach dem Termin fest — Maßnahmen werden auf Wunsch zu Aufgaben.",
             '<button class="btn btn-primary" data-neu="protokoll">Protokoll anlegen</button>');

    return {
      html:
        '<div class="page-head"><div><h1>Protokolle</h1>' +
          "<p>" + U.num(liste.length) + " von " + U.num(S.state.protokolle.length) +
          " Gesprächsprotokollen · nächste Nummer " + U.esc(S.naechsteNummer()) + "</p></div>" +
          '<div class="actions">' +
            '<button class="btn" data-csv="protokolle">' + U.icon("download", 15) + " CSV</button>" +
            '<button class="btn btn-primary" data-neu="protokoll">' + U.icon("plus", 15) + " Neues Protokoll</button>" +
          "</div></div>" +
        '<div class="card"><div class="toolbar">' +
          '<div class="grow"><input type="search" id="p-q" placeholder="Betreff, Teilnehmer, Inhalt …" value="' + U.esc(f.q) + '"></div>' +
          U.select("p-status", f.status, D.PROTOKOLL_STATUS.map(function (s) {
            return { value: s.id, label: s.label };
          }), "Alle Status") +
          U.select("p-kanal", f.kanal, D.KANAELE.map(function (x) {
            return { value: x.id, label: x.label };
          }), "Alle Gesprächsarten") +
          U.select("p-deal", f.dealId, S.state.deals.map(function (d) {
            return { value: d.id, label: d.titel };
          }), "Alle Deals") +
        "</div>" + tabelle + "</div>",
      mount: function (root) {
        var q = root.querySelector("#p-q");
        q.addEventListener("input", function () {
          filter.protokolle.q = q.value;
          global.App.render({ fokus: "#p-q" });
        });
        [["p-status", "status"], ["p-kanal", "kanal"], ["p-deal", "dealId"]].forEach(function (paar) {
          root.querySelector('[name="' + paar[0] + '"]').addEventListener("change", function (e) {
            filter.protokolle[paar[1]] = e.target.value;
            global.App.render();
          });
        });
        root.querySelectorAll("tr[data-open]").forEach(function (tr) {
          tr.addEventListener("click", function (e) {
            if (e.target.closest("button") || e.target.closest("a")) return;
            location.hash = "#/protokoll/" + tr.getAttribute("data-open");
          });
        });
        root.querySelectorAll("[data-edit]").forEach(function (b) {
          b.addEventListener("click", function () { F.protokoll(b.getAttribute("data-edit")); });
        });
        root.querySelectorAll("[data-del]").forEach(function (b) {
          b.addEventListener("click", function () { loescheProtokoll(b.getAttribute("data-del")); });
        });
      }
    };
  }

  function loescheProtokoll(id, danach) {
    var p = S.protokoll(id);
    if (!p) return;
    U.frage("Protokoll löschen?", p.nummer + " „" + p.betreff + "“ wird entfernt.", function () {
      var snapshot = S.deleteProtokoll(id);
      U.toast("Protokoll gelöscht.", "warn", {
        label: "Rückgängig",
        run: function () { S.restoreProtokoll(snapshot); U.toast("Wiederhergestellt.", "ok"); }
      });
      if (danach) danach();
    });
  }

  /* =====================================================================
     Protokoll-Detail (Dokumentansicht, druckbar)
     ===================================================================== */
  function protokollDetail(id) {
    var p = S.protokoll(id);
    if (!p) {
      return { html: leer("Protokoll nicht gefunden", "Der Eintrag wurde möglicherweise gelöscht.",
        '<a class="btn btn-primary" href="#/protokolle">Zur Protokollliste</a>'), mount: function () {} };
    }
    var d = p.dealId ? S.deal(p.dealId) : null;
    var k = p.kontaktId ? S.kontakt(p.kontaktId) : null;
    var e = S.state.einstellungen;

    function absatz(titel, text) {
      if (!text) return "";
      return '<section class="doc-block"><h3>' + U.esc(titel) + "</h3>" +
        '<p style="white-space:pre-wrap">' + U.esc(text) + "</p></section>";
    }

    var kopf = [
      ["Betreff", U.esc(p.betreff)],
      ["Datum", U.datum(p.datum + "T12:00:00") + (p.uhrzeit ? ", " + U.esc(p.uhrzeit) + " Uhr" : "") +
        (p.dauer ? " (" + p.dauer + " Min.)" : "")],
      ["Art", U.esc(kanal(p.kanal).label)],
      ["Bezug", d ? dealLink(d) + " · " + U.kategoriePill(d.kategorie) : '<span class="muted">interner Termin</span>'],
      ["Gegenpartei", k ? '<a href="#/kontakt/' + k.id + '">' + U.esc(S.kontaktName(k)) + "</a>" +
        (k.firma ? " · " + U.esc(k.firma) : "") : '<span class="muted">—</span>'],
      ["Teilnehmer", U.esc(p.teilnehmer || "—")],
      ["Protokollführung", U.esc(p.verfasser || "—")],
      ["Freigabe", p.freigeber ? U.esc(p.freigeber) : '<span class="muted">offen</span>']
    ].map(function (r) {
      return '<div class="doc-meta-row"><span class="k">' + U.esc(r[0]) + "</span><span class=\"v\">" + r[1] + "</span></div>";
    }).join("");

    var schritte = (p.naechsteSchritte || []).length
      ? '<div class="table-wrap"><table class="data compact"><thead><tr>' +
        '<th style="width:50%">Maßnahme</th><th>Verantwortlich</th><th>Termin</th><th>Aufgabe</th>' +
        "</tr></thead><tbody>" + p.naechsteSchritte.map(function (s) {
          return "<tr><td>" + U.esc(s.text) + "</td>" +
            "<td>" + U.esc(s.verantwortlich || "—") + "</td>" +
            "<td>" + (s.faellig ? U.datum(s.faellig + "T12:00:00") : "—") + "</td>" +
            "<td>" + (s.uebernommen ? '<span class="pill pill-green">übernommen</span>'
              : '<span class="pill">offen</span>') + "</td></tr>";
        }).join("") + "</tbody></table></div>"
      : '<p class="muted" style="font-size:0.87rem">Keine Maßnahmen vereinbart.</p>';

    var nochNichtUebernommen = (p.naechsteSchritte || []).filter(function (s) {
      return s.text && !s.uebernommen;
    }).length;

    return {
      html:
        '<div class="breadcrumb"><a href="#/protokolle">Protokolle</a> › ' + U.esc(p.nummer) + "</div>" +
        '<div class="page-head no-print"><div><h1>' + U.esc(p.nummer) + "</h1>" +
          "<p>" + U.esc(p.betreff) + "</p></div>" +
          '<div class="actions">' +
            (nochNichtUebernommen
              ? '<button class="btn" data-schritte-uebernehmen="1">' + U.icon("check", 15) +
                " " + nochNichtUebernommen + " Maßnahme(n) als Aufgabe</button>"
              : "") +
            '<button class="btn" data-kopieren="1">' + U.icon("copy", 15) + " Als Text kopieren</button>" +
            '<button class="btn" data-drucken="1">' + U.icon("print", 15) + " Drucken / PDF</button>" +
            '<button class="btn" data-edit-protokoll="1">' + U.icon("edit", 15) + " Bearbeiten</button>" +
            '<button class="btn btn-danger btn-icon" data-del-protokoll="1" title="Löschen">' + U.icon("trash", 15) + "</button>" +
          "</div></div>" +

        '<div class="row no-print" style="margin-bottom:1rem">' +
          '<span class="muted" style="font-size:0.85rem">Status:</span>' +
          D.PROTOKOLL_STATUS.map(function (s) {
            return '<button class="btn btn-sm' + (p.status === s.id ? " btn-primary" : "") +
              '" data-status="' + s.id + '">' + U.esc(s.label) + "</button>";
          }).join("") +
          (p.vertraulich ? '<span class="pill pill-red">' + U.icon("lock", 12) + " vertraulich</span>" : "") +
        "</div>" +

        '<article class="card protokoll-doc">' +
          '<header class="doc-head">' +
            "<div><div class=\"doc-firma\">" + U.esc(e.firma) + "</div>" +
            '<h2>Gesprächsprotokoll</h2></div>' +
            '<div class="doc-nummer"><span class="mono">' + U.esc(p.nummer) + "</span>" +
            "<div>" + U.statusPill(p.status) + "</div></div>" +
          "</header>" +
          '<div class="doc-meta">' + kopf + "</div>" +
          absatz("Besprochene Punkte", p.themen) +
          absatz("Ergebnisse und Vereinbarungen", p.ergebnisse) +
          absatz("Offene Punkte", p.offenePunkte) +
          '<section class="doc-block"><h3>Nächste Schritte</h3>' + schritte + "</section>" +
          '<footer class="doc-foot">' +
            '<div class="sig"><span class="line"></span>' + U.esc(p.verfasser || "") +
              "<small>Protokollführung</small></div>" +
            '<div class="sig"><span class="line"></span>' + U.esc(p.freigeber || "") +
              "<small>Freigabe</small></div>" +
          "</footer>" +
          '<p class="doc-note">Erstellt am ' + U.datumZeit(p.createdAt) +
            (p.updatedAt && p.updatedAt !== p.createdAt ? " · zuletzt geändert " + U.datumZeit(p.updatedAt) : "") +
            (p.vertraulich ? " · Vertraulich — nur für interne Verwendung" : "") + "</p>" +
        "</article>",
      mount: function (root) {
        root.querySelectorAll("[data-status]").forEach(function (b) {
          b.addEventListener("click", function () {
            S.setProtokollStatus(p.id, b.getAttribute("data-status"));
            U.toast("Status aktualisiert.", "ok");
          });
        });
        var edit = root.querySelector("[data-edit-protokoll]");
        if (edit) edit.addEventListener("click", function () { F.protokoll(p.id); });

        var kopieren = root.querySelector("[data-kopieren]");
        if (kopieren) kopieren.addEventListener("click", function () {
          U.kopieren(S.protokollText(p), "Protokoll in die Zwischenablage kopiert.");
        });

        var drucken = root.querySelector("[data-drucken]");
        if (drucken) drucken.addEventListener("click", function () { global.print(); });

        var uebernehmen = root.querySelector("[data-schritte-uebernehmen]");
        if (uebernehmen) uebernehmen.addEventListener("click", function () {
          var n = S.aufgabenAusProtokoll(p);
          S.save(); S.emit();
          U.toast(n + " Aufgabe(n) aus dem Protokoll erzeugt.", "ok");
        });

        var del = root.querySelector("[data-del-protokoll]");
        if (del) del.addEventListener("click", function () {
          loescheProtokoll(p.id, function () { location.hash = "#/protokolle"; });
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

    function zeile(t) {
      var fl = U.faelligText(t.faellig);
      var d = t.dealId ? S.deal(t.dealId) : null;
      var kt = t.kontaktId ? S.kontakt(t.kontaktId) : null;
      return '<div class="task-row' + (t.erledigt ? " done" : "") + '">' +
        '<input type="checkbox" data-toggle="' + t.id + '"' + (t.erledigt ? " checked" : "") + ' aria-label="Erledigt">' +
        '<div class="grow"><div class="t">' + U.esc(t.titel) + "</div>" +
          '<div class="m">' +
            '<span class="tag">' + U.esc(aufgabenTyp(t.typ).label) + "</span>" +
            '<span class="' + (t.erledigt ? "faint" : fl.cls) + '">' + (t.erledigt ? "erledigt" : U.esc(fl.text)) + "</span>" +
            '<span class="pill ' + prio(t.prioritaet).cls + '">' + prio(t.prioritaet).label + "</span>" +
            (d ? '<a href="#/deal/' + d.id + '">' + U.esc(d.titel) + "</a>" : "") +
            (kt ? '<a href="#/kontakt/' + kt.id + '">' + U.esc(S.kontaktName(kt)) + "</a>" : "") +
            (t.protokollId ? '<a href="#/protokoll/' + t.protokollId + '">' + U.icon("protokoll", 12) + " Protokoll</a>" : "") +
            (t.notiz ? '<span class="faint">' + U.esc(t.notiz) + "</span>" : "") +
          "</div></div>" +
        '<button class="btn btn-sm btn-icon btn-ghost" data-task-edit="' + t.id + '" title="Bearbeiten">' + U.icon("edit", 14) + "</button>" +
        '<button class="btn btn-sm btn-icon btn-ghost" data-task-del="' + t.id + '" title="Löschen">' + U.icon("trash", 14) + "</button>" +
        "</div>";
    }

    function gruppe(titel, liste, klasse) {
      if (!liste.length) return "";
      return '<div class="card"><div class="card-head"><h2 class="' + (klasse || "") + '">' + U.esc(titel) + "</h2>" +
        '<span class="sub">' + liste.length + "</span></div>" +
        '<div class="card-body" style="padding:0 1rem">' + liste.map(zeile).join("") + "</div></div>";
    }

    var ueberfaellig = sichtbar.filter(function (t) { return !t.erledigt && t.faellig && t.faellig < heute; });
    var heuteListe   = sichtbar.filter(function (t) { return !t.erledigt && t.faellig === heute; });
    var woche        = sichtbar.filter(function (t) {
      var dd = U.tageBis(t.faellig);
      return !t.erledigt && dd !== null && dd > 0 && dd <= 7;
    });
    var spaeter      = sichtbar.filter(function (t) {
      var dd = U.tageBis(t.faellig);
      return !t.erledigt && (dd === null || dd > 7);
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
     Auswertungen
     ===================================================================== */
  function berichte() {
    var k = S.kpis();
    var stufen = S.proStage();

    var trichterStufen = stufen
      .filter(function (p) { return p.stage.id !== "verloren"; })
      .map(function (p) { return { label: p.stage.label, wert: p.anzahl, farbe: p.stage.color }; });

    var palette = ["#4f6df5", "#22c55e", "#f59e0b", "#a78bfa", "#0ea5e9", "#ef4444", "#14b8a6", "#94a3b8"];

    var kategorien = S.proKategorie();
    var donutDaten = kategorien.map(function (r) {
      return { label: r.kategorie.label, wert: r.volumen, farbe: r.kategorie.farbe };
    });

    var kategorieTabelle = '<div class="table-wrap"><table class="data compact"><thead><tr>' +
      '<th>Anlageklasse</th><th class="num">Deals</th><th class="num">davon aktiv</th>' +
      '<th class="num">Volumen</th><th class="num">Marge</th><th class="num">Quote</th>' +
      "</tr></thead><tbody>" + kategorien.map(function (r) {
        var entschieden = r.gewonnen + r.verloren;
        return "<tr><td>" + U.kategoriePill(r.kategorie.id, true) + "</td>" +
          '<td class="num">' + r.anzahl + "</td>" +
          '<td class="num">' + r.aktiv + "</td>" +
          '<td class="num">' + U.eurKurz(r.volumen) + "</td>" +
          '<td class="num">' + (r.marge ? U.eurKurz(r.marge) : "—") + "</td>" +
          '<td class="num">' + (entschieden ? U.dez((r.gewonnen / entschieden) * 100) + " %" : "—") + "</td></tr>";
      }).join("") + "</tbody></table></div>";

    var nachOrt = S.gruppiereNach("land").slice(0, 8).map(function (g, i) {
      return { label: g.key, wert: g.volumen, farbe: palette[i % palette.length] };
    });

    /* Quellen */
    var quellen = {};
    S.state.deals.forEach(function (d) {
      var q = d.quelle || "Ohne Angabe";
      if (!quellen[q]) quellen[q] = { key: q, anzahl: 0, volumen: 0, gewonnen: 0, verloren: 0 };
      quellen[q].anzahl++;
      quellen[q].volumen += d.volumen || 0;
      if (d.stage === "gewonnen") quellen[q].gewonnen++;
      if (d.stage === "verloren") quellen[q].verloren++;
    });
    var quellenTabelle = '<div class="table-wrap"><table class="data compact"><thead><tr>' +
      '<th>Quelle</th><th class="num">Deals</th><th class="num">Volumen</th>' +
      '<th class="num">Gewonnen</th><th class="num">Quote</th></tr></thead><tbody>' +
      Object.keys(quellen).map(function (key) { return quellen[key]; })
        .sort(function (a, b) { return b.volumen - a.volumen; })
        .map(function (q) {
          var entschieden = q.gewonnen + q.verloren;
          return "<tr><td>" + U.esc(q.key) + "</td>" +
            '<td class="num">' + q.anzahl + "</td>" +
            '<td class="num">' + U.eurKurz(q.volumen) + "</td>" +
            '<td class="num">' + q.gewonnen + "</td>" +
            '<td class="num">' + (entschieden ? U.dez((q.gewonnen / entschieden) * 100) + " %" : "—") + "</td></tr>";
        }).join("") + "</tbody></table></div>";

    /* Team inklusive Protokollleistung */
    var team = {};
    D.TEAM.forEach(function (m) {
      team[m.name] = { key: m.name, rolle: m.rolle, aktiv: 0, volumen: 0, gewichtet: 0, gewonnen: 0, protokolle: 0 };
    });
    S.state.deals.forEach(function (d) {
      var b = d.betreuer || "Nicht zugeordnet";
      if (!team[b]) team[b] = { key: b, rolle: "", aktiv: 0, volumen: 0, gewichtet: 0, gewonnen: 0, protokolle: 0 };
      if (S.isOffen(d)) {
        team[b].aktiv++;
        team[b].volumen += d.volumen || 0;
        team[b].gewichtet += S.gewichtet(d);
      }
      if (d.stage === "gewonnen") team[b].gewonnen++;
    });
    S.state.protokolle.forEach(function (p) {
      if (p.verfasser && team[p.verfasser]) team[p.verfasser].protokolle++;
    });
    var teamTabelle = '<div class="table-wrap"><table class="data compact"><thead><tr>' +
      '<th>Team</th><th class="num">Aktive Deals</th><th class="num">Volumen</th>' +
      '<th class="num">Gewichtet</th><th class="num">Abschlüsse</th><th class="num">Protokolle</th>' +
      "</tr></thead><tbody>" +
      Object.keys(team).map(function (key) { return team[key]; })
        .sort(function (a, b) { return b.gewichtet - a.gewichtet || b.protokolle - a.protokolle; })
        .map(function (t) {
          return '<tr><td><div class="row" style="gap:0.5rem;flex-wrap:nowrap">' +
            '<span class="avatar" style="width:26px;height:26px;font-size:0.68rem">' + U.esc(U.initialen(t.key)) + "</span>" +
            "<div>" + U.esc(t.key) + '<div class="cell-sub">' + U.esc(t.rolle || "") + "</div></div></div></td>" +
            '<td class="num">' + t.aktiv + "</td>" +
            '<td class="num">' + U.eurKurz(t.volumen) + "</td>" +
            '<td class="num">' + U.eurKurz(t.gewichtet) + "</td>" +
            '<td class="num">' + t.gewonnen + "</td>" +
            '<td class="num">' + t.protokolle + "</td></tr>";
        }).join("") + "</tbody></table></div>";

    return {
      html:
        '<div class="page-head"><div><h1>Auswertungen</h1>' +
          "<p>Kennzahlen über " + U.num(k.dealsGesamt) + " Deals, " + U.num(k.kontakte) +
          " Kontakte und " + U.num(k.protokolle) + " Protokolle</p></div>" +
          '<div class="actions"><button class="btn" data-drucken="1">' + U.icon("print", 15) + " Drucken</button></div></div>" +
        '<div class="stack">' +
          '<div class="grid grid-kpi">' +
            '<div class="card kpi"><div class="label">' + U.icon("euro", 15) + "Abschlussvolumen</div>" +
              '<div class="value">' + U.eurKurz(k.abschlussvolumen) + '</div><div class="foot">' + k.gewonnen + " abgeschlossene Deals</div></div>" +
            '<div class="card kpi"><div class="label">' + U.icon("chart", 15) + "Gewichtete Marge</div>" +
              '<div class="value">' + U.eurKurz(k.margeGewichtet) + '</div><div class="foot">aus ' + k.aktiveDeals + " aktiven Deals</div></div>" +
            '<div class="card kpi"><div class="label">' + U.icon("check", 15) + "Abschlussquote</div>" +
              '<div class="value">' + U.dez(k.quote) + ' %</div><div class="foot">' + k.gewonnen + " von " + (k.gewonnen + k.verloren) + " entschieden</div></div>" +
            '<div class="card kpi"><div class="label">' + U.icon("protokoll", 15) + "Protokolle</div>" +
              '<div class="value">' + U.num(k.protokolle) + '</div><div class="foot">' + k.protokolleEntwurf + " im Entwurf</div></div>" +
          "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Funnel nach Phase</h2><span class="sub">Anzahl Deals</span></div>' +
              '<div class="card-body">' + U.trichter(trichterStufen) + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Volumen nach Anlageklasse</h2></div>' +
              '<div class="card-body">' + (donutDaten.length ? U.donut(donutDaten, U.eurKurz) : '<p class="muted">Keine Daten</p>') + "</div></div>" +
          "</div>" +
          '<div class="card"><div class="card-head"><h2>Anlageklassen im Vergleich</h2></div>' + kategorieTabelle + "</div>" +
          '<div class="grid grid-2">' +
            '<div class="card"><div class="card-head"><h2>Volumen nach Land</h2></div>' +
              '<div class="card-body">' + (nachOrt.length ? U.balken(nachOrt, U.eurKurz) : '<p class="muted">Keine Daten</p>') + "</div></div>" +
            '<div class="card"><div class="card-head"><h2>Protokolle je Monat</h2><span class="sub">12 Monate</span></div>' +
              '<div class="card-body">' + U.saeulen(S.protokolleProMonat(12).map(function (m) {
                return { label: m.label, wert: m.anzahl };
              })) + "</div></div>" +
          "</div>" +
          '<div class="card"><div class="card-head"><h2>Neue Deals je Monat</h2><span class="sub">12 Monate</span></div>' +
            '<div class="card-body">' + U.saeulen(S.neuProMonat(12).map(function (m) {
              return { label: m.label, wert: m.anzahl };
            })) + "</div></div>" +
          '<div class="card"><div class="card-head"><h2>Quellen-Performance</h2></div>' + quellenTabelle + "</div>" +
          '<div class="card"><div class="card-head"><h2>Team-Performance</h2></div>' + teamTabelle + "</div>" +
        "</div>",
      mount: function (root) {
        var p = root.querySelector("[data-drucken]");
        if (p) p.addEventListener("click", function () { global.print(); });
      }
    };
  }

  /* =====================================================================
     Einstellungen
     ===================================================================== */
  function einstellungen() {
    var e = S.state.einstellungen;
    var groesse = 0;
    try { groesse = (localStorage.getItem("offmarket-crm-v2") || "").length; } catch (err) { /* ignorieren */ }

    return {
      html:
        '<div class="page-head"><div><h1>Einstellungen</h1>' +
          "<p>Profil, Protokollführung, Darstellung und Datenverwaltung</p></div></div>" +
        '<div class="grid grid-2">' +
          '<div class="card"><div class="card-head"><h2>Profil</h2></div><div class="card-body">' +
            '<div class="form-grid">' +
              U.feld("Unternehmen", U.input("firma", e.firma), true) +
              U.feld("Angemeldet als", U.select("nutzer", e.nutzer, D.TEAM_NAMEN)) +
              U.feld("Protokollführung (Standard)", U.select("assistenz", e.assistenz, D.TEAM_NAMEN)) +
              U.feld("Ziel-Marge (%)", U.input("zielMarge", e.zielMarge, { typ: "number", min: 0, schritt: 0.5 })) +
            "</div>" +
            '<div class="divider"></div>' +
            '<label class="check"><input type="checkbox" id="auto-aufgaben"' +
              (e.aufgabenAusProtokoll ? " checked" : "") +
              "> Maßnahmen aus Protokollen standardmäßig als Aufgaben übernehmen</label>" +
            '<div class="divider"></div>' +
            '<button class="btn btn-primary" id="profil-speichern">Speichern</button>' +
          "</div></div>" +
          '<div class="card"><div class="card-head"><h2>Darstellung</h2></div><div class="card-body">' +
            '<p class="muted" style="font-size:0.87rem;margin-bottom:0.7rem">Standardmäßig folgt das Design deiner Systemeinstellung.</p>' +
            '<div class="row">' +
              '<button class="btn' + (e.theme === "light" ? " btn-primary" : "") + '" data-theme-set="light">' + U.icon("sun", 15) + " Hell</button>" +
              '<button class="btn' + (e.theme === "dark" ? " btn-primary" : "") + '" data-theme-set="dark">' + U.icon("moon", 15) + " Dunkel</button>" +
              '<button class="btn' + ((e.theme || "auto") === "auto" ? " btn-primary" : "") + '" data-theme-set="auto">System</button>' +
            "</div></div></div>" +
          '<div class="card span-2"><div class="card-head"><h2>Daten</h2>' +
            '<span class="sub">' + U.num(S.state.deals.length) + " Deals · " + U.num(S.state.kontakte.length) +
            " Kontakte · " + U.num(S.state.aufgaben.length) + " Aufgaben · " + U.num(S.state.protokolle.length) +
            " Protokolle · " + U.num(Math.round(groesse / 1024)) + " KB</span></div>" +
            '<div class="card-body">' +
              '<p class="muted" style="font-size:0.87rem;margin-bottom:0.8rem">' +
              "Alle Daten liegen ausschließlich lokal im Browser (localStorage). Für ein Backup oder den Wechsel des Geräts nutze den JSON-Export. " +
              "Ein Datenbestand aus der Immobilien-Version wird beim ersten Start automatisch übernommen.</p>" +
              '<div class="row">' +
                '<button class="btn" id="export-json">' + U.icon("download", 15) + " JSON-Export</button>" +
                '<button class="btn" id="import-json">' + U.icon("upload", 15) + " JSON-Import</button>" +
                '<button class="btn" data-csv="deals">' + U.icon("download", 15) + " Deals als CSV</button>" +
                '<button class="btn" data-csv="kontakte">' + U.icon("download", 15) + " Kontakte als CSV</button>" +
                '<button class="btn" data-csv="protokolle">' + U.icon("download", 15) + " Protokolle als CSV</button>" +
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
              "<li><kbd>N</kbd><span class=\"grow\">Neuen Deal anlegen</span></li>" +
              "<li><kbd>P</kbd><span class=\"grow\">Neues Protokoll anlegen</span></li>" +
              "<li><kbd>Esc</kbd><span class=\"grow\">Dialog schließen</span></li>" +
            "</ul></div></div>" +
        "</div>",
      mount: function (root) {
        root.querySelector("#profil-speichern").addEventListener("click", function () {
          S.setEinstellung("firma", root.querySelector('[name="firma"]').value.trim() || "OffMarket Partners");
          S.setEinstellung("nutzer", root.querySelector('[name="nutzer"]').value);
          S.setEinstellung("assistenz", root.querySelector('[name="assistenz"]').value);
          S.setEinstellung("zielMarge", Number(root.querySelector('[name="zielMarge"]').value) || 2);
          S.setEinstellung("aufgabenAusProtokoll", root.querySelector("#auto-aufgaben").checked);
          U.toast("Einstellungen gespeichert.", "ok");
          global.App.render();
        });
        root.querySelectorAll("[data-theme-set]").forEach(function (b) {
          b.addEventListener("click", function () {
            global.App.setTheme(b.getAttribute("data-theme-set"));
          });
        });
        root.querySelector("#export-json").addEventListener("click", function () {
          U.download("deal-crm-" + S.heuteISO() + ".json", S.exportJSON(), "application/json");
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
              U.toast(r.deals + " Deals, " + r.kontakte + " Kontakte, " + r.protokolle + " Protokolle importiert.", "ok");
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
          U.frage("Wirklich alle Daten löschen?", "Deals, Kontakte, Aufgaben, Protokolle und Verlauf werden unwiderruflich entfernt.", function () {
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
    var dealTreffer = S.state.deals.filter(function (d) {
      return (d.titel + " " + d.ort + " " + d.land + " " + S.kategorie(d.kategorie).label + " " +
              (d.tags || []).join(" ")).toLowerCase().indexOf(s) !== -1;
    });
    var kontaktTreffer = S.state.kontakte.filter(function (k) {
      return (S.kontaktName(k) + " " + k.firma + " " + k.email + " " + k.telefon + " " + k.ort)
        .toLowerCase().indexOf(s) !== -1;
    });
    var protokollTreffer = S.state.protokolle.filter(function (p) {
      return (p.nummer + " " + p.betreff + " " + p.teilnehmer + " " + p.themen + " " + p.ergebnisse)
        .toLowerCase().indexOf(s) !== -1;
    });
    var aufgabenTreffer = S.state.aufgaben.filter(function (t) {
      return (t.titel + " " + t.notiz).toLowerCase().indexOf(s) !== -1;
    });

    var gesamt = dealTreffer.length + kontaktTreffer.length + protokollTreffer.length + aufgabenTreffer.length;

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
          block("Deals", dealTreffer, function (d) {
            return '<li><div class="grow"><div class="cell-title">' + dealLink(d) + "</div>" +
              '<div class="cell-sub">' + U.esc(S.kategorie(d.kategorie).label + " · " + (d.ort || "")) + "</div></div>" +
              U.stagePill(d.stage) + '<span class="mono nowrap">' + U.eurKurz(d.volumen) + "</span></li>";
          }) +
          block("Protokolle", protokollTreffer, function (p) {
            return '<li><div class="grow"><div class="cell-title">' +
              '<a href="#/protokoll/' + p.id + '">' + U.esc(p.betreff) + "</a></div>" +
              '<div class="cell-sub">' + U.esc(p.nummer) + " · " + U.datum(p.datum + "T12:00:00") + "</div></div>" +
              U.statusPill(p.status) + "</li>";
          }) +
          block("Kontakte", kontaktTreffer, function (k) {
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
    deals: deals,
    dealDetail: dealDetail,
    pipeline: pipeline,
    kontakte: kontakte,
    kontaktDetail: kontaktDetail,
    protokolle: protokolle,
    protokollDetail: protokollDetail,
    aufgaben: aufgaben,
    berichte: berichte,
    einstellungen: einstellungen,
    suche: suche,
    gefilterteDeals: gefilterteDeals,
    gefilterteProtokolle: gefilterteProtokolle
  };
})(window);
