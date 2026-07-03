from __future__ import annotations

from src.project_config import PROJECT_SETTINGS
from src.utils.dataframe_utils import REQUIRED_OUTPUT_COLUMNS
from src.utils.io_utils import build_path_from_settings, read_dataframe_if_exists, write_json
from src.utils.validation_utils import build_validation_report, validation_report_to_markdown

FILES = [
    "official_eurostat_sbs.csv",
    "business_demography_distribution.csv",
    "oecd_sdbs_inventory.csv",
    "istat_sources_inventory.csv",
]

KEYS = ["country_code", "year", "source_dataset_id", "sector_code_original", "size_class_original", "metric_code"]


def main() -> None:
    reports = []
    for filename in FILES:
        path = build_path_from_settings(PROJECT_SETTINGS, "processed", filename)
        df = read_dataframe_if_exists(path)
        report = build_validation_report(df, filename, REQUIRED_OUTPUT_COLUMNS, KEYS)
        reports.append(report)
        print(filename, report["is_valid"])

    json_path = build_path_from_settings(PROJECT_SETTINGS, "validation", "validation_report.json")
    md_path = build_path_from_settings(PROJECT_SETTINGS, "validation", "validation_report.md")
    write_json(reports, json_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(validation_report_to_markdown(reports), encoding="utf-8")


if __name__ == "__main__":
    main()
