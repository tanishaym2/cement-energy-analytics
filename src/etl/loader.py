"""
loader.py

Loads the cement plant Excel workbook.
"""

from pathlib import Path
import pandas as pd

from config import WORKBOOK_PATH


class WorkbookLoader:
    """Loads all sheets from the workbook."""

    def __init__(self, workbook_path: Path = WORKBOOK_PATH):
        self.workbook_path = workbook_path

        # Open workbook once
        self.excel = pd.ExcelFile(self.workbook_path)

        # Remove accidental leading/trailing spaces
        self.sheet_lookup = {
            sheet.strip(): sheet
            for sheet in self.excel.sheet_names
        }

    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Load a sheet by its cleaned name."""

        if sheet_name not in self.sheet_lookup:
            raise ValueError(
                f"Sheet '{sheet_name}' not found.\n"
                f"Available: {list(self.sheet_lookup.keys())}"
            )

        actual_name = self.sheet_lookup[sheet_name]

        return pd.read_excel(
            self.workbook_path,
            sheet_name=actual_name,
            header=None
        )

    def load_all(self) -> dict[str, pd.DataFrame]:
        """Load all three sheets."""

        return {
            "A": self.load_sheet("A. Inventory Data of Cement"),
            "B": self.load_sheet("B. Electricity Data and Impacts"),
            "C": self.load_sheet("C. Impact Assessment Results"),
        }


if __name__ == "__main__":

    loader = WorkbookLoader()

    sheets = loader.load_all()

    print(f"\nWorkbook Loaded:")
    print(loader.workbook_path)

    for name, df in sheets.items():
        print("\n" + "=" * 60)
        print(f"Sheet {name}")
        print("=" * 60)
        print("Shape:", df.shape)
        print(df.head())