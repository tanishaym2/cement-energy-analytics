"""
Utility functions for extracting logical tables from worksheets.
"""

from pathlib import Path
import pandas as pd


def extract_table(
    sheet_df: pd.DataFrame,
    start_row: int,
    end_row: int,
) -> pd.DataFrame:
    """
    Extract one logical table from a worksheet.

    Parameters
    ----------
    sheet_df : pd.DataFrame
    start_row : int
    end_row : int

    Returns
    -------
    pd.DataFrame
    """

    table = sheet_df.iloc[start_row:end_row + 1].copy()

    table.reset_index(drop=True, inplace=True)

    return table


def save_table(
    table: pd.DataFrame,
    output_path: Path,
):

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    table.to_csv(
        output_path,
        index=False,
    )