import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

"""utils.py

Gemeinsame Hilfsfunktionen für die Wetter‑ETL‑Pipeline.

Enthält aktuell:
* ``dwd_table``   – kombiniert Roh‑DataFrames (Temp, Regen, Sonne)
* ``custom_round`` – kaufmännisches Runden via ``decimal``
"""

def dwd_table(df: pd.DataFrame) -> pd.DataFrame:
     """Führt Temperatur‑, Niederschlags‑ und Sonnenschein‑Rohdaten zusammen."""
     result = pd.merge(left = df["df_raw"][0], right= df["df_raw"][1], how = "inner", on = ["Jahr", "Monat"]).merge(df["df_raw"][2], how = "right", on = ["Jahr", "Monat"])
     return result 

def custom_round(value, precision):
    """Rundet *value* kaufmännisch (``ROUND_HALF_UP``)."""
    
    if precision == 0:

        result = Decimal(value).quantize(Decimal(), rounding = ROUND_HALF_UP)
        return result

    precision = 1 / (10**precision)

    result = Decimal(value).quantize(Decimal(str(precision)), rounding = ROUND_HALF_UP)

    return result

