import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

local_tz = pendulum.timezone("America/Phoenix")

with DAG(
    dag_id="dad_jokes_dag",
    start_date=pendulum.datetime(2026, 3, 24, 7, 0, tz=local_tz),
    schedule="0 7 * * *",
    catchup=False,
    tags=["nas", "python"],
) as dag:
    run_dad_jokes = BashOperator(
        task_id="run_dad_jokes",
        bash_command="python3 /mnt/prox-share/github/python-projects/week-projects/dad_jokes/dad_jokes.py",
    )