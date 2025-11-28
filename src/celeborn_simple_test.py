#!/usr/bin/env python3
"""
Simple PySpark Celeborn test with local disk storage
"""

from pyspark.sql import SparkSession

# Path to Celeborn shaded client JAR (Scala 2.13)
import os
celeborn_home = os.environ.get("CELEBORN_HOME", os.path.abspath("../celeborn"))
celeborn_jar = f"{celeborn_home}/client-spark/spark-4-shaded/target/celeborn-client-spark-4-shaded_2.13-0.7.0-SNAPSHOT.jar"

spark = SparkSession.builder \
    .appName("Celeborn-Simple-Test") \
    .master("local[4]") \
    .config("spark.jars", celeborn_jar) \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.shuffle.manager", "org.apache.spark.shuffle.celeborn.SparkShuffleManager") \
    .config("spark.celeborn.master.endpoints", "localhost:9097") \
    .config("spark.shuffle.service.enabled", "false") \
    .config("spark.dynamicAllocation.shuffleTracking.enabled", "false") \
    .config("spark.celeborn.client.spark.shuffle.writer", "hash") \
    .config("spark.celeborn.client.push.replicate.enabled", "false") \
    .getOrCreate()

print("\n✅ Spark created successfully!")
print(f"App ID: {spark.sparkContext.applicationId}")
print(f"Master: {spark.sparkContext.master}\n")

# Simple test
print("Creating DataFrame and running groupBy (triggers shuffle)...")
df = spark.range(100000).selectExpr("id", "cast(rand() * 10 as int) as key")
result = df.groupBy("key").count().orderBy("key")

print("Results:")
result.show()

spark.stop()
print("\n✅ Test completed successfully!")

