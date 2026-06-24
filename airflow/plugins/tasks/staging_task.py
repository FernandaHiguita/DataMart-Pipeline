
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from io import StringIO
import pandas as pd

@task
def load_staging(parquet_path):
    df = pd.read_parquet(parquet_path)

    hook = PostgresHook(postgres_conn_id="analytics_db")

    conn = hook.get_conn()
    cur = conn.cursor()

    buffer = StringIO()
    df.to_csv(buffer,index=False,header=False)
    buffer.seek(0)

    cur.execute("TRUNCATE TABLE staging.sales_raw;")

    cur.copy_expert(
        '''
        COPY staging.sales_raw
        FROM STDIN
        WITH CSV
        ''',
        buffer
    )

    conn.commit()
    cur.close()
    conn.close()

    return "staging_loaded"
