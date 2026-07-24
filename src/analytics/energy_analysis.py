"""
Energy Analytics

Extracts energy consumption results from Sheet C tables
(C1, C6, C11, C15).
"""

from pathlib import Path
import pandas as pd

INTERIM_DIR = Path("data/interim/sheet_c")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

TABLES = {
    "C1": "Nandyal",
    "C6": "Nimbahera",
    "C11": "Mangrol",
    "C15": "Nimbol",
}

rows = []

for table, plant in TABLES.items():

    df = pd.read_csv(INTERIM_DIR / f"{table}.csv")

    for _, row in df.iterrows():

        category = row.iloc[1]

        if pd.isna(category):
            continue

        category = str(category).strip()

        # Skip titles and headers
        if (
            category.startswith("Table")
            or category == "Categories"
            or category == "Raw materials"
            or category == "Fuels"
            or category == "Electricity"
            or category == "Transportation"
            or category == "Other upstream processes"
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
            "process": category,
            "ground_to_gate_MJ": ground,
            "gate_to_gate_MJ": gate,
            "CSI_MJ": csi
        })

energy = pd.DataFrame(rows)

energy.to_csv(
    EXPORT_DIR / "energy_analysis.csv",
    index=False
)

print("\nEnergy Analysis\n")
print(energy.head(20))

print("\nRows:", len(energy))

print("\nSaved:")
print(EXPORT_DIR / "energy_analysis.csv")