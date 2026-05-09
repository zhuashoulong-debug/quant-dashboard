from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

from formula_lab.akshare_daily import cache_path, today_yyyymmdd
from formula_lab.akshare_universe import fetch_a_share_universe
from formula_lab.data_service import load_or_fetch_daily
from formula_lab.market_cache import append_manifest_event, metadata_path_for
from formula_lab.stock_pool import StockItem, normalize_stock_code, read_stock_pool


DEFAULT_START_DATE = "20100101"


def _parse_codes(codes: str) -> list[StockItem]:
    items: list[StockItem] = []
    for raw_code in codes.split(","):
        raw_code = raw_code.strip()
        if raw_code:
            items.append(StockItem(code=normalize_stock_code(raw_code), name=""))
    return items


def _load_targets(args: argparse.Namespace) -> list[StockItem]:
    if args.codes:
        targets = _parse_codes(args.codes)
    elif args.pool:
        targets = read_stock_pool(args.pool)
    else:
        if args.market != "a-share":
            raise ValueError("only a-share universe fetching is implemented")
        targets = fetch_a_share_universe()

    if args.limit is not None:
        targets = targets[: args.limit]
    return targets


def _manifest_path(cache_root: str | Path) -> Path:
    return Path(cache_root) / "akshare" / "qfq" / "daily" / "download_manifest.jsonl"


def download_targets(args: argparse.Namespace) -> int:
    targets = _load_targets(args)
    manifest_path = _manifest_path(args.cache_root)
    failures = 0

    for index, stock in enumerate(targets, start=1):
        data_path = cache_path(args.cache_root, stock, args.start, args.end)
        if data_path.exists() and metadata_path_for(data_path).exists() and not args.refresh:
            status = "skipped"
            rows = None
            error = None
        else:
            try:
                data = load_or_fetch_daily(
                    stock,
                    start_date=args.start,
                    end_date=args.end,
                    cache_root=args.cache_root,
                    refresh=args.refresh,
                )
                status = "downloaded"
                rows = len(data)
                error = None
            except Exception as exc:  # noqa: BLE001 - manifest should capture every failed code.
                status = "failed"
                rows = None
                error = str(exc)
                failures += 1

        append_manifest_event(
            manifest_path,
            {
                "time": datetime.now(timezone.utc).isoformat(),
                "market": args.market,
                "source": "akshare",
                "adjust": "qfq",
                "period": "daily",
                "start_date": args.start,
                "end_date": args.end,
                "index": index,
                "total": len(targets),
                "code": stock.code,
                "name": stock.name,
                "status": status,
                "rows": rows,
                "error": error,
                "path": str(data_path),
            },
        )
        print(f"[{index}/{len(targets)}] {stock.code} {status}")

        if args.sleep > 0 and index < len(targets):
            time.sleep(args.sleep)

    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cache market daily data locally.")
    parser.add_argument("--market", default="a-share", choices=["a-share"])
    parser.add_argument("--start", default=DEFAULT_START_DATE)
    parser.add_argument("--end", default=today_yyyymmdd())
    parser.add_argument("--cache-root", default="data/raw")
    parser.add_argument("--codes", help="Comma-separated stock codes, e.g. 002222,301269")
    parser.add_argument("--pool", help="Excel stock pool path with columns: 代码, 名称")
    parser.add_argument("--limit", type=int, help="Limit target count for smoke runs")
    parser.add_argument("--sleep", type=float, default=0.25)
    parser.add_argument("--refresh", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return download_targets(args)


if __name__ == "__main__":
    raise SystemExit(main())
