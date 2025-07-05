import pandas as pd

###Step 1: Load Excel
df = pd.read_excel("./dataset_samples/D2_Customer_Info.xlsx")
print(df.head())

###Step 2: Data Quality Checks
#Validate Age
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
#print(df["Age"])
df["AgeValid"] = df["Age"].between(18, 99)
#Validate Email Structure (basic check)
df["EmailValid"] = df["Email"].str.contains(r"^[^@]+@[^@]+\.[^@]+$", na=False)
# Clean PurchaseAmount
df["PurchaseAmount"] = (
    df["PurchaseAmount"]                 # Original column (could be mixed types)
    .astype(str)                         # Convert everything to string
    .str.replace(",", "", regex=False)   # Remove commas (like "12,500" → "12500")
    .replace("N/A", pd.NA)               # Turn "N/A" into a proper missing value
    .astype(float)                       # Convert to float for numeric operations
)

###Step 3: Transformation
#Trim whitespace from names:
df["Name"] = df["Name"].str.strip()
#Convert JoinDate to datetime:
df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors="coerce")
#Flag old joiners (before 2022):
df["JoinedBefore2022"] = df["JoinDate"] < pd.Timestamp("2022-01-01")

###Step 4: Export Cleaned Data
df.to_excel("./dataset_samples/D2_Customer_Info_Cleaned.xlsx", index=False)
df.to_csv("./dataset_samples/D2_Customer_Info_Cleaned.csv", index=False, encoding="utf-8")

###Step 5: Data Filtering & Segmentation
#Customers with valid emails and joined after 2022:
df_filtered = df[df["EmailValid"] & (df["JoinDate"] > "2022-01-01")]
#High-value customers (PurchaseAmount > ₹10,000):
df_high_value = df[df["PurchaseAmount"] > 10000]

###Step 6: Handling Missing Data
#Fill missing ages with median:
df["Age"] = df["Age"].fillna(df["Age"].median())
#Drop rows with missing JoinDate:
df = df.dropna(subset=["JoinDate"])

###Step 7: Feature Engineering (Mini Preview of Day 3)
#Customer tenure in days:
df["DaysSinceJoin"] = (pd.Timestamp("now") - df["JoinDate"]).dt.days
#Month of joining:
df["JoinMonth"] = df["JoinDate"].dt.month
df["JoinMonthName"] = df["JoinDate"].dt.strftime("%B")
df["JoinMonName"] = df["JoinDate"].dt.strftime("%b")

###Step 8: Final Export with Audit Columns
df["DataStatus"] = df["EmailValid"] & df["AgeValid"]

df.to_excel("./dataset_samples/D2_Customer_Info_Final.xlsx", index=False)
df_filtered.to_excel("./dataset_samples/D2_Customer_Info_Filtered.xlsx", index=False)

print(df.head())