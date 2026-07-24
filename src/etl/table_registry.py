"""
Detect all logical tables from the workbook.
"""

import re
import pandas as pd

from src.etl.loader import WorkbookLoader
from src.config import INTERIM_DIR

TABLE_PATTERN = re.compile(r"Table\s+([ABC]\d+)", re.IGNORECASE)
CASE_PATTERN = re.compile(r"Case\s+Study\s+(\d+)", re.IGNORECASE)


def build_registry():

    loader = WorkbookLoader()
    sheets = loader.load_all()

    registry = []

    for sheet_name, df in sheets.items():

        current_case = None

        for row_number, row in df.iterrows():

            for value in row:

                if pd.isna(value):
                    continue

                text = str(value).strip()

                case = CASE_PATTERN.search(text)
                if case:
                    current_case = int(case.group(1))

                table = TABLE_PATTERN.search(text)

                if table:

                    registry.append({
                        "sheet": sheet_name,
                        "table_id": table.group(1),
                        "case_study": current_case,
                        "start_row": row_number,
                        "title": text
                    })

    # -----------------------------
    # Convert to DataFrame
    # -----------------------------

    registry_df = pd.DataFrame(registry)

    # -----------------------------
    # Calculate end_row
    # -----------------------------

    registry_df = registry_df.sort_values(
        by=["sheet", "start_row"]
    ).reset_index(drop=True)

    end_rows = []

    for sheet in registry_df["sheet"].unique():

        sheet_tables = registry_df[
            registry_df["sheet"] == sheet
        ]

        indices = sheet_tables.index.tolist()

        last_row = len(sheets[sheet]) - 1

        for i, idx in enumerate(indices):

            if i < len(indices) - 1:
                next_start = registry_df.loc[
                    indices[i + 1],
                    "start_row"
                ]
                end_rows.append(next_start - 1)
            else:
                end_rows.append(last_row)

    registry_df["end_row"] = end_rows

    # Reorder columns
    registry_df = registry_df[
        [
            "sheet",
            "table_id",
            "case_study",
            "start_row",
            "end_row",
            "title",
        ]
    ]

    print(registry_df)

    registry_df.to_csv(
        INTERIM_DIR / "table_registry.csv",
        index=False,
    )

    print("\nRegistry saved successfully.")


if __name__ == "__main__":
    build_registry()