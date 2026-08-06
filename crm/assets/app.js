/* Deal CRM — Router, Layout-Shell und globale Interaktionen */
(function (global) {
  "use strict";

  var S = global.Store, U = global.UI, D = global.CRMData, V = global.Views, F = global.Forms;

  var NAV = [
    { hash: "#/dashboard",     label: "Übersicht",     icon: "dashboard" },
    { hash: "#/pipeline",      label: "Pipeline",      icon: "kanban" },
    { hash: "#/deals",         label: "Deals",         icon: "briefcase", count: function () { return S.state.deals.length; } },
    { hash: "#/kontakte",      label: "Kontakte",      icon: "users",     count: function () { return S.state.kontakte.length; } },
    { hash: "#/protokolle",    label: "Protokolle",    icon: "protokoll", count: function () { return S.state.protokolle.length; } },
    { hash: "#/aufgaben",      label: "Aufgaben",      icon: "check",     count: function () {
        return S.state.aufgaben.filter(function (t) { return !t.erledigt; }).length; } },
    { hash: "#/berichte",      label: "Auswertungen",  icon: "chart" },
    { hash: "#/einstellungen", label: "Einstellungen", icon: "settings" }
  ];

  var aktuellerRoute = "";

  /* ---------- Theme ---------- */
  function setTheme(wert) {
    S.setEinstellung("theme", wert);
    wendeThemeAn();
    render();
  }

  function wendeThemeAn() {
    var wert = S.state.einstellungen.theme || "auto";
    var dunkel = wert === "dark" ||
      (wert === "auto" && global.matchMedia && global.matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.setAttribute("data-theme", dunkel ? "dark" : "light");
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.innerHTML = U.icon(dunkel ? "sun" : "moon", 17);
      btn.title = dunkel ? "Helles Design" : "Dunkles Design";
    }
  }

  /* ---------- Navigation ---------- */
  function zeichneNav() {
    var basis = (location.hash || "#/dashboard").split("/").slice(0, 2).join("/");
    var alias = { "#/deal": "#/deals", "#/kontakt": "#/kontakte", "#/protokoll": "#/protokolle" };
    if (alias[basis]) basis = alias[basis];

    document.getElementById("nav").innerHTML =
      '<div class="nav-label">Vertrieb</div>' +
      NAV.slice(0, 4).map(navLink.bind(null, basis)).join("") +
      '<div class="nav-label">Dokumentation</div>' +
      NAV.slice(4, 6).map(navLink.bind(null, basis)).join("") +
      '<div class="nav-label">Analyse &amp; System</div>' +
      NAV.slice(6).map(navLink.bind(null, basis)).join("");

    var e = S.state.einstellungen;
    document.getElementById("who").innerHTML =
      '<span class="avatar">' + U.esc(U.initialen(e.nutzer)) + "</span>" +
      '<div class="who"><strong>' + U.esc(e.nutzer) + "</strong><span>" + U.esc(e.firma) + "</span></div>";
  }

  function navLink(basis, item) {
    var aktiv = item.hash === basis;
    var n = item.count ? item.count() : null;
    return '<a href="' + item.hash + '" class="' + (aktiv ? "active" : "") + '">' +
      U.icon(item.icon, 18) + U.esc(item.label) +
      (n ? '<span class="count">' + U.num(n) + "</span>" : "") + "</a>";
  }

  /* ---------- Routing ---------- */
  function route() {
    var hash = location.hash || "#/dashboard";
    var teile = hash.replace(/^#\//, "").split("/");
    var name = teile[0] || "dashboard";
    var param = teile[1] ? decodeURIComponent(teile[1]) : "";

    switch (name) {
      case "":
      case "dashboard":     return V.dashboard();
      case "deals":         return V.deals();
      case "deal":          return V.dealDetail(param);
      case "pipeline":      return V.pipeline();
      case "kontakte":      return V.kontakte();
      case "kontakt":       return V.kontaktDetail(param);
      case "protokolle":    return V.protokolle();
      case "protokoll":     return V.protokollDetail(param);
      case "aufgaben":      return V.aufgaben();
      case "berichte":      return V.berichte();
      case "einstellungen": return V.einstellungen();
      case "suche":         return V.suche(param);
      default:              return V.dashboard();
    }
  }

  function render(opts) {
    opts = opts || {};
    var view = route();
    var root = document.getElementById("view");

    /* Cursorposition eines fokussierten Filterfelds erhalten */
    var caret = null;
    if (opts.fokus) {
      var vorher = root.querySelector(opts.fokus);
      if (vorher) caret = vorher.selectionStart;
    }

    root.innerHTML = view.html;
    view.mount(root);
    zeichneNav();
    bindeGlobaleAktionen(root);

    if (opts.fokus) {
      var el = root.querySelector(opts.fokus);
      if (el) {
        el.focus();
        if (caret !== null && el.setSelectionRange) el.setSelectionRange(caret, caret);
      }
    } else if (aktuellerRoute !== location.hash) {
      global.scrollTo(0, 0);
    }
    aktuellerRoute = location.hash;
    document.body.classList.remove("nav-open");
  }

  /* ---------- Aktionen, die in mehreren Ansichten vorkommen ---------- */
  function neu(art) {
    if (art === "deal") F.deal(null, function (d) { location.hash = "#/deal/" + d.id; });
    if (art === "kontakt") F.kontakt(null);
    if (art === "aufgabe") F.aufgabe(null);
    if (art === "protokoll") F.protokoll(null, null, function (p) { location.hash = "#/protokoll/" + p.id; });
  }

  function bindeGlobaleAktionen(root) {
    root.querySelectorAll("[data-neu]").forEach(function (b) {
      b.addEventListener("click", function () { neu(b.getAttribute("data-neu")); });
    });
    root.querySelectorAll("[data-csv]").forEach(function (b) {
      b.addEventListener("click", function () { exportCSV(b.getAttribute("data-csv")); });
    });
  }

  function exportCSV(art) {
    if (art === "deals") {
      var liste = V.gefilterteDeals();
      var spalten = [
        { label: "Bezeichnung", get: function (d) { return d.titel; } },
        { label: "Kategorie", get: function (d) { return S.kategorie(d.kategorie).label; } },
        { label: "Phase", get: function (d) { return S.stage(d.stage).label; } },
        { label: "Volumen", get: function (d) { return d.volumen || ""; } },
        { label: "Menge", get: function (d) { return d.menge || ""; } },
        { label: "Einheit", get: function (d) { return d.einheit || ""; } },
        { label: "Preis je Einheit", get: function (d) {
            return S.preisProEinheit(d) ? Math.round(S.preisProEinheit(d)) : ""; } },
        { label: "Marge", get: function (d) { return d.marge || ""; } },
        { label: "Marge %", get: function (d) {
            return S.margeProzent(d) ? S.margeProzent(d).toFixed(1).replace(".", ",") : ""; } },
        { label: "Ertrag p. a.", get: function (d) { return d.ertragJahr || ""; } },
        { label: "Faktor", get: function (d) {
            return S.faktor(d) ? S.faktor(d).toFixed(1).replace(".", ",") : ""; } },
        { label: "Wahrscheinlichkeit %", get: function (d) { return d.wahrscheinlichkeit; } },
        { label: "Gewichtet", get: function (d) { return Math.round(S.gewichtet(d)); } },
        { label: "Ort", get: function (d) { return d.ort; } },
        { label: "Land", get: function (d) { return d.land; } },
        { label: "Quelle", get: function (d) { return d.quelle; } },
        { label: "Betreuer", get: function (d) { return d.betreuer; } },
        { label: "Gegenpartei", get: function (d) {
            return d.kontaktId ? S.kontaktName(S.kontakt(d.kontaktId)) : ""; } },
        { label: "Fachdaten", get: function (d) {
            return Object.keys(d.details || {}).map(function (key) {
              return key + ": " + d.details[key];
            }).join(" | "); } },
        { label: "Schlagwörter", get: function (d) { return (d.tags || []).join(", "); } },
        { label: "Geändert", get: function (d) { return U.datum(d.updatedAt); } }
      ];
      U.download("deals-" + S.heuteISO() + ".csv", S.toCSV(liste, spalten), "text/csv");
      U.toast(liste.length + " Deals exportiert.", "ok");
      return;
    }

    if (art === "kontakte") {
      var spaltenK = [
        { label: "Vorname", get: function (k) { return k.vorname; } },
        { label: "Nachname", get: function (k) { return k.nachname; } },
        { label: "Rolle", get: function (k) {
            var t = D.KONTAKTTYPEN.filter(function (x) { return x.id === k.typ; })[0];
            return t ? t.label : k.typ; } },
        { label: "Firma", get: function (k) { return k.firma; } },
        { label: "E-Mail", get: function (k) { return k.email; } },
        { label: "Telefon", get: function (k) { return k.telefon; } },
        { label: "Straße", get: function (k) { return k.strasse; } },
        { label: "PLZ", get: function (k) { return k.plz; } },
        { label: "Ort", get: function (k) { return k.ort; } },
        { label: "Land", get: function (k) { return k.land || ""; } },
        { label: "Deals", get: function (k) {
            return S.state.deals.filter(function (d) { return d.kontaktId === k.id; }).length; } },
        { label: "Protokolle", get: function (k) { return S.protokolleFuer(null, k.id).length; } },
        { label: "Notizen", get: function (k) { return k.notizen; } }
      ];
      U.download("kontakte-" + S.heuteISO() + ".csv", S.toCSV(S.state.kontakte, spaltenK), "text/csv");
      U.toast(S.state.kontakte.length + " Kontakte exportiert.", "ok");
      return;
    }

    if (art === "protokolle") {
      var listeP = V.gefilterteProtokolle();
      var spaltenP = [
        { label: "Nummer", get: function (p) { return p.nummer; } },
        { label: "Datum", get: function (p) { return p.datum; } },
        { label: "Uhrzeit", get: function (p) { return p.uhrzeit; } },
        { label: "Dauer (Min.)", get: function (p) { return p.dauer || ""; } },
        { label: "Art", get: function (p) {
            var kn = D.KANAELE.filter(function (x) { return x.id === p.kanal; })[0];
            return kn ? kn.label : p.kanal; } },
        { label: "Betreff", get: function (p) { return p.betreff; } },
        { label: "Deal", get: function (p) { return p.dealId ? (S.deal(p.dealId) || {}).titel || "" : ""; } },
        { label: "Kontakt", get: function (p) {
            return p.kontaktId ? S.kontaktName(S.kontakt(p.kontaktId)) : ""; } },
        { label: "Teilnehmer", get: function (p) { return p.teilnehmer; } },
        { label: "Protokollführung", get: function (p) { return p.verfasser; } },
        { label: "Freigabe", get: function (p) { return p.freigeber || ""; } },
        { label: "Status", get: function (p) {
            var s = D.PROTOKOLL_STATUS.filter(function (x) { return x.id === p.status; })[0];
            return s ? s.label : p.status; } },
        { label: "Vertraulich", get: function (p) { return p.vertraulich ? "ja" : "nein"; } },
        { label: "Besprochene Punkte", get: function (p) { return p.themen; } },
        { label: "Ergebnisse", get: function (p) { return p.ergebnisse; } },
        { label: "Offene Punkte", get: function (p) { return p.offenePunkte || ""; } },
        { label: "Nächste Schritte", get: function (p) {
            return (p.naechsteSchritte || []).map(function (s) {
              return s.text + (s.verantwortlich ? " (" + s.verantwortlich + ")" : "") +
                (s.faellig ? " bis " + s.faellig : "");
            }).join(" | "); } }
      ];
      U.download("protokolle-" + S.heuteISO() + ".csv", S.toCSV(listeP, spaltenP), "text/csv");
      U.toast(listeP.length + " Protokolle exportiert.", "ok");
    }
  }

  /* ---------- Start ---------- */
  function init() {
    S.load();
    wendeThemeAn();

    if (!location.hash) location.hash = "#/dashboard";
    render();

    global.addEventListener("hashchange", function () { render(); });
    S.subscribe(function () { render(); });

    var suchfeld = document.getElementById("global-search");
    suchfeld.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && suchfeld.value.trim()) {
        location.hash = "#/suche/" + encodeURIComponent(suchfeld.value.trim());
      }
      if (e.key === "Escape") suchfeld.blur();
    });

    document.getElementById("theme-toggle").addEventListener("click", function () {
      var dunkel = document.documentElement.getAttribute("data-theme") === "dark";
      setTheme(dunkel ? "light" : "dark");
    });

    document.getElementById("neues-protokoll").addEventListener("click", function () { neu("protokoll"); });
    document.getElementById("neuer-deal").addEventListener("click", function () { neu("deal"); });

    document.getElementById("burger").addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
    });
    document.getElementById("scrim").addEventListener("click", function () {
      document.body.classList.remove("nav-open");
    });

    if (global.matchMedia) {
      var mq = global.matchMedia("(prefers-color-scheme: dark)");
      var handler = function () {
        if ((S.state.einstellungen.theme || "auto") === "auto") wendeThemeAn();
      };
      if (mq.addEventListener) mq.addEventListener("change", handler);
      else if (mq.addListener) mq.addListener(handler);
    }

    document.addEventListener("keydown", function (e) {
      var imFeld = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
      if (imFeld || e.metaKey || e.ctrlKey || e.altKey) return;
      if (document.querySelector(".modal-backdrop")) return;

      if (e.key === "/") {
        e.preventDefault();
        suchfeld.focus();
        suchfeld.select();
      }
      if (e.key === "n" || e.key === "N") { e.preventDefault(); neu("deal"); }
      if (e.key === "p" || e.key === "P") { e.preventDefault(); neu("protokoll"); }
    });
  }

  global.App = { init: init, render: render, setTheme: setTheme };
})(window);
