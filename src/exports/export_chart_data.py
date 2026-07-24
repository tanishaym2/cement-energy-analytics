"""
Prepare chart-ready datasets.
"""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

conn = sqlite3.connect(DB_PATH)

inventory = pd.read_sql(
    "SELECT * FROM inventory",
    conn
)

composition = pd.read_sql(
    "SELECT * FROM composition",
    conn
)

conn.close()

# -------------------------
# Materials by Plant
# -------------------------

materials = (
    inventory.groupby(
        ["plant", "category"]
    )["value"]
    .sum()
    .reset_index()
)

materials.to_csv(
    EXPORT_DIR / "materials_by_plant.csv",
    index=False
)

# -------------------------
# Product Composition
# -------------------------

composition_chart = (
    composition.groupby(
        ["product", "material"]
    )["value"]
    .sum()
    .reset_index()
)

composition_chart.to_csv(
    EXPORT_DIR / "composition_chart.csv",
    index=False
)

print("Chart datasets exported.")