import numpy as np
import pandas as pd

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
		df[col].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)


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

# --- Main script ----
df = extract_csv('data/dirty_cafe_sales.csv')
df = clean_cafe_sales(df)

print(df.head())