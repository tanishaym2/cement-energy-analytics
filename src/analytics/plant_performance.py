"""
Plant Performance Analytics

Generates summary metrics for each cement plant.
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

    transport = pd.read_sql(
        "SELECT * FROM transport",
        conn
    )

    conn.close()

    # -----------------------------
    # Inventory Metrics
    # -----------------------------

    inventory_summary = (
        inventory.groupby("plant")
        .agg(
            total_material_quantity=("value", "sum"),
            material_count=("material", "count"),
            unique_materials=("material", "nunique"),
        )
        .reset_index()
    )

    # -----------------------------
    # Category Counts
    # -----------------------------

    category_counts = (
        inventory.groupby(["plant", "category"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # -----------------------------
    # Transport Metrics
    # -----------------------------

    transport_summary = (
        transport.groupby("plant")
        .agg(
            avg_transport_distance=("distance_km", "mean"),
            max_transport_distance=("distance_km", "max"),
            transport_records=("material", "count"),
        )
        .reset_index()
    )

    # -----------------------------
    # Merge Everything
    # -----------------------------

    performance = (
        inventory_summary
        .merge(category_counts, on="plant", how="left")
        .merge(transport_summary, on="plant", how="left")
    )

    performance = performance.round(2)

    performance.to_csv(
        EXPORT_DIR / "plant_performance.csv",
        index=False
    )

    print("\nPlant Performance\n")
    print(performance)

    print("\nSaved:")
    print(EXPORT_DIR / "plant_performance.csv")


if __name__ == "__main__":
    main()