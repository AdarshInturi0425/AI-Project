# Example DuckDB Queries for Semantic Layer

This guide shows how to query the gold layer using DuckDB SQL.

## Setup

The `sql_layer.py` script registers `gold_view.csv` as a DuckDB table and runs queries.

```python
import duckdb

# Connect to in-memory database
conn = duckdb.connect(':memory:')

# Register CSV as table
conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")

# Query it
result = conn.execute("SELECT * FROM gold_view LIMIT 5").fetch_df()
print(result)
```

---

## Query Examples

### 1. Find Top 5 Customers by Total Spend

```sql
SELECT 
    customer_id,
    total_spend,
    transaction_count,
    ROUND(avg_transaction_amount, 2) as avg_transaction_amount
FROM gold_view
ORDER BY total_spend DESC
LIMIT 5;
```

**Output:**
```
customer_id  | total_spend | transaction_count | avg_transaction_amount
c_001        | 145.49      | 3                 | 48.50
c_002        | 300.00      | 2                 | 150.00
c_003        | 75.25       | 1                 | 75.25
```

---

### 2. Find Most Frequent Customers (by transaction count)

```sql
SELECT 
    customer_id,
    transaction_count,
    total_spend,
    ROUND(avg_transaction_amount, 2) as avg_per_transaction
FROM gold_view
WHERE transaction_count > 2
ORDER BY transaction_count DESC
LIMIT 10;
```

---

### 3. Spending Distribution by Quartiles

```sql
SELECT 
    CASE 
        WHEN total_spend < APPROX_QUANTILE(total_spend, 0.25) OVER () THEN 'Q1 (Low)'
        WHEN total_spend < APPROX_QUANTILE(total_spend, 0.50) OVER () THEN 'Q2'
        WHEN total_spend < APPROX_QUANTILE(total_spend, 0.75) OVER () THEN 'Q3'
        ELSE 'Q4 (High)'
    END as quartile,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spend), 2) as avg_spend,
    MIN(total_spend) as min_spend,
    MAX(total_spend) as max_spend
FROM gold_view
GROUP BY quartile
ORDER BY quartile;
```

---

### 4. High-Value Customers (Top 10% by spend)

```sql
WITH percentiles AS (
    SELECT APPROX_QUANTILE(total_spend, 0.90) as p90
    FROM gold_view
)
SELECT 
    customer_id,
    total_spend,
    transaction_count,
    ROUND(avg_transaction_amount, 2) as avg_transaction_amount
FROM gold_view
WHERE total_spend >= (SELECT p90 FROM percentiles)
ORDER BY total_spend DESC;
```

---

### 5. Customer Segmentation

```sql
SELECT 
    CASE 
        WHEN transaction_count = 1 THEN 'One-time Buyer'
        WHEN transaction_count BETWEEN 2 AND 5 THEN 'Occasional'
        WHEN transaction_count BETWEEN 6 AND 20 THEN 'Regular'
        ELSE 'VIP (20+ transactions)'
    END as segment,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spend), 2) as avg_spend_per_customer,
    ROUND(SUM(total_spend), 2) as total_segment_spend
FROM gold_view
GROUP BY segment
ORDER BY total_segment_spend DESC;
```

---

### 6. Average Transaction Value Analysis

```sql
SELECT 
    CASE 
        WHEN avg_transaction_amount < 50 THEN 'Low (<$50)'
        WHEN avg_transaction_amount < 100 THEN 'Medium ($50-$100)'
        WHEN avg_transaction_amount < 200 THEN 'High ($100-$200)'
        ELSE 'Premium (>$200)'
    END as price_tier,
    COUNT(*) as customer_count,
    ROUND(AVG(avg_transaction_amount), 2) as avg_tier_price,
    ROUND(SUM(total_spend), 2) as tier_total_spend
FROM gold_view
GROUP BY price_tier
ORDER BY tier_total_spend DESC;
```

---

### 7. Total Business Metrics

