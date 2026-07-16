"""Mean-reversion pullback strategy for equity indices (Nasdaq 100, US30).

Logic (long-only, daily bars):
  Trend filter : close above the 200-day SMA (only trade with the long-term trend)
  Entry        : RSI(2) drops below an oversold threshold (short, sharp pullback)
  Exit         : RSI(2) recovers above an overbought threshold,
                 or close crosses back above the 5-day SMA,
                 or a time stop after `max_hold_days` trading days

This is the classic short-term mean-reversion structure (Connors-style RSI-2):
it wins often because indices in uptrends tend to snap back after 2-3 down
days, but individual losses can be larger than individual wins. Win rate
alone is NOT a measure of profitability - always read it together with
profit factor and max drawdown.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length).mean()


def rsi(series: pd.Series, length: int) -> pd.Series:
    """Wilder's RSI."""
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / length, min_periods=length, adjust=False).mean()
    rs = avg_gain / avg_loss
    out = 100.0 - 100.0 / (1.0 + rs)
    return out.where(avg_loss != 0, 100.0)


@dataclass(frozen=True)
class StrategyParams:
    trend_sma: int = 200      # long-term trend filter
    rsi_len: int = 2          # fast RSI length
    entry_rsi: float = 5.0    # enter when RSI(2) below this
    exit_rsi: float = 65.0    # exit when RSI(2) above this
    exit_sma: int = 5         # ... or close back above this SMA
    max_hold_days: int = 10   # time stop (catastrophe guard)
    stop_loss_pct: float = 8.0  # catastrophe stop: exit if close falls this % below entry

    def label(self) -> str:
        return (
            f"SMA{self.trend_sma} trend / RSI{self.rsi_len}<{self.entry_rsi:g} entry / "
            f"RSI>{self.exit_rsi:g} or close>SMA{self.exit_sma} exit / "
            f"{self.max_hold_days}d time stop / {self.stop_loss_pct:g}% stop loss"
        )


def build_signals(df: pd.DataFrame, p: StrategyParams) -> pd.DataFrame:
    """Return df with entry/exit signal columns evaluated on each bar's close."""
    out = df.copy()
    out["trend_sma"] = sma(out["close"], p.trend_sma)
    out["exit_sma"] = sma(out["close"], p.exit_sma)
    out["rsi"] = rsi(out["close"], p.rsi_len)

    out["entry_signal"] = (out["close"] > out["trend_sma"]) & (out["rsi"] < p.entry_rsi)
    out["exit_signal"] = (out["rsi"] > p.exit_rsi) | (out["close"] > out["exit_sma"])
    return out.dropna(subset=["trend_sma", "rsi"])
