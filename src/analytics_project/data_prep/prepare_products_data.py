"""
scripts/data_preparation/prepare_products_data.py

This script reads product data from the data/raw folder, cleans the data,
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove invalid ratings
- Remove outliers
- Validate data
- Standardize formatting
"""

#####################################
# Imports
#####################################

import pathlib
import sys
import pandas as pd

#####################################
# Resolve Project Root
#####################################

CURRENT_DIR = pathlib.Path(__file__).resolve().parent

# Locate the project root (folder containing /src)
for parent in CURRENT_DIR.parents:
    if (parent / "src").exists():
        PROJECT_ROOT = parent
        break
else:
    raise RuntimeError("Could not locate project root containing /src folder")

SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

# Local logger
from analytics_project.utils_logger import logger

#####################################
# Paths
#####################################

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"

RAW_DATA_DIR.mkdir(exist_ok=True, parents=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True, parents=True)

#####################################
# Functions
#####################################


def read_raw_data(file_name: str) -> pd.DataFrame:
    logger.info(f"FUNCTION START: read_raw_data with {file_name}")
    file_path = RAW_DATA_DIR / file_name
    logger.info(f"Reading data from {file_path}")

    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    logger.info(f"Saving prepared data with shape {df.shape}")
    file_path = PREPARED_DATA_DIR / file_name
    df.to_csv(file_path, index=False)
    logger.info(f"Saved cleaned data to {file_path}")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("FUNCTION START: remove_duplicates")

    initial = len(df)
    subset = ["productid"] if "productid" in df.columns else None

    df = df.drop_duplicates(subset=subset, keep="first")
    removed = initial - len(df)

    logger.info(f"Removed {removed} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("FUNCTION START: handle_missing_values")
    logger.info(f"Missing before:\n{df.isna().sum()}")

    # Drop rows missing ProductID
    if "productid" in df.columns:
        before = len(df)
        df = df.dropna(subset=["productid"])
        logger.info(f"Dropped {before - len(df)} rows missing ProductID")

    # Fill text columns
    text_cols = ["productname", "category", "seasonal"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Convert UnitPrice to numeric
    if "unitprice" in df.columns:
        df["unitprice"] = df["unitprice"].astype(str).str.replace(",", "", regex=False)
        df["unitprice"] = pd.to_numeric(df["unitprice"], errors="coerce")
        df["unitprice"] = df["unitprice"].fillna(0)

    logger.info(f"Missing after:\n{df.isna().sum()}")
    return df


def remove_invalid_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows where rating is not between 1 and 5 (removes zeros).
    """
    logger.info("FUNCTION START: remove_invalid_ratings")

    if "rating" in df.columns:
        before = len(df)
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df = df[df["rating"].between(1, 5)]
        removed = before - len(df)
        logger.info(f"Removed {removed} rows with invalid ratings")

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("FUNCTION START: remove_outliers")

    initial = len(df)

    if "unitprice" in df.columns:
        q1 = df["unitprice"].quantile(0.25)
        q3 = df["unitprice"].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        logger.info(f"UnitPrice IQR bounds: {lower} to {upper}")

        df = df[(df["unitprice"] >= lower) & (df["unitprice"] <= upper)]

    removed = initial - len(df)
    logger.info(f"Removed {removed} outlier rows")
    return df


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("FUNCTION START: standardize_formats")

    if "category" in df.columns:
        df["category"] = df["category"].astype(str).str.strip().str.title()

    if "seasonal" in df.columns:
        df["seasonal"] = df["seasonal"].astype(str).str.strip().str.upper()
        df["seasonal"] = df["seasonal"].where(df["seasonal"].isin(["Y", "N"]), "N")

    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("FUNCTION START: validate_data")

    if "unitprice" in df.columns:
        before = len(df)
        df = df[df["unitprice"] >= 0]
        logger.info(f"Removed {before - len(df)} rows with negative prices")

    return df


#####################################
# Main
#####################################


def main() -> None:
    logger.info("====================================")
    logger.info("STARTING prepare_products_data.py")
    logger.info("====================================")

    input_file = "products_data.csv"
    output_file = "products_prepared.csv"

    df = read_raw_data(input_file)
    original_shape = df.shape

    # Standardize column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    changed = [f"{o} -> {n}" for o, n in zip(original_columns, df.columns) if o != n]

    if changed:
        logger.info(f"Renamed columns: {changed}")

    # Apply cleaning steps
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = remove_invalid_ratings(df)
    df = remove_outliers(df)
    df = validate_data(df)
    df = standardize_formats(df)

    save_prepared_data(df, output_file)

    logger.info("====================================")
    logger.info(f"Original rows: {original_shape}")
    logger.info(f"Cleaned rows:  {df.shape}")
    logger.info("FINISHED prepare_products_data.py")
    logger.info("====================================")


if __name__ == "__main__":
    main()
