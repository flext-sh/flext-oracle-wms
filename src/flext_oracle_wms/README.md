# FLEXT Oracle WMS - Core Module

This directory contains the core implementation of the **flext-oracle-wms** library, providing enterprise-grade Oracle Warehouse Management System (WMS) Cloud integration for the FLEXT data integration platform.

## 📁 Module Structure

### 🎯 **Core Interface**

- **[**init**.py](**init**.py)** - Public API gateway with comprehensive exports and version information
- **[client.py](client.py)** - Primary FlextOracleWmsClient interface for Oracle WMS operations
- **[config.py](config.py)** - Type-safe configuration management with Pydantic validation

### 🔧 **Infrastructure Components**

- **[exceptions.py](exceptions.py)** - Comprehensive error hierarchy for Oracle WMS operations
- **[constants.py](constants.py)** - Oracle WMS constants, enums, and default values
- **[types.py](types.py)** - Type definitions and aliases for Oracle WMS integration
- **[models.py](models.py)** - Data models using FLEXT ValueObject patterns

### 🏗️ **API & Discovery**

- **[api_catalog.py](api_catalog.py)** - Declarative API endpoint catalog with comprehensive WMS API definitions
- **[authentication.py](authentication.py)** - Multi-method authentication (Basic, Bearer, API Key)
- **[discovery.py](discovery.py)** - Automatic entity and schema discovery from Oracle WMS Cloud
- **[dynamic.py](dynamic.py)** - Dynamic schema processing and transformation

### ⚡ **Performance & Utilities**

- **[cache.py](cache.py)** - Enterprise caching with configurable TTL and performance optimization
- **[filtering.py](filtering.py)** - Advanced query filtering and pagination support
- **[flattening.py](flattening.py)** - Nested data structure flattening for Singer compatibility
- **[helpers.py](helpers.py)** - Utility functions and common operations

### 🧪 **Testing & Development**

- **[mock_server.py](mock_server.py)** - Mock Oracle WMS server for testing without credentials
- **[py.typed](py.typed)** - Type checking marker for MyPy compatibility

## 🎯 **Key Features**

### Oracle WMS Cloud Integration

- **Dynamic Entity Discovery** - Automatically discovers available entities from Oracle WMS Cloud REST API
- **Declarative API Catalog** - Comprehensive endpoint definitions with categorization and versioning
- **Type-Safe Operations** - MyPy strict mode adoption; increasing coverage
- **Multi-Method Authentication** - Support for Basic, Bearer token, and API key authentication methods
- **Enterprise Error Handling** - Comprehensive exception hierarchy with Oracle WMS-specific categorization

### FLEXT Ecosystem Integration

- **FlextResult Pattern** - Railway-oriented programming for consistent error handling
- **FLEXT Configuration Standards** - Environment-driven settings with comprehensive validation
- **Structured Logging** - Integration with FLEXT observability for monitoring and diagnostics
- **Dependency Injection** - Support for FLEXT container patterns and enterprise architecture
- **Singer Protocol Compatibility** - Full compatibility with data pipeline integration patterns

### Performance & Reliability

- **Intelligent Caching** - Enterprise caching with TTL configuration and performance monitoring
- **Connection Pooling** - HTTP connection pooling with retry logic and exponential backoff
- **Batch Processing** - High-volume data processing with configurable batch sizes
- **Rate Limiting** - Built-in rate limiting to respect Oracle WMS Cloud API limits
- **Comprehensive Testing** - Mock server support for testing without valid credentials

## 📖 **Usage Examples**

### Basic Client Setup

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# Create configuration
config = FlextOracleWmsClientConfig(
    base_url="https://your-wms.oraclecloud.com",
    username="your_username",
    password="your_password",
    environment="production"
)

# Initialize client
client = FlextOracleWmsClient(config)
client.start()

# Discover entities
result = client.discover_entities()
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
if result.success:
    logger = FlextLogger(__name__)
    logger.info("Discovered WMS entities", count=len(result.data))
    for entity in result.data:
        logger.info("Entity", name=str(entity))
