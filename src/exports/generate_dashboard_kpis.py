"""
Generate dashboard KPI cards from SQLite.
"""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/cement.db")
EXPORT_DIR = Path("data/exports")

EXPORT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

inventory = pd.read_sql("SELECT * FROM inventory", conn)
composition = pd.read_sql("SELECT * FROM composition", conn)
transport = pd.read_sql("SELECT * FROM transport", conn)
factors = pd.read_sql("SELECT * FROM emission_factors", conn)

conn.close()

kpis = pd.DataFrame([
    {
        "metric": "Plants",
        "value": inventory["plant"].nunique()
    },
    {
        "metric": "Products",
        "value": composition["product"].nunique()
    },
    {
        "metric": "Materials",
        "value": inventory["material"].nunique()
    },
    {
        "metric": "Transport Records",
        "value": len(transport)
    },
    {
        "metric": "Emission Factors",
        "value": len(factors)
    },
    {
        "metric": "Average Transport Distance (km)",
        "value": round(
            transport["distance_km"].mean(),
            2
        )
    }
])

kpis.to_csv(
    EXPORT_DIR / "dashboard_kpis.csv",
    index=False
)

print(kpis)

print("\nSaved dashboard_kpis.csv")