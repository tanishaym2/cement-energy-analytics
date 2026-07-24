"""
Material Consumption Analytics

Analyzes material usage across all cement plants.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    conn = sqlite3.connect(DB_PATH)

    inventory = pd.read_sql(
        "SELECT * FROM inventory",
        conn
    )

    conn.close()

    # ----------------------------------
    # Total Quantity by Material
    # ----------------------------------

    material_summary = (
        inventory.groupby(["material", "category"])
        .agg(
            total_quantity=("value", "sum"),
            plants_using=("plant", "nunique"),
            records=("material", "count"),
        )
        .reset_index()
    )

    material_summary = material_summary.sort_values(
        by="total_quantity",
        ascending=False
    )

    material_summary = material_summary.round(2)

    material_summary.to_csv(
        EXPORT_DIR / "material_summary.csv",
        index=False
    )

    print("\nMaterial Summary\n")
    print(material_summary)

    print("\nTop 10 Materials\n")
    print(material_summary.head(10))

    print("\nSaved:")
    print(EXPORT_DIR / "material_summary.csv")


if __name__ == "__main__":
    main()