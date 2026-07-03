# Questo script prepara l'inventario OECD SDBS.
#
# Obiettivo:
# mantenere nella pipeline una traccia esplicita della fonte OCSE da usare
# per il confronto internazionale.
#
# In questa prima versione il download completo OECD viene lasciato a una fase
# successiva, dopo verifica del mapping SDMX nel notebook dedicato.
#
# Uso:
# python scripts/03_download_oecd_sdbs.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sources.oecd_sdbs import crea_inventario_oecd_sdbs
from src.utils.io_utils import build_path_from_settings, load_yaml, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    settings = load_yaml("config/settings.yaml")
    sources = load_yaml("config/sources.yaml")

    df, metadata = crea_inventario_oecd_sdbs(settings=settings, sources=sources)

    write_dataframe_csv(df, build_path_from_settings(settings, "raw", "oecd_sdbs_inventory.csv"))
    write_dataframe_json(df, build_path_from_settings(settings, "raw", "oecd_sdbs_inventory.json"))
    write_json(metadata, build_path_from_settings(settings, "raw", "oecd_sdbs_metadata.json"))

    print(f"Inventario OECD SDBS creato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
