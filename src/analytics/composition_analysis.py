"""
Composition Analytics

Summarizes material composition for each cement product.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    conn = sqlite3.connect(DB_PATH)

    composition = pd.read_sql(
        "SELECT * FROM composition",
        conn
    )

    conn.close()

    # ---------------------------------
    # Product Summary
    # ---------------------------------

    summary = (
        composition.groupby("product")
        .agg(
            total_materials=("material", "count"),
            unique_materials=("material", "nunique"),
            total_quantity=("value", "sum"),
        )
        .reset_index()
    )

    # ---------------------------------
    # Material Breakdown
    # ---------------------------------

    breakdown = (
        composition.groupby(
            ["product", "material"]
        )["value"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    final = summary.merge(
        breakdown,
        on="product",
        how="left"
    )

    final = final.round(2)

    final.to_csv(
        EXPORT_DIR / "composition_analysis.csv",
        index=False
    )

    print("\nComposition Analysis\n")
    print(final)

    print("\nSaved:")
    print(EXPORT_DIR / "composition_analysis.csv")


if __name__ == "__main__":
    main()