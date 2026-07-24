"""
Normalize clinker inventory tables into one structured dataset.
"""

import re
import pandas as pd

from src.config import INTERIM_DIR, PROCESSED_DIR


CASE_PLANTS = {
    1: "Nandyal",
    2: "Nimbahera",
    3: "Mangrol",
    4: "Nimbol",
}

TABLE_CASE = {
    "A1": 1,
    "A6": 2,
    "A11": 3,
    "A16": 4,
}


def split_quantity(text):
    """
    Split quantity strings like:
    '1420 kg' -> (1420, 'kg')
    """

    if pd.isna(text):
        return None, None

    text = str(text).strip()

    match = re.match(r"([\d.]+)\s*(.*)", text)

    if match:
        return float(match.group(1)), match.group(2).strip()

    return None, None


def normalize_table(table_name):

    df = pd.read_csv(
        INTERIM_DIR / "sheet_a" / f"{table_name}.csv"
    )

    plant = CASE_PLANTS[TABLE_CASE[table_name]]
    case = TABLE_CASE[table_name]

    rows = []

    current_category = None

    for _, row in df.iterrows():

        material = row["1"]
        amount = row["2"]
        transport = row["3"]

        if pd.isna(material):
            continue

        material = str(material).strip()

        # --------------------------------------------------
        # Skip table titles and metadata
        # --------------------------------------------------

        if (
            material.startswith("Table")
            or material.startswith("Input data")
            or material.startswith("Case Study")
            or material.startswith("Characterization")
            or material.startswith("Inventory")
        ):
            continue

        # Skip header rows
        if material in [
            "Material",
            "Amount",
            "Source of materials (distance from plant and mode of transportation)",
            "Source",
        ]:
            continue

        # --------------------------------------------------
        # Detect section/category
        # --------------------------------------------------

        if material in [
            "Raw materials",
            "Fuels",
            "Electricity",
            "Transportation",
            "Services",
        ]:
            current_category = material
            continue

        value, unit = split_quantity(amount)

        # Ignore rows before any category begins
        if current_category is None:
            continue

        rows.append(
            {
                "plant": plant,
                "case_study": case,
                "category": current_category,
                "material": material,
                "value": value,
                "unit": unit,
                "transport": transport,
            }
        )

    return pd.DataFrame(rows)


def main():

    inventory = pd.concat(
        [
            normalize_table("A1"),
            normalize_table("A6"),
            normalize_table("A11"),
            normalize_table("A16"),
        ],
        ignore_index=True,
    )

    # Remove completely empty rows
    inventory = inventory.dropna(
        subset=["material"],
        how="all",
    )

    # Remove duplicate rows
    inventory = inventory.drop_duplicates()

    inventory.to_csv(
        PROCESSED_DIR / "inventory.csv",
        index=False,
    )

    print("\nInventory Preview\n")
    print(inventory.head(15))

    print("\nShape:", inventory.shape)

    print("\nCategories:")
    print(inventory["category"].value_counts())

    print("\nSaved to:")
    print(PROCESSED_DIR / "inventory.csv")


if __name__ == "__main__":
    main()