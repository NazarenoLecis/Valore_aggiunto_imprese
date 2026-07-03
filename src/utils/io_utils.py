from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


def get_project_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "README.md").exists() and (candidate / "src").exists():
            return candidate
    return current


def aggiungi_project_root_al_path() -> Path:
    root = get_project_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


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
    return pd.read_csv(input_path)


def build_path_from_settings(settings: dict[str, Any], path_key: str, filename: str) -> Path:
    base_path = settings.get("paths", {}).get(path_key)
    if base_path is None:
        raise KeyError(f"Percorso non trovato: {path_key}")
    return get_project_root() / base_path / filename
