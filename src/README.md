# FLEXT Oracle WMS - Source Code

This directory contains the core implementation of the flext-oracle-wms library, providing enterprise-grade Oracle Warehouse Management System (WMS) Cloud integration for the FLEXT data integration platform.

## 📁 Module Organization

### 🎯 **Core Interface**

- **[flext_oracle_wms/](flext_oracle_wms/)** - Main library package with enterprise Oracle WMS integration

### 🏗️ **Architecture Overview**

The source code follows Clean Architecture principles with clear separation of concerns:

```
src/flext_oracle_wms/
├── __init__.py              # Public API gateway with comprehensive exports
├── client.py                # Primary client interface for Oracle WMS operations
├── config.py               # Type-safe configuration management with Pydantic
├── exceptions.py           # Comprehensive error hierarchy for Oracle WMS
├── constants.py            # Oracle WMS constants, enums, and defaults
├── types.py                # Type definitions and aliases for Oracle WMS
├── models.py               # Data models using FLEXT ValueObject patterns
├── api_catalog.py          # Declarative API endpoint catalog
├── authentication.py       # Multi-method authentication (Basic, Bearer, API Key)
├── discovery.py            # Automatic entity and schema discovery
├── dynamic.py              # Dynamic schema processing and transformation
├── cache.py                # Enterprise caching with performance optimization
├── filtering.py            # Advanced query filtering and pagination
├── flattening.py           # Nested data structure flattening
└── helpers.py              # Utility functions and common operations
```

## 🎯 **Key Features**

### Oracle WMS Cloud Integration

- **Type-safe REST API client** with async support and comprehensive error handling
- **Multi-method authentication** supporting Basic, Bearer token, and API key methods
- **Automatic entity discovery** with schema introspection and validation
- **Declarative API catalog** for endpoint management and versioning
- **Enterprise caching** with configurable TTL and performance optimization

### FLEXT Ecosystem Integration

- **FlextResult pattern** for railway-oriented programming and consistent error handling
- **FLEXT configuration standards** with environment-driven settings and validation
- **Structured logging** with correlation IDs and enterprise observability
- **Dependency injection** support with FLEXT container integration
- **Singer protocol compatibility** for data pipeline integration

### Performance & Reliability

- **Connection pooling** and retry logic with exponential backoff
- **Intelligent caching** with cache invalidation and performance monitoring
- **Batch operations** for high-volume data processing
- **Comprehensive error handling** with Oracle WMS-specific error categorization
- **Type safety** with 95%+ type annotation coverage and strict MyPy validation

## 📖 **Module Documentation**

### Core Client Interface

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# Type-safe configuration
config = FlextOracleWmsClientConfig(
    base_url="https://your-wms.oraclecloud.com",
    username="your_username",
    password="your_password"
)

# Enterprise client with comprehensive error handling
client = FlextOracleWmsClient(config)
result = await client.discover_entities()

# Railway-oriented programming with FlextResult
if result.success:
    entities = result.data
    print(f"Discovered {len(entities)} WMS entities")
else:
    logger.error(f"Discovery failed: {result.error}")
```

### Configuration Management

```python
from flext_oracle_wms import FlextOracleWmsClientConfig

# Environment-driven configuration with validation
config = FlextOracleWmsClientConfig(
    base_url=os.getenv("FLEXT_ORACLE_WMS_BASE_URL"),
    username=os.getenv("FLEXT_ORACLE_WMS_USERNAME"),
    password=os.getenv("FLEXT_ORACLE_WMS_PASSWORD"),
    auth_method="basic",
    timeout=30,
    max_retries=3,
    enable_caching=True
)
```

### Error Handling

```python
from flext_oracle_wms.exceptions import (
    FlextOracleWmsError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsAuthenticationError
)

try:
    result = await client.query_entity_data("INVENTORY")
    if result.is_failure:
        # Handle business logic errors via FlextResult
        logger.error(f"Query failed: {result.error}")
except FlextOracleWmsConnectionError:
    # Handle connection issues
    logger.error("Failed to connect to Oracle WMS")
except FlextOracleWmsAuthenticationError:
    # Handle authentication failures
    logger.error("Oracle WMS authentication failed")
```

## 🔧 **Development Guidelines**

### Code Quality Standards

- **Type Safety**: 95%+ type annotation coverage with strict MyPy validation
- **Error Handling**: All operations return FlextResult for consistent error management
- **Documentation**: Comprehensive docstrings following enterprise standards
- **Testing**: 90%+ test coverage requirement with unit and integration tests
- **Linting**: Comprehensive Ruff rules (ALL categories enabled) with zero tolerance

### Architecture Compliance

- **Clean Architecture**: Proper separation of domain, application, and infrastructure concerns
- **FLEXT Integration**: Full compliance with FLEXT ecosystem patterns and standards
- **Railway-Oriented Programming**: Consistent use of FlextResult for error handling
- **Enterprise Patterns**: Connection pooling, caching, retry logic, and observability

### Performance Requirements

- **Response Time**: < 2 seconds for entity discovery operations
- **Throughput**: Support for 100+ concurrent Oracle WMS API connections
- **Reliability**: 99.9% uptime with comprehensive error recovery
- **Memory Efficiency**: Optimized for high-volume data processing scenarios

## 🧪 **Testing**

### Test Coverage

```bash
# Run comprehensive test suite
make test                    # 90%+ coverage requirement
make test-unit              # Unit tests only
make test-integration       # Integration tests with Oracle WMS
make coverage-html          # Generate detailed coverage report
```

### Quality Gates

```bash
# Complete quality validation
make validate               # Lint + type + security + test
make lint                   # Ruff linting (all rules)
make type-check             # MyPy strict mode
make security               # Bandit + pip-audit security scanning
```

## 🔗 **Integration**

### FLEXT Ecosystem Dependencies

- **[flext-core](../../flext-core)** - Foundation patterns, FlextResult, logging, DI container
- **[flext-api](../../flext-api)** - Enterprise API client patterns and authentication
- **[flext-observability](../../flext-observability)** - Monitoring, metrics, health checks

### External Dependencies

- **Pydantic v2.11.7+** - Data validation and settings management
- **HTTPX v0.28.1+** - Async HTTP client for Oracle WMS API communication
- **Python 3.13+** - Latest Python with enhanced type system and performance

## 📚 **Additional Resources**

### Documentation

- **[Project README](../README.md)** - Complete project overview and usage guide
- **[Development Guide](../CLAUDE.md)** - Comprehensive development practices
- **[Examples](../examples/)** - Working code examples and integration patterns
- **[API Documentation](../docs/api/)** - Detailed API reference and specifications

### Oracle WMS Resources

- **[Oracle WMS Cloud Documentation](https://docs.oracle.com/en/cloud/saas/warehouse-management/)**
- **[REST API Reference](https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/)**
- **[Authentication Guide](https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/Authentication.html)**

---

**Module Status**: Production Ready  
**Type Coverage**: 95%+  
**Test Coverage**: 90%+  
**FLEXT Compliance**: Full Integration  
**Last Updated**: January 4, 2025
