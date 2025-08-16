from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import os

os.environ["PYSPARK_PYTHON"] = r"C:\Users\kodur\AppData\Local\Programs\Python\Python311\python.exe"

spark = SparkSession.builder.appName("Day23").getOrCreate()

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

df.printSchema()  # Inferred schema

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df_manual = spark.createDataFrame(data, schema)

df.select("name").show()
df.withColumn("age_plus_5", df.age + 5).show()
df.withColumnRenamed("age", "years").show()

df.filter(df.age > 28).show()
df.where("age < 30").show()

df.orderBy("age").show()
df.sort(df.age.desc()).show()

df.select("name", (df.age * 2).alias("double_age")).show()