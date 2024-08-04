import sys
from pyspark.sql import SparkSession

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
# Read Data from Postgres
####################################
print("######################################")
print("READING DATA FROM POSTGRES")
print("######################################")

df_data = (
    spark.read
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.ecommerce_data")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .load()
)

####################################
# Preprocess Data
####################################
print("######################################")
print("PREPROCESSING DATA")
print("######################################")

# Example preprocessing: filter out null categories and apply any other transformations needed
df_preprocessed = df_data.filter(df_data["category_id"].isNotNull())

####################################
# Write Preprocessed Data back to Postgres
####################################
print("######################################")
print("WRITING PREPROCESSED DATA TO POSTGRES")
print("######################################")

(
    df_preprocessed.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.preprocessed_ecommerce_data")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")  # Overwriting to store the latest preprocessed data
    .save()
)
