from src.utils.config_loader import load_config
from src.utils.secrets_loader import load_secrets_from_gcp
from src.utils.validation import validate_records
from src.utils.logging import etl_logger as logger
from src.transform import transform_data
from src.extract import read_gcs_file
from src.upload import write_to_gcs
import json
import pandas as pd
from cli import parse_args
from src.load import load_to_bigquery

#args = parse_args()

def main():
    # Load config
    config = load_config("config/default_config.yaml")
    
    # Setup logger
    logger.setLevel(config.get("log_level", "INFO"))
    logger.info("Starting ETL flow", extra={"step": "init"})

    # Load secrets securely
    secrets = load_secrets_from_gcp(
        secret_names=["GCP_CLIENT_SECRET"],
        project_id=config["project_id"]
    )
    logger.info("Secrets loaded", extra={"step": "init"})

    # Extract data
    df_raw = read_gcs_file(config["input_bucket"], config["input_blob"])
    logger.info("Data extracted", extra={"step": "extract", "records": len(df_raw)})

    # Validate records  
    with open("config/schema_config.json") as f:
        schema = json.load(f)

    # Prepare df for validation
    df_raw["txn_date"] = pd.to_datetime(df_raw["txn_date"], format="%d-%m-%Y", errors="coerce")
    df_raw["txn_date"] = df_raw["txn_date"].dt.date.astype(str)
    df_raw["item_count"] = df_raw["item_count"].astype(int)
    df_raw["total_amount"] = df_raw["total_amount"].astype(float)
    df_raw["customer_id"] = df_raw["customer_id"].astype(str)

    # Validate
    df_valid, df_invalid = validate_records(df_raw, schema)

    logger.info("Validation complete", extra={
        "step": "validate",
        "valid": len(df_valid),
        "invalid": len(df_invalid),
    })

    # Transform valid data
    df_clean = transform_data(df_valid)
    logger.info("Transformation complete", extra={"step": "transform"})

    # Dry-run logic
    if config["dry_run"]:
        logger.warning("Dry run enabled — skipping load step", extra={"step": "load"})
        print(df_clean.head(3))
    else:
        #Upload to GCP bucket
        output_blob = "cleaned/D16_data_cleaned.csv"
        write_to_gcs(config["output_bucket"], output_blob, df_clean.to_csv(index=False))
        logger.info("Written to GCS", extra={"blob": output_blob, "bucket": config["output_bucket"]})

        # Placeholder for BigQuery loader
        logger.info("Ready to load data", extra={"step": "load", "records": len(df_clean)})
        load_to_bigquery(df_clean, config, secrets)

if __name__ == "__main__":
    main()