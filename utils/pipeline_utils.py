import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError



def extract_csv(file_name: str) -> pd.DataFrame:
	'''Reads a CSV file and returns a Dataframe'''
	df = pd.read_csv(file_name)
	return df


def clean_cafe_sales(df: pd.DataFrame) -> pd.DataFrame:
	'''Cleans and preprocesses the cafe sales data'''

	# strip and rename the column names
	df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')


	# replacing missing values with NaNs
	cols_to_clean = [
		'transaction_date', 'payment_method', 'item', 'quantity',
		'total_spent', 'price_per_unit', 'location', 'transaction_date'
		]
	for col in cols_to_clean:
		df[col] = df[col].replace(['UNKNOWN', 'ERROR'], np.nan)


	# remove rows with missing values from the following columns
	df = df.dropna(subset=[
		'transaction_id', 'item', 'quantity', 'transaction_date', 'price_per_unit'
		])
	
	# converting data type 
	df = df.astype({
		'quantity': 'Int64',
		'item': 'category',
		'total_spent': 'float64',
		'payment_method': 'category',
		'location': 'category'
	})
	df['transaction_date'] = pd.to_datetime(df['transaction_date'])

	# creating a new column 'day_of_week' from 'transaction_date'
	df['day_of_week'] = df['transaction_date'].dt.day_name().astype('category')

	return df


def load_to_postgres(df: pd.DataFrame, table_name: str = 'sales_data'):
    """Loads DataFrame into PostgreSQL table safely using SQLAlchemy engine."""
    try:
        engine = create_engine("postgresql+psycopg2://postgres:4602@localhost:5432/cafe_sales")

        with engine.begin() as conn:
            df.to_sql(table_name, con=conn, if_exists='replace', index=False)

        row_count = len(df)
        print(f"✅ Loaded {row_count} rows into PostgreSQL table: {table_name}")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to load data into PostgreSQL: {e}")

