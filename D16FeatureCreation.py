import pandas as pd
from sklearn.preprocessing import LabelEncoder

data = {
    'customer_id': [101, 102, 103, 104],
    'txn_date': pd.to_datetime(['2025-07-15', '2025-07-15', '2025-07-16', '2025-07-16']),
    'item_count': [5, 2, 1, 3],
    'total_amount': [1500, 400, 200, 800],
    'store_city': ['Hyderabad', 'Delhi', 'Delhi', 'Hyderabad'],
    'customer_segment': ['Gold', 'Silver', 'Bronze', 'Gold']
}

df = pd.DataFrame(data)

#derived columns
df['txn_day'] = df['txn_date'].dt.day_name()
df['is_weekend'] = df['txn_date'].dt.weekday >= 5

#ratios
df['amount_per_item'] = (df['total_amount'] / df['item_count']).round(2)

#flags
df['is_high_value_txn'] = df['total_amount'] > 1000
df['is_loyal_segment'] = df['customer_segment'].isin(['Gold', 'Silver'])


#One-hot encoding - Best for non-ordinal categories
print(pd.get_dummies(df['store_city'], prefix='city'))
df_encoded = pd.get_dummies(df, columns=['store_city'], prefix='city')

#print(df_encoded.head())

#label encoding - Best for ordinal categories or trees (where number matters)
le = LabelEncoder()
df['segment_encoded'] = le.fit_transform(df['customer_segment'])

#Mapping schemes - Custom logic based on domain
segment_map = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
df['segment_mapped'] = df['customer_segment'].map(segment_map)
df['is_loyal'] = df['customer_segment'].map(lambda x: x in ['Gold', 'Silver'])

print(df.head())