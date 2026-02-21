# Power BI Dashboard — Supply Chain Analytics

## Data source

Connect Power BI to your data warehouse (PostgreSQL or Snowflake) and use the views created by the SQL layer:

| View | Purpose |
|------|--------|
| `v_pbi_forecast_vs_actual` | Forecast vs Actual |
| `v_pbi_stockout_risk` | Stock-out risk indicator |
| `v_pbi_inventory_turnover_kpi` | Inventory turnover KPI |
| `v_pbi_demand_trend_by_product` | Demand trend by product |
| `v_pbi_warehouse_heatmap` | Warehouse performance heatmap |
| `v_pbi_reorder_alerts` | Reorder recommendation alerts |

Alternatively, use the CSV exports from `data/output/` (e.g. after running `run_pipeline.py`):

- `demand_forecast.csv`
- `reorder_recommendations.csv`
- `stockout_risk_scores.csv`
- `inventory_demand_cleaned.csv` (from `data/processed/`)

## Dashboard structure

1. **Forecast vs Actual**
   - Line chart: Date on X; Actual sales and Forecast sales (by model) on Y.
   - Slicer: Forecast model (ARIMA / Prophet).

2. **Stock-out risk indicator**
   - Table or matrix: Product, Warehouse, Risk tier, Stockout risk score.
   - Conditional formatting: Red (Critical/High), Yellow (Medium), Green (Low).

3. **Inventory turnover KPI**
   - Card: Overall or per-warehouse turnover ratio.
   - Goal: show improvement (e.g. +20% vs baseline).

4. **Demand trend by product**
   - Line or area chart: Month on X; Monthly sales or revenue by Product.

5. **Warehouse performance heatmap**
   - Matrix: Rows = Product, Columns = Warehouse; Values = Total sales or Stockout %.
   - Background color scale for quick comparison.

6. **Reorder recommendation alerts**
   - Table with filters: only Alert = YES; columns Product, Warehouse, Recommended reorder quantity, Stockout risk score.
   - Use for proactive restocking.

## Connection (PostgreSQL)

- Get Data → PostgreSQL database → Server: `DB_HOST`, Database: `DB_NAME`.
- Use views in `public` (or your `DB_SCHEMA`).

## Connection (Snowflake)

- Get Data → Snowflake → Server: `account.region`, Warehouse, Database, Schema.
- Use the same view names created in your schema.

## Refresh

Schedule refresh in Power BI Service after the Python pipeline (and optional SQL load) runs (e.g. daily).
