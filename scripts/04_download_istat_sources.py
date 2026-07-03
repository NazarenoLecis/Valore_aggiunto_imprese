# Crea l'inventario delle fonti ISTAT candidate.
# Variabili operative in src/project_config.py.

from __future__ import annotations

from src.project_config import PROJECT_SETTINGS, SOURCES
from src.sources.istat_sources import crea_inventario_fonti_istat
from src.utils.io_utils import build_path_from_settings, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    df, metadata = crea_inventario_fonti_istat(settings=PROJECT_SETTINGS, sources=SOURCES)
    write_dataframe_csv(df, build_path_from_settings(PROJECT_SETTINGS, "raw", "istat_sources_inventory.csv"))
    write_dataframe_json(df, build_path_from_settings(PROJECT_SETTINGS, "raw", "istat_sources_inventory.json"))
    write_json(metadata, build_path_from_settings(PROJECT_SETTINGS, "raw", "istat_metadata.json"))
    print(f"Inventario ISTAT creato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
