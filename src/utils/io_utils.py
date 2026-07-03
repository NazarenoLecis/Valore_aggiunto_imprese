"""Utility di input/output usate da tutta la pipeline.

Il progetto non usa argparse. Gli script leggono i parametri dai file YAML
in `config/` e salvano gli output nelle cartelle locali definite in
`config/settings.yaml`.

Questo file contiene solo funzioni. Non contiene classi e non richiede
file `__init__.py`.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def get_project_root() -> Path:
    """Restituisce la root del progetto.

    La funzione risale dalle sottocartelle fino a trovare `README.md` e `config/`.
    Serve per eseguire gli script da qualunque cartella senza usare percorsi assoluti.
    """
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "README.md").exists() and (candidate / "config").exists():
            return candidate
    return current


def aggiungi_project_root_al_path() -> Path:
    """Aggiunge la root del progetto a sys.path.

    Gli script in `scripts/` importano funzioni da `src/` senza installare il
    progetto come pacchetto Python e senza usare file `__init__.py`.
    """
    root = get_project_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Carica un file YAML.

    Il percorso può essere assoluto oppure relativo alla root del progetto.
    """
    root = get_project_root()
    yaml_path = Path(path)
    if not yaml_path.is_absolute():
        yaml_path = root / yaml_path
    with yaml_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def ensure_directory(path: str | Path) -> Path:
    """Crea una cartella se non esiste."""
    root = get_project_root()
    directory = Path(path)
    if not directory.is_absolute():
        directory = root / directory
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def timestamp_utc() -> str:
    """Restituisce un timestamp UTC in formato ISO."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(data: Any, path: str | Path) -> Path:
    """Scrive un oggetto Python in JSON leggibile.

    I JSON finali sono pensati per essere riutilizzati da analisi successive.
    Per questo motivo vengono scritti con indentazione e caratteri Unicode leggibili.
    """
    output_path = Path(path)
    if not output_path.is_absolute():
        output_path = get_project_root() / output_path
    ensure_directory(output_path.parent)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return output_path


def read_json(path: str | Path) -> Any:
    """Legge un file JSON."""
    input_path = Path(path)
    if not input_path.is_absolute():
        input_path = get_project_root() / input_path
    with input_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_dataframe_csv(df: pd.DataFrame, path: str | Path) -> Path:
    """Scrive un DataFrame in CSV UTF-8.

    I CSV sono il formato tabellare principale prodotto dal repository.
    """
    output_path = Path(path)
    if not output_path.is_absolute():
        output_path = get_project_root() / output_path
    ensure_directory(output_path.parent)
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def write_dataframe_json(df: pd.DataFrame, path: str | Path) -> Path:
    """Scrive un DataFrame in JSON orientato a record.

    Il formato `records` produce una lista di oggetti, semplice da leggere in
    Python, JavaScript e strumenti di data visualization.
    """
    output_path = Path(path)
    if not output_path.is_absolute():
        output_path = get_project_root() / output_path
    ensure_directory(output_path.parent)
    records = df.to_dict(orient="records")
    write_json(records, output_path)
    return output_path


def read_dataframe_if_exists(path: str | Path) -> pd.DataFrame:
    """Legge un CSV se esiste, altrimenti restituisce un DataFrame vuoto.

    Questa funzione permette alla pipeline di proseguire anche quando una fonte
    non è ancora implementata o non è disponibile.
    """
    input_path = Path(path)
    if not input_path.is_absolute():
        input_path = get_project_root() / input_path
    if not input_path.exists():
        return pd.DataFrame()
    return pd.read_csv(input_path)


def build_path_from_settings(settings: dict[str, Any], path_key: str, filename: str) -> Path:
    """Costruisce un percorso usando la sezione `paths` di settings.yaml."""
    base_path = settings.get("paths", {}).get(path_key)
    if base_path is None:
        raise KeyError(f"Percorso non trovato in settings.yaml: {path_key}")
    return get_project_root() / base_path / filename
