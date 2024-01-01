from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaConnectionTest") \
    .master("local[*]") \
    .getOrCreate()

# Read data from Kafka as a streaming DataFrame
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "projectDE") \
    .load()

# Select key and value columns
streamingDF = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Write streaming DataFrame to console
query = streamingDF \
    .writeStream \
    .format("console") \
    .start()

# Wait for streaming to finish
query.awaitTermination()