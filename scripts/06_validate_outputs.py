# Questo script valida i dataset puliti.
#
# Obiettivo:
# controllare che i file in data/processed abbiano le colonne minime,
# method_status valido e assenza di duplicati sulla chiave logica principale.
#
# Output:
# - data/validation/validation_report.json
# - data/validation/validation_report.md
#
# Uso:
# python scripts/06_validate_outputs.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.dataframe_utils import REQUIRED_OUTPUT_COLUMNS
from src.utils.io_utils import build_path_from_settings, load_yaml, read_dataframe_if_exists, write_json
from src.utils.validation_utils import build_validation_report, validation_report_to_markdown


def main() -> None:
    settings = load_yaml("config/settings.yaml")

    dataset_files = [
        "official_eurostat_sbs.csv",
        "business_demography_distribution.csv",
        "oecd_sdbs_inventory.csv",
        "istat_sources_inventory.csv",
    ]

    key_columns = [
        "country_code",
        "year",
        "source_dataset_id",
        "sector_code_original",
        "size_class_original",
        "metric_code",
    ]

    reports = []

    for filename in dataset_files:
        path = build_path_from_settings(settings, "processed", filename)
        df = read_dataframe_if_exists(path)
        report = build_validation_report(
            df=df,
            dataset_name=filename,
            required_columns=REQUIRED_OUTPUT_COLUMNS,
            key_columns=key_columns,
        )
        reports.append(report)
        print(f"Validato {filename}. Valido: {report['is_valid']}")

    json_path = build_path_from_settings(settings, "validation", "validation_report.json")
    md_path = build_path_from_settings(settings, "validation", "validation_report.md")

    write_json(reports, json_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(validation_report_to_markdown(reports), encoding="utf-8")

    print(f"Report JSON: {json_path}")
    print(f"Report Markdown: {md_path}")


if __name__ == "__main__":
    main()
