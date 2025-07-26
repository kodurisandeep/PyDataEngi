import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument("--config", type=str, default="config/default_config.yaml", help="Path to config file")
    parser.add_argument("--dry-run", action="store_true", help="Run without loading to BigQuery")
    parser.add_argument("--input-blob", type=str, required=True, help="GCS blob to process")
    return parser.parse_args()