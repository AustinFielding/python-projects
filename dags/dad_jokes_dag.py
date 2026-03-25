import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

# America/Phoenix = Arizona local time (no DST; always MST).
with DAG(
    dag_id="dad_jokes_dag",
    start_date=pendulum.datetime(2026, 3, 24, tz="America/Phoenix"),
    schedule="0 7 * * *",
    catchup=False,
    timezone=pendulum.timezone("America/Phoenix"),
    tags=["nas", "python"],
) as dag:
    run_dad_jokes = BashOperator(
        task_id="run_dad_jokes",
        bash_command="python3 /mnt/prox-share/github/python-projects/week-projects/dad_jokes/dad_jokes.py",
    )