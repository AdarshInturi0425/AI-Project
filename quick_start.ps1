# Run as: powershell -ExecutionPolicy Bypass -File quick_start.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "SemanticLayer Quick Start (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Setup
Write-Host "`n[1/4] Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& ".\.venv\Scripts\Activate.ps1"
python -m pip install -q --upgrade pip setuptools wheel
pip install -q -r SemanticLayer/requirements.txt

# 2. Run ETL
Write-Host "[2/4] Running ETL pipeline..." -ForegroundColor Yellow
python SemanticLayer/scripts/process_data_spark.py | Out-Null

# 3. Show summary
Write-Host "[3/4] Generating summary stats..." -ForegroundColor Yellow
python SemanticLayer/scripts/summary_stats.py

# 4. Run tests
Write-Host "[4/4] Running tests..." -ForegroundColor Yellow
pytest -q SemanticLayer/tests/ 2>$null | Select-Object -First 20

Write-Host "`n✓ Quick start completed!" -ForegroundColor Green
Write-Host "`nNext commands:" -ForegroundColor Yellow
Write-Host "  • View gold layer: Get-Content SemanticLayer/data/gold/gold_view.csv -Head 20"
Write-Host "  • Run SQL queries: python SemanticLayer/scripts/sql_layer.py"
Write-Host "  • Open notebook: SemanticLayer/notebooks/semantic_layer_demo_colab.ipynb"
Write-Host "  • See example queries: Get-Content SemanticLayer/EXAMPLE_QUERIES.md"
