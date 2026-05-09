from __future__ import annotations

import unittest

from formula_lab.validation_views import VALIDATION_VIEWS, validation_view_ids


class ValidationViewTests(unittest.TestCase):
    def test_views_keep_old_subplots_consolidated(self) -> None:
        self.assertEqual(validation_view_ids(), ["overview", "base", "background", "source"])
        self.assertLessEqual(len(VALIDATION_VIEWS), 4)

    def test_every_view_has_small_named_field_list(self) -> None:
        for view in VALIDATION_VIEWS:
            self.assertIn("label", view)
            self.assertIn("fields", view)
            self.assertGreater(len(view["fields"]), 0)
            self.assertLessEqual(len(view["fields"]), 10)
            for field in view["fields"]:
                self.assertIn("key", field)
                self.assertIn("label", field)
                self.assertIn(field["kind"], {"bool", "number"})


if __name__ == "__main__":
    unittest.main()
