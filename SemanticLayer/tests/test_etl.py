# filepath: /Users/dattu/AI/AI-Project/SemanticLayer/tests/test_etl.py
"""
ETL Pipeline Tests
"""

import pandas as pd
import pytest
from pathlib import Path

class TestETL:
    """Test ETL pipeline outputs."""
    
    def test_gold_view_exists(self):
        """Test that gold view file exists."""
        gold_path = Path('SemanticLayer/data/gold/gold_view.csv')
        assert gold_path.exists(), "gold_view.csv should exist"
    
    def test_gold_view_has_data(self):
        """Test that gold view has data."""
        df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
        assert len(df) > 0, "gold_view should have rows"
    
    def test_gold_view_structure(self):
        """Test that gold view has correct columns."""
        df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
        expected_cols = ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount']
        assert list(df.columns) == expected_cols, f"Columns should be {expected_cols}"
    
    def test_no_null_values(self):
        """Test that there are no null values in gold view."""
        df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
        assert df.isnull().sum().sum() == 0, "No null values allowed"
    
    def test_positive_spending(self):
        """Test that all customers have positive spending."""
        df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
        assert (df['total_spend'] > 0).all(), "All customers should have positive spend"
    
    def test_transaction_count_positive(self):
        """Test that transaction counts are positive."""
        df = pd.read_csv('SemanticLayer/data/gold/gold_view.csv')
        assert (df['transaction_count'] > 0).all(), "Transaction count should be positive"
    
    def test_silver_layer_exists(self):
        """Test that silver layer files exist."""
        customers_path = Path('SemanticLayer/data/silver/customers_silver.csv')
        transactions_path = Path('SemanticLayer/data/silver/transactions_silver.csv')
        
        assert customers_path.exists(), "customers_silver.csv should exist"
        assert transactions_path.exists(), "transactions_silver.csv should exist"
    
    def test_metadata_exists(self):
        """Test that metadata file exists."""
        metadata_path = Path('SemanticLayer/data/metadata.json')
        assert metadata_path.exists(), "metadata.json should exist"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
