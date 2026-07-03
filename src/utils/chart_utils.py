"""Utility per i grafici.

Le funzioni operative verranno estese nei notebook. Questo file resta separato
per rispettare la regola di usare funzioni riutilizzabili in src/utils.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.io_utils import write_dataframe_csv


def salva_dati_grafico(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Salva i dati alla base di un grafico in CSV.

    I notebook possono usare questi CSV per ricostruire i grafici e controllare
    la coerenza tra tabella e visualizzazione.
    """
    return write_dataframe_csv(df, output_path)
