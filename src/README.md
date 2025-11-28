# Celeborn PySpark Examples

This directory contains PySpark examples demonstrating integration with Apache Celeborn for remote shuffle service.

## Prerequisites

1. **Java 17+**
   ```bash
   brew install openjdk@17
   export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
   export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
   ```

2. **Build Celeborn with Scala 2.13** (for Spark 4.x/PySpark compatibility)
   ```bash
   cd ../celeborn
   ./build/mvn clean package -DskipTests -Paws -Pspark-4.0
   ```

3. **Python Environment with PySpark**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pyspark
   ```

## Running Celeborn Services

### Start Master
```bash
cd ../celeborn
./sbin/start-master.sh
```

### Start Worker
```bash
./sbin/start-worker.sh
```

### Debug Mode (with remote debugging enabled)
```bash
./sbin/start-master-debug.sh  # Debug port: 5005
./sbin/start-worker-debug.sh  # Debug port: 5006
```

## Running Examples

### Simple Test
```bash
export CELEBORN_HOME="$(pwd)/../celeborn"
python celeborn_simple_test.py
```

### Full Example
```bash
export CELEBORN_HOME="$(pwd)/../celeborn"
python celeborn_pyspark_example.py
```

## Configuration

### For S3 Storage
Edit `../celeborn/conf/celeborn-defaults.conf`:
```properties
celeborn.storage.availableTypes  S3
celeborn.storage.s3.dir  s3a://YOUR-BUCKET-NAME/shuffle
celeborn.hadoop.fs.s3a.access.key  YOUR_AWS_ACCESS_KEY_HERE
celeborn.hadoop.fs.s3a.secret.key  YOUR_AWS_SECRET_KEY_HERE
celeborn.storage.s3.endpoint.region  YOUR_AWS_REGION
```

**Note:** For S3 support, you'll also need to add AWS SDK JARs to the spark.jars configuration in the Python scripts.

### For Local Storage (Default)
```properties
celeborn.worker.storage.dirs  /tmp/celeborn
```

## Monitoring

- **Master UI:** http://localhost:9098
- **Worker UI:** http://localhost:9096
- **Prometheus Metrics:** http://localhost:9096/metrics/prometheus

## Stopping Services

```bash
cd ../celeborn
./sbin/stop-worker.sh
./sbin/stop-master.sh
```

## Files

- `celeborn_simple_test.py` - Basic shuffle test
- `celeborn_pyspark_example.py` - Comprehensive example with multiple operations


