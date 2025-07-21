import pandas as pd

# Example: read a CSV from 'raw'
file_path = 'gs://sandeep-data-bucket/raw/sample.csv'

df = pd.read_csv(file_path, storage_options={"token": "cloud"})
print(df.head())