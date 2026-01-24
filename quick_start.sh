#!/bin/bash

set -e

echo "=========================================="
echo "SemanticLayer Quick Start"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Setup
echo -e "\n${YELLOW}[1/4] Setting up environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q --upgrade pip setuptools wheel
pip install -q -r SemanticLayer/requirements.txt

# 2. Run ETL
echo -e "${YELLOW}[2/4] Running ETL pipeline...${NC}"
python SemanticLayer/scripts/process_data_spark.py > /dev/null 2>&1

# 3. Show summary
echo -e "${YELLOW}[3/4] Generating summary stats...${NC}"
python SemanticLayer/scripts/summary_stats.py

# 4. Run tests
echo -e "${YELLOW}[4/4] Running tests...${NC}"
pytest -q SemanticLayer/tests/ 2>&1 | head -20

echo -e "\n${GREEN}✓ Quick start completed!${NC}"
echo -e "\n${YELLOW}Next commands:${NC}"
echo "  • View gold layer: head -20 SemanticLayer/data/gold/gold_view.csv"
echo "  • Run SQL queries: python SemanticLayer/scripts/sql_layer.py"
echo "  • Open notebook: SemanticLayer/notebooks/semantic_layer_demo_colab.ipynb"
echo "  • See example queries: cat SemanticLayer/EXAMPLE_QUERIES.md"
