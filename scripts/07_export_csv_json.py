from __future__ import annotations

from pathlib import Path

from src.export.export_csv_json import esporta_dataset_csv_json
from src.project_config import PROJECT_SETTINGS
from src.utils.io_utils import build_path_from_settings, get_project_root, read_dataframe_if_exists

DATASETS = {
    "official_eurostat_sbs": "official_eurostat_sbs.csv",
    "business_demography_distribution": "business_demography_distribution.csv",
    "oecd_sdbs_inventory": "oecd_sdbs_inventory.csv",
    "istat_sources_inventory": "istat_sources_inventory.csv",
}


def main() -> None:
    root = get_project_root()
    csv_dir = Path(root / PROJECT_SETTINGS["paths"]["processed_csv"])
    json_dir = Path(root / PROJECT_SETTINGS["paths"]["processed_json"])

    for dataset_name, filename in DATASETS.items():
        path = build_path_from_settings(PROJECT_SETTINGS, "processed", filename)
        df = read_dataframe_if_exists(path)
        outputs = esporta_dataset_csv_json(df, dataset_name, csv_dir, json_dir)
        print(f"Esportato {dataset_name}: {outputs}")


if __name__ == "__main__":
    main()
