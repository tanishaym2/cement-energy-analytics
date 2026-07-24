"""
Calculate plant-level KPIs from the normalized SQLite database.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/cement.db")
OUTPUT_PATH = Path("data/processed/plants_summary.csv")


def load_table(conn, table):
    return pd.read_sql(f"SELECT * FROM {table}", conn)


def main():

    conn = sqlite3.connect(DB_PATH)

    inventory = load_table(conn, "inventory")
    transport = load_table(conn, "transport")
    composition = load_table(conn, "composition")

    conn.close()

    # -----------------------------
    # Inventory Summary
    # -----------------------------

    inventory_summary = (
        inventory.groupby(["plant", "category"], dropna=False)["value"]
        .sum()
        .reset_index()
    )

    inventory_pivot = (
        inventory_summary.pivot(
            index="plant",
            columns="category",
            values="value"
        )
        .fillna(0)
        .reset_index()
    )

    # -----------------------------
    # Transport Summary
    # -----------------------------

    transport_summary = (
        transport.groupby("plant")["distance_km"]
        .mean()
        .reset_index()
        .rename(columns={
            "distance_km": "avg_transport_distance_km"
        })
    )

    # -----------------------------
    # Product Counts
    # -----------------------------

    product_summary = (
        composition.groupby("product")
        .size()
        .reset_index(name="records")
    )

    print("\nInventory Summary")
    print(inventory_pivot)

    print("\nTransport Summary")
    print(transport_summary)

    print("\nProducts")
    print(product_summary)

    final = inventory_pivot.merge(
        transport_summary,
        on="plant",
        how="left"
    )

    final.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nSaved:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()