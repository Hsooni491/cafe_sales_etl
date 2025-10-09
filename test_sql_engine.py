from sqlalchemy import create_engine, text  # <-- add text import

engine = create_engine("postgresql+psycopg2://postgres:4602@localhost:5432/cafe_sales")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Connected successfully!")
        print(result.scalar())
except Exception as e:
    print(f"❌ Connection failed: {e}")
