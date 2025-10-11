import pandas as pd
import numpy as np
import pandas as pd
import pandas as pd
import psycopg2
from psycopg2 import sql

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

import pandas as pd
import psycopg2
from psycopg2 import sql

def load_to_postgres(df: pd.DataFrame, table_name: str = "sales_data"):
    """Safe PostgreSQL loader using psycopg2 with automatic BIGINT handling."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="cafe_sales",
            user="postgres",
            password="4602"
        )
        cur = conn.cursor()

        # ✅ Drop old table
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))

        # ✅ Create table dynamically with smart type detection
        create_stmt = "CREATE TABLE {} (".format(table_name)
        cols = []
        for col, dtype in df.dtypes.items():
            dtype_str = str(dtype)

            if "int" in dtype_str:
                # Automatically choose BIGINT for large numbers
                if df[col].abs().max() > 2_147_483_647:
                    col_type = "BIGINT"
                else:
                    col_type = "INTEGER"
            elif "float" in dtype_str:
                col_type = "FLOAT"
            elif "datetime" in dtype_str:
                col_type = "TIMESTAMP"
            else:
                col_type = "TEXT"
            cols.append(f"{col} {col_type}")
        create_stmt += ", ".join(cols) + ");"
        cur.execute(create_stmt)

        # ✅ Insert rows
        cols_str = ", ".join(df.columns)
        values_template = ", ".join(["%s"] * len(df.columns))
        insert_stmt = f"INSERT INTO {table_name} ({cols_str}) VALUES ({values_template})"

        data = [tuple(x) for x in df.to_numpy()]
        cur.executemany(insert_stmt, data)

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ Loaded {len(df)} rows into PostgreSQL table: {table_name}")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to load data into PostgreSQL: {e}")
