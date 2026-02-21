import pandas as pd
import numpy as np
from pathlib import Path

try:
    from config import (
        DATA_PROCESSED, DATA_OUTPUT,
        CLEANED_DATA_FILE, FORECAST_OUTPUT_FILE,
        REORDER_ALERTS_FILE, STOCKOUT_RISK_FILE,
        FORECAST_HORIZON_DAYS,
    )
except ImportError:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
    DATA_OUTPUT = PROJECT_ROOT / "data" / "output"
    CLEANED_DATA_FILE = "inventory_demand_cleaned.csv"
    FORECAST_OUTPUT_FILE = "demand_forecast.csv"
    REORDER_ALERTS_FILE = "reorder_recommendations.csv"
    STOCKOUT_RISK_FILE = "stockout_risk_scores.csv"
    FORECAST_HORIZON_DAYS = 90


def load_inventory_and_forecast(
    cleaned_path: Path | None = None,
    forecast_path: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cleaned_path = cleaned_path or (DATA_PROCESSED / CLEANED_DATA_FILE)
    forecast_path = forecast_path or (DATA_OUTPUT / FORECAST_OUTPUT_FILE)
    inv = pd.read_csv(cleaned_path)
    inv["date"] = pd.to_datetime(inv["date"])
    latest = inv.sort_values("date").groupby(["product_id", "warehouse_id"]).last().reset_index()
    latest = latest.rename(columns={"date": "as_of_date"})
    if forecast_path.exists():
        fc = pd.read_csv(forecast_path)
        fc["date"] = pd.to_datetime(fc["date"])
    else:
        fc = pd.DataFrame()
    return latest, fc


def compute_daily_forecast(fc: pd.DataFrame) -> float:
    if fc.empty or "forecast" not in fc.columns:
        return np.nan
    return fc["forecast"].mean()


def stockout_risk_score(
    inventory_level: float,
    reorder_point: float,
    lead_time_days: int,
    daily_demand: float,
    supplier_delay: int = 0,
) -> float:
    if daily_demand <= 0 or np.isnan(daily_demand):
        days_supply = 999 if inventory_level > 0 else 0
    else:
        days_supply = inventory_level / daily_demand
    required_days = lead_time_days + supplier_delay + 7
    if days_supply >= required_days * 1.5:
        return 0.0
    if days_supply <= 0:
        return 100.0
    ratio = days_supply / required_days
    return max(0, min(100, (1 - ratio) * 100))


def reorder_quantity(
    reorder_point: int,
    inventory_level: float,
    lead_time_days: int,
    daily_demand: float,
    safety_days: int = 7,
) -> float:
    if np.isnan(daily_demand) or daily_demand <= 0:
        return max(0, reorder_point - inventory_level)
    target = (lead_time_days + safety_days) * daily_demand
    return max(0, target - inventory_level)


def run_reorder_and_risk(
    cleaned_path: Path | None = None,
    forecast_path: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    latest, fc = load_inventory_and_forecast(cleaned_path, forecast_path)
    daily_demand = compute_daily_forecast(fc) if not fc.empty else 50.0

    rows_risk = []
    rows_reorder = []
    for _, r in latest.iterrows():
        inv = r.get("inventory_level", 0)
        rop = r.get("reorder_point", 50)
        lt = int(r.get("lead_time", 7))
        delay = int(r.get("supplier_delay", 0))
        risk = stockout_risk_score(inv, rop, lt, daily_demand, delay)
        qty = reorder_quantity(rop, inv, lt, daily_demand)
        rows_risk.append({
            "product_id": r["product_id"],
            "warehouse_id": r["warehouse_id"],
            "as_of_date": r["as_of_date"],
            "inventory_level": inv,
            "reorder_point": rop,
            "lead_time": lt,
            "daily_demand_estimate": round(daily_demand, 2),
            "stockout_risk_score": round(risk, 2),
        })
        rows_reorder.append({
            "product_id": r["product_id"],
            "warehouse_id": r["warehouse_id"],
            "as_of_date": r["as_of_date"],
            "inventory_level": inv,
            "reorder_point": rop,
            "recommended_reorder_quantity": max(0, int(np.ceil(qty))),
            "stockout_risk_score": round(risk, 2),
            "alert": "YES" if risk > 50 or inv < rop else "NO",
        })

    risk_df = pd.DataFrame(rows_risk)
    reorder_df = pd.DataFrame(rows_reorder)
    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    risk_df.to_csv(DATA_OUTPUT / STOCKOUT_RISK_FILE, index=False)
    reorder_df.to_csv(DATA_OUTPUT / REORDER_ALERTS_FILE, index=False)
    return risk_df, reorder_df


if __name__ == "__main__":
    run_reorder_and_risk()
    print("Stock-out risk saved to", DATA_OUTPUT / STOCKOUT_RISK_FILE)
    print("Reorder recommendations saved to", DATA_OUTPUT / REORDER_ALERTS_FILE)
