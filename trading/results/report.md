# Mean-Reversion Backtest Report

**Strategy:** SMA200 trend / RSI2<5 entry / RSI>65 or close>SMA5 exit / 10d time stop / 8% stop loss
**Execution:** fills at the signal bar's close, 2 bps cost per side, 100% of equity per trade, long only, no leverage.
**Sample split:** the 2016-01-01+ segment is shown separately as a robustness check (parameters follow the published Connors RSI-2 family rather than a fit to this data).

## Nasdaq 100 (^NDX)

Data: 1985-10-01 to 2026-07-16, 10276 daily bars (Yahoo Finance).

| metric | full sample | in-sample (< 2016) | out-of-sample (>= 2016) |
|---|---|---|---|
| trades | 166 | 121 | 42 |
| win_rate_pct | 75.9 | 75.2 | 81.0 |
| avg_win_pct | 1.71 | 1.86 | 1.33 |
| avg_loss_pct | -2.73 | -3.03 | -1.84 |
| profit_factor | 1.98 | 1.86 | 3.08 |
| expectancy_pct | 0.64 | 0.65 | 0.73 |
| avg_bars_held | 3.5 | 3.4 | 3.3 |
| strategy_cagr_pct | 2.52 | 2.47 | 3.12 |
| buyhold_cagr_pct | 14.14 | 12.38 | 20.37 |
| max_drawdown_pct | -23.9 | -23.9 | -8.7 |
| buyhold_max_dd_pct | -82.9 | -82.9 | -35.6 |
| exposure_pct | 7.3 | 7.2 | 7.3 |
| sharpe | 0.41 | 0.39 | 0.52 |

## US30 / Dow Jones (^DJI)

Data: 1992-01-02 to 2026-07-16, 8695 daily bars (Yahoo Finance).

| metric | full sample | in-sample (< 2016) | out-of-sample (>= 2016) |
|---|---|---|---|
| trades | 143 | 89 | 50 |
| win_rate_pct | 75.5 | 76.4 | 72.0 |
| avg_win_pct | 1.07 | 1.14 | 1.01 |
| avg_loss_pct | -1.84 | -1.8 | -1.89 |
| profit_factor | 1.8 | 2.04 | 1.37 |
| expectancy_pct | 0.36 | 0.44 | 0.19 |
| avg_bars_held | 3.6 | 3.7 | 3.6 |
| strategy_cagr_pct | 1.46 | 1.64 | 0.91 |
| buyhold_cagr_pct | 8.66 | 7.58 | 11.59 |
| max_drawdown_pct | -15.3 | -15.3 | -12.5 |
| buyhold_max_dd_pct | -53.8 | -53.8 | -37.1 |
| exposure_pct | 7.7 | 7.1 | 9.4 |
| sharpe | 0.38 | 0.46 | 0.21 |

## How to read these numbers

- **Win rate** counts profitable trades. Mean reversion wins often but its average loss is larger than its average win - profit factor > 1 is what makes it net profitable.
- **Exposure** is low (capital is in the market only a small fraction of days); CAGR on total equity is therefore modest even when per-trade edge is strong. Practitioners run this as an overlay on cash or scale it with futures.
- Past performance does not guarantee future results. This is research code, not investment advice.
