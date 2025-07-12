import pandas as pd

# Simulate messy raw data
data = {
    'custID': [101, 102, 103],
    'Amt': ['2500.50', '1800', 'NaN'],
    'orderDt': ['2025-07-12', '2025-07-13', '2025-07-14'],
}
df = pd.DataFrame(data)

print("🧾 BEFORE normalization:")
df.info()
print(df.head(), '\n')

# ✅ Step 1: Rename columns
df.rename(columns={
    'custID': 'customer_id',
    'orderDt': 'order_date',
    'Amt': 'amount'
}, inplace=True)

# ✅ Step 2: Reorder columns for clarity
desired_order = ['customer_id', 'order_date', 'amount']
df = df[desired_order]

# ✅ Step 3: Clean and infer types
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Coerce 'NaN' safely
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# ✅ Step 4: Use convert_dtypes() if you want full inference
df = df.convert_dtypes()

print("✅ AFTER normalization:")
df.info()
print(df.head())