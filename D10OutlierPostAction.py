import pandas as pd

def detect_outliers_boxplot(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    print(Q1, Q3)
    IQR = Q3 - Q1
    return df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

def remove_outliers_iqr(df, col, threshold=1.5):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - threshold * IQR
    upper = Q3 + threshold * IQR
    return df[(df[col] >= lower) & (df[col] <= upper)]

def replace_outliers_with_median(df, col, threshold=1.5):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - threshold * IQR
    upper = Q3 + threshold * IQR
    median = df[col].median()

    df_copy = df.copy()
    df_copy.loc[(df[col] < lower) | (df[col] > upper), col] = median
    return df_copy

def cap_outliers(df, col, threshold=1.5):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - threshold * IQR
    upper = Q3 + threshold * IQR

    df_copy = df.copy()
    df_copy[col] = df[col].clip(lower, upper)
    return df_copy

def flag_outliers(df, col, threshold=1.5):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - threshold * IQR
    upper = Q3 + threshold * IQR

    df_copy = df.copy()
    df_copy['is_outlier'] = (df[col] < lower) | (df[col] > upper)
    return df_copy


# Your sample data
df = pd.DataFrame({'values': [10, 12, 14, 13, 15, 11, 100, 12, 13, 10, -30, 14, 12]})

print("Boxplot Outliers:\n", detect_outliers_boxplot(df, 'values'))

# Remove outliers
cleaned_df = remove_outliers_iqr(df, 'values')
print("Removed Outliers:\n", cleaned_df)

# Replace outliers with median
median_imputed_df = replace_outliers_with_median(df, 'values')
print("Median Replaced:\n", median_imputed_df)

# Cap extreme values (Winsorizing)
capped_df = cap_outliers(df, 'values')
print("Capped Values:\n", capped_df)

# Flag outliers with boolean column
flagged_df = flag_outliers(df, 'values')
print("Flagged Outliers:\n", flagged_df)