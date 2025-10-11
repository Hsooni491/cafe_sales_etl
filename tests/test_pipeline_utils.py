import pandas as pd
import numpy as np
from utils.pipeline_utils import extract_csv, clean_cafe_sales

def test_extract_csv():
    df = extract_csv('data/dirty_cafe_sales.csv')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_clean_cafe_sales():
    raw = pd.DataFrame({
    'Transaction ID': [1, 2],
    'Transaction Date': ['2025-10-09', 'ERROR'],
    'Item': ['Latte', 'UNKNOWN'],
    'Quantity': [1, np.nan],
    'Price Per Unit': [10.0, 5.0],
    'Total Spent': [10.0, np.nan],
    'Location': ['Main', 'UNKNOWN'],
    'Payment Method': ['Card', 'Cash']
})
    cleaned = clean_cafe_sales(raw)
    assert 'day_of_week' in cleaned.columns
    assert cleaned['transaction_date'].dtype == 'datetime64[ns]'

