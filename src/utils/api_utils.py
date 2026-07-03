"""Utility per scaricare dati statistici e convertirli in DataFrame."""

from __future__ import annotations

from itertools import product
from typing import Any

import pandas as pd
import requests


def get_json(url: str, params: dict[str, Any] | None = None, timeout: int = 90) -> dict[str, Any]:
    """Scarica una risposta JSON da un endpoint HTTP."""
    response = requests.get(url, params=params or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def jsonstat_to_dataframe(data: dict[str, Any]) -> pd.DataFrame:
    """Converte una risposta JSON-stat in una tabella pandas."""
    dimension_ids = data.get("id", [])
    values = data.get("value", {})
    statuses = data.get("status", {})

    if not dimension_ids:
        return pd.DataFrame()

    categories_by_dimension: list[list[str]] = []

    for dimension_id in dimension_ids:
        dimension = data.get("dimension", {}).get(dimension_id, {})
        index = dimension.get("category", {}).get("index", {})
        if isinstance(index, dict):
            ordered_codes = [code for code, _ in sorted(index.items(), key=lambda item: item[1])]
        else:
            ordered_codes = list(index)
        categories_by_dimension.append(ordered_codes)

    records: list[dict[str, Any]] = []

    for flat_index, combination in enumerate(product(*categories_by_dimension)):
        if isinstance(values, dict):
            value = values.get(str(flat_index))
        else:
            value = values[flat_index] if flat_index < len(values) else None

        if isinstance(statuses, dict):
            quality_flag = statuses.get(str(flat_index))
        else:
            quality_flag = statuses[flat_index] if flat_index < len(statuses) else None

        record = {dimension_id: combination[i] for i, dimension_id in enumerate(dimension_ids)}
        record["value"] = value
        record["quality_flag"] = quality_flag
        records.append(record)

    return pd.DataFrame.from_records(records)


def scarica_jsonstat_dataset(
    base_url: str,
    dataset_id: str,
    params: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Scarica un dataset JSON-stat e lo converte in DataFrame."""
    url = f"{base_url.rstrip('/')}/{dataset_id}"
    payload = get_json(url, params=params or {})
    return jsonstat_to_dataframe(payload)
