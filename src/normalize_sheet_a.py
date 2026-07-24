"""
Inspect all extracted Sheet A tables before normalization.
"""

from pathlib import Path
import pandas as pd

from config import INTERIM_DIR


def main():

    folder = INTERIM_DIR / "sheet_a"

    for csv_file in sorted(folder.glob("A*.csv")):

        df = pd.read_csv(csv_file)

        print("\n" + "=" * 80)
        print(csv_file.stem)
        print("=" * 80)

        print(df.head(10))

        print("\nColumns:")
        print(df.columns.tolist())


if __name__ == "__main__":
    main()