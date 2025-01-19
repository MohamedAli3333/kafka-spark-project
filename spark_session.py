from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when, count
from pyspark.sql.types import StringType, DoubleType, StructType, StructField
from pyspark.sql import functions as F


spark = SparkSession.builder \
    .appName("KafkaConsumerToMySQL") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .config("spark.jars", "C:\\spark\\spark-3.2.4-bin-hadoop2.7\\jars\\mysql-connector-j-9.1.0.jar") \
    .getOrCreate()


kafka_broker = 'localhost:9092'


df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", "transactions") \
    .load()


raw_df = df.selectExpr("CAST(value AS STRING)")


schema = StructType([
    StructField("DEPOSIT AMT", DoubleType(), True),
    StructField("WITHDRAWAL AMT", DoubleType(), True)
])


df_parsed = raw_df.select(from_json(col("value"), schema).alias("data")) \
    .select(col("data.`DEPOSIT AMT`").alias("Deposit"),
            col("data.`WITHDRAWAL AMT`").alias("Withdrawal"))


aggregated_counts = df_parsed \
    .withColumn("deposit_occurrences", when(col("Deposit").isNotNull() & (col("Deposit") > 0), 1).otherwise(0)) \
    .withColumn("withdrawal_occurrences", when(col("Withdrawal").isNotNull() & (col("Withdrawal") > 0), 1).otherwise(0)) \
    .agg(
        F.sum("deposit_occurrences").alias("total_deposit_count"),
        F.sum("withdrawal_occurrences").alias("total_withdrawal_count")
    )

def write_to_mysql(batch_df, epoch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/financial_db") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "transactions") \
        .option("user", "root") \
        .option("password", "Mohamed123456") \
        .mode("overwrite") \
        .save()


query = aggregated_counts.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("complete") \
    .start()

query.awaitTermination()
