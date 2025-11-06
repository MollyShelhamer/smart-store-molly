"""
prepare_customers_data.py

Clean customer_data.csv located under data/raw and save the cleaned
version into data/prepared/customers_prepared.csv.
"""

import pathlib
import sys
import pandas as pd

# ---------------------------------------------------------
# Add project root to sys.path (your src folder is one level
# above analytics_project)
# ---------------------------------------------------------
CURRENT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent  # goes from:
# data_prep → analytics_project → src → project root
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

# ---------------------------------------------------------
# Import project logger
# ---------------------------------------------------------
from analytics_project.utils_logger import logger

# ---------------------------------------------------------
# Define folder paths
# ---------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PREPARED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Read CSV safely
# ---------------------------------------------------------
def read_raw_data(filename: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / filename
    logger.info(f"Reading raw data from {file_path}")

    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------
# Save the cleaned CSV
# ---------------------------------------------------------
def save_prepared_data(df: pd.DataFrame, filename: str):
    output_path = PREPARED_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned data to {output_path}")


# ---------------------------------------------------------
# Clean column names
# ---------------------------------------------------------
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    original = df.columns.tolist()
    df.columns = [col.strip() for col in df.columns]
    changed = [f"{o} → {n}" for o, n in zip(original, df.columns) if o != n]

    if changed:
        logger.info("Column names standardized: " + ", ".join(changed))

    return df


# ---------------------------------------------------------
# Remove duplicates (based on CustomerID)
# ---------------------------------------------------------
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    if "CustomerID" not in df.columns:
        logger.warning("CustomerID not found — duplicate removal skipped.")
        return df

    before = len(df)
    df = df.drop_duplicates(subset=["CustomerID"], keep="first")
    after = len(df)

    logger.info(f"Removed {before - after} duplicate rows.")
    return df


# ---------------------------------------------------------
# Handle missing values
# ---------------------------------------------------------
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows missing CustomerID
    if "CustomerID" in df.columns:
        before = len(df)
        df = df.dropna(subset=["CustomerID"])
        after = len(df)
        logger.info(f"Dropped {before - after} rows with missing CustomerID.")

    # Fill basic text fields
    for text_col in ["Name", "Region", "LoyaltyTier"]:
        if text_col in df.columns:
            missing = df[text_col].isna().sum()
            if missing > 0:
                df[text_col] = df[text_col].fillna("Unknown")
                logger.info(f"Filled {missing} missing values in {text_col}.")

    # RewardPoints numeric cleaning
    if "RewardPoints" in df.columns:
        df["RewardPoints"] = df["RewardPoints"].astype(str).str.replace(",", "", regex=False)
        df["RewardPoints"] = pd.to_numeric(df["RewardPoints"], errors="coerce")
        missing = df["RewardPoints"].isna().sum()

        if missing:
            df["RewardPoints"] = df["RewardPoints"].fillna(0)
            logger.info(f"Replaced {missing} invalid RewardPoints values with 0.")

    return df


# ---------------------------------------------------------
# Standardize Region + LoyaltyTier
# ---------------------------------------------------------
def standardize_categories(df: pd.DataFrame) -> pd.DataFrame:
    # REGION standardization
    if "Region" in df.columns:
        df["Region"] = df["Region"].astype(str).str.strip().str.title()
        df["Region"] = df["Region"].replace(
            {
                "East": "East",
                "West": "West",
                "North": "North",
                "South": "South",
                "South-West": "South-West",
                "South-Western": "South-West",
                "Southwest": "South-West",
                "South West": "South-West",
            }
        )

    # TIER standardization
    if "LoyaltyTier" in df.columns:
        df["LoyaltyTier"] = df["LoyaltyTier"].astype(str).str.strip().str.title()
        valid = {"Bronze", "Silver", "Gold", "Unknown"}
        df["LoyaltyTier"] = df["LoyaltyTier"].where(df["LoyaltyTier"].isin(valid), "Unknown")

    return df


# ---------------------------------------------------------
# Convert JoinDate → datetime
# ---------------------------------------------------------
def convert_join_date(df: pd.DataFrame) -> pd.DataFrame:
    if "JoinDate" in df.columns:
        df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors="ignore", infer_datetime_format=True)
    return df


# ---------------------------------------------------------
# Remove outliers using IQR method
# ---------------------------------------------------------
def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    if "RewardPoints" not in df.columns:
        return df

    q1 = df["RewardPoints"].quantile(0.25)
    q3 = df["RewardPoints"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    before = len(df)
    df = df[(df["RewardPoints"] >= lower) & (df["RewardPoints"] <= upper)]
    after = len(df)

    logger.info(f"Removed {before - after} RewardPoints outliers.")
    return df


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------
def main():
    logger.info("======= START prepare_customers_data.py =======")

    df = read_raw_data("customers_data.csv")
    if df.empty:
        logger.error("No data loaded — exiting.")
        return

    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = standardize_categories(df)
    df = convert_join_date(df)
    df = remove_outliers(df)

    save_prepared_data(df, "customers_prepared.csv")

    logger.info("======= FINISHED prepare_customers_data.py =======")


if __name__ == "__main__":
    main()
