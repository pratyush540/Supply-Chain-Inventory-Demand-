# Supply Chain Analytics — Inventory & Demand Forecasting Platform

Enterprise-grade pipeline for **demand forecasting** and **stock-out risk** to reduce stockouts and improve inventory turnover. Built with Python, SQL, and Power BI.

---

## Business objectives

| Goal | Target | How the platform helps |
|------|--------|-------------------------|
| **Reduce stockouts** | ≥ 25% | Predictive restocking via reorder recommendations and stock-out risk scores |
| **Improve inventory turnover** | ≥ 20% | Demand-driven planning and reorder points aligned to forecasted demand |
| **Proactive planning** | Yes | 30–90 day demand forecasts (ARIMA + Prophet) and alerts for at-risk SKU/warehouse |

---

## Business impact

- **25% reduction in stockouts**: Reorder logic uses lead time, current inventory, and forecasted daily demand to suggest order quantities; stock-out risk score (0–100) highlights critical product-warehouse pairs so teams act before shortages.
- **20% improvement in inventory turnover**: Inventory turnover is computed at product-warehouse level (sales / avg inventory). Forecasting and reorder recommendations reduce overstock and align inventory to demand.
- **Better forecast accuracy**: Time-series models (ARIMA, Prophet) are evaluated with MAE and RMSE; optional features include seasonality and promotion flags for promotion-driven demand.

---

## Technology stack

- **Python**: Pandas, NumPy, Statsmodels (ARIMA), Prophet, Scikit-learn
- **SQL**: PostgreSQL or Snowflake-compatible DDL, aggregations, and views
- **Power BI**: Dashboards for forecast vs actual, stock-out risk, turnover KPI, demand trends, warehouse heatmap, reorder alerts

---

## Data structure

Dataset schema (generated or ingested):

| Column | Description |
|--------|-------------|
| `product_id` | Product/SKU identifier |
| `warehouse_id` | Warehouse or location |
| `date` | Daily snapshot date |
| `sales_quantity` | Units sold |
| `inventory_level` | On-hand inventory |
| `reorder_point` | Reorder threshold |
| `lead_time` | Supplier lead time (days) |
| `promotion_flag` | 1 if promotion, 0 otherwise |
| `seasonality_index` | Seasonal factor |
| `price` | Unit price |
| `supplier_delay` | Extra delay (days) |
| `stockout_flag` | Target: 1 if stockout, 0 otherwise |

---

## Project structure

```
Supply-Chain-Analytics-main/
├── config.py                 # Paths and DB config (env-based)
├── run_pipeline.py           # End-to-end pipeline entrypoint
├── requirements.txt
├── README.md
├── data/
│   ├── raw/                  # Raw or generated input (e.g. inventory_demand_raw.csv)
│   ├── processed/            # Cleaned data
│   └── output/              # Forecasts, reorder alerts, risk scores
├── models/                   # Saved models (optional)
├── src/
│   ├── data_generator.py     # Synthetic data with required schema
│   ├── data_pipeline.py      # Clean and preprocess
│   ├── feature_engineering.py # Lags, rolling stats, date features
│   ├── forecast.py          # ARIMA + Prophet, MAE/RMSE comparison
│   └── reorder_risk.py      # Reorder recommendations + stock-out risk score
├── sql/
│   ├── ddl.sql              # Tables for historical, forecast, reorder, risk
│   ├── aggregations.sql     # Monthly trends, warehouse performance, turnover, stockout frequency
│   └── views_powerbi.sql    # Views for Power BI
└── power_bi/
    └── README.md            # Dashboard structure and connection guide
```

---

## Quick start

1. **Clone and setup**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Supply-Chain-Analytics.git
   cd Supply-Chain-Analytics
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Generate data and run pipeline** (no DB required for CSV output)
   ```bash
   python run_pipeline.py
   ```
   This will:
   - Generate synthetic data in `data/raw/` if missing
   - Clean and write `data/processed/inventory_demand_cleaned.csv`
   - Build features and write `data/output/inventory_demand_featured.csv`
   - Run ARIMA and Prophet, compare MAE/RMSE, write `data/output/demand_forecast.csv`
   - Compute reorder recommendations and stock-out risk in `data/output/`

3. **SQL layer**  
   Run in order against your database:
   - `sql/ddl.sql` — create tables
   - Load `data/processed/inventory_demand_cleaned.csv` and `data/output/*.csv` into the tables (use your ETL or COPY/INSERT)
   - `sql/aggregations.sql` — create aggregation views
   - `sql/views_powerbi.sql` — create Power BI views

4. **Power BI**  
   See `power_bi/README.md` for data sources (DB views or CSV), and dashboard layout: Forecast vs Actual, Stock-out risk, Inventory turnover KPI, Demand by product, Warehouse heatmap, Reorder alerts.

---

## Configuration

- **Paths**: Edit `config.py` if you need different data/output paths.
- **Database**: Set env vars `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_SCHEMA` for PostgreSQL. For Snowflake use `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_WAREHOUSE`, etc.

---

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| Cleaned history | `data/processed/inventory_demand_cleaned.csv` | Ready for SQL load and modeling |
| Featured dataset | `data/output/inventory_demand_featured.csv` | Lags, rolling stats for advanced models |
| Demand forecast | `data/output/demand_forecast.csv` | Next 30–90 days by model (ARIMA, Prophet) |
| Reorder recommendations | `data/output/reorder_recommendations.csv` | Suggested order qty and alert flag |
| Stock-out risk | `data/output/stockout_risk_scores.csv` | Risk score 0–100 per product-warehouse |

---

## License

MIT License. See [LICENSE](LICENSE).
