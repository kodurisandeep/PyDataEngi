import pandas as pd
import re

def validate_employee_data(df):
    errors = []

    # Schema check
    expected_columns = ['id', 'name', 'age', 'status', 'email', 'pan']
    if set(df.columns) != set(expected_columns):
        errors.append(f"Schema mismatch! Expected columns: {expected_columns}")

    for i, row in df.iterrows():
        # Type check
        if not isinstance(row['age'], int):
            errors.append(f"[Row {i}] Age must be an integer.")

        # Range check
        if not (18 <= row['age'] <= 99):
            errors.append(f"[Row {i}] Age {row['age']} not in valid range (18-99).")

        # Null check
        if pd.isnull(row['name']) or row['email'] == '':
            errors.append(f"[Row {i}] Name or Email is missing.")

        # Length check (PAN)
        if len(str(row['pan'])) != 10:
            errors.append(f"[Row {i}] PAN length invalid: {row['pan']}")

        # Pattern check (Email and PAN)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", row['email']):
            errors.append(f"[Row {i}] Email format invalid: {row['email']}")
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", str(row['pan'])):
            errors.append(f"[Row {i}] PAN format invalid: {row['pan']}")

        # Category check
        if row['status'] not in ['Active', 'Inactive']:
            errors.append(f"[Row {i}] Status '{row['status']}' not allowed.")

    return errors

df = pd.DataFrame({
    'id': [101, 102, 103, 104],
    'name': ['Alice', 'Bob', None, 'D@ve'],
    'age': [25, 17, 45, 120],                       # range issues
    'status': ['Active', 'Inactive', 'Retired', 'Active'],  # category issue
    'email': ['alice@example.com', 'bob@abc', 'carol@example.com', ''],  # pattern + null
    'pan': ['ABCDE1234F', 'XYZ9999F', 'PQRS1234H', 'ABCD12345Z']         # length + pattern
})

issues = validate_employee_data(df)
for issue in issues:
    print(issue)