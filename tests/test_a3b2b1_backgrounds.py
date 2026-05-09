from __future__ import annotations

import unittest

import pandas as pd

from formula_lab.a3b2b1 import add_a3b2b1_backgrounds


def make_cross_sample() -> pd.DataFrame:
    closes = [10.0] * 179 + [15.0]
    rows = []
    for index, close in enumerate(closes):
        rows.append(
            {
                "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=index),
                "code": "000001",
                "name": "sample",
                "open": close,
                "high": close,
                "low": close,
                "close": close,
                "volume": 100000,
                "amount": close * 100000,
            }
        )
    return pd.DataFrame(rows)


class A3b2b1BackgroundTests(unittest.TestCase):
    def test_add_a3b2b1_backgrounds_adds_diagnostic_columns(self) -> None:
        result = add_a3b2b1_backgrounds(make_cross_sample())

        expected_columns = {
            "body_ratio",
            "upper_shadow_ratio",
            "amount_ratio",
            "bullish_strong",
            "long_upper_shadow",
            "large_amount",
            "structure_break_up",
            "effective_cross_1",
            "warm_up_base",
            "warm_up",
            "violent_up",
            "violent_up_risk",
            "blue_compression_quality",
            "blue_quality_background",
            "blue_warm_source",
            "blue_violent_source",
            "yellow_warm_source",
            "yellow_violent_source",
            "diagnostic_k",
            "old_near_squeeze",
            "old_breakthrough_background",
            "new_late_squeeze",
            "new_breakthrough_background",
            "old_blue_squeeze_background",
        }

        self.assertTrue(expected_columns.issubset(result.columns))
        self.assertTrue(result.iloc[-1]["effective_cross_1"])
        self.assertTrue(result.iloc[-1]["diagnostic_k"])


if __name__ == "__main__":
    unittest.main()
