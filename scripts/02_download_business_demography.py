# Questo script scarica Eurostat Business Demography.
#
# Obiettivo:
# creare una copia raw della fonte usata per descrivere la distribuzione
# più granulare delle imprese e degli occupati.
#
# Nota metodologica:
# questa fonte non misura direttamente il valore aggiunto nelle classi fini.
# Va usata come fonte di distribuzione, non come misura diretta del valore aggiunto.
#
# Uso:
# python scripts/02_download_business_demography.py

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sources.eurostat_business_demography import scarica_business_demography
from src.utils.io_utils import build_path_from_settings, load_yaml, write_dataframe_csv, write_dataframe_json, write_json


def main() -> None:
    settings = load_yaml("config/settings.yaml")
    sources = load_yaml("config/sources.yaml")

    df, metadata = scarica_business_demography(settings=settings, sources=sources)

    write_dataframe_csv(df, build_path_from_settings(settings, "raw", "business_demography_raw.csv"))
    write_dataframe_json(df, build_path_from_settings(settings, "raw", "business_demography_raw.json"))
    write_json(metadata, build_path_from_settings(settings, "raw", "business_demography_metadata.json"))

    print(f"Business Demography scaricato. Righe: {len(df)}")


if __name__ == "__main__":
    main()
