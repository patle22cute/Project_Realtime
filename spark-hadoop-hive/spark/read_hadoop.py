from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from schema import *
from spark_streaming_function import *

spark = SparkSession.builder \
    .appName("read_HDFS") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

data = spark.read.csv("hdfs://namenode:9000/mydata/ouput")
data.show(10)
data.printSchema()
