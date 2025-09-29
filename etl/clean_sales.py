import numpy as np
import pandas as pd

df = pd.read_csv("data/dirty_cafe_sales.csv")

# strip and rename the column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# remove rows with missing values from item and transaction_id column
df = df.dropna(subset=['item', 'transaction_id', 'transaction_date'])

# replacing missing values with NaNs
df['transaction_date'].replace('UNKNOWN', np.nan, inplace=True)
df['payment_method'].replace(['ERROR', 'UNKNOWN'], np.nan, inplace=True)
df['item'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['quantity'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['total_spent'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['price_per_unit'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['location'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['transaction_date'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)

# converting data type 
df['quantity'] = df['quantity'].astype('Int64')
df['item'] = df['item'].astype('category')
df['total_spent'] = df['total_spent'].astype('float64')
df['price_per_unit'] = df['total_spent'].astype('float64')
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

