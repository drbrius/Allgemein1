/* OffMarket CRM — Router, Layout-Shell und globale Interaktionen */
(function (global) {
  "use strict";

  var S = global.Store, U = global.UI, D = global.CRMData, V = global.Views, F = global.Forms;

  var NAV = [
    { hash: "#/dashboard",     label: "Übersicht",     icon: "dashboard" },
    { hash: "#/pipeline",      label: "Pipeline",      icon: "kanban" },
    { hash: "#/objekte",       label: "Objekte",       icon: "building", count: function () { return S.state.objekte.length; } },
    { hash: "#/kontakte",      label: "Kontakte",      icon: "users",    count: function () { return S.state.kontakte.length; } },
    { hash: "#/aufgaben",      label: "Aufgaben",      icon: "check",    count: function () {
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
    if (basis === "#/objekt") basis = "#/objekte";
    if (basis === "#/kontakt") basis = "#/kontakte";

    document.getElementById("nav").innerHTML =
      '<div class="nav-label">Vertrieb</div>' +
      NAV.slice(0, 5).map(navLink.bind(null, basis)).join("") +
      '<div class="nav-label">Analyse &amp; System</div>' +
      NAV.slice(5).map(navLink.bind(null, basis)).join("");

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
      case "objekte":       return V.objekte();
      case "objekt":        return V.objektDetail(param);
      case "pipeline":      return V.pipeline();
      case "kontakte":      return V.kontakte();
      case "kontakt":       return V.kontaktDetail(param);
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
  function bindeGlobaleAktionen(root) {
    root.querySelectorAll("[data-neu]").forEach(function (b) {
      b.addEventListener("click", function () {
        var art = b.getAttribute("data-neu");
        if (art === "objekt") F.objekt(null, function (o) { location.hash = "#/objekt/" + o.id; });
        if (art === "kontakt") F.kontakt(null);
        if (art === "aufgabe") F.aufgabe(null);
      });
    });
    root.querySelectorAll("[data-csv]").forEach(function (b) {
      b.addEventListener("click", function () { exportCSV(b.getAttribute("data-csv")); });
    });
  }

  function exportCSV(art) {
    if (art === "objekte") {
      var liste = V.gefilterteObjekte();
      var spalten = [
        { label: "Bezeichnung", get: function (o) { return o.titel; } },
        { label: "Straße", get: function (o) { return o.strasse; } },
        { label: "PLZ", get: function (o) { return o.plz; } },
        { label: "Ort", get: function (o) { return o.ort; } },
        { label: "Objektart", get: function (o) { return o.typ; } },
        { label: "Baujahr", get: function (o) { return o.baujahr || ""; } },
        { label: "Einheiten", get: function (o) { return o.einheiten || ""; } },
        { label: "Fläche m²", get: function (o) { return o.wohnflaeche || ""; } },
        { label: "Kaufpreis", get: function (o) { return o.kaufpreis || ""; } },
        { label: "Jahresmiete", get: function (o) { return o.mieteJahr || ""; } },
        { label: "Faktor", get: function (o) { return S.faktor(o) ? S.faktor(o).toFixed(1).replace(".", ",") : ""; } },
        { label: "Rendite %", get: function (o) { return S.rendite(o) ? S.rendite(o).toFixed(1).replace(".", ",") : ""; } },
        { label: "Phase", get: function (o) { return S.stage(o.stage).label; } },
        { label: "Wahrscheinlichkeit %", get: function (o) { return o.wahrscheinlichkeit; } },
        { label: "Quelle", get: function (o) { return o.quelle; } },
        { label: "Betreuer", get: function (o) { return o.betreuer; } },
        { label: "Eigentümer", get: function (o) { return o.kontaktId ? S.kontaktName(S.kontakt(o.kontaktId)) : ""; } },
        { label: "Schlagwörter", get: function (o) { return (o.tags || []).join(", "); } },
        { label: "Aktualisiert", get: function (o) { return U.datum(o.updatedAt); } }
      ];
      U.download("objekte-" + S.heuteISO() + ".csv", S.toCSV(liste, spalten), "text/csv");
      U.toast(liste.length + " Objekte exportiert.", "ok");
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
        { label: "Objekte", get: function (k) {
            return S.state.objekte.filter(function (o) { return o.kontaktId === k.id; }).length; } },
        { label: "Notizen", get: function (k) { return k.notizen; } }
      ];
      U.download("kontakte-" + S.heuteISO() + ".csv", S.toCSV(S.state.kontakte, spaltenK), "text/csv");
      U.toast(S.state.kontakte.length + " Kontakte exportiert.", "ok");
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

    document.getElementById("neues-objekt").addEventListener("click", function () {
      F.objekt(null, function (o) { location.hash = "#/objekt/" + o.id; });
    });

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
      if (e.key === "/" && !imFeld) {
        e.preventDefault();
        suchfeld.focus();
        suchfeld.select();
      }
      if ((e.key === "n" || e.key === "N") && !imFeld && !e.metaKey && !e.ctrlKey) {
        if (document.querySelector(".modal-backdrop")) return;
        e.preventDefault();
        F.objekt(null, function (o) { location.hash = "#/objekt/" + o.id; });
      }
    });
  }

  global.App = { init: init, render: render, setTheme: setTheme };
})(window);
