import jsonschema
from jsonschema import validate, ValidationError
import pandas as pd

def validate_records(df: pd.DataFrame, schema: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_records = []
    invalid_records = []

    for idx, row in df.iterrows():
        try:
            validate(instance=row.to_dict(), schema=schema)
            valid_records.append(row)
        except ValidationError as e:
            row_dict = row.to_dict()
            row_dict["__error__"] = str(e)
            invalid_records.append(row_dict)

    df_valid = pd.DataFrame(valid_records) if valid_records else pd.DataFrame(columns=df.columns)
    df_invalid = pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame(columns=df.columns.tolist() + ["__error__"])

    return df_valid, df_invalid