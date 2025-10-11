import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from etl.clean_sales import extract_csv, clean_cafe_sales
import pandas as pd

def test_clean_sales_end_to_end(tmp_path):
    # Create a temporary CSV
    csv_file = tmp_path / "dirty_test.csv"
    pd.DataFrame({
        "Transaction ID": [1, 2],
        "Transaction Date": ["2025-10-09", "ERROR"],
        "Item": ["Latte", "UNKNOWN"],
        "Quantity": [1, None],
        "Price Per Unit": [10.0, 5.0],
        "Total Spent": [10.0, None],
        "Location": ["Main", "UNKNOWN"],
        "Payment Method": ["Card", "Cash"]
    }).to_csv(csv_file, index=False)

    df = extract_csv(str(csv_file))
    cleaned = clean_cafe_sales(df)
    assert not cleaned.empty
    assert "day_of_week" in cleaned.columns
    assert cleaned["quantity"].dtype.name.startswith("Int")
