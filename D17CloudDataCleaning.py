from prefect import flow, task
import pandas as pd
import gcsfs
from datetime import datetime
from google.oauth2 import service_account

# Service account setup
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(
    filename="C:/Users/kodur/source/repos/PyDataEngi/key.json",
    scopes=SCOPES
)
fs = gcsfs.GCSFileSystem(token=creds)

# Schema expectations
EXPECTED_SCHEMA = {
    "transaction_id": "int64",
    "customer_name": "object",
    "amount": "float64",
    "date": "datetime64[ns]"
}

@task
def load_raw_data(path):
    df = pd.read_csv(f"gs://{path}", storage_options={"token": creds})
    return df

@task
def clean_data(df):
    df.drop_duplicates(inplace=True)
    df['amount'].fillna(0, inplace=True)
    df['customer_name'] = df['customer_name'].str.strip().str.title()
    df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y", errors="coerce")
    return df

@task
def validate_schema(df):
    for col, dtype in EXPECTED_SCHEMA.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
        if str(df[col].dtype) != str(dtype):
            print(f"⚠️ Column '{col}' has type {df[col].dtype}, expected {dtype}")
    print("✅ Schema validation complete.")

@task
def save_cleaned_data(df, bucket_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path_gcs = f"{bucket_path}/cleaned/D16_sales_data_cleaned_{timestamp}.csv"
    with fs.open(path_gcs, 'w') as f:
        df.to_csv(f, index=False)
    print(f"✅ Cleaned data saved to {path_gcs}")

@flow
def gcs_cleaning_pipeline():
    raw_path = "sandeep-data-bucket/raw/D16_sales_data_gcp.csv"
    bucket_base = "sandeep-data-bucket"
    df = load_raw_data(raw_path)
    cleaned = clean_data(df)
    validate_schema(cleaned)
    save_cleaned_data(cleaned, bucket_base)

# Trigger flow
gcs_cleaning_pipeline()