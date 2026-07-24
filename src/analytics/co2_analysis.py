"""
CO₂ Analytics

Extracts CO₂ emission results from Sheet C
(C2, C7, C12, C16).
"""

from pathlib import Path
import pandas as pd

INTERIM_DIR = Path("data/interim/sheet_c")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

TABLES = {
    "C2": "Nandyal",
    "C7": "Nimbahera",
    "C12": "Mangrol",
    "C16": "Nimbol",
}

rows = []

for table, plant in TABLES.items():

    df = pd.read_csv(INTERIM_DIR / f"{table}.csv")

    for _, row in df.iterrows():

        item = row.iloc[1]

        if pd.isna(item):
            continue

        item = str(item).strip()

        # Skip titles and headers
        if (
            item.startswith("Table")
            or item == "Input"
            or item == "Raw materials"
            or item == "Fuels"
            or item == "Electricity"
            or item == "Transportation"
            or item == "Other upstream default processes"
        ):
            continue

        try:
            ground = float(row.iloc[2])
        except:
            ground = None

        try:
            gate = float(row.iloc[3])
        except:
            gate = None

        try:
            csi = float(row.iloc[4])
        except:
            csi = None

        rows.append({
            "plant": plant,
            "source": item,
            "ground_to_gate_CO2": ground,
            "gate_to_gate_CO2": gate,
            "CSI_CO2": csi
        })

co2 = pd.DataFrame(rows)

co2.to_csv(
    EXPORT_DIR / "co2_analysis.csv",
    index=False
)

print("\nCO₂ Analysis\n")
print(co2.head(20))

print("\nRows:", len(co2))

print("\nSaved:")
print(EXPORT_DIR / "co2_analysis.csv")