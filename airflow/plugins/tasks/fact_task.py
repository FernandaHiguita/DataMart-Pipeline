
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook

@task
def load_fact_sales(_):

    hook = PostgresHook(postgres_conn_id="analytics_db")

    hook.run('''
    INSERT INTO dw.fact_sales(
        invoice_no,
        date_key,
        product_key,
        customer_key,
        country_key,
        quantity,
        unit_price,
        revenue
    )
    SELECT
        s.invoiceno,
        CAST(to_char(s.invoicedate::timestamp,'YYYYMMDD') AS INTEGER),
        p.product_key,
        c.customer_key,
        co.country_key,
        s.quantity,
        s.unitprice,
        s.revenue
    FROM staging.sales_raw s
    JOIN dw.dim_product p
      ON p.stock_code = s.stockcode
    LEFT JOIN dw.dim_customer c
      ON c.customer_id = s.customerid
    JOIN dw.dim_country co
      ON co.country_name = s.country;
    ''')

    return True
