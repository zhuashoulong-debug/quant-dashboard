from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from formula_lab.market_cache import build_daily_cache_metadata, write_cache_metadata
from formula_lab.stock_pool import StockItem, to_akshare_symbol, to_prefixed_market_symbol


CANONICAL_COLUMNS = {
    "日期": "date",
    "date": "date",
    "股票代码": "code",
    "code": "code",
    "开盘": "open",
    "open": "open",
    "收盘": "close",
    "close": "close",
    "最高": "high",
    "high": "high",
    "最低": "low",
    "low": "low",
    "成交量": "volume",
    "volume": "volume",
    "vol": "volume",
    "成交额": "amount",
    "amount": "amount",
    "振幅": "amplitude",
    "amplitude": "amplitude",
    "涨跌幅": "pct_chg",
    "pct_chg": "pct_chg",
    "涨跌额": "change",
    "change": "change",
    "换手率": "turnover",
    "turnover": "turnover",
}

REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount"]
OUTPUT_COLUMNS = [
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


def fetch_qfq_daily(
    stock: StockItem,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    errors: list[str] = []
    for provider, fetcher in (
        ("eastmoney", _fetch_qfq_daily_eastmoney),
        ("tencent", _fetch_qfq_daily_tencent),
        ("sina", _fetch_qfq_daily_sina),
    ):
        try:
            data = fetcher(stock, start_date, end_date)
            data.attrs["provider"] = provider
            return data
        except Exception as exc:  # noqa: BLE001 - caller should see every provider failure.
            errors.append(f"{provider}: {exc}")
    raise RuntimeError("all AKShare daily providers failed; " + " | ".join(errors))


def _fetch_qfq_daily_eastmoney(
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


def _fetch_qfq_daily_tencent(
    stock: StockItem,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    import akshare as ak

    raw = ak.stock_zh_a_hist_tx(
        symbol=to_prefixed_market_symbol(stock.code),
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    return normalize_akshare_daily(raw, stock)


def _fetch_qfq_daily_sina(
    stock: StockItem,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    import akshare as ak

    raw = ak.stock_zh_a_daily(
        symbol=to_prefixed_market_symbol(stock.code),
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    return normalize_akshare_daily(raw, stock)


def normalize_akshare_daily(raw: pd.DataFrame, stock: StockItem) -> pd.DataFrame:
    data = raw.rename(columns=CANONICAL_COLUMNS).copy()
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"AKShare daily data missing columns: {', '.join(missing)}")

    data["date"] = pd.to_datetime(data["date"])
    data["code"] = stock.code
    data["name"] = stock.name

    for column in OUTPUT_COLUMNS:
        if column not in data.columns:
            data[column] = pd.NA

    data = data[OUTPUT_COLUMNS].sort_values("date").reset_index(drop=True)
    return data


def cache_path(
    cache_root: str | Path,
    stock: StockItem,
    start_date: str,
    end_date: str,
) -> Path:
    root = Path(cache_root)
    return root / "akshare" / "qfq" / "daily" / f"{stock.code}_{start_date}_{end_date}.csv"


def write_daily_cache(
    data: pd.DataFrame,
    path: str | Path,
    *,
    stock: StockItem | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    if stock is not None and start_date is not None and end_date is not None:
        metadata = build_daily_cache_metadata(
            data,
            stock,
            start_date=start_date,
            end_date=end_date,
        )
        write_cache_metadata(metadata, output_path)
    return output_path


def today_yyyymmdd() -> str:
    return date.today().strftime("%Y%m%d")
