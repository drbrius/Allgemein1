# -*- coding: utf-8 -*-
"""German content for CalcMate. Consumed by tools/build.py."""

SITE = {
    "title": "Kostenlose Online-Rechner – Prozent, MwSt, Kredit, BMI &amp; mehr | CalcMate",
    "desc": "Kostenlose Online-Rechner ohne Anmeldung: Prozentrechner, MwSt-Rechner, Rabatt, Kredit, Spritkosten, Trinkgeld, Tagerechner, Dreisatz, Gefälle, BMI und Zinseszins.",
    "app_name": "CalcMate – Kostenlose Online-Rechner",
    "app_desc": "Kostenlose Online-Rechner ohne Anmeldung: Taschenrechner, Prozentrechner, Mehrwertsteuer-Rechner, Rabatt-Rechner, Dreisatz, Gefälle, BMI, Zinseszins, Kredit, Spritkosten, Trinkgeld und Tagerechner.",
    "hub_h1": "Kostenlose Online-Rechner – schnell, modern, ohne Anmeldung",
    "hub_intro": "Alltagsrechnungen einfach gemacht: Prozente, Mehrwertsteuer, Rabatt, Kredit, Spritkosten, BMI, Zinseszins, Tage zwischen zwei Daten und mehr – alles gratis, direkt im Browser.",
    "home": "Startseite",
    "faq_title": "Häufige Fragen",
    "related_title": "Passende Rechner",
    "lang_nav_label": "Sprachen",
    "footer": "© 2026 CalcMate – kostenlose Online-Rechner. Alle Ergebnisse ohne Gewähr.",
    "hub_faqs": [
        ("Sind diese Online-Rechner kostenlos?",
         "Ja, alle Rechner auf CalcMate sind völlig kostenlos. Es gibt keine Registrierung, keinen Login und keine versteckten Kosten – einfach Seite öffnen und losrechnen."),
        ("Wie berechne ich einen Prozentwert?",
         "Multipliziere den Grundwert mit dem Prozentsatz und teile durch 100. Beispiel: 20 % von 150 sind 150 × 20 ÷ 100 = 30. Unser Prozentrechner erledigt das sofort für dich."),
        ("Wie wird die Mehrwertsteuer berechnet?",
         "Um die MwSt aufzuschlagen, multipliziere den Nettopreis mit (1 + Steuersatz ÷ 100). Um sie aus einem Bruttopreis herauszurechnen, teile durch denselben Faktor. Der MwSt-Rechner beherrscht beide Richtungen."),
        ("Wie wird die monatliche Kreditrate berechnet?",
         "Bei einem Annuitätenkredit gilt: Rate = Kreditbetrag × Monatszins ÷ (1 − (1 + Monatszins)^−Monate). Der Kreditrechner zeigt dir Monatsrate, Gesamtzahlung und Zinskosten auf einen Blick."),
        ("Wie wird der BMI berechnet?",
         "Der Body-Mass-Index ist das Gewicht in Kilogramm geteilt durch das Quadrat der Körpergröße in Metern: BMI = kg / m². Ein BMI zwischen 18,5 und 25 gilt als Normalgewicht."),
    ],
    "i18n": {
        "error": "Fehler",
        "bmi_label": "BMI",
        "bmi_under": "Untergewicht",
        "bmi_normal": "Normalgewicht",
        "bmi_over": "Übergewicht",
        "bmi_obese": "Adipositas",
        "weeks": "Wochen",
        "days": "Tage",
    },
}

