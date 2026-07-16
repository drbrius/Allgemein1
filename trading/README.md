# Nasdaq 100 & US30 Trading Strategies

Two rules-based, long-only strategies for the Nasdaq 100 (NAS100/NQ) and the
Dow Jones Industrial Average (US30/YM), backtested on free Yahoo Finance data:

1. **Daily mean reversion** (`strategy.py`) - multi-day swing trades,
   daily bars since 1985 (NDX) / 1992 (DJI).
2. **Intraday sniper** (`sniper.py`) - one precise strike at the open,
   never held longer than 5 hours, hourly bars (~3 years, all Yahoo serves).

## Strategy 1: daily mean reversion

### Rules

| Rule | Definition |
|---|---|
| Trend filter | Close above the 200-day SMA (trade only with the long-term uptrend) |
| Entry | RSI(2) closes below 5 (a short, sharp pullback inside the uptrend) |
| Exit | RSI(2) closes above 65, **or** close crosses back above the 5-day SMA |
| Time stop | Exit after 10 trading days if neither exit has fired |
| Stop loss | Exit if the close falls 8% below the entry price (catastrophe guard) |
| Sizing | 100% of equity per trade, long only, no leverage |
| Costs | 2 bps per side (slippage + commission) |

The rules are the classic Connors-style RSI-2 pullback structure: equity
indices in uptrends tend to snap back after two or three hard down days.
Signals are evaluated and filled on the daily close.

### Backtest results (full sample, 2 bps/side costs)

| Metric | Nasdaq 100 (1985-2026) | US30 (1992-2026) |
|---|---|---|
| Trades | 166 | 143 |
| **Win rate** | **75.9%** | **75.5%** |
| Profit factor | 1.98 | 1.80 |
| Expectancy per trade | +0.64% | +0.36% |
| Avg win / avg loss | +1.71% / −2.73% | +1.07% / −1.84% |
| Avg holding time | 3.5 days | 3.6 days |
| Max drawdown | −23.9% | −15.3% |
| Time in market | 7.3% | 7.7% |

Robustness check on the 2016+ segment: Nasdaq 100 held up strongly
(81.0% win rate, profit factor 3.08); US30 softened but stayed profitable
(72.0% win rate, profit factor 1.37). Full tables incl. in-sample/out-of-sample
splits are in [`results/report.md`](results/report.md), and every individual
trade is listed in `results/*_trades.csv`.

## Strategy 2: intraday sniper (max 5-hour hold)

### Rules

| Rule | Definition |
|---|---|
| Setup (daily) | Yesterday closed with daily RSI(2) < 10 while above the 200-day SMA |
| Entry | Buy the next session's 9:30 open (market-on-open; signal known at prior close) |
| Target | +0.5% above the entry open (limit order) |
| Stop loss | −2.5% below the entry open |
| Time stop | Exit at the close of the 5th hourly bar (14:30) — **never held > 5 hours, never overnight** |
| Sizing / costs | 100% of equity per trade, long only, 2 bps per side |

The setup is the daily strategy's oversold condition; the sniper only harvests
the first morning of the snapback. Intrabar stop/target conflicts are resolved
pessimistically (stop assumed to fill first).

### Backtest results (hourly data, Aug 2023 – Jul 2026)

| Metric | Nasdaq 100 | US30 |
|---|---|---|
| Trades | 58 | 59 |
| **Win rate** | **75.9%** | 61.0% |
| Profit factor | 1.76 | 1.38 |
| Expectancy per trade | +0.15% | +0.07% |
| Avg win / avg loss | +0.45% / −0.80% | +0.41% / −0.47% |
| Avg hold | 2.6 h | 3.3 h |
| Max drawdown | −2.7% | −3.2% |
| Sharpe (annualized) | 1.10 | 0.77 |

Split check (pre/post Sep 2025): Nasdaq 100 was stable — 76.7% / 73.3% win
rate, profit factor 1.73 / 1.84. **US30 did not validate**: 54.5% win rate and
breakeven profit factor in the earlier segment. The post-oversold morning
drift is weak on the Dow; treat this as a Nasdaq-only strategy.

Also tested and **rejected** (no edge after costs on this data): pure hourly
RSI-2 mean reversion with hourly trend filters, morning-only dip entries, and
fading small opening gap-downs. This matches the documented pattern that
index returns accrue mostly overnight — the cash session alone has little
long drift, which is exactly what a ≤5h intraday strategy is confined to.
Full tables in [`results/sniper_report.md`](results/sniper_report.md), trades
in `results/*_sniper_trades.csv`.

## How to run

```bash
pip install -r requirements.txt
python3 download_data.py          # refresh daily + hourly CSVs from Yahoo Finance
python3 run_backtest.py           # daily strategy -> results/report.md
python3 run_sniper_backtest.py    # sniper strategy -> results/sniper_report.md
```

## Honest limitations — read before trading this

- **A 75% win rate is not the same as profitability.** Both strategies win
  often precisely because their average loss is larger than their average win
  (the sniper's 0.5% target vs 2.5% stop makes this explicit). The edge lives
  in the profit factor being above 1, not in the win rate. A win rate can
  always be pushed higher by taking tiny profits and huge losses — that is
  why both numbers are reported.
- **The sniper sample is small.** ~58 trades in under 3 years (Yahoo serves
  no more hourly history): a 75% win rate over 58 trades carries roughly a
  ±10-point confidence band. The daily strategy's 40-year sample is the
  stronger evidence; the sniper inherits its setup from it.
- **Low exposure, modest absolute return.** Capital is deployed only ~7% of
  days, so equity CAGR (~1.5–2.5%) is far below buy-and-hold. In practice this
  is used as a tactical overlay or scaled with futures/margin, which also
  scales the drawdowns.
- **Cash indices are not directly tradable.** Real fills on NQ/YM futures,
  QQQ/DIA ETFs, or CFDs will differ from index closes; CFD financing costs on
  multi-day holds are not modeled.
- **Tail risk is real.** Before the stop-loss rule, a single entry one week
  before the 1987 crash lost 35% — mean reversion sells insurance against
  panic, and occasionally the panic is justified. Gap risk means an 8% stop
  on close can still fill far below −8%.
- **Backtest ≠ future.** Results come from one historical path; the US30
  edge has weakened since 2016. Past performance does not guarantee future
  results. This is research code for educational purposes, not investment
  advice.
