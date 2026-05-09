from __future__ import annotations

import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd

from formula_lab.akshare_daily import cache_path
from formula_lab.market_cache import metadata_path_for
from formula_lab.stock_pool import StockItem
from scripts import download_market_data


def make_args(cache_root: Path) -> argparse.Namespace:
    return argparse.Namespace(
        cache_root=str(cache_root),
        codes=None,
        end="20260131",
        limit=None,
        market="a-share",
        pool=None,
        refresh=False,
        retries=1,
        retry_sleep=0,
        sleep=0,
        start="20260101",
        workers=2,
    )


class DownloadMarketDataTests(unittest.TestCase):
    def test_download_targets_retries_and_records_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            stocks = [
                StockItem(code="000001", name="one"),
                StockItem(code="000002", name="two"),
            ]
            attempts: dict[str, int] = {}

            def fake_load(stock: StockItem, **_: object) -> pd.DataFrame:
                attempts[stock.code] = attempts.get(stock.code, 0) + 1
                if stock.code == "000002" and attempts[stock.code] == 1:
                    raise RuntimeError("temporary")
                return pd.DataFrame({"date": ["2026-01-01"], "close": [1.0]})

            args = make_args(cache_root)
            with (
                mock.patch.object(download_market_data, "_load_targets", return_value=stocks),
                mock.patch.object(download_market_data, "load_or_fetch_daily", side_effect=fake_load),
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(download_market_data.download_targets(args), 0)

            manifest = cache_root / "akshare" / "qfq" / "daily" / "download_manifest.jsonl"
            events = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(events), 2)
            by_code = {event["code"]: event for event in events}
            self.assertEqual(by_code["000001"]["status"], "downloaded")
            self.assertEqual(by_code["000002"]["status"], "downloaded")
            self.assertEqual(by_code["000002"]["attempts"], 2)

    def test_download_targets_skips_cached_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = Path(tmp)
            stock = StockItem(code="000001", name="one")
            data_path = cache_path(cache_root, stock, "20260101", "20260131")
            data_path.parent.mkdir(parents=True)
            data_path.write_text("date,close\n2026-01-01,1\n", encoding="utf-8")
            metadata_path_for(data_path).write_text("{}", encoding="utf-8")

            args = make_args(cache_root)
            with (
                mock.patch.object(download_market_data, "_load_targets", return_value=[stock]),
                mock.patch.object(download_market_data, "load_or_fetch_daily") as load_mock,
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(download_market_data.download_targets(args), 0)

            load_mock.assert_not_called()
            manifest = cache_root / "akshare" / "qfq" / "daily" / "download_manifest.jsonl"
            event = json.loads(manifest.read_text(encoding="utf-8").strip())
            self.assertEqual(event["status"], "skipped")
            self.assertEqual(event["attempts"], 0)


if __name__ == "__main__":
    unittest.main()
