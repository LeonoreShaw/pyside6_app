"""ZIP/CSV data processing for standard deviation calculation."""

import zipfile
import io
import pandas as pd
from typing import List, Tuple, Optional


# Column index mapping (1-based user-facing index to column name)
COLUMN_MAP = {
    1: "value_a",
    2: "value_b",
    3: "value_c",
}


def get_column_name(col_index: int) -> str:
    """Get the column name for a given 1-based index."""
    return COLUMN_MAP.get(col_index, "value_a")


def list_csv_files(zip_path: str) -> List[str]:
    """List all .csv files in a ZIP archive."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            return [name for name in zf.namelist()
                    if name.lower().endswith('.csv') and not name.startswith('__MACOSX')]
    except (zipfile.BadZipFile, FileNotFoundError, PermissionError) as e:
        raise RuntimeError(f"Cannot open ZIP file: {e}")


def process_single_csv(
    zip_path: str,
    csv_filename: str,
    col_index: int = 1
) -> Tuple[str, Optional[float], Optional[str]]:
    """
    Process a single CSV file from a ZIP archive.

    Returns:
        (filename, std_value, error_message)
        If successful, error_message is None.
        If failed, std_value is None and error_message describes the issue.
    """
    col_name = get_column_name(col_index)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            with zf.open(csv_filename) as f:
                raw_bytes = f.read()

        # Try reading with different encodings
        df = None
        for encoding in ['utf-8', 'gbk', 'latin-1']:
            try:
                df = pd.read_csv(io.BytesIO(raw_bytes), encoding=encoding)
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue

        if df is None:
            return (csv_filename, None, "Failed to decode CSV file")

        # Check if the target column exists
        if col_name not in df.columns:
            # Try by positional index as fallback
            if col_index < len(df.columns):
                col_name = df.columns[col_index]
            else:
                available = ", ".join(df.columns.tolist())
                return (csv_filename, None, f"Column '{col_name}' not found. Available: {available}")

        # Get the column data and compute std
        series = pd.to_numeric(df[col_name], errors='coerce')
        non_null_count = series.notna().sum()

        if non_null_count == 0:
            return (csv_filename, None, f"No numeric data in column '{col_name}'")

        std_val = float(series.std())
        return (csv_filename, std_val, None)

    except zipfile.BadZipFile:
        return (csv_filename, None, "Corrupt ZIP entry")
    except pd.errors.EmptyDataError:
        return (csv_filename, None, "CSV file is empty")
    except Exception as e:
        return (csv_filename, None, str(e))
