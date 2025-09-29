import numpy as np
import pandas as pd

df = pd.read_csv("data/dirty_cafe_sales.csv")

# strip and rename the column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

df = df.dropna(subset=['item', 'transaction_id'])

# replacing missing values with NaNs
df['transaction_date'].replace('UNKNOWN', np.nan, inplace=True)
df['payment_method'].replace('ERROR', np.nan, inplace=True)
df['payment_method'].replace('UNKNOWN', np.nan, inplace=True)

print(df['payment_method'].unique())