# 🚀 START HERE NOW - Quick Test (Option 1)

You're about to test everything in 15 minutes!

---

## 📍 Step 0: Make Sure You're Ready

**Check these first:**

```bash
# 1. Are you in the right directory?
pwd
# Should show: /Users/dattu/AI/AI-Project

# 2. Do you have virtual environment?
ls .venv/
# Should show: bin, lib, pyvenv.cfg, etc.

# 3. Have you installed dependencies?
pip list | grep pyspark
# Should show: pyspark 3.x.x
```

If any of above fail, run:
```bash
cd /Users/dattu/AI/AI-Project
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r SemanticLayer/requirements.txt
```

---

## 🎯 Run Tests Now

Follow this exact sequence:

### **Copy & Paste Block 1: Setup (30 seconds)**

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### **Copy & Paste Block 2: Quick Checks (1 minute)**

```bash
# Verify syntax
python -m py_compile SemanticLayer/scripts/summary_stats.py
python -m py_compile SemanticLayer/scripts/data_validation.py

# Check imports
python -c "import pyspark, pandas, duckdb, pytest; print('✓ OK')"
```

### **Copy & Paste Block 3: Main ETL (5-10 minutes) ⏱️**

```bash
# This is the core test - run the data pipeline
python SemanticLayer/scripts/process_data_spark.py
```

**Watch for:**
```
✓ Loading raw data...
✓ Cleaning to Silver layer...
✓ Writing Silver tables...
✓ Building Gold semantic view...
✓ Metadata updated
```

### **Copy & Paste Block 4: Verify Results (2 minutes)**

```bash
# Check files created
ls -lah SemanticLayer/data/gold/gold_view.csv

# View data
head -5 SemanticLayer/data/gold/gold_view.csv

# Show first few rows with Python
python << 'EOF'
import pandas as pd
df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
print(f"✓ Rows: {len(df)}")
print(f"✓ Columns: {list(df.columns)}")
print("\nData:")
print(df.head(3).to_string())
EOF
```

### **Copy & Paste Block 5: Data Quality (2 minutes)**

```bash
# Validate data
python SemanticLayer/scripts/data_validation.py
```

**Watch for:**
```
✓ File exists
✓ CSV structure
✓ No nulls
...
SUMMARY: 15 passed, 0 failed
```

### **Copy & Paste Block 6: Summary Stats (1 minute)**

```bash
# Show key metrics
python SemanticLayer/scripts/summary_stats.py
```

### **Copy & Paste Block 7: SQL Queries (1 minute)**

```bash
# Run example queries
python SemanticLayer/scripts/sql_layer.py
```

### **Copy & Paste Block 8: Final Tests (2 minutes)**

```bash
# Run all automated tests
pytest -v SemanticLayer/tests/
```

**Watch for:**
```
4 passed in 2.34s
```

---

## ✅ Success Checklist

After running all blocks, verify:

- [ ] Block 3 (ETL) had no errors
- [ ] Block 4: gold_view.csv has rows > 0
- [ ] Block 5: Data validation shows "0 failed"
- [ ] Block 6: Summary stats display numbers
- [ ] Block 7: SQL queries show results
- [ ] Block 8: Tests show "4 passed"

**If all ✅, you're done!**

---

## 🚀 Ready to Push?

```bash
git add .
git commit -m "[DOCS] Add comprehensive documentation & automation"
git push origin feature/semantic-layer-pyspark-sql-tests
```

Then create Pull Request on GitHub!

---

## 🆘 Troubleshooting Quick Fixes

**"Java not found"** (Block 3)
```bash
python SemanticLayer/scripts/process_data.py  # Pandas fallback
```

**"Module not found"** (Block 2)
```bash
pip install -r SemanticLayer/requirements.txt
```

**"gold_view.csv is empty"** (Block 4)
→ Re-run Block 3, check error output

**"Test failed"** (Block 8)
```bash
pytest -vv SemanticLayer/tests/  # Get more details
```

---

## 📚 Need More Help?

- **Full guide:** See GUIDED_TEST_EXECUTION.md
- **Issues?** See TROUBLESHOOTING.ipynb
- **Understanding project?** See PROJECT_OVERVIEW.md

---

**Let's go! Start with Block 1 above! 🎯**
