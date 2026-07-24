"""
Extract every Sheet A table into CSV.
"""

import pandas as pd

from loader import WorkbookLoader
from parser_utils import extract_table, save_table
from config import INTERIM_DIR


def main():

    loader = WorkbookLoader()

    sheets = loader.load_all()

    sheet_a = sheets["A"]

    registry = pd.read_csv(
        INTERIM_DIR / "table_registry.csv"
    )

    registry = registry[
        registry["sheet"] == "A"
    ].copy()

    registry = registry.sort_values(
        "start_row"
    ).reset_index(drop=True)

    for i, row in registry.iterrows():

        start = row["start_row"]

        if i == len(registry) - 1:
            end = len(sheet_a) - 1
        else:
            end = registry.iloc[i + 1]["start_row"] - 1

        table = extract_table(
            sheet_a,
            int(start),
            int(end),
        )

        save_table(
            table,
            INTERIM_DIR / "sheet_a" / f"{row['table_id']}.csv"
        )

        print(f"Saved {row['table_id']}")


if __name__ == "__main__":
    main()