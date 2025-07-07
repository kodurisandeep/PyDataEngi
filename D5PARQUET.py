import pandas as pd  # Import pandas for DataFrame and file operations
import zipfile
import pyarrow.parquet as pq
import mimetypes

# ✅ Sample DataFrame creation
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Sandeep', 'Aditi', 'Rohan']
})

# ✅ Write DataFrame to a Parquet file (columnar format, efficient for analytics)
df.to_parquet('./dataset_samples/D5_sample.parquet', index=False)

# ✅ Read the Parquet file back into a DataFrame
df_parquet = pd.read_parquet('./dataset_samples/D5_sample.parquet')
print(df_parquet)  # Display contents of Parquet file

# ✅ Write DataFrame to a GZIP-compressed CSV file
df.to_csv('./dataset_samples/D5_compressed_data.csv.gz', index=False, compression='gzip')

# ✅ Read the GZIP-compressed CSV file
df_gzip = pd.read_csv('./dataset_samples/D5_compressed_data.csv.gz', compression='gzip')
print(df_gzip.head())  # Display top rows of GZIP file

# ✅ Define zip compression options: specify filename inside the archive
compression_opts = dict(method='zip', archive_name='nested.csv')

# ✅ Write DataFrame into a ZIP archive containing 'nested.csv'
df.to_csv('./dataset_samples/D5_archive.zip', index=False, compression=compression_opts)


# ✅ Read CSV file from ZIP archive using zip:// protocol
df_zip = pd.read_csv('./dataset_samples/D5_archive.zip')
print(df_zip.head())  # Display top rows of extracted file from ZIP

# Create a zip archive with multiple files
with zipfile.ZipFile('./dataset_samples/D5_multi_archive.zip', 'w') as zipf:
    zipf.write('./dataset_samples/D5_compressed_data.csv.gz', arcname='compressed.csv.gz')
    zipf.write('./dataset_samples/D5_sample.parquet', arcname='data.parquet')
    zipf.write('./dataset_samples/D5_archive.zip', arcname='original_archive.zip')

metadata = pq.ParquetFile('./dataset_samples/D5_sample.parquet').metadata
print(metadata.schema)

file_path = './dataset_samples/D5_compressed_data.csv.gz'
print(mimetypes.guess_type(file_path))