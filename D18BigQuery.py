import pandas as pd
from pandas_gbq import to_gbq
from google.cloud import bigquery

product_df = pd.DataFrame({
    "product_id": [101, 102, 103],
    "category": ["books", "electronics", "clothing"],
    "price": [250.0, 800.0, 450.0],
    "created_at": ["2023-06-01", "2023-06-02", "2023-06-02"]
})

product_df["created_at"] = pd.to_datetime(product_df["created_at"]).dt.date

pricing_df = pd.DataFrame({
    "product_id": [101, 102, 103],
    "discount": [50.0, 100.0, 75.0]
})

PROJECT_ID = "tranquil-post-461304-m7"
DATASET = "sandeep_dataset"

to_gbq(product_df, f"{DATASET}.product_data", project_id=PROJECT_ID, if_exists="replace")
to_gbq(pricing_df, f"{DATASET}.pricing_data", project_id=PROJECT_ID, if_exists="replace")


client = bigquery.Client()

query = f"""
SELECT 
    p.product_id, p.category, p.price, p.created_at,
    q.discount,
    p.price - q.discount AS final_price
FROM `{PROJECT_ID}.{DATASET}.product_data` p
JOIN `{PROJECT_ID}.{DATASET}.pricing_data` q
ON p.product_id = q.product_id
"""

joined_df = client.query(query).to_dataframe()
print(joined_df.head())

table_id = f"{PROJECT_ID}.{DATASET}.product_data_partitioned"
schema = [
    bigquery.SchemaField("product_id", "INTEGER"),
    bigquery.SchemaField("category", "STRING"),
    bigquery.SchemaField("price", "FLOAT"),
    bigquery.SchemaField("created_at", "DATE"),
]

table = bigquery.Table(table_id, schema=schema)
table.time_partitioning = bigquery.TimePartitioning(field="created_at")
table.clustering_fields = ["category"]

table = client.create_table(table, exists_ok=True)
client.load_table_from_dataframe(product_df, table).result()