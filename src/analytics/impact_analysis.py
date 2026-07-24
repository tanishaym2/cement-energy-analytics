"""
Impact Assessment Analytics

Extracts impact assessment results from
C3, C8, C13 and C17.
"""

from pathlib import Path
import pandas as pd

INTERIM_DIR = Path("data/interim/sheet_c")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

TABLES = {
    "C3": ("Nandyal", "OPC"),
    "C8": ("Nimbahera", "OPC"),
    "C13": ("Mangrol", "OPC"),
    "C17": ("Nimbol", "OPC"),
}

rows = []

for table, (plant, product) in TABLES.items():

    df = pd.read_csv(INTERIM_DIR / f"{table}.csv")

    for _, row in df.iterrows():

        component = row.iloc[1]

        if pd.isna(component):
            continue

        component = str(component).strip()

        if (
            component.startswith("Table")
            or component == "Total"
        ):
            continue

        try:
            ground_co2 = float(row.iloc[2])
        except:
            ground_co2 = None

        try:
            ground_energy = float(row.iloc[3])
        except:
            ground_energy = None

        try:
            gate_co2 = float(row.iloc[4])
        except:
            gate_co2 = None

        try:
            gate_energy = float(row.iloc[5])
        except:
            gate_energy = None

        rows.append({
            "plant": plant,
            "product": product,
            "component": component,
            "ground_co2": ground_co2,
            "ground_energy": ground_energy,
            "gate_co2": gate_co2,
            "gate_energy": gate_energy
        })

impact = pd.DataFrame(rows)

impact.to_csv(
    EXPORT_DIR / "impact_analysis.csv",
    index=False
)

print(impact.head())

print("\nRows:", len(impact))