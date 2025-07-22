from google.oauth2 import service_account
import gcsfs
import pandas as pd
from datetime import datetime

# Define expected schema
EXPECTED_COLUMNS = {
    "transaction_id": "int64",
    "customer_name": "object",
    "amount": "float64",
    "date": "object"
}

# Load credentials
scopes = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(
    filename="C:/Users/kodur/source/repos/PyDataEngi/key.json",
    scopes=scopes
)

# Initialize GCS filesystem
fs = gcsfs.GCSFileSystem(token=creds)

try:
    # Read CSV from GCS
    df = pd.read_csv("gs://sandeep-data-bucket/raw/D16_sales_data_gcp.csv", storage_options={"token": creds})
    print("✅ CSV loaded successfully.")

    # 🔍 Schema Validation
    def validate_schema(df, expected):
        for col, dtype in expected.items():
            if col not in df.columns:
                raise ValueError(f"❌ Missing expected column: {col}")
            if df[col].dtype != dtype:
                raise TypeError(f"❌ Column '{col}' type mismatch: expected {dtype}, got {df[col].dtype}")
        print("✅ Schema validation passed.")

    validate_schema(df, EXPECTED_COLUMNS)

    # Save locally as Parquet
    df.to_parquet("./dataset_samples/D16_sales_data_gcp.parquet", engine="pyarrow", index=False)
    print("✅ Parquet file saved locally.")

    # Upload to GCS with versioning
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path_gcs = f"sandeep-data-bucket/converted/D16_sales_data_v{timestamp}.parquet"

    with fs.open(path_gcs, 'wb') as f:
        df.to_parquet(f, engine="pyarrow", index=False)
    print("✅ Parquet file uploaded to GCS.")

    # Folder audit
    for folder in ["raw", "cleaned", "converted"]:
        full_path = f"sandeep-data-bucket/{folder}"
        exists = fs.exists(full_path)
        print(f"{folder} exists: {exists}")
        if exists:
            files = fs.ls(full_path)
            print(f"Files in {folder}:")
            for item in files:
                if not fs.isdir(item):
                    print("  -", item)
            print("-" * 40)

except Exception as e:
    print(f"🚨 Error encountered: {e}")