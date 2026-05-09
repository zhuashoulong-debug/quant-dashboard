from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from formula_lab.stock_pool import StockItem


@dataclass(frozen=True)
class DailyCacheMetadata:
    source: str
    provider: str
    market: str
    code: str
    name: str
    adjust: str
    period: str
    start_date: str
    end_date: str
    downloaded_at: str
    rows: int
    first_date: str | None
    last_date: str | None
    columns: list[str]


def metadata_path_for(data_path: str | Path) -> Path:
    path = Path(data_path)
    return path.with_name(f"{path.name}.meta.json")


def build_daily_cache_metadata(
    data: pd.DataFrame,
    stock: StockItem,
    start_date: str,
    end_date: str,
    *,
    source: str = "akshare",
    provider: str | None = None,
    market: str = "a_share",
    adjust: str = "qfq",
    period: str = "daily",
) -> DailyCacheMetadata:
    first_date = None
    last_date = None
    if not data.empty and "date" in data.columns:
        dates = pd.to_datetime(data["date"])
        first_date = dates.min().strftime("%Y-%m-%d")
        last_date = dates.max().strftime("%Y-%m-%d")

    return DailyCacheMetadata(
        source=source,
        provider=provider or str(data.attrs.get("provider", "")),
        market=market,
        code=stock.code,
        name=stock.name,
        adjust=adjust,
        period=period,
        start_date=start_date,
        end_date=end_date,
        downloaded_at=datetime.now(timezone.utc).isoformat(),
        rows=len(data),
        first_date=first_date,
        last_date=last_date,
        columns=[str(column) for column in data.columns],
    )


def write_cache_metadata(metadata: DailyCacheMetadata, data_path: str | Path) -> Path:
    output_path = metadata_path_for(data_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(metadata), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def append_manifest_event(
    manifest_path: str | Path,
    event: dict[str, object],
) -> Path:
    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True))
        handle.write("\n")
    return path
