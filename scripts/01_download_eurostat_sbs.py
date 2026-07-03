# Scarica Eurostat Structural Business Statistics.
# Variabili operative in src/project_config.py.

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.project_config import PROJECT_SETTINGS, SOURCES
from src.sources.eurostat_sbs import scarica_eurostat_sbs
from src.utils.io_utils import build_path_from_settings, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    df, metadata = scarica_eurostat_sbs(settings=PROJECT_SETTINGS, sources=SOURCES)
    write_dataframe_csv(df, build_path_from_settings(PROJECT_SETTINGS, "raw", "eurostat_sbs_raw.csv"))
    write_dataframe_json(df, build_path_from_settings(PROJECT_SETTINGS, "raw", "eurostat_sbs_raw.json"))
    write_json(metadata, build_path_from_settings(PROJECT_SETTINGS, "raw", "eurostat_sbs_metadata.json"))
    print(f"Eurostat SBS scaricato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
