"""Utility per validare i dataset finali."""

from __future__ import annotations

from typing import Any

import pandas as pd


ALLOWED_METHOD_STATUS = {
    "observed_official",
    "distribution_only",
    "estimated_from_distribution",
    "italy_granular_observed",
    "experimental",
    "not_available",
}


def check_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    """Restituisce le colonne obbligatorie mancanti."""
    return [column for column in required_columns if column not in df.columns]


def check_method_status(df: pd.DataFrame) -> list[str]:
    """Controlla che `method_status` contenga solo valori ammessi."""
    if "method_status" not in df.columns:
        return ["Colonna method_status assente"]
    observed = set(df["method_status"].dropna().unique())
    invalid = sorted(observed - ALLOWED_METHOD_STATUS)
    return [f"method_status non ammesso: {value}" for value in invalid]


def check_duplicate_keys(df: pd.DataFrame, key_columns: list[str]) -> int:
    """Conta le righe duplicate rispetto a una chiave logica."""
    existing_keys = [column for column in key_columns if column in df.columns]
    if not existing_keys:
        return 0
    return int(df.duplicated(subset=existing_keys).sum())


def build_validation_report(
    df: pd.DataFrame,
    dataset_name: str,
    required_columns: list[str],
    key_columns: list[str],
) -> dict[str, Any]:
    """Costruisce un report di validazione semplice.

    Il report viene salvato sia in JSON sia in Markdown dagli script di validazione.
    """
    missing_columns = check_required_columns(df, required_columns)
    method_status_errors = check_method_status(df)
    duplicate_count = check_duplicate_keys(df, key_columns)

    return {
        "dataset_name": dataset_name,
        "rows": int(len(df)),
        "columns": list(df.columns),
        "missing_required_columns": missing_columns,
        "method_status_errors": method_status_errors,
        "duplicate_count": duplicate_count,
        "is_valid": not missing_columns and not method_status_errors and duplicate_count == 0,
    }


def validation_report_to_markdown(reports: list[dict[str, Any]]) -> str:
    """Converte una lista di report in Markdown leggibile."""
    lines = ["# Report di validazione", ""]
    for report in reports:
        lines.append(f"## {report['dataset_name']}")
        lines.append("")
        lines.append(f"- Righe: {report['rows']}")
        lines.append(f"- Valido: {report['is_valid']}")
        lines.append(f"- Duplicati: {report['duplicate_count']}")
        lines.append(f"- Colonne obbligatorie mancanti: {report['missing_required_columns']}")
        lines.append(f"- Errori method_status: {report['method_status_errors']}")
        lines.append("")
    return "\n".join(lines)
