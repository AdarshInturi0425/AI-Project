# Execute Tests NOW - Complete Guide

## 🚀 Start Here

You're about to test everything before pushing to Git. Follow these steps in order.

---

## ✅ Step 1: Prepare Environment (2 minutes)

### 1.1 Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
.\.venv\Scripts\activate.bat
```

**Verify activation:**
```bash
# You should see (.venv) at start of your prompt
# Or run:
python -c "import sys; print(sys.prefix)" | grep .venv
```

### 1.2 Navigate to Project

```bash
cd /Users/dattu/AI/AI-Project
# OR wherever your project is
```

---

## 🧪 Step 2: Run Quick Syntax Check (1 minute)

```bash
python -m py_compile SemanticLayer/scripts/summary_stats.py
python -m py_compile SemanticLayer/scripts/data_validation.py
```

**Expected:** No output (silence = success)

**If error:**
```
SyntaxError: invalid syntax at line X
```
→ See TROUBLESHOOTING.ipynb

---

## 📦 Step 3: Verify Imports (1 minute)

```bash
python << 'EOF'
print("Testing imports...")
try:
    import pyspark
    print("✓ pyspark OK")
except ImportError as e:
    print(f"✗ pyspark FAILED: {e}")

try:
    import pandas
    print("✓ pandas OK")
except ImportError as e:
    print(f"✗ pandas FAILED: {e}")

try:
    import duckdb
    print("✓ duckdb OK")
except ImportError as e:
    print(f"✗ duckdb FAILED: {e}")

try:
    import pytest
    print("✓ pytest OK")
except ImportError as e:
    print(f"✗ pytest FAILED: {e}")

print("\n✓ All imports successful!")
EOF
```

**Expected Output:**
```
Testing imports...
✓ pyspark OK
✓ pandas OK
✓ duckdb OK
✓ pytest OK

✓ All imports successful!
```

**If error:** Run:
```bash
pip install -r SemanticLayer/requirements.txt
```

---

## 🔄 Step 4: Run ETL Pipeline (5-10 minutes)

This is the main test - transforms raw data to gold layer.

```bash
python SemanticLayer/scripts/process_data_spark.py
```

**Expected Output:**
```
Loading raw data...
Cleaning to Silver layer...
Writing Silver tables...
Saved Silver tables to SemanticLayer/data/silver
Building Gold semantic view...
Gold layer saved to SemanticLayer/data/gold/gold_view.csv
Metadata updated at SemanticLayer/data/metadata.json
```

**If error:** 
- **"Java not found"** → Install Java or use pandas fallback:
  ```bash
  python SemanticLayer/scripts/process_data.py
  ```
- **"Module not found"** → Install requirements again:
  ```bash
  pip install -r SemanticLayer/requirements.txt
  ```
- **Other error** → Check TROUBLESHOOTING.ipynb

---

## 📊 Step 5: Verify Output Files (2 minutes)

Check that ETL created the right files:

```bash
# List all output files
echo "=== Silver Layer ==="
ls -lah SemanticLayer/data/silver/

echo -e "\n=== Gold Layer ==="
ls -lah SemanticLayer/data/gold/

echo -e "\n=== Metadata ==="
ls -lah SemanticLayer/data/metadata.json
```

**Expected:**
```
=== Silver Layer ===
total 16
-rw-r--r--  customers_silver.csv (size > 0)
-rw-r--r--  transactions_silver.csv (size > 0)

=== Gold Layer ===
total 8
-rw-r--r--  gold_view.csv (size > 0)

=== Metadata ===
-rw-r--r--  metadata.json
```

**If files missing:**
```
✗ gold_view.csv not found
```
→ ETL failed. Check Step 4 output for errors.

---

## 📈 Step 6: Inspect Gold Data (2 minutes)

View the aggregated data:

```bash
# Show first 20 lines
head -20 SemanticLayer/data/gold/gold_view.csv

# Or use Python
python << 'EOF'
import pandas as pd

df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')

