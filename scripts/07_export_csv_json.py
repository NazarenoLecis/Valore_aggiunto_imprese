# Questo script esporta i dataset finali in CSV e JSON.
#
# Obiettivo:
# creare file riutilizzabili da analisi successive o da altri progetti.
# Il repository genera solo output locali. La pubblicazione esterna non è
# gestita da questo progetto.
#
# Output:
# - data/processed_csv/*.csv
# - data/processed_json/*.json
#
# Uso:
# python scripts/07_export_csv_json.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.export.export_csv_json import esporta_dataset_csv_json
from src.utils.io_utils import build_path_from_settings, load_yaml, read_dataframe_if_exists


def main() -> None:
    settings = load_yaml("config/settings.yaml")

    dataset_files = {
        "official_eurostat_sbs": "official_eurostat_sbs.csv",
        "business_demography_distribution": "business_demography_distribution.csv",
        "oecd_sdbs_inventory": "oecd_sdbs_inventory.csv",
        "istat_sources_inventory": "istat_sources_inventory.csv",
    }

    csv_dir = PROJECT_ROOT / settings["paths"]["processed_csv"]
    json_dir = PROJECT_ROOT / settings["paths"]["processed_json"]

    for dataset_name, filename in dataset_files.items():
        path = build_path_from_settings(settings, "processed", filename)
        df = read_dataframe_if_exists(path)
        outputs = esporta_dataset_csv_json(df, dataset_name, csv_dir, json_dir)
        print(f"Esportato {dataset_name}: {outputs}")


if __name__ == "__main__":
    main()
