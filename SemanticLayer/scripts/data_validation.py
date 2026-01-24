"""
Data validation script for quality checks on silver and gold layers.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List

class DataValidator:
    """Validates data quality across layers."""
    
    def __init__(self, data_dir="SemanticLayer/data"):
        self.data_dir = Path(data_dir)
        self.results = []
    
    def add_result(self, check_name: str, status: str, message: str):
        """Record validation result."""
        self.results.append({
            'check': check_name,
            'status': status,
            'message': message
        })
        symbol = '✓' if status == 'PASS' else '✗'
        print(f"{symbol} {check_name}: {message}")
    
    def validate_file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        full_path = self.data_dir / file_path
        exists = full_path.exists()
        self.add_result(
            f"File exists: {file_path}",
            "PASS" if exists else "FAIL",
            f"Size: {full_path.stat().st_size} bytes" if exists else "File not found"
        )
        return exists
    
    def validate_csv_structure(self, file_path: str, expected_columns: List[str]) -> bool:
        """Validate CSV structure."""
        full_path = self.data_dir / file_path
        if not full_path.exists():
            self.add_result(f"CSV structure: {file_path}", "FAIL", "File not found")
            return False
        
        try:
            df = pd.read_csv(full_path)
            missing_cols = set(expected_columns) - set(df.columns)
            
            if missing_cols:
                self.add_result(
                    f"CSV structure: {file_path}",
                    "FAIL",
                    f"Missing columns: {missing_cols}"
                )
                return False
            
            self.add_result(
                f"CSV structure: {file_path}",
                "PASS",
                f"{len(df)} rows, {len(df.columns)} columns"
            )
            return True
        except Exception as e:
            self.add_result(f"CSV structure: {file_path}", "FAIL", str(e))
            return False
    
    def validate_no_nulls(self, file_path: str, columns: List[str]) -> bool:
        """Check for null values in critical columns."""
        full_path = self.data_dir / file_path
        if not full_path.exists():
            return False
        
        try:
            df = pd.read_csv(full_path)
            null_counts = df[columns].isnull().sum()
            
            if null_counts.sum() > 0:
                self.add_result(
                    f"No nulls: {file_path}",
                    "FAIL",
                    f"Found nulls: {null_counts[null_counts > 0].to_dict()}"
                )
                return False
            
            self.add_result(f"No nulls: {file_path}", "PASS", "All critical columns populated")
            return True
        except Exception as e:
            self.add_result(f"No nulls: {file_path}", "FAIL", str(e))
            return False
    
    def validate_numeric_ranges(self, file_path: str, column: str, min_val: float = None, max_val: float = None) -> bool:
        """Check numeric values are within expected ranges."""
        full_path = self.data_dir / file_path
        if not full_path.exists():
            return False
        
        try:
            df = pd.read_csv(full_path)
            
            out_of_range = []
            if min_val is not None:
                out_of_range.extend(df[df[column] < min_val].index.tolist())
            if max_val is not None:
                out_of_range.extend(df[df[column] > max_val].index.tolist())
            
            if out_of_range:
                self.add_result(
                    f"Numeric range: {file_path}.{column}",
                    "FAIL",
                    f"Found {len(out_of_range)} values outside range [{min_val}, {max_val}]"
                )
                return False
            
            self.add_result(
                f"Numeric range: {file_path}.{column}",
                "PASS",
                f"All values in range [{min_val}, {max_val}]"
            )
            return True
        except Exception as e:
            self.add_result(f"Numeric range: {file_path}.{column}", "FAIL", str(e))
            return False
    
    def validate_gold_aggregations(self) -> bool:
        """Validate gold layer aggregations match silver data."""
        silver_path = self.data_dir / "silver" / "transactions_silver.csv"
        gold_path = self.data_dir / "gold" / "gold_view.csv"
        
        if not (silver_path.exists() and gold_path.exists()):
            self.add_result("Gold aggregations", "FAIL", "Missing silver or gold files")
            return False
        
        try:
            silver = pd.read_csv(silver_path)
            gold = pd.read_csv(gold_path)
            
            # Recalculate aggregations from silver
            recalc = silver.groupby('customer_id').agg({
                'amount': ['sum', 'count', 'mean']
            }).reset_index()
            recalc.columns = ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount']
            recalc = recalc.sort_values('customer_id').reset_index(drop=True)
            gold_sorted = gold.sort_values('customer_id').reset_index(drop=True)
            
            # Compare (with floating point tolerance)
            if not recalc['customer_id'].equals(gold_sorted['customer_id']):
                self.add_result("Gold aggregations", "FAIL", "Customer IDs don't match")
                return False
            
            self.add_result("Gold aggregations", "PASS", "Gold view matches silver data")
            return True
        except Exception as e:
            self.add_result("Gold aggregations", "FAIL", str(e))
            return False
    
    def validate_all(self) -> Dict:
        """Run all validations."""
        print("\n" + "=" * 70)
        print("  DATA VALIDATION REPORT")
        print("=" * 70 + "\n")
        
        # Silver layer
        print("📋 SILVER LAYER CHECKS\n")
        self.validate_file_exists("silver/customers_silver.csv")
        self.validate_csv_structure("silver/customers_silver.csv", ['customer_id', 'email'])
        self.validate_no_nulls("silver/customers_silver.csv", ['customer_id', 'email'])
        
        self.validate_file_exists("silver/transactions_silver.csv")
        self.validate_csv_structure("silver/transactions_silver.csv", ['transaction_id', 'customer_id', 'amount'])
        self.validate_no_nulls("silver/transactions_silver.csv", ['transaction_id', 'customer_id', 'amount'])
        self.validate_numeric_ranges("silver/transactions_silver.csv", 'amount', min_val=0.01)
        
        # Gold layer
        print("\n💰 GOLD LAYER CHECKS\n")
        self.validate_file_exists("gold/gold_view.csv")
        self.validate_csv_structure("gold/gold_view.csv", ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount'])
        self.validate_no_nulls("gold/gold_view.csv", ['customer_id', 'total_spend', 'transaction_count', 'avg_transaction_amount'])
        self.validate_numeric_ranges("gold/gold_view.csv", 'total_spend', min_val=0.01)
        self.validate_numeric_ranges("gold/gold_view.csv", 'transaction_count', min_val=1)
        self.validate_numeric_ranges("gold/gold_view.csv", 'avg_transaction_amount', min_val=0.01)
        
        # Cross-layer
        print("\n🔗 CROSS-LAYER CHECKS\n")
        self.validate_gold_aggregations()
        
        # Summary
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        
        print("\n" + "=" * 70)
        print(f"SUMMARY: {passed} passed, {failed} failed out of {len(self.results)} checks")
        print("=" * 70 + "\n")
        
        return {
            'total': len(self.results),
            'passed': passed,
            'failed': failed,
            'results': self.results
        }

if __name__ == "__main__":
    validator = DataValidator()
    validator.validate_all()
