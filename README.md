# SemanticLayer: Data Aggregation & Analytics Platform

[![GitHub Actions](https://github.com/AdarshInturi0425/AI-Project/workflows/SemanticLayer%20Tests/badge.svg)](https://github.com/AdarshInturi0425/AI-Project/actions)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready data pipeline that transforms raw transaction data into semantic analytics layer using **PySpark** (with pandas fallback) and **DuckDB** for SQL queries.

---

## ⚡ Quick Start

### One-Command Setup (recommended)

```bash
# macOS/Linux
chmod +x quick_start.sh
./quick_start.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File quick_start.ps1
```

This will:
1. ✅ Setup Python environment
2. ✅ Install dependencies
3. ✅ Run ETL pipeline
4. ✅ Display summary statistics
5. ✅ Run all tests

### Manual Setup

```bash
# Clone repo
git clone https://github.com/AdarshInturi0425/AI-Project.git
cd AI-Project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r SemanticLayer/requirements.txt

# Run ETL
python SemanticLayer/scripts/process_data_spark.py

# View results
head -20 SemanticLayer/data/gold/gold_view.csv

# Run tests
pytest -q
```

---

## 📋 Features

### Data Pipeline (PySpark + Pandas)
- **Raw Layer**: Input CSV files with customer and transaction data
- **Silver Layer**: Cleaned, deduplicated data with type validation
- **Gold Layer**: Aggregated semantic views for analytics
- **Metadata**: Schema tracking and data lineage

### Query Layer (DuckDB)
- In-memory SQL queries on gold layer
- High-performance analytics without heavy infrastructure
- Export results as pandas DataFrames or CSV

### Validation & Testing
- Automated data quality checks
- Unit tests for ETL aggregations
- Integration tests with pytest
- CI/CD via GitHub Actions

### Documentation
- OS-specific setup guides (Windows, macOS, Linux)
- Comprehensive troubleshooting notebook
- 10+ example SQL queries
- Contributing guidelines

---

## 📁 Project Structure

```
SemanticLayer/
├── data/
│   ├── raw/                    # Input data
│   ├── silver/                 # Cleaned data
│   ├── gold/                   # Semantic analytics layer
│   └── metadata.json           # Schema metadata
├── scripts/
│   ├── process_data_spark.py   # PySpark ETL (recommended)
│   ├── process_data.py         # Pandas ETL (fallback)
│   ├── sql_layer.py            # DuckDB queries
│   ├── summary_stats.py        # Summary statistics
│   └── data_validation.py      # Data quality checks
├── notebooks/
│   ├── semantic_layer_demo_colab.ipynb    # PySpark demo
│   ├── colab_duckdb.ipynb                 # DuckDB demo (no Java)
│   └── TROUBLESHOOTING.ipynb              # Troubleshooting guide
├── tests/
│   └── test_etl.py             # Pytest tests
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

## 🚀 Usage Examples

### 1. Generate Summary Statistics

```bash
python SemanticLayer/scripts/summary_stats.py
```

**Output:**
```
Total Customers:        520
Total Spend:           $48,500.00
Total Transactions:     1,250
Avg Transaction Amount: $38.80
```

### 2. Run SQL Queries

```bash
python SemanticLayer/scripts/sql_layer.py
```

Includes:
- Top 5 spenders
- Transaction frequency distribution
- Spending by segment

### 3. Validate Data Quality

```bash
python SemanticLayer/scripts/data_validation.py
```

Checks:
- ✓ File existence and structure
- ✓ Null value handling
- ✓ Numeric ranges
- ✓ Gold aggregation accuracy

### 4. Run Automated Tests

```bash
pytest -v SemanticLayer/tests/
```

### 5. Query Gold Layer (Python)

```python
import duckdb
import pandas as pd

# Load gold view
conn = duckdb.connect(':memory:')
conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")

# Top 5 customers
result = conn.execute("""
    SELECT customer_id, total_spend
    FROM gold_view
    ORDER BY total_spend DESC
    LIMIT 5
""").fetch_df()

print(result)
```

---

## 📊 Example Queries

See [EXAMPLE_QUERIES.md](SemanticLayer/EXAMPLE_QUERIES.md) for:

1. Top customers by spend
2. Most frequent customers
3. Spending distribution (quartiles)
4. High-value customers (90th percentile)
5. Customer segmentation
6. Average transaction value analysis
7. Total business metrics
8. Customer filtering
9. Outlier detection
10. Time-based analysis (template)

---

## 🔧 Configuration

### Adding Custom Data

1. Place raw CSV files in `SemanticLayer/data/raw/`
2. Update schema in relevant script
3. Run ETL: `python SemanticLayer/scripts/process_data_spark.py`

### Customizing Aggregations

Edit `SemanticLayer/scripts/process_data_spark.py`:

```python
# Modify gold layer aggregations
gold_df = silver_transactions.groupBy("customer_id").agg(
    F.sum("amount").alias("total_spend"),
    F.count("transaction_id").alias("transaction_count"),
    F.avg("amount").alias("avg_transaction_amount"),
    # Add custom metrics here
).collect()
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Complete setup instructions |
| [SETUP_BY_OS.md](SETUP_BY_OS.md) | OS-specific guides (Win/Mac/Linux) |
| [TROUBLESHOOTING.ipynb](SemanticLayer/notebooks/TROUBLESHOOTING.ipynb) | Common issues & solutions |
| [EXAMPLE_QUERIES.md](SemanticLayer/EXAMPLE_QUERIES.md) | 10+ SQL query examples |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## 🐍 Python Versions & Dependencies

**Supported Python:** 3.8, 3.9, 3.10, 3.11

**Key Dependencies:**
- `pyspark>=3.4.0` – Data processing
- `pandas>=1.3.0` – Data manipulation
- `duckdb>=0.8.0` – SQL queries
- `pytest>=7.0.0` – Testing

See `SemanticLayer/requirements.txt` for full list.

---

## ⚠️ Prerequisites

### Required
- **Python 3.8+** ([download](https://www.python.org/downloads/))
- **Git** ([download](https://git-scm.com/))

### For PySpark ETL
- **Java/JDK 11+** ([download](https://adoptium.net/))

### Optional
- **Docker** (for containerized execution)
- **Google Colab** (for notebook demos)

---

## 🏃 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Java not found` | Install JDK 11+, set `JAVA_HOME` env var |
| `Module not found` | Activate venv: `source .venv/bin/activate` |
| `gold_view.csv missing` | Run ETL: `python SemanticLayer/scripts/process_data_spark.py` |
| `Tests fail` | Re-generate data, check file paths, see `TROUBLESHOOTING.ipynb` |

**Full troubleshooting guide:** See [TROUBLESHOOTING.ipynb](SemanticLayer/notebooks/TROUBLESHOOTING.ipynb)

---

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run specific test file
pytest -v SemanticLayer/tests/test_etl.py

# Run with coverage report
pytest --cov=SemanticLayer SemanticLayer/tests/

# Run tests matching pattern
pytest -k "gold_view" -v
```

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Branching strategy
- Code style guidelines
- Testing requirements
- Pull request process

Quick contribution steps:
```bash
git checkout -b feature/my-feature
# Make changes
pytest -v  # Verify tests pass
git commit -m "[FEATURE] Add my feature"
git push origin feature/my-feature
# Open Pull Request on GitHub
```

---

## 📈 Performance

Typical runtime on sample data (520 customers, 1,250 transactions):
- **PySpark ETL**: 15-30 seconds (includes JVM startup)
- **SQL queries**: <1 second (DuckDB)
- **Data validation**: 2-5 seconds
- **Tests**: 20-40 seconds

---

## 🐳 Docker Support

Run in Docker to avoid system dependencies:

```bash
docker build -t semantic-layer .
docker run semantic-layer
```

See `Dockerfile` for details.

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Adarsh Inturi** ([@AdarshInturi0425](https://github.com/AdarshInturi0425))

---

## 🙏 Acknowledgments

- PySpark & Spark community
- DuckDB for in-memory SQL engine
- pytest for testing framework
- Pandas for data manipulation

---

## 💡 Next Steps

1. ✅ [Setup](SETUP_GUIDE.md) the project
2. ✅ [Explore](EXAMPLE_QUERIES.md) example queries
3. ✅ [Run tests](README.md#-testing) to verify installation
4. ✅ [Contribute](CONTRIBUTING.md) improvements
5. ✅ Deploy to production ([guide coming soon](docs/DEPLOYMENT.md))

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/AdarshInturi0425/AI-Project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AdarshInturi0425/AI-Project/discussions)
- **Email**: contact@example.com

---

**Made with ❤️ by the AI-Project team**