"""
DAG: cafe_sales_etl
Author: Alhussain Baaalawi
Description:
    Full ETL workflow for café sales data — extracts raw CSV,
    cleans and loads it into PostgreSQL, validates data quality,
    runs SQL-based reports, and generates visual plots.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path
import sys


# -------------------------------------------------------------------
# 1️⃣  Setup: make project root importable
# -------------------------------------------------------------------
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from utils.pipeline_utils import extract_csv, clean_cafe_sales, load_to_postgres


# -------------------------------------------------------------------
# 2️⃣  Default DAG arguments
# -------------------------------------------------------------------
default_args = {
    "start_date": datetime(2025, 10, 10),
    "retries": 1,
}


# -------------------------------------------------------------------
# 3️⃣  Task functions
# -------------------------------------------------------------------

def extract_task(**context):
    """Extract raw CSV and push as JSON to XCom."""
    data_path = root_path / "data" / "dirty_cafe_sales.csv"
    df = extract_csv(data_path)
    context["ti"].xcom_push(key="raw_df", value=df.to_json())



def clean_task(**context):
    """Clean raw DataFrame and push cleaned JSON."""
    import pandas as pd
    raw_json = context["ti"].xcom_pull(key="raw_df")
    df = pd.read_json(raw_json)
    cleaned_df = clean_cafe_sales(df)
    context["ti"].xcom_push(key="clean_df", value=cleaned_df.to_json())


def load_task(**context):
    """Load cleaned data into PostgreSQL (Airflow-safe)."""
    import pandas as pd
    import io
    import json
    from utils.pipeline_utils import load_to_postgres

    # Pull the cleaned JSON string from XCom
    clean_json = context["ti"].xcom_pull(key="clean_df")

    # ✅ Wrap in StringIO (Pandas 2.2 requires it)
    df = pd.read_json(io.StringIO(clean_json))

    # ✅ Ensure DataFrame is valid before loading
    if df.empty:
        raise ValueError("❌ DataFrame is empty — nothing to load.")

    # ✅ Explicitly call your safe load_to_postgres()
    load_to_postgres(df)



def validate_data_task():
    """Check that table exists, has rows, and no NULL total_spent."""
    from sqlalchemy import create_engine, text

    engine = create_engine("postgresql+psycopg2://postgres:4602@localhost:5432/cafe_sales")

    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM sales_data")).scalar()
        if count == 0:
            raise ValueError("❌ Validation failed: no rows in sales_data.")

        nulls = conn.execute(
            text("SELECT COUNT(*) FROM sales_data WHERE total_spent IS NULL")
        ).scalar()
        if nulls > 0:
            raise ValueError("❌ Validation failed: NULL total_spent values found.")

        print(f"✅ Validation passed: {count} rows, 0 nulls in total_spent.")


def run_sql_reports():
    """Execute all SQL queries in /sql_queries and save CSV outputs."""
    from sqlalchemy import create_engine, text
    import pandas as pd
    import os

    engine = create_engine("postgresql+psycopg2://postgres:4602@localhost:5432/cafe_sales")
    sql_dir = root_path / "sql_queries"
    reports_dir = root_path / "reports"
    reports_dir.mkdir(exist_ok=True)

    # ✅ Use a connection context — this solves the 'cursor' error
    with engine.connect() as conn:
        for file in os.listdir(sql_dir):
            if file.endswith(".sql"):
                qpath = sql_dir / file
                qname = file.replace(".sql", "")
                with open(qpath) as f:
                    query = f.read()

                # ✅ Wrap in text() and pass connection explicitly
                result = conn.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())

                df.to_csv(reports_dir / f"{qname}.csv", index=False)
                print(f"✅ Report saved: {qname}.csv")



def create_plots():
    """Generate plots from report CSVs."""
    import pandas as pd
    import matplotlib.pyplot as plt

    reports_dir = root_path / "reports"
    plots_dir = root_path / "plots"
    plots_dir.mkdir(exist_ok=True)

    for file in reports_dir.glob("*.csv"):
        df = pd.read_csv(file)
        plt.figure(figsize=(8, 5))

        # Choose plot type automatically
        if "revenue" in df.columns:
            df.plot(kind="bar", x=df.columns[0], y="revenue", legend=False, title=file.stem)
        elif "daily_revenue" in df.columns:
            df.plot(kind="line", x=df.columns[0], y="daily_revenue", marker="o", title=file.stem)
        else:
            df.plot(kind="bar", legend=False, title=file.stem)

        plt.tight_layout()
        plot_path = plots_dir / f"{file.stem}.png"
        plt.savefig(plot_path)
        plt.close()
        print(f"✅ Plot generated: {plot_path}")


# -------------------------------------------------------------------
# 4️⃣  Define DAG and tasks
# -------------------------------------------------------------------
with DAG(
    dag_id="cafe_sales_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="Full ETL pipeline for Cafe Sales data",
) as dag:

    extract = PythonOperator(
        task_id="extract_csv",
        python_callable=extract_task,
        provide_context=True,
    )

    clean = PythonOperator(
        task_id="clean_data",
        python_callable=clean_task,
        provide_context=True,
    )

    load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_task,
        provide_context=True,
    )

    validate = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data_task,
    )

    sql_reports = PythonOperator(
        task_id="generate_reports",
        python_callable=run_sql_reports,
    )

    plot = PythonOperator(
        task_id="generate_plots",
        python_callable=create_plots,
    )

    # Task dependencies
    extract >> clean >> load >> validate >> sql_reports >> plot
