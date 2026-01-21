#!/usr/bin/env python3
"""
PySpark ETL: Process raw CSV files into Silver (cleaned) and Gold (semantic view) layers.

- Reads: data/customers.csv, data/transactions.csv
- Writes:
    data/silver/customers_silver.csv
    data/silver/transactions_silver.csv
    data/gold/gold_view.csv
    data/metadata.json (updated with metric info)
"""
from pathlib import Path
import json
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
METADATA_FILE = DATA_DIR / "metadata.json"

SILVER_DIR.mkdir(parents=True, exist_ok=True)
GOLD_DIR.mkdir(parents=True, exist_ok=True)

def create_spark(app_name="semantic-layer-etl"):
    return SparkSession.builder.master("local[*]").appName(app_name).getOrCreate()

def read_raw_tables(spark, data_dir: Path):
    customers_path = str((data_dir / "customers.csv").resolve())
    transactions_path = str((data_dir / "transactions.csv").resolve())
    customers = spark.read.option("header", "true").option("inferSchema", "true").csv(customers_path)
    transactions = spark.read.option("header", "true").option("inferSchema", "true").csv(transactions_path)
    return customers, transactions

def clean_customers_df(df):
    # Lowercase column names
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().lower())
    # parse created_at if present
    if "created_at" in df.columns:
        df = df.withColumn("created_at", F.to_timestamp("created_at"))
    # drop exact duplicates
    df = df.dropDuplicates()
    return df

def clean_transactions_df(df):
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().lower())
    # ensure amount numeric and fill nulls with 0.0
    if "amount" in df.columns:
        df = df.withColumn("amount", F.col("amount").cast(DoubleType()))
        df = df.withColumn("amount", F.when(F.col("amount").isNull(), F.lit(0.0)).otherwise(F.col("amount)))
    if "transaction_date" in df.columns:
        df = df.withColumn("transaction_date", F.to_timestamp("transaction_date"))
    if "status" in df.columns:
        df = df.withColumn("status", F.lower(F.col("status")))
    return df

def build_gold_view(transactions_df):
    if "customer_id" not in transactions_df.columns:
        raise ValueError("transactions must include customer_id")
    agg = transactions_df.groupBy("customer_id").agg(
        F.round(F.sum("amount"), 2).alias("total_spend"),
        F.count("transaction_id").alias("transaction_count"),
        F.round(F.avg("amount"), 2).alias("avg_transaction_amount")
    )
    return agg

def write_csv_df(df, path: Path):
    # Write single CSV file for convenience (coalesce(1)). Overwrites existing path.
    tmp = path.with_suffix(".tmp")
    if tmp.exists():
        tmp.unlink()
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(str(tmp))
    # move generated part file to expected path
    import shutil
    import glob
    # find part file
    part_files = list(tmp.glob("part-*.csv"))
    if not part_files:
        # if Spark wrote a directory with a single CSV, just copy the directory content
        # fallback: raise
        raise RuntimeError(f"No part file after writing {tmp}")
    part = part_files[0]
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(part), str(path))
    # remove _SUCCESS and tmp dir leftovers
    for f in tmp.glob("*"):
        try:
            f.unlink()
        except Exception:
            pass
    try:
        tmp.rmdir()
    except Exception:
        pass

def update_metadata_with_metrics(metadata_path: Path, gold_rel_path: str):
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    metadata.setdefault("tables", [])
    gold_entry = {
        "name": "gold_view",
        "path": gold_rel_path,
        "description": "Aggregated semantic view per customer with metrics used by AI and BI",
        "columns": [
            {"name": "customer_id", "type": "string", "description": "PK - customer identifier"},
            {"name": "total_spend", "type": "double", "description": "Sum of transaction amount"},
            {"name": "transaction_count", "type": "integer", "description": "Number of transactions"},
            {"name": "avg_transaction_amount", "type": "double", "description": "Average transaction amount"}
        ],
        "metrics": [
            {"name": "total_spend", "expression": "SUM(amount)", "description": "Total amount spent by customer"},
            {"name": "transaction_count", "expression": "COUNT(transaction_id)", "description": "Number of transactions per customer"},
            {"name": "avg_transaction_amount", "expression": "AVG(amount)", "description": "Average transaction amount per customer"}
        ],
        "semantic_tags": ["gold", "semantic_view", "customer_metrics"]
    }
    metadata["tables"] = [t for t in metadata["tables"] if t.get("name") != "gold_view"]
    metadata["tables"].append(gold_entry)
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata updated at {metadata_path}")

def main():
    spark = create_spark()
    try:
        customers, transactions = read_raw_tables(spark, DATA_DIR)
    except Exception as e:
        print(f"Failed to read input CSVs from {DATA_DIR}: {e}", file=sys.stderr)
        spark.stop()
        return

    print("Cleaning to Silver layer...")
    customers_silver = clean_customers_df(customers)
    transactions_silver = clean_transactions_df(transactions)

    # write silver
    print("Writing Silver tables...")
    write_csv_df(customers_silver, SILVER_DIR / "customers_silver.csv")
    write_csv_df(transactions_silver, SILVER_DIR / "transactions_silver.csv")
    print(f"Saved Silver tables to {SILVER_DIR}")

    print("Building Gold semantic view...")
    gold_view = build_gold_view(transactions_silver)
    gold_path = GOLD_DIR / "gold_view.csv"
    write_csv_df(gold_view, gold_path)
    print(f"Gold layer saved to {gold_path}")

    # Update metadata
    update_metadata_with_metrics(METADATA_FILE, str(gold_path.relative_to(ROOT)))
    spark.stop()


if __name__ == "__main__":
    main()