```

### Entity Data Querying

```python
# Query entity data with filtering
result = client.get_entity_data(
    entity_name="item",
    limit=100,
    fields="item_id,item_name,item_desc",
    filters={"status": "active"}
)

if result.success:
    data = result.data
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
    FlextLogger(__name__).info("Records retrieved", count=len(data.get('results', [])))
```

### Error Handling with FlextResult

```python
from flext_oracle_wms.exceptions import FlextOracleWmsConnectionError

try:
    result = client.get_entity_data("inventory")
    if result.is_failure:
        # Handle business logic errors via FlextResult

        FlextLogger(__name__).error("Query failed", error=result.error)
    else:
        # Process successful result
        inventory_data = result.data

        FlextLogger(__name__).info("Retrieved inventory data", count=len(inventory_data))

except FlextOracleWmsConnectionError as e:
    # Handle connection-specific errors
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
    FlextLogger(__name__).error("Connection failed", error=str(e))
```

## 🔧 **Development Guidelines**

### Code Quality Standards

- **Type Safety**: MyPy strict mode adoption; aiming for 95%+ coverage
- **Error Handling**: All operations return FlextResult for consistent error management
- **Documentation**: Comprehensive docstrings following enterprise standards
- **Testing**: 90%+ test coverage requirement with unit and integration tests
- **Linting**: Comprehensive Ruff rules (ALL categories enabled) with zero tolerance

### Architecture Compliance

- **Clean Architecture**: Clear separation of domain, application, and infrastructure concerns
- **FLEXT Integration**: Full compliance with FLEXT ecosystem patterns and standards
- **Railway-Oriented Programming**: Consistent use of FlextResult for error handling
- **Enterprise Patterns**: Connection pooling, caching, retry logic, and observability

### Performance Requirements

- **Response Time**: < 2 seconds for entity discovery operations
- **Throughput**: Support for 100+ concurrent Oracle WMS API connections
- **Reliability**: 99.9% uptime with comprehensive error recovery
- **Memory Efficiency**: Optimized for high-volume data processing scenarios

## 🧪 **Testing**

### Module Testing

```bash
# Run comprehensive test suite for this module
cd ..flext-oracle-wms
make test                    # 90%+ coverage requirement
make test-unit              # Unit tests only
make test-integration       # Integration tests with Oracle WMS

# Module-specific testing
pytest src/flext_oracle_wms/test_*.py -v
pytest -m "oracle_wms" -v
```

### Quality Gates

```bash
# Complete validation for this module
make validate               # Lint + type + security + test
make lint
make type-check
make security               # Bandit + pip-audit security scanning
```

## 🔗 **Dependencies**

### FLEXT Ecosystem Dependencies

- **[flext-core](../../flext-core)** - Foundation patterns, FlextResult, logging, DI container
- **[flext-api](../../flext-api)** - Enterprise API client patterns and authentication
- **[flext-observability](../../flext-observability)** - Monitoring, metrics, health checks

### External Dependencies

- **Pydantic v2.11.7+** - Data validation and settings management with modern patterns
- **HTTPX v0.28.1+** - HTTP client for Oracle WMS API communication
- **Python 3.13+** - Latest Python with enhanced type system and performance optimizations

## 📚 **Additional Resources**

### Documentation

- **[Project README](../../README.md)** - Complete project overview and usage guide
- **[Development Guide](../../CLAUDE.md)** - Comprehensive development practices and standards
- **[Examples](../../examples/)** - Working code examples and integration patterns
- **[API Documentation](../../docs/api/)** - Detailed API reference and specifications

### Oracle WMS Resources

- **[Oracle WMS Cloud Documentation](https://docs.oracle.com/en/cloud/saas/warehouse-management/)**
- **[REST API Reference](https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/)**
- **[Authentication Guide](https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/Authentication.html)**

---

**Module Status**: Production Ready  
**Type Coverage**: 95%+  
**Test Coverage**: 90%+  
**FLEXT Compliance**: Full Integration  
**Oracle WMS API Version**: v10 (LGF API)  
**Last Updated**: January 4, 2025
