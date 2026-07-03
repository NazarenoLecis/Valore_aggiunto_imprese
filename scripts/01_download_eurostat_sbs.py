# Questo script scarica Eurostat Structural Business Statistics.
#
# Obiettivo:
# creare una copia raw della fonte principale per valore aggiunto,
# imprese e occupazione per classe dimensionale.
#
# Input:
# - config/settings.yaml
# - config/sources.yaml
#
# Output:
# - data/raw/eurostat_sbs_raw.csv
# - data/raw/eurostat_sbs_raw.json
# - data/raw/eurostat_sbs_metadata.json
#
# Uso:
# python scripts/01_download_eurostat_sbs.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sources.eurostat_sbs import scarica_eurostat_sbs
from src.utils.io_utils import build_path_from_settings, load_yaml, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    settings = load_yaml("config/settings.yaml")
    sources = load_yaml("config/sources.yaml")

    df, metadata = scarica_eurostat_sbs(settings=settings, sources=sources)

    write_dataframe_csv(df, build_path_from_settings(settings, "raw", "eurostat_sbs_raw.csv"))
    write_dataframe_json(df, build_path_from_settings(settings, "raw", "eurostat_sbs_raw.json"))
    write_json(metadata, build_path_from_settings(settings, "raw", "eurostat_sbs_metadata.json"))

    print(f"Eurostat SBS scaricato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
