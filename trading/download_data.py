"""Download free daily OHLC history for Nasdaq 100 and Dow Jones (US30).

Data source: Yahoo Finance public chart API (no API key required).
Saves one CSV per index into trading/data/.
"""

import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

SYMBOLS = {
    "nasdaq100": "^NDX",  # Nasdaq 100 index (basis of NAS100 / NQ futures)
    "us30": "^DJI",       # Dow Jones Industrial Average (basis of US30 / YM futures)
}

# range=max silently downgrades granularity; explicit period1/period2 keeps 1d bars.
CHART_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    "?period1=0&period2={now}&interval=1d&events=history"
)


def fetch_daily_history(symbol: str) -> pd.DataFrame:
    url = CHART_URL.format(symbol=symbol.replace("^", "%5E"), now=int(time.time()))
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(4):
        try:
            with urlopen(req, timeout=60) as resp:
                payload = json.load(resp)
            break
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))

    result = payload["chart"]["result"][0]
    quote = result["indicators"]["quote"][0]
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(result["timestamp"], unit="s", utc=True).date,
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"],
            "volume": quote["volume"],
        }
    )
    df = df.dropna(subset=["open", "high", "low", "close"])
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date").sort_index()


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for name, symbol in SYMBOLS.items():
        df = fetch_daily_history(symbol)
        out = DATA_DIR / f"{name}.csv"
        df.to_csv(out)
        print(f"{name} ({symbol}): {len(df)} bars, {df.index[0].date()} -> {df.index[-1].date()} -> {out}")


if __name__ == "__main__":
    sys.exit(main())
