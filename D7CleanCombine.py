import pandas as pd
import chardet
import datetime

def logging(message, level="INFO"):
    dt=datetime.datetime.now().strftime("%Y-%m-%d")
    with open(f"./dataset_samples/D7_log_{dt}.txt","a") as f:
        f.write(f"[{datetime.datetime.now()}] [{level}] {message}\n")

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

    #Combine all df
    df_combined = pd.concat([df_csv, df_json, df_par, df_xl, df_xml], ignore_index=True)
    logging("Combined all DataFrames")

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