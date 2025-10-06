import sys
from pathlib import Path

# --- Dynamically add project root to sys.path (must come before imports) ---
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from utils.pipeline_utils import extract_csv, clean_cafe_sales
import logging

logs_dir = root_path / "logs" # this points to your logs folder
log_file = logs_dir / "pipeline.log" # this is the log file path

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	handlers=[
		logging.StreamHandler(),
		logging.FileHandler(log_file, mode='a')
	]
)

# --- Main script ----
try:
	df = extract_csv('data/dirty_cafe_sales.csv')
	df = clean_cafe_sales(df)
	logging.info('Successfully extracted, transformed.')

except Exception as e:
	logging.error(f'Pipeline failed with error: {e}')

print(df.head())