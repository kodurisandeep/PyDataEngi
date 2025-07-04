import pandas as pd
import csv
from datetime import datetime

# === CONFIG ===
source_file = "dataset_samples/iris_malformed.csv"
bad_rows_file = "dataset_samples/iris_malformed_bad.csv"
log_file = "dataset_samples/d1csvlog_log.txt"

# === LOGGING SETUP ===
def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%b-%d %H:%M:%S %p")
    with open(log_file, "a") as log_f:
        log_f.write(f"[{timestamp}] [{level}] {message}\n")

# === QUOTE CHECK UTILITY ===
def has_unbalanced_quotes(line: str) -> bool:
    return line.count('"') % 2 != 0

# === START PROCESSING ===
log(f"Starting data parsing for file: {source_file}")

good_rows = []
bad_rows = []
total_rows = 0

try:
    with open(source_file, "r", encoding="utf-8") as infile:
        headers = infile.readline().strip().split(",")
        for idx, line in enumerate(infile, start=2):
            total_rows += 1
            clean_line = line.strip()
            if has_unbalanced_quotes(clean_line):
                row = clean_line.split(",")
                bad_rows.append((idx, row))
                log(f"Line {idx} has unbalanced quotes: {clean_line}", level="WARN")
            else:
                row = clean_line.split(",")
                if len(row) != len(headers):
                    bad_rows.append((idx, row))
                    log(f"Line {idx} has incorrect column count: {clean_line}", level="WARN")
                else:
                    good_rows.append(row)
except Exception as e:
    log(f"Failed to process file: {str(e)}", level="ERROR")
    raise

# === SAVE GOOD DATA ===
df = pd.DataFrame(good_rows, columns=headers)
log(f"Parsed {len(good_rows)} good rows successfully")

# === SAVE BAD ROWS ===
if bad_rows:
    with open(bad_rows_file, "w", encoding="utf-8", newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(headers)
        for _, row in bad_rows:
            writer.writerow(row)
    log(f"{len(bad_rows)} bad rows saved to: {bad_rows_file}")
else:
    log("No bad rows detected")

# === SUMMARY ===
log(f"Total rows read: {total_rows}")
log("Parsing complete\n")
print(*good_rows, sep="\n")