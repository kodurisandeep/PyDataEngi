import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🔹 Sample dataset with encoded categories
df = pd.DataFrame({
    'UserID': range(1, 11),
    'UserType': ['A', 'B', 'C', 'A', 'C', 'B', 'B', 'A', 'C', 'X'],
    'Region': ['East', 'West', 'East', 'South', 'West', 'South', 'East', 'West', 'East', 'North']
})

print("🔸 Original DataFrame")
print(df)

# 🔸 Frequency counts
user_type_counts = df['UserType'].value_counts()
print("\n🔸 Frequency of UserType")
print(user_type_counts)

region_freq = df['Region'].value_counts(normalize=True).round(2)
print("\n🔸 Region Frequencies (Percentage)")
print(region_freq)

# 🔹 Mapping scheme codes
codebook = {'A': 'Admin', 'B': 'Business', 'C': 'Customer'}
df['UserTypeLabel'] = df['UserType'].map(codebook).fillna('Unknown')

print("\n🔸 DataFrame after scheme decoding")
print(df[['UserType', 'UserTypeLabel']])

# 🔹 Grouped frequency: UserType per Region
grouped = df.groupby('Region')['UserTypeLabel'].value_counts().unstack().fillna(0).astype(int)
print("\n🔸 UserType Distribution by Region")
print(grouped)


# 🔹 Barplot - Count of each decoded category
plt.figure(figsize=(6, 4))
sns.countplot(
    data=df,
    x='UserTypeLabel',
    hue='UserTypeLabel',
    order=df['UserTypeLabel'].value_counts().index,
    palette='Set2',
    legend=False
)
plt.title("User Type Distribution")
plt.xlabel("User Type")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 🔹 Heatmap - Region vs User Type
plt.figure(figsize=(6, 4))
sns.heatmap(grouped, annot=True, fmt='d', cmap='YlGnBu')
plt.title("User Type by Region (Count)")
plt.ylabel("Region")
plt.xlabel("User Type")
plt.tight_layout()
plt.show()