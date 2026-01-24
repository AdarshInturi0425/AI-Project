# Step-by-Step Testing Guide

## 🎯 Quick Testing (5 minutes)

Follow these steps in order:

### Step 1: Activate Virtual Environment

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.\.venv\Scripts\activate.bat
```

### Step 2: Run Automated Test Suite

**macOS/Linux:**
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

**Windows PowerShell:**
```powershell
powershell -ExecutionPolicy Bypass -File run_all_tests.ps1
```

### Step 3: Review Results

Look for:
```
✅ ALL TESTS PASSED - READY TO PUSH
```

If you see this, you're good to push! ✨

---

## 🔍 Detailed Testing (15 minutes)

If quick test failed, debug step-by-step:

### Test 1: Check Syntax

```bash
python -m py_compile SemanticLayer/scripts/*.py
```

**Expected:** No output (or success message)

**If error:** Fix the Python syntax error shown

### Test 2: Check Imports

```bash
python -c "import pyspark, pandas, duckdb; print('✓ All OK')"
```

**Expected:** `✓ All OK`

**If error:** Install missing package:
```bash
pip install -r SemanticLayer/requirements.txt
```

### Test 3: Run ETL

```bash
python SemanticLayer/scripts/process_data_spark.py
```

**Expected:** Output like:
```
Loading raw data...
Cleaning to Silver layer...
Writing Silver tables...
Building Gold semantic view...
✓ Success!
```

**If error:** See [TROUBLESHOOTING.ipynb](SemanticLayer/notebooks/TROUBLESHOOTING.ipynb)

### Test 4: Check Output Files

```bash
# List output files
ls -la SemanticLayer/data/gold/
ls -la SemanticLayer/data/silver/

# View gold layer
head -10 SemanticLayer/data/gold/gold_view.csv

# Check metadata
cat SemanticLayer/data/metadata.json
```

**Expected:** 
- Files exist with size > 0
- gold_view.csv has customer data
- metadata.json contains valid JSON

### Test 5: Run Data Validation

```bash
python SemanticLayer/scripts/data_validation.py
```

**Expected:** Multiple ✓ marks and "PASSED" at end

**If fails:** Run with verbose output:
```bash
python -u SemanticLayer/scripts/data_validation.py
```

### Test 6: Run Summary Statistics

```bash
python SemanticLayer/scripts/summary_stats.py
```

**Expected:** Key metrics displayed

### Test 7: Run Tests

```bash
pytest -v SemanticLayer/tests/
```

**Expected:** All tests show "PASSED"

**If fails:**
```bash
pytest -vv SemanticLayer/tests/  # More detail
```

---

## 📋 Checklist Before Pushing

Before running `git push`, verify:

- [ ] `python -m py_compile` runs with no errors
- [ ] `python -c "import pyspark, pandas, duckdb; print('OK')"` outputs "OK"
- [ ] ETL script completes without errors
- [ ] gold_view.csv exists and has data
- [ ] Data validation passes all checks
- [ ] Summary statistics display correctly
- [ ] All pytest tests pass
- [ ] Documentation files exist (check count: 12 files)
- [ ] No Python syntax errors

---

## ✅ Final Sign-off

When you can answer YES to all:

1. ✅ All syntax checks pass?
2. ✅ All imports work?
3. ✅ ETL pipeline runs?
4. ✅ Output files created?
5. ✅ Data validation passes?
6. ✅ All tests pass?
7. ✅ Documentation files exist?
8. ✅ Quick start scripts work?

**Then you're ready to push!** 🚀

---

## 🚀 Ready? Push with:

```bash
git add .
git commit -m "[DOCS] Add comprehensive documentation & automation"
git push origin feature/semantic-layer-pyspark-sql-tests

# Or to master (solo only):
git push origin master
```

---

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for detailed push instructions.
