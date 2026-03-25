from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dad_jokes_dag",
    start_date=datetime(2026, 3, 24),
    schedule=None,
    catchup=False,
    tags=["nas", "python"],
) as dag:
    run_dad_jokes = BashOperator(
        task_id="run_dad_jokes",
        bash_command="python3 /mnt/prox-share/github/python-projects/week-projects/dad_jokes/dad_jokes.py",
    )