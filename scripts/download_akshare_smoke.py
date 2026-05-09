from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from formula_lab.akshare_daily import (
    cache_path,
    fetch_qfq_daily,
    today_yyyymmdd,
    write_daily_cache,
)
from formula_lab.stock_pool import read_stock_pool, select_stock


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download one AKShare qfq daily smoke sample.")
    parser.add_argument("--pool", default=r"D:\数据包.xlsx", help="Excel stock pool path.")
    parser.add_argument("--code", default="002222", help="Six digit stock code.")
    parser.add_argument("--start", default="20240101", help="Start date, YYYYMMDD.")
    parser.add_argument("--end", default=today_yyyymmdd(), help="End date, YYYYMMDD.")
    parser.add_argument("--cache-root", default="data/raw", help="Local cache root.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pool = read_stock_pool(args.pool)
    stock = select_stock(pool, args.code)
    data = fetch_qfq_daily(stock, start_date=args.start, end_date=args.end)
    output = write_daily_cache(data, cache_path(args.cache_root, stock, args.start, args.end))

    print(f"stock={stock.code} {stock.name}")
    print(f"rows={len(data)}")
    if not data.empty:
        print(f"date_range={data['date'].min().date()} -> {data['date'].max().date()}")
        print("columns=" + ",".join(data.columns))
        print(data.tail(3).to_string(index=False))
    print(f"cache={Path(output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
