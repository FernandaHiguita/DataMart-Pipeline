
from airflow.decorators import task
import pandas as pd

@task
def data_quality(paths):
    csv_df = pd.read_csv(paths["csv_path"])
    xlsx_df = pd.read_excel(paths["xlsx_path"])

    df = pd.concat([csv_df, xlsx_df], ignore_index=True)

    df.columns = [c.lower().strip() for c in df.columns]

    df = df.drop_duplicates(
        subset=["invoiceno","stockcode","invoicedate"]
    )

    df = df[df["quantity"] != 0]
    df = df[df["unitprice"] >= 0]

    df["revenue"] = df["quantity"] * df["unitprice"]

    output = "/tmp/sales_clean.parquet"
    df.to_parquet(output,index=False)

    return output
