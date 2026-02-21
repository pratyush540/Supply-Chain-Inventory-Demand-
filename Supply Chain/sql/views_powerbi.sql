CREATE OR REPLACE VIEW v_pbi_forecast_vs_actual AS
SELECT
    COALESCE(h.date, f.date) AS date,
    h.total_daily_sales AS actual_sales,
    f.forecast AS forecast_sales,
    f.model AS forecast_model
FROM v_daily_demand_summary h
FULL OUTER JOIN demand_forecast f ON h.date = f.date
ORDER BY date, model;

CREATE OR REPLACE VIEW v_pbi_stockout_risk AS
SELECT
    product_id,
    warehouse_id,
    as_of_date,
    inventory_level,
    reorder_point,
    stockout_risk_score,
    CASE
        WHEN stockout_risk_score >= 75 THEN 'Critical'
        WHEN stockout_risk_score >= 50 THEN 'High'
        WHEN stockout_risk_score >= 25 THEN 'Medium'
        ELSE 'Low'
    END AS risk_tier
FROM stockout_risk_scores
ORDER BY stockout_risk_score DESC;

CREATE OR REPLACE VIEW v_pbi_inventory_turnover_kpi AS
SELECT
    warehouse_id,
    SUM(total_sales_quantity) AS total_sales,
    AVG(avg_inventory_level) AS avg_inventory,
    ROUND(SUM(total_sales_quantity)::NUMERIC / NULLIF(AVG(avg_inventory_level), 0), 4) AS turnover_ratio
FROM v_inventory_turnover
GROUP BY warehouse_id;

CREATE OR REPLACE VIEW v_pbi_demand_trend_by_product AS
SELECT
    product_id,
    DATE_TRUNC('month', date)::DATE AS month_start,
    SUM(sales_quantity) AS monthly_sales,
    SUM(sales_quantity * price) AS monthly_revenue
FROM inventory_demand_historical
GROUP BY product_id, DATE_TRUNC('month', date)
ORDER BY product_id, month_start;

CREATE OR REPLACE VIEW v_pbi_warehouse_heatmap AS
SELECT
    product_id,
    warehouse_id,
    SUM(sales_quantity) AS total_sales,
    SUM(stockout_flag) AS stockout_events,
    ROUND(100.0 * SUM(stockout_flag) / NULLIF(COUNT(*), 0), 2) AS stockout_pct
FROM inventory_demand_historical
GROUP BY product_id, warehouse_id;

CREATE OR REPLACE VIEW v_pbi_reorder_alerts AS
SELECT
    product_id,
    warehouse_id,
    as_of_date,
    inventory_level,
    reorder_point,
    recommended_reorder_quantity,
    stockout_risk_score,
    alert
FROM reorder_recommendations
WHERE alert = 'YES'
ORDER BY stockout_risk_score DESC;
