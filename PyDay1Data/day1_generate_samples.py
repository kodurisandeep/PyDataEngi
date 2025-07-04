# -*- coding: utf-8 -*-
import pandas as pd
import os

os.makedirs("dataset_samples", exist_ok=True)

# 1. Malformed Iris CSV (inconsistent delimiters and missing values)
iris_data = """SepalLength,SepalWidth,PetalLength,PetalWidth,Species
5.1,3.5,1.4,0.2,Iris-setosa
4.9,,1.4,0.2,Iris-setosa
"4.7",3.2,,0.2,"Iris-setosa"
4.6,3.1,1.5,,Iris-setosa
5.0,3.6,1.4,0.2,"Iris-setosa
"""

with open("dataset_samples/iris_malformed.csv", "w", encoding="utf-8") as f:
    f.write(iris_data)

# 2. Pipe-delimited sales data
sales_data = """Date|Region|Salesperson|Units|Revenue
2025-07-01|East|Amit|10|5000
2025-07-02|West|Sneha|8|4200
2025-07-02|South|Ravi|12|6200
2025-07-03|North|Meena|5|2500
"""

with open("dataset_samples/sales_pipe.txt", "w", encoding="utf-8") as f:
    f.write(sales_data)

# 3. UTF-16 encoded CSV
utf16_data = [
    ["City", "Country", "Population"],
    ["São Paulo", "Brazil", "12M"],
    ["München", "Germany", "1.5M"],
    ["Zürich", "Switzerland", "400k"]
]

pd.DataFrame(utf16_data[1:], columns=utf16_data[0]) \
  .to_csv("dataset_samples/utf16_data.csv", index=False, encoding="utf-16")

print("✅ Sample files generated inside dataset_samples/")