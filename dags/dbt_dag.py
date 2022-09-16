from datetime import timedelta
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "jared-rimmer",
    "depends_on_past": False,
    "email": ["jared-rimmer@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "dbt_and_great_expectations",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
)


dbt_run = DockerOperator(
    api_version="auto",
    docker_url="tcp://docker-proxy:2375",
    command="run",
    image="custom-dbt",
    network_mode="bridge",
    task_id="dbt_run",
    dag=dag,
)