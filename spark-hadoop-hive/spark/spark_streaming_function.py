from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, regexp_replace

def create_or_get_spark_session(app_name):
    spark = SparkSession.builder \
    .appName(app_name) \
    .master("spark://spark-master:7077") \
    .getOrCreate()

    return spark

def create_kafka_read_stream(spark, kafka_address, kafka_port, topic, starting_offset="earliest"):
    read_stream = (spark
                   .readStream
                   .format("kafka")
                   .option("kafka.bootstrap.servers", f"{kafka_address}:{kafka_port}")
                   .option("failOnDataLoss", False)
                   .option("startingOffsets", starting_offset)
                   .option("subscribe", topic)
                   .load())

    return read_stream

def process_stream(stream, stream_schema, topic):
    stream = stream.withColumn("value_string", col("value").cast("string"))

    transformed_stream = (stream
                        .select(
                            from_json(col("value_string"), stream_schema).alias("data")
                        )
                        .select(
                            col("data.User").alias("User"),
                            col("data.Card").alias("Card"),
                            col("data.Year").alias("Year"),
                            col("data.Month").alias("Month"),
                            col("data.Day").alias("Day"),
                            col("data.Time").alias("Time"),
                            col("data.Amount").alias("Amount"),
                            col("data.`Use Chip`").alias("Use_Chip"),
                            col("data.`Merchant Name`").alias("Merchant_Name"),
                            col("data.`Merchant City`").alias("Merchant_City"),
                            col("data.`Merchant State`").alias("Merchant_State"),
                            col("data.Zip").alias("Zip"),
                            col("data.MCC").alias("MCC"),
                            col("data.Errors?").alias("Errors?"),
                            col("data.`Is Fraud?`").alias("Is_Fraud")
                        )
                        .filter(col("Is_Fraud") == "No")
                        )
    return transformed_stream

def create_file_write_stream_GCS(stream, storage_path, checkpoint_path, trigger="120 seconds", output_mode="append", file_format="csv"):
    write_stream = (stream
                    .writeStream
                    .format(file_format)
                    .partitionBy("month", "day", "hour")
                    .option("path", storage_path)
                    .option("checkpointLocation", checkpoint_path)
                    .trigger(processingTime=trigger)
                    .outputMode(output_mode))

    return write_stream

def create_console_write_stream(stream, trigger="20 seconds", output_mode = "append"):
    write_stream = (stream
                    .writeStream
                    .format("console")
                    .outputMode(output_mode)
                    .trigger(processingTime=trigger))
    
    return write_stream

def create_file_write_stream_HDFS(stream, storage_path, checkpoint_path, trigger, output_mode, file_format):
    write_stream = (stream
        .writeStream
        .format(file_format)    
        .partitionBy("Year","Month")
        .option("path", f"hdfs://{storage_path}") 
        .option("checkpointLocation", f"hdfs://{checkpoint_path}") 
        .trigger(processingTime=trigger) 
        .outputMode(output_mode))
    
    return write_stream

