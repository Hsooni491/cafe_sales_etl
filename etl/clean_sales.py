import numpy as np
import pandas as pd

df = pd.read_csv("data/dirty_cafe_sales.csv")

# strip and rename the column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# remove rows with missing values from item and transaction_id column
df = df.dropna(subset=['item', 'transaction_id'])

# replacing missing values with NaNs
df['transaction_date'].replace('UNKNOWN', np.nan, inplace=True)
df['payment_method'].replace(['ERROR', 'UNKNOWN'], np.nan, inplace=True)
df['item'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['quantity'].replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
df['item'] = df['item'].astype('category')


# This line cause a ValueError, 'cannot convert float Nan to int' (I'll edit it later)
df['quantity'] = df['quantity'].astype('int')


print(df['quantity'].unique())