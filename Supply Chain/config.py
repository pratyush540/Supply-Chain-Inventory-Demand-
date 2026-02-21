import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_OUTPUT = PROJECT_ROOT / "data" / "output"
MODELS_DIR = PROJECT_ROOT / "models"

for _dir in (DATA_RAW, DATA_PROCESSED, DATA_OUTPUT, MODELS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

RAW_DATA_FILE = "inventory_demand_raw.csv"
CLEANED_DATA_FILE = "inventory_demand_cleaned.csv"
FEATURED_DATA_FILE = "inventory_demand_featured.csv"
FORECAST_OUTPUT_FILE = "demand_forecast.csv"
REORDER_ALERTS_FILE = "reorder_recommendations.csv"
STOCKOUT_RISK_FILE = "stockout_risk_scores.csv"

FORECAST_HORIZON_DAYS = 90
EVAL_HORIZON_DAYS = 30

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "supply_chain"),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "schema": os.getenv("DB_SCHEMA", "public"),
}

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "")
