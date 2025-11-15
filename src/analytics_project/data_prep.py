from data_scrubber import DataScrubber
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PREPARED_DIR = DATA_DIR / "prepared"

PREPARED_DIR.mkdir(parents=True, exist_ok=True)


def clean_with_scrubber(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean any DataFrame safely:
    - Preserve numeric columns (including IDs)
    - Fill missing string/object columns with "UNKNOWN"
    - Remove duplicates and clean strings
    """
    scrubber = DataScrubber(df)

    # Remove duplicate records
    df = scrubber.remove_duplicate_records()

    # Fill missing string/object columns manually
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("UNKNOWN")  # safe for strings only

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Clean string/object columns with DataScrubber formatting
    for col in df.select_dtypes(include=["object"]).columns:
        df = scrubber.format_column_strings_to_upper_and_trim(col)

    return df


def clean_file(filename: str):
    input_path = RAW_DIR / filename
    output_path = PREPARED_DIR / filename.replace("_data.csv", "_prepared.csv")

    if not input_path.exists():
        print(f" File not found: {input_path}")
        return

    print(f" Processing: {filename}")

    df = pd.read_csv(input_path)
    cleaned = clean_with_scrubber(df)
    cleaned.to_csv(output_path, index=False)

    print(f" Saved cleaned file to: {output_path}")


# List of all CSVs to clean
files_to_clean = ["customers_data.csv", "products_data.csv", "sales_data.csv"]

for file in files_to_clean:
    clean_file(file)

print(" All files cleaned successfully!")
