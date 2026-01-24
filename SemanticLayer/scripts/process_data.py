# filepath: /Users/dattu/AI/AI-Project/SemanticLayer/scripts/process_data.py
"""
Pandas-based ETL pipeline (fallback when PySpark/Java not available)
Transforms raw data → silver (cleaned) → gold (aggregated)
"""

import pandas as pd
import json
from pathlib import Path

def load_raw_data():
    """Load raw CSV files."""
    print("Loading raw data...")
    
    raw_dir = Path("SemanticLayer/data/raw")
    
    customers = pd.read_csv(raw_dir / "customers.csv")
    transactions = pd.read_csv(raw_dir / "transactions.csv")
    
    print(f"  Customers: {len(customers)} rows")
    print(f"  Transactions: {len(transactions)} rows")
    
    return customers, transactions

def clean_to_silver(customers, transactions):
    """Clean and deduplicate data."""
    print("\nCleaning to Silver layer...")
    
    # Clean customers
    customers_clean = customers.dropna(subset=['customer_id']).drop_duplicates(subset=['customer_id'])
    print(f"  Customers cleaned: {len(customers_clean)} rows")
    
    # Clean transactions
    transactions_clean = transactions.dropna(subset=['customer_id', 'amount'])
    transactions_clean = transactions_clean[transactions_clean['amount'] > 0]
    transactions_clean = transactions_clean.drop_duplicates(subset=['transaction_id'])
    print(f"  Transactions cleaned: {len(transactions_clean)} rows")
    
    return customers_clean, transactions_clean

def save_silver(customers, transactions):
    """Save cleaned data to silver layer."""
    print("\nWriting Silver tables...")
    
    silver_dir = Path("SemanticLayer/data/silver")
    silver_dir.mkdir(parents=True, exist_ok=True)
    
    customers.to_csv(silver_dir / "customers_silver.csv", index=False)
    transactions.to_csv(silver_dir / "transactions_silver.csv", index=False)
    
    print(f"  Saved Silver tables to {silver_dir}")

def build_gold_layer(transactions):
    """Build aggregated semantic layer."""
    print("\nBuilding Gold semantic view...")
    
    gold = transactions.groupby('customer_id').agg({
        'amount': ['sum', 'count', 'mean']
    }).reset_index()
    
    gold.columns = ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount']
    gold['avg_transaction_amount'] = gold['avg_transaction_amount'].round(2)
    gold = gold.sort_values('total_spend', ascending=False).reset_index(drop=True)
    
    print(f"  Created {len(gold)} customer records")
    
    return gold

def save_gold(gold):
    """Save gold layer."""
    gold_dir = Path("SemanticLayer/data/gold")
    gold_dir.mkdir(parents=True, exist_ok=True)
    
    gold.to_csv(gold_dir / "gold_view.csv", index=False)
    print(f"  Gold layer saved to {gold_dir / 'gold_view.csv'}")

def update_metadata(customers, transactions, gold):
    """Update metadata."""
    print("\nUpdating metadata...")
    
    metadata = {
        "tables": {
            "customers_silver": {
                "columns": list(customers.columns),
                "rows": len(customers)
            },
            "transactions_silver": {
                "columns": list(transactions.columns),
                "rows": len(transactions)
            },
            "gold_view": {
                "columns": list(gold.columns),
                "rows": len(gold)
            }
        }
    }
    
    metadata_path = Path("SemanticLayer/data/metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  Metadata updated at {metadata_path}")

def main():
    """Main ETL execution."""
    print("=" * 60)
    print("PANDAS-BASED ETL PIPELINE (No Java Required)")
    print("=" * 60)
    
    try:
        # Extract
        customers, transactions = load_raw_data()
        
        # Transform
        customers_clean, transactions_clean = clean_to_silver(customers, transactions)
        
        # Load Silver
        save_silver(customers_clean, transactions_clean)
        
        # Build Gold
        gold = build_gold_layer(transactions_clean)
        
        # Save Gold
        save_gold(gold)
        
        # Update metadata
        update_metadata(customers_clean, transactions_clean, gold)
        
        print("\n" + "=" * 60)
        print("✅ ETL Pipeline Completed Successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
