# -*- coding: utf-8 -*-
"""French content for CalcMate. Consumed by tools/build.py."""

SITE = {
    "title": "Calculatrices en ligne gratuites – Pourcentage, TVA, Prêt, IMC &amp; plus | CalcMate",
    "desc": "Calculatrices en ligne gratuites sans inscription : pourcentage, TVA, remise, prêt, coût du carburant, pourboire, jours entre deux dates, règle de trois, pente, IMC et intérêts composés.",
    "app_name": "CalcMate – Calculatrices en ligne gratuites",
    "app_desc": "Calculatrices en ligne gratuites sans inscription : calculatrice, pourcentage, TVA, remise, règle de trois, pente, IMC, intérêts composés, prêt, coût du carburant, pourboire et jours entre deux dates.",
    "hub_h1": "Calculatrices en ligne gratuites – rapides, modernes, sans inscription",
    "hub_intro": "Les calculs du quotidien en toute simplicité : pourcentages, TVA, remises, prêts, coût du carburant, IMC, intérêts composés, jours entre deux dates et plus – le tout gratuit, directement dans votre navigateur.",
    "home": "Accueil",
    "faq_title": "Questions fréquentes",
    "related_title": "Calculatrices associées",
    "lang_nav_label": "Langues",
    "footer": "© 2026 CalcMate – calculatrices en ligne gratuites. Résultats fournis sans garantie.",
    "hub_faqs": [
        ("Ces calculatrices en ligne sont-elles gratuites ?",
         "Oui, toutes les calculatrices de CalcMate sont entièrement gratuites. Aucune inscription, aucun compte, aucun coût caché : ouvrez la page et commencez à calculer."),
        ("Comment calculer un pourcentage d'un nombre ?",
         "Multipliez le nombre par le pourcentage puis divisez par 100. Par exemple, 20 % de 150 font 150 × 20 ÷ 100 = 30. Notre calculateur de pourcentage le fait instantanément."),
        ("Comment calculer la TVA ?",
         "Pour ajouter la TVA, multipliez le prix hors taxes par (1 + taux ÷ 100). Pour extraire la TVA d'un prix TTC, divisez par le même facteur. Le calculateur de TVA gère les deux sens automatiquement."),
        ("Comment calculer la mensualité d'un prêt ?",
         "Pour un prêt à taux fixe : mensualité = capital × taux mensuel ÷ (1 − (1 + taux mensuel)^−mois). Le calculateur de prêt affiche la mensualité, le coût total et les intérêts en un coup d'œil."),
        ("Comment calcule-t-on l'IMC ?",
         "L'indice de masse corporelle est le poids en kilogrammes divisé par le carré de la taille en mètres : IMC = kg / m². Un IMC entre 18,5 et 25 correspond à une corpulence normale."),
    ],
    "i18n": {
        "error": "Erreur",
        "bmi_label": "IMC",
        "bmi_under": "Insuffisance pondérale",
        "bmi_normal": "Corpulence normale",
        "bmi_over": "Surpoids",
        "bmi_obese": "Obésité",
        "weeks": "semaines",
        "days": "jours",
    },
}

