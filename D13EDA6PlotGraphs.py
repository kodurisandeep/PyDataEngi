import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style='whitegrid')
np.random.seed(42)

# Step 1: Create synthetic dataset
dates = pd.date_range('2023-01-01', periods=100, freq='D')
sales = np.random.normal(loc=200, scale=50, size=100).round()
temperature = np.random.normal(loc=30, scale=5, size=100).round(1)
traffic = np.random.randint(1000, 3000, size=100)

df = pd.DataFrame({
    'date': dates,
    'sales': sales,
    'temperature': temperature,
    'traffic': traffic
})

# Step 2: Line Plot — Sales over Time
plt.figure(figsize=(10, 4))
plt.plot(df['date'], df['sales'], color='teal', label='Daily Sales')
plt.title('Line Plot: Daily Sales Trend')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.tight_layout()
plt.show()

# Step 3: Histogram — Distribution of Temperature
plt.figure(figsize=(8, 4))
sns.histplot(df['temperature'], bins=20, color='coral', kde=True)
plt.title('Histogram: Temperature Distribution')
plt.xlabel('Temperature (°C)')
plt.tight_layout()
plt.show()

# Step 4: Heatmap — Correlation between variables
plt.figure(figsize=(6, 4))
corr = df.drop(columns='date').corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Heatmap: Feature Correlations')
plt.tight_layout()
plt.show()