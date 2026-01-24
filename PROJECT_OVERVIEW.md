# SemanticLayer - Complete Project Overview

## 🎯 What is This Project?

**SemanticLayer** is a **data pipeline** that transforms raw business data into clean, aggregated insights.

Think of it like a **factory assembly line**:
1. **Raw Materials** (messy transaction data) → 
2. **Quality Control** (data cleaning) → 
3. **Assembly** (aggregation) → 
4. **Finished Product** (analytics-ready insights)

---

## 📊 Real-World Example

Imagine you run an e-commerce store with 1,000 customers and 50,000 transactions.

### The Problem
- Data is scattered across systems
- Duplicates and errors exist
- Hard to answer business questions like:
  - *Who are my top 10 customers?*
  - *What's the average order value?*
  - *How many one-time buyers do I have?*

### The Solution: SemanticLayer
This project **automatically**:
1. Cleans your data
2. Removes duplicates
3. Calculates key metrics
4. Stores results in queryable format
5. Provides SQL interface for analysis

---

## 🏗️ Three-Layer Architecture

### Layer 1: RAW Data
```
Input CSV files with messy data
├── customers_raw.csv
│   ├── customer_id, email, email (duplicate column!), created_date
│   └── Some rows with missing emails
└── transactions_raw.csv
    ├── transaction_id, customer_id, amount, timestamp, status
    └── Some invalid amounts (negative, zero)
```

**Why it's messy:**
- Extra/duplicate columns
- Missing values (NULLs)
- Invalid data (negative amounts)
- Inconsistent formatting

### Layer 2: SILVER Data (Cleaned)
```
Deduplicated, validated data
├── customers_silver.csv
│   ├── Only essential columns: customer_id, email
│   ├── No duplicates
│   └── All NULLs removed
└── transactions_silver.csv
    ├── Only valid transactions
    ├── No negative amounts
    └── Consistent formatting
```

**Why it's better:**
- ✓ Deduplicated
- ✓ Validated (no nulls in key fields)
- ✓ Standardized format
- ✓ Ready for analysis

### Layer 3: GOLD Data (Aggregated)
```
Business metrics per customer (SEMANTIC LAYER)
├── gold_view.csv
│   ├── customer_id: Unique identifier
│   ├── total_spend: Sum of all purchases
│   ├── transaction_count: Number of purchases
│   └── avg_transaction_amount: Average order value
```

**Why it's valuable:**
- ✓ Business metrics ready to use
- ✓ One row per customer
- ✓ Perfect for dashboards/reports
- ✓ Enables customer segmentation

---

## 📈 Data Flow Visualization

```
Raw Layer               Silver Layer            Gold Layer
─────────────────       ──────────────          ──────────
customers_raw.csv  ──→  Remove duplicates  ──→  Aggregate
(1,100 rows)            Remove NULLs            by customer
                        (1,000 rows)            (customers_gold)
                                                (1,000 rows, 1 per customer)

transactions_raw.csv ─→ Filter invalid   ──→   Calculate:
(55,000 rows)           Remove negatives        - total_spend
                        Clean format            - transaction_count
                        (50,000 rows)           - avg_transaction_amount
                                                (1,000 rows aggregated)
```

---

## 🔍 Understanding Each Component

### 1. ETL Script (process_data_spark.py)

**What it does:**
- **E**xtract: Reads raw CSV files
- **T**ransform: Cleans and aggregates data
- **L**oad: Writes to silver/gold layers

**Example:**
```python
# Pseudocode
raw_customers = read_csv("raw/customers_raw.csv")
clean_customers = raw_customers.dropna().drop_duplicates()
write_csv(clean_customers, "silver/customers_silver.csv")

# Aggregate to gold
gold = clean_transactions.groupby("customer_id").agg({
    "amount": ["sum", "count", "mean"]
})
write_csv(gold, "gold/gold_view.csv")
```

**Output:**
- ✓ `silver/customers_silver.csv` (clean customer data)
- ✓ `silver/transactions_silver.csv` (clean transactions)
- ✓ `gold/gold_view.csv` (aggregated metrics)
- ✓ `metadata.json` (schema info)

---

### 2. SQL Query Layer (sql_layer.py)

**What it does:**
- Reads gold layer CSV
- Registers as DuckDB table
- Runs SQL queries for analysis

**Example Question → Query → Answer:**

**Question:** *"Who are my top 5 customers?"*

