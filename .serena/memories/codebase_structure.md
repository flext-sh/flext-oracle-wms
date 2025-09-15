# Codebase Structure Overview

## Directory Layout
```
flext-oracle-wms/
├── src/flext_oracle_wms/           # Main package (18 Python files)
├── tests/                          # Test suite (26 test files)
├── docs/                          # Documentation (restructured)
├── examples/                      # Usage examples
├── scripts/                       # Utility scripts
├── reports/                       # Coverage/quality reports
├── Makefile                       # Build automation
├── pyproject.toml                 # Project configuration
├── docker-compose.yml             # Container orchestration
└── README.md                      # Project documentation
```

## Core Source Modules (src/flext_oracle_wms/)
1. **__init__.py** - Package exports and API surface
2. **wms_client.py** - Main Oracle WMS client (570+ lines)
3. **wms_discovery.py** - Entity discovery logic (1489+ lines, largest file)
4. **wms_config.py** - Configuration management 
5. **wms_api.py** - API endpoint definitions (22 endpoints)
6. **wms_exceptions.py** - Exception hierarchy (16 exception classes)
7. **wms_operations.py** - Business operations
8. **wms_models.py** - Data models and types
9. **authentication.py** - Auth handling
10. **http_client.py** - HTTP client wrapper
11. **filtering.py** - Data filtering utilities
12. **flattening.py** - Data flattening for Singer
13. **dynamic.py** - Dynamic schema processing
14. **cache.py** - Caching implementations
15. **api_service.py** - API service layer
16. **wms_constants.py** - Constants and enums

## Key Statistics
- **Total Lines**: 6,974 lines across all source files
- **Implementation vs Scaffolding**: ~5,112 implementation lines, ~1,862 comments/docs/empty
- **Classes**: 99 total (violates FLEXT unified class requirement)
- **API Endpoints**: 22 Oracle WMS endpoints defined
- **Test Files**: 26 test modules with comprehensive coverage

## Architecture Patterns
- **Domain-Driven Design**: Separate concerns for client, discovery, operations
- **Type Safety**: Comprehensive Pydantic models and MyPy annotations  
- **Error Handling**: FlextResult pattern for type-safe error handling
- **Configuration**: Pydantic-based config with validation
- **Testing**: Mock server for development, real integration target

## Major Components
- **Client Layer**: FlextOracleWmsClient for Oracle WMS communication
- **Discovery Engine**: Dynamic schema and entity discovery
- **Operations Layer**: Business logic for WMS operations
- **Configuration**: Flexible config with environment support
- **Exception Handling**: Comprehensive error hierarchy
- **Testing Infrastructure**: Mock server and test utilities