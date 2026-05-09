from __future__ import annotations

import unittest

import pandas as pd

from formula_lab.a3b2b1 import add_a3b2b1_backgrounds, yellow_permission_layer


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
            "first_expand_start",
            "speed_valid",
            "speed_after_running",
            "rush_valid",
            "strong_track_occupancy",
            "yellow_candidate_valid",
            "old_yellow_display_occupancy",
            "old_candidate_cooling",
            "yellow_reset_pullback",
            "yellow_recontraction_reset",
            "strong_trend_running",
            "near_strong_track_signal",
            "yellow_reset_after_signal",
            "yellow_time_reset",
            "yellow_after_reset",
            "strong_reset_after_signal",
            "strong_time_reset",
            "strong_after_reset",
            "yellow_hard_cooling",
            "yellow_after_same_trend",
            "yellow_self_permission",
            "yellow_strong_permission",
            "yellow_display_permission",
            "yellow_fresh_permission",
            "experimental_yellow_valid",
            "blue_warm_valid",
            "blue_violent_valid",
            "blue_valid",
            "yellow_warm_valid",
            "yellow_violent_valid",
            "yellow_valid",
            "effective_start_signal_pre",
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

    def test_yellow_permission_layer_blocks_same_segment_repeats(self) -> None:
        yellow_candidate = pd.Series([False, True, True, False, True, False, True])
        strong_track_occupancy = pd.Series([False] * len(yellow_candidate))
        reset_event = pd.Series([False] * len(yellow_candidate))
        strong_trend_running = pd.Series([True] * len(yellow_candidate))

        result = yellow_permission_layer(
            yellow_candidate=yellow_candidate,
            strong_track_occupancy=strong_track_occupancy,
            yellow_reset_event=reset_event,
            strong_reset_event=reset_event,
            strong_trend_running=strong_trend_running,
            hard_window=2,
            segment_window=4,
            strong_window=2,
        )

        self.assertTrue(result.iloc[1]["experimental_yellow_valid"])
        self.assertTrue(result.iloc[2]["yellow_hard_cooling"])
        self.assertFalse(result.iloc[2]["experimental_yellow_valid"])
        self.assertTrue(result.iloc[4]["yellow_after_same_trend"])
        self.assertFalse(result.iloc[4]["experimental_yellow_valid"])
        self.assertTrue(result.iloc[6]["yellow_time_reset"])
        self.assertTrue(result.iloc[6]["experimental_yellow_valid"])

    def test_yellow_permission_layer_needs_reset_after_recent_strong_signal(self) -> None:
        yellow_candidate = pd.Series([False, True, True])
        strong_track_occupancy = pd.Series([True, False, False])
        reset_event = pd.Series([False, True, False])
        strong_trend_running = pd.Series([False, False, False])

        result = yellow_permission_layer(
            yellow_candidate=yellow_candidate,
            strong_track_occupancy=strong_track_occupancy,
            yellow_reset_event=reset_event,
            strong_reset_event=reset_event,
            strong_trend_running=strong_trend_running,
            hard_window=1,
            segment_window=4,
            strong_window=3,
        )

        self.assertTrue(result.iloc[1]["near_strong_track_signal"])
        self.assertFalse(result.iloc[1]["strong_after_reset"])
        self.assertFalse(result.iloc[1]["yellow_strong_permission"])
        self.assertFalse(result.iloc[1]["experimental_yellow_valid"])
        self.assertTrue(result.iloc[2]["strong_reset_after_signal"])
        self.assertTrue(result.iloc[2]["yellow_strong_permission"])
        self.assertTrue(result.iloc[2]["experimental_yellow_valid"])

    def test_yellow_permission_layer_ignores_same_bar_yellow_reset(self) -> None:
        yellow_candidate = pd.Series([False, True, True, True])
        strong_track_occupancy = pd.Series([False] * len(yellow_candidate))
        yellow_reset_event = pd.Series([False, False, True, False])
        strong_reset_event = pd.Series([False] * len(yellow_candidate))
        strong_trend_running = pd.Series([True] * len(yellow_candidate))

        result = yellow_permission_layer(
            yellow_candidate=yellow_candidate,
            strong_track_occupancy=strong_track_occupancy,
            yellow_reset_event=yellow_reset_event,
            strong_reset_event=strong_reset_event,
            strong_trend_running=strong_trend_running,
            hard_window=0,
            segment_window=4,
            strong_window=2,
        )

        self.assertTrue(result.iloc[1]["experimental_yellow_valid"])
        self.assertFalse(result.iloc[2]["yellow_reset_after_signal"])
        self.assertTrue(result.iloc[2]["yellow_after_same_trend"])
        self.assertFalse(result.iloc[2]["experimental_yellow_valid"])
        self.assertTrue(result.iloc[3]["yellow_reset_after_signal"])
        self.assertTrue(result.iloc[3]["experimental_yellow_valid"])


if __name__ == "__main__":
    unittest.main()
