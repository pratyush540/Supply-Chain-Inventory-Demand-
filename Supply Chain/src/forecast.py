import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta

try:
    from config import (
        DATA_PROCESSED, DATA_OUTPUT, MODELS_DIR,
        CLEANED_DATA_FILE, FORECAST_OUTPUT_FILE,
        FORECAST_HORIZON_DAYS, EVAL_HORIZON_DAYS,
    )
except ImportError:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
    DATA_OUTPUT = PROJECT_ROOT / "data" / "output"
    MODELS_DIR = PROJECT_ROOT / "models"
    CLEANED_DATA_FILE = "inventory_demand_cleaned.csv"
    FORECAST_OUTPUT_FILE = "demand_forecast.csv"
    FORECAST_HORIZON_DAYS = 90
    EVAL_HORIZON_DAYS = 30

MODELS_DIR.mkdir(parents=True, exist_ok=True)


def load_cleaned(path: Path | None = None) -> pd.DataFrame:
    path = path or (DATA_PROCESSED / CLEANED_DATA_FILE)
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def prepare_ts_series(df: pd.DataFrame, level: str = "product") -> pd.DataFrame:
    if level == "product":
        ts = df.groupby(["date"])["sales_quantity"].sum().reset_index()
        ts = ts.rename(columns={"sales_quantity": "y"})
        ts["ds"] = ts["date"]
    else:
        ts = df.groupby(["product_id", "warehouse_id", "date"])["sales_quantity"].sum().reset_index()
        ts = ts.rename(columns={"sales_quantity": "y", "date": "ds"})
    return ts


def evaluate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {"MAE": mae, "RMSE": rmse}


def forecast_arima(series: pd.Series, horizon: int) -> np.ndarray:
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(series.astype(float), order=(2, 1, 2))
    fitted = model.fit()
    return fitted.forecast(steps=horizon).values


def forecast_prophet(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    from prophet import Prophet
    df = df[["ds", "y"]].dropna()
    df["y"] = df["y"].astype(float)
    m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    m.fit(df)
    future = m.make_future_dataframe(periods=horizon)
    pred = m.predict(future)
    return pred[["ds", "yhat"]].tail(horizon)


def run_forecast_product_level(
    horizon_days: int | None = None,
    eval_days: int | None = None,
    input_path: Path | None = None,
) -> tuple:
    horizon_days = horizon_days or FORECAST_HORIZON_DAYS
    eval_days = eval_days or EVAL_HORIZON_DAYS
    df = load_cleaned(input_path)
    ts = prepare_ts_series(df, level="product")
    ts = ts.sort_values("ds").reset_index(drop=True)
    ts["y"] = ts["y"].astype(float)

    n = len(ts)
    train = ts.iloc[: max(1, n - eval_days)]
    test = ts.iloc[-eval_days:] if n > eval_days else pd.DataFrame()

    results = []
    metrics_all = {}

    try:
        arima_pred = forecast_arima(train["y"], horizon=min(horizon_days, len(train)))
        if len(test):
            arima_eval = forecast_arima(train["y"], horizon=len(test))
            metrics_all["ARIMA"] = evaluate_metrics(test["y"].values, arima_eval)
        else:
            metrics_all["ARIMA"] = {"MAE": np.nan, "RMSE": np.nan}
        last_date = train["ds"].max()
        arima_dates = pd.date_range(start=last_date + timedelta(days=1), periods=len(arima_pred), freq="D")
        for i, d in enumerate(arima_dates):
            if i < horizon_days:
                results.append({"date": d, "model": "ARIMA", "forecast": float(arima_pred[i])})
    except Exception as e:
        metrics_all["ARIMA"] = {"MAE": np.nan, "RMSE": np.nan, "error": str(e)}

    try:
        prophet_future = forecast_prophet(train, horizon=horizon_days)
        if len(test) and len(prophet_future) >= len(test):
            prophet_eval = forecast_prophet(train, horizon=len(test))
            metrics_all["Prophet"] = evaluate_metrics(
                test["y"].values[: len(prophet_eval)],
                prophet_eval["yhat"].values[: len(test)],
            )
        else:
            metrics_all["Prophet"] = {"MAE": np.nan, "RMSE": np.nan}
        for _, row in prophet_future.iterrows():
            results.append({"date": row["ds"], "model": "Prophet", "forecast": float(row["yhat"])})
    except Exception as e:
        metrics_all["Prophet"] = {"MAE": np.nan, "RMSE": np.nan, "error": str(e)}

    forecast_df = pd.DataFrame(results)
    if not forecast_df.empty:
        output_path = DATA_OUTPUT / FORECAST_OUTPUT_FILE
        output_path.parent.mkdir(parents=True, exist_ok=True)
        forecast_df.to_csv(output_path, index=False)
    return forecast_df, metrics_all


if __name__ == "__main__":
    forecast_df, metrics = run_forecast_product_level()
    print("Model comparison:", metrics)
    print("Forecast saved to", DATA_OUTPUT / FORECAST_OUTPUT_FILE)
