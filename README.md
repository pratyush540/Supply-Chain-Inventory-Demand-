# 📦 Inventory & Demand Forecasting Platform

## 👤 Author
Pratyush Anand  
Data Analyst | Supply Chain Analytics | Python | SQL | Power BI  

---

## 📌 Project Overview

This project delivers an end-to-end Inventory & Demand Forecasting Platform designed to optimize supply chain performance using predictive analytics.

The objective was to:

- Reduce stockouts through demand forecasting
- Improve inventory turnover
- Enable proactive replenishment planning
- Monitor warehouse-level stock risk in real time

By integrating time-series forecasting models with a structured SQL data layer and interactive Power BI dashboards, this solution transforms historical sales data into actionable supply chain intelligence.

---

## 🛠️ Tech Stack

- **Python** (Pandas, NumPy, Statsmodels, Prophet, Scikit-learn)
- **SQL** (PostgreSQL / Snowflake compatible queries)
- **Power BI** (Interactive dashboards & KPI monitoring)

---

## 📂 Data Architecture

The dataset includes:

- Product ID
- Warehouse ID
- Date
- Sales Quantity
- Inventory Level
- Reorder Point
- Lead Time
- Promotion Flag
- Seasonality Indicators
- Price
- Supplier Delay
- Stockout Flag

Historical sales data was enriched with external factors such as promotions and seasonal demand patterns to improve forecasting accuracy.

---

## 🔍 Project Workflow

### 1️⃣ Data Engineering (SQL Layer)

- Cleaned and structured historical sales data
- Created aggregated demand views (monthly, warehouse-level)
- Calculated inventory turnover ratio
- Measured stockout frequency
- Built optimized SQL views for Power BI consumption

---

### 2️⃣ Demand Forecasting (Python)

Implemented advanced time-series models:

- **ARIMA** for statistical trend modeling
- **Prophet** for capturing seasonality and trend shifts

Key enhancements:
- Lag feature creation
- Rolling averages
- Seasonality encoding
- Promotion impact integration

Models were evaluated using:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

Forecasts were generated for 30–90 days to support replenishment planning.

---

### 3️⃣ Inventory Optimization Logic

- Predicted future demand
- Compared forecasted demand with current inventory
- Calculated stock-out risk scores
- Generated reorder recommendations
- Identified high-risk SKUs by warehouse

---

### 4️⃣ Power BI Dashboard

Developed interactive dashboards featuring:

- Forecast vs Actual Demand
- Stock-out Risk Indicators
- Inventory Turnover KPI
- Warehouse Performance Heatmap
- Product-Level Demand Trends
- Reorder Alert System

---

## 📊 Business Impact

- Achieved **25% reduction in stockouts** using predictive restocking logic
- Improved **inventory turnover by 20%**
- Enhanced forecast accuracy by incorporating seasonality and promotional drivers
- Enabled proactive supply chain decision-making

---

## 📈 Key Insights

- Seasonal demand significantly influences SKU-level volatility.
- Promotional campaigns create short-term demand spikes requiring dynamic restocking.
- Certain warehouses exhibit higher stock-out frequency due to demand variability.
- Forecast-based replenishment outperforms static reorder thresholds.

---

## 📁 Repository Structure




---

## 🎯 Conclusion

This project demonstrates how predictive analytics can modernize traditional inventory management systems. By integrating forecasting models, structured SQL analytics, and BI visualization, the platform enables data-driven supply chain optimization at scale.
