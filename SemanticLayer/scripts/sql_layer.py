# filepath: /Users/dattu/AI/AI-Project/SemanticLayer/scripts/sql_layer.py
"""
DuckDB SQL Query Layer
Executes example queries on the gold layer
"""

import duckdb
import pandas as pd

def run_queries():
    """Run example SQL queries on gold layer."""
    
    conn = duckdb.connect(':memory:')
    
    # Register gold view
    conn.execute("CREATE TABLE gold_view AS SELECT * FROM 'SemanticLayer/data/gold/gold_view.csv'")
    
    print("\n" + "=" * 60)
    print("  TOP SPENDERS")
    print("=" * 60)
    
    result = conn.execute("""
        SELECT customer_id, total_spend, transaction_count
        FROM gold_view
        ORDER BY total_spend DESC
        LIMIT 5
    """).fetch_df()
    
    print(result.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("  CUSTOMERS FILTERED BY SPEND > 100")
    print("=" * 60)
    
    result = conn.execute("""
        SELECT customer_id, total_spend, transaction_count, avg_transaction_amount
        FROM gold_view
        WHERE total_spend > 100
        ORDER BY total_spend DESC
    """).fetch_df()
    
    print(result.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("  SUMMARY METRICS")
    print("=" * 60)
    
    result = conn.execute("""
        SELECT 
            COUNT(*) as total_customers,
            ROUND(SUM(total_spend), 2) as total_revenue,
            ROUND(AVG(total_spend), 2) as avg_customer_value,
            ROUND(AVG(transaction_count), 2) as avg_transactions
        FROM gold_view
    """).fetch_df()
    
    print(result.to_string(index=False))
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_queries()