```sql
SELECT 
    COUNT(*) as total_customers,
    SUM(transaction_count) as total_transactions,
    ROUND(SUM(total_spend), 2) as total_revenue,
    ROUND(AVG(total_spend), 2) as avg_customer_ltv,
    ROUND(AVG(avg_transaction_amount), 2) as avg_transaction_value,
    ROUND(MAX(total_spend), 2) as highest_customer_value,
    ROUND(MIN(total_spend), 2) as lowest_customer_value
FROM gold_view;
```

**Output:**
```
total_customers | total_transactions | total_revenue | avg_customer_ltv | ...
520             | 1,250              | $48,500.00    | $93.27          | ...
```

---

### 8. Filter by Customer ID

```sql
SELECT 
    customer_id,
    total_spend,
    transaction_count,
    ROUND(avg_transaction_amount, 2) as avg_transaction_amount
FROM gold_view
WHERE customer_id = 'c_001';
```

---

### 9. Find Outliers (unusually high/low values)

```sql
WITH stats AS (
    SELECT 
        AVG(total_spend) as avg_spend,
        STDDEV(total_spend) as stddev_spend
    FROM gold_view
)
SELECT 
    customer_id,
    total_spend,
    ROUND((total_spend - stats.avg_spend) / stats.stddev_spend, 2) as z_score,
    CASE 
        WHEN total_spend > stats.avg_spend + (3 * stats.stddev_spend) THEN 'HIGH OUTLIER'
        WHEN total_spend < stats.avg_spend - (3 * stats.stddev_spend) THEN 'LOW OUTLIER'
        ELSE 'Normal'
    END as status
FROM gold_view, stats
WHERE ABS((total_spend - stats.avg_spend) / stats.stddev_spend) > 2
ORDER BY z_score DESC;
```

---

### 10. Time-based Analysis (if date columns added)

```sql
-- Note: Current gold_view doesn't have dates, but here's the template:
-- Add transaction_date to silver layer first, then aggregate to gold

SELECT 
    DATE_TRUNC('month', transaction_date) as month,
    COUNT(DISTINCT customer_id) as active_customers,
    SUM(amount) as monthly_revenue,
    ROUND(AVG(amount), 2) as avg_transaction_value
FROM transactions_silver
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month DESC;
```

---

## Running Queries via Python

```python
import duckdb
import pandas as pd

# Connect
conn = duckdb.connect(':memory:')

# Load gold view
conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")

# Example: Top 5 customers
result = conn.execute("""
    SELECT customer_id, total_spend
    FROM gold_view
    ORDER BY total_spend DESC
    LIMIT 5
""").fetch_df()

print(result)
```

---

## Running Queries via CLI

```bash
# Interactive DuckDB shell
duckdb

# In DuckDB:
.read SemanticLayer/data/gold/gold_view.csv as gold_view
SELECT * FROM gold_view LIMIT 10;
```

---

## Common Aggregations Reference

| Function | Description | Example |
|----------|-------------|---------|
| `COUNT(*)` | Row count | `COUNT(*) as total_rows` |
| `SUM()` | Sum of values | `SUM(total_spend) as total_revenue` |
| `AVG()` | Average | `AVG(avg_transaction_amount)` |
| `MIN()` / `MAX()` | Min/Max | `MIN(total_spend) as lowest_spend` |
| `STDDEV()` | Standard deviation | `STDDEV(total_spend) as spend_variance` |
| `APPROX_QUANTILE()` | Percentiles | `APPROX_QUANTILE(total_spend, 0.90)` |
| `GROUP BY` | Grouping | `GROUP BY customer_segment` |
| `HAVING` | Filter groups | `HAVING COUNT(*) > 5` |
| `ORDER BY` | Sorting | `ORDER BY total_spend DESC` |
| `LIMIT` | Row limit | `LIMIT 10` |

---

## More Resources

- [DuckDB SQL Documentation](https://duckdb.org/docs/sql/introduction)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [SemanticLayer Notebook](SemanticLayer/notebooks/semantic_layer_demo_colab.ipynb)
