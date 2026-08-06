/* OffMarket CRM — UI-Bausteine: Formatierung, Icons, Modal, Toasts, Diagramme */
(function (global) {
  "use strict";

  var D = global.CRMData;

  /* ---------- Formatierung ---------- */
  var nfEur = new Intl.NumberFormat("de-DE", {
    style: "currency", currency: "EUR", maximumFractionDigits: 0
  });
  var nfNum = new Intl.NumberFormat("de-DE");
  var nfDez = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

  function eur(n) { return nfEur.format(Math.round(n || 0)); }

  function eurKurz(n) {
    n = n || 0;
    if (Math.abs(n) >= 1e6) return nfDez.format(n / 1e6) + " Mio. €";
    if (Math.abs(n) >= 1e3) return nfNum.format(Math.round(n / 1e3)) + " Tsd. €";
    return eur(n);
  }

  function num(n) { return nfNum.format(n || 0); }
  function dez(n) { return nfDez.format(n || 0); }

  function datum(iso) {
    if (!iso) return "—";
    var d = new Date(iso);
    if (isNaN(d)) return "—";
    return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
  }

  function datumZeit(iso) {
    if (!iso) return "—";
    var d = new Date(iso);
    if (isNaN(d)) return "—";
    return d.toLocaleDateString("de-DE", { day: "2-digit", month: "short" }) + ", " +
      d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
  }

  function relativ(iso) {
    if (!iso) return "—";
    var diff = Date.now() - new Date(iso).getTime();
    var tage = Math.floor(diff / 864e5);
    if (tage < 0) return "in " + Math.abs(tage) + " Tagen";
    if (tage === 0) return "heute";
    if (tage === 1) return "gestern";
    if (tage < 30) return "vor " + tage + " Tagen";
    if (tage < 365) return "vor " + Math.floor(tage / 30) + " Mon.";
    return "vor " + Math.floor(tage / 365) + " J.";
  }

  function tageBis(datumISO) {
    if (!datumISO) return null;
    var heute = new Date(); heute.setHours(0, 0, 0, 0);
    var ziel = new Date(datumISO + "T00:00:00");
    if (isNaN(ziel)) return null;
    return Math.round((ziel - heute) / 864e5);
  }

  function faelligText(datumISO) {
    var t = tageBis(datumISO);
    if (t === null) return { text: "ohne Termin", cls: "faint" };
    if (t < 0) return { text: Math.abs(t) + " Tage überfällig", cls: "overdue" };
    if (t === 0) return { text: "heute fällig", cls: "due-today" };
    if (t === 1) return { text: "morgen", cls: "" };
    if (t < 7) return { text: "in " + t + " Tagen", cls: "" };
    return { text: datum(datumISO + "T00:00:00"), cls: "muted" };
  }

  function esc(s) {
    return String(s === null || s === undefined ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function initialen(name) {
    return String(name || "?").trim().split(/\s+/).slice(0, 2)
      .map(function (w) { return w.charAt(0).toUpperCase(); }).join("");
  }

  /* ---------- Icons ---------- */
  function icon(name, size) {
    var path = D.ICONS[name] || "";
    var s = size || 18;
    return '<svg class="icon" width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" ' +
      'aria-hidden="true">' + path + "</svg>";
  }

  function stagePill(stageId) {
    var s = global.Store.stage(stageId);
    return '<span class="pill" style="background:' + s.color + '22;color:' + s.color + '">' +
      '<span class="dot"></span>' + esc(s.label) + "</span>";
  }

  /* ---------- Toasts ---------- */
  function toast(text, art, aktion) {
    var host = document.getElementById("toasts");
    if (!host) return;
    var el = document.createElement("div");
    el.className = "toast " + (art || "");
    el.innerHTML = "<span>" + esc(text) + "</span>";
    if (aktion) {
      var btn = document.createElement("button");
      btn.className = "btn btn-sm undo";
      btn.textContent = aktion.label;
      btn.addEventListener("click", function () {
        aktion.run();
        el.remove();
      });
      el.appendChild(btn);
    }
    host.appendChild(el);
    setTimeout(function () { el.remove(); }, aktion ? 7000 : 3200);
  }

  /* ---------- Modal ---------- */
  var offen = null;

  function modal(opts) {
    schliessen();
    var backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.innerHTML =
      '<div class="modal' + (opts.narrow ? " narrow" : "") + '" role="dialog" aria-modal="true">' +
        "<header><h2>" + esc(opts.titel) + "</h2>" +
          '<button class="btn btn-ghost btn-icon btn-close" aria-label="Schließen">' + icon("close", 18) + "</button>" +
        "</header>" +
        '<div class="body">' + opts.body + "</div>" +
        '<footer>' +
          '<button class="btn" data-act="abbrechen">' + esc(opts.abbrechenLabel || "Abbrechen") + "</button>" +
          '<button class="btn ' + (opts.gefahr ? "btn-danger" : "btn-primary") + '" data-act="ok">' +
            esc(opts.okLabel || "Speichern") + "</button>" +
        "</footer>" +
      "</div>";

    document.body.appendChild(backdrop);
    offen = backdrop;

    var dialog = backdrop.querySelector(".modal");
    backdrop.addEventListener("mousedown", function (e) {
      if (e.target === backdrop) schliessen();
    });
    backdrop.querySelector(".btn-close").addEventListener("click", schliessen);
    backdrop.querySelector('[data-act="abbrechen"]').addEventListener("click", schliessen);
    backdrop.querySelector('[data-act="ok"]').addEventListener("click", function () {
      if (opts.onOk && opts.onOk(dialog) === false) return;
      schliessen();
    });
    dialog.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName !== "TEXTAREA" && !e.shiftKey) {
        e.preventDefault();
        if (opts.onOk && opts.onOk(dialog) === false) return;
        schliessen();
      }
    });

    var erstes = dialog.querySelector("input, select, textarea");
    if (erstes) erstes.focus();
    if (opts.onOpen) opts.onOpen(dialog);
    return dialog;
  }

  function schliessen() {
    if (offen) { offen.remove(); offen = null; }
  }

  function frage(titel, text, onJa, okLabel) {
    modal({
      titel: titel,
      narrow: true,
      body: '<p style="font-size:0.9rem">' + esc(text) + "</p>",
      okLabel: okLabel || "Löschen",
      gefahr: true,
      onOk: function () { onJa(); }
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") schliessen();
  });

  /* ---------- Formular-Bausteine ---------- */
  function feld(label, inner, breit) {
    return '<label class="field' + (breit ? " full" : "") + '"><span>' + esc(label) + "</span>" + inner + "</label>";
  }

  function input(name, wert, opts) {
    opts = opts || {};
    return '<input type="' + (opts.typ || "text") + '" name="' + name + '" value="' + esc(wert === 0 ? "0" : (wert || "")) + '"' +
      (opts.platzhalter ? ' placeholder="' + esc(opts.platzhalter) + '"' : "") +
      (opts.schritt ? ' step="' + opts.schritt + '"' : "") +
      (opts.min !== undefined ? ' min="' + opts.min + '"' : "") + ">";
  }

  function textarea(name, wert, platzhalter) {
    return '<textarea name="' + name + '" placeholder="' + esc(platzhalter || "") + '">' + esc(wert || "") + "</textarea>";
  }

  function select(name, wert, optionen, leerLabel) {
    var html = '<select name="' + name + '">';
    if (leerLabel) html += '<option value="">' + esc(leerLabel) + "</option>";
    optionen.forEach(function (o) {
      var v = typeof o === "string" ? o : o.value;
      var l = typeof o === "string" ? o : o.label;
      html += '<option value="' + esc(v) + '"' + (String(v) === String(wert) ? " selected" : "") + ">" + esc(l) + "</option>";
    });
    return html + "</select>";
  }

  function formWerte(dialog) {
    var out = {};
    dialog.querySelectorAll("[name]").forEach(function (el) {
      out[el.name] = el.type === "checkbox" ? el.checked : el.value.trim();
    });
    return out;
  }

  function markiereFehler(dialog, felder) {
    dialog.querySelectorAll(".invalid").forEach(function (el) { el.classList.remove("invalid"); });
    felder.forEach(function (n) {
      var el = dialog.querySelector('[name="' + n + '"]');
      if (el) el.classList.add("invalid");
    });
    if (felder.length) {
      var erstes = dialog.querySelector('[name="' + felder[0] + '"]');
      if (erstes) erstes.focus();
    }
  }

  /* ---------- Diagramme (reines SVG/HTML, keine Bibliothek) ---------- */
  function balken(daten, formatter) {
    var max = Math.max.apply(null, daten.map(function (d) { return d.wert; }).concat([1]));
    return daten.map(function (d) {
      var pct = Math.max(2, (d.wert / max) * 100);
      return '<div class="bar-row">' +
        '<span class="nowrap" title="' + esc(d.label) + '">' + esc(d.label) + "</span>" +
        '<span class="track"><span class="fill" style="width:' + pct + "%;background:" + d.farbe + '"></span></span>' +
        '<span class="val">' + esc(formatter ? formatter(d.wert) : num(d.wert)) + "</span>" +
        "</div>";
    }).join("");
  }

  function donut(daten, formatter) {
    var gesamt = daten.reduce(function (s, d) { return s + d.wert; }, 0);
    var r = 54, umfang = 2 * Math.PI * r, offset = 0;
    var kreise = "";
    if (gesamt > 0) {
      daten.forEach(function (d) {
        var anteil = d.wert / gesamt;
        var len = anteil * umfang;
        kreise += '<circle cx="70" cy="70" r="' + r + '" fill="none" stroke="' + d.farbe + '" stroke-width="20" ' +
          'stroke-dasharray="' + len + " " + (umfang - len) + '" stroke-dashoffset="' + (-offset) + '" ' +
          'transform="rotate(-90 70 70)"><title>' + esc(d.label) + "</title></circle>";
        offset += len;
      });
    } else {
      kreise = '<circle cx="70" cy="70" r="' + r + '" fill="none" stroke="var(--surface-3)" stroke-width="20"/>';
    }

    var legende = daten.map(function (d) {
      return '<span class="k"><i style="background:' + d.farbe + '"></i>' + esc(d.label) +
        " <b>" + esc(formatter ? formatter(d.wert) : num(d.wert)) + "</b></span>";
    }).join("");

    return '<div class="row" style="gap:1.2rem;align-items:center;justify-content:center">' +
      '<svg width="140" height="140" viewBox="0 0 140 140">' + kreise +
        '<text x="70" y="66" text-anchor="middle" font-size="13" font-weight="700" fill="currentColor">' +
          esc(formatter ? formatter(gesamt) : num(gesamt)) + "</text>" +
        '<text x="70" y="84" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.6">Gesamt</text>' +
      "</svg></div>" +
      '<div class="chart-legend">' + legende + "</div>";
  }

  function saeulen(punkte, formatter) {
    var w = 100 / Math.max(punkte.length, 1);
    var max = Math.max.apply(null, punkte.map(function (p) { return p.wert; }).concat([1]));
    var balkenHtml = punkte.map(function (p, i) {
      var h = (p.wert / max) * 100;
      return '<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:4px">' +
        '<span style="font-size:0.68rem;color:var(--text-muted)">' + (p.wert ? esc(formatter ? formatter(p.wert) : p.wert) : "") + "</span>" +
        '<div style="width:70%;min-height:2px;height:' + Math.max(h, 2) + 'px;background:var(--accent);border-radius:4px 4px 0 0;opacity:' +
          (0.45 + 0.55 * (p.wert / max)) + '" title="' + esc(p.label + ": " + p.wert) + '"></div>' +
        '<span style="font-size:0.7rem;color:var(--text-muted)">' + esc(p.label) + "</span>" +
        "</div>";
    }).join("");
    return '<div style="display:flex;align-items:flex-end;gap:4px;height:150px">' + balkenHtml + "</div>" +
      (w ? "" : "");
  }

  function trichter(stufen) {
    var max = Math.max.apply(null, stufen.map(function (s) { return s.wert; }).concat([1]));
    return stufen.map(function (s) {
      var pct = Math.max(4, (s.wert / max) * 100);
      return '<div class="funnel-step">' +
        '<span class="nowrap muted">' + esc(s.label) + "</span>" +
        '<div class="funnel-bar" style="width:' + pct + "%;background:" + s.farbe + '">' + s.wert + "</div>" +
        "</div>";
    }).join("");
  }

  /* ---------- Download ---------- */
  function download(dateiname, inhalt, mime) {
    var blob = new Blob([inhalt], { type: (mime || "text/plain") + ";charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = dateiname;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  global.UI = {
    eur: eur, eurKurz: eurKurz, num: num, dez: dez,
    datum: datum, datumZeit: datumZeit, relativ: relativ,
    tageBis: tageBis, faelligText: faelligText,
    esc: esc, initialen: initialen, icon: icon, stagePill: stagePill,
    toast: toast, modal: modal, schliessen: schliessen, frage: frage,
    feld: feld, input: input, textarea: textarea, select: select,
    formWerte: formWerte, markiereFehler: markiereFehler,
    balken: balken, donut: donut, saeulen: saeulen, trichter: trichter,
    download: download
  };
})(window);
