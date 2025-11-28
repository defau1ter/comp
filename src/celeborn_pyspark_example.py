#!/usr/bin/env python3
"""
PySpark Example using Celeborn for Shuffle Storage

This script demonstrates how to use Celeborn as the shuffle service
for PySpark jobs. It performs operations that generate shuffle data
which will be stored in Celeborn (and ultimately in HDFS).
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as _sum, avg, max as _max
import time

def create_spark_session_with_celeborn():
    """
    Create SparkSession configured to use Celeborn for shuffle operations
    """
    print("=" * 80)
    print("Creating Spark Session with Celeborn Configuration...")
    print("=" * 80)
    
    # Path to Celeborn shaded client JAR (includes all dependencies, Scala 2.13)
    import os
    
    # Configure these paths for your environment
    celeborn_home = os.environ.get("CELEBORN_HOME", os.path.abspath("../celeborn"))
    celeborn_jar = f"{celeborn_home}/client-spark/spark-4-shaded/target/celeborn-client-spark-4-shaded_2.13-0.7.0-SNAPSHOT.jar"
    
    # For S3 support, uncomment and add AWS dependencies:
    # home_dir = os.path.expanduser("~")
    # jars = [
    #     celeborn_jar,
    #     f"{home_dir}/.m2/repository/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar",
    #     f"{home_dir}/.m2/repository/com/amazonaws/aws-java-sdk-s3/1.12.532/aws-java-sdk-s3-1.12.532.jar",
    # ]
    # celeborn_jar = ",".join(jars)
    
    spark = SparkSession.builder \
        .appName("PySpark-Celeborn-Example") \
        .master("local[4]") \
        .config("spark.jars", celeborn_jar) \
        .config("spark.sql.catalogImplementation", "in-memory") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.shuffle.manager", "org.apache.spark.shuffle.celeborn.SparkShuffleManager") \
        .config("spark.celeborn.master.endpoints", "localhost:9097") \
        .config("spark.shuffle.service.enabled", "false") \
        .config("spark.dynamicAllocation.shuffleTracking.enabled", "false") \
        .config("spark.celeborn.client.spark.shuffle.writer", "hash") \
        .config("spark.celeborn.client.push.replicate.enabled", "false") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.localShuffleReader.enabled", "false") \
        .getOrCreate()
    
    print("\n✅ Spark Session Created with Celeborn Shuffle Manager\n")
    print(f"   Application ID: {spark.sparkContext.applicationId}")
    print(f"   Master: {spark.sparkContext.master}")
    print(f"   Shuffle Manager: Celeborn")
    print(f"   Celeborn Master: localhost:9097")
    print(f"   Storage: Local Disk (/tmp/celeborn)")
    print()
    
    return spark


def run_shuffle_example(spark):
    """
    Run example operations that generate shuffle data
    """
    print("=" * 80)
    print("Running Shuffle Operations (data will be stored in Celeborn)")
    print("=" * 80)
    print()
    
    # Create sample data - this will generate shuffle during aggregations
    print("📊 Step 1: Creating sample dataset with 1 million records...")
    df = spark.range(0, 1000000) \
        .selectExpr(
            "id",
            "cast(rand() * 100 as int) as category",
            "cast(rand() * 1000 as double) as value",
            "cast(rand() * 50 as int) as region"
        )
    
    print(f"   Created DataFrame with {df.count():,} records")
    print()
    
    # Operation 1: GroupBy aggregation (triggers shuffle)
    print("📊 Step 2: Performing GroupBy aggregation (triggers shuffle)...")
    start_time = time.time()
    
    agg_df = df.groupBy("category") \
        .agg(
            count("*").alias("count"),
            _sum("value").alias("total_value"),
            avg("value").alias("avg_value"),
            _max("value").alias("max_value")
        ) \
        .orderBy("category")
    
    result_count = agg_df.count()
    elapsed = time.time() - start_time
    
    print(f"   ✅ Aggregation completed in {elapsed:.2f} seconds")
    print(f"   Results: {result_count} categories")
    print()
    print("   Sample results:")
    agg_df.show(10, truncate=False)
    
    # Operation 2: Join operation (triggers shuffle)
    print("📊 Step 3: Performing Join operation (triggers shuffle)...")
    start_time = time.time()
    
    # Create another dataset
    regions_df = spark.createDataFrame([
        (0, "North"), (1, "South"), (2, "East"), (3, "West"), (4, "Central")
    ] * 10, ["region", "region_name"])
    
    joined_df = df.join(regions_df, "region") \
        .groupBy("region_name") \
        .agg(
            count("*").alias("count"),
            avg("value").alias("avg_value")
        ) \
        .orderBy("region_name")
    
    elapsed = time.time() - start_time
    
    print(f"   ✅ Join completed in {elapsed:.2f} seconds")
    print()
    print("   Results by region:")
    joined_df.show(truncate=False)
    
    # Operation 3: Repartition (triggers shuffle)
    print("📊 Step 4: Repartitioning data (triggers shuffle)...")
    start_time = time.time()
    
    repartitioned_df = df.repartition(20, "category")
    partition_count = repartitioned_df.rdd.getNumPartitions()
    
    elapsed = time.time() - start_time
    
    print(f"   ✅ Repartitioning completed in {elapsed:.2f} seconds")
    print(f"   Number of partitions: {partition_count}")
    print()
    
    return agg_df, joined_df


def main():
    """
    Main function
    """
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "PYSPARK WITH CELEBORN EXAMPLE" + " " * 28 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    try:
        # Create Spark session with Celeborn
        spark = create_spark_session_with_celeborn()
        
        # Run shuffle operations
        agg_df, joined_df = run_shuffle_example(spark)
        
        print("=" * 80)
        print("✅ ALL OPERATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("📊 Summary:")
        print("   - All shuffle data was stored in Celeborn")
        print("   - Celeborn stored data locally: /tmp/celeborn")
        print("   - Check Celeborn UI for shuffle metrics:")
        print("     * Master UI: http://localhost:9098")
        print("     * Worker UI: http://localhost:9096")
        print()
        print("💾 To verify shuffle data locally:")
        print("   $ ls -lh /tmp/celeborn")
        print()
        
        # Keep application alive for a moment to see Celeborn metrics
        print("⏳ Keeping application alive for 10 seconds to view metrics...")
        time.sleep(10)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if 'spark' in locals():
            print("\n🛑 Stopping Spark session...")
            spark.stop()
            print("✅ Spark session stopped")
    
    print("\n" + "=" * 80)
    print("🎉 Job completed successfully!")
    print("=" * 80 + "\n")
    return 0


if __name__ == "__main__":
    exit(main())
