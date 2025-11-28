# Celeborn with S3 Support - Setup Guide

This guide explains how to build and run Apache Celeborn with S3 storage support and integrate it with PySpark.

## 🚨 Important: Before Committing to GitHub

All sensitive credentials have been removed. When deploying:

1. Copy `celeborn/conf/celeborn-defaults.conf.template` to `celeborn/conf/celeborn-defaults.conf`
2. Add your actual AWS credentials to the config file
3. **Never commit `celeborn-defaults.conf`** (it's in `.gitignore`)

## Prerequisites

### 1. Java Installation
```bash
# Install Java 11 for Celeborn services
brew install openjdk@11

# Install Java 17 for PySpark
brew install openjdk@17
```

### 2. Python Environment
```bash
python3 -m venv path/to/venv
source path/to/venv/bin/activate
pip install pyspark
```

## Building Celeborn

### For Celeborn Services (Java 11, Scala 2.12)
```bash
cd comp/celeborn
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@11/11.0.29/libexec/openjdk.jdk/Contents/Home"
./build/mvn clean package -DskipTests -Paws
```

### For PySpark Integration (Java 17, Scala 2.13)
```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
./build/mvn clean package -DskipTests -Paws -Pspark-4.0
```

**Why two builds?**
- Celeborn services use Scala 2.12
- PySpark 4.x requires Scala 2.13
- The `-Paws` profile includes S3 support (hadoop-aws library)

### Setup Runtime Directories
```bash
cd comp/celeborn

# For Scala 2.12 (Celeborn services)
ln -sf worker/target/scala-2.12/jars worker-jars
ln -sf master/target/scala-2.12/jars master-jars
ln -sf cli/target/scala-2.12/jars cli-jars
cp worker/target/celeborn-worker_2.12-*.jar worker/target/scala-2.12/jars/
cp master/target/celeborn-master_2.12-*.jar master/target/scala-2.12/jars/
cp cli/target/celeborn-cli_2.12-*.jar cli/target/scala-2.12/jars/

# For Scala 2.13 (PySpark integration)
ln -sf worker/target/scala-2.13/jars worker-jars
ln -sf master/target/scala-2.13/jars master-jars
ln -sf cli/target/scala-2.13/jars cli-jars
cp worker/target/celeborn-worker_2.13-*.jar worker/target/scala-2.13/jars/
cp master/target/celeborn-master_2.13-*.jar master/target/scala-2.13/jars/
cp cli/target/celeborn-cli_2.13-*.jar cli/target/scala-2.13/jars/
```

## Configuration

### S3 Storage Configuration

Edit `celeborn/conf/celeborn-defaults.conf`:

```properties
celeborn.storage.availableTypes  S3
celeborn.storage.s3.dir  s3a://your-bucket/shuffle
celeborn.hadoop.fs.s3a.access.key  YOUR_AWS_ACCESS_KEY
celeborn.hadoop.fs.s3a.secret.key  YOUR_AWS_SECRET_KEY
celeborn.storage.s3.endpoint.region  your-region
```

**Security Best Practice:** Use environment variables instead:
```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

### Local Storage Configuration

```properties
celeborn.worker.storage.dirs  /tmp/celeborn
```

## Running Celeborn

### Normal Mode
```bash
cd comp/celeborn
./sbin/start-master.sh
./sbin/start-worker.sh
```

### Debug Mode (with Remote Debugging)
```bash
./sbin/start-master-debug.sh  # Debug port: 5005
./sbin/start-worker-debug.sh  # Debug port: 5006
```

### Verify Services
```bash
# Check processes
ps aux | grep celeborn

# Check ports
lsof -i :9097  # Master RPC
lsof -i :9098  # Master HTTP
lsof -i :9096  # Worker HTTP
lsof -i :5005  # Master Debug
lsof -i :5006  # Worker Debug

# Check logs
tail -f celeborn/logs/celeborn-*-Master*.out
tail -f celeborn/logs/celeborn-*-Worker*.out
```

## Running PySpark Examples

### Setup Environment
```bash
cd src
source ../celeborn/path/to/venv/bin/activate
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export CELEBORN_HOME="$(pwd)/../celeborn"
```

### Run Simple Test
```bash
python celeborn_simple_test.py
```

### Run Full Example
```bash
python celeborn_pyspark_example.py
```

## Debugging in VS Code

### Method 1: Launch from VS Code
Use the built-in launch configurations in `.vscode/launch.json`:
1. Open Run and Debug panel (⇧⌘D)
2. Select "Start Master" or "Start Worker"
3. Press F5 to launch with debugging

### Method 2: Attach to Running Processes
Add this to `.vscode/launch.json`:

```json
{
    "type": "java",
    "request": "attach",
    "name": "Attach to Master",
    "hostName": "localhost",
    "port": 5005
},
{
    "type": "java",
    "request": "attach",
    "name": "Attach to Worker",
    "hostName": "localhost",
    "port": 5006
}
```

## Troubleshooting

### ClassNotFoundException: S3AFileSystem
**Problem:** Missing S3 support libraries  
**Solution:** Rebuild with `-Paws` profile

### NoClassDefFoundError: HttpService
**Problem:** Missing service JARs in classpath  
**Solution:** Copy module JARs to target/scala-*/jars/ directories (see Setup Runtime Directories)

### Scala Version Mismatch
**Problem:** PySpark uses Scala 2.13 but Celeborn built with 2.12  
**Solution:** Build with `-Pspark-4.0` profile for Scala 2.13

### Java Version Mismatch
**Problem:** PySpark requires Java 17+  
**Solution:** Set `JAVA_HOME` and `PATH` to Java 17 before running Python scripts

## Monitoring and UI

- **Master UI:** http://localhost:9098
- **Worker UI:** http://localhost:9096
- **Metrics:** http://localhost:9096/metrics/prometheus

## Stopping Services

```bash
cd comp/celeborn
./sbin/stop-worker.sh
./sbin/stop-master.sh

# Or stop all
./sbin/stop-all.sh
```

## Directory Structure

```
dummy/
├── celeborn/                    # Celeborn source code
│   ├── conf/                    # Configuration files
│   ├── sbin/                    # Start/stop scripts
│   ├── logs/                    # Runtime logs (gitignored)
│   ├── master-jars/             # Symlink to master jars
│   ├── worker-jars/             # Symlink to worker jars
│   └── cli-jars/                # Symlink to cli jars
├── src/                         # Python examples
│   ├── celeborn_simple_test.py
│   ├── celeborn_pyspark_example.py
│   └── README.md
└── .gitignore                   # Protects credentials and build artifacts
```

## Key Points

✅ **All credentials removed** - Safe to commit to GitHub  
✅ **S3 support enabled** - Build with `-Paws` profile  
✅ **Debug mode available** - Remote debugging on ports 5005/5006  
✅ **PySpark compatible** - Scala 2.13 build for PySpark integration  
✅ **Working examples** - Simple test verified shuffle data storage  

## Next Steps

1. Configure your AWS credentials in `celeborn/conf/celeborn-defaults.conf`
2. Start Celeborn services
3. Run Python examples
4. Monitor shuffle data in S3 or local storage

