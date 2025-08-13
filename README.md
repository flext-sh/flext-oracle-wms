# flext-oracle-wms

**Type**: Infrastructure Library | **Status**: Active Development | **Dependencies**: flext-core

Oracle WMS Cloud integration library providing REST API connectivity and data operations for the FLEXT ecosystem.

> ⚠️ Development Status: API client working; entity discovery functional; Singer integration incomplete; business domain separation needed.

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig; config = FlextOracleWmsClientConfig(base_url='https://test.com', username='test', password='test'); print('✅ Working')"

# Development setup
make setup
```

## Current Reality

**What Actually Works:**

- REST API client with async HTTP operations
- Multiple authentication methods (basic, bearer, API key)
- Entity discovery and schema processing
- Configuration management with Pydantic validation
- Error handling with FlextResult patterns

**What Needs Work:**

- Singer ecosystem integration (tap/target/DBT projects)
- Business domain separation (WMS vs infrastructure)
- Oracle database integration with flext-db-oracle
- Performance optimization (connection pooling, caching)

## Architecture Role in FLEXT Ecosystem

### **Infrastructure Component**

FLEXT Oracle WMS provides Oracle WMS Cloud connectivity for data integration:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | Web | CLI | Quality | Observability  │
├═════════════════════════════════════════════════════════════════┤
│ Infrastructure: Oracle | LDAP | LDIF | gRPC | [ORACLE-WMS]      │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├─────────────────────────────────────────────────────────────────┤
│ Foundation: FLEXT-CORE (FlextResult | DI | Domain Patterns)     │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **WMS API Client**: REST API connectivity with Oracle WMS Cloud
2. **Entity Discovery**: Automatic schema and endpoint discovery
3. **Data Operations**: Query, filter, and transform WMS data

## Key Features

### **Current Capabilities**

- **FlextOracleWmsClient**: Main client interface with async operations
- **Multi-Auth Support**: Basic, Bearer Token, and API Key authentication
- **Entity Discovery**: Automatic WMS entity and schema discovery
- **Configuration Management**: Type-safe config with environment variables

### **FLEXT Core Integration**

- **FlextResult Pattern**: Type-safe error handling for all operations
- **Enterprise Patterns**: Clean Architecture and dependency injection
- **Structured Logging**: Integration with flext-observability

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-oracle-wms
poetry install

# Development setup
make setup
```

### Basic Usage

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# Configure client
config = FlextOracleWmsClientConfig(
    base_url="https://your-wms-instance.oraclecloud.com",
    username="your_username",
    password="your_password"
)

# Initialize client
async def main():
    client = FlextOracleWmsClient(config)

    # Discover entities
    result = await client.discover_entities()
    if result.success:
        entities = result.data
        print(f"Found {len(entities)} WMS entities")
    else:
        print(f"Discovery failed: {result.error}")
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation pipeline (run before commits)
make validate              # Full validation (lint + type + security + test)
make check                 # Quick lint + type check + test
make test                  # Run all tests (90% coverage requirement)
make lint                  # Code linting
make type-check            # Type checking
make format                # Code formatting
make security              # Security scanning
```

### Testing

```bash
# Test categories
make test-unit             # Unit tests only
make test-integration      # Integration tests only
make coverage-html         # Generate HTML coverage report

# Specific test patterns
pytest tests/test_client.py -v
pytest -k "authentication" -v
pytest -m integration -v
```

## Configuration

### Environment Variables

```bash
# WMS connection settings
export FLEXT_ORACLE_WMS_BASE_URL="https://your-wms.oraclecloud.com"
export FLEXT_ORACLE_WMS_USERNAME="api_user"
export FLEXT_ORACLE_WMS_PASSWORD="secure_password"

# Authentication configuration
export FLEXT_ORACLE_WMS_AUTH_METHOD="basic"  # basic, bearer, api_key
export FLEXT_ORACLE_WMS_TIMEOUT="30"
export FLEXT_ORACLE_WMS_MAX_RETRIES="3"
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 90% target
- **Type Safety**: MyPy strict mode adoption
- **Linting**: Ruff with comprehensive rules
- **Security**: Bandit + pip-audit scanning

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
from flext_oracle_wms import FlextOracleWmsClient

async def safe_operation():
    result = await client.discover_entities()
    if result.success:
        return result.data
    else:
        logger.error(f"Operation failed: {result.error}")
        return None
```

### **Service Integration**

- **flext-db-oracle**: Oracle database connectivity patterns
- **Singer Ecosystem**: Integration with tap/target/DBT projects
- **flext-observability**: Monitoring and metrics collection

## Current Status

**Version**: 0.9.0 (Development)

**Completed**:

- ✅ REST API client with async HTTP operations
- ✅ Multiple authentication methods
- ✅ Entity discovery and schema processing
- ✅ Type-safe configuration management

**In Progress**:

- 🔄 Singer ecosystem integration
- 🔄 Performance optimization (connection pooling, caching)
- 🔄 Business domain separation

**Planned**:

- 📋 Oracle database integration with flext-db-oracle
- 📋 Real-time inventory streaming
- 📋 Advanced WMS business operations

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain 90% coverage
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---
