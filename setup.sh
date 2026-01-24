#!/bin/bash

set -e  # Exit on error

echo "=========================================="
echo "SemanticLayer Automated Setup"
echo "=========================================="

# Detect OS
OS_TYPE=$(uname -s)
echo "Detected OS: $OS_TYPE"

# 1. Check Python version
echo -e "\n[1/6] Checking Python version..."
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "ERROR: Python 3.8+ required"
    exit 1
fi

# 2. Check/Install Java
echo -e "\n[2/6] Checking Java installation..."
if ! command -v java &> /dev/null; then
    echo "Java not found. Installing..."
    
    if [ "$OS_TYPE" = "Darwin" ]; then
        # macOS
        echo "Installing via Homebrew (macOS)..."
        if ! command -v brew &> /dev/null; then
            echo "ERROR: Homebrew not found. Install from https://brew.sh"
            exit 1
        fi
        brew install openjdk@11
        JAVA_HOME=$(brew --prefix openjdk@11)
        echo "export JAVA_HOME=$JAVA_HOME" >> ~/.zshrc
        echo "export PATH=\"$JAVA_HOME/bin:\$PATH\"" >> ~/.zshrc
        
    elif [ "$OS_TYPE" = "Linux" ]; then
        # Linux (Ubuntu/Debian)
        echo "Installing via apt (Linux)..."
        sudo apt-get update
        sudo apt-get install -y openjdk-11-jdk
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
        
    else
        echo "ERROR: Unsupported OS for automatic Java installation"
        echo "Please install Java manually from https://adoptium.net/"
        exit 1
    fi
else
    echo "Java already installed: $(java -version 2>&1 | head -1)"
fi

# 3. Create virtual environment
echo -e "\n[3/6] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Removing..."
    rm -rf .venv
fi
python3 -m venv .venv
source .venv/bin/activate
echo "Virtual environment created and activated"

# 4. Install dependencies
echo -e "\n[4/6] Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r SemanticLayer/requirements.txt
echo "Dependencies installed successfully"

# 5. Run ETL
echo -e "\n[5/6] Running PySpark ETL..."
python SemanticLayer/scripts/process_data_spark.py
echo "ETL completed"

# 6. Verify output
echo -e "\n[6/6] Verifying output files..."
FILES=(
    "SemanticLayer/data/silver/customers_silver.csv"
    "SemanticLayer/data/silver/transactions_silver.csv"
    "SemanticLayer/data/gold/gold_view.csv"
    "SemanticLayer/data/metadata.json"
)

ALL_EXIST=true
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(du -h "$file" | cut -f1)
        echo "✓ $file ($SIZE)"
    else
        echo "✗ $file (MISSING)"
        ALL_EXIST=false
    fi
done

echo -e "\n=========================================="
if [ "$ALL_EXIST" = true ]; then
    echo "✓ Setup completed successfully!"
    echo "=========================================="
    echo -e "\nNext steps:"
    echo "1. View gold layer: head -20 SemanticLayer/data/gold/gold_view.csv"
    echo "2. Run SQL queries: python SemanticLayer/scripts/sql_layer.py"
    echo "3. Run tests: pytest -q"
    echo -e "\nTo activate venv in future: source .venv/bin/activate"
else
    echo "✗ Setup had issues. Check output above."
    exit 1
fi
