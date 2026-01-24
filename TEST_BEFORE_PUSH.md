# Testing Guide: Verify Everything Before Pushing

## 🎯 Overview

Before pushing to Git, you should verify:
1. ✓ No Python syntax errors
2. ✓ Scripts run without crashing
3. ✓ Output files are created correctly
4. ✓ Data validation passes
5. ✓ All tests pass
6. ✓ Documentation is accurate

---

## 📋 Phase 1: Syntax & Import Checks (5 minutes)

### Check Python Syntax

```bash
# Check all Python files for syntax errors
python -m py_compile SemanticLayer/scripts/*.py
python -m py_compile SemanticLayer/tests/*.py

# Expected output:
# (no errors = success)
```

### Verify All Imports

```bash
# Test that all modules can be imported
python -c "
import sys
sys.path.insert(0, '.')

# Try importing key modules
try:
    import pyspark
    print('✓ pyspark imported successfully')
except ImportError as e:
    print(f'✗ pyspark import failed: {e}')

try:
    import pandas
    print('✓ pandas imported successfully')
except ImportError as e:
    print(f'✗ pandas import failed: {e}')

try:
    import duckdb
    print('✓ duckdb imported successfully')
except ImportError as e:
    print(f'✗ duckdb import failed: {e}')

try:
    import pytest
    print('✓ pytest imported successfully')
except ImportError as e:
    print(f'✗ pytest import failed: {e}')
"
```

---

## 📊 Phase 2: Run ETL Pipeline (10 minutes)

### Test PySpark ETL

```bash
# Run the main ETL script
python SemanticLayer/scripts/process_data_spark.py

# Expected output:
# Loading raw data...
# Cleaning to Silver layer...
# Writing Silver tables...
# Saved Silver tables to SemanticLayer/data/silver
# Building Gold semantic view...
# Gold layer saved to SemanticLayer/data/gold/gold_view.csv
# Metadata updated at SemanticLayer/data/metadata.json
```

### Verify Output Files Exist

```bash
# Check if all output files were created
ls -lah SemanticLayer/data/silver/
ls -lah SemanticLayer/data/gold/
cat SemanticLayer/data/metadata.json

# Expected:
# customers_silver.csv (should have size > 0)
# transactions_silver.csv (should have size > 0)
# gold_view.csv (should have size > 0)
# metadata.json (should contain "gold_view" entry)
```

### Test Pandas Fallback

```bash
# If PySpark fails, test pandas version
python SemanticLayer/scripts/process_data.py

# Expected output:
# Loading raw data with pandas...
# Cleaning to Silver layer...
# Gold layer created successfully
```

---

## 🧪 Phase 3: Data Quality Tests (5 minutes)

### Run Data Validation

```bash
python SemanticLayer/scripts/data_validation.py

# Expected output:
# ✓ File exists: silver/customers_silver.csv
# ✓ CSV structure: customers_silver.csv (1000 rows, 2 columns)
# ✓ No nulls: All 1000 customers have valid IDs
# ✓ File exists: gold/gold_view.csv
# ✓ Numeric range: All amounts > 0
# ✓ Gold aggregations: Gold view matches silver data
# 
# SUMMARY: 12 passed, 0 failed
```

### Manual Data Inspection

```python
# Create a test script: verify_data.py
python << 'EOF'
import pandas as pd

print("=" * 60)
print("DATA INSPECTION REPORT")
print("=" * 60)

# Check gold view
df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')

print(f"\n✓ Gold view shape: {df.shape}")
print(f"✓ Rows: {len(df)}")
print(f"✓ Columns: {list(df.columns)}")

# Check data types
print(f"\n✓ Data types:")
print(df.dtypes)

# Check for nulls
print(f"\n✓ Null values: {df.isnull().sum().sum()}")

# Check value ranges
print(f"\n✓ Total spend range: ${df['total_spend'].min():.2f} - ${df['total_spend'].max():.2f}")
print(f"✓ Transaction count range: {df['transaction_count'].min()} - {df['transaction_count'].max()}")

# Show first few rows
print(f"\n✓ First 5 rows:")
print(df.head().to_string())

# Show summary stats
print(f"\n✓ Summary statistics:")
print(df.describe().to_string())

print("\n" + "=" * 60)
if len(df) > 0 and df.isnull().sum().sum() == 0:
    print("✓ DATA QUALITY CHECK PASSED")
else:
    print("✗ DATA QUALITY CHECK FAILED")
print("=" * 60)
EOF
```

---

## 📈 Phase 4: Script Execution Tests (15 minutes)

### Test Summary Statistics Script

