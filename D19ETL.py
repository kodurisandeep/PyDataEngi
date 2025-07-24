import logging, json
import pandas as pd
from datetime import datetime
from google.cloud import storage, bigquery, pubsub_v1
from pythonjsonlogger import jsonlogger
import time
from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
client.setup_logging()  # Adds Cloud Logging handler

# ---------- Structured Logging Setup ----------
logger = logging.getLogger("structuredLogger")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s %(pipeline_step)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# ---------- GCP Clients Setup ----------
PROJECT_ID = "tranquil-post-461304-m7"
BUCKET_NAME = "log-etl-errors"  # ensure this exists
BLOB_NAME = "failed-records.json"
BQ_TABLE = f"{PROJECT_ID}.etl_logs.failed_records"
TOPIC_ID = "etl-alerts"
TOPIC_PATH = pubsub_v1.PublisherClient().topic_path(PROJECT_ID, TOPIC_ID)

storage_client = storage.Client()
bigquery_client = bigquery.Client()
publisher = pubsub_v1.PublisherClient()

# ---------- Mock Data ----------
product_df = pd.DataFrame([
    {"product_id": 101, "name": "Laptop"},
    {"product_id": None, "name": "Broken Record"},  # This will fail validation
    {"product_id": 103, "name": "Tablet"}
])

# ---------- Failure Handlers ----------
def save_to_gcs(record):
    blob = storage_client.bucket(BUCKET_NAME).blob(BLOB_NAME)
    existing = blob.download_as_text() if blob.exists() else ""
    new_content = existing + json.dumps(record) + "\n"
    blob.upload_from_string(new_content, content_type="application/json")

def write_to_bigquery(record):
    bigquery_client.insert_rows_json(BQ_TABLE, [record])

def publish_alert(message):
    data = json.dumps({"alert": message}).encode("utf-8")
    publisher.publish(TOPIC_PATH, data=data)

# ---------- ETL Processing ----------
for index, row in product_df.iterrows():
    try:
        logger.info("Processing row", extra={"pipeline_step": "read_row"})
        if pd.isna(row["product_id"]):
            raise ValueError("Missing product_id")

        logger.info("Valid row", extra={"pipeline_step": "validate_row"})

    except Exception as e:
        failed_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "pipeline_step": "validate_row",
            "error_message": str(e),
            "record_payload": row.to_json()
        }

        logger.error("Failure encountered", extra={"pipeline_step": "error_handler"})
        save_to_gcs(failed_record)
        write_to_bigquery(failed_record)
        publish_alert(f"ETL validation failed: {str(e)}")
        time.sleep(1)  # Optional, gives message time to propagate

for handler in logging.getLogger().handlers:
    if hasattr(handler, "flush"):
        handler.flush()
