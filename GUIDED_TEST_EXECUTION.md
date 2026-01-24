# 🧪 GUIDED TEST EXECUTION - Option 1 (Quick Test)

Follow these steps in order. Copy and paste each command exactly.

---

## 📍 Current Location Check

First, verify you're in the right directory:

```bash
pwd
# Should show: /Users/dattu/AI/AI-Project
# If not, run:
cd /Users/dattu/AI/AI-Project
```

---

## ✅ Test 1: Activate Virtual Environment (1 minute)

**Pick your OS:**

### macOS/Linux:
```bash
source .venv/bin/activate
```

### Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt:
```cmd
.\.venv\Scripts\activate.bat
```

**Verify activation:**
```bash
# Should show (.venv) in your prompt
python --version
# Should show Python 3.8+
```

**Expected Output:**
```
(.venv) $ Python 3.9.0
```

**Status:** ✅ PASS / ❌ FAIL
- If PASS → Continue to Test 2
- If FAIL → Run again, or see TROUBLESHOOTING.ipynb

---

## ✅ Test 2: Syntax Check (1 minute)

Check Python files for errors:

```bash
python -m py_compile SemanticLayer/scripts/summary_stats.py
python -m py_compile SemanticLayer/scripts/data_validation.py
```

**Expected Output:**
```
(no output = success)
```

**Status:** ✅ PASS / ❌ FAIL
- If PASS → Continue to Test 3
- If FAIL → Paste error message here and I'll fix it

---

## ✅ Test 3: Check Imports (1 minute)

Verify all required packages are installed:

```bash
python << 'EOF'
import sys
print("Testing imports...")
print("-" * 40)

packages = ['pyspark', 'pandas', 'duckdb', 'pytest']
all_ok = True

for pkg in packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError as e:
        print(f"✗ {pkg}: {e}")
        all_ok = False

print("-" * 40)
if all_ok:
    print("✅ All imports OK!")
else:
    print("❌ Some imports failed")
    print("Run: pip install -r SemanticLayer/requirements.txt")
EOF
```

**Expected Output:**
```
Testing imports...
----------------------------------------
✓ pyspark
✓ pandas
✓ duckdb
✓ pytest
----------------------------------------
✅ All imports OK!
```

**Status:** ✅ PASS / ❌ FAIL
- If PASS → Continue to Test 4
- If FAIL → Run:
  ```bash
  pip install -r SemanticLayer/requirements.txt
  ```
  Then repeat Test 3

---

## ✅ Test 4: Run ETL Pipeline (5-10 minutes) ⏱️

This is the main test. It transforms data from raw → silver → gold:

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

**Status:** ✅ PASS / ❌ FAIL

**If FAIL - Common errors:**

**Error: "Java gateway process exited"**
```bash
# Use pandas fallback instead:
python SemanticLayer/scripts/process_data.py
```

**Error: "No module named 'pyspark'"**
```bash
# Install requirements:
pip install -r SemanticLayer/requirements.txt
# Then retry Test 4
```

**Other errors:**
- Copy the error message
- Check TROUBLESHOOTING.ipynb
- Or share with me

If PASS → Continue to Test 5

---

## ✅ Test 5: Verify Output Files (2 minutes)

Check that ETL created the correct files:

```bash
echo "=== Checking Silver Layer ==="
ls -lah SemanticLayer/data/silver/

echo -e "\n=== Checking Gold Layer ==="
ls -lah SemanticLayer/data/gold/

echo -e "\n=== Checking Metadata ==="
cat SemanticLayer/data/metadata.json
```

**Expected Output:**
```
=== Checking Silver Layer ===
total 16
-rw-r--r--  customers_silver.csv (size > 0)
-rw-r--r--  transactions_silver.csv (size > 0)

=== Checking Gold Layer ===
total 8
-rw-r--r--  gold_view.csv (size > 0)

=== Checking Metadata ===
{
  "tables": {
    "gold_view": {...}
  }
}
```

**Status:** ✅ PASS / ❌ FAIL
- If all files exist with size > 0 → PASS, continue to Test 6
- If any file missing → FAIL, check Test 4 output for errors

---

## ✅ Test 6: Inspect Gold Data (2 minutes)

View the final aggregated data:

```bash
echo "=== Gold View Preview ==="
head -6 SemanticLayer/data/gold/gold_view.csv

echo -e "\n=== Gold View Statistics ==="
python << 'EOF'
import pandas as pd

df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Null values: {df.isnull().sum().sum()}")
print(f"\nData preview:")
print(df.head(3).to_string())
EOF
```

**Expected Output:**
```
=== Gold View Preview ===
customer_id,total_spend,transaction_count,avg_transaction_amount
c_001,145.49,3,48.50
c_002,300.00,2,150.00

=== Gold View Statistics ===
Rows: 5
Columns: ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount']
Null values: 0

Data preview:
  customer_id  total_spend  transaction_count  avg_transaction_amount
0       c_001       145.49                  3                   48.50
1       c_002       300.00                  2                  150.00
2       c_003        75.25                  1                   75.25
```

**Status:** ✅ PASS / ❌ FAIL
- If data looks good (rows > 0, no nulls) → PASS, continue to Test 7
- If data missing or wrong → FAIL, re-run Test 4

---

