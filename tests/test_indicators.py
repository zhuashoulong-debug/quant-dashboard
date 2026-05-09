from __future__ import annotations

import math
import unittest

import pandas as pd

from formula_lab.indicators import add_boll_pctb


class IndicatorTests(unittest.TestCase):
    def test_add_boll_pctb_uses_sample_std(self) -> None:
        data = pd.DataFrame({"close": list(range(1, 21))})

        result = add_boll_pctb(data)
        last = result.iloc[-1]

        self.assertEqual(last["boll_mid"], 10.5)
        self.assertTrue(math.isclose(last["boll_upper"], 22.3321595662, rel_tol=1e-10))
        self.assertTrue(math.isclose(last["boll_lower"], -1.3321595662, rel_tol=1e-10))
        self.assertTrue(math.isclose(last["pctb"], 0.9014482710, rel_tol=1e-10))

    def test_add_boll_pctb_requires_close(self) -> None:
        with self.assertRaisesRegex(ValueError, "close"):
            add_boll_pctb(pd.DataFrame({"open": [1, 2, 3]}))


if __name__ == "__main__":
    unittest.main()
