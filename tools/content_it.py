# -*- coding: utf-8 -*-
"""Italian content for CalcMate. Consumed by tools/build.py."""

SITE = {
    "title": "Calcolatrici online gratuite – Percentuale, IVA, Prestito, IMC &amp; altro | CalcMate",
    "desc": "Calcolatrici online gratuite senza registrazione: percentuale, IVA, sconto, prestito, costo carburante, mancia, giorni tra due date, regola del tre, pendenza, IMC e interesse composto.",
    "app_name": "CalcMate – Calcolatrici online gratuite",
    "app_desc": "Calcolatrici online gratuite senza registrazione: calcolatrice, percentuale, IVA, sconto, regola del tre, pendenza, IMC, interesse composto, prestito, costo carburante, mancia e giorni tra due date.",
    "hub_h1": "Calcolatrici online gratuite – veloci, moderne, senza registrazione",
    "hub_intro": "I calcoli di tutti i giorni resi semplici: percentuali, IVA, sconti, prestiti, costi del carburante, IMC, interesse composto, giorni tra due date e altro – tutto gratis, direttamente nel browser.",
    "home": "Home",
    "faq_title": "Domande frequenti",
    "related_title": "Calcolatrici correlate",
    "lang_nav_label": "Lingue",
    "footer": "© 2026 CalcMate – calcolatrici online gratuite. Risultati forniti senza garanzia.",
    "hub_faqs": [
        ("Queste calcolatrici online sono gratuite?",
         "Sì, tutte le calcolatrici di CalcMate sono completamente gratuite. Nessuna registrazione, nessun login, nessun costo nascosto: apri la pagina e inizia a calcolare."),
        ("Come si calcola la percentuale di un numero?",
         "Moltiplica il numero per la percentuale e dividi per 100. Ad esempio, il 20% di 150 è 150 × 20 ÷ 100 = 30. Il nostro calcolatore di percentuale lo fa istantaneamente."),
        ("Come si calcola l'IVA?",
         "Per aggiungere l'IVA, moltiplica il prezzo netto per (1 + aliquota ÷ 100). Per scorporare l'IVA da un prezzo lordo, dividi per lo stesso fattore. Il calcolatore IVA gestisce automaticamente entrambe le direzioni."),
        ("Come si calcola la rata mensile di un prestito?",
         "Per un prestito a tasso fisso: rata = capitale × tasso mensile ÷ (1 − (1 + tasso mensile)^−mesi). Il calcolatore di prestito mostra rata mensile, importo totale e costo degli interessi a colpo d'occhio."),
        ("Come si calcola l'IMC (BMI)?",
         "L'indice di massa corporea è il peso in chilogrammi diviso per il quadrato dell'altezza in metri: IMC = kg / m². Un IMC tra 18,5 e 25 è considerato normopeso."),
    ],
    "i18n": {
        "error": "Errore",
        "bmi_label": "IMC",
        "bmi_under": "Sottopeso",
        "bmi_normal": "Normopeso",
        "bmi_over": "Sovrappeso",
        "bmi_obese": "Obesità",
        "weeks": "settimane",
        "days": "giorni",
    },
}

