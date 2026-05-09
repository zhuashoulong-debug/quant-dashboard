from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def _download_one(args: argparse.Namespace, stock: StockItem, index: int, total: int) -> dict[str, object]:
    data_path = cache_path(args.cache_root, stock, args.start, args.end)
    attempts = 0
    if data_path.exists() and metadata_path_for(data_path).exists() and not args.refresh:
        status = "skipped"
        rows = None
        error = None
    else:
        max_attempts = max(1, args.retries + 1)
        status = "failed"
        rows = None
        error = None
        for attempt in range(1, max_attempts + 1):
            attempts = attempt
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
                break
            except Exception as exc:  # noqa: BLE001 - manifest should capture every failed code.
                error = str(exc)
                if attempt < max_attempts and args.retry_sleep > 0:
                    time.sleep(args.retry_sleep)

        if attempts > 0 and args.sleep > 0:
            time.sleep(args.sleep)

    return {
        "time": datetime.now(timezone.utc).isoformat(),
        "market": args.market,
        "source": "akshare",
        "adjust": "qfq",
        "period": "daily",
        "start_date": args.start,
        "end_date": args.end,
        "index": index,
        "total": total,
        "code": stock.code,
        "name": stock.name,
        "status": status,
        "rows": rows,
        "attempts": attempts,
        "error": error,
        "path": str(data_path),
    }


def download_targets(args: argparse.Namespace) -> int:
    targets = _load_targets(args)
    manifest_path = _manifest_path(args.cache_root)
    failures = 0
    workers = max(1, args.workers)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_download_one, args, stock, index, len(targets)): stock
            for index, stock in enumerate(targets, start=1)
        }
        for future in as_completed(futures):
            event = future.result()
            if event["status"] == "failed":
                failures += 1
            append_manifest_event(manifest_path, event)
            print(
                f"[{event['index']}/{event['total']}] "
                f"{event['code']} {event['status']} attempts={event['attempts']}",
                flush=True,
            )

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
    parser.add_argument("--workers", type=int, default=1, help="Concurrent downloads; use 3-5 for gentle full-market runs")
    parser.add_argument("--retries", type=int, default=2, help="Retries per stock after the first failed attempt")
    parser.add_argument("--retry-sleep", type=float, default=2.0, help="Seconds to wait between retry attempts")
    parser.add_argument("--refresh", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return download_targets(args)


if __name__ == "__main__":
    raise SystemExit(main())
