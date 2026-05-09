from __future__ import annotations

import math

import pandas as pd

from formula_lab.indicators import add_boll_pctb


def ref(values: pd.Series, periods: int = 1) -> pd.Series:
    return values.shift(periods)


def rolling_count(condition: pd.Series, window: int) -> pd.Series:
    return condition.fillna(False).astype(int).rolling(window, min_periods=1).sum()


def barslast(condition: pd.Series) -> pd.Series:
    last_seen: int | None = None
    distances: list[float] = []
    for index, flag in enumerate(condition.fillna(False).astype(bool)):
        if flag:
            last_seen = index
            distances.append(0.0)
        elif last_seen is None:
            distances.append(math.inf)
        else:
            distances.append(float(index - last_seen))
    return pd.Series(distances, index=condition.index)


def safe_divide(numerator: pd.Series, denominator: pd.Series, floor: float = 0.0001) -> pd.Series:
    safe_denominator = denominator.where(denominator.abs() > floor, floor)
    return numerator / safe_denominator


def choose(condition: pd.Series, truthy: pd.Series | float, falsy: pd.Series | float) -> pd.Series:
    truthy_series = truthy if isinstance(truthy, pd.Series) else pd.Series(truthy, index=condition.index)
    falsy_series = falsy if isinstance(falsy, pd.Series) else pd.Series(falsy, index=condition.index)
    return truthy_series.where(condition.fillna(False), falsy_series)


