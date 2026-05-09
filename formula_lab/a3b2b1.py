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


def yellow_permission_layer(
    yellow_candidate: pd.Series,
    strong_track_occupancy: pd.Series,
    yellow_reset_event: pd.Series,
    strong_reset_event: pd.Series,
    strong_trend_running: pd.Series,
    hard_window: int = 8,
    segment_window: int = 20,
    strong_window: int = 8,
) -> pd.DataFrame:
    near_strong_track_signal = ref(rolling_count(strong_track_occupancy, strong_window), 1) > 0
    last_yellow_index: int | None = None
    last_yellow_reset_index: int | None = None
    last_strong_index: int | None = None
    last_strong_reset_index: int | None = None
    rows: list[dict[str, bool]] = []

    for position, index in enumerate(yellow_candidate.index):
        bars_since_yellow = math.inf if last_yellow_index is None else position - last_yellow_index
        bars_since_strong = math.inf if last_strong_index is None else position - last_strong_index
        time_reset = last_yellow_index is not None and bars_since_yellow > segment_window
        yellow_reset_after_signal = (
            last_yellow_index is not None
            and last_yellow_reset_index is not None
            and last_yellow_reset_index > last_yellow_index
        )
        after_reset = yellow_reset_after_signal or time_reset
        strong_reset_after_signal = (
            last_strong_index is not None
            and last_strong_reset_index is not None
            and last_strong_reset_index > last_strong_index
        )
        strong_time_reset = last_strong_index is not None and bars_since_strong > strong_window
        strong_after_reset = strong_reset_after_signal or strong_time_reset
        hard_cooling = last_yellow_index is not None and bars_since_yellow <= hard_window
        after_same_trend = (
            last_yellow_index is not None
            and bars_since_yellow <= segment_window
            and bool(strong_trend_running.loc[index])
            and not after_reset
        )
        self_permission = not hard_cooling and not after_same_trend
        strong_permission = (not bool(near_strong_track_signal.loc[index])) or strong_after_reset
        display_permission = self_permission and strong_permission
        yellow_valid = bool(yellow_candidate.loc[index]) and display_permission

        rows.append(
            {
                "near_strong_track_signal": bool(near_strong_track_signal.loc[index]),
                "yellow_reset_after_signal": bool(yellow_reset_after_signal),
                "yellow_time_reset": bool(time_reset),
                "yellow_after_reset": bool(after_reset),
                "strong_reset_after_signal": bool(strong_reset_after_signal),
                "strong_time_reset": bool(strong_time_reset),
                "strong_after_reset": bool(strong_after_reset),
                "yellow_hard_cooling": bool(hard_cooling),
                "yellow_after_same_trend": bool(after_same_trend),
                "yellow_self_permission": bool(self_permission),
                "yellow_strong_permission": bool(strong_permission),
                "yellow_display_permission": bool(display_permission),
                "yellow_fresh_permission": bool(self_permission),
                "experimental_yellow_valid": bool(yellow_valid),
            }
        )

        if yellow_valid:
            last_yellow_index = position
        if bool(strong_track_occupancy.loc[index]):
            last_strong_index = position
        if bool(yellow_reset_event.loc[index]):
            last_yellow_reset_index = position
        if bool(strong_reset_event.loc[index]):
            last_strong_reset_index = position

    return pd.DataFrame(rows, index=yellow_candidate.index)


