# Apache Celeborn with S3 Support & PySpark Integration

This repository contains a working setup of Apache Celeborn with S3 storage support and PySpark integration examples.

⚠️ **All sensitive credentials have been removed for GitHub safety.**

## 📁 Directory Structure

```
comp/
├── celeborn/              # Apache Celeborn source code
│   ├── conf/             # Configuration files (credentials removed)
│   ├── sbin/             # Start/stop scripts (including debug mode)
│   └── ...               # Source code and build artifacts
├── src/                   # PySpark example scripts
│   ├── celeborn_simple_test.py         # Simple shuffle test
│   ├── celeborn_pyspark_example.py     # Comprehensive example
│   └── README.md                        # Usage instructions
├── .gitignore             # Protects credentials and build artifacts
└── SETUP_GUIDE.md         # Complete setup and configuration guide
```

## 🚀 Quick Start

1. **Read the [SETUP_GUIDE.md](SETUP_GUIDE.md)** for detailed instructions

2. **Configure your credentials** in `celeborn/conf/celeborn-defaults.conf`
   ```properties
   celeborn.hadoop.fs.s3a.access.key  YOUR_AWS_ACCESS_KEY
   celeborn.hadoop.fs.s3a.secret.key  YOUR_AWS_SECRET_KEY
   ```

3. **Build Celeborn with S3 support**
   ```bash
   cd celeborn
   ./build/mvn clean package -DskipTests -Paws -Pspark-4.0
   ```

4. **Start services**
   ```bash
   ./sbin/start-master.sh
   ./sbin/start-worker.sh
   ```

5. **Run PySpark examples**
   ```bash
   cd ../src
   python celeborn_simple_test.py
   ```

## ✨ Features

✅ **S3 Storage Support** - Remote shuffle storage in S3  
✅ **Debug Mode** - Remote debugging on ports 5005 (Master) & 5006 (Worker)  
✅ **PySpark Integration** - Working examples with Scala 2.13  
✅ **Credentials Safe** - All sensitive data removed/templatized  

## 📊 Key Issues Solved

1. **ClassNotFoundException: S3AFileSystem** → Build with `-Paws` profile
2. **Scala Version Mismatch** → Build with `-Pspark-4.0` for Scala 2.13
3. **Java Version Requirements** → Java 17 for PySpark, Java 11 for services
4. **Runtime Classpath** → Created symlinks and copied module JARs

## 🔗 Resources

- **Master UI:** http://localhost:9098
- **Worker UI:** http://localhost:9096
- **Celeborn Docs:** https://celeborn.apache.org/

## ⚙️ Configuration

See `celeborn/conf/celeborn-defaults.conf.template` for all available options.

**Important:** The actual `celeborn-defaults.conf` is gitignored to protect credentials.

## 🛑 Before Committing

Run this check:
```bash
# Verify no credentials in tracked files
git grep -E "(AKIA|secret|key.*=" -- '*.conf' '*.py' '*.sh' || echo "✅ No credentials found"
```

## 📝 License

Apache License 2.0 - See `celeborn/LICENSE`

