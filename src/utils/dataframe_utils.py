"""Utility per pulizia e trasformazione dei DataFrame."""

from __future__ import annotations

import pandas as pd


REQUIRED_OUTPUT_COLUMNS = [
    "country_code",
    "country_name",
    "year",
    "source_name",
    "source_dataset_id",
    "sector_code_original",
    "sector_label_original",
    "sector_code_harmonised",
    "sector_label_harmonised",
    "sector_level",
    "size_class_original",
    "size_class_harmonised",
    "metric_code",
    "metric_label",
    "value",
    "unit",
    "method_status",
    "quality_flag",
    "download_timestamp",
    "source_url",
    "notes",
]


def normalizza_nomi_colonne(df: pd.DataFrame) -> pd.DataFrame:
    """Rende i nomi delle colonne più semplici da usare.

    La funzione applica trasformazioni conservative: minuscole, spazi sostituiti
    con underscore e rimozione di caratteri ricorrenti nelle esportazioni.
    """
    clean_columns = []
    for column in df.columns:
        clean = str(column).strip().lower()
        clean = clean.replace(" ", "_").replace("-", "_").replace(".", "_")
        clean_columns.append(clean)
    output = df.copy()
    output.columns = clean_columns
    return output


def aggiungi_colonne_mancanti(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Aggiunge colonne mancanti con valore nullo."""
    output = df.copy()
    for column in columns:
        if column not in output.columns:
            output[column] = None
    return output


def ordina_colonne_output(df: pd.DataFrame) -> pd.DataFrame:
    """Ordina le colonne finali mettendo prima quelle standard."""
    output = aggiungi_colonne_mancanti(df, REQUIRED_OUTPUT_COLUMNS)
    remaining_columns = [column for column in output.columns if column not in REQUIRED_OUTPUT_COLUMNS]
    return output[REQUIRED_OUTPUT_COLUMNS + remaining_columns]


def calcola_quote(
    df: pd.DataFrame,
    group_columns: list[str],
    value_column: str = "value",
    output_column: str = "share",
) -> pd.DataFrame:
    """Calcola quote percentuali dentro gruppi definiti.

    Esempio: quota di valore aggiunto per classe dimensionale dentro paese,
    anno e settore.
    """
    output = df.copy()
    denominator = output.groupby(group_columns)[value_column].transform("sum")
    output[output_column] = output[value_column] / denominator
    return output


def crea_dataset_vuoto_standard() -> pd.DataFrame:
    """Crea un DataFrame vuoto con lo schema standard."""
    return pd.DataFrame(columns=REQUIRED_OUTPUT_COLUMNS)
