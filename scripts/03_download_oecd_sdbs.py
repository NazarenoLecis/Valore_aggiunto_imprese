# Crea l'inventario OECD SDBS.
# Variabili operative in src/project_config.py.

from __future__ import annotations

from src.project_config import PROJECT_SETTINGS, SOURCES
from src.sources.oecd_sdbs import crea_inventario_oecd_sdbs
from src.utils.io_utils import build_path_from_settings, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    df, metadata = crea_inventario_oecd_sdbs(settings=PROJECT_SETTINGS, sources=SOURCES)
    write_dataframe_csv(df, build_path_from_settings(PROJECT_SETTINGS, "raw", "oecd_sdbs_inventory.csv"))
    write_dataframe_json(df, build_path_from_settings(PROJECT_SETTINGS, "raw", "oecd_sdbs_inventory.json"))
    write_json(metadata, build_path_from_settings(PROJECT_SETTINGS, "raw", "oecd_sdbs_metadata.json"))
    print(f"Inventario OECD SDBS creato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
