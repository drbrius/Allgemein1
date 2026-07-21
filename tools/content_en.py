# -*- coding: utf-8 -*-
"""English content for CalcMate. Consumed by tools/build.py."""

SITE = {
    "title": "Free Online Calculators – Percentage, VAT, Loan, BMI &amp; More | CalcMate",
    "desc": "Free online calculators, no sign-up needed: percentage, VAT, discount, loan, fuel cost, tip, days between dates, rule of three, slope, BMI and compound interest.",
    "app_name": "CalcMate – Free Online Calculators",
    "app_desc": "Free online calculators without sign-up: basic calculator, percentage, VAT, discount, rule of three, slope, BMI, compound interest, loan, fuel cost, tip and days between dates.",
    "hub_h1": "Free Online Calculators – Fast, Modern, No Sign-Up",
    "hub_intro": "Everyday calculations made simple: percentages, VAT, discounts, loans, fuel costs, BMI, compound interest, days between dates and more – all free, directly in your browser.",
    "home": "Home",
    "faq_title": "Frequently Asked Questions",
    "related_title": "Related calculators",
    "lang_nav_label": "Languages",
    "footer": "© 2026 CalcMate – free online calculators. All results are provided without guarantee.",
    "hub_faqs": [
        ("Are these online calculators free?",
         "Yes, all calculators on CalcMate are completely free. There is no registration, no login and no hidden cost – just open the page and start calculating."),
        ("How do I calculate a percentage of a number?",
         "Multiply the number by the percentage and divide by 100. For example, 20% of 150 is 150 × 20 ÷ 100 = 30. Our percentage calculator does this instantly for you."),
        ("How is VAT calculated?",
         "To add VAT, multiply the net price by (1 + VAT rate ÷ 100). To remove VAT from a gross price, divide by the same factor. The VAT calculator handles both directions automatically."),
        ("How is a monthly loan payment calculated?",
         "For a fixed-rate loan: payment = principal × monthly rate ÷ (1 − (1 + monthly rate)^−months). The loan calculator shows the monthly payment, total repayment and interest cost at a glance."),
        ("How is the BMI calculated?",
         "The body mass index is your weight in kilograms divided by the square of your height in metres: BMI = kg / m². A BMI between 18.5 and 25 is considered normal weight."),
    ],
    "i18n": {
        "error": "Error",
        "bmi_label": "BMI",
        "bmi_under": "Underweight",
        "bmi_normal": "Normal weight",
        "bmi_over": "Overweight",
        "bmi_obese": "Obesity",
        "weeks": "weeks",
        "days": "days",
    },
}

