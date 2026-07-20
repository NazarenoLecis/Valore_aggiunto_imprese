"""Download e inventari delle fonti dati."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from valore_aggiunto_imprese.utils import scarica_jsonstat_dataset, timestamp_utc


def scarica_eurostat_sbs(
    settings: dict[str, Any], sources: dict[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Scarica il dataset Eurostat SBS configurato in `config.py`."""
    source_config = sources["eurostat_sbs"]
    base_url = source_config["base_url"]
    dataset_id = source_config["dataset_id"]
    first_year = max(
        int(settings["start_year"]), int(source_config.get("first_year", settings["start_year"]))
    )
    configured_end_year = settings.get("end_year", "latest")
    if configured_end_year == "latest":
        end_year = int(source_config.get("last_year", datetime.now().year))
    else:
        end_year = int(configured_end_year)

    params = {
        "format": "JSON",
        "lang": "en",
        **source_config.get("filters", {}),
        "geo": settings["default_countries"],
        "time": [str(year) for year in range(first_year, end_year + 1)],
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


def scarica_business_demography(
    settings: dict[str, Any], sources: dict[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Scarica il dataset Eurostat Business Demography indicato nella configurazione."""
    source_config = sources["eurostat_business_demography"]
    base_url = source_config["base_url"]
    dataset_id = source_config["dataset_id"]
    first_year = max(
        int(settings["start_year"]),
        int(source_config.get("first_year", settings["start_year"])),
    )
    configured_end_year = settings.get("end_year", "latest")
    if configured_end_year == "latest":
        end_year = int(source_config.get("last_year", datetime.now().year))
    else:
        end_year = min(
            int(configured_end_year),
            int(source_config.get("last_year", configured_end_year)),
        )

    params = {
        "format": "JSON",
        "lang": "en",
        **source_config.get("filters", {}),
        "geo": settings["default_countries"],
        "time": [str(year) for year in range(first_year, end_year + 1)],
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


def crea_inventario_oecd_sdbs(
    settings: dict[str, Any], sources: dict[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Crea una tabella di inventario per la fonte OECD SDBS."""
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


def crea_inventario_fonti_istat(
    settings: dict[str, Any], sources: dict[str, Any]
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Crea un inventario delle fonti ISTAT candidate."""
    source_config = sources["istat"]
    rows = []

    for candidate in source_config.get("candidate_sources", []):
        rows.append(
            {
                "source_name": source_config["source_name"],
                "candidate_source": candidate,
                "country_code": "IT",
                "method_status": "experimental",
                "download_timestamp": timestamp_utc(),
                "notes": "Fonte candidata da verificare manualmente o tramite API ISTAT.",
            }
        )

    df = pd.DataFrame(rows)
    metadata = {
        "source_name": source_config["source_name"],
        "rows": int(len(df)),
        "download_timestamp": timestamp_utc(),
        "note": "Inventario fonti ISTAT candidate.",
    }
    return df, metadata
