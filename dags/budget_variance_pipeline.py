"""Daily budget variance pipeline.

The order is not negotiable. dbt cannot call an API, so the classification
agent runs as a Python step between two dbt invocations: it reads the invoices
staging left without a category, asks the model, and writes the predictions
back for the marts to pick up.
"""

from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_DIR}/analytics"
DBT = "/home/airflow/dbt-venv/bin/dbt"

with DAG(
    dag_id="budget_variance_pipeline",
    description="Load invoices, classifies those without category and rebuilds the mart models.", 
    start_date=datetime(2026,10,1),
    schedule="0 6 * * *",
    catchup=False,
    tags=['budget', 'invoice', 'variance']
):
    load_raw = BashOperator(
        task_id="load_raw",
        bash_command=f"cd {PROJECT_DIR} && python ingestion/load_raw.py"
    )
    dbt_staging = BashOperator(
        task_id="dbt_staging",
        bash_command=f"cd {DBT_DIR} && {DBT} run --select path:models/staging path:models/intermediate"
    )
    classify_invoices = BashOperator(
        task_id="classify_invoices",
        bash_command=f"cd {PROJECT_DIR} && python -m agent.classify_invoices"
    )
    dbt_marts = BashOperator(
        task_id="dbt_marts",
        bash_command=f"cd {DBT_DIR} && {DBT} run --select path:models/marts",
        # The marts are rebuilt whether or not the agent finished. A token limit
        # or an API outage leaves invoices without a category, and the mart
        # already reports those as their own bucket. It must never hold the report.
        trigger_rule="all_done"
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {DBT} test"
    )

load_raw >> dbt_staging >> classify_invoices >> dbt_marts >> dbt_test