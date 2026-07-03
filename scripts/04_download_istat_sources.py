# Questo script crea un inventario delle fonti ISTAT candidate.
#
# Obiettivo:
# verificare quali fonti italiane possono offrire una granularità maggiore
# rispetto ai dataset internazionali.
#
# Output:
# - data/raw/istat_sources_inventory.csv
# - data/raw/istat_sources_inventory.json
# - data/raw/istat_metadata.json
#
# Uso:
# python scripts/04_download_istat_sources.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sources.istat_sources import crea_inventario_fonti_istat
from src.utils.io_utils import build_path_from_settings, load_yaml, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    settings = load_yaml("config/settings.yaml")
    sources = load_yaml("config/sources.yaml")

    df, metadata = crea_inventario_fonti_istat(settings=settings, sources=sources)

    write_dataframe_csv(df, build_path_from_settings(settings, "raw", "istat_sources_inventory.csv"))
    write_dataframe_json(df, build_path_from_settings(settings, "raw", "istat_sources_inventory.json"))
    write_json(metadata, build_path_from_settings(settings, "raw", "istat_metadata.json"))

    print(f"Inventario ISTAT creato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
