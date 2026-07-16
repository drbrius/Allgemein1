"""Backtest engine and performance metrics for the mean-reversion strategy.

Execution model:
  - Signals are evaluated on the daily close; fills happen at that same close
    (standard convention for close-based mean-reversion systems).
  - `cost_bps` is charged per side (slippage + commission), so a round trip
    costs 2 * cost_bps.
  - Position sizing: 100% of current equity per trade, long only, no leverage.
"""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from strategy import StrategyParams, build_signals

TRADING_DAYS = 252


@dataclass
class Trade:
    entry_date: pd.Timestamp
    exit_date: pd.Timestamp
    entry_price: float
    exit_price: float
    bars_held: int
    ret: float  # net fractional return of the trade


@dataclass
class BacktestResult:
    name: str
    params: object
    trades: list[Trade] = field(default_factory=list)
    equity: pd.Series | None = None  # strategy equity curve (start = 1.0)
    buyhold: pd.Series | None = None
    periods_per_year: float = TRADING_DAYS  # bars per year, for annualizing Sharpe

    # ---- trade statistics -------------------------------------------------
    @property
    def n_trades(self) -> int:
        return len(self.trades)

    @property
    def wins(self) -> list[Trade]:
        return [t for t in self.trades if t.ret > 0]

    @property
    def losses(self) -> list[Trade]:
        return [t for t in self.trades if t.ret <= 0]

    @property
    def win_rate(self) -> float:
        return len(self.wins) / self.n_trades if self.n_trades else float("nan")

    @property
    def avg_win(self) -> float:
        return float(np.mean([t.ret for t in self.wins])) if self.wins else float("nan")

    @property
    def avg_loss(self) -> float:
        return float(np.mean([t.ret for t in self.losses])) if self.losses else float("nan")

    @property
    def profit_factor(self) -> float:
        gross_win = sum(t.ret for t in self.wins)
        gross_loss = -sum(t.ret for t in self.losses)
        return gross_win / gross_loss if gross_loss > 0 else float("inf")

    @property
    def expectancy(self) -> float:
        return float(np.mean([t.ret for t in self.trades])) if self.trades else float("nan")

    @property
    def avg_bars_held(self) -> float:
        return float(np.mean([t.bars_held for t in self.trades])) if self.trades else float("nan")

    # ---- equity-curve statistics ------------------------------------------
    @property
    def total_return(self) -> float:
        return float(self.equity.iloc[-1] / self.equity.iloc[0] - 1.0)

    @property
    def cagr(self) -> float:
        years = (self.equity.index[-1] - self.equity.index[0]).days / 365.25
        return float((self.equity.iloc[-1] / self.equity.iloc[0]) ** (1.0 / years) - 1.0)

    @property
    def buyhold_cagr(self) -> float:
        years = (self.buyhold.index[-1] - self.buyhold.index[0]).days / 365.25
        return float((self.buyhold.iloc[-1] / self.buyhold.iloc[0]) ** (1.0 / years) - 1.0)

    @property
    def max_drawdown(self) -> float:
        dd = self.equity / self.equity.cummax() - 1.0
        return float(dd.min())

    @property
    def buyhold_max_drawdown(self) -> float:
        dd = self.buyhold / self.buyhold.cummax() - 1.0
        return float(dd.min())

    @property
    def exposure(self) -> float:
        """Fraction of days with capital in the market."""
        daily = self.equity.pct_change().fillna(0.0)
        return float((daily != 0).mean())

    @property
    def sharpe(self) -> float:
        """Annualized Sharpe of daily strategy returns (rf = 0)."""
        daily = self.equity.pct_change().dropna()
        if daily.std() == 0:
            return float("nan")
        return float(daily.mean() / daily.std() * np.sqrt(self.periods_per_year))


def run_backtest(
    df: pd.DataFrame,
    params,
    name: str = "",
    cost_bps: float = 2.0,
    signal_builder=build_signals,
    periods_per_year: float = TRADING_DAYS,
) -> BacktestResult:
    """Run the engine over any bar size.

    `params` must provide max_hold_bars and stop_loss_pct; `signal_builder`
    must return df plus boolean entry_signal / exit_signal columns evaluated
    on each bar's close.
    """
    data = signal_builder(df, params)
    cost = cost_bps / 10_000.0

    closes = data["close"].to_numpy()
    entries = data["entry_signal"].to_numpy()
    exits = data["exit_signal"].to_numpy()
    dates = data.index

    result = BacktestResult(name=name, params=params, periods_per_year=periods_per_year)
    equity = np.ones(len(data))
    cash = 1.0
    units = 0.0  # index units held
    entry_i = -1

    for i in range(len(data)):
        px = closes[i]
        if units > 0.0:
            bars_held = i - entry_i
            stopped = px <= closes[entry_i] * (1.0 - params.stop_loss_pct / 100.0)
            if exits[i] or stopped or bars_held >= params.max_hold_bars:
                cash = units * px * (1.0 - cost)
                result.trades.append(
                    Trade(
                        entry_date=dates[entry_i],
                        exit_date=dates[i],
                        entry_price=float(closes[entry_i]),
                        exit_price=float(px),
                        bars_held=bars_held,
                        ret=float(cash / entry_cash - 1.0),
                    )
                )
                units = 0.0
        elif entries[i]:
            entry_cash = cash
            units = cash / (px * (1.0 + cost))
            cash = 0.0
            entry_i = i

        equity[i] = cash if units == 0.0 else units * px

    # Liquidate any open position at the last close so stats include it.
    if units > 0.0:
        cash = units * closes[-1] * (1.0 - cost)
        result.trades.append(
            Trade(
                entry_date=dates[entry_i],
                exit_date=dates[-1],
                entry_price=float(closes[entry_i]),
                exit_price=float(closes[-1]),
                bars_held=len(data) - 1 - entry_i,
                ret=float(cash / entry_cash - 1.0),
            )
        )
        equity[-1] = cash

    result.equity = pd.Series(equity, index=dates)
    result.buyhold = data["close"] / data["close"].iloc[0]
    return result


def trades_to_frame(result: BacktestResult) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "entry_date": [t.entry_date.date() for t in result.trades],
            "exit_date": [t.exit_date.date() for t in result.trades],
            "entry_price": [round(t.entry_price, 2) for t in result.trades],
            "exit_price": [round(t.exit_price, 2) for t in result.trades],
            "bars_held": [t.bars_held for t in result.trades],
            "return_pct": [round(100 * t.ret, 3) for t in result.trades],
        }
    )


def summarize(result: BacktestResult) -> dict:
    return {
        "trades": result.n_trades,
        "win_rate_pct": round(100 * result.win_rate, 1),
        "avg_win_pct": round(100 * result.avg_win, 2),
        "avg_loss_pct": round(100 * result.avg_loss, 2),
        "profit_factor": round(result.profit_factor, 2),
        "expectancy_pct": round(100 * result.expectancy, 2),
        "avg_bars_held": round(result.avg_bars_held, 1),
        "strategy_cagr_pct": round(100 * result.cagr, 2),
        "buyhold_cagr_pct": round(100 * result.buyhold_cagr, 2),
        "max_drawdown_pct": round(100 * result.max_drawdown, 1),
        "buyhold_max_dd_pct": round(100 * result.buyhold_max_drawdown, 1),
        "exposure_pct": round(100 * result.exposure, 1),
        "sharpe": round(result.sharpe, 2),
    }
