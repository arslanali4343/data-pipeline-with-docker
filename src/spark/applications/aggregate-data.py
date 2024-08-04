import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg

# Create spark session
spark = (SparkSession
         .builder
         .getOrCreate()
         )

####################################
# Parameters
####################################
postgres_db = sys.argv[1]
postgres_user = sys.argv[2]
postgres_pwd = sys.argv[3]

####################################
# Read Preprocessed Data from Postgres
####################################
print("######################################")
print("READING PREPROCESSED DATA FROM POSTGRES")
print("######################################")

df_preprocessed = (
    spark.read
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.preprocessed_ecommerce_data")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .load()
)

####################################
# Aggregate Data
####################################
print("######################################")
print("AGGREGATING DATA")
print("######################################")

# Example aggregation: count events per category and average price
df_aggregated = (
    df_preprocessed.groupBy("category_id")
    .agg(count("*").alias("event_count"), avg("price").alias("avg_price"))
)

####################################
# Write Aggregated Data back to Postgres
####################################
print("######################################")
print("WRITING AGGREGATED DATA TO POSTGRES")
print("######################################")

(
    df_aggregated.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.aggregated_ecommerce_data")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")  # Overwriting to store the latest aggregated data
    .save()
)
