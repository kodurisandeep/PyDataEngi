from pyspark.sql import SparkSession
import os

os.environ["PYSPARK_PYTHON"] = r"C:\Users\kodur\AppData\Local\Programs\Python\Python311\python.exe"

spark = SparkSession.builder.appName("DAG_DeepDive").getOrCreate()

# Sample data: People and their cities
people_data = [("Sandeep", 28, "Hyderabad"), ("Asha", 25, "Mumbai"), ("Ravi", 30, "Hyderabad")]
city_data = [("Hyderabad", "Telangana"), ("Mumbai", "Maharashtra")]

# Create DataFrames
people_df = spark.createDataFrame(people_data, ["Name", "Age", "City"])
city_df = spark.createDataFrame(city_data, ["City", "State"])

# Step 1: Filter
filtered_df = people_df.filter(people_df.Age > 26)

# Step 2: Join
joined_df = filtered_df.join(city_df, on="City", how="inner")

# Step 3: GroupBy + Aggregation
agg_df = joined_df.groupBy("State").count()

# Step 4: Write to memory (triggers execution)
agg_df.show()

agg_df.explain(True)

spark.stop()
