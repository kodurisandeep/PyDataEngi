import json
import pandas as pd

with open("./dataset_samples/D3_Customer_Orders.json") as f:
    data = json.load(f)

### Flatten the Orders with Customer Info
# This gives you one row per order, with customer details included in each row.
df = pd.json_normalize(
    data,
    record_path=["orders"],
    meta=[
        ["customer", "id"],
        ["customer", "name"],
        ["customer", "email"],
        ["customer", "address", "city"],
        ["customer", "address", "zip"]
    ],
    meta_prefix="",
    errors="ignore"
)
df.columns = df.columns.str.replace(r"\.", "_", regex=True)
#print(df.head())

### 1. Basic Analysis
#Total spend per customer:
df["total_value"] = df["price"] * df["quantity"]
print("Total spend per customer:")
print(df.groupby("customer_id")["total_value"].sum())
#Count of items ordered:
print("Count of items ordered:")
print(df.groupby("customer_name")["item"].count())

### 2. Date-Based Insights
#Filter only delivered orders:
print("Filter only delivered orders:")
print(df[df["delivery_status"] == "Delivered"].head)
#Orders after June 3rd:
print("Orders after June 3rd:")
print(df[pd.to_datetime(df["delivery_date"], errors="coerce") > "2023-06-03"].head)
#Order level audit
df["status_flag"] = df.apply(
    lambda row: "HighValue" if row["total_value"] > 50000
    else ("Pending" if row["delivery_status"] == "Pending" else "Standard"),
    axis=1
)

### 3. Export to Excel
df.to_excel("./dataset_samples/D3_Flattened_Orders.xlsx", index=False)
# Export to multiple sheets in same excel
df_delivered = df[df["delivery_status"] == "Delivered"]
df_pending = df[df["delivery_status"] == "Pending"]
df_shipped = df[df["delivery_status"] == "Shipped"]
with pd.ExcelWriter("./dataset_samples/D3_Flattened_Orders_Split.xlsx") as writer:
    df_delivered.to_excel(writer, sheet_name="Delivered", index=False)
    df_pending.to_excel(writer, sheet_name="Pending", index=False)
    df_shipped.to_excel(writer, sheet_name="Shipped", index=False)

#Summary metrics
summary = {
    "Total Orders": len(df),
    "Unique Customers": df["customer_id"].nunique(),
    "Total Spend": df["total_value"].sum()
}
print(summary)

