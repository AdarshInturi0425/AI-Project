# Learning Path: From Beginner to Advanced

This guide teaches you how to use and understand the SemanticLayer project step-by-step.

---

## 🎯 Learning Objectives

By the end of this guide, you will:
1. Understand the 3-layer data architecture
2. Run the ETL pipeline on sample data
3. Write SQL queries to analyze data
4. Add your own data and metrics
5. Troubleshoot common issues
6. Contribute improvements

---

## 📖 Module 1: Fundamentals (30 minutes)

### 1.1 Core Concepts

**What is a Data Pipeline?**
```
Raw Data → Clean → Aggregate → Analyze
  ↓          ↓       ↓          ↓
Messy    Organized  Summary   Insights
```

**Example: E-commerce**
```
Raw:        100 customers, 5,000 transactions (messy)
Silver:     95 customers, 4,800 valid transactions (clean)
Gold:       95 customers with metrics (aggregated)
Analysis:   Top 10 customers, avg order value, etc.
```

### 1.2 Three Layers

| Layer | Purpose | Format | Example |
|-------|---------|--------|---------|
| **RAW** | Input data | CSV files | `customers_raw.csv` (with errors) |
| **SILVER** | Clean data | CSV files | `customers_silver.csv` (deduplicated) |
| **GOLD** | Business metrics | CSV files | `gold_view.csv` (aggregated) |

### 1.3 Key Technologies

| Tool | Purpose | Why It's Used |
|------|---------|---------------|
| **PySpark** | Process large datasets | Fast, distributed computing |
| **Pandas** | Process small datasets | Simple, flexible |
| **DuckDB** | Query with SQL | No database setup needed |
| **pytest** | Test code | Ensure quality |

---

## 🚀 Module 2: Getting Started (1 hour)

### 2.1 Installation

```bash
# 1. Clone repository
git clone https://github.com/AdarshInturi0425/AI-Project.git
cd AI-Project

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\Activate.ps1  # Windows

# 3. Install dependencies
pip install -r SemanticLayer/requirements.txt

# 4. Verify installation
python -c "import pyspark, pandas, duckdb; print('OK')"
```

### 2.2 Run Your First ETL

```bash
# Run the pipeline
python SemanticLayer/scripts/process_data_spark.py
```

**Expected output:**
```
Loading raw data...
Cleaning to Silver layer...
Writing Silver tables...
Building Gold semantic view...
Metadata updated
✓ Success!
```

### 2.3 Inspect Results

```bash
# View the gold layer (1st 20 rows)
head -20 SemanticLayer/data/gold/gold_view.csv

# Or with Python
python -c "
import pandas as pd
df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
print(df.head())
print(f'Shape: {df.shape}')
print(f'Columns: {list(df.columns)}')
"
```

**Expected output:**
```
  customer_id  total_spend  transaction_count  avg_transaction_amount
0       c_001       145.49                  3                   48.50
1       c_002       300.00                  2                  150.00
2       c_003        75.25                  1                   75.25
```

---

## 📊 Module 3: Data Analysis (1.5 hours)

### 3.1 Summary Statistics

```bash
python SemanticLayer/scripts/summary_stats.py
```

**Study these metrics:**
- Total customers
- Total revenue
- Average transaction value
- Top 5 customers
- Customer segments

### 3.2 Basic SQL Queries

**Question 1: "Who are my top 3 customers?"**

```python
import duckdb

conn = duckdb.connect(':memory:')
conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")

result = conn.execute("""
    SELECT customer_id, total_spend, transaction_count
    FROM gold_view
    ORDER BY total_spend DESC
    LIMIT 3
""").fetch_df()

print(result)
```

**Question 2: "What's my average customer value?"**

```python
result = conn.execute("""
    SELECT 
        AVG(total_spend) as avg_customer_value,
        MIN(total_spend) as min_value,
        MAX(total_spend) as max_value
    FROM gold_view
""").fetch_df()

print(result)
```

**Question 3: "How many transactions per customer (on average)?"**

