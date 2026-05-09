from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from formula_lab.stock_pool import StockItem, to_akshare_symbol


CANONICAL_COLUMNS = {
    "日期": "date",
    "股票代码": "code",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "pct_chg",
    "涨跌额": "change",
    "换手率": "turnover",
}


def fetch_qfq_daily(
    stock: StockItem,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    import akshare as ak

    raw = ak.stock_zh_a_hist(
        symbol=to_akshare_symbol(stock.code),
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    return normalize_akshare_daily(raw, stock)


def normalize_akshare_daily(raw: pd.DataFrame, stock: StockItem) -> pd.DataFrame:
    missing = [column for column in CANONICAL_COLUMNS if column not in raw.columns]
    if missing:
        raise ValueError(f"AKShare daily data missing columns: {', '.join(missing)}")

    data = raw.rename(columns=CANONICAL_COLUMNS).copy()
    data["date"] = pd.to_datetime(data["date"])
    data["code"] = stock.code
    data["name"] = stock.name

    ordered = [
        "date",
        "code",
        "name",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "amplitude",
        "pct_chg",
        "change",
        "turnover",
    ]
    data = data[ordered].sort_values("date").reset_index(drop=True)
    return data


def cache_path(
    cache_root: str | Path,
    stock: StockItem,
    start_date: str,
    end_date: str,
) -> Path:
    root = Path(cache_root)
    return root / "akshare" / "qfq" / "daily" / f"{stock.code}_{start_date}_{end_date}.csv"


def write_daily_cache(data: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def today_yyyymmdd() -> str:
    return date.today().strftime("%Y%m%d")

