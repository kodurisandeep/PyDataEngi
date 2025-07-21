import logging
import pandas as pd
import sqlite3  # Simulating a DB target

# 🧾 Logging Configuration
logging.basicConfig(
    filename='./dataset_samples/D16_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 📥 Step 1: Read Source Data
def read_csv(path):
    logging.info("Reading source data")
    try:
        df = pd.read_csv(path)
        logging.info(f"Successfully read {len(df)} rows")
        return df
    except FileNotFoundError as fnf:
        logging.error(f"File not found: {fnf}")
        raise
    except Exception as e:
        logging.error(f"Error while reading CSV: {e}")
        raise

# 🔧 Step 2: Transform Data
def clean_data(df):
    logging.info("Transforming data")
    try:
        # Example: Drop nulls and filter invalid rows
        df_clean = df.dropna()
        df_clean = df_clean[df_clean['amount'] > 0]
        logging.info(f"Cleaned data: {len(df_clean)} rows remaining")
        return df_clean
    except KeyError as ke:
        logging.error(f"Missing expected column: {ke}")
        raise
    except Exception as e:
        logging.error(f"Error during transformation: {e}")
        raise

# 📤 Step 3: Load to Target DB
def load_to_db(df, db_path, table_name):
    logging.info("Loading data to database")
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logging.info(f"Loaded {len(df)} records into '{table_name}'")
    except Exception as e:
        logging.error(f"DB load failed: {e}")
        raise
    finally:
        conn.close()
        logging.info("DB connection closed")

# 🚀 Full ETL Orchestration
def run_pipeline():
    logging.info("Pipeline started")
    try:
        df_raw = read_csv("./dataset_samples/D16_sales_data.csv")
        df_clean = clean_data(df_raw)
        load_to_db(df_clean, "./dataset_samples/etl_output.db", "sales_table")
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        # Optional: send alert or write to quarantine
        print("Pipeline terminated due to error.")
    else:
        print("Pipeline ran successfully.")

run_pipeline()