```python
result = conn.execute("""
    SELECT 
        AVG(transaction_count) as avg_transactions,
        MAX(transaction_count) as max_transactions
    FROM gold_view
""").fetch_df()

print(result)
```

### 3.3 Exercises

**Exercise 1:** Find all customers with more than 5 transactions
```python
result = conn.execute("""
    SELECT * FROM gold_view
    WHERE transaction_count > 5
    ORDER BY transaction_count DESC
""").fetch_df()
print(result)
```

**Exercise 2:** Calculate median spending (hint: use APPROX_QUANTILE)
```python
result = conn.execute("""
    SELECT APPROX_QUANTILE(total_spend, 0.5) as median_spend
    FROM gold_view
""").fetch_df()
print(result)
```

**Exercise 3:** Segment customers into "Low", "Medium", "High"
```python
result = conn.execute("""
    SELECT 
        CASE 
            WHEN total_spend < 100 THEN 'Low'
            WHEN total_spend < 300 THEN 'Medium'
            ELSE 'High'
        END as segment,
        COUNT(*) as customer_count,
        AVG(total_spend) as avg_spend
    FROM gold_view
    GROUP BY segment
    ORDER BY avg_spend DESC
""").fetch_df()
print(result)
```

---

## 🔧 Module 4: Working with Data (2 hours)

### 4.1 Validate Data Quality

```bash
python SemanticLayer/scripts/data_validation.py
```

**Understand these checks:**
- ✓ Files exist and aren't corrupted
- ✓ Required columns present
- ✓ No unexpected NULL values
- ✓ Amounts are positive
- ✓ Gold aggregations match silver data

### 4.2 Add Your Own Data

#### Step 1: Create Input Files

Create `SemanticLayer/data/raw/customers.csv`:
```
customer_id,email
c_001,alice@example.com
c_002,bob@example.com
c_003,charlie@example.com
c_004,diana@example.com
c_005,eve@example.com
```

Create `SemanticLayer/data/raw/transactions.csv`:
```
transaction_id,customer_id,amount
t_001,c_001,50.00
t_002,c_001,75.50
t_003,c_001,49.99
t_004,c_002,150.00
t_005,c_002,150.00
t_006,c_003,75.25
t_007,c_004,100.00
t_008,c_004,120.00
t_009,c_004,110.00
t_010,c_005,80.00
```

#### Step 2: Run ETL

```bash
python SemanticLayer/scripts/process_data_spark.py
```

#### Step 3: Analyze Results

```bash
head -10 SemanticLayer/data/gold/gold_view.csv

# Expected output:
# customer_id,total_spend,transaction_count,avg_transaction_amount
# c_001,175.49,3,58.50
# c_002,300.00,2,150.00
# c_003,75.25,1,75.25
# c_004,330.00,3,110.00
# c_005,80.00,1,80.00
```

### 4.3 Exercise: Analyze Real Scenario

**Scenario:** You're a marketing manager analyzing customer behavior.

```python
import duckdb

conn = duckdb.connect(':memory:')
conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")

# Question 1: Who should we focus on? (High spenders)
high_spenders = conn.execute("""
    SELECT customer_id, total_spend
    FROM gold_view
    WHERE total_spend > (SELECT AVG(total_spend) * 1.5 FROM gold_view)
    ORDER BY total_spend DESC
""").fetch_df()
print("High Spenders:", len(high_spenders))
print(high_spenders)

# Question 2: Who might churn? (One-time buyers)
churn_risk = conn.execute("""
    SELECT customer_id, total_spend, transaction_count
    FROM gold_view
    WHERE transaction_count = 1
""").fetch_df()
print("\nChurn Risk (One-time buyers):", len(churn_risk))
print(churn_risk)

# Question 3: Best targets for upsell? (Regular, low-spend customers)
upsell_targets = conn.execute("""
    SELECT customer_id, total_spend, transaction_count, avg_transaction_amount
    FROM gold_view
    WHERE transaction_count > 2 AND total_spend < 200
    ORDER BY transaction_count DESC
""").fetch_df()
print("\nUpsell Targets:", len(upsell_targets))
print(upsell_targets)
```

