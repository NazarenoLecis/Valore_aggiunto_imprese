from __future__ import annotations

import runpy
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SCRIPTS = [
    "01_download_eurostat_sbs.py",
    "02_download_business_demography.py",
    "03_download_oecd_sdbs.py",
    "04_download_istat_sources.py",
    "05_build_clean_datasets.py",
    "06_validate_outputs.py",
    "07_export_csv_json.py",
]


def main() -> None:
    for script_name in SCRIPTS:
        script_path = PROJECT_ROOT / "scripts" / script_name
        print(f"Esecuzione: {script_name}")
        runpy.run_path(str(script_path), run_name="__main__")

    print("Pipeline completata")
    print("Output CSV: data/processed_csv/")
    print("Output JSON: data/processed_json/")
    print("Report validazione: data/validation/")


if __name__ == "__main__":
    main()
