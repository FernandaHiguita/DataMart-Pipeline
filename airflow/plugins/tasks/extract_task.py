
from airflow.decorators import task

@task
def extract_sources():
    return {
        "csv_path": "/opt/airflow/data/data.csv",
        "xlsx_path": "/opt/airflow/data/online_retail_II.xlsx"
    }
