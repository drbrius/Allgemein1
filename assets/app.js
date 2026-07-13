/* CalcMate — calculator logic (no dependencies) */
(function () {
  "use strict";

  var LANG = document.documentElement.lang || "en";
  var I18N = window.CALC_I18N || {};

  function fmt(n, digits) {
    if (!isFinite(n)) return I18N.error || "Error";
    return new Intl.NumberFormat(LANG, {
      maximumFractionDigits: digits === undefined ? 4 : digits
    }).format(n);
  }

  function parseNum(s) {
    if (typeof s !== "string") return NaN;
    s = s.trim().replace(/\s/g, "");
    if (s === "") return NaN;
    // Accept both comma and dot as decimal separator
    if (s.indexOf(",") !== -1 && s.indexOf(".") !== -1) {
      // Assume the last occurring symbol is the decimal separator
      if (s.lastIndexOf(",") > s.lastIndexOf(".")) {
        s = s.replace(/\./g, "").replace(",", ".");
      } else {
        s = s.replace(/,/g, "");
      }
    } else {
      s = s.replace(",", ".");
    }
    return parseFloat(s);
  }

  /* ---------- Expression evaluator (safe, no eval) ---------- */

  function tokenize(str) {
    str = str
      .replace(/×/g, "*")
      .replace(/÷/g, "/")
      .replace(/−/g, "-")
      .replace(/,/g, ".");
    var tokens = [];
    var i = 0;
    while (i < str.length) {
      var c = str[i];
      if (c === " ") { i++; continue; }
      if (/[0-9.]/.test(c)) {
        var j = i;
        while (j < str.length && /[0-9.]/.test(str[j])) j++;
        var num = parseFloat(str.slice(i, j));
        if (isNaN(num)) throw new Error("number");
        tokens.push({ type: "num", value: num });
        i = j;
        continue;
      }
      if ("+-*/()%".indexOf(c) !== -1) {
        tokens.push({ type: c });
        i++;
        continue;
      }
      throw new Error("char");
    }
    return tokens;
  }

  function toRpn(tokens) {
    var out = [];
    var ops = [];
    var prec = { "u-": 3, "*": 2, "/": 2, "+": 1, "-": 1 };
    var prev = null;
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (t.type === "num") {
        out.push(t);
      } else if (t.type === "%") {
        out.push(t); // postfix
      } else if (t.type === "(") {
        ops.push(t);
      } else if (t.type === ")") {
        while (ops.length && ops[ops.length - 1].type !== "(") out.push(ops.pop());
        if (!ops.length) throw new Error("paren");
        ops.pop();
      } else {
        var type = t.type;
        var unary = type === "-" &&
          (prev === null || (prev.type !== "num" && prev.type !== ")" && prev.type !== "%"));
        if (unary) type = "u-";
        while (
          ops.length &&
          ops[ops.length - 1].type !== "(" &&
          (prec[ops[ops.length - 1].type] > prec[type] ||
            (prec[ops[ops.length - 1].type] === prec[type] && type !== "u-"))
        ) {
          out.push(ops.pop());
        }
        ops.push({ type: type });
      }
      prev = t;
    }
    while (ops.length) {
      var op = ops.pop();
      if (op.type === "(") throw new Error("paren");
      out.push(op);
    }
    return out;
  }

  function evalRpn(rpn) {
    var st = [];
    for (var i = 0; i < rpn.length; i++) {
      var t = rpn[i];
      if (t.type === "num") {
        st.push(t.value);
      } else if (t.type === "%") {
        if (st.length < 1) throw new Error("stack");
        st.push(st.pop() / 100);
      } else if (t.type === "u-") {
        if (st.length < 1) throw new Error("stack");
        st.push(-st.pop());
      } else {
        if (st.length < 2) throw new Error("stack");
        var b = st.pop();
        var a = st.pop();
        var r;
        if (t.type === "+") r = a + b;
        else if (t.type === "-") r = a - b;
        else if (t.type === "*") r = a * b;
        else r = a / b;
        st.push(r);
      }
    }
    if (st.length !== 1) throw new Error("stack");
    return st[0];
  }

  function evaluate(expr) {
    var tokens = tokenize(expr);
    if (!tokens.length) return null;
    return evalRpn(toRpn(tokens));
  }

  /* ---------- Basic calculator keypad ---------- */

  var calc = document.querySelector("[data-calculator]");
  if (calc) {
    var display = calc.querySelector(".calc-display");

    function calcResult() {
      var expr = display.value;
      if (!expr.trim()) return;
      try {
        var result = evaluate(expr);
        if (result === null) return;
        if (!isFinite(result)) {
          display.value = I18N.error || "Error";
        } else {
          // Round away binary float noise, keep up to 10 significant digits
          display.value = String(parseFloat(result.toPrecision(12)));
        }
      } catch (e) {
        display.value = I18N.error || "Error";
      }
      display.focus();
    }

    calc.addEventListener("click", function (ev) {
      var btn = ev.target.closest("button[data-key]");
      if (!btn) return;
      var key = btn.getAttribute("data-key");
      if (display.value === (I18N.error || "Error")) display.value = "";
      if (key === "=") {
        calcResult();
      } else if (key === "C") {
        display.value = "";
        display.focus();
      } else if (key === "back") {
        display.value = display.value.slice(0, -1);
        display.focus();
      } else {
        display.value += key;
        display.focus();
      }
    });

    display.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" || ev.key === "=") {
        ev.preventDefault();
        calcResult();
      } else if (ev.key === "Escape") {
        display.value = "";
      }
    });

    // Only allow characters the evaluator understands
    display.addEventListener("input", function () {
      display.value = display.value.replace(/[^0-9+\-*/().,%×÷−\s]/g, "");
    });
  }

  /* ---------- Small form calculators ---------- */

  function val(form, name) {
    return parseNum(form.elements[name].value);
  }

  function setOut(form, name, text) {
    var el = form.querySelector('[data-out="' + name + '"]');
    if (el) el.textContent = text;
  }

  var handlers = {
    /* p % of x */
    "pct-of": function (f) {
      var p = val(f, "p"), x = val(f, "x");
      if (isNaN(p) || isNaN(x)) return "";
      return "= " + fmt((p / 100) * x);
    },
    /* x is what % of y */
    "pct-what": function (f) {
      var x = val(f, "x"), y = val(f, "y");
      if (isNaN(x) || isNaN(y) || y === 0) return "";
      return "= " + fmt((x / y) * 100) + " %";
    },
    /* % change from a to b */
    "pct-change": function (f) {
      var a = val(f, "a"), b = val(f, "b");
      if (isNaN(a) || isNaN(b) || a === 0) return "";
      var ch = ((b - a) / Math.abs(a)) * 100;
      return "= " + (ch > 0 ? "+" : "") + fmt(ch) + " %";
    },
    /* VAT */
    "vat": function (f) {
      var amount = val(f, "amount");
      var rate = val(f, "rate");
      if (isNaN(amount) || isNaN(rate) || rate < 0) {
        setOut(f, "net", "–"); setOut(f, "vat", "–"); setOut(f, "gross", "–");
        return;
      }
      var net, gross;
      if (f.elements.dir.value === "net2gross") {
        net = amount;
        gross = amount * (1 + rate / 100);
      } else {
        gross = amount;
        net = amount / (1 + rate / 100);
      }
      setOut(f, "net", fmt(net, 2));
      setOut(f, "vat", fmt(gross - net, 2));
      setOut(f, "gross", fmt(gross, 2));
    },
    /* Rule of three: a -> b, c -> x */
    "rule3": function (f) {
      var a = val(f, "a"), b = val(f, "b"), c = val(f, "c");
      if (isNaN(a) || isNaN(b) || isNaN(c)) return "";
      var inverse = f.elements.inverse.checked;
      var x;
      if (inverse) {
        if (c === 0) return "";
        x = (a * b) / c;
      } else {
        if (a === 0) return "";
        x = (b * c) / a;
      }
      return "X = " + fmt(x);
    },
    /* BMI */
    "bmi": function (f) {
      var w = val(f, "weight"), h = val(f, "height");
      if (isNaN(w) || isNaN(h) || w <= 0 || h <= 0) return "";
      var m = h / 100;
      var bmi = w / (m * m);
      var cat;
      if (bmi < 18.5) cat = I18N.bmi_under;
      else if (bmi < 25) cat = I18N.bmi_normal;
      else if (bmi < 30) cat = I18N.bmi_over;
      else cat = I18N.bmi_obese;
      return "BMI = " + fmt(bmi, 1) + " — " + cat;
    },
    /* Slope: horizontal length + height -> percent, angle, slope length */
    "slope": function (f) {
      var l = val(f, "len"), h = val(f, "height");
      if (isNaN(l) || isNaN(h) || l <= 0 || h < 0) {
        setOut(f, "percent", "–"); setOut(f, "angle", "–"); setOut(f, "hyp", "–");
        return;
      }
      setOut(f, "percent", fmt((h / l) * 100, 2) + " %");
      setOut(f, "angle", fmt(Math.atan2(h, l) * 180 / Math.PI, 2) + "°");
      setOut(f, "hyp", fmt(Math.sqrt(l * l + h * h), 2));
    },
    /* Compound interest */
    "interest": function (f) {
      var p = val(f, "principal"), r = val(f, "rate"), y = val(f, "years");
      if (isNaN(p) || isNaN(r) || isNaN(y) || y < 0) {
        setOut(f, "final", "–"); setOut(f, "earned", "–");
        return;
      }
      var final_ = p * Math.pow(1 + r / 100, y);
      setOut(f, "final", fmt(final_, 2));
      setOut(f, "earned", fmt(final_ - p, 2));
    }
  };

  document.querySelectorAll("form[data-calc]").forEach(function (form) {
    var kind = form.getAttribute("data-calc");
    var handler = handlers[kind];
    if (!handler) return;
    var output = form.querySelector(".result");

    function update() {
      var text = handler(form);
      if (output && text !== undefined) output.textContent = text || "";
    }

    form.addEventListener("input", update);
    form.addEventListener("change", update);
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      update();
    });
    update();
  });

  /* Remember chosen language for the root landing page */
  try {
    var m = location.pathname.match(/\/(de|en|fr|it)\/(?:index\.html)?$/);
    if (m) localStorage.setItem("calcmate-lang", m[1]);
  } catch (e) { /* storage unavailable */ }
})();