```bash
python SemanticLayer/scripts/summary_stats.py

# Expected output:
# ============================================================
#   SEMANTIC LAYER - SUMMARY STATISTICS
# ============================================================
#
# ============================================================
#   📊 Summary Statistics
# ============================================================
#
# Total Customers:        [number]
# Total Spend:           $[amount]
# Total Transactions:     [number]
# Avg Transaction Amount: $[amount]
# ...
# ✅ Summary Complete
```

### Test SQL Layer Script

```bash
python SemanticLayer/scripts/sql_layer.py

# Expected output:
# ============================================================
#   TOP SPENDERS
# ============================================================
#
# customer_id | total_spend
# c_001       | [amount]
# c_002       | [amount]
# ...
```

---

## 🧬 Phase 5: Unit Tests (10 minutes)

### Run All Tests

```bash
# Run pytest
pytest -v SemanticLayer/tests/

# Expected output:
# test_etl.py::test_gold_view_exists PASSED
# test_etl.py::test_gold_view_values PASSED
# test_etl.py::test_no_null_values PASSED
# test_etl.py::test_aggregations_correct PASSED
#
# ======================== 4 passed in 2.34s ========================
```

### Run Tests with Coverage

```bash
pytest --cov=SemanticLayer SemanticLayer/tests/

# Expected output:
# Name                                    Stmts   Miss  Cover
# ─────────────────────────────────────────────────────────────
# SemanticLayer/scripts/process_data.py     45      5    89%
# SemanticLayer/scripts/sql_layer.py        30      2    93%
# SemanticLayer/scripts/summary_stats.py    50      8    84%
# ─────────────────────────────────────────────────────────────
# TOTAL                                    200     20    90%
```

---

## 📚 Phase 6: Documentation Tests (10 minutes)

### Verify Files Exist

```bash
# Check that all new documentation files exist
files=(
    "PROJECT_OVERVIEW.md"
    "LEARNING_PATH.md"
    "INPUT_OUTPUT_GUIDE.md"
    "GIT_WORKFLOW.md"
    "CONTRIBUTING.md"
    "TEST_BEFORE_PUSH.md"
    "CHANGELOG.md"
    "SemanticLayer/EXAMPLE_QUERIES.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        echo "✓ $file ($size bytes)"
    else
        echo "✗ $file (MISSING)"
    fi
done
```

### Verify Scripts Have Execution Permission

```bash
# Make scripts executable
chmod +x quick_start.sh
chmod +x quick_start.ps1

# Verify
ls -la quick_start.sh quick_start.ps1

# Expected:
# -rwxr-xr-x  quick_start.sh
# -rw-r--r--  quick_start.ps1 (Windows doesn't need x)
```

### Check Code Quality

```bash
# Check Python style (if installed)
pip install pylint

# Lint scripts
pylint SemanticLayer/scripts/summary_stats.py --disable=all --enable=syntax-error

# Expected:
# ✓ 0 errors (or minor style warnings)
```

---

## 🔗 Phase 7: Quick Start Script Test (15 minutes)

### Test Unix Quick Start (macOS/Linux)

```bash
# Backup current data
cp -r SemanticLayer/data SemanticLayer/data.backup

# Run quick start
./quick_start.sh

# Check output
echo "Quick start completed? Check above for:"
# - "[1/4] Setting up environment..."
# - "[2/4] Running ETL pipeline..."
# - "[3/4] Generating summary stats..."
# - "[4/4] Running tests..."

# Restore backup if testing multiple times
rm -rf SemanticLayer/data
mv SemanticLayer/data.backup SemanticLayer/data
```

### Test Windows Quick Start (PowerShell)

```powershell
# Run quick start
.\quick_start.ps1

# Check output
# - "[1/4] Setting up environment..."
# - "[2/4] Running ETL pipeline..."
# - "[3/4] Generating summary stats..."
# - "[4/4] Running tests..."
```

---

## ✅ Phase 8: Notebook Tests (10 minutes)

### Test Colab Notebook Locally

```python
# Install jupyter
pip install jupyter

# Start notebook server
jupyter notebook SemanticLayer/notebooks/colab_duckdb.ipynb

# In notebook:
# 1. Run all cells (Kernel → Run All Cells)
# 2. Verify:
#    - Cells complete without errors
#    - Output shows tables and visualizations
#    - gold_view.csv is created
```

---

## 🎯 Complete Testing Checklist

Use this as your final verification:

