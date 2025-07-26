from google.cloud import storage
import pandas as pd
from io import StringIO

def read_gcs_file(bucket_name: str, blob_name: str) -> pd.DataFrame:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    data = blob.download_as_bytes()
    df = pd.read_csv(StringIO(data.decode("utf-8")))
    df["txn_date"] = pd.to_datetime(df["txn_date"], format="%d-%m-%Y", errors="coerce")
    return df