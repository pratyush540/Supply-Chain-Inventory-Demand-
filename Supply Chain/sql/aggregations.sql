CREATE OR REPLACE VIEW v_monthly_demand_trends AS
SELECT
    DATE_TRUNC('month', date)::DATE AS month_start,
    SUM(sales_quantity) AS total_sales_quantity,
    COUNT(DISTINCT product_id) AS product_count,
    COUNT(DISTINCT warehouse_id) AS warehouse_count,
    SUM(sales_quantity * price) AS total_revenue
FROM inventory_demand_historical
GROUP BY DATE_TRUNC('month', date)
ORDER BY month_start;

CREATE OR REPLACE VIEW v_warehouse_performance AS
SELECT
    warehouse_id,
    COUNT(DISTINCT date) AS days_with_data,
    SUM(sales_quantity) AS total_sales,
    SUM(sales_quantity * price) AS total_revenue,
    SUM(stockout_flag) AS stockout_events,
    COUNT(*) AS record_count,
    ROUND(100.0 * SUM(stockout_flag) / NULLIF(COUNT(*), 0), 2) AS stockout_rate_pct
FROM inventory_demand_historical
GROUP BY warehouse_id
ORDER BY total_sales DESC;

CREATE OR REPLACE VIEW v_inventory_turnover AS
SELECT
    product_id,
    warehouse_id,
    SUM(sales_quantity) AS total_sales_quantity,
    AVG(inventory_level) AS avg_inventory_level,
    CASE
        WHEN AVG(inventory_level) > 0 THEN ROUND(SUM(sales_quantity)::NUMERIC / AVG(inventory_level), 4)
        ELSE NULL
    END AS inventory_turnover_ratio
FROM inventory_demand_historical
GROUP BY product_id, warehouse_id
ORDER BY inventory_turnover_ratio DESC NULLS LAST;

CREATE OR REPLACE VIEW v_stockout_frequency AS
SELECT
    product_id,
    warehouse_id,
    COUNT(*) AS total_days,
    SUM(stockout_flag) AS stockout_days,
    ROUND(100.0 * SUM(stockout_flag) / NULLIF(COUNT(*), 0), 2) AS stockout_frequency_pct
FROM inventory_demand_historical
GROUP BY product_id, warehouse_id
HAVING SUM(stockout_flag) > 0
ORDER BY stockout_frequency_pct DESC;

CREATE OR REPLACE VIEW v_daily_demand_summary AS
SELECT
    date,
    SUM(sales_quantity) AS total_daily_sales,
    AVG(inventory_level) AS avg_inventory_level
FROM inventory_demand_historical
GROUP BY date
ORDER BY date;
