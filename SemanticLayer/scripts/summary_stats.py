"""
Summary statistics script for the semantic layer.
Displays top customers, spending patterns, and data quality metrics.
"""

import pandas as pd
import os
from pathlib import Path

def load_gold_view():
    """Load the gold view CSV."""
    gold_path = Path(__file__).parent.parent / "data" / "gold" / "gold_view.csv"
    if not gold_path.exists():
        print(f"Error: Gold view not found at {gold_path}")
        print("Run: python SemanticLayer/scripts/process_data_spark.py")
        return None
    return pd.read_csv(gold_path)

def print_header(title):
    """Print formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")

def print_summary_stats(df):
    """Print basic statistics."""
    print_header("📊 Summary Statistics")
    print(f"Total Customers:        {len(df)}")
    print(f"Total Spend:           ${df['total_spend'].sum():,.2f}")
    print(f"Total Transactions:     {int(df['transaction_count'].sum())}")
    print(f"Avg Transaction Amount: ${df['avg_transaction_amount'].mean():,.2f}")
    print(f"Median Transaction:     ${df['avg_transaction_amount'].median():,.2f}")
    print(f"Min Transaction:        ${df['avg_transaction_amount'].min():,.2f}")
    print(f"Max Transaction:        ${df['avg_transaction_amount'].max():,.2f}")

def print_top_customers(df, n=5):
    """Print top N customers by spending."""
    print_header(f"🏆 Top {n} Customers by Total Spend")
    top = df.nlargest(n, 'total_spend')[['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount']]
    
    for idx, (_, row) in enumerate(top.iterrows(), 1):
        print(f"{idx}. {row['customer_id']}")
        print(f"   Total Spend:      ${row['total_spend']:,.2f}")
        print(f"   Transactions:     {int(row['transaction_count'])}")
        print(f"   Avg per Trans:    ${row['avg_transaction_amount']:,.2f}\n")

def print_high_frequency_customers(df, n=5):
    """Print top N customers by transaction count."""
    print_header(f"📈 Top {n} Customers by Transaction Count")
    top = df.nlargest(n, 'transaction_count')[['customer_id', 'transaction_count', 'total_spend', 'avg_transaction_amount']]
    
    for idx, (_, row) in enumerate(top.iterrows(), 1):
        print(f"{idx}. {row['customer_id']}")
        print(f"   Transactions:     {int(row['transaction_count'])}")
        print(f"   Total Spend:      ${row['total_spend']:,.2f}")
        print(f"   Avg per Trans:    ${row['avg_transaction_amount']:,.2f}\n")

def print_spending_distribution(df):
    """Print spending distribution by quartiles."""
    print_header("💰 Spending Distribution (Quartiles)")
    quartiles = df['total_spend'].quantile([0.25, 0.5, 0.75])
    
    print(f"25th Percentile (Q1):   ${quartiles[0.25]:,.2f}")
    print(f"50th Percentile (Q2):   ${quartiles[0.5]:,.2f}")
    print(f"75th Percentile (Q3):   ${quartiles[0.75]:,.2f}")
    
    print("\nCustomer Segments:")
    low = len(df[df['total_spend'] < quartiles[0.25]])
    mid_low = len(df[(df['total_spend'] >= quartiles[0.25]) & (df['total_spend'] < quartiles[0.5])])
    mid_high = len(df[(df['total_spend'] >= quartiles[0.5]) & (df['total_spend'] < quartiles[0.75])])
    high = len(df[df['total_spend'] >= quartiles[0.75]])
    
    print(f"  Low Spenders (Q1):    {low} customers")
    print(f"  Mid-Low (Q2):         {mid_low} customers")
    print(f"  Mid-High (Q3):        {mid_high} customers")
    print(f"  High Spenders (Q4):   {high} customers")

def print_data_quality(df):
    """Print data quality metrics."""
    print_header("🔍 Data Quality Metrics")
    
    print(f"Total Records:          {len(df)}")
    print(f"Missing Values:         {df.isnull().sum().sum()}")
    print(f"Duplicate Customers:    {len(df) - df['customer_id'].nunique()}")
    print(f"Columns:                {', '.join(df.columns.tolist())}")
    print(f"Data Types:\n{df.dtypes.to_string()}")

def main():
    """Main execution."""
    df = load_gold_view()
    if df is None:
        return
    
    print("\n" + "=" * 60)
    print("  SEMANTIC LAYER - SUMMARY STATISTICS")
    print("=" * 60)
    
    print_summary_stats(df)
    print_top_customers(df, n=5)
    print_high_frequency_customers(df, n=5)
    print_spending_distribution(df)
    print_data_quality(df)
    
    print_header("✅ Summary Complete")
    print("For detailed SQL queries, run:")
    print("  python SemanticLayer/scripts/sql_layer.py\n")

if __name__ == "__main__":
    main()
