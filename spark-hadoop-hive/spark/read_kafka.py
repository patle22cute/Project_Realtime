# Import the necessary modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

from schema import *
from spark_streaming_function import *



KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS",'broker')
KAFKA_PORT = "29092"
LISTEN_EVENTS_TOPICS  = "projectDE"
storage_path = "namenode:9000/mydata/output"
checkpoint_path = "namenode:9000/checkpoints"
trigger = "10 seconds"
output_mode= "append" 
file_format = "csv"

spark = create_or_get_spark_session('AppName')
listen_events = create_kafka_read_stream(spark, KAFKA_ADDRESS, KAFKA_PORT, LISTEN_EVENTS_TOPICS)

listen_events = process_stream(listen_events, schema[LISTEN_EVENTS_TOPICS], LISTEN_EVENTS_TOPICS)

#1
# listen_events_writer = create_console_write_stream(listen_events)
# listen_events_writer.start()
# spark.streams.awaitAnyTermination()

#2

write_stream = create_file_write_stream_HDFS(listen_events,storage_path, checkpoint_path, trigger, output_mode, file_format)
write_stream.start()
spark.streams.awaitAnyTermination()

# (listen_events
# .writeStream
# .format("parquet")    
# .option("path", "hdfs://namenode:9000/mydata/output") 
# .option("checkpointLocation", "hdfs://namenode:9000/checkpoints") 
# .trigger(processingTime="10 seconds") 
# .outputMode("append")).start()

# spark.streams.awaitAnyTermination()

# from pyspark.sql.types import (IntegerType,
#                                StringType,
#                                DoubleType,
#                                StructField,
#                                StructType,
#                                LongType,
#                                BooleanType)

# # Test 1
# schema = {
#     'projectDE': StructType([
#         StructField("User", StringType(), True),
#         StructField("Card", StringType(), True),
#         StructField("Year", StringType(), True),
#         StructField("Month", StringType(), True),
#         StructField("Day", StringType(), True),
#         StructField("Time", StringType(), True),
#         StructField("Amount", StringType(), True),
#         StructField("Use Chip", StringType(), True),
#         StructField("Swipe Transaction", StringType(), True),
#         StructField("Merchant Name", StringType(), True),
#         StructField("Merchant City", StringType(), True),
#         StructField("Monterey Park", StringType(), True),
#         StructField("Merchant State", StringType(), True),
#         StructField("Zip", StringType(), True),
#         StructField("MCC", StringType(), True),
#         StructField("Errors?", StringType(), True),
#         StructField("Is Fraud?", StringType(), True)
#     ])
# }   


# spark = SparkSession.builder \
#     .appName("app_name") \
#     .master("spark://spark-master:7077") \
#     .getOrCreate()

# read_stream = (spark
#                    .readStream
#                    .format("kafka")
#                    .option("kafka.bootstrap.servers", "broker:29092")
#                    .option("failOnDataLoss", False)
#                    .option("startingOffsets", "earliest")
#                    .option("subscribe", "projectDE")
#                    .load())

# stream= read_stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# query = stream.writeStream \
#     .trigger(processingTime='5 seconds') \
#     .outputMode("update") \
#     .format("console") \
#     .option("truncate", "false") \
#     .start()

# query.awaitTermination()

