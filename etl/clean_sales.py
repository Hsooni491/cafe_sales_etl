import numpy as np
import pandas as pd

df = pd.read_csv("data/dirty_cafe_sales.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

df = df.dropna(subset=['item', 'transaction_id'])

df['transaction_date'].replace('UNKNOWN', np.nan, inplace=True)

print(df[df['transaction_date'].isna() == True])