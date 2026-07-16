"""Download free OHLC history for Nasdaq 100 and Dow Jones (US30).

Data source: Yahoo Finance public chart API (no API key required).
Saves per index into trading/data/:
  <name>.csv     daily bars, full history (for the daily mean-reversion strategy)
  <name>_1h.csv  hourly bars, ~ last 730 trading days (for the intraday sniper strategy;
                 Yahoo does not serve hourly data further back)
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
DAILY_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    "?period1=0&period2={now}&interval=1d&events=history"
)
# Hourly bars only accept range= (explicit periods beyond the limit return HTTP 422).
HOURLY_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=730d&interval=1h"
)


def _fetch_chart(url: str, tz: str | None = None) -> pd.DataFrame:
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
    stamps = pd.to_datetime(result["timestamp"], unit="s", utc=True)
    if tz:
        stamps = stamps.tz_convert(tz)
    else:
        stamps = pd.to_datetime(stamps.date)
    df = pd.DataFrame(
        {
            "date": stamps,
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"],
            "volume": quote["volume"],
        }
    )
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df.set_index("date").sort_index()


def fetch_daily_history(symbol: str) -> pd.DataFrame:
    return _fetch_chart(DAILY_URL.format(symbol=symbol.replace("^", "%5E"), now=int(time.time())))


def fetch_hourly_history(symbol: str) -> pd.DataFrame:
    """Hourly bars with timestamps in exchange time (America/New_York)."""
    return _fetch_chart(HOURLY_URL.format(symbol=symbol.replace("^", "%5E")), tz="America/New_York")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for name, symbol in SYMBOLS.items():
        for suffix, fetch in (("", fetch_daily_history), ("_1h", fetch_hourly_history)):
            df = fetch(symbol)
            out = DATA_DIR / f"{name}{suffix}.csv"
            df.to_csv(out)
            print(f"{name}{suffix} ({symbol}): {len(df)} bars, {df.index[0].date()} -> {df.index[-1].date()} -> {out}")


if __name__ == "__main__":
    sys.exit(main())
