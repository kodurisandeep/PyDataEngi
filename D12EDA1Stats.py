import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Seed for reproducibility
np.random.seed(42)

# 🔧 Simulated employee dataset
df = pd.DataFrame({
    'salary': np.random.normal(loc=50000, scale=15000, size=100),  # Normally distributed salaries
    'experience': np.random.randint(1, 30, size=100),               # Random years of experience
    'department': np.random.choice(['HR', 'Finance', 'Tech', 'Sales'], size=100)  # Categorical dept
})

df['salary'] = df['salary'].round(2)  # Retain 2 decimal points

# 📏 Basic check: row count
print("Number of rows:", len(df))

# 📊 Descriptive stats for numeric columns
print("\nNumeric Summary:\n", df.describe().round(2))

# 📊 Descriptive stats including non-numeric columns
print("\nFull Summary:\n", df.describe(include='all').round(2))

# 📈 Histogram with KDE to visualize salary distribution
sns.histplot(df['salary'], kde=True)
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.show()

# 📉 Skew & Kurtosis - Measures of distribution shape
print("Skew:", df['salary'].skew())       # Skewness → asymmetry
print("Kurtosis:", df['salary'].kurt())   # Kurtosis → peakedness

# 🔍 Quantiles - important percentiles
print("Quantiles:\n", df['salary'].quantile([0.25, 0.5, 0.75]))

# 📊 Binning salaries into quartile groups
df['salary_group'] = pd.qcut(df['salary'], q=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High'])

# ✅ Optional: Quick check of how many records fall into each bin
print("\nSalary Group Counts:\n", df['salary_group'].value_counts())