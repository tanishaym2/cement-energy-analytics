"""
Normalize cement composition tables.
"""

import re
import pandas as pd

from config import INTERIM_DIR, PROCESSED_DIR


TABLES = [
    "A2","A3","A4",
    "A8","A9",
    "A13","A14",
    "A17","A18",
    "A20","A21",
    "A24","A25"
]


def detect_product(table):

    if table in ["A2","A8","A13","A17","A20"]:
        return "OPC"

    if table in ["A9","A14","A18","A21"]:
        return "PPC"

    if table in ["A4","A25"]:
        return "PSC"

    if table in ["A3","A24"]:
        return "GGBS"

    return "Unknown"


rows = []

for table in TABLES:

    df = pd.read_csv(
        INTERIM_DIR / "sheet_a" / f"{table}.csv"
    )

    product = detect_product(table)

    for _, row in df.iterrows():

        material = row["1"]
        amount = row["2"]

        if pd.isna(material):
            continue

        material = str(material).strip()

        if material.startswith("Table"):
            continue

        if material.startswith("Input"):
            continue

        if material in ["Material","Amount"]:
            continue

        value = None
        unit = None

        if isinstance(amount,str):

            m = re.match(r"([\d.]+)\s*(.*)",amount)

            if m:

                value=float(m.group(1))
                unit=m.group(2)

        rows.append({

            "table":table,
            "product":product,
            "material":material,
            "value":value,
            "unit":unit

        })

composition=pd.DataFrame(rows)

composition.to_csv(

    PROCESSED_DIR/"composition.csv",

    index=False

)

print(composition.head())

print()

print(composition.shape)