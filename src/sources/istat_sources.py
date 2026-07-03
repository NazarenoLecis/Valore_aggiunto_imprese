"""Inventario fonti ISTAT per il modulo Italia.

Il compito iniziale del modulo ISTAT è verificare quali fonti pubbliche possono
supportare un dettaglio più granulare sulle imprese italiane.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.utils.io_utils import timestamp_utc


def crea_inventario_fonti_istat(settings: dict[str, Any], sources: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Crea un inventario delle fonti ISTAT candidate.

    La funzione non forza il download di dataset non ancora mappati. Produce
    una tabella utile per il notebook dedicato alle fonti italiane.
    """
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
