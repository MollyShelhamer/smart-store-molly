from data_scrubber import DataScrubber
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PREPARED_DIR = DATA_DIR / "prepared"

PREPARED_DIR.mkdir(parents=True, exist_ok=True)


def clean_with_scrubber(df: pd.DataFrame) -> pd.DataFrame:
    """Clean any DataFrame using DataScrubber with a universal-safe pipeline."""

    scrubber = DataScrubber(df)

    df = scrubber.remove_duplicate_records()
    df = scrubber.handle_missing_data(fill_value="UNKNOWN")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Clean object/string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df = scrubber.format_column_strings_to_upper_and_trim(col)

    return df


def clean_file(filename: str):
    input_path = RAW_DIR / filename
    output_path = PREPARED_DIR / filename.replace(".csv", "_prepared.csv")

    if not input_path.exists():
        print(f"⚠️ File not found: {input_path}")
        return

    print(f"📄 Processing: {filename}")

    df = pd.read_csv(input_path)
    cleaned = clean_with_scrubber(df)
    cleaned.to_csv(output_path, index=False)

    print(f"✅ Saved cleaned file to: {output_path}")


# Run all files
clean_file("customers_data.csv")
clean_file("products_data.csv")
clean_file("sales_data.csv")

print("🎉 All files cleaned successfully!")
