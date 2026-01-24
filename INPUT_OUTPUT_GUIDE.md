# Input & Output Guide: How Data Flows Through the Project

## 🎯 Quick Summary

```
INPUT (Your Data)
    ↓
    └─→ ETL Pipeline
            ↓
         Cleaning
            ↓
         Aggregation
            ↓
OUTPUT (Analysis Ready)
```

---

## 📥 INPUTS: How to Provide Data

### Input Format

The project accepts **CSV files** in `SemanticLayer/data/raw/` directory.

### Required Input Files

#### 1. Customers File: `customers.csv`

**Location:** `SemanticLayer/data/raw/customers.csv`

**Format:**
```
customer_id,email
c_001,alice@example.com
c_002,bob@example.com
c_003,charlie@example.com
```

**Requirements:**
- ✓ Column name: `customer_id` (required)
- ✓ Column name: `email` (required)
- ✓ No duplicate customer IDs
- ✓ CSV format (comma-separated)

**Example with more columns:**
```
customer_id,email,name,signup_date
c_001,alice@example.com,Alice Smith,2023-01-15
c_002,bob@example.com,Bob Jones,2023-02-20
```

#### 2. Transactions File: `transactions.csv`

**Location:** `SemanticLayer/data/raw/transactions.csv`

**Format:**
```
transaction_id,customer_id,amount
t_001,c_001,50.00
t_002,c_001,75.50
t_003,c_002,150.00
```

**Requirements:**
- ✓ Column name: `transaction_id` (unique, required)
- ✓ Column name: `customer_id` (required, must exist in customers)
- ✓ Column name: `amount` (numeric, required)
- ✓ CSV format (comma-separated)

**Example with more columns:**
```
transaction_id,customer_id,amount,transaction_date,product_id
t_001,c_001,50.00,2023-01-20,p_123
t_002,c_001,75.50,2023-02-15,p_456
t_003,c_002,150.00,2023-01-25,p_789
```

---

### How to Create Input Files

#### Option 1: Manually Create CSV

```bash
# Create raw directory
mkdir -p SemanticLayer/data/raw

# Create customers.csv
cat > SemanticLayer/data/raw/customers.csv << 'EOF'
customer_id,email
c_001,alice@example.com
c_002,bob@example.com
c_003,charlie@example.com
EOF

# Create transactions.csv
cat > SemanticLayer/data/raw/transactions.csv << 'EOF'
transaction_id,customer_id,amount
t_001,c_001,50.00
t_002,c_001,75.50
t_003,c_002,150.00
t_004,c_003,100.00
EOF
```

#### Option 2: Export from Your System

**From Excel:**
1. Open workbook
2. Select data
3. Save As → Format: CSV

**From SQL Database:**
```sql
-- Export customers
SELECT customer_id, email 
INTO OUTFILE 'customers.csv'
FROM customers;

-- Export transactions
SELECT transaction_id, customer_id, amount
INTO OUTFILE 'transactions.csv'
FROM transactions;
```

**From Python/Pandas:**
```python
import pandas as pd

# Export customers
customers = pd.DataFrame({
    'customer_id': ['c_001', 'c_002', 'c_003'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
})
customers.to_csv('SemanticLayer/data/raw/customers.csv', index=False)

# Export transactions
transactions = pd.DataFrame({
    'transaction_id': ['t_001', 't_002', 't_003', 't_004'],
    'customer_id': ['c_001', 'c_001', 'c_002', 'c_003'],
    'amount': [50.00, 75.50, 150.00, 100.00]
})
transactions.to_csv('SemanticLayer/data/raw/transactions.csv', index=False)
```

---

### Data Quality: What NOT to Include

