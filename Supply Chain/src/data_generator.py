import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "inventory_demand_raw.csv"


def generate_inventory_demand_data(
    n_products: int = 50,
    n_warehouses: int = 5,
    start_date: str = "2022-01-01",
    end_date: str = "2024-12-31",
    seed: int = 42,
    output_path: Path | str | None = None,
) -> pd.DataFrame:
    np.random.seed(seed)
    output_path = Path(output_path) if output_path else OUTPUT_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    product_ids = [f"P{i:04d}" for i in range(n_products)]
    warehouse_ids = [f"WH{i:02d}" for i in range(n_warehouses)]

    rows = []
    for date in dates:
        for product_id in product_ids:
            for warehouse_id in warehouse_ids:
                month = date.month
                seasonality_index = 0.8 + 0.4 * np.sin(2 * np.pi * (month - 1) / 12) + np.random.uniform(-0.1, 0.1)
                seasonality_index = max(0.5, min(1.5, seasonality_index))

                promotion_flag = 1 if np.random.random() < 0.15 else 0
                base_price = np.random.uniform(10, 200)
                price = base_price * (0.9 if promotion_flag else 1.0)

                lead_time = int(np.random.choice([3, 5, 7, 10, 14], p=[0.2, 0.3, 0.25, 0.15, 0.1]))
                supplier_delay = int(np.random.exponential(2))

                base_demand = np.random.poisson(30) * seasonality_index * (1.2 if promotion_flag else 1.0)
                sales_quantity = max(0, int(base_demand + np.random.normal(0, 5)))

                reorder_point = int(np.random.uniform(20, 100))
                inv_level = max(0, int(np.random.uniform(0, 150) - sales_quantity * 0.3))
                stockout_flag = 1 if inv_level <= 0 or inv_level < reorder_point * 0.5 else 0

                rows.append({
                    "product_id": product_id,
                    "warehouse_id": warehouse_id,
                    "date": date.strftime("%Y-%m-%d"),
                    "sales_quantity": sales_quantity,
                    "inventory_level": inv_level,
                    "reorder_point": reorder_point,
                    "lead_time": lead_time,
                    "promotion_flag": promotion_flag,
                    "seasonality_index": round(seasonality_index, 4),
                    "price": round(price, 2),
                    "supplier_delay": supplier_delay,
                    "stockout_flag": stockout_flag,
                })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df = generate_inventory_demand_data()
    print(f"Generated {len(df):,} rows -> {OUTPUT_PATH}")
