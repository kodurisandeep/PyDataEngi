import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data
data = {
    'values': [10, 12, 14, 13, 15, 11, 100, 12, 13, 10, -30, 14, 12, 120, 110, 130, -10, -50]
}
df = pd.DataFrame(data)

# Plot boxplot
plt.figure(figsize=(8, 5))
sns.boxplot(x=df['values'], color='skyblue')
plt.title('Boxplot of Values with Outliers')
plt.xlabel('Value')
plt.grid(True)
plt.show()