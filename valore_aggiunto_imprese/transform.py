"""Funzioni per costruire dataset puliti.

Questa prima versione standardizza le colonne minime e mantiene i codici
originali delle fonti. I mapping dettagliati per indicatori, settori e classi
vanno raffinati dopo l'esplorazione dei dataset nei notebook.
"""

from __future__ import annotations

import pandas as pd

from valore_aggiunto_imprese.utils import normalizza_nomi_colonne, ordina_colonne_output


def prepara_dataset_generico(
    df: pd.DataFrame,
    source_name: str,
    dataset_id: str,
    method_status: str,
) -> pd.DataFrame:
    """Prepara un dataset nello schema standard del progetto."""
    if df.empty:
        return ordina_colonne_output(pd.DataFrame())

    output = normalizza_nomi_colonne(df)

    output["source_name"] = output.get("source_name", source_name)
    output["source_dataset_id"] = output.get("source_dataset_id", dataset_id)
    output["method_status"] = output.get("method_status", method_status)

    # Mapping iniziale conservativo. Le fonti hanno nomi diversi per paese,
    # settore, classe dimensionale e indicatore. Qui copiamo i codici originali
    # quando esistono e lasciamo vuoti i campi armonizzati da completare.
    output["country_code"] = output.get("geo")
    output["country_name"] = output.get("geo_label")
    output["year"] = output.get("time")
    output["sector_code_original"] = output.get("nace_r2", output.get("isic4"))
    output["sector_label_original"] = output.get("nace_r2_label", output["sector_code_original"])
    output["sector_code_harmonised"] = output["sector_code_original"]
    output["sector_label_harmonised"] = output["sector_label_original"]
    output["sector_level"] = None
    output["size_class_original"] = output.get("size_emp", output.get("sizeclas"))
    output["size_class_harmonised"] = output["size_class_original"]
    output["metric_code"] = output.get(
        "indic_sbs",
        output.get("indic_sb", output.get("na_item", output.get("measure"))),
    )
    output["metric_label"] = output.get(
        "indic_sbs_label",
        output.get("indic_sb_label", output.get("na_item_label", output["metric_code"])),
    )
    if dataset_id == "nama_10r_3gva":
        output["metric_code"] = "B1G"
        output["metric_label"] = "Value added, gross"
    output["unit"] = output.get("unit")
    output["source_url"] = None
    output["notes"] = None

    return ordina_colonne_output(output)
