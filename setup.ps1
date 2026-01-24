# Run as: powershell -ExecutionPolicy Bypass -File setup.ps1

param(
    [switch]$SkipJava = $false
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "SemanticLayer Automated Setup (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python version
Write-Host "`n[1/6] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion"

# 2. Check/Install Java
if (-not $SkipJava) {
    Write-Host "`n[2/6] Checking Java installation..." -ForegroundColor Yellow
    try {
        $javaVersion = java -version 2>&1
        Write-Host "Java already installed: $($javaVersion[0])"
    } catch {
        Write-Host "Java not found. Please install from:" -ForegroundColor Red
        Write-Host "  https://adoptium.net/" -ForegroundColor Cyan
        Write-Host "Then set JAVA_HOME environment variable and re-run this script." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "[2/6] Skipping Java check (--SkipJava flag used)"
}

# 3. Create virtual environment
Write-Host "`n[3/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force .venv
}
python -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
Write-Host "Virtual environment created and activated" -ForegroundColor Green

# 4. Install dependencies
Write-Host "`n[4/6] Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
pip install -r SemanticLayer/requirements.txt
Write-Host "Dependencies installed successfully" -ForegroundColor Green

# 5. Run ETL
Write-Host "`n[5/6] Running PySpark ETL..." -ForegroundColor Yellow
python SemanticLayer/scripts/process_data_spark.py
Write-Host "ETL completed" -ForegroundColor Green

# 6. Verify output
Write-Host "`n[6/6] Verifying output files..." -ForegroundColor Yellow
$files = @(
    "SemanticLayer/data/silver/customers_silver.csv",
    "SemanticLayer/data/silver/transactions_silver.csv",
    "SemanticLayer/data/gold/gold_view.csv",
    "SemanticLayer/data/metadata.json"
)

$allExist = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "✓ $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "✗ $file (MISSING)" -ForegroundColor Red
        $allExist = $false
    }
}

Write-Host "`n==========================================" -ForegroundColor Cyan
if ($allExist) {
    Write-Host "✓ Setup completed successfully!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. View gold layer: Get-Content SemanticLayer/data/gold/gold_view.csv -Head 20"
    Write-Host "2. Run SQL queries: python SemanticLayer/scripts/sql_layer.py"
    Write-Host "3. Run tests: pytest -q"
    Write-Host "`nTo activate venv in future: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
} else {
    Write-Host "✗ Setup had issues. Check output above." -ForegroundColor Red
    exit 1
}
