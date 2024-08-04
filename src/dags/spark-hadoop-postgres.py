import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
spark_conn = os.environ.get("spark_conn", "spark_conn")
spark_master = "spark://spark:7077"
postgres_driver_jar = "/usr/local/spark/assets/jars/postgresql-42.2.6.jar"

data_file = "/usr/local/spark/assets/data/2019-Oct.csv"
postgres_db = "jdbc:postgresql://postgres:5432/airflow"
postgres_user = "airflow"
postgres_pwd = "airflow"
sampling_ratio = 0.01  # Adjust the sampling ratio as needed

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="spark-postgres-quarterly",
    description="This DAG handles quarterly data ingestion, preprocessing, and aggregation.",
    default_args=default_args,
    schedule_interval="@quarterly"
)

start = DummyOperator(task_id="start", dag=dag)

# Task to ingest the data from the CSV file
spark_job_ingest_data = SparkSubmitOperator(
    task_id="spark_job_ingest_data",
    application="/usr/local/spark/applications/ingest-data.py",
    name="ingest-data",
    conn_id="spark_conn",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[data_file, postgres_db, postgres_user, postgres_pwd, str(sampling_ratio)],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag
)

# Task to preprocess the data
spark_job_preprocess_data = SparkSubmitOperator(
    task_id="spark_job_preprocess_data",
    application="/usr/local/spark/applications/preprocess-data.py",
    name="preprocess-data",
    conn_id="spark_conn",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag
)

# Task to aggregate the data
spark_job_aggregate_data = SparkSubmitOperator(
    task_id="spark_job_aggregate_data",
    application="/usr/local/spark/applications/aggregate-data.py",
    name="aggregate-data",
    conn_id="spark_conn",
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag
)



end = DummyOperator(task_id="end", dag=dag)

start >> spark_job_ingest_data >> spark_job_preprocess_data >> spark_job_aggregate_data >> end
