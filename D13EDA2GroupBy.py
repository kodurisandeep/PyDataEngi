import pandas as pd
import seaborn as sns
import matplotlib.pyplot as pt

data = {
    'Region': ['East', 'West', 'East', 'West', 'South', 'East', 'South'],
    'Product': ['Pen', 'Pen', 'Notebook', 'Notebook', 'Pen', 'Pen', 'Notebook'],
    'Month': ['Jan', 'Jan', 'Feb', 'Feb', 'Jan', 'Feb', 'Feb'],
    'Sales': [120, 100, 150, 200, 80, 110, 130]
}

df = pd.DataFrame(data)
print(df)

total_sales_by_region = df.groupby('Region')['Sales'].sum()
print(total_sales_by_region)

pivot = df.pivot_table(values='Sales', index='Region', columns='Month', aggfunc='sum', fill_value=0)
print(pivot)

summary = df.groupby(['Region', 'Product'])['Sales'].agg(['sum', 'mean', 'count'])
print(summary)

sns.barplot(x=total_sales_by_region.index, y=total_sales_by_region.values)
pt.title("Sales by region")
pt.xlabel("Region")
pt.ylabel("Sales sum")
pt.show()

pivot_reset = pivot.reset_index().melt(id_vars='Region', var_name='Month', value_name='Sales')
sns.barplot(data=pivot_reset, x='Region', y='Sales', hue='Month')
pt.title("Monthly Sales by Region")
pt.xlabel("Region")
pt.ylabel("Sales")
pt.show()

summary_melted = summary.reset_index().melt(
    id_vars=['Region', 'Product'],
    value_vars=['sum', 'mean', 'count'],
    var_name='Metric',
    value_name='Sales'
)

summary_melted['Group'] = summary_melted['Region'] + ' - ' + summary_melted['Product']

sub_summary=summary_melted[['Group', 'Metric', 'Sales']]

sns.barplot(
    data=sub_summary,
    x='Group', y='Sales',
    hue='Metric'
)

pt.title("Sales Summary by Region and Product (sum, mean, count)")
pt.xlabel("Region - Product")
pt.ylabel("Value")
pt.show()