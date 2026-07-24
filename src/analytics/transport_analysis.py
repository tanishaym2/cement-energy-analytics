"""
Transport Analytics

Analyzes transportation distances and transport modes
for each cement plant.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def detect_transport_mode(text):

    if pd.isna(text):
        return "Unknown"

    text = str(text).lower()

    has_truck = "truck" in text
    has_train = "train" in text

    if has_truck and has_train:
        return "Truck + Train"
    elif has_train:
        return "Train"
    elif has_truck:
        return "Truck"

    return "Unknown"


def main():

    conn = sqlite3.connect(DB_PATH)

    transport = pd.read_sql(
        "SELECT * FROM transport",
        conn
    )

    conn.close()

    # ---------------------------------
    # Detect Transport Mode
    # ---------------------------------

    transport["transport_mode"] = transport[
        "raw_transport"
    ].apply(detect_transport_mode)

    # ---------------------------------
    # Plant Summary
    # ---------------------------------

    summary = (
        transport.groupby("plant")
        .agg(
            avg_distance=("distance_km", "mean"),
            max_distance=("distance_km", "max"),
            min_distance=("distance_km", "min"),
            transport_records=("material", "count"),
        )
        .reset_index()
    )

    # ---------------------------------
    # Mode Counts
    # ---------------------------------

    modes = (
        transport.groupby(
            ["plant", "transport_mode"]
        )
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    final = summary.merge(
        modes,
        on="plant",
        how="left"
    )

    final = final.round(2)

    final.to_csv(
        EXPORT_DIR / "transport_analysis.csv",
        index=False
    )

    print("\nTransport Analysis\n")
    print(final)

    print("\nSaved:")
    print(EXPORT_DIR / "transport_analysis.csv")


if __name__ == "__main__":
    main()