CALCS = {

    "calculator": {
        "slug": "taschenrechner",
        "name": "Taschenrechner",
        "title": "Taschenrechner online – kostenlos &amp; ohne Anmeldung | CalcMate",
        "desc": "Kostenloser Online-Taschenrechner mit Klammern und Prozent: addieren, subtrahieren, multiplizieren und dividieren – direkt im Browser, ohne Anmeldung.",
        "h1": "Online-Taschenrechner",
        "card": "Grundrechenarten mit Klammern und Prozent – direkt im Browser.",
        "intro": "Ein kostenloser Taschenrechner für Addition, Subtraktion, Multiplikation und Division – mit Klammern und Prozent. Tippe einen Ausdruck ein oder nutze die Tasten und drücke <kbd>=</kbd> oder Enter.",
        "form": """\
<div class="calculator" data-calculator>
  <input class="calc-display" type="text" inputmode="decimal" aria-label="Anzeige des Taschenrechners" placeholder="0" autocomplete="off">
  <div class="calc-keys">
    <button type="button" class="danger" data-key="C">C</button>
    <button type="button" class="op" data-key="(">(</button>
    <button type="button" class="op" data-key=")">)</button>
    <button type="button" class="danger" data-key="back">⌫</button>
    <button type="button" data-key="7">7</button>
    <button type="button" data-key="8">8</button>
    <button type="button" data-key="9">9</button>
    <button type="button" class="op" data-key="÷">÷</button>
    <button type="button" data-key="4">4</button>
    <button type="button" data-key="5">5</button>
    <button type="button" data-key="6">6</button>
    <button type="button" class="op" data-key="×">×</button>
    <button type="button" data-key="1">1</button>
    <button type="button" data-key="2">2</button>
    <button type="button" data-key="3">3</button>
    <button type="button" class="op" data-key="−">−</button>
    <button type="button" data-key="0">0</button>
    <button type="button" data-key=",">,</button>
    <button type="button" class="op" data-key="%">%</button>
    <button type="button" class="op" data-key="+">+</button>
    <button type="button" class="equals" data-key="=">=</button>
  </div>
</div>""",
        "seo": """\
<h2>So funktioniert der Online-Taschenrechner</h2>
<p>Der Rechner beherrscht die vier Grundrechenarten, Klammern und Prozent und hält sich dabei an die Regel „Punkt vor Strich“: Multiplikation und Division werden vor Addition und Subtraktion ausgeführt, Klammern haben Vorrang. Du kannst komplette Ausdrücke eintippen und erst am Ende auswerten lassen.</p>
<p class="formula">(12 + 8) × 2,5 = 50&nbsp;&nbsp;·&nbsp;&nbsp;200 − 15 % = 200 − 0,15 × 200 = 170</p>
<p>Die Prozent-Taste wandelt die zuvor eingegebene Zahl in ein Hundertstel um: 15 % wird zu 0,15. So lassen sich Aufschläge und Abschläge direkt im Ausdruck rechnen. Als Dezimaltrennzeichen funktionieren Komma und Punkt gleichermaßen.</p>""",
        "faqs": [
            ("Beachtet der Rechner Punkt-vor-Strich?",
             "Ja. Multiplikation und Division werden vor Addition und Subtraktion ausgewertet, und Klammern haben immer Vorrang. 2 + 3 × 4 ergibt also 14, während (2 + 3) × 4 gleich 20 ist."),
            ("Wie funktioniert die Prozent-Taste?",
             "Die %-Taste teilt die davor stehende Zahl durch 100. Aus 50 % wird 0,5. So kannst du zum Beispiel 80 × 25 % eingeben und erhältst 20."),
            ("Kann ich die Tastatur benutzen?",
             "Ja. Klicke in das Anzeigefeld und tippe deinen Ausdruck direkt ein – Ziffern, + − × ÷ (auch * und /), Klammern und Komma. Mit Enter oder = wird gerechnet, Escape leert die Anzeige."),
        ],
    },

    "percentage": {
        "slug": "prozentrechner",
        "name": "Prozentrechner",
        "title": "Prozentrechner – Prozente online berechnen | CalcMate",
        "desc": "Prozentrechner online: Prozentwert, Prozentsatz und prozentuale Veränderung berechnen – mit Formeln und Beispielen. Kostenlos und ohne Anmeldung.",
        "h1": "Prozentrechner",
        "card": "Prozentwert, Prozentsatz und prozentuale Veränderung berechnen.",
        "intro": "Prozente online berechnen: den Prozentwert eines Betrags ermitteln, herausfinden, wie viel Prozent eine Zahl von einer anderen ist, oder die prozentuale Zu- bzw. Abnahme zwischen zwei Werten bestimmen.",
        "form": """\
<div class="subform">
  <h3>Wie viel sind X % von einem Wert?</h3>
  <form class="calc-form" data-calc="pct-of" novalidate>
    <div class="fields">
      <label>Prozentsatz (%)<input type="text" inputmode="decimal" name="p" placeholder="20"></label>
      <label>Grundwert<input type="text" inputmode="decimal" name="x" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>X ist wie viel Prozent von Y?</h3>
  <form class="calc-form" data-calc="pct-what" novalidate>
    <div class="fields">
      <label>Wert X<input type="text" inputmode="decimal" name="x" placeholder="30"></label>
      <label>Grundwert Y<input type="text" inputmode="decimal" name="y" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>Prozentuale Veränderung von A nach B</h3>
  <form class="calc-form" data-calc="pct-change" novalidate>
    <div class="fields">
      <label>Ausgangswert A<input type="text" inputmode="decimal" name="a" placeholder="100"></label>
      <label>Neuer Wert B<input type="text" inputmode="decimal" name="b" placeholder="120"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>""",
        "seo": """\
<h2>Prozentrechnung: die drei Grundformeln</h2>
<p>Fast jede Prozentaufgabe lässt sich auf drei Fragen zurückführen: Wie groß ist der Prozentwert? Wie hoch ist der Prozentsatz? Und wie stark hat sich ein Wert prozentual verändert?</p>
<p class="formula">Prozentwert = Grundwert × Prozentsatz ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;Prozentsatz = Prozentwert ÷ Grundwert × 100</p>
<p>Beispiele: 20 % von 150 sind 150 × 20 ÷ 100 = 30. Die Zahl 30 entspricht 30 ÷ 150 × 100 = 20 % von 150. Und steigt ein Preis von 100 € auf 120 €, beträgt die Veränderung (120 − 100) ÷ 100 × 100 = +20 %.</p>
<p>Achtung bei Auf- und Abschlägen: Ein Anstieg um 20 % und ein anschließender Rückgang um 20 % führen nicht zum Ausgangswert zurück, denn der zweite Prozentsatz bezieht sich auf den neuen, höheren Grundwert (100 → 120 → 96).</p>""",
        "faqs": [
            ("Wie berechne ich einen Prozentwert?",
             "Multipliziere den Grundwert mit dem Prozentsatz und teile durch 100. Beispiel: 20 % von 150 sind 150 × 20 ÷ 100 = 30."),
            ("Wie finde ich heraus, wie viel Prozent X von Y ist?",
             "Teile X durch Y und multipliziere mit 100. Beispiel: 30 von 150 sind 30 ÷ 150 × 100 = 20 %."),
            ("Wie berechnet man die prozentuale Veränderung?",
             "Ziehe den Ausgangswert vom neuen Wert ab, teile durch den Ausgangswert und multipliziere mit 100: (B − A) ÷ A × 100. Von 100 auf 120 sind das +20 %, von 120 auf 100 dagegen −16,67 %."),
        ],
    },

    "vat": {
        "slug": "mehrwertsteuer-rechner",
        "name": "MwSt-Rechner",
        "title": "Mehrwertsteuer-Rechner – MwSt berechnen (netto ↔ brutto) | CalcMate",
        "desc": "MwSt-Rechner online: Mehrwertsteuer aufschlagen oder herausrechnen – netto zu brutto und brutto zu netto, mit 19 %, 7 % oder beliebigem Steuersatz.",
        "h1": "Mehrwertsteuer-Rechner",
        "card": "MwSt aufschlagen oder herausrechnen – netto ↔ brutto.",
        "intro": "Mehrwertsteuer in einem Schritt aufschlagen oder herausrechnen: von netto zu brutto oder von brutto zu netto mit beliebigem Steuersatz. In Deutschland gilt der Regelsatz von 19 % (ermäßigt 7 %), in Österreich 20 % und in der Schweiz 8,1 %.",
        "form": """\
<form class="calc-form" data-calc="vat" novalidate>
  <div class="fields">
    <label>Betrag<input type="text" inputmode="decimal" name="amount" placeholder="100"></label>
    <label>Steuersatz (%)<input type="text" inputmode="decimal" name="rate" value="19"></label>
  </div>
  <fieldset>
    <label><input type="radio" name="dir" value="net2gross" checked> Netto → Brutto (MwSt aufschlagen)</label>
    <label><input type="radio" name="dir" value="gross2net"> Brutto → Netto (MwSt herausrechnen)</label>
  </fieldset>
  <dl class="result-list">
    <div><dt>Netto</dt><dd data-out="net">–</dd></div>
    <div><dt>MwSt</dt><dd data-out="vat">–</dd></div>
    <div><dt>Brutto</dt><dd data-out="gross">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>MwSt berechnen: die Formeln</h2>
<p>Vom Nettobetrag zum Bruttobetrag führt ein einziger Faktor. Bei 19 % Mehrwertsteuer ist das 1,19 – beim ermäßigten Satz von 7 % entsprechend 1,07.</p>
<p class="formula">Brutto = Netto × (1 + Satz ÷ 100)&nbsp;&nbsp;·&nbsp;&nbsp;Netto = Brutto ÷ (1 + Satz ÷ 100)</p>
<p>Beispiel: 100 € netto ergeben bei 19 % genau 119 € brutto, die enthaltene MwSt beträgt 19 €. Umgekehrt stecken in 119 € brutto 119 ÷ 1,19 = 100 € netto. Ein häufiger Fehler ist, aus dem Bruttobetrag einfach 19 % abzuziehen – das ergibt zu wenig, weil sich die 19 % auf den Nettobetrag beziehen.</p>
<p>Der ermäßigte Satz von 7 % gilt in Deutschland unter anderem für Lebensmittel, Bücher, Zeitungen und den öffentlichen Nahverkehr. In Österreich beträgt der Regelsatz 20 % (ermäßigt 10 % bzw. 13 %), in der Schweiz 8,1 % (reduziert 2,6 %).</p>""",
        "faqs": [
            ("Wie wird die Mehrwertsteuer berechnet?",
             "Um die MwSt aufzuschlagen, multipliziere den Nettopreis mit (1 + Steuersatz ÷ 100) – bei 19 % also mit 1,19. Um sie aus einem Bruttopreis herauszurechnen, teile durch denselben Faktor."),
            ("Wie rechne ich die MwSt aus einem Bruttobetrag heraus?",
             "Teile den Bruttobetrag durch 1,19 (bei 19 %) bzw. 1,07 (bei 7 %). Beispiel: 119 € brutto ÷ 1,19 = 100 € netto, die MwSt beträgt 19 €. Einfach 19 % vom Brutto abzuziehen wäre falsch."),
            ("Welche Mehrwertsteuersätze gelten in Deutschland?",
             "Der Regelsatz beträgt 19 %. Der ermäßigte Satz von 7 % gilt z. B. für Lebensmittel, Bücher, Zeitungen und den öffentlichen Nahverkehr."),
        ],
    },

    "discount": {
        "slug": "rabatt-rechner",
        "name": "Rabatt-Rechner",
        "title": "Rabatt-Rechner – Preis nach Rabatt berechnen | CalcMate",
        "desc": "Rabatt online berechnen: Wie viel sparst du bei X % Rabatt und was kostet der Artikel danach? Kostenloser Rabattrechner mit Formel und Beispielen.",
        "h1": "Rabatt-Rechner",
        "card": "Ersparnis und neuen Preis bei X % Rabatt berechnen.",
        "intro": "Berechne in Sekunden, wie viel du bei einem Rabatt sparst und was der Artikel nach Abzug kostet: einfach Preis und Rabatt in Prozent eingeben.",
        "form": """\
<form class="calc-form" data-calc="discount" novalidate>
  <div class="fields">
    <label>Preis<input type="text" inputmode="decimal" name="price" placeholder="80"></label>
    <label>Rabatt (%)<input type="text" inputmode="decimal" name="pct" placeholder="25"></label>
  </div>
  <dl class="result-list">
    <div><dt>Ersparnis</dt><dd data-out="saved">–</dd></div>
    <div><dt>Neuer Preis</dt><dd data-out="final">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Rabatt berechnen: so geht’s</h2>
<p>Der Rabatt ist ein prozentualer Abschlag auf den ursprünglichen Preis. Die Ersparnis und der neue Preis ergeben sich aus zwei einfachen Formeln:</p>
<p class="formula">Ersparnis = Preis × Rabatt ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;Neuer Preis = Preis − Ersparnis</p>
<p>Beispiel: Ein Pullover kostet 80 € und ist um 25 % reduziert. Die Ersparnis beträgt 80 × 25 ÷ 100 = 20 €, der neue Preis 60 €. Praktischer Kopfrechen-Trick: 25 % sind ein Viertel, 50 % die Hälfte, 10 % ein Zehntel des Preises.</p>
<p>Vorsicht bei gestaffelten Rabatten: „20 % + 10 %“ sind nicht 30 %. Der zweite Rabatt wird auf den bereits reduzierten Preis gewährt – aus 100 € werden erst 80 €, dann 72 €, also insgesamt 28 % Nachlass.</p>""",
        "faqs": [
            ("Wie berechne ich einen Rabatt?",
             "Multipliziere den Preis mit dem Rabatt in Prozent und teile durch 100 – das ist die Ersparnis. Der neue Preis ist der alte Preis minus Ersparnis. Beispiel: 80 € mit 25 % Rabatt = 20 € gespart, 60 € zu zahlen."),
            ("Was kostet ein Artikel nach 20 % Rabatt?",
             "Multipliziere den Preis mit 0,8. Beispiel: 50 € × 0,8 = 40 €. Allgemein gilt: neuer Preis = alter Preis × (1 − Rabatt ÷ 100)."),
            ("Wie funktionieren gestaffelte Rabatte, z. B. 20 % + 10 %?",
             "Die Rabatte werden nacheinander angewendet, nicht addiert. Aus 100 € werden mit 20 % erst 80 €, mit weiteren 10 % dann 72 €. Der Gesamtrabatt beträgt also 28 %, nicht 30 %."),
        ],
    },

    "rule3": {
        "slug": "dreisatzrechner",
        "name": "Dreisatzrechner",
        "title": "Dreisatzrechner – Dreisatz online lösen | CalcMate",
        "desc": "Dreisatz online berechnen: proportional und antiproportional. Wenn A dem Wert B entspricht, was entspricht C? Kostenlos, mit Formel und Beispielen.",
        "h1": "Dreisatzrechner",
        "card": "Proportionale und antiproportionale Verhältnisse lösen.",
        "intro": "Verhältnisse in Sekunden lösen: Wenn A dem Wert B entspricht, was entspricht dann C? Ideal für Rezepte, Preise, Geschwindigkeiten und Einheiten. Für umgekehrt proportionale Zusammenhänge (mehr Arbeiter → weniger Zeit) einfach das Kästchen anhaken.",
        "form": """\
<form class="calc-form" data-calc="rule3" novalidate>
  <div class="fields">
    <label>A<input type="text" inputmode="decimal" name="a" placeholder="4"></label>
    <label>entspricht B<input type="text" inputmode="decimal" name="b" placeholder="12"></label>
    <label>C<input type="text" inputmode="decimal" name="c" placeholder="7"></label>
  </div>
  <fieldset>
    <label class="check"><input type="checkbox" name="inverse"> Umgekehrt proportional (antiproportional)</label>
  </fieldset>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>So funktioniert der Dreisatz</h2>
<p>Der Dreisatz führt eine bekannte Beziehung („A entspricht B“) auf eine Einheit zurück und rechnet dann auf die gesuchte Menge hoch. Beim proportionalen Dreisatz wachsen beide Größen gemeinsam, beim antiproportionalen Dreisatz sinkt die eine, wenn die andere steigt.</p>
<p class="formula">proportional: X = B × C ÷ A&nbsp;&nbsp;·&nbsp;&nbsp;antiproportional: X = A × B ÷ C</p>
<p>Beispiel proportional: 4 Äpfel kosten 12 €. Was kosten 7 Äpfel? X = 12 × 7 ÷ 4 = 21 €. Beispiel antiproportional: 4 Maler brauchen 12 Stunden. Wie lange brauchen 6 Maler? X = 4 × 12 ÷ 6 = 8 Stunden.</p>""",
        "faqs": [
            ("Wie funktioniert der Dreisatz?",
             "Rechne zuerst auf eine Einheit herunter und dann auf die gesuchte Menge hoch. Kosten 4 Äpfel 12 €, kostet 1 Apfel 3 € und 7 Äpfel kosten 21 €. Als Formel: X = B × C ÷ A."),
            ("Was ist ein umgekehrter (antiproportionaler) Dreisatz?",
             "Hier sinkt die eine Größe, wenn die andere steigt – etwa mehr Arbeiter, weniger Zeit. Die Formel lautet dann X = A × B ÷ C: Brauchen 4 Maler 12 Stunden, schaffen es 6 Maler in 8 Stunden."),
            ("Wofür braucht man den Dreisatz im Alltag?",
             "Für Rezepte auf andere Portionszahlen, Preisvergleiche pro Kilo oder Liter, Umrechnung von Geschwindigkeiten und Einheiten, Materialbedarf oder Arbeitszeitplanung – überall dort, wo zwei Größen in einem festen Verhältnis stehen."),
        ],
    },

    "slope": {
        "slug": "gefaelle-rechner",
        "name": "Gefälle-Rechner",
        "title": "Gefälle-Rechner – Gefälle in Prozent &amp; Grad berechnen | CalcMate",
        "desc": "Gefälle und Steigung online berechnen: aus Länge und Höhe das Gefälle in Prozent und Grad ermitteln oder Prozent und Grad umrechnen. Mit Dreiecksskizze.",
        "h1": "Gefälle-Rechner",
        "card": "Gefälle und Steigung in Prozent und Grad – mit Skizze.",
        "intro": "Berechne Gefälle bzw. Steigung in Prozent und Grad – aus der horizontalen Länge und der Höhe (dem Höhenunterschied). Alternativ kannst du das Gefälle direkt in Prozent oder Grad eingeben und umrechnen. Praktisch für Dach, Rampe, Straße oder Abwasserrohr.",
        "form": """\
<svg class="slope-figure" viewBox="0 0 360 190" role="img" aria-label="Rechtwinkliges Dreieck: horizontale Länge unten, Höhe rechts, Winkel α links">
  <polygon points="30,160 310,160 310,50" fill="#eef2fc"/>
  <line x1="30" y1="160" x2="310" y2="160" stroke="#1c2430" stroke-width="2"/>
  <line x1="310" y1="160" x2="310" y2="50" stroke="#1c2430" stroke-width="2"/>
  <line x1="30" y1="160" x2="310" y2="50" stroke="#4f6df5" stroke-width="2.5"/>
  <path d="M 296 160 L 296 146 L 310 146" fill="none" stroke="#9aa3b5" stroke-width="1.5"/>
  <path d="M 64 160 A 34 34 0 0 0 61.6 147.6" fill="none" stroke="#6b7385" stroke-width="1.5"/>
  <text x="78" y="156" font-size="14" fill="#6b7385">α</text>
  <text x="170" y="182" font-size="14" fill="#6b7385" text-anchor="middle">Länge</text>
  <text x="318" y="110" font-size="14" fill="#6b7385">Höhe</text>
</svg>
<form class="calc-form" data-calc="slope" novalidate>
  <fieldset>
    <label><input type="radio" name="mode" value="lh" checked> Länge &amp; Höhe</label>
    <label><input type="radio" name="mode" value="pct"> Gefälle in %</label>
    <label><input type="radio" name="mode" value="deg"> Winkel in Grad</label>
  </fieldset>
  <div class="fields">
    <label data-field="pct" hidden>Gefälle (%)<input type="text" inputmode="decimal" name="pct" placeholder="12"></label>
    <label data-field="deg" hidden>Winkel (°)<input type="text" inputmode="decimal" name="deg" placeholder="6,84"></label>
    <label data-field="len">Länge (m)<input type="text" inputmode="decimal" name="len" placeholder="100"></label>
    <label data-field="height">Höhe (m)<input type="text" inputmode="decimal" name="height" placeholder="12"></label>
  </div>
  <dl class="result-list">
    <div><dt>Gefälle</dt><dd data-out="percent">–</dd></div>
    <div><dt>Winkel α</dt><dd data-out="angle">–</dd></div>
    <div><dt>Höhe (m)</dt><dd data-out="height">–</dd></div>
    <div><dt>Schräglänge (m)</dt><dd data-out="hyp">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Gefälle in Prozent und Grad</h2>
<p>Das Gefälle in Prozent gibt an, wie viele Meter Höhenunterschied auf 100 Meter horizontale Länge entfallen. Der Winkel ergibt sich über den Arkustangens desselben Verhältnisses.</p>
<p class="formula">Gefälle (%) = Höhe ÷ Länge × 100&nbsp;&nbsp;·&nbsp;&nbsp;Winkel α = arctan(Höhe ÷ Länge)</p>
<p>Beispiel: 12 m Höhenunterschied auf 100 m Länge ergeben 12 % Gefälle und einen Winkel von etwa 6,84°. Die Schräglänge (Hypotenuse) folgt aus dem Satz des Pythagoras: √(100² + 12²) ≈ 100,72 m.</p>
<p>Typische Richtwerte: Abwasserrohre benötigen mindestens 1–2 % Gefälle, barrierefreie Rampen dürfen höchstens 6 % Steigung haben, und 100 % Gefälle entsprechen genau 45°.</p>""",
        "faqs": [
            ("Wie berechnet man ein Gefälle in Prozent?",
             "Teile die Höhe (den Höhenunterschied) durch die horizontale Länge und multipliziere mit 100: Gefälle (%) = Höhe ÷ Länge × 100. Beispiel: 12 m Höhe auf 100 m Länge ergeben ein Gefälle von 12 %."),
            ("Wie rechnet man Gefälle-Prozent in Grad um?",
             "Der Winkel ist der Arkustangens des Verhältnisses: α = arctan(Prozent ÷ 100). 12 % entsprechen arctan(0,12) ≈ 6,84°, 100 % entsprechen genau 45°."),
            ("Was bedeutet 100 % Gefälle?",
             "Bei 100 % Gefälle ist der Höhenunterschied genauso groß wie die horizontale Strecke – das entspricht einem Winkel von 45°, nicht etwa einer senkrechten Wand."),
        ],
    },

    "bmi": {
        "slug": "bmi-rechner",
        "name": "BMI-Rechner",
        "title": "BMI-Rechner – Body-Mass-Index berechnen | CalcMate",
        "desc": "BMI online berechnen: Body-Mass-Index aus Gewicht und Größe inklusive Einordnung von Untergewicht bis Adipositas. Kostenlos und ohne Anmeldung.",
        "h1": "BMI-Rechner",
        "card": "Body-Mass-Index aus Gewicht und Größe – mit Einordnung.",
        "intro": "Berechne deinen Body-Mass-Index (BMI) aus Gewicht und Körpergröße. Der BMI ist ein schneller Richtwert für ein gesundes Körpergewicht: Werte zwischen 18,5 und 25 gelten bei Erwachsenen als Normalgewicht.",
        "form": """\
<form class="calc-form" data-calc="bmi" novalidate>
  <div class="fields">
    <label>Gewicht (kg)<input type="text" inputmode="decimal" name="weight" placeholder="70"></label>
    <label>Größe (cm)<input type="text" inputmode="decimal" name="height" placeholder="175"></label>
  </div>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>So wird der BMI berechnet</h2>
<p>Der Body-Mass-Index setzt das Körpergewicht ins Verhältnis zur Körpergröße. Er wurde von der Weltgesundheitsorganisation (WHO) als grober Richtwert für Erwachsene definiert.</p>
<p class="formula">BMI = Gewicht (kg) ÷ Größe (m)²</p>
<p>Beispiel: 70 kg bei 1,75 m ergeben 70 ÷ (1,75 × 1,75) ≈ 22,9 – Normalgewicht. Die WHO-Einteilung: unter 18,5 Untergewicht, 18,5–24,9 Normalgewicht, 25–29,9 Übergewicht, ab 30 Adipositas.</p>
<p>Der BMI unterscheidet nicht zwischen Muskel- und Fettmasse: Sportliche Menschen mit viel Muskulatur können einen hohen BMI bei niedrigem Körperfettanteil haben. Für Kinder, Schwangere und ältere Menschen gelten eigene Referenzwerte – im Zweifel ärztlichen Rat einholen.</p>""",
        "faqs": [
            ("Wie wird der BMI berechnet?",
             "Der Body-Mass-Index ist das Gewicht in Kilogramm geteilt durch das Quadrat der Körpergröße in Metern: BMI = kg / m². Beispiel: 70 kg bei 1,75 m ergeben einen BMI von etwa 22,9."),
            ("Welcher BMI gilt als normal?",
             "Bei Erwachsenen gilt laut WHO ein BMI von 18,5 bis 24,9 als Normalgewicht. Unter 18,5 spricht man von Untergewicht, ab 25 von Übergewicht und ab 30 von Adipositas."),
            ("Wie aussagekräftig ist der BMI?",
             "Der BMI ist nur ein grober Richtwert. Er unterscheidet nicht zwischen Muskel- und Fettmasse und berücksichtigt weder Alter noch Geschlecht oder Statur. Für eine fundierte Einschätzung sind zusätzliche Messwerte und ärztlicher Rat sinnvoll."),
        ],
    },

    "interest": {
        "slug": "zinseszinsrechner",
        "name": "Zinseszinsrechner",
        "title": "Zinseszinsrechner – Zinseszins online berechnen | CalcMate",
        "desc": "Zinseszins online berechnen: Endkapital und Zinsertrag aus Startkapital, Zinssatz und Laufzeit – mit Formel, Beispiel und 72er-Regel. Kostenlos.",
        "h1": "Zinseszinsrechner",
        "card": "Endkapital und Zinsertrag mit Zinseszins berechnen.",
        "intro": "So wächst dein Erspartes: Gib Startkapital, jährlichen Zinssatz und Laufzeit in Jahren ein und berechne das Endkapital inklusive Zinseszins.",
        "form": """\
<form class="calc-form" data-calc="interest" novalidate>
  <div class="fields">
    <label>Startkapital<input type="text" inputmode="decimal" name="principal" placeholder="10000"></label>
    <label>Zinssatz (% p.a.)<input type="text" inputmode="decimal" name="rate" placeholder="3"></label>
    <label>Laufzeit (Jahre)<input type="text" inputmode="decimal" name="years" placeholder="10"></label>
  </div>
  <dl class="result-list">
    <div><dt>Endkapital</dt><dd data-out="final">–</dd></div>
    <div><dt>Zinsertrag</dt><dd data-out="earned">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Die Zinseszinsformel</h2>
<p>Beim Zinseszins werden die Zinsen am Ende jeder Periode dem Kapital zugeschlagen und in der Folgeperiode mitverzinst. Dadurch wächst das Kapital nicht linear, sondern exponentiell.</p>
<p class="formula">Endkapital = Startkapital × (1 + Zinssatz ÷ 100)^Jahre</p>
<p>Beispiel: 10.000 € bei 3 % pro Jahr ergeben nach 10 Jahren 10.000 × 1,03¹⁰ ≈ 13.439,16 € – der Zinsertrag beträgt rund 3.439 €. Ohne Zinseszins (nur einfache Zinsen) wären es lediglich 3.000 €.</p>
<p>Faustregel zur Verdopplung („72er-Regel“): Teile 72 durch den Zinssatz, und du erhältst die ungefähre Anzahl Jahre bis zur Kapitalverdopplung. Bei 6 % dauert es also rund 12 Jahre.</p>""",
        "faqs": [
            ("Was ist der Zinseszinseffekt?",
             "Zinsen werden dem Kapital gutgeschrieben und in den Folgejahren mitverzinst. Das Kapital wächst dadurch exponentiell: Aus 10.000 € werden bei 3 % nach 10 Jahren rund 13.439 € statt 13.000 € mit einfachen Zinsen."),
            ("Wie lautet die Zinseszinsformel?",
             "Endkapital = Startkapital × (1 + Zinssatz ÷ 100) hoch Anzahl der Jahre. Beispiel: 10.000 € × 1,03¹⁰ ≈ 13.439,16 €."),
            ("Wie lange dauert es, bis sich mein Kapital verdoppelt?",
             "Nutze die 72er-Regel: 72 geteilt durch den Zinssatz ergibt näherungsweise die Jahre bis zur Verdopplung. Bei 6 % sind es etwa 12 Jahre, bei 3 % etwa 24 Jahre."),
        ],
    },

    "loan": {
        "slug": "kreditrechner",
        "name": "Kreditrechner",
        "title": "Kreditrechner – monatliche Rate berechnen | CalcMate",
        "desc": "Kreditrechner online: monatliche Rate, Gesamtzahlung und Zinskosten für einen Annuitätenkredit aus Kreditbetrag, Zinssatz und Laufzeit berechnen.",
        "h1": "Kreditrechner",
        "card": "Monatliche Rate, Gesamtzahlung und Zinskosten eines Kredits.",
        "intro": "Berechne die monatliche Rate für einen Kredit mit fester Verzinsung (Annuitätendarlehen): Kreditbetrag, jährlichen Zinssatz und Laufzeit eingeben – der Rechner zeigt Monatsrate, Gesamtzahlung und Zinskosten.",
        "form": """\
<form class="calc-form" data-calc="loan" novalidate>
  <div class="fields">
    <label>Kreditbetrag<input type="text" inputmode="decimal" name="principal" placeholder="20000"></label>
    <label>Zinssatz (% p.a.)<input type="text" inputmode="decimal" name="rate" placeholder="5"></label>
    <label>Laufzeit (Jahre)<input type="text" inputmode="decimal" name="years" placeholder="5"></label>
  </div>
  <dl class="result-list">
    <div><dt>Monatliche Rate</dt><dd data-out="monthly">–</dd></div>
    <div><dt>Gesamtzahlung</dt><dd data-out="total">–</dd></div>
    <div><dt>Zinskosten</dt><dd data-out="interest">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>So wird die Kreditrate berechnet</h2>
<p>Bei einem Annuitätendarlehen bleibt die monatliche Rate über die gesamte Laufzeit konstant. Sie besteht aus einem Zins- und einem Tilgungsanteil; mit jeder Zahlung sinkt die Restschuld, der Zinsanteil wird kleiner und der Tilgungsanteil größer.</p>
<p class="formula">Rate = Kreditbetrag × i ÷ (1 − (1 + i)^−n)&nbsp;&nbsp;mit&nbsp;&nbsp;i = Jahreszins ÷ 12 ÷ 100, n = Monate</p>
<p>Beispiel: 20.000 € zu 5 % Zinsen über 5 Jahre (60 Monatsraten) ergeben eine Rate von etwa 377,42 €. Insgesamt zahlst du rund 22.645 € zurück – die Zinskosten betragen also etwa 2.645 €.</p>
<p>Hinweis: Der Rechner arbeitet mit dem nominalen Sollzins. Banken müssen zusätzlich den effektiven Jahreszins ausweisen, der Nebenkosten einrechnet und Angebote vergleichbar macht. Kürzere Laufzeiten bedeuten höhere Raten, aber deutlich geringere Gesamtzinskosten.</p>""",
        "faqs": [
            ("Wie wird die monatliche Kreditrate berechnet?",
             "Mit der Annuitätenformel: Rate = Kreditbetrag × Monatszins ÷ (1 − (1 + Monatszins)^−Monate). Beispiel: 20.000 € zu 5 % über 5 Jahre ergeben rund 377,42 € pro Monat."),
            ("Was ist der Unterschied zwischen Sollzins und Effektivzins?",
             "Der Sollzins ist der reine Zins auf die Restschuld. Der effektive Jahreszins enthält zusätzlich Nebenkosten und die Verrechnungstermine und eignet sich deshalb besser für den Vergleich verschiedener Kreditangebote."),
            ("Wie kann ich die Zinskosten eines Kredits senken?",
             "Kürzere Laufzeit wählen, Sondertilgungen nutzen, Angebote über den Effektivzins vergleichen und nur so viel aufnehmen, wie wirklich nötig. Schon ein halber Prozentpunkt weniger Zins spart über die Laufzeit spürbar Geld."),
        ],
    },

    "fuel": {
        "slug": "spritkostenrechner",
        "name": "Spritkostenrechner",
        "title": "Spritkostenrechner – Benzinkosten pro Fahrt berechnen | CalcMate",
        "desc": "Spritkosten online berechnen: Kraftstoffverbrauch und Kosten einer Fahrt aus Strecke, Verbrauch pro 100 km und Kraftstoffpreis. Kostenlos und schnell.",
        "h1": "Spritkostenrechner",
        "card": "Kraftstoffverbrauch und Kosten für eine Strecke berechnen.",
        "intro": "Was kostet die Fahrt? Gib Strecke, Durchschnittsverbrauch und Kraftstoffpreis ein und erhalte die benötigte Kraftstoffmenge, die Gesamtkosten und die Kosten pro 100 km.",
        "form": """\
<form class="calc-form" data-calc="fuel" novalidate>
  <div class="fields">
    <label>Strecke (km)<input type="text" inputmode="decimal" name="distance" placeholder="350"></label>
    <label>Verbrauch (l/100 km)<input type="text" inputmode="decimal" name="consumption" placeholder="6,5"></label>
    <label>Preis pro Liter<input type="text" inputmode="decimal" name="price" placeholder="1,85"></label>
  </div>
  <dl class="result-list">
    <div><dt>Kraftstoff (l)</dt><dd data-out="liters">–</dd></div>
    <div><dt>Kosten</dt><dd data-out="cost">–</dd></div>
    <div><dt>Kosten / 100 km</dt><dd data-out="per100">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Spritkosten berechnen: die Formel</h2>
<p>Die Kosten einer Fahrt ergeben sich aus drei Größen: der Strecke, dem Durchschnittsverbrauch deines Autos und dem aktuellen Kraftstoffpreis.</p>
<p class="formula">Kosten = Strecke ÷ 100 × Verbrauch × Literpreis</p>
<p>Beispiel: Für 350 km mit einem Verbrauch von 6,5 l/100 km brauchst du 22,75 Liter. Bei 1,85 € pro Liter kostet die Fahrt rund 42,09 € – das entspricht etwa 12,03 € pro 100 km.</p>
<p>Spar-Tipps: vorausschauend fahren und früh hochschalten, unnötigen Ballast und Dachträger entfernen, Reifendruck prüfen und Preise vergleichen – zwischen Autobahntankstelle und freier Tankstelle liegen oft mehr als 10 Cent pro Liter. Bei Fahrgemeinschaften teilst du die Gesamtkosten einfach durch die Zahl der Mitfahrer.</p>""",
        "faqs": [
            ("Wie berechne ich die Spritkosten für eine Fahrt?",
             "Teile die Strecke durch 100, multipliziere mit dem Verbrauch pro 100 km und dem Literpreis. Beispiel: 350 km ÷ 100 × 6,5 l × 1,85 € ≈ 42,09 €."),
            ("Wie viel kostet mich das Fahren pro 100 km?",
             "Multipliziere einfach den Verbrauch pro 100 km mit dem Literpreis. Bei 6,5 l/100 km und 1,85 €/l sind das rund 12,03 € pro 100 km."),
            ("Wie kann ich meinen Spritverbrauch senken?",
             "Vorausschauend fahren, früh hochschalten, korrekte Reifendrücke, unnötiges Gewicht und Dachaufbauten vermeiden und kurze Strecken bündeln. Zusammen senkt das den Verbrauch oft um 10–20 %."),
        ],
    },

    "tip": {
        "slug": "trinkgeld-rechner",
        "name": "Trinkgeld-Rechner",
        "title": "Trinkgeld-Rechner – Trinkgeld berechnen &amp; Rechnung teilen | CalcMate",
        "desc": "Trinkgeld online berechnen und die Rechnung gerecht aufteilen: Betrag, Prozentsatz und Personenzahl eingeben – Trinkgeld, Gesamtbetrag und Anteil pro Person.",
        "h1": "Trinkgeld-Rechner",
        "card": "Trinkgeld berechnen und die Rechnung pro Person aufteilen.",
        "intro": "Wie viel Trinkgeld ist angemessen und was zahlt jeder? Rechnungsbetrag, Trinkgeld in Prozent und Personenzahl eingeben – der Rechner zeigt Trinkgeld, Gesamtbetrag und den Anteil pro Person.",
        "form": """\
<form class="calc-form" data-calc="tip" novalidate>
  <div class="fields">
    <label>Rechnungsbetrag<input type="text" inputmode="decimal" name="bill" placeholder="86,50"></label>
    <label>Trinkgeld (%)<input type="text" inputmode="decimal" name="pct" value="10"></label>
    <label>Personen<input type="text" inputmode="numeric" name="people" placeholder="2"></label>
  </div>
  <dl class="result-list">
    <div><dt>Trinkgeld</dt><dd data-out="tip">–</dd></div>
    <div><dt>Gesamt</dt><dd data-out="total">–</dd></div>
    <div><dt>Pro Person</dt><dd data-out="person">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Wie viel Trinkgeld ist üblich?</h2>
<p>In Deutschland, Österreich und der Schweiz sind 5–10 % des Rechnungsbetrags üblich – oft wird einfach aufgerundet. In den USA erwarten Servicekräfte dagegen 15–20 %, weil das Trinkgeld dort ein wesentlicher Teil des Einkommens ist.</p>
<p class="formula">Trinkgeld = Rechnung × Prozentsatz ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;Pro Person = (Rechnung + Trinkgeld) ÷ Personen</p>
<p>Beispiel: Bei 86,50 € Rechnung und 10 % Trinkgeld gibst du 8,65 € – zusammen 95,15 €. Zu zweit zahlt jeder 47,58 €. Kopfrechen-Trick: 10 % erhältst du, indem du das Komma um eine Stelle nach links verschiebst; 5 % sind die Hälfte davon.</p>""",
        "faqs": [
            ("Wie viel Trinkgeld gibt man in Deutschland?",
             "Üblich sind 5–10 % im Restaurant, oder man rundet auf einen glatten Betrag auf. Bei sehr gutem Service dürfen es auch mehr sein – Trinkgeld ist freiwillig."),
            ("Wie berechne ich 10 % Trinkgeld im Kopf?",
             "Verschiebe das Komma des Rechnungsbetrags um eine Stelle nach links: 10 % von 86,50 € sind 8,65 €. Für 5 % halbierst du diesen Wert, für 20 % verdoppelst du ihn."),
            ("Wird das Trinkgeld vom Brutto- oder Nettobetrag berechnet?",
             "Im Alltag wird das Trinkgeld üblicherweise auf den Bruttobetrag der Rechnung (inklusive Mehrwertsteuer) gegeben – so macht es auch dieser Rechner."),
        ],
    },

    "date": {
        "slug": "tagerechner",
        "name": "Tagerechner",
        "title": "Tagerechner – Tage zwischen zwei Daten berechnen | CalcMate",
        "desc": "Tage zwischen zwei Daten online zählen: Start- und Enddatum wählen und die Differenz in Tagen und Wochen anzeigen – kostenlos, ohne Anmeldung.",
        "h1": "Tagerechner: Tage zwischen zwei Daten",
        "card": "Tage und Wochen zwischen zwei Daten zählen.",
        "intro": "Wie viele Tage liegen zwischen zwei Terminen? Wähle Start- und Enddatum – der Rechner zählt die Kalendertage und rechnet sie in Wochen um. Praktisch für Fristen, Urlaub, Countdown oder Projektplanung.",
        "form": """\
<form class="calc-form" data-calc="datediff" novalidate>
  <div class="fields">
    <label>Startdatum<input type="date" name="start"></label>
    <label>Enddatum<input type="date" name="end"></label>
  </div>
  <dl class="result-list">
    <div><dt>Tage</dt><dd data-out="days">–</dd></div>
    <div><dt>Wochen</dt><dd data-out="weeks">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>So zählt der Tagerechner</h2>
<p>Der Rechner ermittelt die echte Kalenderdifferenz zwischen beiden Daten – Schaltjahre und unterschiedliche Monatslängen werden automatisch berücksichtigt. Das Enddatum wird dabei nicht mitgezählt: Vom 1. zum 2. Januar ist es 1 Tag.</p>
<p class="formula">1. Januar 2026 → 1. März 2026 = 59 Tage (31 Tage Januar + 28 Tage Februar)</p>
<p>Soll das Enddatum mitzählen (z. B. „Urlaub vom 5. bis 9. August – wie viele Urlaubstage?“), addiere einfach 1 zum Ergebnis: 4 + 1 = 5 Tage. Für Fristen gilt je nach Kontext die eine oder andere Zählweise – im Zweifel die maßgebliche Regelung prüfen.</p>""",
        "faqs": [
            ("Wird das Enddatum mitgezählt?",
             "Nein, der Rechner zeigt die Differenz zwischen beiden Daten: Vom 1. zum 2. Januar ist es 1 Tag. Soll das Enddatum mitzählen, addiere einfach 1 zum Ergebnis."),
            ("Berücksichtigt der Rechner Schaltjahre?",
             "Ja. Gerechnet wird mit echten Kalenderdaten, Schaltjahre und unterschiedliche Monatslängen fließen automatisch korrekt ein."),
            ("Wie viele Tage hat ein Jahr?",
             "Ein normales Jahr hat 365 Tage, ein Schaltjahr 366. Schaltjahre sind durch 4 teilbare Jahre – volle Jahrhunderte allerdings nur, wenn sie durch 400 teilbar sind (2000 war ein Schaltjahr, 2100 nicht)."),
        ],
    },
}
