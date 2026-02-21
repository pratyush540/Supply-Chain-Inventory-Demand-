import pandas as pd
import numpy as np
from pathlib import Path

try:
    from config import DATA_PROCESSED, DATA_OUTPUT, CLEANED_DATA_FILE, FEATURED_DATA_FILE
except ImportError:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
    DATA_OUTPUT = PROJECT_ROOT / "data" / "output"
    CLEANED_DATA_FILE = "inventory_demand_cleaned.csv"
    FEATURED_DATA_FILE = "inventory_demand_featured.csv"

LAG_DAYS = [1, 7, 14, 28]
ROLLING_WINDOWS = [7, 14, 28]


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["month"] = out["date"].dt.month
    out["day_of_week"] = out["date"].dt.dayofweek
    out["quarter"] = out["date"].dt.quarter
    out["year"] = out["date"].dt.year
    return out


def add_lag_and_rolling(
    df: pd.DataFrame,
    value_col: str = "sales_quantity",
    group_cols: list | None = None,
) -> pd.DataFrame:
    group_cols = group_cols or ["product_id", "warehouse_id"]
    out = df.sort_values(group_cols + ["date"]).copy()

    for lag in LAG_DAYS:
        out[f"{value_col}_lag_{lag}"] = out.groupby(group_cols)[value_col].shift(lag)

    for w in ROLLING_WINDOWS:
        out[f"{value_col}_rolling_mean_{w}"] = (
            out.groupby(group_cols)[value_col].transform(lambda x: x.shift(1).rolling(w, min_periods=1).mean())
        )
        out[f"{value_col}_rolling_std_{w}"] = (
            out.groupby(group_cols)[value_col].transform(lambda x: x.shift(1).rolling(w, min_periods=1).std())
        )
    out = out.bfill().ffill()
    return out


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_date_features(df)
    df = add_lag_and_rolling(df, value_col="sales_quantity", group_cols=["product_id", "warehouse_id"])
    return df


def run_feature_engineering(
    input_path: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    input_path = input_path or (DATA_PROCESSED / CLEANED_DATA_FILE)
    if not input_path.exists():
        raise FileNotFoundError(f"Cleaned data not found: {input_path}. Run data_pipeline.py first.")
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    featured = build_features(df)
    output_path = output_path or (DATA_OUTPUT / FEATURED_DATA_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(output_path, index=False)
    return featured


if __name__ == "__main__":
    run_feature_engineering()
    print("Featured data saved to", DATA_OUTPUT / FEATURED_DATA_FILE)
