import numpy as np
import pandas as pd

df = pd.read_csv("data/dirty_cafe_sales.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print(df.describe())
df = df.dropna(subset=['item', 'transaction_id'])

print(df['payment_method'].isnull().sum())

df['transaction_date'].replace('UNKNOWN', np.nan, inplace=True)