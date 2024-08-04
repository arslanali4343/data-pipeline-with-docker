import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import IntegerType, LongType, DoubleType, StringType

# Create spark session
spark = (SparkSession
         .builder
         .getOrCreate()
         )

####################################
# Parameters
####################################
data_file = sys.argv[1]
postgres_db = sys.argv[2]
postgres_user = sys.argv[3]
postgres_pwd = sys.argv[4]
sampling_ratio = float(sys.argv[5])  # New parameter for sampling ratio

####################################
# Read CSV Data
####################################
print("######################################")
print("READING CSV FILE")
print("######################################")

df_data_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(data_file)
    .sample(fraction=sampling_ratio)  # Apply sampling ratio
)

# Cast columns to the correct data types
df_data_csv_casted = (
    df_data_csv
    .withColumn('event_time', to_timestamp(col("event_time")))
    .withColumn('event_type', col("event_type").cast(StringType()))
    .withColumn('product_id', col("product_id").cast(IntegerType()))
    .withColumn('category_id', col("category_id").cast(LongType()))
    .withColumn('category_code', col("category_code").cast(StringType()))
    .withColumn('brand', col("brand").cast(StringType()))
    .withColumn('price', col("price").cast(DoubleType()))
    .withColumn('user_id', col("user_id").cast(IntegerType()))
    .withColumn('user_session', col("user_session").cast(StringType()))
)

####################################
# Load data to Postgres
####################################
print("######################################")
print("LOADING POSTGRES TABLE")
print("######################################")

(
    df_data_csv_casted.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.ecommerce_data")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("append")  # Appending to avoid overwriting
    .save()
)
