from pyspark.sql import SparkSession
import os

os.environ["PYSPARK_PYTHON"] = r"C:\Users\kodur\AppData\Local\Programs\Python\Python311\python.exe"

# Create SparkSession
spark = SparkSession.builder.appName("Day21_SparkIntro").master("local[*]").getOrCreate()

# Sample data
data = [("Sandeep", 28), ("Asha", 25), ("Ravi", 30)]
columns = ["Name", "Age"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Transformation (lazy)
df_filtered = df.filter(df.Age > 26)

# Action (triggers execution)
df_filtered.show()

df_filtered.explain(True)

# Stop SparkSession
spark.stop()