# Nasdaq 100 & US30 Mean-Reversion Strategy

A rules-based, long-only mean-reversion strategy for the Nasdaq 100 (NAS100/NQ)
and the Dow Jones Industrial Average (US30/YM), backtested on free daily data
from Yahoo Finance (Nasdaq 100 since 1985, US30 since 1992).

## Strategy rules

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

## Backtest results (full sample, 2 bps/side costs)

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

## How to run

```bash
pip install -r requirements.txt
python3 download_data.py   # refresh CSVs in data/ from Yahoo Finance
python3 run_backtest.py    # prints stats, rewrites results/
```

## Honest limitations — read before trading this

- **A 75% win rate is not the same as profitability.** This strategy wins
  often precisely because its average loss (−2.7% / −1.8%) is larger than its
  average win (+1.7% / +1.1%). The edge lives in the profit factor being
  above 1, not in the win rate. A win rate can always be pushed higher by
  taking tiny profits and huge losses — that is why both numbers are reported.
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
