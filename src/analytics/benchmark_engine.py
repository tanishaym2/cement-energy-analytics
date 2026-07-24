"""
Industrial Benchmark Engine

Generates plant benchmarking KPIs for the dashboard.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(name):
    return pd.read_csv(EXPORT_DIR / name)


def main():

    energy = load_csv("energy_analysis.csv")
    co2 = load_csv("co2_analysis.csv")

    # -----------------------------
    # Plant Energy
    # -----------------------------

    energy_summary = (
        energy.groupby("plant")
        .agg(
            total_energy=("ground_to_gate_MJ", "sum"),
            avg_energy=("ground_to_gate_MJ", "mean"),
        )
        .reset_index()
    )

    # -----------------------------
    # Plant CO2
    # -----------------------------

    co2_summary = (
        co2.groupby("plant")
        .agg(
            total_co2=("ground_to_gate_CO2", "sum"),
            avg_co2=("ground_to_gate_CO2", "mean"),
        )
        .reset_index()
    )

    benchmark = energy_summary.merge(
        co2_summary,
        on="plant"
    )

    # -----------------------------
    # Ranking
    # -----------------------------

    benchmark["Energy Rank"] = (
        benchmark["total_energy"]
        .rank(method="dense")
        .astype(int)
    )

    benchmark["CO2 Rank"] = (
        benchmark["total_co2"]
        .rank(method="dense")
        .astype(int)
    )

    benchmark["Sustainability Score"] = (
        100
        - (
            benchmark["Energy Rank"]
            + benchmark["CO2 Rank"]
        )
        * 8
    )

    benchmark = benchmark.sort_values(
        "Sustainability Score",
        ascending=False
    )

    benchmark.to_csv(
        EXPORT_DIR / "plant_benchmark.csv",
        index=False,
    )

    print("\nPlant Benchmark\n")
    print(benchmark)


if __name__ == "__main__":
    main()