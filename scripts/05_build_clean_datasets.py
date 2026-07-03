# Questo script costruisce dataset puliti a partire dai file raw.
#
# Obiettivo:
# applicare uno schema comune ai dati scaricati dalle fonti.
#
# Input:
# - data/raw/eurostat_sbs_raw.csv
# - data/raw/business_demography_raw.csv
# - data/raw/oecd_sdbs_inventory.csv
# - data/raw/istat_sources_inventory.csv
#
# Output:
# - data/processed/official_eurostat_sbs.csv
# - data/processed/business_demography_distribution.csv
# - data/processed/oecd_sdbs_inventory.csv
# - data/processed/istat_sources_inventory.csv
#
# Uso:
# python scripts/05_build_clean_datasets.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.transform.build_clean_datasets import prepara_dataset_generico
from src.utils.io_utils import build_path_from_settings, load_yaml, read_dataframe_if_exists, write_dataframe_csv


def main() -> None:
    settings = load_yaml("config/settings.yaml")

    jobs = [
        {
            "input": "eurostat_sbs_raw.csv",
            "output": "official_eurostat_sbs.csv",
            "source_name": "Eurostat Structural Business Statistics",
            "dataset_id": "sbs_sc_ovw",
            "method_status": "observed_official",
        },
        {
            "input": "business_demography_raw.csv",
            "output": "business_demography_distribution.csv",
            "source_name": "Eurostat Business Demography",
            "dataset_id": "bd_9bd_sz_cl_r2",
            "method_status": "distribution_only",
        },
        {
            "input": "oecd_sdbs_inventory.csv",
            "output": "oecd_sdbs_inventory.csv",
            "source_name": "OECD Structural and Demographic Business Statistics",
            "dataset_id": "DSD_SDBSBSC_ISIC4",
            "method_status": "observed_official",
        },
        {
            "input": "istat_sources_inventory.csv",
            "output": "istat_sources_inventory.csv",
            "source_name": "ISTAT",
            "dataset_id": "istat_inventory",
            "method_status": "experimental",
        },
    ]

    for job in jobs:
        raw_path = build_path_from_settings(settings, "raw", job["input"])
        processed_path = build_path_from_settings(settings, "processed", job["output"])

        raw_df = read_dataframe_if_exists(raw_path)
        clean_df = prepara_dataset_generico(
            raw_df,
            source_name=job["source_name"],
            dataset_id=job["dataset_id"],
            method_status=job["method_status"],
        )
        write_dataframe_csv(clean_df, processed_path)
        print(f"Creato {processed_path.name}. Righe: {len(clean_df)}")


if __name__ == "__main__":
    main()
