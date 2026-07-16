"""Run the mean-reversion backtest on Nasdaq 100 and US30 and write a report.

Usage:
    python3 download_data.py   # refresh data first (optional, CSVs are committed)
    python3 run_backtest.py

Outputs:
    results/report.md            summary tables (full sample + in/out-of-sample)
    results/<index>_trades.csv   every trade with dates, prices and returns
"""

from pathlib import Path

import pandas as pd

from backtest import run_backtest, summarize, trades_to_frame
from strategy import StrategyParams

DATA_DIR = Path(__file__).parent / "data"
RESULTS_DIR = Path(__file__).parent / "results"

INDICES = {"nasdaq100": "Nasdaq 100 (^NDX)", "us30": "US30 / Dow Jones (^DJI)"}
OOS_SPLIT = "2016-01-01"  # everything from here on is out-of-sample
COST_BPS = 2.0            # per side (slippage + commission)


def metrics_table(rows: dict[str, dict]) -> str:
    keys = list(next(iter(rows.values())).keys())
    header = "| metric | " + " | ".join(rows) + " |"
    sep = "|---" * (len(rows) + 1) + "|"
    lines = [header, sep]
    for k in keys:
        lines.append("| " + k + " | " + " | ".join(str(r[k]) for r in rows.values()) + " |")
    return "\n".join(lines)


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    params = StrategyParams()
    report = [
        "# Mean-Reversion Backtest Report",
        "",
        f"**Strategy:** {params.label()}",
        f"**Execution:** fills at the signal bar's close, {COST_BPS:g} bps cost per side, "
        "100% of equity per trade, long only, no leverage.",
        f"**Sample split:** the {OOS_SPLIT}+ segment is shown separately as a robustness check "
        "(parameters follow the published Connors RSI-2 family rather than a fit to this data).",
        "",
    ]

    for name, title in INDICES.items():
        df = pd.read_csv(DATA_DIR / f"{name}.csv", index_col=0, parse_dates=True)
        segments = {
            "full sample": df,
            f"in-sample (< {OOS_SPLIT[:4]})": df[df.index < OOS_SPLIT],
            f"out-of-sample (>= {OOS_SPLIT[:4]})": df[df.index >= OOS_SPLIT],
        }
        rows = {}
        for seg_name, seg_df in segments.items():
            result = run_backtest(seg_df, params, name=f"{name} {seg_name}", cost_bps=COST_BPS)
            rows[seg_name] = summarize(result)
            if seg_name == "full sample":
                trades_to_frame(result).to_csv(RESULTS_DIR / f"{name}_trades.csv", index=False)

        span = f"{df.index[0].date()} to {df.index[-1].date()}"
        report += [f"## {title}", "", f"Data: {span}, {len(df)} daily bars (Yahoo Finance).", "",
                   metrics_table(rows), ""]
        print(f"\n=== {title} ({span}) ===")
        print(pd.DataFrame(rows).to_string())

    report += [
        "## How to read these numbers",
        "",
        "- **Win rate** counts profitable trades. Mean reversion wins often but its "
        "average loss is larger than its average win - profit factor > 1 is what makes it net profitable.",
        "- **Exposure** is low (capital is in the market only a small fraction of days); "
        "CAGR on total equity is therefore modest even when per-trade edge is strong. "
        "Practitioners run this as an overlay on cash or scale it with futures.",
        "- Past performance does not guarantee future results. This is research code, "
        "not investment advice.",
        "",
    ]
    (RESULTS_DIR / "report.md").write_text("\n".join(report))
    print(f"\nReport written to {RESULTS_DIR / 'report.md'}")


if __name__ == "__main__":
    main()
