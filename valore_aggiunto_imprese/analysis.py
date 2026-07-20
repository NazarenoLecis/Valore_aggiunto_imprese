"""Utility leggere usate dai notebook di analisi."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from valore_aggiunto_imprese.config import (
    BUSINESS_DEMOGRAPHY_SIZE_CLASSES,
    COUNTRIES,
    EUROSTAT_OFFICIAL_SIZE_CLASSES,
    SECTORS,
)
from valore_aggiunto_imprese.utils import get_project_root

COUNTRY_LABELS = {row["code"]: row["label_it"] for row in COUNTRIES}
SECTOR_LABELS = {row["eurostat_nace"]: row["label_it"] for row in SECTORS if row["eurostat_nace"]}
OFFICIAL_SIZE_LABELS = {
    row["original"]: row["harmonised"] for row in EUROSTAT_OFFICIAL_SIZE_CLASSES
}
BUSINESS_SIZE_LABELS = {
    row["original"]: row["harmonised"] for row in BUSINESS_DEMOGRAPHY_SIZE_CLASSES
}

SIZE_ORDER_OFFICIAL = ["0-9", "10-19", "20-49", "50-249", "250+"]
SIZE_ORDER_BUSINESS = ["0 dip.", "1-4 dip.", "5-9 dip."]

METRIC_LABELS = {
    "AV_MEUR": "Valore aggiunto (mln euro)",
    "ENT_NR": "Imprese",
    "EMP_NR": "Persone occupate",
    "SAL_NR": "Dipendenti",
    "LABPRY_TEUR": "Produttivita apparente (migliaia euro)",
    "V11910": "Imprese attive",
    "V16910": "Persone occupate",
    "V16911": "Dipendenti",
}


def read_project_csv(relative_path: str | Path) -> pd.DataFrame:
    path = get_project_root() / relative_path
    if not path.exists():
        raise FileNotFoundError(
            f"File non trovato: {path}. Eseguire prima python -m valore_aggiunto_imprese.pipeline"
        )
    return pd.read_csv(path)


def enrich_sbs(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    if "country_code" not in output.columns and "geo" in output.columns:
        output["country_code"] = output["geo"]
    if "sector_code_original" not in output.columns and "nace_r2" in output.columns:
        output["sector_code_original"] = output["nace_r2"]
    if "size_class_original" not in output.columns and "size_emp" in output.columns:
        output["size_class_original"] = output["size_emp"]
    if "metric_code" not in output.columns and "indic_sbs" in output.columns:
        output["metric_code"] = output["indic_sbs"]
    if "year" not in output.columns and "time" in output.columns:
        output["year"] = output["time"]

    output["country_label"] = (
        output["country_code"].map(COUNTRY_LABELS).fillna(output["country_code"])
    )
    output["sector_label"] = (
        output["sector_code_original"].map(SECTOR_LABELS).fillna(output["sector_code_original"])
    )
    output["size_label"] = (
        output["size_class_original"]
        .map(OFFICIAL_SIZE_LABELS)
        .fillna(output["size_class_original"])
    )
    output["metric_label_readable"] = (
        output["metric_code"].map(METRIC_LABELS).fillna(output["metric_code"])
    )
    output["year"] = pd.to_numeric(output["year"], errors="coerce").astype("Int64")
    output["value"] = pd.to_numeric(output["value"], errors="coerce")
    return output


def enrich_business_demography(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    if "country_code" not in output.columns and "geo" in output.columns:
        output["country_code"] = output["geo"]
    if "sector_code_original" not in output.columns and "nace_r2" in output.columns:
        output["sector_code_original"] = output["nace_r2"]
    if "size_class_original" not in output.columns and "sizeclas" in output.columns:
        output["size_class_original"] = output["sizeclas"]
    if "metric_code" not in output.columns and "indic_sb" in output.columns:
        output["metric_code"] = output["indic_sb"]
    if "year" not in output.columns and "time" in output.columns:
        output["year"] = output["time"]

    output["country_label"] = (
        output["country_code"].map(COUNTRY_LABELS).fillna(output["country_code"])
    )
    output["sector_label"] = (
        output["sector_code_original"].map(SECTOR_LABELS).fillna(output["sector_code_original"])
    )
    output["size_label"] = (
        output["size_class_original"]
        .map(BUSINESS_SIZE_LABELS)
        .fillna(output["size_class_original"])
    )
    output["metric_label_readable"] = (
        output["metric_code"].map(METRIC_LABELS).fillna(output["metric_code"])
    )
    output["year"] = pd.to_numeric(output["year"], errors="coerce").astype("Int64")
    output["value"] = pd.to_numeric(output["value"], errors="coerce")
    return output


def add_share(
    df: pd.DataFrame,
    group_columns: list[str],
    value_column: str = "value",
) -> pd.DataFrame:
    output = df.copy()
    denominator = output.groupby(group_columns, observed=True)[value_column].transform("sum")
    output["share"] = output[value_column] / denominator
    output["share_pct"] = output["share"] * 100
    return output


def add_source_note(fig, fonte: str):
    """Aggiunge fonte ed elaborazione in basso a sinistra a un grafico Plotly."""
    fig.add_annotation(
        text=f"Fonte: {fonte}. Elaborazione di Nazareno Lecis.",
        xref="paper",
        yref="paper",
        x=0,
        y=-0.18,
        xanchor="left",
        yanchor="top",
        showarrow=False,
        align="left",
        font={"size": 11, "color": "#4b5563"},
    )
    fig.update_layout(margin={"b": 90}, plot_bgcolor="white", paper_bgcolor="white")
    return fig


def latest_year_with_values(
    df: pd.DataFrame,
    metric_code: str | None = None,
    filters: dict[str, object] | None = None,
) -> int:
    output = df.copy()
    if metric_code is not None:
        output = output[output["metric_code"] == metric_code]
    for column, value in (filters or {}).items():
        output = output[output[column] == value]
    output = output.dropna(subset=["value"])
    years = pd.to_numeric(output["year"], errors="coerce").dropna()
    if years.empty:
        raise ValueError("Nessun anno con valori disponibili per la selezione richiesta.")
    return int(years.max())


def latest_common_year_with_values(
    df: pd.DataFrame,
    metric_codes: list[str],
    filters: dict[str, object] | None = None,
) -> int:
    common_years: set[int] | None = None
    for metric_code in metric_codes:
        output = df[df["metric_code"] == metric_code].copy()
        for column, value in (filters or {}).items():
            output = output[output[column] == value]
        output = output.dropna(subset=["value"])
        years = set(pd.to_numeric(output["year"], errors="coerce").dropna().astype(int))
        common_years = years if common_years is None else common_years & years
    if not common_years:
        raise ValueError("Nessun anno comune con valori disponibili per le metriche richieste.")
    return max(common_years)
