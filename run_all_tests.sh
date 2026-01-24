#!/bin/bash

set -e  # Exit on error

echo "=========================================="
echo "COMPREHENSIVE TEST SUITE"
echo "=========================================="
echo "This script will test all components"
echo "Expected time: 5-10 minutes"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

passed=0
failed=0

# Helper functions
test_section() {
    echo -e "\n${YELLOW}[TEST $1]${NC} $2"
    echo "─────────────────────────────────────"
}

test_pass() {
    echo -e "${GREEN}✓ PASSED${NC}: $1"
    ((passed++))
}

test_fail() {
    echo -e "${RED}✗ FAILED${NC}: $1"
    ((failed++))
}

# ============================================
# PHASE 1: Environment Check
# ============================================
test_section "1.1" "Checking Python version"
python_version=$(python --version 2>&1)
if [[ $python_version == *"3."* ]]; then
    test_pass "Python version: $python_version"
else
    test_fail "Invalid Python version: $python_version"
fi

# ============================================
# PHASE 2: Syntax Check
# ============================================
test_section "2.1" "Checking Python syntax"
if python -m py_compile SemanticLayer/scripts/summary_stats.py 2>/dev/null; then
    test_pass "summary_stats.py syntax"
else
    test_fail "summary_stats.py syntax"
fi

if python -m py_compile SemanticLayer/scripts/data_validation.py 2>/dev/null; then
    test_pass "data_validation.py syntax"
else
    test_fail "data_validation.py syntax"
fi

# ============================================
# PHASE 3: Import Check
# ============================================
test_section "3.1" "Checking module imports"
if python -c "import pyspark" 2>/dev/null; then
    test_pass "pyspark import"
else
    test_fail "pyspark import"
fi

if python -c "import pandas" 2>/dev/null; then
    test_pass "pandas import"
else
    test_fail "pandas import"
fi

if python -c "import duckdb" 2>/dev/null; then
    test_pass "duckdb import"
else
    test_fail "duckdb import"
fi

# ============================================
# PHASE 4: ETL Pipeline
# ============================================
test_section "4.1" "Running PySpark ETL"
if python SemanticLayer/scripts/process_data_spark.py > /tmp/etl.log 2>&1; then
    test_pass "ETL pipeline executed"
    
    # Check output files
    if [ -f "SemanticLayer/data/silver/customers_silver.csv" ]; then
        test_pass "customers_silver.csv created"
    else
        test_fail "customers_silver.csv not found"
    fi
    
    if [ -f "SemanticLayer/data/gold/gold_view.csv" ]; then
        test_pass "gold_view.csv created"
    else
        test_fail "gold_view.csv not found"
    fi
    
    if [ -f "SemanticLayer/data/metadata.json" ]; then
        test_pass "metadata.json created"
    else
        test_fail "metadata.json not found"
    fi
else
    test_fail "ETL pipeline execution"
    tail -20 /tmp/etl.log
fi

# ============================================
# PHASE 5: Data Validation
# ============================================
test_section "5.1" "Running data validation"
if python SemanticLayer/scripts/data_validation.py > /tmp/validation.log 2>&1; then
    if grep -q "failed.*0" /tmp/validation.log; then
        test_pass "Data validation checks"
    else
        test_fail "Data validation found issues"
        tail -10 /tmp/validation.log
    fi
else
    test_fail "Data validation script"
    tail -10 /tmp/validation.log
fi

# ============================================
# PHASE 6: Summary Statistics
# ============================================
test_section "6.1" "Running summary statistics"
if python SemanticLayer/scripts/summary_stats.py > /tmp/stats.log 2>&1; then
    if grep -q "Summary Statistics" /tmp/stats.log; then
        test_pass "Summary statistics generation"
    else
        test_fail "Summary statistics output format"
    fi
else
    test_fail "Summary statistics script"
    tail -10 /tmp/stats.log
fi

# ============================================
# PHASE 7: SQL Layer
# ============================================
test_section "7.1" "Running SQL queries"
if python SemanticLayer/scripts/sql_layer.py > /tmp/sql.log 2>&1; then
    if grep -q "customer_id" /tmp/sql.log; then
        test_pass "SQL queries execution"
    else
        test_fail "SQL queries output format"
    fi
else
    test_fail "SQL layer script"
    tail -10 /tmp/sql.log
fi

# ============================================
# PHASE 8: Pytest
# ============================================
test_section "8.1" "Running pytest"
if pytest -q SemanticLayer/tests/ > /tmp/pytest.log 2>&1; then
    test_pass "All pytest tests"
    # Count passed tests
    test_count=$(grep -c "PASSED" /tmp/pytest.log || echo "unknown")
    echo "         Tests passed: $test_count"
else
    test_fail "Some pytest tests failed"
    tail -20 /tmp/pytest.log
fi

# ============================================
# PHASE 9: File Existence
# ============================================
test_section "9.1" "Checking documentation files"
doc_files=(
    "PROJECT_OVERVIEW.md"
    "LEARNING_PATH.md"
    "INPUT_OUTPUT_GUIDE.md"
    "CONTRIBUTING.md"
    "GIT_WORKFLOW.md"
    "CHANGELOG.md"
)

for file in "${doc_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        test_pass "$file exists ($size bytes)"
    else
        test_fail "$file missing"
    fi
done

# ============================================
# PHASE 10: Gold View Data Check
# ============================================
test_section "10.1" "Checking gold_view.csv data"
if [ -f "SemanticLayer/data/gold/gold_view.csv" ]; then
    row_count=$(tail -n +2 SemanticLayer/data/gold/gold_view.csv | wc -l)
    if [ "$row_count" -gt 0 ]; then
        test_pass "gold_view.csv has data ($row_count rows)"
    else
        test_fail "gold_view.csv is empty"
    fi
else
    test_fail "gold_view.csv not found"
fi

# ============================================
# Summary
# ============================================
echo -e "\n=========================================="
echo "TEST RESULTS SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $passed${NC}"
echo -e "${RED}Failed: $failed${NC}"
total=$((passed + failed))
echo "Total:  $total"

echo -e "\n=========================================="
if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED - READY TO PUSH${NC}"
    echo "=========================================="
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED - DO NOT PUSH YET${NC}"
    echo "=========================================="
    echo ""
    echo "Troubleshooting:"
    echo "  • Check error messages above"
    echo "  • See TEST_BEFORE_PUSH.md for fixes"
    echo "  • See TROUBLESHOOTING.ipynb for help"
    exit 1
fi
