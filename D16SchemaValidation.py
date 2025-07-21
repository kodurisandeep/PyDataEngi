from pydantic import BaseModel, field_validator
from datetime import datetime
import pandas as pd

class Transaction(BaseModel):
    customer_id: int
    store_city: str
    customer_segment: str
    txn_date: datetime
    item_count: int
    total_amount: float

    @field_validator('total_amount')
    def check_positive_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be positive")
        else:
            print("Data is good")
        return value

# Example usage:
record = {
    "customer_id": 101,
    "store_city": "Hyderabad",
    "customer_segment": "Gold",
    "txn_date": "2025-07-15",
    "item_count": 5,
    "total_amount": 1500
}

txn = Transaction(**record)  # Automatically validates

#Manual Validation
def validate_schema(df):
    # Column existence
    required_cols = ['customer_id', 'txn_date', 'total_amount']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    # Type checks
    if not pd.api.types.is_integer_dtype(df['customer_id']):
        raise TypeError("customer_id must be integer")
    if not pd.api.types.is_numeric_dtype(df['total_amount']):
        raise TypeError("total_amount must be numeric")
    
    # Range checks
    if (df['total_amount'] <= 0).any():
        raise ValueError("Some amounts are non-positive")

    print("✅ Schema validated")

# Example usage:
df = pd.read_csv("./dataset_samples/D16_data.csv")
validate_schema(df)