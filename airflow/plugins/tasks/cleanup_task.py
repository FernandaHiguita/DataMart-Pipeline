
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook

@task
def cleanup_stage(_):
    hook = PostgresHook(postgres_conn_id="analytics_db")
    hook.run("TRUNCATE TABLE staging.sales_raw;")