CALCS = {

    "calculator": {
        "slug": "calculator",
        "name": "Calculator",
        "title": "Online Calculator – Free Basic Calculator | CalcMate",
        "desc": "Free online calculator with parentheses and percent: add, subtract, multiply and divide directly in your browser – no sign-up, no download.",
        "h1": "Online Calculator",
        "card": "Basic arithmetic with parentheses and percent – right in your browser.",
        "intro": "A free basic calculator for addition, subtraction, multiplication and division – with parentheses and percent. Type an expression or use the keypad, then press <kbd>=</kbd> or Enter.",
        "form": """\
<div class="calculator" data-calculator>
  <input class="calc-display" type="text" inputmode="decimal" aria-label="Calculator display" placeholder="0" autocomplete="off">
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
    <button type="button" data-key=".">.</button>
    <button type="button" class="op" data-key="%">%</button>
    <button type="button" class="op" data-key="+">+</button>
    <button type="button" class="equals" data-key="=">=</button>
  </div>
</div>""",
        "seo": """\
<h2>How the online calculator works</h2>
<p>The calculator handles the four basic operations, parentheses and percent, and follows the standard order of operations: multiplication and division are evaluated before addition and subtraction, and parentheses always take precedence. You can type a complete expression and evaluate it at the end.</p>
<p class="formula">(12 + 8) × 2.5 = 50&nbsp;&nbsp;·&nbsp;&nbsp;200 − 15% = 200 − 0.15 × 200 = 170</p>
<p>The percent key converts the number before it into hundredths: 15% becomes 0.15, so you can apply surcharges and reductions directly inside an expression. Both the decimal point and the decimal comma are accepted.</p>""",
        "faqs": [
            ("Does the calculator follow the order of operations?",
             "Yes. Multiplication and division are evaluated before addition and subtraction, and parentheses always come first. So 2 + 3 × 4 equals 14, while (2 + 3) × 4 equals 20."),
            ("How does the percent key work?",
             "The % key divides the preceding number by 100, so 50% becomes 0.5. For example, entering 80 × 25% gives 20."),
            ("Can I use my keyboard?",
             "Yes. Click into the display and type your expression directly – digits, + − × ÷ (or * and /), parentheses and a decimal point. Press Enter or = to evaluate, and Escape to clear the display."),
        ],
    },

    "percentage": {
        "slug": "percentage-calculator",
        "name": "Percentage Calculator",
        "title": "Percentage Calculator – Work Out Percentages Online | CalcMate",
        "desc": "Percentage calculator online: find X% of a number, what percent X is of Y, and the percentage change between two values – with formulas and examples.",
        "h1": "Percentage Calculator",
        "card": "Percentage of a value, percent share and percentage change.",
        "intro": "Calculate percentages online: find a percentage of a value, work out what percent one number is of another, or determine the percentage increase or decrease between two values.",
        "form": """\
<div class="subform">
  <h3>What is X% of a value?</h3>
  <form class="calc-form" data-calc="pct-of" novalidate>
    <div class="fields">
      <label>Percent (%)<input type="text" inputmode="decimal" name="p" placeholder="20"></label>
      <label>Value<input type="text" inputmode="decimal" name="x" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>X is what percent of Y?</h3>
  <form class="calc-form" data-calc="pct-what" novalidate>
    <div class="fields">
      <label>Value X<input type="text" inputmode="decimal" name="x" placeholder="30"></label>
      <label>Base value Y<input type="text" inputmode="decimal" name="y" placeholder="150"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>

<div class="subform">
  <h3>Percentage change from A to B</h3>
  <form class="calc-form" data-calc="pct-change" novalidate>
    <div class="fields">
      <label>Initial value A<input type="text" inputmode="decimal" name="a" placeholder="100"></label>
      <label>New value B<input type="text" inputmode="decimal" name="b" placeholder="120"></label>
    </div>
    <output class="result" aria-live="polite"></output>
  </form>
</div>""",
        "seo": """\
<h2>Percentages: the three basic formulas</h2>
<p>Almost every percentage problem comes down to one of three questions: How much is X% of a value? What percent is X of Y? And by what percentage did a value change?</p>
<p class="formula">part = base × percent ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;percent = part ÷ base × 100</p>
<p>Examples: 20% of 150 is 150 × 20 ÷ 100 = 30. The number 30 is 30 ÷ 150 × 100 = 20% of 150. And if a price rises from 100 to 120, the change is (120 − 100) ÷ 100 × 100 = +20%.</p>
<p>Watch out with successive changes: a 20% increase followed by a 20% decrease does not return to the original value, because the second percentage applies to the new, higher base (100 → 120 → 96).</p>""",
        "faqs": [
            ("How do I calculate a percentage of a number?",
             "Multiply the number by the percentage and divide by 100. For example, 20% of 150 is 150 × 20 ÷ 100 = 30."),
            ("How do I work out what percent X is of Y?",
             "Divide X by Y and multiply by 100. For example, 30 out of 150 is 30 ÷ 150 × 100 = 20%."),
            ("How is percentage change calculated?",
             "Subtract the initial value from the new value, divide by the initial value and multiply by 100: (B − A) ÷ A × 100. From 100 to 120 that is +20%; from 120 to 100 it is −16.67%."),
        ],
    },

    "vat": {
        "slug": "vat-calculator",
        "name": "VAT Calculator",
        "title": "VAT Calculator – Add or Remove VAT (Net ↔ Gross) | CalcMate",
        "desc": "VAT calculator online: add VAT to a net price or remove VAT from a gross price at 20%, 19% or any custom rate – with formulas and examples.",
        "h1": "VAT Calculator",
        "card": "Add or remove VAT – net ↔ gross at any rate.",
        "intro": "Add or remove VAT in one step: convert net to gross or gross to net at any VAT rate. The standard rate in the United Kingdom is 20%, in Germany 19%, in France 20% and in Italy 22%.",
        "form": """\
<form class="calc-form" data-calc="vat" novalidate>
  <div class="fields">
    <label>Amount<input type="text" inputmode="decimal" name="amount" placeholder="100"></label>
    <label>VAT rate (%)<input type="text" inputmode="decimal" name="rate" value="20"></label>
  </div>
  <fieldset>
    <label><input type="radio" name="dir" value="net2gross" checked> Net → Gross (add VAT)</label>
    <label><input type="radio" name="dir" value="gross2net"> Gross → Net (remove VAT)</label>
  </fieldset>
  <dl class="result-list">
    <div><dt>Net</dt><dd data-out="net">–</dd></div>
    <div><dt>VAT</dt><dd data-out="vat">–</dd></div>
    <div><dt>Gross</dt><dd data-out="gross">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>How to calculate VAT</h2>
<p>A single factor converts a net price into a gross price. At a 20% VAT rate that factor is 1.20; at 19% it is 1.19.</p>
<p class="formula">gross = net × (1 + rate ÷ 100)&nbsp;&nbsp;·&nbsp;&nbsp;net = gross ÷ (1 + rate ÷ 100)</p>
<p>Example: 100 net at 20% VAT gives a gross price of 120, and the VAT amount is 20. Conversely, a gross price of 120 contains 120 ÷ 1.20 = 100 net. A common mistake is subtracting 20% from the gross price – that gives too little, because the 20% applies to the net amount, not the gross.</p>
<p>Standard rates differ by country: 20% in the UK and France, 19% in Germany, 22% in Italy, 8.1% in Switzerland. Many countries also apply reduced rates to essentials such as food, books and public transport.</p>""",
        "faqs": [
            ("How is VAT calculated?",
             "To add VAT, multiply the net price by (1 + VAT rate ÷ 100) – at 20% that means multiplying by 1.20. To remove VAT from a gross price, divide by the same factor."),
            ("How do I remove VAT from a gross price?",
             "Divide the gross price by 1.20 at a 20% rate (or 1.19 at 19%). Example: 120 gross ÷ 1.20 = 100 net, so the VAT amount is 20. Simply subtracting 20% from the gross would be wrong."),
            ("What are the standard VAT rates in Europe?",
             "The United Kingdom and France use 20%, Germany 19%, Italy 22%, Spain 21% and Switzerland 8.1%. Most countries also have reduced rates for essentials such as food and books."),
        ],
    },

    "discount": {
        "slug": "discount-calculator",
        "name": "Discount Calculator",
        "title": "Discount Calculator – Price After Discount | CalcMate",
        "desc": "Discount calculator online: how much do you save with X% off and what does the item cost afterwards? Free, with formula and examples.",
        "h1": "Discount Calculator",
        "card": "Savings and final price after X% off.",
        "intro": "Work out in seconds how much you save with a discount and what the item costs after the reduction: just enter the price and the discount percentage.",
        "form": """\
<form class="calc-form" data-calc="discount" novalidate>
  <div class="fields">
    <label>Price<input type="text" inputmode="decimal" name="price" placeholder="80"></label>
    <label>Discount (%)<input type="text" inputmode="decimal" name="pct" placeholder="25"></label>
  </div>
  <dl class="result-list">
    <div><dt>You save</dt><dd data-out="saved">–</dd></div>
    <div><dt>Final price</dt><dd data-out="final">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>How to calculate a discount</h2>
<p>A discount is a percentage reduction of the original price. The savings and the final price follow from two simple formulas:</p>
<p class="formula">savings = price × discount ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;final price = price − savings</p>
<p>Example: a sweater costs 80 and is 25% off. The savings are 80 × 25 ÷ 100 = 20, so the final price is 60. Handy mental shortcuts: 25% is a quarter, 50% is half and 10% is a tenth of the price.</p>
<p>Be careful with stacked discounts: “20% + 10% off” is not 30% off. The second discount applies to the already reduced price – 100 becomes 80, then 72, an overall reduction of 28%.</p>""",
        "faqs": [
            ("How do I calculate a discount?",
             "Multiply the price by the discount percentage and divide by 100 – that is your savings. The final price is the original price minus the savings. Example: 80 with 25% off = 20 saved, 60 to pay."),
            ("What does an item cost after 20% off?",
             "Multiply the price by 0.8. Example: 50 × 0.8 = 40. In general: final price = original price × (1 − discount ÷ 100)."),
            ("How do stacked discounts like 20% + 10% work?",
             "The discounts are applied one after another, not added. 100 becomes 80 after 20% off, then 72 after a further 10% off. The total discount is 28%, not 30%."),
        ],
    },

    "rule3": {
        "slug": "rule-of-three",
        "name": "Rule of Three",
        "title": "Rule of Three Calculator – Solve Proportions Online | CalcMate",
        "desc": "Rule of three calculator: solve direct and inverse proportions online. If A corresponds to B, what does C correspond to? Free, with formulas and examples.",
        "h1": "Rule of Three Calculator",
        "card": "Solve direct and inverse proportions in seconds.",
        "intro": "Solve proportions in seconds: if A corresponds to B, what does C correspond to? Ideal for recipes, prices, speeds and unit conversions. Tick the box for inversely proportional relationships (more workers → less time).",
        "form": """\
<form class="calc-form" data-calc="rule3" novalidate>
  <div class="fields">
    <label>A<input type="text" inputmode="decimal" name="a" placeholder="4"></label>
    <label>corresponds to B<input type="text" inputmode="decimal" name="b" placeholder="12"></label>
    <label>C<input type="text" inputmode="decimal" name="c" placeholder="7"></label>
  </div>
  <fieldset>
    <label class="check"><input type="checkbox" name="inverse"> Inversely proportional</label>
  </fieldset>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>How the rule of three works</h2>
<p>The rule of three reduces a known relationship (“A corresponds to B”) to one unit and then scales it up to the quantity you are looking for. In a direct proportion both quantities grow together; in an inverse proportion one goes down as the other goes up.</p>
<p class="formula">direct: X = B × C ÷ A&nbsp;&nbsp;·&nbsp;&nbsp;inverse: X = A × B ÷ C</p>
<p>Direct example: 4 apples cost 12. What do 7 apples cost? X = 12 × 7 ÷ 4 = 21. Inverse example: 4 painters need 12 hours. How long do 6 painters need? X = 4 × 12 ÷ 6 = 8 hours.</p>""",
        "faqs": [
            ("How does the rule of three work?",
             "First scale down to one unit, then scale up to the quantity you need. If 4 apples cost 12, one apple costs 3 and 7 apples cost 21. As a formula: X = B × C ÷ A."),
            ("What is an inverse rule of three?",
             "In an inverse proportion one quantity decreases as the other increases – more workers, less time. The formula becomes X = A × B ÷ C: if 4 painters need 12 hours, 6 painters finish in 8 hours."),
            ("What is the rule of three used for in everyday life?",
             "Scaling recipes to a different number of servings, comparing prices per kilo or litre, converting speeds and units, estimating material needs or working time – anywhere two quantities stand in a fixed ratio."),
        ],
    },

    "slope": {
        "slug": "slope-calculator",
        "name": "Slope Calculator",
        "title": "Slope Calculator – Percent &amp; Degrees | CalcMate",
        "desc": "Calculate a slope or gradient online: get percent and degrees from length and height, or convert between percent and degrees. With triangle diagram.",
        "h1": "Slope Calculator",
        "card": "Slope and gradient in percent and degrees – with diagram.",
        "intro": "Work out a slope or gradient in percent and degrees – from the horizontal length and the height (rise). Alternatively, enter the slope directly in percent or degrees to convert between the two. Handy for roofs, ramps, roads and drainage pipes.",
        "form": """\
<svg class="slope-figure" viewBox="0 0 360 190" role="img" aria-label="Right triangle: horizontal length at the bottom, height on the right, angle α on the left">
  <polygon points="30,160 310,160 310,50" fill="#eef2fc"/>
  <line x1="30" y1="160" x2="310" y2="160" stroke="#1c2430" stroke-width="2"/>
  <line x1="310" y1="160" x2="310" y2="50" stroke="#1c2430" stroke-width="2"/>
  <line x1="30" y1="160" x2="310" y2="50" stroke="#4f6df5" stroke-width="2.5"/>
  <path d="M 296 160 L 296 146 L 310 146" fill="none" stroke="#9aa3b5" stroke-width="1.5"/>
  <path d="M 64 160 A 34 34 0 0 0 61.6 147.6" fill="none" stroke="#6b7385" stroke-width="1.5"/>
  <text x="78" y="156" font-size="14" fill="#6b7385">α</text>
  <text x="170" y="182" font-size="14" fill="#6b7385" text-anchor="middle">Length</text>
  <text x="318" y="110" font-size="14" fill="#6b7385">Height</text>
</svg>
<form class="calc-form" data-calc="slope" novalidate>
  <fieldset>
    <label><input type="radio" name="mode" value="lh" checked> Length &amp; height</label>
    <label><input type="radio" name="mode" value="pct"> Slope in %</label>
    <label><input type="radio" name="mode" value="deg"> Angle in degrees</label>
  </fieldset>
  <div class="fields">
    <label data-field="pct" hidden>Slope (%)<input type="text" inputmode="decimal" name="pct" placeholder="12"></label>
    <label data-field="deg" hidden>Angle (°)<input type="text" inputmode="decimal" name="deg" placeholder="6.84"></label>
    <label data-field="len">Length (m)<input type="text" inputmode="decimal" name="len" placeholder="100"></label>
    <label data-field="height">Height (m)<input type="text" inputmode="decimal" name="height" placeholder="12"></label>
  </div>
  <dl class="result-list">
    <div><dt>Slope</dt><dd data-out="percent">–</dd></div>
    <div><dt>Angle α</dt><dd data-out="angle">–</dd></div>
    <div><dt>Height (m)</dt><dd data-out="height">–</dd></div>
    <div><dt>Slope length (m)</dt><dd data-out="hyp">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>Slope in percent and degrees</h2>
<p>The slope in percent tells you how many metres of rise there are per 100 metres of horizontal length. The angle is the arctangent of the same ratio.</p>
<p class="formula">slope (%) = height ÷ length × 100&nbsp;&nbsp;·&nbsp;&nbsp;angle α = arctan(height ÷ length)</p>
<p>Example: a rise of 12 m over a horizontal length of 100 m is a 12% slope with an angle of about 6.84°. The slope length (hypotenuse) follows from the Pythagorean theorem: √(100² + 12²) ≈ 100.72 m.</p>
<p>Typical reference values: drainage pipes need at least a 1–2% fall, accessible ramps should not exceed a 6% gradient, and a 100% slope corresponds to exactly 45°.</p>""",
        "faqs": [
            ("How do you calculate a slope in percent?",
             "Divide the height (rise) by the horizontal length and multiply by 100: slope (%) = height ÷ length × 100. For example, a rise of 12 m over a length of 100 m is a 12% slope."),
            ("How do you convert a slope in percent to degrees?",
             "The angle is the arctangent of the ratio: α = arctan(percent ÷ 100). A 12% slope corresponds to arctan(0.12) ≈ 6.84°, and 100% corresponds to exactly 45°."),
            ("What does a 100% slope mean?",
             "At a 100% slope the rise equals the horizontal distance – that is an angle of 45°, not a vertical wall."),
        ],
    },

    "bmi": {
        "slug": "bmi-calculator",
        "name": "BMI Calculator",
        "title": "BMI Calculator – Body Mass Index | CalcMate",
        "desc": "Calculate your BMI online: body mass index from weight and height, with WHO categories from underweight to obesity. Free, no sign-up.",
        "h1": "BMI Calculator",
        "card": "Body mass index from weight and height – with category.",
        "intro": "Calculate your body mass index (BMI) from your weight and height. The BMI is a quick guide to healthy body weight: values between 18.5 and 25 are considered normal weight for adults.",
        "form": """\
<form class="calc-form" data-calc="bmi" novalidate>
  <div class="fields">
    <label>Weight (kg)<input type="text" inputmode="decimal" name="weight" placeholder="70"></label>
    <label>Height (cm)<input type="text" inputmode="decimal" name="height" placeholder="175"></label>
  </div>
  <output class="result" aria-live="polite"></output>
</form>""",
        "seo": """\
<h2>How the BMI is calculated</h2>
<p>The body mass index relates your weight to your height. It is defined by the World Health Organization (WHO) as a rough guide for adults.</p>
<p class="formula">BMI = weight (kg) ÷ height (m)²</p>
<p>Example: 70 kg at 1.75 m gives 70 ÷ (1.75 × 1.75) ≈ 22.9 – normal weight. The WHO categories: below 18.5 underweight, 18.5–24.9 normal weight, 25–29.9 overweight, 30 and above obesity.</p>
<p>The BMI does not distinguish between muscle and fat mass: athletic people with a lot of muscle can have a high BMI despite low body fat. Separate reference values apply to children, pregnant women and older people – when in doubt, seek medical advice.</p>""",
        "faqs": [
            ("How is the BMI calculated?",
             "The body mass index is your weight in kilograms divided by the square of your height in metres: BMI = kg / m². Example: 70 kg at 1.75 m gives a BMI of about 22.9."),
            ("What BMI is considered normal?",
             "According to the WHO, a BMI of 18.5 to 24.9 counts as normal weight for adults. Below 18.5 is underweight, 25 and above is overweight, and 30 and above is obesity."),
            ("How meaningful is the BMI?",
             "The BMI is only a rough guide. It does not distinguish muscle from fat and ignores age, sex and build. For a solid assessment, additional measurements and medical advice are recommended."),
        ],
    },

    "interest": {
        "slug": "compound-interest-calculator",
        "name": "Compound Interest",
        "title": "Compound Interest Calculator – Final Balance &amp; Interest | CalcMate",
        "desc": "Compound interest calculator: final balance and interest earned from starting capital, annual rate and term – with formula, example and the rule of 72.",
        "h1": "Compound Interest Calculator",
        "card": "Final balance and interest earned with compounding.",
        "intro": "See how your savings grow: enter a starting amount, an annual interest rate and a term in years to calculate the final balance including compound interest.",
        "form": """\
<form class="calc-form" data-calc="interest" novalidate>
  <div class="fields">
    <label>Starting capital<input type="text" inputmode="decimal" name="principal" placeholder="10000"></label>
    <label>Interest rate (% p.a.)<input type="text" inputmode="decimal" name="rate" placeholder="3"></label>
    <label>Term (years)<input type="text" inputmode="decimal" name="years" placeholder="10"></label>
  </div>
  <dl class="result-list">
    <div><dt>Final balance</dt><dd data-out="final">–</dd></div>
    <div><dt>Interest earned</dt><dd data-out="earned">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>The compound interest formula</h2>
<p>With compound interest, the interest earned in each period is added to the capital and earns interest itself in the following periods. The balance therefore grows exponentially rather than linearly.</p>
<p class="formula">final balance = starting capital × (1 + rate ÷ 100)^years</p>
<p>Example: 10,000 at 3% per year grows to 10,000 × 1.03¹⁰ ≈ 13,439.16 after 10 years – about 3,439 of interest. With simple interest (no compounding) it would only be 3,000.</p>
<p>Rule of thumb for doubling (“rule of 72”): divide 72 by the interest rate to get the approximate number of years until your capital doubles. At 6% that is about 12 years.</p>""",
        "faqs": [
            ("What is the compound interest effect?",
             "Interest is credited to the capital and earns interest itself in later years. The balance grows exponentially: 10,000 at 3% becomes about 13,439 after 10 years, versus 13,000 with simple interest."),
            ("What is the compound interest formula?",
             "Final balance = starting capital × (1 + rate ÷ 100) to the power of the number of years. Example: 10,000 × 1.03¹⁰ ≈ 13,439.16."),
            ("How long does it take to double my money?",
             "Use the rule of 72: divide 72 by the interest rate to estimate the years to double. At 6% it takes about 12 years; at 3% about 24 years."),
        ],
    },

    "loan": {
        "slug": "loan-calculator",
        "name": "Loan Calculator",
        "title": "Loan Calculator – Monthly Payment, Interest &amp; Total Cost | CalcMate",
        "desc": "Loan calculator online: monthly payment, total repayment and interest cost of a fixed-rate loan from amount, interest rate and term. Free, no sign-up.",
        "h1": "Loan Calculator",
        "card": "Monthly payment, total repayment and interest cost of a loan.",
        "intro": "Calculate the monthly payment for a fixed-rate (amortizing) loan: enter the loan amount, the annual interest rate and the term – the calculator shows the monthly payment, total repayment and interest cost.",
        "form": """\
<form class="calc-form" data-calc="loan" novalidate>
  <div class="fields">
    <label>Loan amount<input type="text" inputmode="decimal" name="principal" placeholder="20000"></label>
    <label>Interest rate (% p.a.)<input type="text" inputmode="decimal" name="rate" placeholder="5"></label>
    <label>Term (years)<input type="text" inputmode="decimal" name="years" placeholder="5"></label>
  </div>
  <dl class="result-list">
    <div><dt>Monthly payment</dt><dd data-out="monthly">–</dd></div>
    <div><dt>Total repayment</dt><dd data-out="total">–</dd></div>
    <div><dt>Interest cost</dt><dd data-out="interest">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>How the monthly payment is calculated</h2>
<p>With an amortizing fixed-rate loan the monthly payment stays constant over the whole term. Each payment consists of an interest portion and a principal portion; as the outstanding balance shrinks, the interest portion falls and the principal portion grows.</p>
<p class="formula">payment = principal × i ÷ (1 − (1 + i)^−n)&nbsp;&nbsp;where&nbsp;&nbsp;i = annual rate ÷ 12 ÷ 100, n = months</p>
<p>Example: 20,000 at 5% over 5 years (60 monthly payments) gives a payment of about 377.42. In total you repay about 22,645, so the interest cost is roughly 2,645.</p>
<p>Note: the calculator uses the nominal interest rate. Lenders also quote an APR (annual percentage rate) that includes fees and makes offers comparable. Shorter terms mean higher payments but considerably lower total interest.</p>""",
        "faqs": [
            ("How is a monthly loan payment calculated?",
             "With the annuity formula: payment = principal × monthly rate ÷ (1 − (1 + monthly rate)^−months). Example: 20,000 at 5% over 5 years gives about 377.42 per month."),
            ("What is the difference between the nominal rate and the APR?",
             "The nominal rate is the pure interest on the outstanding balance. The APR additionally includes fees and the timing of payments, which makes it the better figure for comparing loan offers."),
            ("How can I reduce the interest cost of a loan?",
             "Choose a shorter term, make extra repayments where allowed, compare offers by APR and only borrow what you really need. Even half a percentage point less interest saves a noticeable amount over the term."),
        ],
    },

    "fuel": {
        "slug": "fuel-cost-calculator",
        "name": "Fuel Cost Calculator",
        "title": "Fuel Cost Calculator – Cost of a Trip | CalcMate",
        "desc": "Fuel cost calculator: fuel needed and cost of a trip from distance, consumption per 100 km and fuel price – plus cost per 100 km. Free and fast.",
        "h1": "Fuel Cost Calculator",
        "card": "Fuel needed and cost of a trip from distance and consumption.",
        "intro": "What does the trip cost? Enter the distance, your car's average consumption and the fuel price to get the amount of fuel needed, the total cost and the cost per 100 km.",
        "form": """\
<form class="calc-form" data-calc="fuel" novalidate>
  <div class="fields">
    <label>Distance (km)<input type="text" inputmode="decimal" name="distance" placeholder="350"></label>
    <label>Consumption (l/100 km)<input type="text" inputmode="decimal" name="consumption" placeholder="6.5"></label>
    <label>Price per litre<input type="text" inputmode="decimal" name="price" placeholder="1.85"></label>
  </div>
  <dl class="result-list">
    <div><dt>Fuel (l)</dt><dd data-out="liters">–</dd></div>
    <div><dt>Cost</dt><dd data-out="cost">–</dd></div>
    <div><dt>Cost / 100 km</dt><dd data-out="per100">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>How to calculate fuel costs</h2>
<p>The cost of a trip follows from three inputs: the distance, your car's average consumption and the current fuel price.</p>
<p class="formula">cost = distance ÷ 100 × consumption × price per litre</p>
<p>Example: for 350 km at a consumption of 6.5 l/100 km you need 22.75 litres. At 1.85 per litre the trip costs about 42.09 – roughly 12.03 per 100 km.</p>
<p>Saving tips: drive smoothly and shift up early, remove unnecessary weight and roof racks, check your tyre pressure and compare fuel prices – stations can differ by more than 10 cents per litre. In a carpool, simply divide the total cost by the number of passengers.</p>""",
        "faqs": [
            ("How do I calculate the fuel cost of a trip?",
             "Divide the distance by 100, multiply by the consumption per 100 km and by the price per litre. Example: 350 km ÷ 100 × 6.5 l × 1.85 ≈ 42.09."),
            ("What does driving cost per 100 km?",
             "Simply multiply the consumption per 100 km by the fuel price. At 6.5 l/100 km and 1.85 per litre that is about 12.03 per 100 km."),
            ("How can I lower my fuel consumption?",
             "Drive smoothly, shift up early, keep tyres properly inflated, avoid unnecessary weight and roof attachments, and combine short trips. Together this often cuts consumption by 10–20%."),
        ],
    },

    "tip": {
        "slug": "tip-calculator",
        "name": "Tip Calculator",
        "title": "Tip Calculator – Tip &amp; Split the Bill | CalcMate",
        "desc": "Tip calculator online: work out the tip, the total and each person's share when splitting the bill – with common tipping percentages by country.",
        "h1": "Tip Calculator",
        "card": "Work out the tip and split the bill per person.",
        "intro": "How much should you tip and what does each person pay? Enter the bill amount, the tip percentage and the number of people – the calculator shows the tip, the total and the share per person.",
        "form": """\
<form class="calc-form" data-calc="tip" novalidate>
  <div class="fields">
    <label>Bill amount<input type="text" inputmode="decimal" name="bill" placeholder="86.50"></label>
    <label>Tip (%)<input type="text" inputmode="decimal" name="pct" value="15"></label>
    <label>People<input type="text" inputmode="numeric" name="people" placeholder="2"></label>
  </div>
  <dl class="result-list">
    <div><dt>Tip</dt><dd data-out="tip">–</dd></div>
    <div><dt>Total</dt><dd data-out="total">–</dd></div>
    <div><dt>Per person</dt><dd data-out="person">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>How much should you tip?</h2>
<p>Tipping customs vary widely. In the United States 15–20% is expected, since tips form a large part of servers' income. In the UK 10–12.5% is common if no service charge is included, while in much of continental Europe 5–10% or rounding up is perfectly polite.</p>
<p class="formula">tip = bill × percent ÷ 100&nbsp;&nbsp;·&nbsp;&nbsp;per person = (bill + tip) ÷ people</p>
<p>Example: on a bill of 86.50 with a 15% tip you add 12.98, making a total of 99.48. Split between two people, each pays 49.74. Mental shortcut: move the decimal point one place to the left for 10%, then adjust – add half of that again for 15%, or double it for 20%.</p>""",
        "faqs": [
            ("How much do you tip in the USA?",
             "In restaurants 15–20% of the pre-tax bill is standard, with 18–20% common for good service. Tipping much less is generally considered rude, as tips are a core part of servers' pay."),
            ("How do I quickly work out a 15% or 20% tip in my head?",
             "Move the decimal point one place left to get 10% – for 86.50 that is 8.65. Add half of that again for 15% (about 12.98), or double it for 20% (17.30)."),
            ("Should the tip be calculated before or after tax?",
             "In the US it is customary to tip on the pre-tax amount, though many people simply tip on the total. In most European countries the bill already includes VAT and the tip is given on the final amount."),
        ],
    },

    "date": {
        "slug": "days-between-dates",
        "name": "Days Between Dates",
        "title": "Days Between Dates – Date Difference Calculator | CalcMate",
        "desc": "Count the days between two dates online: pick a start and end date to get the difference in days and weeks – free, with leap years handled correctly.",
        "h1": "Days Between Dates",
        "card": "Count the days and weeks between two dates.",
        "intro": "How many days are there between two dates? Pick a start and an end date – the calculator counts the calendar days and converts them into weeks. Handy for deadlines, holidays, countdowns and project planning.",
        "form": """\
<form class="calc-form" data-calc="datediff" novalidate>
  <div class="fields">
    <label>Start date<input type="date" name="start"></label>
    <label>End date<input type="date" name="end"></label>
  </div>
  <dl class="result-list">
    <div><dt>Days</dt><dd data-out="days">–</dd></div>
    <div><dt>Weeks</dt><dd data-out="weeks">–</dd></div>
  </dl>
</form>""",
        "seo": """\
<h2>How the day counter works</h2>
<p>The calculator determines the true calendar difference between the two dates – leap years and the different month lengths are handled automatically. The end date is not counted: from 1 January to 2 January is 1 day.</p>
<p class="formula">1 January 2026 → 1 March 2026 = 59 days (31 days of January + 28 days of February)</p>
<p>If the end date should count as well (for example, “holiday from 5 to 9 August – how many days off?”), simply add 1 to the result: 4 + 1 = 5 days. For legal deadlines, either counting convention may apply depending on the jurisdiction – check the applicable rules when it matters.</p>""",
        "faqs": [
            ("Is the end date included in the count?",
             "No, the calculator shows the difference between the two dates: from 1 January to 2 January is 1 day. If the end date should be included, add 1 to the result."),
            ("Does the calculator account for leap years?",
             "Yes. It works with real calendar dates, so leap years and varying month lengths are automatically handled correctly."),
            ("How many days are there in a year?",
             "A common year has 365 days, a leap year 366. Leap years are years divisible by 4 – but full centuries only if they are divisible by 400 (2000 was a leap year, 2100 will not be)."),
        ],
    },
}
