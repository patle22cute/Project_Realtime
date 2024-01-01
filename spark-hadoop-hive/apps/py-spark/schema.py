from pyspark.sql.types import (IntegerType,
                               StringType,
                               DoubleType,
                               StructField,
                               StructType,
                               LongType,
                               BooleanType)

schema = {
    'projectDE': StructType([
        StructField("User", StringType(), True),
        StructField("Card", StringType(), True),
        StructField("Year", StringType(), True),
        StructField("Month", StringType(), True),
        StructField("Day", StringType(), True),
        StructField("Time", StringType(), True),
        StructField("Amount", StringType(), True),
        StructField("Use Chip", StringType(), True),
        StructField("Merchant Name", StringType(), True),
        StructField("Merchant City", StringType(), True),
        StructField("Merchant State", StringType(), True),
        StructField("Zip", StringType(), True),
        StructField("MCC", StringType(), True),
        StructField("Errors?", StringType(), True),
        StructField("Is Fraud?", StringType(), True)
    ])
}   

