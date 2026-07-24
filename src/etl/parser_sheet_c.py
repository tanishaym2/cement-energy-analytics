"""
Parse all tables from Sheet C into individual CSV files.
"""

import pandas as pd

from src.etl.loader import WorkbookLoader
from src.config import INTERIM_DIR

def main():

    registry = pd.read_csv(
        INTERIM_DIR / "table_registry.csv"
    )

    loader = WorkbookLoader()

    sheets = loader.load_all()

    sheet = sheets["C"]

    output_dir = INTERIM_DIR / "sheet_c"
    output_dir.mkdir(parents=True, exist_ok=True)

    registry = registry[
        registry["sheet"] == "C"
    ].reset_index(drop=True)

    for _, row in registry.iterrows():

        table = row["table_id"]

        start = int(row["start_row"])
        end = int(row["end_row"])

        table_df = sheet.iloc[start:end + 1]

        table_df.to_csv(
            output_dir / f"{table}.csv",
            index=False,
        )

        print(f"Saved {table}")


if __name__ == "__main__":
    main()