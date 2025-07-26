import json
import pandas as pd
from io import BytesIO
from prefect import flow, task
from prefect_gcp.cloud_storage import GcpCredentials, GcsBucket
from prefect_gcp.bigquery import BigQueryWarehouse
import asyncio
from google.cloud import bigquery

# Tasks (unchanged)
@task
def read_from_gcs(path: str) -> pd.DataFrame:
    gcs = GcsBucket.load("gcs-block")
    data = gcs.read_path(path)
    return pd.read_csv(BytesIO(data))

@task
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df.columns = [col.strip().lower() for col in df.columns]
    return df

@task
def log_metadata(df: pd.DataFrame):
    print(f"✅ Rows: {len(df)}, Columns: {df.columns.tolist()}")

@task
def write_to_bigquery(df: pd.DataFrame):
    creds = GcpCredentials.load("gcp-creds")
    client = creds.get_bigquery_client()
    dataset_id = "sandeep_dataset"
    table_id = "sandeep_table"
    project_id = creds.project
    dataset_ref = bigquery.Dataset(f"{project_id}.{dataset_id}")
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        client.create_dataset(dataset_ref, exists_ok=True)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job = client.load_table_from_dataframe(df, table_ref)
    job.result()

# Flow (unchanged)
@flow(name="GCS → BQ ETL")
def etl_flow():
    df = read_from_gcs("raw/D16_data.csv")
    df_clean = clean_data(df)
    log_metadata(df_clean)
    write_to_bigquery(df_clean)

# Block Registration (runs only on manual execution)
if __name__ == "__main__":
    async def register_blocks():
        with open("C:\\Users\\kodur\\Downloads\\tranquil-post-461304-m7-7a5b75008282.json") as f:
            key_dict = json.load(f)

        creds = GcpCredentials(service_account_info=key_dict)
        await creds.save("gcp-creds", overwrite=True)
        await GcsBucket(bucket="sandeep-data", gcp_credentials=creds).save("gcs-block", overwrite=True)
        await BigQueryWarehouse(gcp_credentials=creds).save("bq-block", overwrite=True)

    asyncio.run(register_blocks())
    etl_flow()