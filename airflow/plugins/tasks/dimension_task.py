
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook

@task
def load_dimensions(_):

    hook = PostgresHook(postgres_conn_id="analytics_db")

    sql = '''
    INSERT INTO dw.dim_product(stock_code,description)
    SELECT DISTINCT stockcode,description
    FROM staging.sales_raw
    ON CONFLICT DO NOTHING;

    INSERT INTO dw.dim_customer(customer_id)
    SELECT DISTINCT customerid
    FROM staging.sales_raw
    WHERE customerid IS NOT NULL
    ON CONFLICT DO NOTHING;

    INSERT INTO dw.dim_country(country_name)
    SELECT DISTINCT country
    FROM staging.sales_raw
    ON CONFLICT DO NOTHING;
    '''

    hook.run(sql)

    return True

@task
def generate_dim_date():
    return True
