# filepath: /Users/dattu/AI/AI-Project/SemanticLayer/scripts/transform_ecommerce_data.py
"""
Transform e-commerce data to SemanticLayer format
Converts: customers.csv + orders.csv + order_items.csv
Into: customers_raw.csv + transactions_raw.csv
"""

import pandas as pd
from pathlib import Path

def transform_ecommerce_data(source_dir, output_dir):
    """Transform e-commerce data to SemanticLayer format."""
    
    print("=" * 60)
    print("TRANSFORMING E-COMMERCE DATA")
    print("=" * 60)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 1. Load and prepare customers
    print("\n[1/3] Processing customers data...")
    customers = pd.read_csv(f"{source_dir}/customers.csv")
    customers_raw = customers[['customer_id', 'email']].copy()
    customers_raw.to_csv(f"{output_dir}/customers.csv", index=False)
    print(f"✓ Created customers.csv ({len(customers_raw)} rows)")
    print(f"  Columns: {list(customers_raw.columns)}")
    
    # 2. Load and prepare orders with order_items
    print("\n[2/3] Processing orders data...")
    orders = pd.read_csv(f"{source_dir}/orders.csv")
    order_items = pd.read_csv(f"{source_dir}/order_items.csv")
    
    # Merge orders with order_items to get line-level transactions
    transactions = order_items.merge(orders[['order_id', 'customer_id', 'order_time']], 
                                     on='order_id', how='left')
    
    # Create transaction_id (order_id + line item)
    transactions['transaction_id'] = (transactions['order_id'].astype(str) + 
                                     '_' + transactions.index.astype(str))
    
    # Select required columns
    transactions_raw = transactions[[
        'transaction_id', 
        'customer_id', 
        'line_total_usd'
    ]].copy()
    
    # Rename amount column
    transactions_raw.columns = ['transaction_id', 'customer_id', 'amount']
    
    # Remove negative amounts
    transactions_raw = transactions_raw[transactions_raw['amount'] > 0]
    
    transactions_raw.to_csv(f"{output_dir}/transactions.csv", index=False)
    print(f"✓ Created transactions.csv ({len(transactions_raw)} rows)")
    print(f"  Columns: {list(transactions_raw.columns)}")
    
    # 3. Summary statistics
    print("\n[3/3] Data summary:")
    print(f"  Total customers: {customers_raw['customer_id'].nunique()}")
    print(f"  Total transactions: {len(transactions_raw)}")
    print(f"  Total revenue: ${transactions_raw['amount'].sum():,.2f}")
    print(f"  Avg transaction: ${transactions_raw['amount'].mean():.2f}")
    
    print("\n" + "=" * 60)
    print("✅ DATA TRANSFORMATION COMPLETE!")
    print("=" * 60)
    print(f"\nFiles saved to: {output_dir}/")
    print("  • customers.csv")
    print("  • transactions.csv")
    print("\nNext step: python SemanticLayer/scripts/process_data.py")

if __name__ == "__main__":
    # Source: your e-commerce data
    source = "/Users/dattu/Downloads/archive 2"
    
    # Destination: SemanticLayer raw data
    output = "SemanticLayer/data/raw"
    
    transform_ecommerce_data(source, output)
