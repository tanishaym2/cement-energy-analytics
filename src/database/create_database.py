"""
Create SQLite database from normalized datasets.
"""

import sqlite3
import pandas as pd

from pathlib import Path
import sys
from pathlib import Path

# Add src folder to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import PROCESSED_DIR

DB_PATH = Path("data/cement.db")


def load_table(conn, csv_name, table_name):

    csv_path = PROCESSED_DIR / csv_name

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {table_name}: {len(df)} rows")


def main():

    conn = sqlite3.connect(DB_PATH)

    load_table(conn, "inventory.csv", "inventory")
    load_table(conn, "composition.csv", "composition")
    load_table(conn, "transport.csv", "transport")
    load_table(conn, "emission_factors.csv", "emission_factors")

    conn.commit()

    conn.close()

    print("\nSQLite database created successfully.")
    print(DB_PATH)


if __name__ == "__main__":
    main()