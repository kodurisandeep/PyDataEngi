from datetime import datetime
import pandas as pd
import pytz
from zoneinfo import ZoneInfo

def parse_date_with_formats(date_str):
    formats = [
        '%d-%m-%Y',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%b %d, %Y',
        '%Y-%m-%dT%H:%M:%SZ'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # If nothing matches

# Sample date strings in various formats
dates = ['12-07-2025', '2025/07/12', 'Jul 12, 2025', '2025-07-12T09:20:00Z']

# Convert to datetime using pandas (auto handles many formats)
df = pd.DataFrame({'raw_date': dates})
df['standardized_date'] = df['raw_date'].apply(lambda x: parse_date_with_formats(x))

print(df[['raw_date', 'standardized_date']])

# Sample mixed format dates
data = {
    'raw_date': [
        '12-07-2025',      # DD-MM-YYYY
        '2025/07/12',      # YYYY/MM/DD
        'Jul 12, 2025',    # Month day, year
        '2025-07-12T09:20:00Z',  # ISO 8601
        '07-12-2025',      # MM-DD-YYYY (ambiguous!)
        '2025.07.12'       # YYYY.MM.DD (less common)
    ]
}

df = pd.DataFrame(data)

# Use to_datetime with errors='coerce' for flexibility
df['standardized_date'] = pd.to_datetime(df['raw_date'], errors='coerce', dayfirst=True)

print(df)

dt = datetime(2025, 7, 12, 9, 20)
local_tz = pytz.timezone('Asia/Kolkata')
utc_tz = pytz.UTC

# Localize and convert
localized_dt = local_tz.localize(dt)
utc_dt = localized_dt.astimezone(utc_tz)

print("Local:", localized_dt)
print("UTC:", utc_dt)

dt = datetime(2025, 7, 12, 9, 20)
dt_local = dt.replace(tzinfo=ZoneInfo('Asia/Kolkata'))
dt_utc = dt_local.astimezone(ZoneInfo('UTC'))

print("Local:", dt_local)
print("UTC:", dt_utc)

# Sample log line
log_line = "2025-07-12T04:25:30Z INFO User login successful from IP 192.168.0.1"

# Step 1: Extract timestamp (we'll keep it simple)
timestamp_str = log_line.split()[0]

# Step 2: Parse as UTC datetime
dt_utc = pd.to_datetime(timestamp_str, utc=True)

# Step 3: Convert to local timezone (e.g., Asia/Kolkata)
dt_local = dt_utc.tz_convert(ZoneInfo("Asia/Kolkata"))

# Step 4: Print both
print(f"UTC : {dt_utc}")
print(f"Local: {dt_local}")
print(f"Local: {dt_utc.astimezone(ZoneInfo('Asia/Kolkata'))}")
