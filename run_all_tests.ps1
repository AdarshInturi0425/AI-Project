# Comprehensive test suite for Windows
# Run as: powershell -ExecutionPolicy Bypass -File run_all_tests.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "COMPREHENSIVE TEST SUITE (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Expected time: 5-10 minutes`n"

$passed = 0
$failed = 0

function Test-Section {
    param([string]$number, [string]$title)
    Write-Host "`n[TEST $number] $title" -ForegroundColor Yellow
    Write-Host "─────────────────────────────────────"
}

function Test-Pass {
    param([string]$message)
    Write-Host "✓ PASSED: $message" -ForegroundColor Green
    $global:passed++
}

function Test-Fail {
    param([string]$message)
    Write-Host "✗ FAILED: $message" -ForegroundColor Red
    $global:failed++
}

# ============================================
# PHASE 1: Python Version
# ============================================
Test-Section "1.1" "Checking Python version"
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "3\.") {
    Test-Pass "Python version: $pythonVersion"
} else {
    Test-Fail "Invalid Python version: $pythonVersion"
}

# ============================================
# PHASE 2: Syntax Check
# ============================================
Test-Section "2.1" "Checking Python syntax"
$result = python -m py_compile SemanticLayer/scripts/summary_stats.py 2>&1
if ($?) { Test-Pass "summary_stats.py syntax" } else { Test-Fail "summary_stats.py syntax" }

$result = python -m py_compile SemanticLayer/scripts/data_validation.py 2>&1
if ($?) { Test-Pass "data_validation.py syntax" } else { Test-Fail "data_validation.py syntax" }

# ============================================
# PHASE 3: Imports
# ============================================
Test-Section "3.1" "Checking module imports"
$result = python -c "import pyspark" 2>&1
if ($?) { Test-Pass "pyspark import" } else { Test-Fail "pyspark import" }

$result = python -c "import pandas" 2>&1
if ($?) { Test-Pass "pandas import" } else { Test-Fail "pandas import" }

$result = python -c "import duckdb" 2>&1
if ($?) { Test-Pass "duckdb import" } else { Test-Fail "duckdb import" }

# ============================================
# PHASE 4: ETL Pipeline
# ============================================
Test-Section "4.1" "Running PySpark ETL"
$result = python SemanticLayer/scripts/process_data_spark.py 2>&1
if ($?) {
    Test-Pass "ETL pipeline executed"
    
    if (Test-Path "SemanticLayer/data/silver/customers_silver.csv") {
        Test-Pass "customers_silver.csv created"
    } else {
        Test-Fail "customers_silver.csv not found"
    }
    
    if (Test-Path "SemanticLayer/data/gold/gold_view.csv") {
        Test-Pass "gold_view.csv created"
    } else {
        Test-Fail "gold_view.csv not found"
    }
} else {
    Test-Fail "ETL pipeline execution"
}

# ============================================
# PHASE 5: Data Validation
# ============================================
Test-Section "5.1" "Running data validation"
$result = python SemanticLayer/scripts/data_validation.py 2>&1
if ($?) {
    if ($result -match "failed.*0") {
        Test-Pass "Data validation checks"
    } else {
        Test-Fail "Data validation found issues"
    }
} else {
    Test-Fail "Data validation script"
}

# ============================================
# PHASE 6: Summary Statistics
# ============================================
Test-Section "6.1" "Running summary statistics"
$result = python SemanticLayer/scripts/summary_stats.py 2>&1
if ($?) {
    if ($result -match "Summary Statistics") {
        Test-Pass "Summary statistics generation"
    } else {
        Test-Fail "Summary statistics output format"
    }
} else {
    Test-Fail "Summary statistics script"
}

# ============================================
# PHASE 7: Files Check
# ============================================
Test-Section "7.1" "Checking documentation files"
$docFiles = @(
    "PROJECT_OVERVIEW.md",
    "LEARNING_PATH.md",
    "INPUT_OUTPUT_GUIDE.md",
    "CONTRIBUTING.md",
    "GIT_WORKFLOW.md",
    "CHANGELOG.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Test-Pass "$file exists ($size bytes)"
    } else {
        Test-Fail "$file missing"
    }
}

# ============================================
# Summary
# ============================================
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "TEST RESULTS SUMMARY" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
$total = $passed + $failed
Write-Host "Total:  $total"

Write-Host "`n==========================================" -ForegroundColor Cyan
if ($failed -eq 0) {
    Write-Host "✅ ALL TESTS PASSED - READY TO PUSH" -ForegroundColor Green
} else {
    Write-Host "❌ SOME TESTS FAILED - DO NOT PUSH YET" -ForegroundColor Red
    Write-Host "Troubleshooting: See TEST_BEFORE_PUSH.md for fixes"
}
Write-Host "==========================================" -ForegroundColor Cyan
