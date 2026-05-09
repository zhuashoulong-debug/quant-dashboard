from __future__ import annotations

import pandas as pd

from formula_lab.stock_pool import StockItem, normalize_stock_code


CODE_COLUMNS = ("code", "symbol", "代码", "股票代码", "证券代码")
NAME_COLUMNS = ("name", "名称", "股票简称", "证券简称")


def _first_existing_column(data: pd.DataFrame, candidates: tuple[str, ...]) -> str:
    for column in candidates:
        if column in data.columns:
            return column
    raise ValueError(f"missing any of columns: {', '.join(candidates)}")


def normalize_a_share_universe(raw: pd.DataFrame) -> list[StockItem]:
    code_column = _first_existing_column(raw, CODE_COLUMNS)
    name_column = _first_existing_column(raw, NAME_COLUMNS)

    items: list[StockItem] = []
    seen: set[str] = set()
    for _, row in raw.iterrows():
        raw_code = row[code_column]
        if isinstance(raw_code, str) and raw_code.lower().startswith(("sh", "sz", "bj")):
            raw_code = raw_code[2:]
        try:
            code = normalize_stock_code(raw_code)
        except ValueError:
            continue
        if code in seen:
            continue
        name = "" if pd.isna(row[name_column]) else str(row[name_column]).strip()
        items.append(StockItem(code=code, name=name))
        seen.add(code)

    return sorted(items, key=lambda item: item.code)


def fetch_a_share_universe() -> list[StockItem]:
    import akshare as ak

    errors: list[str] = []
    for provider, fetcher in (
        ("eastmoney_spot", ak.stock_zh_a_spot_em),
        ("sina_spot", ak.stock_zh_a_spot),
        ("exchange_code_name", ak.stock_info_a_code_name),
    ):
        try:
            items = normalize_a_share_universe(fetcher())
            if items:
                return items
            errors.append(f"{provider}: empty universe")
        except Exception as exc:  # noqa: BLE001 - keep fallback provider context.
            errors.append(f"{provider}: {exc}")
    raise RuntimeError("all AKShare A-share universe providers failed; " + " | ".join(errors))
