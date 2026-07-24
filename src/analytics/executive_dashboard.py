"""
Executive Dashboard Generator

Combines all analytics into one dashboard dataset.
"""

from pathlib import Path
import pandas as pd

EXPORT_DIR = Path("data/exports")


def load(name):
    return pd.read_csv(EXPORT_DIR / name)


def main():

    plant = load("plant_performance.csv")
    transport = load("transport_analysis.csv")
    benchmark = load("plant_benchmark.csv")

    dashboard = (
        plant.merge(
            transport,
            on="plant",
            how="left",
            suffixes=("", "_transport")
        )
        .merge(
            benchmark,
            on="plant",
            how="left"
        )
    )

    dashboard.to_csv(
        EXPORT_DIR / "executive_dashboard.csv",
        index=False
    )

    print("\nExecutive Dashboard\n")
    print(dashboard)

    print("\nSaved:")
    print(EXPORT_DIR / "executive_dashboard.csv")


if __name__ == "__main__":
    main()