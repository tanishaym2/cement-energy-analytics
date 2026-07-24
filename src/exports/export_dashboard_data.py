"""
Export dashboard-ready datasets from SQLite.
"""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    conn = sqlite3.connect(DB_PATH)

    # -----------------------------
    # Plants Summary
    # -----------------------------
    inventory = pd.read_sql("SELECT * FROM inventory", conn)

    plants = (
        inventory.groupby("plant")
        .agg(
            total_materials=("value", "sum"),
            unique_materials=("material", "count"),
        )
        .reset_index()
    )

    plants.to_csv(
        EXPORT_DIR / "plants_summary.csv",
        index=False,
    )

    # -----------------------------
    # Composition Summary
    # -----------------------------
    composition = pd.read_sql(
        "SELECT * FROM composition",
        conn,
    )

    composition_summary = (
        composition.groupby("product")
        .agg(
            materials=("material", "count"),
            total_quantity=("value", "sum"),
        )
        .reset_index()
    )

    composition_summary.to_csv(
        EXPORT_DIR / "composition_summary.csv",
        index=False,
    )

    # -----------------------------
    # Transport Summary
    # -----------------------------
    transport = pd.read_sql(
        "SELECT * FROM transport",
        conn,
    )

    transport_summary = (
        transport.groupby("plant")
        .agg(
            avg_distance=("distance_km", "mean"),
            max_distance=("distance_km", "max"),
            transport_records=("material", "count"),
        )
        .reset_index()
    )

    transport_summary.to_csv(
        EXPORT_DIR / "transport_summary.csv",
        index=False,
    )

    conn.close()

    print("\nExports Generated Successfully!\n")
    print(plants)
    print()
    print(composition_summary)
    print()
    print(transport_summary)


if __name__ == "__main__":
    main()