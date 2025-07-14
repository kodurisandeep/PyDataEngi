from ast import Lambda
import pandas as pd
import chardet
import datetime
from dateutil import parser

def logging(message, level="INFO"):
    with open("./dataset_samples/D11_log.log","a") as f:
        f.write(f"[{datetime.datetime.now()}] [{level}] {message}\n")

def correct_date(value):
    if pd.isnull(value):
        return None
    value = str(value).strip().replace(".", "-").replace("/", "-")
    try:
        return parser.parse(value, dayfirst=False)  # dayfirst can be adjusted if needed
    except Exception:
        return None

def detect_outliers_boxplot(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    print(Q1, Q3)
    IQR = Q3 - Q1
    return df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

import re

def clean_text(value):
    value = str(value).lower().strip()
    value = re.sub(r'[^a-z ]', '', value)
    corrections = {
        "cnl": "canal",
        "canl": "canal",
        "canal": "canal",
        "drp": "drip irrigation",
        "drip": "drip irrigation",
        "drip irrigation": "drip irrigation",
        "flood": "flood irrigation",
        "flood irrigation": "flood irrigation",
        "borwell": "borewell",
        "borewell": "borewell",
    }
    return corrections.get(value, value)

def check_mismatch(row):
    expected = {
        "canal": "canal",
        "flood irrigation": "flood irrigation",
        "borewell": "borewell",
        "drip irrigation": "drip irrigation"
    }
    return row["water_source"] in expected and row["irrigation_type"] != expected[row["water_source"]]

with open("./dataset_samples/D11_Irrigation.csv","rb") as f:
    result = chardet.detect(f.read(10000))
logging("Checked encode value of input file")

df = pd.read_csv("./dataset_samples/D11_Irrigation.csv",
              encoding=result["encoding"], engine="python", on_bad_lines="warn")
logging("Created data frame from input file")

df.columns=df.columns.str.strip().str.lower()
logging("Changed column names to lower case")

df["irrigation_type"]=df["irrigation_type"].fillna("NA")
logging("Filled irrigation type column null values with Na")

df["water_depth"]=pd.to_numeric(df["water_depth"],errors="coerce")
logging("Converted water depth column to numeric")

df["water_depth"]=df["water_depth"].fillna(0)
logging("Filled water depth column null values with 0")

df["duplicate_row"]=df.duplicated()
logging("Tag duplicate rows")

for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.strip().str.lower()
logging("Adjusted case, white space for all values")

df["irrigation_type"] = df["irrigation_type"].apply(clean_text)
df["water_source"] = df["water_source"].apply(clean_text)
logging("Standardized irrigation_type and water_source using regex and mapping")

df["cleaned_date"] = df["survey_date"].apply(correct_date)
df["parsed_date"] = pd.to_datetime(df["cleaned_date"], errors="coerce", dayfirst=True)

df["survey_date"] = df["survey_date"].apply(correct_date)
df["survey_date"] = pd.to_datetime(df["survey_date"], errors="coerce", dayfirst=True)


logging(detect_outliers_boxplot(df, "irrigated_area"))
logging(detect_outliers_boxplot(df, "water_depth"))
logging("Detected outliers using IQR Boxplot")

valid_categories_irrigation = ["canal", "flood irrigation", "borewell", "drip irrigation"]

for i, row in df.iterrows():
    if not (2 <= row["water_depth"] <= 100):
        logging(f"Water depth in row {i} is not in range of 2 & 100")

    if row["irrigation_type"] not in valid_categories_irrigation:
        logging(f"Irrigation type in row {i} is not a valid category")

df["mismatch_source_irrigation"] = df.apply(check_mismatch, axis=1)
logging("Applied mismatch logic per row between source and irrigation_type")

df.to_csv("./dataset_samples/D11_Updated.csv", index=False)