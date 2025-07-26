import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Strip whitespace from strings
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Convert txn_date to datetime
    df["txn_date"] = pd.to_datetime(df["txn_date"], errors="coerce")

    # Fill missing item_count with zero (if safe)
    df["item_count"] = df["item_count"].fillna(0).astype(int)

    # Optional tagging: e.g. high-value customers
    df["customer_value_segment"] = pd.cut(
        df["total_amount"],
        bins=[0, 500, 2000, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    return df