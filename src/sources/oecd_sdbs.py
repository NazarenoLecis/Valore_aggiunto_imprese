"""Modulo OECD SDBS.

La fonte OECD usa una struttura API diversa da Eurostat. In questa prima
versione il modulo crea un inventario operativo e prepara lo spazio per il
download effettivo.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.utils.io_utils import timestamp_utc


def crea_inventario_oecd_sdbs(settings: dict[str, Any], sources: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Crea una tabella di inventario per la fonte OECD SDBS.

    La funzione permette di mantenere la pipeline completa anche prima di
    finalizzare il mapping tecnico dell'endpoint OECD.
    """
    source_config = sources["oecd_sdbs"]
    row = {
        "source_name": source_config["source_name"],
        "source_dataset_id": source_config["dataset_id"],
        "base_url": source_config["base_url"],
        "method_status": source_config.get("method_status", "observed_official"),
        "download_timestamp": timestamp_utc(),
        "notes": source_config.get("note"),
    }
    df = pd.DataFrame([row])
    metadata = {
        "source_name": source_config["source_name"],
        "dataset_id": source_config["dataset_id"],
        "rows": int(len(df)),
        "download_timestamp": timestamp_utc(),
        "note": "Inventario creato. Download OECD da finalizzare con mapping SDMX.",
    }
    return df, metadata
