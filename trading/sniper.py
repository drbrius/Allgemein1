"""Intraday "sniper" strategy - daily oversold setup, next-morning strike, max 5h hold.

The pure intraday variants tested first (hourly RSI-2 mean reversion with
trend filters, morning-dip entries, opening gap fades) all came out at or
below breakeven after costs on 2023-2026 hourly data - equity index drift
accrues overnight, so the cash session itself offers almost no long edge.
What does survive validation is combining timeframes:

  Setup (daily)   : yesterday's close is deeply oversold - RSI(2) < 10 -
                    while still above the 200-day SMA (same edge family as
                    the daily strategy in strategy.py)
  Entry (intraday): buy the next session's 9:30 open (market-on-open order;
                    the signal is known at the prior close)
  Target          : +0.5% above the entry open (limit order)
  Stop loss       : -2.5% below the entry open
  Time stop       : exit at the close of the 5th hourly bar (14:30) ->
                    the position never lives longer than 5 hours
  No overnight    : by construction

Intrabar fills are modeled pessimistically: if a bar touches both the stop
and the target, the stop is assumed to fill first.

NOTE the asymmetry: the 0.5% target vs 2.5% stop makes a high win rate
partly mechanical (many small wins, few larger losses). The profit factor,
not the win rate, is the evidence of edge - read them together.
"""

from dataclasses import dataclass

import pandas as pd

from backtest import BacktestResult, Trade
from strategy import rsi, sma

TRADING_DAYS = 252


@dataclass(frozen=True)
class SniperParams:
    trend_sma: int = 200      # daily SMA trend filter
    rsi_len: int = 2          # daily RSI length
    entry_rsi: float = 10.0   # setup: yesterday's daily RSI(2) below this
    target_pct: float = 0.5   # intraday profit target above the entry open
    stop_pct: float = 2.5     # intraday stop loss below the entry open
    max_hold_hours: int = 5   # hard cap; exit at that hourly bar's close

    def label(self) -> str:
        return (
            f"daily RSI{self.rsi_len}<{self.entry_rsi:g} above SMA{self.trend_sma} setup / "
            f"buy next open / +{self.target_pct:g}% target / -{self.stop_pct:g}% stop / "
            f"{self.max_hold_hours}h max hold, no overnight"
        )


def load_hourly(path) -> pd.DataFrame:
    """Load an hourly CSV; timestamps carry mixed DST offsets, so parse as UTC first."""
    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_datetime(df.index, utc=True).tz_convert("America/New_York")
    return df


def run_sniper_backtest(
    daily: pd.DataFrame,
    hourly: pd.DataFrame,
    params: SniperParams,
    name: str = "",
    cost_bps: float = 2.0,
) -> BacktestResult:
    cost = cost_bps / 10_000.0

    sig = daily.copy()
    sig["rsi"] = rsi(sig["close"], params.rsi_len)
    sig["sma"] = sma(sig["close"], params.trend_sma)
    signal_dates = {
        ts.date()
        for ts in sig.index[(sig["rsi"] < params.entry_rsi) & (sig["close"] > sig["sma"])]
    }
    daily_dates = sig.index.map(lambda ts: ts.date())

    result = BacktestResult(name=name, params=params, periods_per_year=TRADING_DAYS)
    session_dates: list = []
    session_equity: list[float] = []
    equity = 1.0

    day = pd.Series(hourly.index.date, index=hourly.index)
    for d, bars in hourly.groupby(day, sort=True):
        prior = daily_dates[daily_dates < d]
        traded_ret = 0.0
        if len(prior) and prior[-1] in signal_dates:
            open_px = float(bars["open"].iloc[0])
            entry = open_px * (1.0 + cost)
            target = open_px * (1.0 + params.target_pct / 100.0)
            stop = open_px * (1.0 - params.stop_pct / 100.0)
            n_bars = min(params.max_hold_hours, len(bars))
            exit_px, bars_held = None, n_bars
            for j in range(n_bars):
                bar = bars.iloc[j]
                if bar["low"] <= stop:       # pessimistic: stop checked first
                    exit_px, bars_held = stop, j + 1
                elif bar["high"] >= target:
                    exit_px, bars_held = target, j + 1
                if exit_px is not None:
                    break
            if exit_px is None:
                exit_px = float(bars["close"].iloc[n_bars - 1])
            traded_ret = exit_px * (1.0 - cost) / entry - 1.0
            result.trades.append(
                Trade(
                    entry_date=bars.index[0],
                    exit_date=bars.index[bars_held - 1],
                    entry_price=open_px,
                    exit_price=float(exit_px),
                    bars_held=bars_held,
                    ret=float(traded_ret),
                )
            )
            equity *= 1.0 + traded_ret
        session_dates.append(pd.Timestamp(d))
        session_equity.append(equity)

    result.equity = pd.Series(session_equity, index=pd.DatetimeIndex(session_dates))
    session_close = hourly.groupby(day, sort=True)["close"].last()
    result.buyhold = pd.Series(
        (session_close / session_close.iloc[0]).to_numpy(),
        index=pd.DatetimeIndex(session_dates),
    )
    return result
