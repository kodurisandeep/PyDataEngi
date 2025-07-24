from google.cloud import bigquery, pubsub_v1

client = bigquery.Client()
project_id = "tranquil-post-461304-m7"
dataset_id = "etl_logs"
full_dataset_id = f"{project_id}.{dataset_id}"

# Step 1: Create Dataset if Needed
dataset = bigquery.Dataset(full_dataset_id)
dataset.location = "asia-south1"  # or your preferred region
client.create_dataset(dataset, exists_ok=True)
print(f"Dataset created: {full_dataset_id}")

# Step 2: Create Table
table_id = f"{full_dataset_id}.failed_records"
schema = [
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("pipeline_step", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("error_message", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("record_payload", "STRING", mode="NULLABLE"),
]

table = bigquery.Table(table_id, schema=schema)
client.create_table(table, exists_ok=True)
print(f"Created table: {table.project}.{table.dataset_id}.{table.table_id}")

# Step 3: Create Pub/Sub Topic
topic_id = "etl-alerts"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Topic created: {topic.name}")
except Exception as e:
    if "ALREADY_EXISTS" in str(e):
        print("Topic already exists.")
    else:
        raise e