## ✅ Test 7: Run Data Validation (2 minutes)

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
💰 GOLD LAYER CHECKS
...
SUMMARY: 15 passed, 0 failed out of 15 checks
======================================================================
```

**Status:** ✅ PASS / ❌ FAIL
- If "0 failed" → PASS, continue to Test 8
- If any failed → FAIL, read error messages and fix

---

## ✅ Test 8: Run Summary Statistics (2 minutes)

Calculate business metrics:

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
...

🏆 Top 5 Customers by Total Spend
============================================================

1. c_004
   Total Spend:      $330.00
   Transactions:     3
   Avg per Trans:    $110.00
...
```

**Status:** ✅ PASS / ❌ FAIL
- If output shows metrics → PASS, continue to Test 9
- If error → FAIL, check gold_view.csv exists (Test 6)

---

## ✅ Test 9: Run SQL Queries (2 minutes)

Execute sample queries:

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
...
```

**Status:** ✅ PASS / ❌ FAIL
- If queries execute and show results → PASS, continue to Test 10
- If error → FAIL, check gold_view.csv (Test 6)

---

## ✅ Test 10: Run pytest Tests (3 minutes)

Run automated unit tests:

```bash
pytest -v SemanticLayer/tests/
```

**Expected Output:**
```
SemanticLayer/tests/test_etl.py::test_gold_view_exists PASSED          [ 25%]
SemanticLayer/tests/test_etl.py::test_gold_view_values PASSED          [ 50%]
SemanticLayer/tests/test_etl.py::test_no_null_values PASSED            [ 75%]
SemanticLayer/tests/test_etl.py::test_aggregations_correct PASSED      [100%]

===================== 4 passed in 2.34s =====================
```

**Status:** ✅ PASS / ❌ FAIL
- If "4 passed" → PASS, continue to documentation check
- If any FAILED → FAIL, run with more detail:
  ```bash
  pytest -vv SemanticLayer/tests/
  ```

---

## ✅ Test 11: Verify Documentation (1 minute)

Check all documentation files exist:

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
    "SemanticLayer/scripts/data_validation.py",
    "GUIDED_TEST_EXECUTION.md",
]

print("Documentation Files Check:")
print("=" * 60)

present = 0
missing = 0

for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"✓ {file}")
        present += 1
    else:
        print(f"✗ {file} (MISSING)")
        missing += 1

print("=" * 60)
print(f"Present: {present}/{len(files)}")
print(f"Missing: {missing}/{len(files)}")

if missing == 0:
    print("\n✅ All documentation files present!")
else:
    print(f"\n❌ {missing} files missing")
EOF
```

**Expected Output:**
```
Documentation Files Check:
============================================================
✓ PROJECT_OVERVIEW.md
✓ LEARNING_PATH.md
...
============================================================
Present: 12/12
Missing: 0/12

✅ All documentation files present!
```

**Status:** ✅ PASS / ❌ FAIL
- If all present → PASS

---

## 📋 FINAL SUMMARY

You completed all 11 tests! Now let's verify:

```bash
python << 'EOF'
print("\n" + "=" * 60)
print("FINAL TEST SUMMARY")
print("=" * 60)

tests = [
    "Test 1: Activate virtual environment",
    "Test 2: Python syntax check",
    "Test 3: Module imports",
    "Test 4: ETL pipeline",
    "Test 5: Output files",
    "Test 6: Gold data inspection",
    "Test 7: Data validation",
    "Test 8: Summary statistics",
    "Test 9: SQL queries",
    "Test 10: pytest tests",
    "Test 11: Documentation files"
]

print("\nIf ALL tests above showed ✅ PASS, you're ready!\n")
print("Now run:")
print("")
print("  git add .")
print("  git commit -m '[DOCS] Add comprehensive documentation'")
print("  git push origin feature/semantic-layer-pyspark-sql-tests")
print("")
print("=" * 60)
EOF
```

---

## 🎯 Final Checklist

✅ Mark each test as you complete:

- [ ] Test 1: Virtual environment activated
- [ ] Test 2: Python syntax OK
- [ ] Test 3: Imports working
- [ ] Test 4: ETL pipeline ran successfully
- [ ] Test 5: Output files created
- [ ] Test 6: Gold data looks correct
- [ ] Test 7: Data validation passed
- [ ] Test 8: Summary stats displayed
- [ ] Test 9: SQL queries executed
- [ ] Test 10: All pytest tests passed
- [ ] Test 11: All documentation files present

**If all checked ✅, proceed to push:**

```bash
git add .
git commit -m "[DOCS] Add comprehensive documentation & automation

- PROJECT_OVERVIEW.md: Complete project explanation
- LEARNING_PATH.md: 8-module learning path
- INPUT_OUTPUT_GUIDE.md: Data flow guide
- GIT_WORKFLOW.md: Git workflow guide
- CONTRIBUTING.md: Contribution guidelines
- TEST_BEFORE_PUSH.md: Testing guide
- EXECUTE_TESTS_NOW.md: Test execution guide
- GUIDED_TEST_EXECUTION.md: Step-by-step tests
- CHANGELOG.md: Version history
- Summary scripts: summary_stats.py, data_validation.py
- Quick start scripts: quick_start.sh, quick_start.ps1
- Examples: EXAMPLE_QUERIES.md, colab_duckdb.ipynb
- Automated CI/CD: GitHub Actions workflow"

git push origin feature/semantic-layer-pyspark-sql-tests
```

---

## ✅ Test Completed!

You're ready to push to Git! 🚀
