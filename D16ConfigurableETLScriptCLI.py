import argparse
import pandas as pd
import os

def run_etl(source_file, output_dir, drop_cols):
    # Step 1: Load data
    df = pd.read_csv(source_file)
    
    # Step 2: Drop unwanted columns
    df_cleaned = df.drop(columns=drop_cols)
    
    # Step 3: Save output
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_data.csv")
    df_cleaned.to_csv(output_path, index=False)
    print(f"✅ Cleaned file saved at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL with argparse")
    parser.add_argument("--source_file", required=True, help="Path to input CSV file")
    parser.add_argument("--output_dir", default="output", help="Directory to save cleaned file")
    parser.add_argument("--drop_cols", nargs="+", default=[], help="List of columns to drop")

    args = parser.parse_args()
    run_etl(args.source_file, args.output_dir, args.drop_cols)