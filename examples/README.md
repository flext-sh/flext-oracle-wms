# FLEXT Oracle WMS - Usage Examples

This directory contains comprehensive examples demonstrating Oracle WMS Cloud integration patterns using the flext-oracle-wms library. All examples are tested and represent real-world usage scenarios.

## 📁 Example Categories

### 🚀 **Getting Started**

- **[basic_usage.py](basic_usage.py)** - Simple client setup and entity discovery
- **[configuration.py](configuration.py)** - Configuration management patterns
- **[authentication.py](authentication.py)** - Multiple authentication methods

### 🔍 **Data Operations**

- **[entity_discovery.py](entity_discovery.py)** - Comprehensive entity discovery
- **[inventory_queries.py](inventory_queries.py)** - Inventory data querying patterns
- **[schema_processing.py](schema_processing.py)** - Dynamic schema discovery and processing
- **[data_filtering.py](data_filtering.py)** - Advanced filtering and pagination

### 🏗️ **Enterprise Integration**

- **[flext_integration.py](flext_integration.py)** - Integration with FLEXT ecosystem
- **[error_handling.py](error_handling.py)** - Comprehensive error handling patterns
- **[performance_optimization.py](performance_optimization.py)** - Caching and performance
- **[monitoring.py](monitoring.py)** - Logging and observability

### 📊 **Data Pipeline Integration**

- **[singer_integration.py](singer_integration.py)** - Singer protocol patterns
- **[batch_processing.py](batch_processing.py)** - Bulk data operations
- **[real_time_sync.py](real_time_sync.py)** - Real-time data synchronization

### 🧪 **Testing & Development**

- **[mock_testing.py](mock_testing.py)** - Testing with mock client
- **[development_patterns.py](development_patterns.py)** - Development best practices
- **[debugging.py](debugging.py)** - Debugging and diagnostics

## 🎯 **Quick Start**

### Basic Client Setup

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# Configure Oracle WMS connection
config = FlextOracleWmsClientConfig(
    base_url="https://your-wms-instance.oraclecloud.com",
    username="your_username",
    password="your_password"
)

# Initialize client
client = FlextOracleWmsClient(config)

# Discover available entities
result = await client.discover_entities()
if result.success:
    print(f"Found {len(result.data)} WMS entities")
    for entity in result.data:
        print(f"- {entity.name}: {entity.description}")
```

### Environment Configuration

```bash
# Set environment variables for Oracle WMS
export FLEXT_ORACLE_WMS_BASE_URL="https://your-wms.oraclecloud.com"
export FLEXT_ORACLE_WMS_USERNAME="your_username"
export FLEXT_ORACLE_WMS_PASSWORD="your_password"
export FLEXT_ORACLE_WMS_AUTH_METHOD="basic"
```

## 📖 **Example Structure**

Each example follows a consistent structure:

```python
"""
Example: [Description]

This example demonstrates [specific functionality] with Oracle WMS Cloud
integration using the flext-oracle-wms library.

Requirements:
    - Oracle WMS Cloud instance access
    - Valid authentication credentials
    - [Additional requirements if any]

Environment Variables:
    - FLEXT_ORACLE_WMS_BASE_URL: Oracle WMS Cloud base URL
    - FLEXT_ORACLE_WMS_USERNAME: Authentication username
    - FLEXT_ORACLE_WMS_PASSWORD: Authentication password

Usage:
    python [example_file.py]:
"""

import asyncio
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

async def main():
    """Main example function with comprehensive error handling."""
    # Implementation here
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 **Prerequisites**

### Oracle WMS Cloud Access

- Valid Oracle WMS Cloud instance
- API access credentials (username/password or API key)
- Appropriate permissions for entity discovery and data access

### Python Environment

```bash
# Install dependencies
pip install flext-oracle-wms

# Or with Poetry
poetry add flext-oracle-wms
```

### Environment Setup

```bash
# Copy example environment file
cp .env.example .env

# Edit with your Oracle WMS credentials
nano .env
```

## 🚨 **Security Notes**

### Credential Management

- **Never hardcode credentials** in examples or production code
- Use environment variables or secure credential management
- Rotate credentials regularly following security best practices

### Network Security

- Ensure HTTPS connections to Oracle WMS Cloud
- Use secure authentication methods (Bearer tokens preferred)
- Implement proper timeout and retry mechanisms

## 🧪 **Testing Examples**

### Run Individual Examples

```bash
# Run specific example
python examples/basic_usage.py

# Run with debug logging
FLEXT_LOG_LEVEL=debug python examples/entity_discovery.py
```

### Run All Examples

```bash
# Test all examples (requires environment setup)
python -m pytest examples/ -v

# Run examples in development mode
make examples-test
```

## 📚 **Additional Resources**

### Documentation

- **[Project README](../README.md)** - Complete project overview
- **[API Documentation](../docs/api/)** - Detailed API reference
- **[Development Guide](../CLAUDE.md)** - Development practices

### Oracle WMS Resources

- **[Oracle WMS Cloud Documentation](https://docs.oracle.com/en/cloud/saas/warehouse-management/)**
- **[REST API Reference](https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/)**
- **[Authentication Guide](https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/Authentication.html)**

## 🤝 **Contributing Examples**

### Adding New Examples

1. Follow the standard example structure
2. Include comprehensive docstrings and comments
3. Test with actual Oracle WMS environment
4. Update this README with new example description

### Example Quality Standards

- **Professional English** throughout
- **Working code** tested with Oracle WMS Cloud
- **Comprehensive error handling** with FlextResult patterns
- **Clear documentation** explaining purpose and usage
- **Security best practices** for credential management

---

**Last Updated**: January 4, 2025  
**Example Status**: Production Ready  
**Environment**: Oracle WMS Cloud Integration  
**Language**: Python 3.13+