CALCS = {

    "calculator": {
        "slug": "calculatrice",
        "name": "Calculatrice",
        "title": "Calculatrice en ligne – gratuite et sans inscription | CalcMate",
        "desc": "Calculatrice en ligne gratuite avec parenthèses et pourcentage : addition, soustraction, multiplication et division – directement dans le navigateur.",
        "h1": "Calculatrice en ligne",
        "card": "Les quatre opérations avec parenthèses et pourcentage.",
        "intro": "Une calculatrice gratuite pour l'addition, la soustraction, la multiplication et la division – avec parenthèses et pourcentage. Saisissez une expression ou utilisez le clavier, puis appuyez sur <kbd>=</kbd> ou Entrée.",
        "form": """\
<div class="calculator" data-calculator>
  <input class="calc-display" type="text" inputmode="decimal" aria-label="Écran de la calculatrice" placeholder="0" autocomplete="off">
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
<h2>Comment fonctionne la calculatrice en ligne</h2>
<p>La calculatrice gère les quatre opérations de base, les parenthèses et le pourcentage, en respectant la priorité des opérations : multiplication et division sont évaluées avant addition et soustraction, et les parenthèses ont toujours la priorité. Vous pouvez saisir une expression complète et ne l'évaluer qu'à la fin.</p>
<p class="formula">(12 + 8) × 2,5 = 50&nbsp;&nbsp;·&nbsp;&nbsp;200 − 15 % = 200 − 0,15 × 200 = 170</p>
<p>La touche pourcentage convertit le nombre qui la précède en centièmes : 15 % devient 0,15, ce qui permet d'appliquer majorations et réductions directement dans l'expression. La virgule et le point décimal sont tous deux acceptés.</p>""",
        "faqs": [
            ("La calculatrice respecte-t-elle la priorité des opérations ?",
             "Oui. La multiplication et la division sont évaluées avant l'addition et la soustraction, et les parenthèses passent toujours en premier. Ainsi 2 + 3 × 4 donne 14, tandis que (2 + 3) × 4 donne 20."),
            ("Comment fonctionne la touche pourcentage ?",
             "La touche % divise le nombre qui la précède par 100 : 50 % devient 0,5. Par exemple, saisir 80 × 25 % donne 20."),
            ("Puis-je utiliser mon clavier ?",
             "Oui. Cliquez dans le champ d'affichage et tapez votre expression directement – chiffres, + − × ÷ (ou * et /), parenthèses et virgule. Appuyez sur Entrée ou = pour calculer, sur Échap pour effacer."),
        ],
    },

    "percentage": {
        "slug": "calcul-pourcentage",
        "name": "Calcul de pourcentage",
        "title": "Calcul de pourcentage en ligne – Calculateur gratuit | CalcMate",
        "desc": "Calculateur de pourcentage en ligne : X % d'une valeur, quel pourcentage X représente de Y, et la variation en pourcentage – avec formules et exemples.",
        "h1": "Calcul de pourcentage",
        "card": "Pourcentage d'une valeur, part en % et variation en %.",
        "intro": "Calculez des pourcentages en ligne : trouvez le pourcentage d'une valeur, déterminez quel pourcentage un nombre représente d'un autre, ou calculez la hausse ou la baisse en pourcentage entre deux valeurs.",
        "form": """\
<div class="subform">
  <h3>Combien font X % d'une valeur ?</h3>
  <form class="calc-form" data-calc="pct-of" novalidate>
    <div class="fields">
      <label>Pourcentage (%)<input type="text" inputmode="decimal" name="p" placeholder="20"></label>
      <label>Valeur<input type="text" inputmode="decimal" name="x" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>X représente quel pourcentage de Y ?</h3>
  <form class="calc-form" data-calc="pct-what" novalidate>
    <div class="fields">
      <label>Valeur X<input type="text" inputmode="decimal" name="x" placeholder="30"></label>
      <label>Valeur de base Y<input type="text" inputmode="decimal" name="y" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>Variation en pourcentage de A vers B</h3>
  <form class="calc-form" data-calc="pct-change" novalidate>
    <div class="fields">
      <label>Valeur initiale A<input type="text" inputmode="decimal" name="a" placeholder="100"></label>
      <label>Nouvelle valeur B<input type="text" inputmode="decimal" name="b" placeholder="120"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>""",
        "seo": """\
<h2>Pourcentages : les trois formules de base</h2>
<p>Presque tout problème de pourcentage se ramène à trois questions : combien vaut X % d'une valeur ? Quel pourcentage X représente-t-il de Y ? Et de quel pourcentage une valeur a-t-elle varié ?</p>
<p class="formula">partie = base × pourcentage ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;pourcentage = partie ÷ base × 100</p>
<p>Exemples : 20 % de 150 font 150 × 20 ÷ 100 = 30. Le nombre 30 représente 30 ÷ 150 × 100 = 20 % de 150. Et si un prix passe de 100 € à 120 €, la variation est de (120 − 100) ÷ 100 × 100 = +20 %.</p>
<p>Attention aux variations successives : une hausse de 20 % suivie d'une baisse de 20 % ne ramène pas à la valeur initiale, car le second pourcentage s'applique à la nouvelle base, plus élevée (100 → 120 → 96).</p>""",
        "faqs": [
            ("Comment calculer un pourcentage d'un nombre ?",
             "Multipliez le nombre par le pourcentage puis divisez par 100. Par exemple, 20 % de 150 font 150 × 20 ÷ 100 = 30."),
            ("Comment savoir quel pourcentage X représente de Y ?",
             "Divisez X par Y et multipliez par 100. Par exemple, 30 sur 150 font 30 ÷ 150 × 100 = 20 %."),
            ("Comment calcule-t-on une variation en pourcentage ?",
             "Soustrayez la valeur initiale de la nouvelle valeur, divisez par la valeur initiale et multipliez par 100 : (B − A) ÷ A × 100. De 100 à 120, cela fait +20 % ; de 120 à 100, −16,67 %."),
        ],
    },

    "vat": {
        "slug": "calcul-tva",
        "name": "Calculateur de TVA",
        "title": "Calcul TVA – Prix HT ↔ TTC en ligne | CalcMate",
        "desc": "Calculateur de TVA en ligne : passer du HT au TTC ou extraire la TVA d'un prix TTC, à 20 %, 5,5 % ou tout autre taux – avec formules et exemples.",
        "h1": "Calculateur de TVA",
        "card": "Ajouter ou extraire la TVA – HT ↔ TTC à tout taux.",
        "intro": "Ajoutez ou retirez la TVA en une étape : convertissez un prix hors taxes (HT) en prix TTC ou inversement, avec n'importe quel taux. Le taux normal est de 20 % en France, 19 % en Allemagne, 22 % en Italie et 8,1 % en Suisse.",
        "form": """\
<form class="calc-form" data-calc="vat" novalidate>
  <div class="fields">
    <label>Montant<input type="text" inputmode="decimal" name="amount" placeholder="100"></label>
    <label>Taux de TVA (%)<input type="text" inputmode="decimal" name="rate" value="20"></label>
  </div>
  <fieldset>
    <label><input type="radio" name="dir" value="net2gross" checked> HT → TTC (ajouter la TVA)</label>
    <label><input type="radio" name="dir" value="gross2net"> TTC → HT (retirer la TVA)</label>
  </fieldset>
  <dl class="result-list">
    <div><dt>HT</dt><dd data-out="net">–</dd></div>
    <div><dt>TVA</dt><dd data-out="vat">–</dd></div>
    <div><dt>TTC</dt><dd data-out="gross">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Calculer la TVA : les formules</h2>
<p>Un seul facteur permet de passer du prix hors taxes au prix TTC. À 20 % de TVA, ce facteur est 1,20 ; au taux réduit de 5,5 %, il est de 1,055.</p>
<p class="formula">TTC = HT × (1 + taux ÷ 100)&nbsp;&nbsp;·&nbsp;&nbsp;HT = TTC ÷ (1 + taux ÷ 100)</p>
<p>Exemple : 100 € HT à 20 % donnent 120 € TTC, la TVA s'élève à 20 €. Inversement, 120 € TTC contiennent 120 ÷ 1,20 = 100 € HT. Erreur fréquente : soustraire 20 % du prix TTC – le résultat est trop faible, car les 20 % s'appliquent au montant HT.</p>
<p>En France, le taux normal est de 20 % ; les taux réduits de 10 %, 5,5 % et 2,1 % s'appliquent notamment à la restauration, aux produits alimentaires, aux livres et aux médicaments remboursables.</p>""",
        "faqs": [
            ("Comment calculer la TVA ?",
             "Pour ajouter la TVA, multipliez le prix HT par (1 + taux ÷ 100) – à 20 %, multipliez donc par 1,20. Pour extraire la TVA d'un prix TTC, divisez par le même facteur."),
            ("Comment retrouver le prix HT à partir du TTC ?",
             "Divisez le prix TTC par 1,20 à 20 % (ou 1,055 à 5,5 %). Exemple : 120 € TTC ÷ 1,20 = 100 € HT, soit 20 € de TVA. Soustraire simplement 20 % du TTC serait faux."),
            ("Quels sont les taux de TVA en France ?",
             "Le taux normal est de 20 %. Les taux réduits sont de 10 % (restauration, transports), 5,5 % (produits alimentaires, livres, énergie) et 2,1 % (médicaments remboursables, presse)."),
        ],
    },

    "discount": {
        "slug": "calcul-remise",
        "name": "Calcul de remise",
        "title": "Calcul de remise – Prix après réduction | CalcMate",
        "desc": "Calculez une remise en ligne : combien économisez-vous avec X % de réduction et quel est le prix final ? Gratuit, avec formule et exemples.",
        "h1": "Calcul de remise",
        "card": "Économie et prix final après X % de réduction.",
        "intro": "Calculez en quelques secondes combien vous économisez grâce à une remise et ce que coûte l'article après réduction : saisissez simplement le prix et le pourcentage de remise.",
        "form": """\
<form class="calc-form" data-calc="discount" novalidate>
  <div class="fields">
    <label>Prix<input type="text" inputmode="decimal" name="price" placeholder="80"></label>
    <label>Remise (%)<input type="text" inputmode="decimal" name="pct" placeholder="25"></label>
  </div>
  <dl class="result-list">
    <div><dt>Économie</dt><dd data-out="saved">–</dd></div>
    <div><dt>Prix final</dt><dd data-out="final">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Comment calculer une remise</h2>
<p>Une remise est une réduction en pourcentage du prix initial. L'économie et le prix final découlent de deux formules simples :</p>
<p class="formula">économie = prix × remise ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;prix final = prix − économie</p>
<p>Exemple : un pull coûte 80 € et bénéficie de 25 % de réduction. L'économie est de 80 × 25 ÷ 100 = 20 €, le prix final de 60 €. Astuces de calcul mental : 25 % représentent un quart, 50 % la moitié et 10 % un dixième du prix.</p>
<p>Attention aux remises cumulées : « 20 % + 10 % » ne font pas 30 %. La seconde remise s'applique au prix déjà réduit – 100 € deviennent 80 €, puis 72 €, soit 28 % de réduction au total.</p>""",
        "faqs": [
            ("Comment calculer une remise ?",
             "Multipliez le prix par le pourcentage de remise et divisez par 100 : c'est votre économie. Le prix final est le prix initial moins l'économie. Exemple : 80 € avec 25 % de remise = 20 € économisés, 60 € à payer."),
            ("Combien coûte un article après 20 % de réduction ?",
             "Multipliez le prix par 0,8. Exemple : 50 € × 0,8 = 40 €. En général : prix final = prix initial × (1 − remise ÷ 100)."),
            ("Comment fonctionnent les remises cumulées, par exemple 20 % + 10 % ?",
             "Les remises s'appliquent l'une après l'autre et ne s'additionnent pas. 100 € deviennent 80 € après 20 %, puis 72 € après 10 % supplémentaires. La remise totale est de 28 %, pas de 30 %."),
        ],
    },

    "rule3": {
        "slug": "regle-de-trois",
        "name": "Règle de trois",
        "title": "Règle de trois – Calculateur de proportions en ligne | CalcMate",
        "desc": "Règle de trois en ligne : résolvez les proportions directes et inverses. Si A correspond à B, à quoi correspond C ? Gratuit, avec formules et exemples.",
        "h1": "Règle de trois",
        "card": "Résoudre les proportions directes et inverses en secondes.",
        "intro": "Résolvez des proportions en quelques secondes : si A correspond à B, à quoi correspond C ? Idéal pour les recettes, les prix, les vitesses et les conversions d'unités. Cochez la case pour les relations inversement proportionnelles (plus d'ouvriers → moins de temps).",
        "form": """\
<form class="calc-form" data-calc="rule3" novalidate>
  <div class="fields">
    <label>A<input type="text" inputmode="decimal" name="a" placeholder="4"></label>
    <label>correspond à B<input type="text" inputmode="decimal" name="b" placeholder="12"></label>
    <label>C<input type="text" inputmode="decimal" name="c" placeholder="7"></label>
  </div>
  <fieldset>
    <label class="check"><input type="checkbox" name="inverse"> Inversement proportionnel</label>
  </fieldset>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>Comment fonctionne la règle de trois</h2>
<p>La règle de trois ramène une relation connue (« A correspond à B ») à une unité, puis passe à l'échelle de la quantité recherchée. Dans une proportion directe, les deux grandeurs augmentent ensemble ; dans une proportion inverse, l'une diminue quand l'autre augmente.</p>
<p class="formula">directe : X = B × C ÷ A&nbsp;&nbsp;·&nbsp;&nbsp;inverse : X = A × B ÷ C</p>
<p>Exemple direct : 4 pommes coûtent 12 €. Combien coûtent 7 pommes ? X = 12 × 7 ÷ 4 = 21 €. Exemple inverse : 4 peintres mettent 12 heures. Combien de temps mettent 6 peintres ? X = 4 × 12 ÷ 6 = 8 heures.</p>""",
        "faqs": [
            ("Comment fonctionne la règle de trois ?",
             "Ramenez d'abord à une unité, puis passez à la quantité recherchée. Si 4 pommes coûtent 12 €, une pomme coûte 3 € et 7 pommes coûtent 21 €. En formule : X = B × C ÷ A."),
            ("Qu'est-ce qu'une règle de trois inverse ?",
             "Dans une proportion inverse, une grandeur diminue quand l'autre augmente – plus d'ouvriers, moins de temps. La formule devient X = A × B ÷ C : si 4 peintres mettent 12 heures, 6 peintres terminent en 8 heures."),
            ("À quoi sert la règle de trois au quotidien ?",
             "Adapter des recettes à un autre nombre de convives, comparer des prix au kilo ou au litre, convertir vitesses et unités, estimer des besoins en matériaux ou du temps de travail – partout où deux grandeurs sont dans un rapport fixe."),
        ],
    },

    "slope": {
        "slug": "calcul-pente",
        "name": "Calcul de pente",
        "title": "Calcul de pente – Pourcentage &amp; degrés | CalcMate",
        "desc": "Calculez une pente en ligne : pourcentage et degrés à partir de la longueur et de la hauteur, ou conversion directe entre % et degrés. Avec schéma.",
        "h1": "Calcul de pente",
        "card": "Pente en pourcentage et en degrés – avec schéma.",
        "intro": "Calculez une pente en pourcentage et en degrés – à partir de la longueur horizontale et de la hauteur (le dénivelé). Vous pouvez aussi saisir directement la pente en pourcentage ou en degrés pour convertir l'une en l'autre. Pratique pour les toits, rampes, routes et canalisations.",
        "form": """\
<svg class="slope-figure" viewBox="0 0 360 190" role="img" aria-label="Triangle rectangle : longueur horizontale en bas, hauteur à droite, angle α à gauche">
  <polygon points="30,160 310,160 310,50" fill="#eef2fc"/>
  <line x1="30" y1="160" x2="310" y2="160" stroke="#1c2430" stroke-width="2"/>
  <line x1="310" y1="160" x2="310" y2="50" stroke="#1c2430" stroke-width="2"/>
  <line x1="30" y1="160" x2="310" y2="50" stroke="#4f6df5" stroke-width="2.5"/>
  <path d="M 296 160 L 296 146 L 310 146" fill="none" stroke="#9aa3b5" stroke-width="1.5"/>
  <path d="M 64 160 A 34 34 0 0 0 61.6 147.6" fill="none" stroke="#6b7385" stroke-width="1.5"/>
  <text x="78" y="156" font-size="14" fill="#6b7385">α</text>
  <text x="170" y="182" font-size="14" fill="#6b7385" text-anchor="middle">Longueur</text>
  <text x="316" y="110" font-size="14" fill="#6b7385">Hauteur</text>
</svg>
<form class="calc-form" data-calc="slope" novalidate>
  <fieldset>
    <label><input type="radio" name="mode" value="lh" checked> Longueur et hauteur</label>
    <label><input type="radio" name="mode" value="pct"> Pente en %</label>
    <label><input type="radio" name="mode" value="deg"> Angle en degrés</label>
  </fieldset>
  <div class="fields">
    <label data-field="pct" hidden>Pente (%)<input type="text" inputmode="decimal" name="pct" placeholder="12"></label>
    <label data-field="deg" hidden>Angle (°)<input type="text" inputmode="decimal" name="deg" placeholder="6,84"></label>
    <label data-field="len">Longueur (m)<input type="text" inputmode="decimal" name="len" placeholder="100"></label>
    <label data-field="height">Hauteur (m)<input type="text" inputmode="decimal" name="height" placeholder="12"></label>
  </div>
  <dl class="result-list">
    <div><dt>Pente</dt><dd data-out="percent">–</dd></div>
    <div><dt>Angle α</dt><dd data-out="angle">–</dd></div>
    <div><dt>Hauteur (m)</dt><dd data-out="height">–</dd></div>
    <div><dt>Longueur de pente (m)</dt><dd data-out="hyp">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Pente en pourcentage et en degrés</h2>
<p>La pente en pourcentage indique combien de mètres de dénivelé correspondent à 100 mètres de longueur horizontale. L'angle est l'arc tangente du même rapport.</p>
<p class="formula">pente (%) = hauteur ÷ longueur × 100&nbsp;&nbsp;·&nbsp;&nbsp;angle α = arctan(hauteur ÷ longueur)</p>
<p>Exemple : un dénivelé de 12 m sur 100 m de longueur donne une pente de 12 % et un angle d'environ 6,84°. La longueur de pente (l'hypoténuse) découle du théorème de Pythagore : √(100² + 12²) ≈ 100,72 m.</p>
<p>Repères usuels : les canalisations d'évacuation nécessitent au moins 1 à 2 % de pente, les rampes accessibles ne doivent pas dépasser 6 %, et une pente de 100 % correspond exactement à 45°.</p>""",
        "faqs": [
            ("Comment calculer une pente en pourcentage ?",
             "Divisez la hauteur (le dénivelé) par la longueur horizontale et multipliez par 100 : pente (%) = hauteur ÷ longueur × 100. Par exemple, 12 m de hauteur sur 100 m de longueur donnent une pente de 12 %."),
            ("Comment convertir une pente en pourcentage en degrés ?",
             "L'angle est l'arc tangente du rapport : α = arctan(pourcentage ÷ 100). Une pente de 12 % correspond à arctan(0,12) ≈ 6,84°, et 100 % correspondent exactement à 45°."),
            ("Que signifie une pente de 100 % ?",
             "À 100 % de pente, le dénivelé est égal à la distance horizontale – cela correspond à un angle de 45°, et non à un mur vertical."),
        ],
    },

    "bmi": {
        "slug": "calcul-imc",
        "name": "Calcul de l'IMC",
        "title": "Calcul IMC – Indice de masse corporelle | CalcMate",
        "desc": "Calculez votre IMC en ligne : indice de masse corporelle à partir du poids et de la taille, avec les catégories OMS. Gratuit et sans inscription.",
        "h1": "Calcul de l'IMC",
        "card": "Indice de masse corporelle avec interprétation OMS.",
        "intro": "Calculez votre indice de masse corporelle (IMC) à partir de votre poids et de votre taille. L'IMC est un repère rapide pour un poids de forme : chez l'adulte, une valeur entre 18,5 et 25 correspond à une corpulence normale.",
        "form": """\
<form class="calc-form" data-calc="bmi" novalidate>
  <div class="fields">
    <label>Poids (kg)<input type="text" inputmode="decimal" name="weight" placeholder="70"></label>
    <label>Taille (cm)<input type="text" inputmode="decimal" name="height" placeholder="175"></label>
  </div>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>Comment l'IMC est-il calculé ?</h2>
<p>L'indice de masse corporelle met le poids en relation avec la taille. Il est défini par l'Organisation mondiale de la santé (OMS) comme repère approximatif pour les adultes.</p>
<p class="formula">IMC = poids (kg) ÷ taille (m)²</p>
<p>Exemple : 70 kg pour 1,75 m donnent 70 ÷ (1,75 × 1,75) ≈ 22,9 – corpulence normale. Les catégories OMS : moins de 18,5 insuffisance pondérale, 18,5–24,9 corpulence normale, 25–29,9 surpoids, 30 et plus obésité.</p>
<p>L'IMC ne distingue pas la masse musculaire de la masse grasse : les personnes sportives et musclées peuvent avoir un IMC élevé avec peu de graisse corporelle. Des valeurs de référence spécifiques s'appliquent aux enfants, aux femmes enceintes et aux personnes âgées – en cas de doute, demandez un avis médical.</p>""",
        "faqs": [
            ("Comment calcule-t-on l'IMC ?",
             "L'indice de masse corporelle est le poids en kilogrammes divisé par le carré de la taille en mètres : IMC = kg / m². Exemple : 70 kg pour 1,75 m donnent un IMC d'environ 22,9."),
            ("Quel IMC est considéré comme normal ?",
             "Selon l'OMS, un IMC de 18,5 à 24,9 correspond à une corpulence normale chez l'adulte. En dessous de 18,5 on parle d'insuffisance pondérale, à partir de 25 de surpoids et à partir de 30 d'obésité."),
            ("L'IMC est-il fiable ?",
             "L'IMC n'est qu'un repère approximatif. Il ne distingue pas muscle et graisse et ne tient compte ni de l'âge, ni du sexe, ni de la morphologie. Pour une évaluation solide, des mesures complémentaires et un avis médical sont recommandés."),
        ],
    },

    "interest": {
        "slug": "interets-composes",
        "name": "Intérêts composés",
        "title": "Calcul des intérêts composés en ligne | CalcMate",
        "desc": "Calculez les intérêts composés en ligne : capital final et intérêts gagnés à partir du capital de départ, du taux et de la durée – avec formule et règle des 72.",
        "h1": "Calculateur d'intérêts composés",
        "card": "Capital final et intérêts gagnés avec capitalisation.",
        "intro": "Voyez votre épargne grandir : saisissez un capital de départ, un taux d'intérêt annuel et une durée en années pour calculer le capital final, intérêts composés inclus.",
        "form": """\
<form class="calc-form" data-calc="interest" novalidate>
  <div class="fields">
    <label>Capital de départ<input type="text" inputmode="decimal" name="principal" placeholder="10000"></label>
    <label>Taux d'intérêt (% par an)<input type="text" inputmode="decimal" name="rate" placeholder="3"></label>
    <label>Durée (années)<input type="text" inputmode="decimal" name="years" placeholder="10"></label>
  </div>
  <dl class="result-list">
    <div><dt>Capital final</dt><dd data-out="final">–</dd></div>
    <div><dt>Intérêts gagnés</dt><dd data-out="earned">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>La formule des intérêts composés</h2>
<p>Avec les intérêts composés, les intérêts de chaque période s'ajoutent au capital et produisent eux-mêmes des intérêts les périodes suivantes. Le capital croît donc de manière exponentielle et non linéaire.</p>
<p class="formula">capital final = capital de départ × (1 + taux ÷ 100)^années</p>
<p>Exemple : 10 000 € à 3 % par an deviennent 10 000 × 1,03¹⁰ ≈ 13 439,16 € après 10 ans – soit environ 3 439 € d'intérêts. Avec des intérêts simples (sans capitalisation), ce ne serait que 3 000 €.</p>
<p>Règle pratique pour le doublement (« règle des 72 ») : divisez 72 par le taux d'intérêt pour obtenir le nombre approximatif d'années nécessaires au doublement du capital. À 6 %, il faut environ 12 ans.</p>""",
        "faqs": [
            ("Qu'est-ce que l'effet des intérêts composés ?",
             "Les intérêts sont ajoutés au capital et produisent eux-mêmes des intérêts les années suivantes. Le capital croît de façon exponentielle : 10 000 € à 3 % deviennent environ 13 439 € en 10 ans, contre 13 000 € avec des intérêts simples."),
            ("Quelle est la formule des intérêts composés ?",
             "Capital final = capital de départ × (1 + taux ÷ 100) puissance nombre d'années. Exemple : 10 000 € × 1,03¹⁰ ≈ 13 439,16 €."),
            ("Combien de temps faut-il pour doubler mon capital ?",
             "Utilisez la règle des 72 : 72 divisé par le taux d'intérêt donne approximativement le nombre d'années nécessaires. À 6 %, environ 12 ans ; à 3 %, environ 24 ans."),
        ],
    },

    "loan": {
        "slug": "calcul-pret",
        "name": "Calcul de prêt",
        "title": "Calcul de prêt – Mensualité, intérêts &amp; coût total | CalcMate",
        "desc": "Calculateur de prêt en ligne : mensualité, coût total et intérêts d'un crédit à taux fixe à partir du montant, du taux et de la durée. Gratuit.",
        "h1": "Calcul de prêt",
        "card": "Mensualité, coût total et intérêts d'un crédit.",
        "intro": "Calculez la mensualité d'un prêt à taux fixe (crédit amortissable) : saisissez le montant emprunté, le taux d'intérêt annuel et la durée – le calculateur affiche la mensualité, le montant total remboursé et le coût des intérêts.",
        "form": """\
<form class="calc-form" data-calc="loan" novalidate>
  <div class="fields">
    <label>Montant du prêt<input type="text" inputmode="decimal" name="principal" placeholder="20000"></label>
    <label>Taux d'intérêt (% par an)<input type="text" inputmode="decimal" name="rate" placeholder="5"></label>
    <label>Durée (années)<input type="text" inputmode="decimal" name="years" placeholder="5"></label>
  </div>
  <dl class="result-list">
    <div><dt>Mensualité</dt><dd data-out="monthly">–</dd></div>
    <div><dt>Total remboursé</dt><dd data-out="total">–</dd></div>
    <div><dt>Coût des intérêts</dt><dd data-out="interest">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Comment la mensualité est-elle calculée ?</h2>
<p>Pour un prêt amortissable à taux fixe, la mensualité reste constante sur toute la durée. Chaque échéance comprend une part d'intérêts et une part de capital ; à mesure que le capital restant dû diminue, la part d'intérêts baisse et la part de capital augmente.</p>
<p class="formula">mensualité = capital × i ÷ (1 − (1 + i)^−n)&nbsp;&nbsp;avec&nbsp;&nbsp;i = taux annuel ÷ 12 ÷ 100, n = mois</p>
<p>Exemple : 20 000 € à 5 % sur 5 ans (60 mensualités) donnent une mensualité d'environ 377,42 €. Au total, vous remboursez environ 22 645 €, soit un coût d'intérêts d'environ 2 645 €.</p>
<p>Remarque : le calculateur utilise le taux nominal. Les banques doivent également indiquer le TAEG (taux annuel effectif global), qui inclut les frais et permet de comparer les offres. Une durée plus courte signifie des mensualités plus élevées mais un coût total des intérêts nettement plus faible.</p>""",
        "faqs": [
            ("Comment calcule-t-on la mensualité d'un prêt ?",
             "Avec la formule d'annuité : mensualité = capital × taux mensuel ÷ (1 − (1 + taux mensuel)^−mois). Exemple : 20 000 € à 5 % sur 5 ans donnent environ 377,42 € par mois."),
            ("Quelle est la différence entre taux nominal et TAEG ?",
             "Le taux nominal est l'intérêt pur sur le capital restant dû. Le TAEG inclut en plus les frais de dossier, l'assurance et le calendrier des paiements : c'est lui qu'il faut utiliser pour comparer les offres de crédit."),
            ("Comment réduire le coût des intérêts d'un prêt ?",
             "Choisissez une durée plus courte, effectuez des remboursements anticipés quand c'est possible, comparez les offres via le TAEG et n'empruntez que le nécessaire. Un demi-point de taux en moins représente déjà une économie sensible sur la durée."),
        ],
    },

    "fuel": {
        "slug": "cout-carburant",
        "name": "Coût du carburant",
        "title": "Coût du carburant – Calculer le budget essence d'un trajet | CalcMate",
        "desc": "Calculez le coût en carburant d'un trajet : litres nécessaires et budget à partir de la distance, de la consommation aux 100 km et du prix du litre.",
        "h1": "Calculateur de coût du carburant",
        "card": "Litres nécessaires et coût d'un trajet en voiture.",
        "intro": "Combien coûte le trajet ? Saisissez la distance, la consommation moyenne de votre voiture et le prix du carburant pour obtenir la quantité de carburant nécessaire, le coût total et le coût aux 100 km.",
        "form": """\
<form class="calc-form" data-calc="fuel" novalidate>
  <div class="fields">
    <label>Distance (km)<input type="text" inputmode="decimal" name="distance" placeholder="350"></label>
    <label>Consommation (l/100 km)<input type="text" inputmode="decimal" name="consumption" placeholder="6,5"></label>
    <label>Prix du litre<input type="text" inputmode="decimal" name="price" placeholder="1,85"></label>
  </div>
  <dl class="result-list">
    <div><dt>Carburant (l)</dt><dd data-out="liters">–</dd></div>
    <div><dt>Coût</dt><dd data-out="cost">–</dd></div>
    <div><dt>Coût / 100 km</dt><dd data-out="per100">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Calculer le coût du carburant : la formule</h2>
<p>Le coût d'un trajet dépend de trois éléments : la distance, la consommation moyenne de votre véhicule et le prix actuel du carburant.</p>
<p class="formula">coût = distance ÷ 100 × consommation × prix du litre</p>
<p>Exemple : pour 350 km avec une consommation de 6,5 l/100 km, il faut 22,75 litres. À 1,85 € le litre, le trajet coûte environ 42,09 € – soit à peu près 12,03 € aux 100 km.</p>
<p>Astuces d'économie : conduite souple et passage rapide des vitesses, suppression du poids inutile et des barres de toit, pression des pneus correcte et comparaison des prix – d'une station à l'autre, l'écart dépasse souvent 10 centimes par litre. En covoiturage, divisez simplement le coût total par le nombre de passagers.</p>""",
        "faqs": [
            ("Comment calculer le coût en carburant d'un trajet ?",
             "Divisez la distance par 100, multipliez par la consommation aux 100 km puis par le prix du litre. Exemple : 350 km ÷ 100 × 6,5 l × 1,85 € ≈ 42,09 €."),
            ("Combien coûte la route aux 100 km ?",
             "Multipliez simplement la consommation aux 100 km par le prix du litre. À 6,5 l/100 km et 1,85 €/l, cela fait environ 12,03 € aux 100 km."),
            ("Comment réduire ma consommation de carburant ?",
             "Conduite souple, passage rapide des rapports, pneus bien gonflés, pas de poids ni de galerie inutiles, et regroupement des petits trajets. L'ensemble réduit souvent la consommation de 10 à 20 %."),
        ],
    },

    "tip": {
        "slug": "calcul-pourboire",
        "name": "Calcul de pourboire",
        "title": "Calcul de pourboire – Pourboire &amp; partage de l'addition | CalcMate",
        "desc": "Calculez le pourboire en ligne et partagez l'addition : montant, pourcentage et nombre de personnes – pourboire, total et part par personne.",
        "h1": "Calcul de pourboire",
        "card": "Calculer le pourboire et partager l'addition par personne.",
        "intro": "Quel pourboire laisser et combien paie chacun ? Saisissez le montant de l'addition, le pourcentage de pourboire et le nombre de personnes – le calculateur affiche le pourboire, le total et la part par personne.",
        "form": """\
<form class="calc-form" data-calc="tip" novalidate>
  <div class="fields">
    <label>Addition<input type="text" inputmode="decimal" name="bill" placeholder="86,50"></label>
    <label>Pourboire (%)<input type="text" inputmode="decimal" name="pct" value="10"></label>
    <label>Personnes<input type="text" inputmode="numeric" name="people" placeholder="2"></label>
  </div>
  <dl class="result-list">
    <div><dt>Pourboire</dt><dd data-out="tip">–</dd></div>
    <div><dt>Total</dt><dd data-out="total">–</dd></div>
    <div><dt>Par personne</dt><dd data-out="person">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Quel pourboire laisser ?</h2>
<p>Les usages varient fortement selon les pays. En France, le service est compris dans l'addition (« service compris ») : le pourboire reste facultatif, souvent 5 à 10 % ou un arrondi pour un bon service. Aux États-Unis, 15 à 20 % sont attendus, car le pourboire constitue une part essentielle du revenu des serveurs.</p>
<p class="formula">pourboire = addition × pourcentage ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;par personne = (addition + pourboire) ÷ personnes</p>
<p>Exemple : pour une addition de 86,50 € avec 10 % de pourboire, vous laissez 8,65 €, soit 95,15 € au total. À deux, chacun paie 47,58 €. Astuce de calcul mental : décalez la virgule d'un rang vers la gauche pour obtenir 10 % ; 5 % en sont la moitié.</p>""",
        "faqs": [
            ("Quel pourboire laisser en France ?",
             "Le service est déjà compris dans l'addition. Le pourboire reste un geste facultatif : quelques pièces ou 5 à 10 % pour un bon service sont appréciés, mais rien n'est obligatoire."),
            ("Comment calculer 10 % de pourboire de tête ?",
             "Décalez la virgule du montant d'un rang vers la gauche : 10 % de 86,50 € font 8,65 €. Pour 5 %, prenez la moitié ; pour 20 %, doublez."),
            ("Le pourboire se calcule-t-il avant ou après la TVA ?",
             "En Europe, les prix affichés incluent la TVA : le pourboire se calcule simplement sur le montant final de l'addition. C'est aussi ce que fait ce calculateur."),
        ],
    },

    "date": {
        "slug": "jours-entre-deux-dates",
        "name": "Jours entre deux dates",
        "title": "Jours entre deux dates – Calculateur de durée | CalcMate",
        "desc": "Comptez les jours entre deux dates en ligne : choisissez les dates de début et de fin et obtenez la différence en jours et en semaines. Gratuit.",
        "h1": "Jours entre deux dates",
        "card": "Compter les jours et les semaines entre deux dates.",
        "intro": "Combien de jours séparent deux dates ? Choisissez la date de début et la date de fin – le calculateur compte les jours calendaires et les convertit en semaines. Pratique pour les délais, les vacances, les comptes à rebours ou la gestion de projet.",
        "form": """\
<form class="calc-form" data-calc="datediff" novalidate>
  <div class="fields">
    <label>Date de début<input type="date" name="start"></label>
    <label>Date de fin<input type="date" name="end"></label>
  </div>
  <dl class="result-list">
    <div><dt>Jours</dt><dd data-out="days">–</dd></div>
    <div><dt>Semaines</dt><dd data-out="weeks">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Comment le calculateur compte-t-il les jours ?</h2>
<p>Le calculateur détermine la différence calendaire réelle entre les deux dates – les années bissextiles et les longueurs de mois différentes sont prises en compte automatiquement. La date de fin n'est pas comptée : du 1er au 2 janvier, il y a 1 jour.</p>
<p class="formula">1er janvier 2026 → 1er mars 2026 = 59 jours (31 jours de janvier + 28 jours de février)</p>
<p>Si la date de fin doit compter aussi (par exemple « vacances du 5 au 9 août : combien de jours de congé ? »), ajoutez simplement 1 au résultat : 4 + 1 = 5 jours. Pour les délais juridiques, l'une ou l'autre convention peut s'appliquer selon les règles en vigueur – vérifiez le texte applicable en cas de doute.</p>""",
        "faqs": [
            ("La date de fin est-elle comptée ?",
             "Non, le calculateur affiche la différence entre les deux dates : du 1er au 2 janvier, il y a 1 jour. Si la date de fin doit être incluse, ajoutez 1 au résultat."),
            ("Les années bissextiles sont-elles prises en compte ?",
             "Oui. Le calcul repose sur de vraies dates calendaires : années bissextiles et longueurs de mois variables sont automatiquement correctes."),
            ("Combien de jours compte une année ?",
             "Une année normale compte 365 jours, une année bissextile 366. Sont bissextiles les années divisibles par 4 – mais les siècles pleins uniquement s'ils sont divisibles par 400 (2000 était bissextile, 2100 ne le sera pas)."),
        ],
    },
}
