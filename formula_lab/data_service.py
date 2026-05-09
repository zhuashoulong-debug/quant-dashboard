from __future__ import annotations

from pathlib import Path

import pandas as pd

from formula_lab.akshare_daily import cache_path, fetch_qfq_daily, write_daily_cache
from formula_lab.a3b2b1 import add_a3b2b1_backgrounds
from formula_lab.stock_pool import StockItem, read_stock_pool, select_stock


def stock_from_pool(pool_path: str | Path, code: str) -> StockItem:
    try:
        return select_stock(read_stock_pool(pool_path), code)
    except FileNotFoundError:
        return StockItem(code=code, name="")


def load_or_fetch_daily(
    stock: StockItem,
    start_date: str,
    end_date: str,
    cache_root: str | Path = "data/raw",
    refresh: bool = False,
) -> pd.DataFrame:
    path = cache_path(cache_root, stock, start_date, end_date)
    if path.exists() and not refresh:
        data = pd.read_csv(path, parse_dates=["date"])
    else:
        data = fetch_qfq_daily(stock, start_date=start_date, end_date=end_date)
        write_daily_cache(data, path)
    return data


def load_daily_with_indicators(
    stock: StockItem,
    start_date: str,
    end_date: str,
    cache_root: str | Path = "data/raw",
    refresh: bool = False,
) -> pd.DataFrame:
    data = load_or_fetch_daily(
        stock=stock,
        start_date=start_date,
        end_date=end_date,
        cache_root=cache_root,
        refresh=refresh,
    )
    return add_a3b2b1_backgrounds(data)
