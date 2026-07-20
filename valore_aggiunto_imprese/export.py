"""Funzioni per esportare dataset finali in CSV e JSON."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from valore_aggiunto_imprese.utils import write_dataframe_csv, write_dataframe_json


def esporta_dataset_csv_json(
    df: pd.DataFrame,
    dataset_name: str,
    csv_dir: str | Path,
    json_dir: str | Path,
) -> dict[str, str]:
    """Esporta un DataFrame in CSV e JSON.

    Restituisce i percorsi dei file creati, utili per report e log finali.
    """
    csv_path = Path(csv_dir) / f"{dataset_name}.csv"
    json_path = Path(json_dir) / f"{dataset_name}.json"

    written_csv = write_dataframe_csv(df, csv_path)
    written_json = write_dataframe_json(df, json_path)

    return {
        "csv": str(written_csv),
        "json": str(written_json),
    }
