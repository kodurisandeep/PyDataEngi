from datetime import date
import pandas as pd
import chardet
import seaborn as sns
import matplotlib.pyplot as plt

def summarize_eda(df):
    top_city = df.groupby('store_city')['total_amount'].sum().idxmax()
    top_cat = df.groupby('product_category')['total_amount'].sum().idxmax()
    payment_mode = df['payment_method'].value_counts().idxmax()
    
    print(f"🔍 Top performing city: {top_city}")
    print(f"🔍 Highest revenue category: {top_cat}")
    print(f"💳 Most used payment method: {payment_mode}")

with open("./dataset_samples/D15_EDAExamSales.csv","rb") as f:
    result = chardet.detect(f.read(10000))

#Read Sales
df = pd.read_csv("./dataset_samples/D15_EDAExamSales.csv", encoding=result["encoding"], engine="python",
                 sep=",", on_bad_lines="warn",)
#print(df.head())


#Descriptive Stats: Summary of quantities and amounts, city-wise and category-wise.
qty_stats = df.groupby(['store_city', 'product_category'])['quantity'].sum().reset_index()
amt_stats = df.groupby(['store_city', 'product_category'])['total_amount'].sum().reset_index()
print(qty_stats)
print(amt_stats)

#Grouping & Aggregation: Which product categories are driving revenue in each city?
#What's the average transaction value per city?
print(df.groupby(['store_city','product_category'])['total_amount'].sum())
city_avg = df.groupby('store_city')['total_amount'].mean().reset_index(name='avg_transaction_value')
df = pd.merge(df, city_avg, on='store_city', how='left')
print(df.head())

#Read Products
with open("./dataset_samples/D15_EDAExamProducts.csv","rb") as f:
    result = chardet.detect(f.read(10000))

dfp = pd.read_csv("./dataset_samples/D15_EDAExamProducts.csv", encoding=result["encoding"], engine="python",
                 sep=",", on_bad_lines="warn",)
#print(dfp.head())

#Joins: Merge sales and products to enrich the dataset
merged_df = pd.merge(df, dfp, on='product_code', how='left')
print(merged_df.columns)

#Categorical Analysis: Distribution of payment methods, and frequency of top 5 brands.
payment_counts = df['payment_method'].value_counts().reset_index()
payment_counts.columns = ['payment_method', 'count']

sns.barplot(x='payment_method', y='count', data=payment_counts)
plt.xlabel('Payment Method')
plt.ylabel('Transaction Count')
plt.title('Distribution of Payment Methods')
plt.tight_layout()
plt.show()

top_brands = merged_df['brand'].value_counts().head(5)
print(top_brands)

#Time-Series: Monthly revenue trends across cities, with rolling averages for smoother insight.
df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
df['month'] = df['date'].dt.to_period("M")

monthly_rev = df.groupby(['store_city', 'month'])['total_amount'].sum().reset_index()
monthly_rev['rolling_avg'] = (
    monthly_rev.groupby('store_city')['total_amount']
    .transform(lambda x: x.rolling(window=2, min_periods=1).mean().round(2))
)

print(monthly_rev)

#Heatmap: Sales by city and category
pivot = df.pivot_table(index='store_city', columns='product_category', values='total_amount', aggfunc='sum', fill_value=0)
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Heatmap: Total Sales by City & Category")
plt.show()

#Monthly trend line
monthly_rev['month_str'] = monthly_rev['month'].astype(str)
sns.lineplot(x='month_str', y='total_amount', hue='store_city', data=monthly_rev)
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend by City")
plt.tight_layout()
plt.show()

print(df)
summarize_eda(df)    
