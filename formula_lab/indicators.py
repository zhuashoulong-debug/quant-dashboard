from __future__ import annotations

import pandas as pd


def add_boll_pctb(
    data: pd.DataFrame,
    window: int = 20,
    width: float = 2.0,
) -> pd.DataFrame:
    """Add BOLL(20,2) and PCTB using the Eastmoney/Tongdaxin sample std style."""
    if "close" not in data.columns:
        raise ValueError("daily data must contain a close column")

    result = data.copy()
    close = result["close"].astype(float)
    mid = close.rolling(window).mean()
    std = close.rolling(window).std(ddof=1)
    upper = mid + width * std
    lower = mid - width * std
    band_width = upper - lower
    pctb_denominator = band_width.where(band_width.abs() > 0.0001, 0.0001)

    result["boll_mid"] = mid
    result["boll_upper"] = upper
    result["boll_lower"] = lower
    result["pctb"] = (close - lower) / pctb_denominator
    return result
