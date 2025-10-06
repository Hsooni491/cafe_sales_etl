import sys
from pathlib import Path
# --- Dynamically add project root to sys.path (must come before imports) ---
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
from utils.pipeline_utils import extract_csv, clean_cafe_sales
import logging

# --- Main script ----
try:
	df = extract_csv('data/dirty_cafe_sales.csv')
	df = clean_cafe_sales(df)
	logging.info('Successfully extracted, transformed.')

except Exception as e:
	logging.error(f'Pipeline failed with error: {e}')

print(df.head())