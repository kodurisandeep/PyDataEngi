from google.cloud import storage

def write_to_gcs(bucket_name: str, blob_name: str, content: str):
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(blob_name)
    blob.upload_from_string(content)
