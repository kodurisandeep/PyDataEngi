import pandas as pd
import chardet
import datetime
import re

standard_columns = ["id", "name", "email", "country"]

def logging(message, level="INFO"):
    dt=datetime.datetime.now().strftime("%Y-%m-%d")
    with open(f"./dataset_samples/D7_log_{dt}.txt","a") as f:
        f.write(f"[{datetime.datetime.now()}] [{level}] {message}\n")

def enforce_column_types(df, source_name):
    expected_types = {
        "id": "Int64",  # pandas nullable integer
        "name": "string",
        "email": "string",
        "country": "string"
    }
    for col, dtype in expected_types.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                logging(f"{source_name}: Failed to cast '{col}' to {dtype} - {str(e)}", level="WARNING")
        else:
            logging(f"{source_name}: Missing expected column '{col}'", level="WARNING")
    return df

def reorder_columns(df, source_name):
    missing_cols = [col for col in standard_columns if col not in df.columns]
    if missing_cols:
        logging(f"{source_name}: Missing columns {missing_cols}", level="WARNING")
        for col in missing_cols:
            df[col] = "NA"  # Fill missing columns with placeholder
    return df[standard_columns]

def validate_email_format(email):
    """
    Validates a single email address against a basic pattern.
    Returns True if valid, False otherwise.
    """
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    email = str(email).strip()
    return bool(re.match(email_pattern, email))

try:

    logging("Fetching encoding value")
    with open("./dataset_samples/D7_customers.csv", "rb") as f:
        result = chardet.detect(f.read(10000))
        logging("Got encoding value")

    df_csv = pd.read_csv("./dataset_samples/D7_customers.csv", on_bad_lines="warn", engine="python", encoding=result["encoding"])
    logging("Read CSV")
    df_csv.to_parquet("./dataset_samples/D7_customers.parquet", index=False)
    logging("Created Parquet")

    df_json = pd.read_json("./dataset_samples/D7_customers.json")
    logging("Read JSON")

    df_par = pd.read_parquet("./dataset_samples/D7_customers.parquet")
    logging("Read Parquet")

    df_xl = pd.read_excel("./dataset_samples/D7_customers.xlsx")
    logging("Read Excel")

    df_xml = pd.read_xml("./dataset_samples/D7_customers.xml")
    logging("Read XML")

    #Verify that all DataFrames (df_csv, df_json, etc.) have the same schema before combining them later
    logging("Verify that all DataFrames (df_csv, df_json, etc.) have the same schema before combining them later")
    logging(df_csv.columns)
    logging(df_json.columns)
    logging(df_par.columns)
    logging(df_xl.columns)
    logging(df_xml.columns)

    #Normalize column names to lowercase and strip whitespace:
    df_csv.columns = df_csv.columns.str.strip().str.lower()
    df_json.columns = df_json.columns.str.strip().str.lower()
    df_par.columns = df_par.columns.str.strip().str.lower()
    df_xl.columns = df_xl.columns.str.strip().str.lower()
    df_xml.columns = df_xml.columns.str.strip().str.lower()
    logging("Normalized column names to lowercase and strip whitespace")

    #Fill NA for empty values
    df_csv=df_csv.fillna("NA")
    df_json=df_json.fillna("NA")
    df_par=df_par.fillna("NA")
    df_xl=df_xl.fillna("NA")
    df_xml=df_xml.fillna("NA")
    logging("Filled NA for empty values")

    #Enforcing column types
    df_csv = enforce_column_types(df_csv, "CSV")
    df_json = enforce_column_types(df_json, "JSON")
    df_par = enforce_column_types(df_par, "Parquet")
    df_xl   = enforce_column_types(df_xl, "Excel")
    df_xml  = enforce_column_types(df_xml, "XML")

    #Column order consistency
    df_csv  = reorder_columns(df_csv, "CSV")
    df_json = reorder_columns(df_json, "JSON")
    df_par  = reorder_columns(df_par, "Parquet")
    df_xl   = reorder_columns(df_xl, "Excel")
    df_xml  = reorder_columns(df_xml, "XML")

    #Combine all df
    df_combined = pd.concat([df_csv, df_json, df_par, df_xl, df_xml], ignore_index=True)
    logging("Combined all DataFrames")

    # Remove exact duplicates
    before = df_combined.shape[0]
    df_combined.drop_duplicates(inplace=True)
    after = df_combined.shape[0]
    logging(f"Removed {before - after} duplicate rows")
    logging("Removed duplicate rows from combined DataFrame")

    # Apply validation function to 'email' column
    df_combined["valid_email"] = df_combined["email"].apply(validate_email_format)

    # Count and log results
    valid_count = df_combined["valid_email"].sum()
    invalid_count = len(df_combined) - valid_count
    logging(f"Email validation completed: {valid_count} valid, {invalid_count} invalid")

    # Replace ID with unique sequence
    df_combined.reset_index(drop=True, inplace=True)
    df_combined["id"] = df_combined.index + 1
    logging("Replaced ID with unique sequence")

    #Create csv from combined df
    df_combined.to_csv("./dataset_samples/D7_final_dataset.csv", index=False)
    logging("Created new file in /dataset_samples/D7_final_dataset.csv")

    print("Done")
except Exception as e:
    logging(f"Failed with error {str(e)}", level="ERROR")
    raise