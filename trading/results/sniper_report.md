# Intraday Sniper Backtest Report

**Strategy:** daily RSI2<10 above SMA200 setup / buy next open / +0.5% target / -2.5% stop / 5h max hold, no overnight
**Execution:** entry at the session open, 2 bps cost per side, 100% of equity per trade, long only, no leverage. Intrabar stop/target conflicts resolve pessimistically (stop first).
**Sample split:** the 2025-09-01+ segment is shown separately as a robustness check. Yahoo serves only ~730 trading days of hourly data, so the whole window is short - treat every number here with wider error bars than the daily report's.

## Nasdaq 100 (^NDX)

Hourly data: 2023-08-17 to 2026-07-16, 5075 bars (Yahoo Finance).

| metric | full sample | pre 2025-09-01 | post 2025-09-01 |
|---|---|---|---|
| trades | 58 | 43 | 15 |
| win_rate_pct | 75.9 | 76.7 | 73.3 |
| avg_win_pct | 0.45 | 0.45 | 0.44 |
| avg_loss_pct | -0.8 | -0.86 | -0.65 |
| profit_factor | 1.76 | 1.73 | 1.84 |
| expectancy_pct | 0.15 | 0.15 | 0.15 |
| strategy_cagr_pct | 2.91 | 3.09 | 2.52 |
| buyhold_cagr_pct | 26.54 | 25.67 | 30.2 |
| max_drawdown_pct | -2.7 | -2.7 | -1.6 |
| buyhold_max_dd_pct | -22.9 | -22.9 | -12.1 |
| exposure_pct | 7.9 | 8.4 | 6.8 |
| sharpe | 1.1 | 1.11 | 1.08 |
| avg_hold_hours | 2.6 | 2.5 | 2.8 |

## US30 / Dow Jones (^DJI)

Hourly data: 2023-08-17 to 2026-07-16, 5075 bars (Yahoo Finance).

| metric | full sample | pre 2025-09-01 | post 2025-09-01 |
|---|---|---|---|
| trades | 59 | 44 | 15 |
| win_rate_pct | 61.0 | 54.5 | 80.0 |
| avg_win_pct | 0.41 | 0.39 | 0.46 |
| avg_loss_pct | -0.47 | -0.47 | -0.45 |
| profit_factor | 1.38 | 0.99 | 4.07 |
| expectancy_pct | 0.07 | -0.0 | 0.28 |
| strategy_cagr_pct | 1.58 | 0.22 | 4.86 |
| buyhold_cagr_pct | 15.66 | 14.69 | 18.98 |
| max_drawdown_pct | -3.2 | -3.2 | -0.8 |
| buyhold_max_dd_pct | -16.3 | -16.3 | -10.0 |
| exposure_pct | 7.9 | 8.4 | 6.8 |
| sharpe | 0.77 | 0.11 | 2.54 |
| avg_hold_hours | 3.3 | 3.7 | 2.2 |

## Validation verdict

- **Nasdaq 100: validated.** Win rate held near 75% in both sub-periods with a profit factor well above 1.
- **US30: NOT validated.** The full-sample win rate stays around 60% and the pre-split segment is roughly breakeven. The post-oversold morning drift is weak on the Dow in this window - do not trade this setup on US30 expecting the Nasdaq's statistics.

## What was tested and rejected first

Pure intraday variants had no edge after costs on this data (profit factors at or below 1.0 across in/out-of-sample splits) and are not implemented:

- Hourly RSI(2) mean reversion with hourly SMA trend filters (the daily edge does not survive a same-day forced exit),
- the same restricted to morning entries with a daily trend filter,
- fading small opening gap-downs toward the prior close.

This matches the well-documented pattern that index returns accrue mostly overnight; the cash session alone offers little long drift to harvest.

## Caveats

- ~58 trades per index in under 3 years: small sample, wide confidence bands. A 75% win rate over 58 trades has a ~90% band of roughly +/-10 points.
- The 0.5% target vs 2.5% stop asymmetry makes the high win rate partly mechanical; the profit factor is the evidence of edge, not the win rate.
- Cash-index opens are idealized fills; real fills on futures/ETFs at the open auction will differ. Past performance does not guarantee future results. Research code, not investment advice.
