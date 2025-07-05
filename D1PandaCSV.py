import pandas as pd
import chardet

# Detect the file's encoding using the chardet library
with open("dataset_samples/iris_malformed.csv", 'rb') as f:
    result = chardet.detect(f.read(100000))  # Read first 100KB for analysis
    print(result)

# Use the detected encoding dynamically
# 'on_bad_lines' handles malformed rows during parsing (e.g., skip or warn)
# 'engine="python"' is more tolerant and pairs well with 'on_bad_lines'
# 'df.head()' returns the first 5 rows; 'print(df)' shows a truncated view (top and bottom)
df = pd.read_csv(
    "dataset_samples/iris_malformed.csv",
    encoding=result['encoding'],
    sep=",",
    on_bad_lines="warn",
    engine="python"
)
#print(df.head())
#print(df['SepalLength'])
for col in ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
#print(df["SepalWidth"].median())
print(df.head())
df["SepalWidth"] = df["SepalWidth"].fillna(df["SepalWidth"].median())
print(df.describe())
df = df.rename(columns={
    "SepalWidth": "SepalWidth2"
})
print(df.head())
