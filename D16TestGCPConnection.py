from google.oauth2 import service_account
import gcsfs
import pandas as pd
from datetime import datetime

# Define required scopes
#scopes = ['https://www.googleapis.com/auth/devstorage.read_write']
scopes = ['https://www.googleapis.com/auth/cloud-platform']


# Load credentials with scopes
creds = service_account.Credentials.from_service_account_file(
    filename="C:/Users/kodur/source/repos/PyDataEngi/key.json",
    scopes=scopes
)

# Use credentials in gcsfs
fs = gcsfs.GCSFileSystem(token=creds)

# List contents of your bucket (testing read access)
print(fs.ls("sandeep-data-bucket"))

# Now read a CSV using pandas + GCS
df = pd.read_csv("gs://sandeep-data-bucket/raw/D16_sales_data_gcp.csv", storage_options={"token": creds})
print(df.head())