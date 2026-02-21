import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import DATA_RAW, DATA_PROCESSED, DATA_OUTPUT, RAW_DATA_FILE


def main():
    from src.data_generator import generate_inventory_demand_data, OUTPUT_PATH
    from src.data_pipeline import run_cleaning
    from src.feature_engineering import run_feature_engineering
    from src.forecast import run_forecast_product_level
    from src.reorder_risk import run_reorder_and_risk

    raw_path = DATA_RAW / RAW_DATA_FILE
    if not raw_path.exists():
        print("Generating synthetic inventory & demand data...")
        generate_inventory_demand_data(
            n_products=30,
            n_warehouses=3,
            start_date="2022-01-01",
            end_date="2024-06-30",
            output_path=raw_path,
        )
    else:
        print("Using existing raw data:", raw_path)

    print("Cleaning and preprocessing...")
    run_cleaning()

    print("Building features...")
    run_feature_engineering()

    print("Running demand forecast (ARIMA + Prophet)...")
    forecast_df, metrics = run_forecast_product_level()
    print("Model comparison:", metrics)

    print("Computing reorder recommendations and stock-out risk...")
    run_reorder_and_risk()

    print("\nPipeline complete. Outputs in:", DATA_OUTPUT)


if __name__ == "__main__":
    main()
