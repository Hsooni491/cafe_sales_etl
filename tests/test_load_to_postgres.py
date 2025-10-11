import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.pipeline_utils import load_to_postgres
import pandas as pd
from sqlalchemy import create_engine

def test_load_to_postgres(monkeypatch):
    df = pd.DataFrame({
        "transaction_id": [1],
        "transaction_date": ["2025-10-09"],
        "item": ["Latte"],
        "quantity": [1],
        "price_per_unit": [10.0],
        "total_spent": [10.0],
        "location": ["Main"],
        "payment_method": ["Card"],
        "day_of_week": ["Thursday"]
    })

    load_to_postgres(df, table_name="test_sales")
    engine = create_engine("postgresql+psycopg2://postgres:4602@localhost:5432/cafe_sales")
    with engine.connect() as conn:
        result = conn.execute("SELECT COUNT(*) FROM test_sales")
        assert result.scalar() == 1
