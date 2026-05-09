from __future__ import annotations

import unittest

import pandas as pd

from formula_lab.akshare_universe import normalize_a_share_universe


class AkshareUniverseTests(unittest.TestCase):
    def test_normalizes_chinese_columns(self) -> None:
        raw = pd.DataFrame(
            {
                "代码": ["2", "002222", "688300"],
                "名称": ["万科A", "福晶科技重复", "联瑞新材"],
            }
        )

        items = normalize_a_share_universe(raw)

        self.assertEqual([item.code for item in items], ["000002", "002222", "688300"])
        self.assertEqual(items[0].name, "万科A")

    def test_normalizes_english_columns(self) -> None:
        raw = pd.DataFrame({"symbol": ["sz301269"], "name": ["华大九天"]})

        items = normalize_a_share_universe(raw)

        self.assertEqual(items[0].code, "301269")
        self.assertEqual(items[0].name, "华大九天")


if __name__ == "__main__":
    unittest.main()
