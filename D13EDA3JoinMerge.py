import pandas as pd

# 🔹 Sample DataFrames for merge
df_customers = pd.DataFrame({
    'CustomerID': [1, 2, 3],
    'Name': ['Sandeep', 'Arjun', 'Priya']
})

df_orders = pd.DataFrame({
    'CustomerID': [2, 3, 4],
    'OrderAmount': [250, 400, 150]
})

# 🔄 SQL-style joins
inner_join = pd.merge(df_customers, df_orders, on='CustomerID', how='inner')
print("🔸 Inner Join (Matching IDs):")
print(inner_join)

left_join = pd.merge(df_customers, df_orders, on='CustomerID', how='left')
print("\n🔸 Left Join (All customers, matched orders):")
print(left_join)

outer_join = pd.merge(df_customers, df_orders, on='CustomerID', how='outer')
print("\n🔸 Outer Join (All rows from both tables):")
print(outer_join)


# 🔹 Sample DataFrames for concat
df_sales_jan = pd.DataFrame({'Region': ['East', 'West'], 'Sales': [100, 150]})
df_sales_feb = pd.DataFrame({'Region': ['South', 'East'], 'Sales': [120, 160]})

# 📚 Vertical stacking (append rows)
sales_all = pd.concat([df_sales_jan, df_sales_feb], ignore_index=True)
print("\n🔸 Concatenated Sales (Vertical):")
print(sales_all)

region_totals = sales_all.groupby('Region')['Sales'].sum().reset_index()
print("\n🔸 Total Sales by Region (Aggregated):")
print(region_totals)


# 📏 Horizontal stacking (combine columns)
df_extra = pd.DataFrame({'Product': ['Pen', 'Notebook', 'Pen']})
combined_cols = pd.concat([region_totals, df_extra], axis=1)
print("\n🔸 Concatenated Columns (Horizontal):")
print(combined_cols)


# 🔄 Merge with different column names
df_left = pd.DataFrame({'ID1': [1, 2], 'Value1': [10, 20]})
df_right = pd.DataFrame({'ID2': [2, 3], 'Value2': [30, 40]})

custom_merge = pd.merge(df_left, df_right, left_on='ID1', right_on='ID2', how='outer')
print("\n🔸 Merge with Different Column Names:")
print(custom_merge)