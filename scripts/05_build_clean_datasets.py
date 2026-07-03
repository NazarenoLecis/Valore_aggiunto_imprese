# Costruisce dataset puliti a partire dai file raw.
# Variabili operative in src/project_config.py.

from __future__ import annotations

from src.project_config import PROJECT_SETTINGS
from src.transform.build_clean_datasets import prepara_dataset_generico
from src.utils.io_utils import build_path_from_settings, read_dataframe_if_exists, write_dataframe_csv


JOBS = [
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


def main() -> None:
    for job in JOBS:
        raw_path = build_path_from_settings(PROJECT_SETTINGS, "raw", job["input"])
        processed_path = build_path_from_settings(PROJECT_SETTINGS, "processed", job["output"])
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