```sql
SELECT 
    customer_id,
    total_spend
FROM gold_view
ORDER BY total_spend DESC
LIMIT 5;
```

**Answer:**
```
customer_id | total_spend
c_001       | $5,432.50
c_002       | $4,921.30
c_003       | $3,841.00
c_004       | $3,500.25
c_005       | $3,200.00
```

---

### 3. Data Validation (data_validation.py)

**What it does:**
- Checks data quality
- Ensures no corruption
- Validates aggregations

**Checks performed:**
- ✓ Files exist and aren't empty
- ✓ Required columns present
- ✓ No unexpected NULLs
- ✓ Amounts are positive
- ✓ Gold metrics match silver data

**Example:**
```
✓ File exists: silver/customers_silver.csv (1.2 MB)
✓ No nulls: All 1000 customers have valid IDs
✓ Numeric range: All amounts > 0
✓ Gold aggregations: Verified against silver data
✓ PASSED: All 15 quality checks
```

---

### 4. Summary Statistics (summary_stats.py)

**What it does:**
- Calculates business insights
- Displays key metrics
- Segments customers

**Example Output:**
```
📊 Summary Statistics
─────────────────────
Total Customers:        1,000
Total Spend:           $520,500.00
Total Transactions:     15,200
Avg Transaction Amount: $34.23

🏆 Top 5 Customers
─────────────────────
1. c_001: $5,432.50 (42 purchases)
2. c_002: $4,921.30 (38 purchases)
...

💰 Spending Distribution
─────────────────────
Low Spenders (Q1):      250 customers
Mid-Low (Q2):           250 customers
Mid-High (Q3):          250 customers
High Spenders (Q4):     250 customers
```

---

## 🚀 How to Use This Project

### Scenario 1: Get Business Insights (Quick Start)

```bash
# 1. Run entire pipeline in one command
./quick_start.sh

# 2. See summary statistics
python SemanticLayer/scripts/summary_stats.py

# 3. Check data quality
python SemanticLayer/scripts/data_validation.py
```

**Output files:**
- `gold_view.csv` – Your analytics data
- Summary report in console

---

### Scenario 2: Run Custom SQL Queries

```bash
# 1. Setup project
source .venv/bin/activate
pip install -r SemanticLayer/requirements.txt

# 2. Run ETL to create gold layer
python SemanticLayer/scripts/process_data_spark.py

# 3. Query data
python -c "
import duckdb
conn = duckdb.connect(':memory:')
conn.execute(\"CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'\")

# Question: Average spending by customer
result = conn.execute('''
    SELECT 
        AVG(total_spend) as avg_customer_value,
        MIN(total_spend) as min_spend,
        MAX(total_spend) as max_spend
    FROM gold_view
''').fetch_df()

print(result)
"
```

---

### Scenario 3: Add Your Own Data

#### Step 1: Prepare Input Files

Create `SemanticLayer/data/raw/`:

**customers_raw.csv:**
```
customer_id,email
c_001,alice@example.com
c_002,bob@example.com
c_003,charlie@example.com
```

**transactions_raw.csv:**
```
transaction_id,customer_id,amount
t_001,c_001,100.00
t_002,c_001,50.50
t_003,c_002,200.00
t_004,c_003,-50.00
```

#### Step 2: Run ETL

```bash
python SemanticLayer/scripts/process_data_spark.py
```

#### Step 3: View Results

```bash
cat SemanticLayer/data/gold/gold_view.csv
```

**Output:**
```
customer_id,total_spend,transaction_count,avg_transaction_amount
c_001,150.50,2,75.25
c_002,200.00,1,200.00
c_003,0.00,1,0.00
```

---

## 📚 Key Concepts to Learn

### 1. What is ETL?

**E**xtract → **T**ransform → **L**oad

| Step | Meaning | Example |
|------|---------|---------|
| **Extract** | Read data from source | `read_csv("raw.csv")` |
| **Transform** | Clean and reshape | `df.dropna().groupby()` |
| **Load** | Write to destination | `write_csv(df, "gold.csv")` |

### 2. What is Aggregation?

Combining many rows into fewer, meaningful rows.

**Before (Raw):**
```
transaction_id | customer_id | amount
t_001          | c_001       | 100
t_002          | c_001       | 50
t_003          | c_001       | 75
t_004          | c_002       | 200
```