CALCS = {

    "calculator": {
        "slug": "calcolatrice",
        "name": "Calcolatrice",
        "title": "Calcolatrice online – gratuita e senza registrazione | CalcMate",
        "desc": "Calcolatrice online gratuita con parentesi e percentuale: addizione, sottrazione, moltiplicazione e divisione – direttamente nel browser.",
        "h1": "Calcolatrice online",
        "card": "Le quattro operazioni con parentesi e percentuale.",
        "intro": "Una calcolatrice gratuita per addizione, sottrazione, moltiplicazione e divisione – con parentesi e percentuale. Digita un'espressione o usa i tasti, poi premi <kbd>=</kbd> o Invio.",
        "form": """\
<div class="calculator" data-calculator>
  <input class="calc-display" type="text" inputmode="decimal" aria-label="Display della calcolatrice" placeholder="0" autocomplete="off">
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
<h2>Come funziona la calcolatrice online</h2>
<p>La calcolatrice gestisce le quattro operazioni di base, le parentesi e la percentuale, rispettando la precedenza degli operatori: moltiplicazione e divisione vengono valutate prima di addizione e sottrazione, e le parentesi hanno sempre la priorità. Puoi digitare un'espressione completa e valutarla solo alla fine.</p>
<p class="formula">(12 + 8) × 2,5 = 50&nbsp;&nbsp;·&nbsp;&nbsp;200 − 15% = 200 − 0,15 × 200 = 170</p>
<p>Il tasto percentuale converte il numero che lo precede in centesimi: 15% diventa 0,15, così puoi applicare maggiorazioni e riduzioni direttamente nell'espressione. Sono accettati sia la virgola sia il punto decimale.</p>""",
        "faqs": [
            ("La calcolatrice rispetta la precedenza degli operatori?",
             "Sì. Moltiplicazione e divisione vengono valutate prima di addizione e sottrazione, e le parentesi hanno sempre la precedenza. Quindi 2 + 3 × 4 dà 14, mentre (2 + 3) × 4 dà 20."),
            ("Come funziona il tasto percentuale?",
             "Il tasto % divide il numero che lo precede per 100: 50% diventa 0,5. Ad esempio, digitando 80 × 25% si ottiene 20."),
            ("Posso usare la tastiera?",
             "Sì. Clicca nel display e digita l'espressione direttamente – cifre, + − × ÷ (oppure * e /), parentesi e virgola. Premi Invio o = per calcolare, Esc per cancellare."),
        ],
    },

    "percentage": {
        "slug": "calcolo-percentuale",
        "name": "Calcolo percentuale",
        "title": "Calcolo percentuale online – Calcolatore gratuito | CalcMate",
        "desc": "Calcolatore di percentuale online: l'X% di un valore, quale percentuale è X di Y e la variazione percentuale tra due valori – con formule ed esempi.",
        "h1": "Calcolo percentuale",
        "card": "Percentuale di un valore, quota in % e variazione in %.",
        "intro": "Calcola percentuali online: trova la percentuale di un valore, scopri quale percentuale rappresenta un numero rispetto a un altro, oppure calcola l'aumento o la diminuzione percentuale tra due valori.",
        "form": """\
<div class="subform">
  <h3>Quanto è l'X% di un valore?</h3>
  <form class="calc-form" data-calc="pct-of" novalidate>
    <div class="fields">
      <label>Percentuale (%)<input type="text" inputmode="decimal" name="p" placeholder="20"></label>
      <label>Valore<input type="text" inputmode="decimal" name="x" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>X è quale percentuale di Y?</h3>
  <form class="calc-form" data-calc="pct-what" novalidate>
    <div class="fields">
      <label>Valore X<input type="text" inputmode="decimal" name="x" placeholder="30"></label>
      <label>Valore base Y<input type="text" inputmode="decimal" name="y" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>Variazione percentuale da A a B</h3>
  <form class="calc-form" data-calc="pct-change" novalidate>
    <div class="fields">
      <label>Valore iniziale A<input type="text" inputmode="decimal" name="a" placeholder="100"></label>
      <label>Nuovo valore B<input type="text" inputmode="decimal" name="b" placeholder="120"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>""",
        "seo": """\
<h2>Percentuali: le tre formule di base</h2>
<p>Quasi ogni problema di percentuale si riduce a tre domande: quanto vale l'X% di un valore? Quale percentuale rappresenta X di Y? E di quale percentuale è variato un valore?</p>
<p class="formula">parte = base × percentuale ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;percentuale = parte ÷ base × 100</p>
<p>Esempi: il 20% di 150 è 150 × 20 ÷ 100 = 30. Il numero 30 rappresenta 30 ÷ 150 × 100 = il 20% di 150. E se un prezzo sale da 100 € a 120 €, la variazione è (120 − 100) ÷ 100 × 100 = +20%.</p>
<p>Attenzione alle variazioni successive: un aumento del 20% seguito da una diminuzione del 20% non riporta al valore iniziale, perché la seconda percentuale si applica alla nuova base, più alta (100 → 120 → 96).</p>""",
        "faqs": [
            ("Come si calcola la percentuale di un numero?",
             "Moltiplica il numero per la percentuale e dividi per 100. Ad esempio, il 20% di 150 è 150 × 20 ÷ 100 = 30."),
            ("Come scopro quale percentuale è X di Y?",
             "Dividi X per Y e moltiplica per 100. Ad esempio, 30 su 150 è 30 ÷ 150 × 100 = 20%."),
            ("Come si calcola la variazione percentuale?",
             "Sottrai il valore iniziale dal nuovo valore, dividi per il valore iniziale e moltiplica per 100: (B − A) ÷ A × 100. Da 100 a 120 è +20%; da 120 a 100 è −16,67%."),
        ],
    },

    "vat": {
        "slug": "calcolo-iva",
        "name": "Calcolo IVA",
        "title": "Calcolo IVA – Scorporo e aggiunta IVA (netto ↔ lordo) | CalcMate",
        "desc": "Calcolatore IVA online: aggiungi l'IVA a un prezzo netto o scorporala da un prezzo lordo, al 22%, 10% o qualsiasi aliquota – con formule ed esempi.",
        "h1": "Calcolo IVA",
        "card": "Aggiungere o scorporare l'IVA – netto ↔ lordo.",
        "intro": "Aggiungi o scorpora l'IVA in un solo passaggio: dal netto al lordo o dal lordo al netto con qualsiasi aliquota. L'aliquota ordinaria in Italia è del 22%, in Germania del 19%, in Francia del 20%.",
        "form": """\
<form class="calc-form" data-calc="vat" novalidate>
  <div class="fields">
    <label>Importo<input type="text" inputmode="decimal" name="amount" placeholder="100"></label>
    <label>Aliquota IVA (%)<input type="text" inputmode="decimal" name="rate" value="22"></label>
  </div>
  <fieldset>
    <label><input type="radio" name="dir" value="net2gross" checked> Netto → Lordo (aggiungi IVA)</label>
    <label><input type="radio" name="dir" value="gross2net"> Lordo → Netto (scorpora IVA)</label>
  </fieldset>
  <dl class="result-list">
    <div><dt>Netto</dt><dd data-out="net">–</dd></div>
    <div><dt>IVA</dt><dd data-out="vat">–</dd></div>
    <div><dt>Lordo</dt><dd data-out="gross">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Calcolare l'IVA: le formule</h2>
<p>Un unico fattore trasforma il prezzo netto in prezzo lordo. Con l'IVA al 22% il fattore è 1,22; con l'aliquota ridotta del 10% è 1,10.</p>
<p class="formula">lordo = netto × (1 + aliquota ÷ 100)&nbsp;&nbsp;·&nbsp;&nbsp;netto = lordo ÷ (1 + aliquota ÷ 100)</p>
<p>Esempio: 100 € netti al 22% danno 122 € lordi, l'IVA è di 22 €. Viceversa, 122 € lordi contengono 122 ÷ 1,22 = 100 € netti. Errore frequente: sottrarre il 22% dal prezzo lordo – il risultato è troppo basso, perché il 22% si applica all'importo netto.</p>
<p>In Italia l'aliquota ordinaria è del 22%; le aliquote ridotte del 10%, 5% e 4% si applicano ad esempio a generi alimentari, ristorazione, libri e prodotti di prima necessità.</p>""",
        "faqs": [
            ("Come si calcola l'IVA?",
             "Per aggiungere l'IVA, moltiplica il prezzo netto per (1 + aliquota ÷ 100) – al 22% moltiplichi quindi per 1,22. Per scorporare l'IVA da un prezzo lordo, dividi per lo stesso fattore."),
            ("Come si scorpora l'IVA da un prezzo lordo?",
             "Dividi il prezzo lordo per 1,22 al 22% (o per 1,10 al 10%). Esempio: 122 € lordi ÷ 1,22 = 100 € netti, quindi l'IVA è di 22 €. Sottrarre semplicemente il 22% dal lordo sarebbe sbagliato."),
            ("Quali aliquote IVA si applicano in Italia?",
             "L'aliquota ordinaria è del 22%. Le aliquote ridotte sono del 10% (es. ristorazione, energia), del 5% e del 4% (beni di prima necessità, alimentari di base, libri)."),
        ],
    },

    "discount": {
        "slug": "calcolo-sconto",
        "name": "Calcolo sconto",
        "title": "Calcolo sconto – Prezzo dopo lo sconto | CalcMate",
        "desc": "Calcola lo sconto online: quanto risparmi con l'X% di sconto e quanto costa l'articolo dopo la riduzione? Gratis, con formula ed esempi.",
        "h1": "Calcolo sconto",
        "card": "Risparmio e prezzo finale con l'X% di sconto.",
        "intro": "Calcola in pochi secondi quanto risparmi con uno sconto e quanto costa l'articolo dopo la riduzione: basta inserire il prezzo e lo sconto in percentuale.",
        "form": """\
<form class="calc-form" data-calc="discount" novalidate>
  <div class="fields">
    <label>Prezzo<input type="text" inputmode="decimal" name="price" placeholder="80"></label>
    <label>Sconto (%)<input type="text" inputmode="decimal" name="pct" placeholder="25"></label>
  </div>
  <dl class="result-list">
    <div><dt>Risparmio</dt><dd data-out="saved">–</dd></div>
    <div><dt>Prezzo finale</dt><dd data-out="final">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Come si calcola uno sconto</h2>
<p>Lo sconto è una riduzione percentuale del prezzo originale. Il risparmio e il prezzo finale derivano da due semplici formule:</p>
<p class="formula">risparmio = prezzo × sconto ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;prezzo finale = prezzo − risparmio</p>
<p>Esempio: un maglione costa 80 € ed è scontato del 25%. Il risparmio è 80 × 25 ÷ 100 = 20 €, il prezzo finale 60 €. Scorciatoie di calcolo mentale: il 25% è un quarto, il 50% è la metà e il 10% è un decimo del prezzo.</p>
<p>Attenzione agli sconti cumulati: «20% + 10%» non fa 30%. Il secondo sconto si applica al prezzo già ridotto – 100 € diventano 80 €, poi 72 €, cioè il 28% di sconto complessivo.</p>""",
        "faqs": [
            ("Come si calcola uno sconto?",
             "Moltiplica il prezzo per la percentuale di sconto e dividi per 100: è il tuo risparmio. Il prezzo finale è il prezzo originale meno il risparmio. Esempio: 80 € con il 25% di sconto = 20 € risparmiati, 60 € da pagare."),
            ("Quanto costa un articolo dopo il 20% di sconto?",
             "Moltiplica il prezzo per 0,8. Esempio: 50 € × 0,8 = 40 €. In generale: prezzo finale = prezzo originale × (1 − sconto ÷ 100)."),
            ("Come funzionano gli sconti cumulati, ad esempio 20% + 10%?",
             "Gli sconti si applicano uno dopo l'altro e non si sommano. 100 € diventano 80 € dopo il 20%, poi 72 € dopo un ulteriore 10%. Lo sconto totale è del 28%, non del 30%."),
        ],
    },

    "rule3": {
        "slug": "regola-del-tre",
        "name": "Regola del tre",
        "title": "Regola del tre – Calcolatore di proporzioni online | CalcMate",
        "desc": "Regola del tre online: risolvi proporzioni dirette e inverse. Se A corrisponde a B, a cosa corrisponde C? Gratis, con formule ed esempi.",
        "h1": "Regola del tre",
        "card": "Risolvere proporzioni dirette e inverse in pochi secondi.",
        "intro": "Risolvi le proporzioni in pochi secondi: se A corrisponde a B, a cosa corrisponde C? Ideale per ricette, prezzi, velocità e conversioni di unità. Spunta la casella per le relazioni inversamente proporzionali (più operai → meno tempo).",
        "form": """\
<form class="calc-form" data-calc="rule3" novalidate>
  <div class="fields">
    <label>A<input type="text" inputmode="decimal" name="a" placeholder="4"></label>
    <label>corrisponde a B<input type="text" inputmode="decimal" name="b" placeholder="12"></label>
    <label>C<input type="text" inputmode="decimal" name="c" placeholder="7"></label>
  </div>
  <fieldset>
    <label class="check"><input type="checkbox" name="inverse"> Inversamente proporzionale</label>
  </fieldset>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>Come funziona la regola del tre</h2>
<p>La regola del tre riconduce una relazione nota («A corrisponde a B») all'unità e poi la riporta alla quantità cercata. In una proporzione diretta le due grandezze crescono insieme; in una proporzione inversa una diminuisce quando l'altra aumenta.</p>
<p class="formula">diretta: X = B × C ÷ A&nbsp;&nbsp;·&nbsp;&nbsp;inversa: X = A × B ÷ C</p>
<p>Esempio diretto: 4 mele costano 12 €. Quanto costano 7 mele? X = 12 × 7 ÷ 4 = 21 €. Esempio inverso: 4 imbianchini impiegano 12 ore. Quanto impiegano 6 imbianchini? X = 4 × 12 ÷ 6 = 8 ore.</p>""",
        "faqs": [
            ("Come funziona la regola del tre?",
             "Prima riduci all'unità, poi moltiplica per la quantità cercata. Se 4 mele costano 12 €, una mela costa 3 € e 7 mele costano 21 €. In formula: X = B × C ÷ A."),
            ("Che cos'è la regola del tre inversa?",
             "In una proporzione inversa una grandezza diminuisce quando l'altra aumenta – più operai, meno tempo. La formula diventa X = A × B ÷ C: se 4 imbianchini impiegano 12 ore, 6 imbianchini finiscono in 8 ore."),
            ("A cosa serve la regola del tre nella vita quotidiana?",
             "Ad adattare ricette a un numero diverso di porzioni, confrontare prezzi al chilo o al litro, convertire velocità e unità, stimare materiali o tempi di lavoro – ovunque due grandezze stiano in un rapporto fisso."),
        ],
    },

    "slope": {
        "slug": "calcolo-pendenza",
        "name": "Calcolo pendenza",
        "title": "Calcolo pendenza – Percentuale &amp; gradi | CalcMate",
        "desc": "Calcola una pendenza online: percentuale e gradi da lunghezza e altezza, oppure conversione diretta tra % e gradi. Con schema del triangolo.",
        "h1": "Calcolo pendenza",
        "card": "Pendenza in percentuale e in gradi – con schema.",
        "intro": "Calcola una pendenza in percentuale e in gradi – a partire dalla lunghezza orizzontale e dall'altezza (il dislivello). In alternativa, inserisci direttamente la pendenza in percentuale o in gradi per convertirle. Utile per tetti, rampe, strade e tubazioni.",
        "form": """\
<svg class="slope-figure" viewBox="0 0 360 190" role="img" aria-label="Triangolo rettangolo: lunghezza orizzontale in basso, altezza a destra, angolo α a sinistra">
  <polygon points="30,160 310,160 310,50" fill="#eef2fc"/>
  <line x1="30" y1="160" x2="310" y2="160" stroke="#1c2430" stroke-width="2"/>
  <line x1="310" y1="160" x2="310" y2="50" stroke="#1c2430" stroke-width="2"/>
  <line x1="30" y1="160" x2="310" y2="50" stroke="#4f6df5" stroke-width="2.5"/>
  <path d="M 296 160 L 296 146 L 310 146" fill="none" stroke="#9aa3b5" stroke-width="1.5"/>
  <path d="M 64 160 A 34 34 0 0 0 61.6 147.6" fill="none" stroke="#6b7385" stroke-width="1.5"/>
  <text x="78" y="156" font-size="14" fill="#6b7385">α</text>
  <text x="170" y="182" font-size="14" fill="#6b7385" text-anchor="middle">Lunghezza</text>
  <text x="316" y="110" font-size="14" fill="#6b7385">Altezza</text>
</svg>
<form class="calc-form" data-calc="slope" novalidate>
  <fieldset>
    <label><input type="radio" name="mode" value="lh" checked> Lunghezza e altezza</label>
    <label><input type="radio" name="mode" value="pct"> Pendenza in %</label>
    <label><input type="radio" name="mode" value="deg"> Angolo in gradi</label>
  </fieldset>
  <div class="fields">
    <label data-field="pct" hidden>Pendenza (%)<input type="text" inputmode="decimal" name="pct" placeholder="12"></label>
    <label data-field="deg" hidden>Angolo (°)<input type="text" inputmode="decimal" name="deg" placeholder="6,84"></label>
    <label data-field="len">Lunghezza (m)<input type="text" inputmode="decimal" name="len" placeholder="100"></label>
    <label data-field="height">Altezza (m)<input type="text" inputmode="decimal" name="height" placeholder="12"></label>
  </div>
  <dl class="result-list">
    <div><dt>Pendenza</dt><dd data-out="percent">–</dd></div>
    <div><dt>Angolo α</dt><dd data-out="angle">–</dd></div>
    <div><dt>Altezza (m)</dt><dd data-out="height">–</dd></div>
    <div><dt>Lunghezza inclinata (m)</dt><dd data-out="hyp">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Pendenza in percentuale e in gradi</h2>
<p>La pendenza in percentuale indica quanti metri di dislivello corrispondono a 100 metri di lunghezza orizzontale. L'angolo è l'arcotangente dello stesso rapporto.</p>
<p class="formula">pendenza (%) = altezza ÷ lunghezza × 100&nbsp;&nbsp;·&nbsp;&nbsp;angolo α = arctan(altezza ÷ lunghezza)</p>
<p>Esempio: un dislivello di 12 m su 100 m di lunghezza dà una pendenza del 12% e un angolo di circa 6,84°. La lunghezza inclinata (ipotenusa) segue dal teorema di Pitagora: √(100² + 12²) ≈ 100,72 m.</p>
<p>Valori di riferimento tipici: le tubazioni di scarico richiedono almeno l'1–2% di pendenza, le rampe accessibili non dovrebbero superare il 6%, e una pendenza del 100% corrisponde esattamente a 45°.</p>""",
        "faqs": [
            ("Come si calcola una pendenza in percentuale?",
             "Dividi l'altezza (il dislivello) per la lunghezza orizzontale e moltiplica per 100: pendenza (%) = altezza ÷ lunghezza × 100. Ad esempio, 12 m di altezza su 100 m di lunghezza danno una pendenza del 12%."),
            ("Come si converte una pendenza in percentuale in gradi?",
             "L'angolo è l'arcotangente del rapporto: α = arctan(percentuale ÷ 100). Il 12% corrisponde ad arctan(0,12) ≈ 6,84°, e il 100% corrisponde esattamente a 45°."),
            ("Cosa significa una pendenza del 100%?",
             "Con una pendenza del 100% il dislivello è uguale alla distanza orizzontale: corrisponde a un angolo di 45°, non a una parete verticale."),
        ],
    },

    "bmi": {
        "slug": "calcolo-imc",
        "name": "Calcolo IMC",
        "title": "Calcolo IMC (BMI) – Indice di massa corporea | CalcMate",
        "desc": "Calcola il tuo IMC online: indice di massa corporea da peso e altezza, con le categorie OMS da sottopeso a obesità. Gratis, senza registrazione.",
        "h1": "Calcolo IMC (BMI)",
        "card": "Indice di massa corporea con interpretazione OMS.",
        "intro": "Calcola il tuo indice di massa corporea (IMC) a partire da peso e altezza. L'IMC è un riferimento rapido per un peso corporeo sano: negli adulti, valori tra 18,5 e 25 sono considerati normopeso.",
        "form": """\
<form class="calc-form" data-calc="bmi" novalidate>
  <div class="fields">
    <label>Peso (kg)<input type="text" inputmode="decimal" name="weight" placeholder="70"></label>
    <label>Altezza (cm)<input type="text" inputmode="decimal" name="height" placeholder="175"></label>
  </div>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>Come si calcola l'IMC</h2>
<p>L'indice di massa corporea mette in relazione il peso con l'altezza. È definito dall'Organizzazione Mondiale della Sanità (OMS) come riferimento approssimativo per gli adulti.</p>
<p class="formula">IMC = peso (kg) ÷ altezza (m)²</p>
<p>Esempio: 70 kg per 1,75 m danno 70 ÷ (1,75 × 1,75) ≈ 22,9 – normopeso. Le categorie OMS: sotto 18,5 sottopeso, 18,5–24,9 normopeso, 25–29,9 sovrappeso, da 30 in su obesità.</p>
<p>L'IMC non distingue tra massa muscolare e massa grassa: persone sportive e muscolose possono avere un IMC alto con poco grasso corporeo. Per bambini, donne in gravidanza e anziani valgono valori di riferimento specifici – in caso di dubbio, consulta un medico.</p>""",
        "faqs": [
            ("Come si calcola l'IMC (BMI)?",
             "L'indice di massa corporea è il peso in chilogrammi diviso per il quadrato dell'altezza in metri: IMC = kg / m². Esempio: 70 kg per 1,75 m danno un IMC di circa 22,9."),
            ("Quale IMC è considerato normale?",
             "Secondo l'OMS, negli adulti un IMC da 18,5 a 24,9 è considerato normopeso. Sotto 18,5 si parla di sottopeso, da 25 di sovrappeso e da 30 di obesità."),
            ("Quanto è affidabile l'IMC?",
             "L'IMC è solo un riferimento approssimativo. Non distingue muscoli e grasso e non tiene conto di età, sesso o corporatura. Per una valutazione seria servono misurazioni aggiuntive e un parere medico."),
        ],
    },

    "interest": {
        "slug": "interesse-composto",
        "name": "Interesse composto",
        "title": "Calcolo interesse composto online | CalcMate",
        "desc": "Calcola l'interesse composto online: capitale finale e interessi maturati da capitale iniziale, tasso e durata – con formula e regola del 72.",
        "h1": "Calcolatore di interesse composto",
        "card": "Capitale finale e interessi maturati con capitalizzazione.",
        "intro": "Guarda crescere i tuoi risparmi: inserisci un capitale iniziale, un tasso di interesse annuo e una durata in anni per calcolare il capitale finale, interesse composto incluso.",
        "form": """\
<form class="calc-form" data-calc="interest" novalidate>
  <div class="fields">
    <label>Capitale iniziale<input type="text" inputmode="decimal" name="principal" placeholder="10000"></label>
    <label>Tasso di interesse (% annuo)<input type="text" inputmode="decimal" name="rate" placeholder="3"></label>
    <label>Durata (anni)<input type="text" inputmode="decimal" name="years" placeholder="10"></label>
  </div>
  <dl class="result-list">
    <div><dt>Capitale finale</dt><dd data-out="final">–</dd></div>
    <div><dt>Interessi maturati</dt><dd data-out="earned">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>La formula dell'interesse composto</h2>
<p>Con l'interesse composto, gli interessi di ogni periodo si aggiungono al capitale e producono a loro volta interessi nei periodi successivi. Il capitale cresce quindi in modo esponenziale, non lineare.</p>
<p class="formula">capitale finale = capitale iniziale × (1 + tasso ÷ 100)^anni</p>
<p>Esempio: 10.000 € al 3% annuo diventano 10.000 × 1,03¹⁰ ≈ 13.439,16 € dopo 10 anni – circa 3.439 € di interessi. Con l'interesse semplice (senza capitalizzazione) sarebbero solo 3.000 €.</p>
<p>Regola pratica per il raddoppio («regola del 72»): dividi 72 per il tasso di interesse e ottieni il numero approssimativo di anni necessari al raddoppio del capitale. Al 6% servono circa 12 anni.</p>""",
        "faqs": [
            ("Che cos'è l'effetto dell'interesse composto?",
             "Gli interessi vengono accreditati sul capitale e producono a loro volta interessi negli anni successivi. Il capitale cresce in modo esponenziale: 10.000 € al 3% diventano circa 13.439 € in 10 anni, contro i 13.000 € dell'interesse semplice."),
            ("Qual è la formula dell'interesse composto?",
             "Capitale finale = capitale iniziale × (1 + tasso ÷ 100) elevato al numero di anni. Esempio: 10.000 € × 1,03¹⁰ ≈ 13.439,16 €."),
            ("Quanto tempo serve per raddoppiare il capitale?",
             "Usa la regola del 72: 72 diviso per il tasso di interesse dà approssimativamente gli anni necessari al raddoppio. Al 6% circa 12 anni; al 3% circa 24 anni."),
        ],
    },

    "loan": {
        "slug": "calcolo-prestito",
        "name": "Calcolo prestito",
        "title": "Calcolo prestito – Rata mensile, interessi &amp; costo totale | CalcMate",
        "desc": "Calcolatore di prestito online: rata mensile, importo totale e costo degli interessi di un prestito a tasso fisso da importo, tasso e durata. Gratis.",
        "h1": "Calcolo prestito",
        "card": "Rata mensile, importo totale e interessi di un prestito.",
        "intro": "Calcola la rata mensile di un prestito a tasso fisso (ammortamento alla francese): inserisci l'importo del prestito, il tasso di interesse annuo e la durata – il calcolatore mostra la rata mensile, l'importo totale rimborsato e il costo degli interessi.",
        "form": """\
<form class="calc-form" data-calc="loan" novalidate>
  <div class="fields">
    <label>Importo del prestito<input type="text" inputmode="decimal" name="principal" placeholder="20000"></label>
    <label>Tasso di interesse (% annuo)<input type="text" inputmode="decimal" name="rate" placeholder="5"></label>
    <label>Durata (anni)<input type="text" inputmode="decimal" name="years" placeholder="5"></label>
  </div>
  <dl class="result-list">
    <div><dt>Rata mensile</dt><dd data-out="monthly">–</dd></div>
    <div><dt>Totale rimborsato</dt><dd data-out="total">–</dd></div>
    <div><dt>Costo interessi</dt><dd data-out="interest">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Come si calcola la rata mensile</h2>
<p>In un prestito con ammortamento alla francese la rata mensile resta costante per tutta la durata. Ogni rata è composta da una quota interessi e una quota capitale; man mano che il debito residuo diminuisce, la quota interessi cala e la quota capitale cresce.</p>
<p class="formula">rata = capitale × i ÷ (1 − (1 + i)^−n)&nbsp;&nbsp;con&nbsp;&nbsp;i = tasso annuo ÷ 12 ÷ 100, n = mesi</p>
<p>Esempio: 20.000 € al 5% per 5 anni (60 rate mensili) danno una rata di circa 377,42 €. In totale rimborsi circa 22.645 €, quindi il costo degli interessi è di circa 2.645 €.</p>
<p>Nota: il calcolatore usa il tasso nominale (TAN). Le banche devono indicare anche il TAEG, che include le spese e rende confrontabili le offerte. Durate più brevi significano rate più alte ma un costo totale degli interessi nettamente inferiore.</p>""",
        "faqs": [
            ("Come si calcola la rata mensile di un prestito?",
             "Con la formula dell'ammortamento alla francese: rata = capitale × tasso mensile ÷ (1 − (1 + tasso mensile)^−mesi). Esempio: 20.000 € al 5% per 5 anni danno circa 377,42 € al mese."),
            ("Qual è la differenza tra TAN e TAEG?",
             "Il TAN è il tasso di interesse puro sul debito residuo. Il TAEG include anche spese, commissioni e la tempistica dei pagamenti: è il valore giusto per confrontare le offerte di prestito."),
            ("Come posso ridurre il costo degli interessi di un prestito?",
             "Scegli una durata più breve, effettua estinzioni parziali quando possibile, confronta le offerte tramite il TAEG e chiedi solo l'importo davvero necessario. Anche mezzo punto di tasso in meno fa risparmiare sensibilmente sulla durata."),
        ],
    },

    "fuel": {
        "slug": "costo-carburante",
        "name": "Costo carburante",
        "title": "Costo carburante – Calcola la spesa di benzina per un viaggio | CalcMate",
        "desc": "Calcola il costo del carburante per un viaggio: litri necessari e spesa da distanza, consumo per 100 km e prezzo al litro. Gratis e veloce.",
        "h1": "Calcolatore costo carburante",
        "card": "Litri necessari e spesa di carburante per un viaggio.",
        "intro": "Quanto costa il viaggio? Inserisci la distanza, il consumo medio della tua auto e il prezzo del carburante per ottenere la quantità di carburante necessaria, la spesa totale e il costo per 100 km.",
        "form": """\
<form class="calc-form" data-calc="fuel" novalidate>
  <div class="fields">
    <label>Distanza (km)<input type="text" inputmode="decimal" name="distance" placeholder="350"></label>
    <label>Consumo (l/100 km)<input type="text" inputmode="decimal" name="consumption" placeholder="6,5"></label>
    <label>Prezzo al litro<input type="text" inputmode="decimal" name="price" placeholder="1,85"></label>
  </div>
  <dl class="result-list">
    <div><dt>Carburante (l)</dt><dd data-out="liters">–</dd></div>
    <div><dt>Costo</dt><dd data-out="cost">–</dd></div>
    <div><dt>Costo / 100 km</dt><dd data-out="per100">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Calcolare il costo del carburante: la formula</h2>
<p>Il costo di un viaggio dipende da tre elementi: la distanza, il consumo medio del veicolo e il prezzo attuale del carburante.</p>
<p class="formula">costo = distanza ÷ 100 × consumo × prezzo al litro</p>
<p>Esempio: per 350 km con un consumo di 6,5 l/100 km servono 22,75 litri. A 1,85 € al litro il viaggio costa circa 42,09 € – più o meno 12,03 € per 100 km.</p>
<p>Consigli per risparmiare: guida fluida e cambio marcia anticipato, niente peso superfluo né portapacchi, pressione degli pneumatici corretta e confronto dei prezzi – tra un distributore e l'altro la differenza supera spesso i 10 centesimi al litro. In caso di car pooling, dividi semplicemente il costo totale per il numero di passeggeri.</p>""",
        "faqs": [
            ("Come calcolo la spesa di carburante per un viaggio?",
             "Dividi la distanza per 100, moltiplica per il consumo per 100 km e per il prezzo al litro. Esempio: 350 km ÷ 100 × 6,5 l × 1,85 € ≈ 42,09 €."),
            ("Quanto costa viaggiare per 100 km?",
             "Moltiplica semplicemente il consumo per 100 km per il prezzo al litro. Con 6,5 l/100 km e 1,85 €/l sono circa 12,03 € per 100 km."),
            ("Come posso ridurre il consumo di carburante?",
             "Guida fluida, cambio marcia anticipato, pneumatici alla giusta pressione, niente pesi o portapacchi inutili e accorpamento dei tragitti brevi. Nel complesso il consumo cala spesso del 10–20%."),
        ],
    },

    "tip": {
        "slug": "calcolo-mancia",
        "name": "Calcolo mancia",
        "title": "Calcolo mancia – Mancia &amp; divisione del conto | CalcMate",
        "desc": "Calcola la mancia online e dividi il conto: importo, percentuale e numero di persone – mancia, totale e quota per persona.",
        "h1": "Calcolo mancia",
        "card": "Calcolare la mancia e dividere il conto per persona.",
        "intro": "Quanta mancia lasciare e quanto paga ciascuno? Inserisci l'importo del conto, la percentuale di mancia e il numero di persone – il calcolatore mostra la mancia, il totale e la quota per persona.",
        "form": """\
<form class="calc-form" data-calc="tip" novalidate>
  <div class="fields">
    <label>Conto<input type="text" inputmode="decimal" name="bill" placeholder="86,50"></label>
    <label>Mancia (%)<input type="text" inputmode="decimal" name="pct" value="10"></label>
    <label>Persone<input type="text" inputmode="numeric" name="people" placeholder="2"></label>
  </div>
  <dl class="result-list">
    <div><dt>Mancia</dt><dd data-out="tip">–</dd></div>
    <div><dt>Totale</dt><dd data-out="total">–</dd></div>
    <div><dt>Per persona</dt><dd data-out="person">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Quanta mancia lasciare?</h2>
<p>Le abitudini variano molto da paese a paese. In Italia la mancia non è obbligatoria: spesso si arrotonda o si lascia il 5–10% per un servizio particolarmente buono (attenzione al coperto, che non è una mancia). Negli Stati Uniti sono attesi il 15–20%, perché la mancia è una parte essenziale del reddito dei camerieri.</p>
<p class="formula">mancia = conto × percentuale ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;per persona = (conto + mancia) ÷ persone</p>
<p>Esempio: con un conto di 86,50 € e il 10% di mancia lasci 8,65 €, per un totale di 95,15 €. In due, ognuno paga 47,58 €. Scorciatoia mentale: sposta la virgola di una posizione a sinistra per ottenere il 10%; il 5% è la metà.</p>""",
        "faqs": [
            ("Quanta mancia si lascia in Italia?",
             "In Italia la mancia è facoltativa: spesso si arrotonda il conto o si lascia il 5–10% per un servizio molto buono. Il coperto indicato sul conto non è una mancia, ma una voce del ristorante."),
            ("Come calcolo il 10% di mancia a mente?",
             "Sposta la virgola dell'importo di una posizione a sinistra: il 10% di 86,50 € è 8,65 €. Per il 5% prendi la metà; per il 20% raddoppia."),
            ("La mancia si calcola prima o dopo l'IVA?",
             "In Europa i prezzi esposti includono già l'IVA: la mancia si calcola semplicemente sull'importo finale del conto. È quello che fa anche questo calcolatore."),
        ],
    },

    "date": {
        "slug": "giorni-tra-due-date",
        "name": "Giorni tra due date",
        "title": "Giorni tra due date – Calcolatore di durata | CalcMate",
        "desc": "Conta i giorni tra due date online: scegli data di inizio e di fine e ottieni la differenza in giorni e settimane. Gratis, con anni bisestili corretti.",
        "h1": "Giorni tra due date",
        "card": "Contare giorni e settimane tra due date.",
        "intro": "Quanti giorni separano due date? Scegli la data di inizio e quella di fine – il calcolatore conta i giorni di calendario e li converte in settimane. Utile per scadenze, vacanze, conti alla rovescia e pianificazione di progetti.",
        "form": """\
<form class="calc-form" data-calc="datediff" novalidate>
  <div class="fields">
    <label>Data di inizio<input type="date" name="start"></label>
    <label>Data di fine<input type="date" name="end"></label>
  </div>
  <dl class="result-list">
    <div><dt>Giorni</dt><dd data-out="days">–</dd></div>
    <div><dt>Settimane</dt><dd data-out="weeks">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Come conta i giorni il calcolatore</h2>
<p>Il calcolatore determina la differenza reale di calendario tra le due date – anni bisestili e mesi di lunghezza diversa sono gestiti automaticamente. La data di fine non viene contata: dal 1° al 2 gennaio c'è 1 giorno.</p>
<p class="formula">1° gennaio 2026 → 1° marzo 2026 = 59 giorni (31 giorni di gennaio + 28 giorni di febbraio)</p>
<p>Se anche la data di fine deve contare (ad esempio «ferie dal 5 al 9 agosto: quanti giorni di ferie?»), aggiungi semplicemente 1 al risultato: 4 + 1 = 5 giorni. Per le scadenze legali può valere l'una o l'altra convenzione a seconda delle regole applicabili – in caso di dubbio, verifica la norma di riferimento.</p>""",
        "faqs": [
            ("La data di fine è inclusa nel conteggio?",
             "No, il calcolatore mostra la differenza tra le due date: dal 1° al 2 gennaio c'è 1 giorno. Se la data di fine deve essere inclusa, aggiungi 1 al risultato."),
            ("Il calcolatore tiene conto degli anni bisestili?",
             "Sì. Il calcolo si basa su vere date di calendario, quindi anni bisestili e mesi di lunghezza variabile sono gestiti automaticamente in modo corretto."),
            ("Quanti giorni ha un anno?",
             "Un anno normale ha 365 giorni, un anno bisestile 366. Sono bisestili gli anni divisibili per 4 – ma i secoli pieni solo se divisibili per 400 (il 2000 è stato bisestile, il 2100 non lo sarà)."),
        ],
    },
}
