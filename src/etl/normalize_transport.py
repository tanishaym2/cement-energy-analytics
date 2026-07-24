"""
Extract transportation information from inventory tables.
"""

import re
import pandas as pd

from config import INTERIM_DIR, PROCESSED_DIR

TABLES = {
    "A1": ("Nandyal", 1),
    "A6": ("Nimbahera", 2),
    "A11": ("Mangrol", 3),
    "A16": ("Nimbol", 4),
}

rows = []

for table, (plant, case) in TABLES.items():

    df = pd.read_csv(INTERIM_DIR / "sheet_a" / f"{table}.csv")

    for _, row in df.iterrows():

        material = row["1"]
        transport = row["3"]

        if pd.isna(material) or pd.isna(transport):
            continue

        material = str(material).strip()
        transport = str(transport).strip()

        if (
            material.startswith("Table")
            or material.startswith("Input")
            or material in ["Material", "Raw materials", "Fuels"]
        ):
            continue

        # First distance found
        match = re.search(r"(\d+)\s*km", transport)
        distance = int(match.group(1)) if match else None

        mode = []

        if "truck" in transport.lower():
            mode.append("Truck")

        if "train" in transport.lower():
            mode.append("Train")

        if "ship" in transport.lower():
            mode.append("Ship")

        source = transport.split("(")[0].strip()

        rows.append(
            {
                "plant": plant,
                "case_study": case,
                "material": material,
                "source": source,
                "distance_km": distance,
                "mode": " + ".join(mode),
                "raw_transport": transport,
            }
        )

transport = pd.DataFrame(rows)

transport.to_csv(
    PROCESSED_DIR / "transport.csv",
    index=False,
)

print(transport.head())

print("\nRows:", len(transport))