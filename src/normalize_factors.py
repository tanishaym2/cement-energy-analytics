"""
Normalize characterization factor tables.
"""

import pandas as pd

from config import INTERIM_DIR, PROCESSED_DIR

TABLES = [
    "A5",
    "A10",
    "A15",
    "A19",
    "A22",
    "A23",
    "A26",
]

rows = []

for table in TABLES:

    df = pd.read_csv(
        INTERIM_DIR / "sheet_a" / f"{table}.csv"
    )

    current_category = None

    for _, row in df.iterrows():

        item = row["1"]
        factor = row["2"]
        unit = row["3"]

        if pd.isna(item):
            continue

        item = str(item).strip()

        # Skip titles
        if (
            item.startswith("Table")
            or item.startswith("Characterization")
            or item.startswith("Input")
        ):
            continue

        # Category headers
        if item in [
            "Raw materials",
            "Fuels",
            "Electricity",
            "Transportation",
            "Services",
        ]:
            current_category = item
            continue

        rows.append(
            {
                "table": table,
                "category": current_category,
                "item": item,
                "factor": factor,
                "unit": unit,
            }
        )

factors = pd.DataFrame(rows)

factors.to_csv(
    PROCESSED_DIR / "emission_factors.csv",
    index=False,
)

print(factors.head())

print("\nRows:", len(factors))