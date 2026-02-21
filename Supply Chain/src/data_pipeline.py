import pandas as pd
import numpy as np
from pathlib import Path

try:
    from config import DATA_RAW, DATA_PROCESSED, RAW_DATA_FILE, CLEANED_DATA_FILE
except ImportError:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_RAW = PROJECT_ROOT / "data" / "raw"
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
    RAW_DATA_FILE = "inventory_demand_raw.csv"
    CLEANED_DATA_FILE = "inventory_demand_cleaned.csv"

REQUIRED_COLUMNS = [
    "product_id", "warehouse_id", "date", "sales_quantity", "inventory_level",
    "reorder_point", "lead_time", "promotion_flag", "seasonality_index",
    "price", "supplier_delay", "stockout_flag",
]


def load_raw_data(path: Path | None = None) -> pd.DataFrame:
    path = path or (DATA_RAW / RAW_DATA_FILE)
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found: {path}. Run src/data_generator.py first.")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    out = df.copy()
    out = out.drop_duplicates(subset=["product_id", "warehouse_id", "date"], keep="first")

    numeric = ["sales_quantity", "inventory_level", "reorder_point", "lead_time",
               "seasonality_index", "price", "supplier_delay"]
    for col in numeric:
        if col in out.columns and out[col].isna().any():
            out[col] = out.groupby(["product_id", "warehouse_id"])[col].transform(
                lambda x: x.fillna(x.median())
            )
            out[col] = out[col].fillna(out[col].median())

    out["sales_quantity"] = out["sales_quantity"].clip(lower=0)
    out["inventory_level"] = out["inventory_level"].clip(lower=0)
    out["reorder_point"] = out["reorder_point"].clip(lower=0)
    out["lead_time"] = out["lead_time"].clip(lower=1)
    out["supplier_delay"] = out["supplier_delay"].clip(lower=0)
    out["seasonality_index"] = out["seasonality_index"].clip(lower=0.1, upper=3.0)
    out["price"] = out["price"].clip(lower=0.01)

    out["promotion_flag"] = (out["promotion_flag"].fillna(0).astype(int).clip(0, 1))
    out["stockout_flag"] = (out["stockout_flag"].fillna(0).astype(int).clip(0, 1))

    out = out.sort_values(["product_id", "warehouse_id", "date"]).reset_index(drop=True)
    return out


def run_cleaning(input_path: Path | None = None, output_path: Path | None = None) -> pd.DataFrame:
    df = load_raw_data(input_path)
    cleaned = clean_data(df)
    output_path = output_path or (DATA_PROCESSED / CLEANED_DATA_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    return cleaned


if __name__ == "__main__":
    run_cleaning()
    print("Cleaned data saved to", DATA_PROCESSED / CLEANED_DATA_FILE)
