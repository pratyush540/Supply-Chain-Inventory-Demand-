CREATE TABLE IF NOT EXISTS inventory_demand_historical (
    product_id       VARCHAR(32) NOT NULL,
    warehouse_id      VARCHAR(32) NOT NULL,
    date             DATE NOT NULL,
    sales_quantity   NUMERIC(18,2) NOT NULL,
    inventory_level  NUMERIC(18,2) NOT NULL,
    reorder_point    NUMERIC(18,2) NOT NULL,
    lead_time        INTEGER NOT NULL,
    promotion_flag   SMALLINT NOT NULL,
    seasonality_index NUMERIC(10,4) NOT NULL,
    price            NUMERIC(18,2) NOT NULL,
    supplier_delay   INTEGER NOT NULL,
    stockout_flag    SMALLINT NOT NULL,
    PRIMARY KEY (product_id, warehouse_id, date)
);

CREATE TABLE IF NOT EXISTS demand_forecast (
    date    DATE NOT NULL,
    model   VARCHAR(32) NOT NULL,
    forecast NUMERIC(18,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS reorder_recommendations (
    product_id                 VARCHAR(32) NOT NULL,
    warehouse_id               VARCHAR(32) NOT NULL,
    as_of_date                 DATE NOT NULL,
    inventory_level            NUMERIC(18,2) NOT NULL,
    reorder_point              NUMERIC(18,2) NOT NULL,
    recommended_reorder_quantity INTEGER NOT NULL,
    stockout_risk_score        NUMERIC(8,2) NOT NULL,
    alert                      VARCHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS stockout_risk_scores (
    product_id             VARCHAR(32) NOT NULL,
    warehouse_id           VARCHAR(32) NOT NULL,
    as_of_date             DATE NOT NULL,
    inventory_level        NUMERIC(18,2) NOT NULL,
    reorder_point          NUMERIC(18,2) NOT NULL,
    lead_time              INTEGER NOT NULL,
    daily_demand_estimate  NUMERIC(18,2) NOT NULL,
    stockout_risk_score    NUMERIC(8,2) NOT NULL
);
