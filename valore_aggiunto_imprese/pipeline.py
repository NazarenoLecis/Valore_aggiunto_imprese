from __future__ import annotations

from typing import Any

from valore_aggiunto_imprese.config import PROJECT_SETTINGS, SOURCES
from valore_aggiunto_imprese.export import esporta_dataset_csv_json
from valore_aggiunto_imprese.sources import (
    crea_inventario_fonti_istat,
    crea_inventario_oecd_sdbs,
    scarica_business_demography,
    scarica_eurostat_sbs,
)
from valore_aggiunto_imprese.transform import prepara_dataset_generico
from valore_aggiunto_imprese.utils import (
    REQUIRED_OUTPUT_COLUMNS,
    build_path_from_settings,
    build_validation_report,
    get_project_root,
    read_dataframe_if_exists,
    validation_report_to_markdown,
    write_dataframe_csv,
    write_dataframe_json,
    write_json,
)

CLEAN_DATASET_JOBS = [
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

VALIDATION_KEYS = [
    "country_code",
    "year",
    "source_dataset_id",
    "sector_code_original",
    "size_class_original",
    "metric_code",
]

VALIDATION_FILES = [
    {"filename": "official_eurostat_sbs.csv", "key_columns": VALIDATION_KEYS},
    {"filename": "business_demography_distribution.csv", "key_columns": VALIDATION_KEYS},
    {"filename": "oecd_sdbs_inventory.csv", "key_columns": ["source_dataset_id"]},
    {"filename": "istat_sources_inventory.csv", "key_columns": ["candidate_source"]},
]

EXPORT_DATASETS = {
    "official_eurostat_sbs": "official_eurostat_sbs.csv",
    "business_demography_distribution": "business_demography_distribution.csv",
    "oecd_sdbs_inventory": "oecd_sdbs_inventory.csv",
    "istat_sources_inventory": "istat_sources_inventory.csv",
}


def download_sources(settings: dict[str, Any], sources: dict[str, Any]) -> None:
    eurostat_sbs, eurostat_sbs_metadata = scarica_eurostat_sbs(settings=settings, sources=sources)
    write_dataframe_csv(
        eurostat_sbs,
        build_path_from_settings(settings, "raw", "eurostat_sbs_raw.csv"),
    )
    write_dataframe_json(
        eurostat_sbs,
        build_path_from_settings(settings, "raw", "eurostat_sbs_raw.json"),
    )
    write_json(
        eurostat_sbs_metadata,
        build_path_from_settings(settings, "raw", "eurostat_sbs_metadata.json"),
    )
    print(f"Eurostat SBS scaricato. Righe: {len(eurostat_sbs)}")

    business_demography, business_demography_metadata = scarica_business_demography(
        settings=settings,
        sources=sources,
    )
    write_dataframe_csv(
        business_demography,
        build_path_from_settings(settings, "raw", "business_demography_raw.csv"),
    )
    write_dataframe_json(
        business_demography,
        build_path_from_settings(settings, "raw", "business_demography_raw.json"),
    )
    write_json(
        business_demography_metadata,
        build_path_from_settings(settings, "raw", "business_demography_metadata.json"),
    )
    print(f"Business Demography scaricato. Righe: {len(business_demography)}")

    oecd_inventory, oecd_metadata = crea_inventario_oecd_sdbs(settings=settings, sources=sources)
    write_dataframe_csv(
        oecd_inventory,
        build_path_from_settings(settings, "raw", "oecd_sdbs_inventory.csv"),
    )
    write_dataframe_json(
        oecd_inventory,
        build_path_from_settings(settings, "raw", "oecd_sdbs_inventory.json"),
    )
    write_json(oecd_metadata, build_path_from_settings(settings, "raw", "oecd_sdbs_metadata.json"))
    print(f"Inventario OECD SDBS creato. Righe: {len(oecd_inventory)}")

    istat_inventory, istat_metadata = crea_inventario_fonti_istat(
        settings=settings, sources=sources
    )
    write_dataframe_csv(
        istat_inventory,
        build_path_from_settings(settings, "raw", "istat_sources_inventory.csv"),
    )
    write_dataframe_json(
        istat_inventory,
        build_path_from_settings(settings, "raw", "istat_sources_inventory.json"),
    )
    write_json(istat_metadata, build_path_from_settings(settings, "raw", "istat_metadata.json"))
    print(f"Inventario ISTAT creato. Righe: {len(istat_inventory)}")


def build_clean_datasets(settings: dict[str, Any]) -> None:
    for job in CLEAN_DATASET_JOBS:
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


def validate_outputs(settings: dict[str, Any]) -> None:
    reports = []
    for file_config in VALIDATION_FILES:
        filename = file_config["filename"]
        path = build_path_from_settings(settings, "processed", filename)
        df = read_dataframe_if_exists(path)
        report = build_validation_report(
            df,
            filename,
            REQUIRED_OUTPUT_COLUMNS,
            file_config["key_columns"],
        )
        reports.append(report)
        print(filename, report["is_valid"])

    json_path = build_path_from_settings(settings, "validation", "validation_report.json")
    md_path = build_path_from_settings(settings, "validation", "validation_report.md")
    write_json(reports, json_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(validation_report_to_markdown(reports), encoding="utf-8")


def export_outputs(settings: dict[str, Any]) -> None:
    root = get_project_root()
    csv_dir = root / settings["paths"]["processed_csv"]
    json_dir = root / settings["paths"]["processed_json"]

    for dataset_name, filename in EXPORT_DATASETS.items():
        path = build_path_from_settings(settings, "processed", filename)
        df = read_dataframe_if_exists(path)
        outputs = esporta_dataset_csv_json(df, dataset_name, csv_dir, json_dir)
        print(f"Esportato {dataset_name}: {outputs}")


def main() -> None:
    print("Step 1/4 - Download fonti e inventari")
    download_sources(PROJECT_SETTINGS, SOURCES)

    print("Step 2/4 - Costruzione dataset puliti")
    build_clean_datasets(PROJECT_SETTINGS)

    print("Step 3/4 - Validazione output")
    validate_outputs(PROJECT_SETTINGS)

    print("Step 4/4 - Export CSV e JSON")
    export_outputs(PROJECT_SETTINGS)

    print("Pipeline completata")
    print("Output CSV: data/processed_csv/")
    print("Output JSON: data/processed_json/")
    print("Report validazione: data/validation/")


if __name__ == "__main__":
    main()