---

## 🧪 Module 5: Testing & Quality (1 hour)

### 5.1 Run Tests

```bash
# Run all tests
pytest -v SemanticLayer/tests/

# Run specific test
pytest -v SemanticLayer/tests/test_etl.py::test_gold_view_values
```

### 5.2 Understand Test Results

**Passing test:**
```
test_etl.py::test_gold_view_values PASSED ✓
```

**Failing test:**
```
test_etl.py::test_gold_view_values FAILED ✗
AssertionError: Expected 145.49, got 145.48
```

### 5.3 Write Your Own Test

Create `SemanticLayer/tests/test_my_analysis.py`:

```python
import pandas as pd
import pytest

def test_gold_view_exists():
    """Test that gold view file exists."""
    df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
    assert len(df) > 0, "Gold view should have data"
    assert 'customer_id' in df.columns
    assert 'total_spend' in df.columns

def test_no_negative_spending():
    """Test that all customers have positive spending."""
    df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
    assert (df['total_spend'] > 0).all(), "All customers should have positive spend"

def test_transaction_count_is_integer():
    """Test that transaction count is numeric."""
    df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
    assert df['transaction_count'].dtype in ['int64', 'int32']
```

Run your test:
```bash
pytest -v SemanticLayer/tests/test_my_analysis.py
```

---

## 🎓 Module 6: Understanding the Code (2 hours)

### 6.1 ETL Script Structure

Read `SemanticLayer/scripts/process_data_spark.py` and understand:

```python
# 1. Load raw data
raw_customers = spark.read.csv("data/raw/customers.csv", header=True)
raw_transactions = spark.read.csv("data/raw/transactions.csv", header=True)

# 2. Clean (transform)
customers_clean = raw_customers.dropna()  # Remove nulls
transactions_clean = raw_transactions.filter("amount > 0")  # Only valid amounts

# 3. Save to silver layer
customers_clean.write.csv("data/silver/customers_silver.csv")
transactions_clean.write.csv("data/silver/transactions_silver.csv")

# 4. Aggregate to gold
gold = transactions_clean.groupBy("customer_id").agg({
    "amount": "sum",
    "transaction_id": "count",
    "amount": "avg"
})

# 5. Save gold layer
gold.write.csv("data/gold/gold_view.csv")
```

### 6.2 SQL Query Patterns

**Pattern 1: Filtering**
```sql
SELECT * FROM table
WHERE column > 100
```

**Pattern 2: Aggregating**
```sql
SELECT customer_id, SUM(amount), COUNT(*)
FROM table
GROUP BY customer_id
```

**Pattern 3: Sorting & Limiting**
```sql
SELECT * FROM table
ORDER BY column DESC
LIMIT 10
```

**Pattern 4: Conditionals**
```sql
SELECT 
    CASE 
        WHEN value > 100 THEN 'High'
        ELSE 'Low'
    END as category
FROM table
```

### 6.3 Code Exercise

Modify `process_data_spark.py` to add a new metric:

**Task:** Add "customer_tier" (Gold/Silver/Bronze) to gold view

```python
# In the aggregation section, add:
gold = transactions_clean.groupBy("customer_id").agg(
    F.sum("amount").alias("total_spend"),
    F.count("transaction_id").alias("transaction_count"),
    F.avg("amount").alias("avg_transaction_amount"),
    # Add this new column:
    F.when(F.sum("amount") > 500, "Gold")
     .when(F.sum("amount") > 200, "Silver")
     .otherwise("Bronze").alias("customer_tier")
)
```

Run it and verify the new column exists in gold_view.csv

---

## 🚀 Module 7: Advanced Topics (3 hours)

### 7.1 Performance Optimization

**Question:** Why is my ETL slow?

**Answer:** Check these:

