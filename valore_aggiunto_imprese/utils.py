from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from pandas.errors import EmptyDataError

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

ALLOWED_METHOD_STATUS = {
    "observed_official",
    "distribution_only",
    "estimated_from_distribution",
    "italy_granular_observed",
    "experimental",
    "not_available",
}


def get_project_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "README.md").exists() and (
            candidate / "valore_aggiunto_imprese"
        ).exists():
            return candidate
    return current


def ensure_directory(path: str | Path) -> Path:
    root = get_project_root()
    directory = Path(path)
    if not directory.is_absolute():
        directory = root / directory
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def timestamp_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(data: Any, path: str | Path) -> Path:
    output_path = Path(path)
    if not output_path.is_absolute():
        output_path = get_project_root() / output_path
    ensure_directory(output_path.parent)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return output_path


def read_json(path: str | Path) -> Any:
    input_path = Path(path)
    if not input_path.is_absolute():
        input_path = get_project_root() / input_path
    with input_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_dataframe_csv(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    if not output_path.is_absolute():
        output_path = get_project_root() / output_path
    ensure_directory(output_path.parent)
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def write_dataframe_json(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    if not output_path.is_absolute():
        output_path = get_project_root() / output_path
    ensure_directory(output_path.parent)
    write_json(df.to_dict(orient="records"), output_path)
    return output_path


def read_dataframe_if_exists(path: str | Path) -> pd.DataFrame:
    input_path = Path(path)
    if not input_path.is_absolute():
        input_path = get_project_root() / input_path
    if not input_path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(input_path)
    except EmptyDataError:
        return pd.DataFrame()


def build_path_from_settings(settings: dict[str, Any], path_key: str, filename: str) -> Path:
    base_path = settings.get("paths", {}).get(path_key)
    if base_path is None:
        raise KeyError(f"Percorso non trovato: {path_key}")
    return get_project_root() / base_path / filename


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
    labels_by_dimension: dict[str, dict[str, str]] = {}
    for dimension_id in dimension_ids:
        dimension = data.get("dimension", {}).get(dimension_id, {})
        category = dimension.get("category", {})
        index = category.get("index", {})
        labels_by_dimension[dimension_id] = category.get("label", {}) or {}
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
        for i, dimension_id in enumerate(dimension_ids):
            label = labels_by_dimension.get(dimension_id, {}).get(combination[i])
            if label is not None:
                record[f"{dimension_id}_label"] = label
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


def normalizza_nomi_colonne(df: pd.DataFrame) -> pd.DataFrame:
    """Rende i nomi delle colonne piu semplici da usare."""
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
    remaining_columns = [
        column for column in output.columns if column not in REQUIRED_OUTPUT_COLUMNS
    ]
    return output[REQUIRED_OUTPUT_COLUMNS + remaining_columns]


def calcola_quote(
    df: pd.DataFrame,
    group_columns: list[str],
    value_column: str = "value",
    output_column: str = "share",
) -> pd.DataFrame:
    """Calcola quote percentuali dentro gruppi definiti."""
    output = df.copy()
    denominator = output.groupby(group_columns)[value_column].transform("sum")
    output[output_column] = output[value_column] / denominator
    return output


def crea_dataset_vuoto_standard() -> pd.DataFrame:
    """Crea un DataFrame vuoto con lo schema standard."""
    return pd.DataFrame(columns=REQUIRED_OUTPUT_COLUMNS)


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
    """Costruisce un report di validazione semplice."""
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


def salva_dati_grafico(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Salva i dati alla base di un grafico in CSV."""
    return write_dataframe_csv(df, output_path)
