from google.cloud import bigquery
from google.oauth2 import service_account
import json
from src.utils.logging import etl_logger as logger

def get_bq_client(secrets):
    """
    Returns a BigQuery client using either credentials_path or GCP_CLIENT_SECRET.

    Args:
        secrets (dict): Credential input dictionary

    Returns:
        bigquery.Client
    """

    if secrets.get("credentials_path"):
        logger.info("[auth] Using service_account_json from credentials_path")
        return bigquery.Client.from_service_account_json(secrets["credentials_path"])

    elif secrets.get("GCP_CLIENT_SECRET"):
        logger.info("[auth] Using service_account_info from secret payload")
        creds_dict = json.loads(secrets["GCP_CLIENT_SECRET"])
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        return bigquery.Client(credentials=creds)

    else:
        logger.warning("[auth] Falling back to default BigQuery client (ADC)")
        return bigquery.Client()

def load_to_bigquery(df_clean, config, secrets):
    
    try:
        if secrets.get("credentials_path"):
            logger.info("[auth] Using credentials_path")
            client = bigquery.Client.from_service_account_json(secrets["credentials_path"])

        elif secrets.get("GCP_CLIENT_SECRET"):
            logger.info("[auth] Using GCP_CLIENT_SECRET")
            creds_dict = json.loads(secrets["GCP_CLIENT_SECRET"])
            creds = service_account.Credentials.from_service_account_info(creds_dict)
            client = bigquery.Client(credentials=creds)

        else:
            logger.info("[auth] Using default credentials")
            client = bigquery.Client()

    except Exception as auth_error:
        logger.error(f"[auth_error] Failed to create BigQuery client: {auth_error}")
        return {"rows_loaded": 0, "errors": str(auth_error)}

    project_id = client.project
    dataset = config.get("bq_dataset")
    table = config.get("bq_table")
    table_id = f"{project_id}.{dataset}.{table}"
    logger.info(f"[bq_target] Loading to: {table_id}")

    job_config = bigquery.LoadJobConfig(
        write_disposition=config.get("write_mode", "WRITE_APPEND"),
        autodetect=False,
        source_format=bigquery.SourceFormat.CSV
    )

    try:
        job = client.load_table_from_dataframe(df_clean, table_id, job_config=job_config)
        job.result()
        logger.info(f"[loaded] {len(df_clean)} rows to {table_id}")
        return {"rows_loaded": len(df_clean), "errors": None}

    except Exception as e:
        logger.error(f"[load_error] {str(e)}")
        return {"rows_loaded": 0, "errors": str(e)}