```python
# 1. Data size
df = pd.read_csv('SemanticLayer/data/raw/transactions.csv')
print(f"Size: {len(df)} rows, {df.memory_usage().sum() / 1024**2:.2f} MB")

# 2. Processing time
import time
start = time.time()
# ... do operation ...
end = time.time()
print(f"Time: {end - start:.2f} seconds")

# 3. Missing indexes
df.set_index('customer_id', inplace=True)  # Faster lookups
```

### 7.2 Scaling Up

**Small data (< 1GB):**
```python
import pandas as pd
df = pd.read_csv('large_file.csv')
result = df.groupby('customer_id').agg({'amount': 'sum'})
```

**Large data (1-100GB):**
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ETL").getOrCreate()
df = spark.read.csv('large_file.csv')
result = df.groupBy('customer_id').agg({'amount': 'sum'})
```

### 7.3 Scheduling & Automation

**Run ETL daily:**

**Linux/macOS (cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /home/user/AI-Project && python SemanticLayer/scripts/process_data_spark.py
```

**Windows (Task Scheduler):**
```batch
# Create batch file: etl_daily.bat
cd C:\Users\User\AI-Project
python SemanticLayer\scripts\process_data_spark.py

# Then schedule in Task Scheduler to run daily
```

---

## ✅ Module 8: Capstone Project (4 hours)

### Project Brief

You work for an online retailer. Create a complete analysis of customer behavior:

### Part 1: Data Preparation

1. Create realistic sample data (100 customers, 1,000 transactions)
2. Add some intentional errors (negative amounts, duplicates)
3. Run ETL to clean it

### Part 2: Analysis

Use SQL to answer:
1. Top 10 customers by revenue
2. Customer retention rate (repeat buyers)
3. Average order value by customer
4. Customer lifetime value distribution
5. Predict churn risk (one-time buyers)

### Part 3: Insights

Generate a report:
```
CUSTOMER ANALYSIS REPORT
========================

Key Metrics:
- Total Customers: 100
- Total Revenue: $X
- Average Customer Value: $Y
- Repeat Customer Rate: Z%

Top 5 Customers:
1. [customer_id]: $[amount]
...

Opportunities:
- High-value customers to nurture: [count]
- Churn risk (one-time buyers): [count]
- Upsell targets (repeat, low-spend): [count]
```

### Part 4: Code Quality

1. Run data validation
2. Run tests
3. Document your queries

---

## 📚 Resources

| Resource | Topic | Time |
|----------|-------|------|
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | What is this project? | 15 min |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | How to install | 20 min |
| [EXAMPLE_QUERIES.md](SemanticLayer/EXAMPLE_QUERIES.md) | SQL examples | 30 min |
| [TROUBLESHOOTING.ipynb](SemanticLayer/notebooks/TROUBLESHOOTING.ipynb) | Fix problems | As needed |
| [YouTube: SQL Tutorial](https://www.youtube.com/watch?v=...) | Learn SQL | 2 hours |
| [DuckDB Docs](https://duckdb.org/docs/) | DuckDB reference | As needed |

---

## 🎯 Your Learning Checklist

**Week 1:**
- [ ] Read PROJECT_OVERVIEW.md
- [ ] Run quick_start.sh
- [ ] Understand the 3-layer architecture
- [ ] View gold_view.csv

**Week 2:**
- [ ] Run summary_stats.py
- [ ] Write 3 SQL queries
- [ ] Understand SQL syntax
- [ ] Add your own data

**Week 3:**
- [ ] Run data_validation.py
- [ ] Write a test
- [ ] Run pytest
- [ ] Modify ETL script

**Week 4:**
- [ ] Complete capstone project
- [ ] Create analysis report
- [ ] Share with team
- [ ] Contribute improvements

---

## 🎓 Next Steps After Learning

1. **Deploy to Production** – Setup automated daily runs
2. **Build Dashboard** – Visualize results in Tableau/PowerBI
3. **Add More Metrics** – Custom calculations for your business
4. **Scale Up** – Handle larger datasets
5. **Contribute** – Submit improvements to project

---

Good luck! 🚀
