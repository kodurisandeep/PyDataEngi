from google.cloud import bigquery

client = bigquery.Client()
dataset_id = "sandeep_dataset"
project_id = "tranquil-post-461304-m7"

tables_to_delete = [
    "product_data",
    "pricing_data",
    "product_data_partitioned"
]

for table in tables_to_delete:
    full_id = f"{project_id}.{dataset_id}.{table}"
    client.delete_table(full_id, not_found_ok=True)
    print(f"Deleted table: {full_id}")

client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
print(f"Deleted dataset: {dataset_id}")