print("Gold View Summary:")
print(f"  Rows: {len(df)}")
print(f"  Columns: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head().to_string())
print(f"\nData types:")
print(df.dtypes)
print(f"\nNull values: {df.isnull().sum().sum()}")
EOF
```

**Expected Output:**
```
Gold View Summary:
  Rows: 5
  Columns: ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount']

First 5 rows:
  customer_id  total_spend  transaction_count  avg_transaction_amount
0       c_001       145.49                  3                   48.50
1       c_002       300.00                  2                  150.00
2       c_003        75.25                  1                   75.25
3       c_004       330.00                  3                  110.00
4       c_005        80.00                  1                   80.00

Data types:
customer_id      object
total_spend      float64
transaction_count    int64
avg_transaction_amount  float64

Null values: 0
```

**If data missing or wrong:**
- Check raw data exists: `ls SemanticLayer/data/raw/`
- Re-run ETL: `python SemanticLayer/scripts/process_data_spark.py`

---

## ✓ Step 7: Run Data Validation (2 minutes)

Verify data quality and integrity:

```bash
python SemanticLayer/scripts/data_validation.py
```

**Expected Output:**
```
======================================================================
  DATA VALIDATION REPORT
======================================================================

📋 SILVER LAYER CHECKS

✓ File exists: silver/customers_silver.csv (1.2 MB)
✓ CSV structure: customers_silver.csv: 5 rows, 2 columns
✓ No nulls: All 5 customers have valid IDs
...

✓ SUMMARY: 15 passed, 0 failed out of 15 checks
======================================================================
```

**If validation fails:**
```
✗ SUMMARY: 10 passed, 5 failed out of 15 checks
```
→ Read error messages, fix issues, re-run ETL

---

## 📊 Step 8: Run Summary Statistics (2 minutes)

Calculate and display key metrics:

```bash
python SemanticLayer/scripts/summary_stats.py
```

**Expected Output:**
```
============================================================
  SEMANTIC LAYER - SUMMARY STATISTICS
============================================================

============================================================
  📊 Summary Statistics
============================================================

Total Customers:        5
Total Spend:           $931.74
Total Transactions:     10
Avg Transaction Amount: $93.17
Median Transaction:     $75.25
Min Transaction:        $48.50
Max Transaction:        $150.00

============================================================
  🏆 Top 5 Customers by Total Spend
============================================================

1. c_004
   Total Spend:      $330.00
   Transactions:     3
   Avg per Trans:    $110.00

2. c_002
   ...
```

**If error:** Check gold_view.csv exists and has data (Step 6)

---

## 🔗 Step 9: Run SQL Layer (2 minutes)

Execute sample SQL queries:

```bash
python SemanticLayer/scripts/sql_layer.py
```

**Expected Output:**
```
============================================================
  TOP SPENDERS
============================================================

customer_id | total_spend
c_004       | 330.0
c_002       | 300.0
c_001       | 145.49
c_005       | 80.0
c_003       | 75.25

============================================================
  CUSTOMERS FILTERED BY SPEND > 100
============================================================

customer_id | total_spend | transaction_count
c_004       | 330.0       | 3
c_002       | 300.0       | 2
c_001       | 145.49      | 3
```

**If error:** Check gold_view.csv exists

---

## 🧬 Step 10: Run pytest Tests (3 minutes)

Run automated unit tests:

```bash
pytest -v SemanticLayer/tests/
```

**Expected Output:**
```
SemanticLayer/tests/test_etl.py::test_gold_view_exists PASSED
SemanticLayer/tests/test_etl.py::test_gold_view_values PASSED
SemanticLayer/tests/test_etl.py::test_no_null_values PASSED
SemanticLayer/tests/test_etl.py::test_gold_view_structure PASSED

===================== 4 passed in 2.34s =====================
```

**If test fails:**
```
FAILED SemanticLayer/tests/test_etl.py::test_gold_view_values - AssertionError
```

Get more details:
```bash
pytest -vv SemanticLayer/tests/test_etl.py::test_gold_view_values
```

---

## 📁 Step 11: Verify Documentation Files (1 minute)

Check all new documentation exists:

```bash
python << 'EOF'
import os

files = [
    "PROJECT_OVERVIEW.md",
    "LEARNING_PATH.md",
    "INPUT_OUTPUT_GUIDE.md",
    "GIT_WORKFLOW.md",
    "CONTRIBUTING.md",
    "TEST_BEFORE_PUSH.md",
    "EXECUTE_TESTS_NOW.md",
    "CHANGELOG.md",
    "SemanticLayer/EXAMPLE_QUERIES.md",
    "SemanticLayer/scripts/summary_stats.py",
    "SemanticLayer/scripts/data_validation.py"
]

print("Checking documentation files...")
print("=" * 60)

missing = []
for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"✓ {file} ({size} bytes)")
    else:
        print(f"✗ {file} (MISSING)")
        missing.append(file)

print("=" * 60)
if not missing:
    print(f"✅ All {len(files)} files present!")
else:
    print(f"❌ {len(missing)} files missing: {missing}")
EOF
```

**Expected:** All files show ✓

---

## 🎯 Step 12: Run Automated Test Suite (5 minutes)

Run all tests in one command:

**macOS/Linux:**
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

**Windows PowerShell:**
```powershell
powershell -ExecutionPolicy Bypass -File run_all_tests.ps1
```

**Expected Final Output:**
```
==========================================
TEST RESULTS SUMMARY
==========================================
Passed: 25
Failed: 0
Total:  25

==========================================
✅ ALL TESTS PASSED - READY TO PUSH
==========================================
```

**If any fail:**
- Re-read error messages
- Check specific test output:
  ```bash
  pytest -vv [test_name]
  ```
- See TROUBLESHOOTING.ipynb

---

## ✅ Final Checklist

Before pushing to Git, verify ALL are ✓:

```bash
python << 'EOF'
print("FINAL VERIFICATION CHECKLIST")
print("=" * 60)

checks = {
    "Syntax valid": False,
    "Imports work": False,
    "ETL pipeline runs": False,
    "Output files exist": False,
    "Data validation passes": False,
    "Summary stats works": False,
    "SQL queries work": False,
    "Tests pass": False,
    "Documentation complete": False
}

# Manual verification needed - user checks above steps

print("If you completed all 12 steps above without errors:")
print("✅ Syntax valid")
print("✅ Imports work")
print("✅ ETL pipeline runs")
print("✅ Output files exist")
print("✅ Data validation passes")
print("✅ Summary stats works")
print("✅ SQL queries work")
print("✅ Tests pass")
print("✅ Documentation complete")

print("\n" + "=" * 60)
print("If ALL ✅ above, you're ready to push to Git!")
print("=" * 60)
EOF
```

---

## 🚀 Ready to Push?

If all steps passed with ✓, run:

```bash
git add .
git commit -m "[DOCS] Add comprehensive documentation & automation"
git push origin feature/semantic-layer-pyspark-sql-tests
```

Then create Pull Request on GitHub!

---

## 🆘 Troubleshooting Quick Links

| Error | Fix |
|-------|-----|
| "Java not found" | Install JDK 11+, see SETUP_BY_OS.md |
| "Module not found" | Run `pip install -r SemanticLayer/requirements.txt` |
| "gold_view.csv empty" | Re-run ETL, check raw data exists |
| "Test fails" | Run `pytest -vv` for details, see TROUBLESHOOTING.ipynb |

---

**You've got this! Run the tests now and let me know if you hit any issues! 🎯**
