"""Configurazione del progetto.

Le variabili operative sono definite in codice Python per mantenere il progetto
semplice e leggibile. Gli script importano queste variabili e le passano alle
funzioni di download, trasformazione, validazione ed export.

Il progetto non usa file YAML, non usa argparse e non usa classi.
"""

from __future__ import annotations

PROJECT_SETTINGS = {
    "project_name": "valore_aggiunto_imprese",
    "language": "it",
    "start_year": 2008,
    "end_year": "latest",
    "paths": {
        "raw": "data/raw",
        "intermediate": "data/intermediate",
        "processed": "data/processed",
        "processed_csv": "data/processed_csv",
        "processed_json": "data/processed_json",
        "validation": "data/validation",
        "charts": "outputs/charts",
    },
    "default_countries": ["IT", "FR", "DE", "ES", "NL", "BE", "AT", "SE", "DK", "FI"],
    "metrics": [
        "value_added",
        "enterprises",
        "persons_employed",
        "employees",
        "apparent_labour_productivity",
    ],
    "output_formats": ["csv", "json"],
}

SOURCES = {
    "eurostat_sbs": {
        "source_name": "Eurostat Structural Business Statistics",
        "dataset_id": "sbs_sc_ovw",
        "base_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data",
        "note": "Fonte principale per valore aggiunto, imprese e occupazione per classe dimensionale.",
        "method_status": "observed_official",
    },
    "eurostat_business_demography": {
        "source_name": "Eurostat Business Demography",
        "dataset_id": "bd_9bd_sz_cl_r2",
        "base_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data",
        "note": "Fonte da verificare per distribuzioni granulari di imprese e occupati.",
        "method_status": "distribution_only",
    },
    "oecd_sdbs": {
        "source_name": "OECD Structural and Demographic Business Statistics",
        "dataset_id": "DSD_SDBSBSC_ISIC4",
        "base_url": "https://sdmx.oecd.org/public/rest/v1/data",
        "note": "Fonte OCSE da verificare in fase di implementazione.",
        "method_status": "observed_official",
    },
    "istat": {
        "source_name": "ISTAT",
        "note": "Modulo di inventario e verifica fonti italiane granulari.",
        "candidate_sources": [
            "Frame SBS",
            "Frame Territoriale",
            "Frame Territoriale Anticipato",
            "Conti economici delle imprese",
            "Microdati struttura e performance imprese",
        ],
    },
}

COUNTRIES = [
    {"code": "IT", "iso3": "ITA", "label_it": "Italia"},
    {"code": "FR", "iso3": "FRA", "label_it": "Francia"},
    {"code": "DE", "iso3": "DEU", "label_it": "Germania"},
    {"code": "ES", "iso3": "ESP", "label_it": "Spagna"},
    {"code": "NL", "iso3": "NLD", "label_it": "Paesi Bassi"},
    {"code": "BE", "iso3": "BEL", "label_it": "Belgio"},
    {"code": "AT", "iso3": "AUT", "label_it": "Austria"},
    {"code": "SE", "iso3": "SWE", "label_it": "Svezia"},
    {"code": "DK", "iso3": "DNK", "label_it": "Danimarca"},
    {"code": "FI", "iso3": "FIN", "label_it": "Finlandia"},
    {"code": "IE", "iso3": "IRL", "label_it": "Irlanda"},
    {"code": "PT", "iso3": "PRT", "label_it": "Portogallo"},
    {"code": "EL", "iso3": "GRC", "label_it": "Grecia"},
    {"code": "PL", "iso3": "POL", "label_it": "Polonia"},
]

EUROSTAT_OFFICIAL_SIZE_CLASSES = [
    {"original": "0-9", "harmonised": "0-9", "label_it": "0-9 occupati", "method_status": "observed_official"},
    {"original": "10-19", "harmonised": "10-19", "label_it": "10-19 occupati", "method_status": "observed_official"},
    {"original": "20-49", "harmonised": "20-49", "label_it": "20-49 occupati", "method_status": "observed_official"},
    {"original": "50-249", "harmonised": "50-249", "label_it": "50-249 occupati", "method_status": "observed_official"},
    {"original": "250+", "harmonised": "250+", "label_it": "250 o più occupati", "method_status": "observed_official"},
]

BUSINESS_DEMOGRAPHY_SIZE_CLASSES = [
    {"original": "0", "harmonised": "0", "label_it": "0 occupati", "method_status": "distribution_only"},
    {"original": "1-4", "harmonised": "1-4", "label_it": "1-4 occupati", "method_status": "distribution_only"},
    {"original": "5-9", "harmonised": "5-9", "label_it": "5-9 occupati", "method_status": "distribution_only"},
    {"original": "10+", "harmonised": "10+", "label_it": "10 o più occupati", "method_status": "distribution_only"},
]

EXPERIMENTAL_FINE_SIZE_CLASSES = [
    "0",
    "1",
    "2-4",
    "5-9",
    "10-14",
    "15-19",
    "20-49",
    "50-99",
    "100-249",
    "250-499",
    "500+",
]

SECTORS = [
    {"sector_code_harmonised": "business_economy", "label_it": "Business economy", "eurostat_nace": "B-S_X_K", "oecd_isic": None},
    {"sector_code_harmonised": "industry", "label_it": "Industria", "eurostat_nace": "B-E", "oecd_isic": "B-E"},
    {"sector_code_harmonised": "manufacturing", "label_it": "Manifattura", "eurostat_nace": "C", "oecd_isic": "C"},
    {"sector_code_harmonised": "construction", "label_it": "Costruzioni", "eurostat_nace": "F", "oecd_isic": "F"},
    {"sector_code_harmonised": "trade", "label_it": "Commercio", "eurostat_nace": "G", "oecd_isic": "G"},
    {"sector_code_harmonised": "transport", "label_it": "Trasporti", "eurostat_nace": "H", "oecd_isic": "H"},
    {"sector_code_harmonised": "accommodation_food", "label_it": "Alloggio e ristorazione", "eurostat_nace": "I", "oecd_isic": "I"},
    {"sector_code_harmonised": "information_communication", "label_it": "Informazione e comunicazione", "eurostat_nace": "J", "oecd_isic": "J"},
    {"sector_code_harmonised": "professional_services", "label_it": "Attività professionali, scientifiche e tecniche", "eurostat_nace": "M", "oecd_isic": "M"},
    {"sector_code_harmonised": "administrative_services", "label_it": "Servizi amministrativi e di supporto", "eurostat_nace": "N", "oecd_isic": "N"},
]
