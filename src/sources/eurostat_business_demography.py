"""Download Eurostat Business Demography.

Questa fonte serve soprattutto per distribuzioni granulari di imprese e occupati.
Il valore aggiunto non va imputato automaticamente usando la sola distribuzione
numerica delle imprese.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.utils.api_utils import scarica_jsonstat_dataset
from src.utils.io_utils import timestamp_utc


def scarica_business_demography(settings: dict[str, Any], sources: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Scarica il dataset Eurostat Business Demography indicato nella configurazione."""
    source_config = sources["eurostat_business_demography"]
    base_url = source_config["base_url"]
    dataset_id = source_config["dataset_id"]

    params = {
        "format": "JSON",
        "lang": "en",
    }

    df = scarica_jsonstat_dataset(base_url=base_url, dataset_id=dataset_id, params=params)
    df["source_name"] = source_config["source_name"]
    df["source_dataset_id"] = dataset_id
    df["method_status"] = source_config.get("method_status", "distribution_only")
    df["download_timestamp"] = timestamp_utc()

    metadata = {
        "source_name": source_config["source_name"],
        "dataset_id": dataset_id,
        "rows": int(len(df)),
        "download_timestamp": timestamp_utc(),
        "note": source_config.get("note"),
    }

    return df, metadata
