import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset (Titanic from seaborn for demo)
df = sns.load_dataset('titanic')

# Set plot style
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# 1. Dataset Overview
print("Shape:", df.shape)
print("\nColumns:\n", df.columns)
print("\nData Types:\n", df.dtypes)
print("\nSample Rows:\n", df.head())

# 2. Data Cleaning Summary
df.drop_duplicates(inplace=True)
df['age'] = df['age'].fillna(df['age'].median())  # Handle age early
df.dropna(subset=['embarked', 'fare'], inplace=True)  # Drop rows missing these critical columns

# Convert to correct types if needed
df['sex'] = df['sex'].astype('category')
df['class'] = df['class'].astype('category')

# 3. Descriptive Stats
print("\nSummary Stats:\n", df.describe(include='all'))
print("\nMissing Values:\n", df.isnull().sum())

# Distribution plots
sns.histplot(df['age'], kde=True)
plt.title("Age Distribution")
#plt.show()

sns.boxplot(x='class', y='fare', data=df)
plt.title("Fare Distribution by Class")
#plt.show()

# 4. Univariate Analysis
sns.countplot(x='sex', data=df)
plt.title("Gender Counts")
#plt.show()

sns.violinplot(x='class', y='age', data=df)
plt.title("Age Spread by Class")
#plt.show()

# 5. Bivariate Analysis
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
#plt.show()

sns.barplot(x='class', y='survived', data=df)
plt.title("Survival Rate by Class")
#plt.show()

# Grouped Stats
grouped = df.groupby(['class', 'sex'], observed=True)['survived'].mean().unstack()
print("\nSurvival Rate:\n", grouped)
print(df.groupby(['class', 'sex'], observed=True)['survived'].mean())

# 6. Categorical Exploration
sns.catplot(x='embarked', hue='survived', data=df, kind='count')
plt.title("Survival by Embark Point")
#plt.show()

# 7. Time-like Analysis (using age as pseudo-temporal trend)
df['age_bin'] = pd.cut(df['age'], bins=[0, 12, 18, 40, 60, 80])
age_grouped = df.groupby('age_bin', observed=True)['survived'].mean()
age_grouped.plot(kind='bar', color='skyblue')
plt.title("Survival Rate by Age Group")
#plt.show()

# 8. Visual Summary
sns.pairplot(df[['age', 'fare', 'survived']], hue='survived')
plt.suptitle("Pairwise Feature Relationships", y=1.02)
#plt.show()