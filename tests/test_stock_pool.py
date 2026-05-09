from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from formula_lab.stock_pool import (
    normalize_stock_code,
    read_stock_pool,
    select_stock,
    to_akshare_symbol,
    to_ts_code,
)


class StockPoolTests(unittest.TestCase):
    def test_normalize_stock_code_keeps_six_digits(self) -> None:
        self.assertEqual(normalize_stock_code("002222"), "002222")
        self.assertEqual(normalize_stock_code(2222), "002222")

    def test_code_conversions(self) -> None:
        self.assertEqual(to_akshare_symbol("002222"), "002222")
        self.assertEqual(to_ts_code("002222"), "002222.SZ")
        self.assertEqual(to_ts_code("688300"), "688300.SH")

    def test_read_stock_pool_from_excel(self) -> None:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["初始", "代码", "名称"])
        sheet.append([1, "002222", "福晶科技"])
        sheet.append([2, "002222", "福晶科技重复"])
        sheet.append([3, "688300", "联瑞新材"])

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pool.xlsx"
            workbook.save(path)
            workbook.close()
            items = read_stock_pool(path)

        self.assertEqual([item.code for item in items], ["002222", "688300"])
        self.assertEqual(select_stock(items, "2222").name, "福晶科技")


if __name__ == "__main__":
    unittest.main()