**After (Aggregated):**
```
customer_id | total_spend | transaction_count | avg_amount
c_001       | 225         | 3                 | 75
c_002       | 200         | 1                 | 200
```

### 3. What is a Semantic Layer?

A business-friendly view of data that answers real questions:
- *How much did customer X spend?*
- *Which customers are most valuable?*
- *What's the average order value?*

NOT technical jargon → BUSINESS INSIGHTS

### 4. What is SQL?

Structured Query Language - asking questions of data:

```sql
-- "Show me top 3 customers"
SELECT customer_id, total_spend
FROM gold_view
ORDER BY total_spend DESC
LIMIT 3;

-- "How many customers spent more than $1000?"
SELECT COUNT(*) as high_value_customers
FROM gold_view
WHERE total_spend > 1000;

-- "Average spending by customer segment"
SELECT 
    CASE WHEN total_spend > 500 THEN 'High'
         ELSE 'Low' END as segment,
    AVG(total_spend) as avg_spend,
    COUNT(*) as customer_count
FROM gold_view
GROUP BY segment;
```

### 5. What is DuckDB?

SQL engine that runs in-memory (no database setup needed).

```python
import duckdb

# Create connection
conn = duckdb.connect(':memory:')

# Register CSV as table
conn.execute("CREATE TABLE data AS SELECT * FROM 'my_file.csv'")

# Query it
result = conn.execute("SELECT * FROM data WHERE value > 100").fetch_df()
```

**Why it's cool:**
- ✓ No installation needed
- ✓ Super fast
- ✓ Works with CSVs directly
- ✓ Returns pandas DataFrames

---

## 🎓 Learning Path

### Week 1: Understanding Concepts
1. Read this file (PROJECT_OVERVIEW.md) → **You are here**
2. Read [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. Run quick_start.sh to see it work

### Week 2: Using the Tools
1. Run [summary_stats.py](SemanticLayer/scripts/summary_stats.py)
2. Try example queries from [EXAMPLE_QUERIES.md](SemanticLayer/EXAMPLE_QUERIES.md)
3. Modify queries to answer your own questions

### Week 3: Understanding Code
1. Read [process_data_spark.py](SemanticLayer/scripts/process_data_spark.py)
2. Understand the transformation steps
3. Try adding custom metrics

### Week 4: Advanced Usage
1. Add your own data files
2. Create custom SQL queries
3. Build dashboards with results
4. Contribute improvements

---

## 💡 Common Questions

### Q: Where does my data come from?
**A:** You place CSV files in `SemanticLayer/data/raw/`:
- `customers_raw.csv`
- `transactions_raw.csv`

### Q: How do I know if my data is valid?
**A:** Run validation:
```bash
python SemanticLayer/scripts/data_validation.py
```

### Q: Can I use my own queries?
**A:** Yes! See [EXAMPLE_QUERIES.md](SemanticLayer/EXAMPLE_QUERIES.md) and modify them.

### Q: What if I don't have Java?
**A:** Use pandas fallback:
```bash
python SemanticLayer/scripts/process_data.py
```

### Q: How do I add a new metric?
**A:** Edit the aggregation in `process_data_spark.py`:
```python
gold_df = silver_transactions.groupBy("customer_id").agg(
    F.sum("amount").alias("total_spend"),
    F.max("amount").alias("max_transaction"),  # Add this
).collect()
```

### Q: Can I schedule this to run daily?
**A:** Yes! Use cron (Linux/Mac) or Task Scheduler (Windows). Example:
```bash
# Run ETL daily at 2 AM
0 2 * * * cd /path/to/project && python SemanticLayer/scripts/process_data_spark.py
```

---

## 🔗 Related Resources

- [Setup Guide](SETUP_GUIDE.md) – How to install
- [Example Queries](SemanticLayer/EXAMPLE_QUERIES.md) – Query templates
- [Troubleshooting](SemanticLayer/notebooks/TROUBLESHOOTING.ipynb) – Fix issues
- [Contributing](CONTRIBUTING.md) – Help improve

---

## ✅ Checklist: Am I Ready?

- [ ] I understand the 3-layer architecture (raw → silver → gold)
- [ ] I know what ETL means
- [ ] I can run quick_start.sh
- [ ] I've seen the gold_view.csv output
- [ ] I can run one example query
- [ ] I know where to put my own data

**Next:** Go to [SETUP_GUIDE.md](SETUP_GUIDE.md) and run the project!
