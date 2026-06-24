import sys

sys.path.append("/opt/airflow/plugins")

from airflow.decorators import dag
from datetime import datetime


from tasks.extract_task import extract_sources
from tasks.quality_task import data_quality
from tasks.staging_task import load_staging
from tasks.dimension_task import load_dimensions, generate_dim_date
from tasks.fact_task import load_fact_sales
from tasks.cleanup_task import cleanup_stage

@dag(
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
    tags=["etl","retail","dw"]
)
def retail_etl_pipeline():
    raw = extract_sources()
    clean = data_quality(raw)
    stage = load_staging(clean)

    dims = load_dimensions(stage)
    dates = generate_dim_date()

    fact = load_fact_sales(stage)

    cleanup_stage(fact)

retail_etl_pipeline()