def add_a3b2b1_backgrounds(data: pd.DataFrame) -> pd.DataFrame:
    required = {"high", "low", "close"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"daily data missing columns: {', '.join(sorted(missing))}")

    result = add_boll_pctb(data)
    close = result["close"].astype(float)
    high = result["high"].astype(float)
    low = result["low"].astype(float)
    prev_close = ref(close)

    mid = result["boll_mid"]
    upper = result["boll_upper"]
    lower = result["boll_lower"]
    pctb = result["pctb"]

    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(20, min_periods=1).mean()
    keltner_upper = mid + 1.5 * atr
    keltner_lower = mid - 1.5 * atr
    squeeze = (upper < keltner_upper) & (lower > keltner_lower)
    near_squeeze = rolling_count(squeeze, 2) >= 1
    effective_squeeze = (rolling_count(squeeze, 5) >= 2) & (barslast(squeeze) <= 2)

    bandwidth = safe_divide(upper - lower, mid)
    long_avg_width = bandwidth.rolling(60, min_periods=1).mean()
    short_avg_width = bandwidth.rolling(20, min_periods=1).mean()
    long_high_width = bandwidth.rolling(60, min_periods=1).max()
    short_high_width = bandwidth.rolling(20, min_periods=1).max()
    long_low_width = bandwidth.rolling(60, min_periods=1).min()
    short_low_width = bandwidth.rolling(20, min_periods=1).min()

    effective_avg_width = choose(long_avg_width > 0.001, long_avg_width, choose(short_avg_width > 0.001, short_avg_width, bandwidth))
    effective_high_width = choose(long_high_width > 0.001, long_high_width, choose(short_high_width > 0.001, short_high_width, bandwidth))
    effective_low_width = choose(long_low_width > 0.001, long_low_width, choose(short_low_width > 0.001, short_low_width, bandwidth))

    previous_effective_avg_width = choose(
        ref(effective_avg_width) > 0.001,
        ref(effective_avg_width),
        ref(bandwidth).clip(lower=0.0001),
    )
    previous_effective_high_width = choose(
        ref(effective_high_width) > 0.001,
        ref(effective_high_width),
        ref(bandwidth).clip(lower=0.0001),
    )
    previous_effective_low_width = choose(
        ref(effective_low_width) > 0.001,
        ref(effective_low_width),
        ref(bandwidth).clip(lower=0.0001),
    )

    current_width_ratio = safe_divide(bandwidth, effective_avg_width)
    previous_width_ratio = safe_divide(ref(bandwidth), previous_effective_avg_width)
    width_abs_high = bandwidth > 0.35
    previous_width_abs_high = ref(bandwidth) > 0.35
    width_relative_high = (current_width_ratio > 1.35) | (previous_width_ratio > 1.35)
    width_near_high = bandwidth >= effective_high_width * 0.85
    width_speed = bandwidth - ref(bandwidth, 5)
    width_speed_rate = safe_divide(width_speed, ref(bandwidth, 5))
    micro_expand_limit = 0.04
    hard_high_width = width_abs_high | previous_width_abs_high | width_relative_high
    soft_hold_width = width_near_high & (width_speed_rate <= micro_expand_limit)
    hold_width = hard_high_width | soft_hold_width
    pre_start_hold_width = ref(hold_width).fillna(False).astype(bool)
    previous_width_near_high = ref(width_near_high).fillna(False).astype(bool)

    old_effective_squeeze = ref(effective_squeeze).fillna(False) | (ref(rolling_count(squeeze, 10)) >= 1)
    daily_scattered_squeeze = (rolling_count(squeeze, 10) >= 2) & (rolling_count(squeeze, 3) >= 1)
    squeeze_width_ok = safe_divide(bandwidth, previous_effective_avg_width) < 1.15
    squeeze_width_ok = squeeze_width_ok & ~pre_start_hold_width & ~previous_width_near_high
    new_effective_squeeze = (ref(effective_squeeze).fillna(False) | daily_scattered_squeeze) & squeeze_width_ok
    width_block = old_effective_squeeze & ~squeeze_width_ok

    bandwidth_high_before = ref(bandwidth.rolling(20, min_periods=1).max())
    bandwidth_low_near = ref(bandwidth.rolling(10, min_periods=1).min())
    shrink_amplitude = safe_divide(bandwidth_low_near, bandwidth_high_before) < 0.85
    compressed_low = bandwidth_low_near < previous_effective_avg_width * 0.98
    compressed_low = compressed_low | (bandwidth_low_near <= previous_effective_low_width * 1.25)
    narrowing = bandwidth < ref(bandwidth)
    narrow_count = ref(rolling_count(narrowing, 10))
    effective_narrow = narrow_count >= 4
    contraction_process = shrink_amplitude | effective_narrow
    old_true_contraction = old_effective_squeeze | (compressed_low & contraction_process)
    new_true_contraction = new_effective_squeeze | (compressed_low & contraction_process)

    late_had_squeeze = ref(rolling_count(squeeze, 10)) >= 1
    position_high = high.rolling(500, min_periods=1).max()
    position_low = low.rolling(500, min_periods=1).min()
    two_year_position = safe_divide(close - position_low, position_high - position_low)
    high_position = two_year_position >= 0.80
    low_position = two_year_position <= 0.40
    late_non_high_abs_width_line = choose(low_position, 0.28, 0.25)
    late_abs_width_line = choose(high_position, 0.22, late_non_high_abs_width_line)
    late_abs_width_ok = bandwidth < late_abs_width_line
    late_near_width_not_break = bandwidth <= ref(bandwidth.rolling(5, min_periods=1).max()) * 1.03
    late_avg_width_ok = safe_divide(bandwidth, previous_effective_avg_width) < 1.08
    late_speed_ok = width_speed_rate <= micro_expand_limit
    late_width_not_expand = late_abs_width_ok & late_near_width_not_break & late_avg_width_ok
    late_width_not_expand = late_width_not_expand & ~pre_start_hold_width & ~previous_width_near_high
    late_width_not_expand = late_width_not_expand & late_speed_ok
    late_squeeze_background = late_had_squeeze & late_width_not_expand

    cross_pctb_1 = (pctb > 1) & (ref(pctb) <= 1)
    manual_cross = (ref(pctb) < 1) & (pctb >= 1)
    cross_pullback_low = ref(pctb.rolling(5, min_periods=1).min())
    recent_above_track = ref(rolling_count(pctb > 1, 5)) >= 1
    shallow_recross = recent_above_track & (cross_pullback_low > 0.85)
    effective_cross_1 = cross_pctb_1 & ~shallow_recross
    bars_count = pd.Series(range(1, len(result) + 1), index=result.index)
    display_permission = bars_count > 120
    diagnostic_k = display_permission & effective_cross_1

    result["tr"] = tr
    result["atr20"] = atr
    result["keltner_upper"] = keltner_upper
    result["keltner_lower"] = keltner_lower
    result["squeeze"] = squeeze.fillna(False)
    result["near_squeeze"] = near_squeeze.fillna(False)
    result["effective_squeeze"] = effective_squeeze.fillna(False)
    result["bandwidth"] = bandwidth
    result["current_width_ratio"] = current_width_ratio
    result["previous_width_ratio"] = previous_width_ratio
    result["width_near_high"] = width_near_high.fillna(False)
    result["width_speed_rate"] = width_speed_rate
    result["pre_start_hold_width"] = pre_start_hold_width.fillna(False)
    result["old_effective_squeeze"] = old_effective_squeeze.fillna(False)
    result["new_effective_squeeze"] = new_effective_squeeze.fillna(False)
    result["width_block"] = width_block.fillna(False)
    result["contraction_process"] = contraction_process.fillna(False)
    result["old_true_contraction"] = old_true_contraction.fillna(False)
    result["new_true_contraction"] = new_true_contraction.fillna(False)
    result["late_squeeze_background"] = late_squeeze_background.fillna(False)
    result["cross_pctb_1"] = cross_pctb_1.fillna(False)
    result["manual_cross"] = manual_cross.fillna(False)
    result["shallow_recross"] = shallow_recross.fillna(False)
    result["effective_cross_1"] = effective_cross_1.fillna(False)
    result["diagnostic_k"] = diagnostic_k.fillna(False)

    result["old_near_squeeze"] = ref(near_squeeze).fillna(False)
    result["old_yesterday_contraction"] = ref(old_true_contraction).fillna(False)
    result["old_today_contraction"] = old_true_contraction.fillna(False)
    result["old_breakthrough_background"] = (
        result["old_near_squeeze"]
        | result["old_yesterday_contraction"]
        | result["old_today_contraction"]
    )

    result["new_near_squeeze"] = ref(near_squeeze).fillna(False)
    result["new_late_squeeze"] = late_squeeze_background.fillna(False)
    result["new_yesterday_contraction"] = ref(new_true_contraction).fillna(False)
    result["new_today_contraction"] = new_true_contraction.fillna(False)
    result["new_breakthrough_background"] = (
        result["new_near_squeeze"]
        | result["new_late_squeeze"]
        | result["new_yesterday_contraction"]
        | result["new_today_contraction"]
    )

    result["old_blue_squeeze_background"] = (
        ref(effective_squeeze).fillna(False)
        | (ref(rolling_count(squeeze, 10)) >= 2)
    )
    return result