❌ **Don't include:**
- Duplicate rows
- Rows with missing required fields (customer_id, amount)
- Negative amounts (unless intentional)
- Invalid email formats (won't break, but noted)
- Extremely large files (>1GB) without optimization

**Example of INVALID data:**
```
transaction_id,customer_id,amount
t_001,c_001,50.00
t_002,,150.00           ← Missing customer_id (INVALID)
t_003,c_003,-50.00      ← Negative amount (INVALID)
t_004,c_004,            ← Missing amount (INVALID)
```

**How to clean before upload:**

```python
import pandas as pd

df = pd.read_csv('transactions.csv')

# Remove rows with missing critical fields
df = df.dropna(subset=['customer_id', 'amount'])

# Remove duplicates
df = df.drop_duplicates(subset=['transaction_id'])

# Remove negative amounts
df = df[df['amount'] > 0]

# Save cleaned
df.to_csv('SemanticLayer/data/raw/transactions.csv', index=False)
```

---

## 📤 OUTPUTS: What You'll Get

After running the ETL pipeline, you'll have:

### Output Layer 1: Silver (Cleaned Data)

**Location:** `SemanticLayer/data/silver/`

**Files:**

#### `customers_silver.csv`
```
customer_id,email
c_001,alice@example.com
c_002,bob@example.com
c_003,charlie@example.com
```

**What changed from raw:**
- ✓ Removed duplicates
- ✓ Removed rows with missing customer_id
- ✓ Standardized format

#### `transactions_silver.csv`
```
transaction_id,customer_id,amount
t_001,c_001,50.00
t_002,c_001,75.50
t_003,c_002,150.00
t_004,c_003,100.00
```

**What changed from raw:**
- ✓ Removed invalid amounts (< 0)
- ✓ Removed transactions for non-existent customers
- ✓ Removed duplicate transactions

---

### Output Layer 2: Gold (Analytics Ready)

**Location:** `SemanticLayer/data/gold/gold_view.csv`

**Format:**
```
customer_id,total_spend,transaction_count,avg_transaction_amount
c_001,125.50,2,62.75
c_002,150.00,1,150.00
c_003,100.00,1,100.00
```

**Column Meanings:**

| Column | Meaning | Example |
|--------|---------|---------|
| `customer_id` | Unique customer identifier | `c_001` |
| `total_spend` | Sum of all transactions for customer | `125.50` |
| `transaction_count` | Number of purchases | `2` |
| `avg_transaction_amount` | Average purchase value | `62.75` |

**How calculated:**
```
total_spend = SUM(transactions.amount) per customer
transaction_count = COUNT(transactions) per customer
avg_transaction_amount = total_spend / transaction_count
```

---

### Output Layer 3: Metadata

**Location:** `SemanticLayer/data/metadata.json`

**Format:**
```json
{
  "tables": {
    "customers_silver": {
      "columns": ["customer_id", "email"],
      "rows": 3,
      "updated": "2024-01-15T10:30:00"
    },
    "transactions_silver": {
      "columns": ["transaction_id", "customer_id", "amount"],
      "rows": 4,
      "updated": "2024-01-15T10:30:00"
    },
    "gold_view": {
      "columns": ["customer_id", "total_spend", "transaction_count", "avg_transaction_amount"],
      "rows": 3,
      "updated": "2024-01-15T10:30:00"
    }
  }
}
```

---

## 🔄 Complete Input → Output Example

### Step 1: Create Input Data

**SemanticLayer/data/raw/customers.csv:**
```
customer_id,email
alice_001,alice@company.com
bob_002,bob@company.com
charlie_003,charlie@company.com
diana_004,diana@company.com
eve_005,eve@company.com
```

**SemanticLayer/data/raw/transactions.csv:**
```
transaction_id,customer_id,amount
tx_001,alice_001,100.00
tx_002,alice_001,50.50
tx_003,alice_001,49.99
tx_004,bob_002,150.00
tx_005,bob_002,150.00
tx_006,charlie_003,75.25
tx_007,diana_004,100.00
tx_008,diana_004,120.00
tx_009,diana_004,110.00
tx_010,eve_005,80.00
```

### Step 2: Run ETL

```bash
python SemanticLayer/scripts/process_data_spark.py
```

### Step 3: See Outputs

**Gold View (SemanticLayer/data/gold/gold_view.csv):**
```
customer_id,total_spend,transaction_count,avg_transaction_amount
alice_001,200.49,3,66.83
bob_002,300.00,2,150.00
charlie_003,75.25,1,75.25
diana_004,330.00,3,110.00
eve_005,80.00,1,80.00
```

### Step 4: Analyze Results

**Question:** *Who are my best customers?*

```python
import pandas as pd

df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')

# Sort by total_spend
top_customers = df.sort_values('total_spend', ascending=False)

print("Top Customers:")
print(top_customers)
```

**Output:**
```
Top Customers:
  customer_id  total_spend  transaction_count  avg_transaction_amount
0    diana_004       330.00                  3                 110.00
1     bob_002        300.00                  2                 150.00
2   alice_001        200.49                  3                  66.83
3  charlie_003        75.25                  1                  75.25
4     eve_005         80.00                  1                  80.00
```

---

## 📊 Output Files Location

```
SemanticLayer/
├── data/
│   ├── raw/                          ← YOUR INPUT FILES
│   │   ├── customers.csv
│   │   └── transactions.csv
│   ├── silver/                       ← CLEANED DATA (INTERMEDIATE)
│   │   ├── customers_silver.csv
│   │   └── transactions_silver.csv
│   ├── gold/                         ← FINAL ANALYSIS DATA (USE THIS!)
│   │   └── gold_view.csv
│   └── metadata.json                 ← DATA SCHEMA INFO
```

---

## 🎯 How to Use Outputs

### Use Case 1: Create Dashboard

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')

# Create visualizations
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Chart 1: Top 5 customers
top_5 = df.nlargest(5, 'total_spend')
axes[0].barh(top_5['customer_id'], top_5['total_spend'])
axes[0].set_title('Top 5 Customers by Spend')

# Chart 2: Transaction frequency distribution
axes[1].hist(df['transaction_count'], bins=10)
axes[1].set_title('Transaction Frequency')

plt.show()
```

### Use Case 2: Export to CRM

```python
import pandas as pd

df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')

# Filter high-value customers
high_value = df[df['total_spend'] > 200]

# Export to Excel for sales team
high_value.to_excel('high_value_customers.xlsx', index=False)
print(f"Exported {len(high_value)} high-value customers to Excel")
```

### Use Case 3: Generate SQL Report

```python
import duckdb

conn = duckdb.connect(':memory:')
conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")

# Generate report
report = conn.execute("""
    SELECT 
        COUNT(*) as total_customers,
        ROUND(SUM(total_spend), 2) as total_revenue,
        ROUND(AVG(total_spend), 2) as avg_customer_value,
        ROUND(AVG(transaction_count), 2) as avg_transactions,
        MAX(total_spend) as max_customer_spend
    FROM gold_view
""").fetch_df()

print(report)
```

---

## ✅ Quality Checklist

Before using outputs:

- [ ] Check gold_view.csv row count matches expected customers
- [ ] Verify total_spend values are reasonable
- [ ] Confirm no NULL values in critical columns
- [ ] Run data_validation.py to verify quality
- [ ] Spot-check a few customers manually

```bash
# Quick verification
python << 'EOF'
import pandas as pd

df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')

print("✓ Row count:", len(df))
print("✓ Columns:", list(df.columns))
print("✓ Data types:", df.dtypes.to_dict())
print("✓ Nulls:", df.isnull().sum().sum())
print("✓ Total revenue:", df['total_spend'].sum())
print("\nFirst few rows:")
print(df.head())
EOF
```

---

## 🔧 Troubleshooting Inputs

### Problem: "No such file or directory"

**Solution:**
```bash
# Check if raw directory exists
ls -la SemanticLayer/data/raw/

# If not, create it
mkdir -p SemanticLayer/data/raw

# Verify files are there
ls -la SemanticLayer/data/raw/
```

### Problem: "Column customer_id not found"

**Solution:**
```bash
# Check actual column names in your CSV
head -1 SemanticLayer/data/raw/customers.csv

# Rename columns if needed
# Using Python:
import pandas as pd
df = pd.read_csv('raw_file.csv')
df = df.rename(columns={'old_name': 'customer_id'})
df.to_csv('SemanticLayer/data/raw/customers.csv', index=False)
```

### Problem: "Empty gold_view.csv"

**Solution:**
```bash
# Check if raw files have data
wc -l SemanticLayer/data/raw/*.csv

# Re-run ETL with verbose output
python -u SemanticLayer/scripts/process_data_spark.py

# Check silver layer (intermediate)
head SemanticLayer/data/silver/transactions_silver.csv
```

---

## 📝 Summary

| Aspect | Details |
|--------|---------|
| **INPUT** | CSV files in `data/raw/` |
| **Process** | ETL pipeline (clean → aggregate) |
| **OUTPUT** | CSV file in `data/gold/` |
| **What's in output** | Customer IDs + spending metrics |
| **How to use** | Queries, dashboards, exports |
| **Validate** | Run data_validation.py |

Next: See [EXAMPLE_QUERIES.md](SemanticLayer/EXAMPLE_QUERIES.md) for query examples!
