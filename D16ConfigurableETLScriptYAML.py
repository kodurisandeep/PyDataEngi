import yaml
import pandas as pd
import os

def run_etl(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Load data
    df = pd.read_csv(config['source_file'])

    # Clean data
    df_cleaned = df.drop(columns=config['drop_cols'])

    # Save output
    os.makedirs(config['output_dir'], exist_ok=True)
    output_path = os.path.join(config['output_dir'], "cleaned_data.csv")
    df_cleaned.to_csv(output_path, index=False)
    print(f"✅ Cleaned file saved at: {output_path}")

if __name__ == "__main__":
    run_etl("D16ETL_Config.yaml")