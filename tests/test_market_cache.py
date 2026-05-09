from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from formula_lab.market_cache import (
    build_daily_cache_metadata,
    metadata_path_for,
    write_cache_metadata,
)
from formula_lab.stock_pool import StockItem


class MarketCacheTests(unittest.TestCase):
    def test_builds_daily_cache_metadata(self) -> None:
        data = pd.DataFrame(
            {
                "date": pd.to_datetime(["2026-05-07", "2026-05-08"]),
                "open": [1.0, 2.0],
                "close": [1.5, 2.5],
            }
        )

        metadata = build_daily_cache_metadata(
            data,
            StockItem(code="002222", name="福晶科技"),
            start_date="20100101",
            end_date="20260509",
        )

        self.assertEqual(metadata.source, "akshare")
        self.assertEqual(metadata.provider, "")
        self.assertEqual(metadata.market, "a_share")
        self.assertEqual(metadata.adjust, "qfq")
        self.assertEqual(metadata.rows, 2)
        self.assertEqual(metadata.first_date, "2026-05-07")
        self.assertEqual(metadata.last_date, "2026-05-08")

    def test_writes_metadata_next_to_cache_file(self) -> None:
        metadata = build_daily_cache_metadata(
            pd.DataFrame({"date": pd.to_datetime(["2026-05-08"])}),
            StockItem(code="002222", name="福晶科技"),
            start_date="20100101",
            end_date="20260509",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "002222_20100101_20260509.csv"
            output_path = write_cache_metadata(metadata, data_path)

            self.assertEqual(output_path, metadata_path_for(data_path))
            written = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(written["code"], "002222")
        self.assertEqual(written["adjust"], "qfq")


if __name__ == "__main__":
    unittest.main()
