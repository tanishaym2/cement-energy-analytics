"""
Detect all logical tables from the workbook.
"""

import re
import pandas as pd

from loader import WorkbookLoader
from config import INTERIM_DIR

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

    registry_df = pd.DataFrame(registry)

    print(registry_df)

    registry_df.to_csv(
        INTERIM_DIR / "table_registry.csv",
        index=False
    )

    print("\nRegistry saved successfully.")


if __name__ == "__main__":
    build_registry()
    
