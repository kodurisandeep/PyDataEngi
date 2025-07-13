import pandas as pd
from scipy import stats

data = {
    'values': [10, 12, 14, 13, 15, 11, 100, 12, 13, 10, -30, 14, 12]
}
df = pd.DataFrame(data)

def detect_outliers_boxplot(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    print(Q1, Q3)
    IQR = Q3 - Q1
    return df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

def detect_outliers_zscore(df, col, threshold=1):
    z_scores = stats.zscore(df[col])
    return df[(z_scores < -threshold) | (z_scores > threshold)]

def detect_outliers_iqr(df, col, multiplier=1.5):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    return df[(df[col] < lower_bound) | (df[col] > upper_bound)]

print("Boxplot Outliers:\n", detect_outliers_boxplot(df, 'values'))
print("Z-score Outliers:\n", detect_outliers_zscore(df, 'values'))
print("IQR Outliers:\n", detect_outliers_iqr(df, 'values'))