import pandas as pd
import os
import json
from pandas import json_normalize
import pyarrow.parquet as pq  # Required for Parquet metadata inspection

# 📘 Step 1: CSV → JSON (line-delimited)
df = pd.read_csv('./dataset_samples/D2_Customer_Info_Cleaned.csv', encoding='utf-8')
df.to_json('./dataset_samples/D6_data.json', orient='records', lines=True)

# 🧩 Optional: JSON Pretty Print (non-line format)
df.to_json('./dataset_samples/D6_pretty.json', orient='records', indent=2)

# 📗 Step 2: JSON → CSV
df = pd.read_json('./dataset_samples/D6_data.json', orient='records', lines=True)
df.to_csv('./dataset_samples/D6_data_converted.csv', index=False, encoding='utf-8')

# 📕 Step 3: CSV → Excel
df = pd.read_csv('./dataset_samples/D6_data_converted.csv', encoding='utf-8')
df.to_excel('./dataset_samples/D6_data_converted.xlsx', index=False, sheet_name='Sheet1')

# 📙 Step 4: Excel → CSV
df = pd.read_excel('./dataset_samples/D6_data_converted.xlsx', sheet_name='Sheet1')
df.to_csv('./dataset_samples/D6_data_from_excel.csv', index=False, encoding='utf-8')

# 📒 Step 5: Optional – Read all sheets from multi-sheet Excel file
try:
    sheets = pd.read_excel('./dataset_samples/D6_multi_sheet_file.xlsx', sheet_name=None)
    for sheet_name, sheet_df in sheets.items():
        print(f"\nSheet: {sheet_name}")
        print(sheet_df.head())
except FileNotFoundError:
    print("Multi-sheet Excel file not found. Skipping that part.")

# 📦 Step 6: Parquet Conversion for bonus practice
df.to_parquet('./dataset_samples/D6_data.parquet', index=False)

# 🔍 Step 7: Peek Parquet Metadata
try:
    parquet_metadata = pq.ParquetFile('./dataset_samples/D6_data.parquet').metadata
    print("\n📄 Parquet schema:\n", parquet_metadata.schema)
except Exception as e:
    print("Unable to read Parquet metadata:", e)

# 📊 Step 8: File Size Comparison
paths = [
    './dataset_samples/D6_data.json',
    './dataset_samples/D6_pretty.json',
    './dataset_samples/D6_data_converted.csv',
    './dataset_samples/D6_data_converted.xlsx',
    './dataset_samples/D6_data.parquet'
]

print("\n📦 File size summary:")
for path in paths:
    if os.path.exists(path):
        size_kb = os.path.getsize(path) / 1024
        print(f"{os.path.basename(path)}: {size_kb:.2f} KB")
    else:
        print(f"{path} not found.")