def add_a3b2b1_backgrounds(data: pd.DataFrame) -> pd.DataFrame:
    required = {"open", "high", "low", "close"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"daily data missing columns: {', '.join(sorted(missing))}")

    result = add_boll_pctb(data)
    open_ = result["open"].astype(float)
    close = result["close"].astype(float)
    high = result["high"].astype(float)
    low = result["low"].astype(float)
    if "amount" in result.columns:
        amount = result["amount"].astype(float)
    elif "volume" in result.columns:
        amount = result["volume"].astype(float) * close * 100
    else:
        amount = pd.Series(0.0, index=result.index)
    prev_close = ref(close)

    mid = result["boll_mid"]
    upper = result["boll_upper"]
    lower = result["boll_lower"]
    pctb = result["pctb"]

    price_range = (high - low).clip(lower=0.0001)
    entity = (close - open_).abs()
    body_ratio = entity / price_range
    entity_high = pd.concat([close, open_], axis=1).max(axis=1)
    entity_low = pd.concat([close, open_], axis=1).min(axis=1)
    upper_shadow_ratio = (high - entity_high) / price_range
    lower_shadow_ratio = (entity_low - low) / price_range
    close_position = (close - low) / price_range
    bullish_strong = (close > open_) & (body_ratio >= 0.45)
    long_upper_shadow = upper_shadow_ratio >= 0.45
    obvious_long_upper_shadow = upper_shadow_ratio >= 0.55
    extreme_long_upper_shadow = upper_shadow_ratio >= 0.65

    amount_ma20 = amount.rolling(20, min_periods=1).mean()
    has_amount = (amount > 0) & (amount_ma20 > 0)
    amount_ratio = safe_divide(amount, amount_ma20)
    warm_amount = has_amount & (amount >= amount_ma20)
    large_amount = has_amount & (amount >= amount_ma20 * 1.2)
    shrinking_amount = has_amount & (amount <= amount_ma20 * 0.8)
    huge_amount = has_amount & (amount >= amount_ma20 * 1.8)
    structure_break_up = close > ref(entity_high.rolling(20, min_periods=1).max())
    structure_break_down = close < ref(entity_low.rolling(20, min_periods=1).min())

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
    result["price_range"] = price_range
    result["body_ratio"] = body_ratio
    result["upper_shadow_ratio"] = upper_shadow_ratio
    result["lower_shadow_ratio"] = lower_shadow_ratio
    result["close_position"] = close_position
    result["bullish_strong"] = bullish_strong.fillna(False)
    result["long_upper_shadow"] = long_upper_shadow.fillna(False)
    result["obvious_long_upper_shadow"] = obvious_long_upper_shadow.fillna(False)
    result["extreme_long_upper_shadow"] = extreme_long_upper_shadow.fillna(False)
    result["amount_ma20"] = amount_ma20
    result["amount_ratio"] = amount_ratio
    result["warm_amount"] = warm_amount.fillna(False)
    result["large_amount"] = large_amount.fillna(False)
    result["shrinking_amount"] = shrinking_amount.fillna(False)
    result["huge_amount"] = huge_amount.fillna(False)
    result["entity_high"] = entity_high
    result["entity_low"] = entity_low
    result["structure_break_up"] = structure_break_up.fillna(False)
    result["structure_break_down"] = structure_break_down.fillna(False)
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

    breakthrough_background = result["new_breakthrough_background"]
    deep_limit = 0.30
    pre_start_relative_high = safe_divide(ref(bandwidth), previous_effective_high_width)
    platform_hot_state = pd.Series(False, index=result.index)
    mid_contraction_breakthrough = pd.Series(False, index=result.index)
    blue_compression_quality = (
        (previous_width_ratio < 1.05)
        & (pre_start_relative_high < 0.70)
        & ~pre_start_hold_width
        & ~previous_width_near_high
        & ~platform_hot_state
    )
    blue_squeeze_background = new_effective_squeeze
    blue_contraction_background = ref(new_true_contraction).fillna(False) | new_true_contraction | mid_contraction_breakthrough
    yesterday_contraction_breakthrough = ref(new_true_contraction).fillna(False)
    blue_quality_background = (
        blue_squeeze_background
        | (blue_contraction_background & contraction_process)
        | yesterday_contraction_breakthrough
    ) & blue_compression_quality
    warm_up_base = (
        effective_cross_1
        & breakthrough_background
        & (pctb < 1.10)
        & (ref(pctb) < 1)
    )
    warm_up = warm_up_base & (warm_amount | structure_break_up) & ~long_upper_shadow
    violent_up_raw = (
        effective_cross_1
        & breakthrough_background
        & (ref(pctb) < 1)
        & (pctb >= 1.10)
        & (pctb < 1 + deep_limit)
    )
    violent_up = violent_up_raw & (large_amount | structure_break_up) & bullish_strong & ~long_upper_shadow
    violent_up_risk = violent_up_raw & long_upper_shadow
    extreme_up_raw = breakthrough_background & (ref(pctb) < 1) & (pctb >= 1 + deep_limit)
    extreme_up = extreme_up_raw & (large_amount | structure_break_up) & bullish_strong & ~long_upper_shadow
    extreme_up_risk = extreme_up_raw & (long_upper_shadow | huge_amount)
    warm_source = warm_up
    violent_source = violent_up
    blue_warm_source = warm_source & blue_quality_background
    blue_violent_source = violent_source & blue_quality_background
    yellow_warm_source = warm_source & ~blue_quality_background
    yellow_violent_source = violent_source & ~blue_quality_background
    blue_signal_source = blue_warm_source | blue_violent_source
    yellow_signal_source = yellow_warm_source | yellow_violent_source
    first_expand_start = pd.Series(False, index=result.index)
    speed_valid = pd.Series(False, index=result.index)
    speed_after_running = pd.Series(False, index=result.index)
    rush_valid = pd.Series(False, index=result.index)
    blue_warm_valid = blue_warm_source & ~first_expand_start & ~speed_valid & ~speed_after_running
    blue_violent_valid = blue_violent_source & ~first_expand_start
    blue_valid = blue_warm_valid | blue_violent_valid
    strong_track_occupancy = first_expand_start | speed_valid | rush_valid | blue_valid
    yellow_candidate_valid = (
        yellow_signal_source
        & ~first_expand_start
        & ~speed_valid
        & ~speed_after_running
    )
    old_yellow_display_occupancy = yellow_signal_source
    old_candidate_cooling = ref(rolling_count(old_yellow_display_occupancy, 8), 1) > 0
    yellow_reset_pullback = pctb < 0.50
    yellow_recontraction_reset = new_effective_squeeze | new_true_contraction
    yellow_reset_shape = yellow_reset_pullback | yellow_recontraction_reset
    strong_trend_running = (pctb > 0.90) & (close >= mid) & ~yellow_reset_shape
    yellow_permissions = yellow_permission_layer(
        yellow_candidate=yellow_candidate_valid.fillna(False),
        strong_track_occupancy=strong_track_occupancy.fillna(False),
        yellow_reset_event=yellow_reset_shape.fillna(False),
        strong_reset_event=yellow_reset_shape.fillna(False),
        strong_trend_running=strong_trend_running.fillna(False),
    )
    yellow_display_permission = yellow_permissions["yellow_display_permission"]
    yellow_fresh_permission = yellow_permissions["yellow_fresh_permission"]
    yellow_warm_valid = (
        yellow_warm_source
        & yellow_display_permission
        & yellow_fresh_permission
        & ~first_expand_start
        & ~speed_valid
        & ~speed_after_running
    )
    yellow_violent_valid = (
        yellow_violent_source
        & yellow_display_permission
        & yellow_fresh_permission
        & ~first_expand_start
        & ~speed_valid
        & ~speed_after_running
    )
    yellow_valid = yellow_warm_valid | yellow_violent_valid
    effective_start_signal_pre = first_expand_start | speed_valid | blue_valid | rush_valid | yellow_valid

    result["warm_up_base"] = warm_up_base.fillna(False)
    result["warm_up"] = warm_up.fillna(False)
    result["violent_up_raw"] = violent_up_raw.fillna(False)
    result["violent_up"] = violent_up.fillna(False)
    result["violent_up_risk"] = violent_up_risk.fillna(False)
    result["extreme_up_raw"] = extreme_up_raw.fillna(False)
    result["extreme_up"] = extreme_up.fillna(False)
    result["extreme_up_risk"] = extreme_up_risk.fillna(False)
    result["pre_start_relative_high"] = pre_start_relative_high
    result["platform_hot_state"] = platform_hot_state.fillna(False)
    result["mid_contraction_breakthrough"] = mid_contraction_breakthrough.fillna(False)
    result["blue_compression_quality"] = blue_compression_quality.fillna(False)
    result["blue_squeeze_background"] = blue_squeeze_background.fillna(False)
    result["blue_contraction_background"] = blue_contraction_background.fillna(False)
    result["yesterday_contraction_breakthrough"] = yesterday_contraction_breakthrough.fillna(False)
    result["blue_quality_background"] = blue_quality_background.fillna(False)
    result["warm_source"] = warm_source.fillna(False)
    result["violent_source"] = violent_source.fillna(False)
    result["blue_warm_source"] = blue_warm_source.fillna(False)
    result["blue_violent_source"] = blue_violent_source.fillna(False)
    result["yellow_warm_source"] = yellow_warm_source.fillna(False)
    result["yellow_violent_source"] = yellow_violent_source.fillna(False)
    result["blue_signal_source"] = blue_signal_source.fillna(False)
    result["yellow_signal_source"] = yellow_signal_source.fillna(False)
    result["first_expand_start"] = first_expand_start.fillna(False)
    result["speed_valid"] = speed_valid.fillna(False)
    result["speed_after_running"] = speed_after_running.fillna(False)
    result["rush_valid"] = rush_valid.fillna(False)
    result = result.copy()
    result["strong_track_occupancy"] = strong_track_occupancy.fillna(False)
    result["yellow_candidate_valid"] = yellow_candidate_valid.fillna(False)
    result["old_yellow_display_occupancy"] = old_yellow_display_occupancy.fillna(False)
    result["old_candidate_cooling"] = old_candidate_cooling.fillna(False)
    result["yellow_reset_pullback"] = yellow_reset_pullback.fillna(False)
    result["yellow_recontraction_reset"] = yellow_recontraction_reset.fillna(False)
    result["strong_trend_running"] = strong_trend_running.fillna(False)
    for column in yellow_permissions.columns:
        result[column] = yellow_permissions[column].fillna(False)
    result["yellow_display_permission"] = yellow_display_permission.fillna(False)
    result["yellow_fresh_permission"] = yellow_fresh_permission.fillna(False)
    result["blue_warm_valid"] = blue_warm_valid.fillna(False)
    result["blue_violent_valid"] = blue_violent_valid.fillna(False)
    result["blue_valid"] = blue_valid.fillna(False)
    result["yellow_warm_valid"] = yellow_warm_valid.fillna(False)
    result["yellow_violent_valid"] = yellow_violent_valid.fillna(False)
    result["yellow_valid"] = yellow_valid.fillna(False)
    result["effective_start_signal_pre"] = effective_start_signal_pre.fillna(False)

    result["old_blue_squeeze_background"] = (
        ref(effective_squeeze).fillna(False)
        | (ref(rolling_count(squeeze, 10)) >= 2)
    )
    return result
