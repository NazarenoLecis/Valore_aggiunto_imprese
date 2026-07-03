"""Download Eurostat Structural Business Statistics.

Questa fonte è la base principale per valore aggiunto, imprese e occupazione
per classe dimensionale nei paesi europei.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.utils.api_utils import scarica_jsonstat_dataset
from src.utils.io_utils import timestamp_utc


def scarica_eurostat_sbs(settings: dict[str, Any], sources: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Scarica il dataset Eurostat SBS configurato in `config/sources.yaml`.

    La funzione restituisce sia la tabella sia un dizionario di metadati.
    Gli script decidono poi dove salvare CSV e JSON.
    """
    source_config = sources["eurostat_sbs"]
    base_url = source_config["base_url"]
    dataset_id = source_config["dataset_id"]

    params = {
        "format": "JSON",
        "lang": "en",
    }

    df = scarica_jsonstat_dataset(base_url=base_url, dataset_id=dataset_id, params=params)
    df["source_name"] = source_config["source_name"]
    df["source_dataset_id"] = dataset_id
    df["method_status"] = source_config.get("method_status", "observed_official")
    df["download_timestamp"] = timestamp_utc()

    metadata = {
        "source_name": source_config["source_name"],
        "dataset_id": dataset_id,
        "rows": int(len(df)),
        "download_timestamp": timestamp_utc(),
        "note": source_config.get("note"),
    }

    return df, metadata