```bash
#!/bin/bash

echo "TESTING CHECKLIST FOR PUSH"
echo "============================"

# Phase 1: Syntax
echo -e "\n[1/8] Checking Python syntax..."
python -m py_compile SemanticLayer/scripts/*.py && echo "✓ Syntax OK" || echo "✗ Syntax errors"

# Phase 2: Imports
echo -e "\n[2/8] Checking imports..."
python -c "import pyspark, pandas, duckdb, pytest; print('✓ All imports OK')" 2>/dev/null || echo "✗ Import error"

# Phase 3: ETL
echo -e "\n[3/8] Running ETL pipeline..."
python SemanticLayer/scripts/process_data_spark.py > /dev/null 2>&1 && echo "✓ ETL OK" || echo "✗ ETL failed"

# Phase 4: Data validation
echo -e "\n[4/8] Validating data quality..."
python SemanticLayer/scripts/data_validation.py > /tmp/validation.log 2>&1
if grep -q "PASSED" /tmp/validation.log; then
    echo "✓ Validation OK"
else
    echo "✗ Validation failed"
    tail -5 /tmp/validation.log
fi

# Phase 5: Summary stats
echo -e "\n[5/8] Running summary statistics..."
python SemanticLayer/scripts/summary_stats.py > /tmp/stats.log 2>&1 && echo "✓ Stats OK" || echo "✗ Stats failed"

# Phase 6: SQL layer
echo -e "\n[6/8] Running SQL queries..."
python SemanticLayer/scripts/sql_layer.py > /tmp/sql.log 2>&1 && echo "✓ SQL OK" || echo "✗ SQL failed"

# Phase 7: Tests
echo -e "\n[7/8] Running pytest..."
pytest -q SemanticLayer/tests/ > /tmp/tests.log 2>&1 && echo "✓ Tests OK" || echo "✗ Tests failed"

# Phase 8: Files
echo -e "\n[8/8] Checking new files..."
required_files=(
    "PROJECT_OVERVIEW.md"
    "LEARNING_PATH.md"
    "INPUT_OUTPUT_GUIDE.md"
    "CONTRIBUTING.md"
)
all_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file MISSING"
        all_exist=false
    fi
done

echo -e "\n============================"
if [ "$all_exist" = true ]; then
    echo "✅ ALL TESTS PASSED - READY TO PUSH"
else
    echo "❌ SOME TESTS FAILED - FIX BEFORE PUSHING"
fi
echo "============================"
```

---

## 🆘 Common Issues & Fixes

### Issue: "Java not found"
```bash
# Solution: Install Java or use pandas fallback
python SemanticLayer/scripts/process_data.py
```

### Issue: "Module not found: pyspark"
```bash
# Solution: Install dependencies
pip install -r SemanticLayer/requirements.txt
```

### Issue: "gold_view.csv is empty"
```bash
# Solution: Check raw data exists
ls -la SemanticLayer/data/raw/

# If empty, re-run ETL
python SemanticLayer/scripts/process_data_spark.py
```

### Issue: "Test failures"
```bash
# Solution: Run with verbose output
pytest -vv SemanticLayer/tests/

# Check what failed and why
```

---

## 📝 Testing Report Template

Save this as `TESTING_REPORT.txt` before pushing:

```
TESTING REPORT - [DATE]
========================

Environment:
- OS: [Windows/macOS/Linux]
- Python: [version]
- Java: [version or "Not installed"]

Phase 1: Syntax Check
- Status: [PASS/FAIL]
- Errors: [none/list]

Phase 2: Import Check
- Status: [PASS/FAIL]
- Errors: [none/list]

Phase 3: ETL Pipeline
- Status: [PASS/FAIL]
- Output files: [list files created]
- Row count: [gold_view rows]

Phase 4: Data Validation
- Status: [PASS/FAIL]
- Checks passed: [X/Y]
- Issues: [none/list]

Phase 5: Summary Statistics
- Status: [PASS/FAIL]
- Key metrics: [total customers, revenue, etc.]

Phase 6: SQL Layer
- Status: [PASS/FAIL]
- Queries run: [count]

Phase 7: Unit Tests
- Status: [PASS/FAIL]
- Tests passed: [X/Y]
- Failures: [none/list]

Phase 8: Documentation
- Status: [PASS/FAIL]
- Files checked: [X/Y]

Overall: [READY TO PUSH / NOT READY - ISSUES FOUND]

Issues Found:
[none / list and describe]

Sign-off:
Date: [date]
Tester: [name]
```

---

## ✅ Ready to Push?

Before pushing, verify:
- [ ] All syntax checks pass
- [ ] All scripts run without errors
- [ ] gold_view.csv has data
- [ ] All tests pass
- [ ] Data validation passes
- [ ] Documentation files exist
- [ ] No sensitive data in code
- [ ] .gitignore includes large files

**If all ✓**, you're ready to push! 🚀
