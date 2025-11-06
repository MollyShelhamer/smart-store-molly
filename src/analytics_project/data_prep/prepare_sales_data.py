"""
scripts/data_preparation/prepare_sales_data.py

Cleans raw sales data:
- Remove duplicates
- Handle missing values
- Remove invalid dates
- Remove invalid amounts
- Remove outliers
- Standardize formatting
"""

#####################################
# IMPORTS
#####################################

import pathlib
import sys
import pandas as pd

#####################################
# PROJECT ROOT RESOLUTION
#####################################

CURRENT_DIR = pathlib.Path(__file__).resolve().parent

# Find the project root by locating folder that contains /src
for parent in CURRENT_DIR.parents:
    if (parent / "src").exists():
        PROJECT_ROOT = parent
        break
else:
    raise RuntimeError("Could not find project root containing /src folder")

SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

# Local logger
from analytics_project.utils_logger import logger

#####################################
# PATHS
#####################################

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"

RAW_DATA_DIR.mkdir(exist_ok=True, parents=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True, parents=True)

#####################################
# FUNCTIONS
#####################################


def read_raw_data(file_name: str) -> pd.DataFrame:
    logger.info(f"Reading raw data: {file_name}")
    path = RAW_DATA_DIR / file_name
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    path = PREPARED_DATA_DIR / file_name
    df.to_csv(path, index=False)
    logger.info(f"Saved cleaned data to {path}")


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    original_cols = df.columns.tolist()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    changed = [f"{o} -> {n}" for o, n in zip(original_cols, df.columns) if o != n]
    if changed:
        logger.info(f"Renamed columns: {changed}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    initial = len(df)
    df = df.drop_duplicates(subset=["transactionid"], keep="first")
    logger.info(f"Removed {initial - len(df)} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Handling missing values")

    # Drop rows missing TransactionID or CustomerID
    before = len(df)
    df = df.dropna(subset=["transactionid", "customerid", "productid"])
    logger.info(f"Dropped {before - len(df)} rows missing critical IDs")

    # Fix StoreCreditCard
    if "storecreditcard" in df.columns:
        df["storecreditcard"] = df["storecreditcard"].astype(str).str.upper()
        df["storecreditcard"] = df["storecreditcard"].where(
            df["storecreditcard"].isin(["Y", "N"]), "N"
        )

    return df


def remove_invalid_dates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Removing invalid dates")

    before = len(df)

    # Convert dates
    df["saledate"] = pd.to_datetime(df["saledate"], errors="coerce")

    df = df.dropna(subset=["saledate"])

    logger.info(f"Removed {before - len(df)} rows with invalid dates")
    return df


def remove_invalid_amounts(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Removing invalid amounts")

    # Convert SaleAmount, invalid = NaN
    df["saleamount"] = pd.to_numeric(df["saleamount"], errors="coerce")

    before = len(df)

    # Remove NaN, Zero, Negative
    df = df[df["saleamount"] > 0]

    logger.info(f"Removed {before - len(df)} rows with invalid SaleAmount")
    return df


def remove_invalid_items(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Removing rows with invalid ItemsPurchased")

    before = len(df)

    df["itemspurchased"] = pd.to_numeric(df["itemspurchased"], errors="coerce")
    df = df[df["itemspurchased"] > 0]

    logger.info(f"Removed {before - len(df)} invalid item count rows")
    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Removing outliers using IQR")

    initial = len(df)

    if "saleamount" in df.columns:
        q1 = df["saleamount"].quantile(0.25)
        q3 = df["saleamount"].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        logger.info(f"Outlier bounds for SaleAmount: {lower} to {upper}")

        df = df[(df["saleamount"] >= lower) & (df["saleamount"] <= upper)]

    logger.info(f"Removed {initial - len(df)} outlier rows")
    return df


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Standardizing formats")

    if "storeid" in df.columns:
        df["storeid"] = df["storeid"].astype(int)

    if "campaignid" in df.columns:
        df["campaignid"] = pd.to_numeric(df["campaignid"], errors="coerce").fillna(0)

    return df


#####################################
# MAIN
#####################################


def main() -> None:
    logger.info("====================================")
    logger.info(" STARTING prepare_sales_data.py")
    logger.info("====================================")

    INPUT = "sales_data.csv"
    OUTPUT = "sales_prepared.csv"

    df = read_raw_data(INPUT)
    original_shape = df.shape

    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = remove_invalid_dates(df)
    df = remove_invalid_amounts(df)
    df = remove_invalid_items(df)
    df = remove_outliers(df)
    df = standardize_formats(df)

    save_prepared_data(df, OUTPUT)

    logger.info("====================================")
    logger.info(f"Original shape: {original_shape}")
    logger.info(f"Cleaned shape:  {df.shape}")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("====================================")


if __name__ == "__main__":
    main()
