# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**flext-oracle-wms** is an enterprise Oracle Warehouse Management System (WMS) integration library built with Python 3.13 and designed for the FLEXT data integration platform. It provides comprehensive WMS operations including inventory management, shipping, receiving, picking, putaway, and cycle counting through Oracle WMS Cloud APIs.

## Architecture

### Core Design Patterns

- **Clean Architecture**: Domain-driven design with clear layer separation using flext-core patterns
- **Enterprise Integration**: Built on flext-api and flext-core foundation libraries
- **Declarative APIs**: API catalog-driven approach for endpoint discovery and management
- **FlextResult Pattern**: Railway-oriented programming for error handling
- **Type Safety**: Strict MyPy configuration with comprehensive type annotations

### Key Components

- **Client Layer**: `FlextOracleWmsClient` - Main client interface using flext-api patterns
- **Authentication**: Enterprise auth patterns with multiple authentication methods
- **Configuration**: Unified config management eliminating tap/target duplication
- **Discovery**: Automatic entity discovery and schema processing
- **Cache Management**: Enterprise caching using flext-core patterns
- **API Catalog**: Declarative API definitions with endpoint categorization

### Dependencies

Core dependencies are managed through flext ecosystem libraries:

- `flext-core`: Base patterns, logging, result handling, dependency injection
- `flext-api`: API client patterns and enterprise authentication
- `flext-observability`: Monitoring and observability features
- `pydantic`: Data validation and settings management
- `httpx`: Async HTTP client for API communications

## Development Commands

### Essential Quality Gates (Zero Tolerance)

```bash
make validate          # Complete validation: lint + type + security + test (90% coverage minimum)
make check            # Essential checks: lint + type + test (pre-commit standard)
make test             # Run tests with 90% coverage requirement
```

### Code Quality

```bash
make lint             # Ruff linting (ALL 17 rule categories enabled)
make type-check       # MyPy strict mode type checking (zero errors tolerated)
make security         # Security scans: bandit + pip-audit + detect-secrets
make format           # Format code with ruff
make fix              # Auto-fix all issues: format + imports + lint

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: Oracle DB Integration Duplication
**Status**: ALTO - Duplicação de patterns com flext-db-oracle
**Problema**:
- WMS-specific Oracle patterns não reutilizam flext-db-oracle
- Connection management duplicado
- Oracle type handling não shared

**TODO**:
- [ ] Integrar com flext-db-oracle como base library
- [ ] Reutilizar Oracle connection patterns de flext-db-oracle
- [ ] Extend flext-db-oracle com WMS-specific optimizations
- [ ] Documentar Oracle WMS specialization strategy

### 🚨 GAP 2: Singer Integration Incomplete
**Status**: ALTO - WMS operations não expostas via Singer
**Problema**:
- Não integra com flext-tap-oracle-wms e flext-target-oracle-wms
- WMS catalog não generated via Singer patterns
- Real-time inventory streaming não implemented

**TODO**:
- [ ] Integrar completamente com WMS Singer projects
- [ ] Implementar WMS catalog generation
- [ ] Criar real-time inventory Singer streams
- [ ] Documentar WMS Singer integration patterns

### 🚨 GAP 3: Business Logic vs Infrastructure Mix
**Status**: ALTO - WMS business logic misturado com infrastructure
**Problema**:
- Inventory management, shipping, picking são business domains
- API client patterns mixed com business rules
- Domain entities não clearly separated

**TODO**:
- [ ] Refatorar para separar WMS domain logic de infrastructure
- [ ] Criar WMS domain entities (Inventory, Shipment, Pick, etc.)
- [ ] Implementar WMS business services usando Clean Architecture
- [ ] Documentar WMS domain model
```

### Testing Commands

```bash
# Core testing
make test             # Full test suite with coverage
make test-unit        # Unit tests only
make test-integration # Integration tests only

# WMS-specific testing
make test-wms         # WMS-specific functionality tests
make test-oracle      # Oracle database connectivity tests
make test-inventory   # Inventory management tests
make test-shipping    # Shipping operations tests
make test-performance # Performance benchmarks

# Coverage reporting
make coverage         # Generate detailed coverage report
make coverage-html    # Generate and open HTML coverage report
```

### Oracle WMS Operations

```bash
# Core WMS operations
make wms-test         # Test WMS connectivity and functionality
make wms-validate     # Validate WMS configuration
make wms-schema       # Validate WMS database schema
make wms-sync         # Synchronize WMS data

# Warehouse operations
make wms-inventory    # Test inventory operations
make wms-shipping     # Test shipping operations
make wms-receiving    # Test receiving operations
make wms-picking      # Test picking operations
make wms-putaway      # Test putaway operations
make wms-cycle-count  # Test cycle counting

# Oracle database operations
make oracle-connect   # Test Oracle WMS database connection
make oracle-schema    # Validate Oracle WMS schema
make oracle-performance # Run Oracle performance tests
```

### Development Setup

```bash
make setup            # Complete development setup (install + pre-commit)
make install          # Install dependencies with Poetry
make dev-install      # Development environment setup
make pre-commit       # Setup pre-commit hooks
```

### Running Individual Tests

```bash
# Run specific test files
pytest tests/test_client.py -v
pytest tests/test_authentication.py -v
pytest tests/test_integration_declarative.py -v

# Run tests with specific markers
pytest -m unit -v           # Unit tests only
pytest -m integration -v    # Integration tests only
pytest -m declarative -v    # Declarative integration tests
pytest -m lgf_api -v        # LGF API specific tests
pytest -m automation -v     # Automation tests
pytest -m performance -v    # Performance tests

# Run single test with debugging
pytest tests/test_client.py::TestFlextOracleWmsClient::test_initialization -v -s
```

## Code Architecture

### Main Client Interface

The `FlextOracleWmsClient` in `src/flext_oracle_wms/client.py` is the primary interface, implementing:

- Declarative API catalog-driven operations
- Enterprise authentication patterns
- Automatic entity discovery and schema processing
- Comprehensive error handling with FlextResult patterns

### Configuration Management

Unified configuration through `FlextOracleWmsClientConfig` and `FlextOracleWmsModuleConfig`:

- Environment-specific settings
- Authentication configuration
- API version management
- Connection pooling and timeout settings

### API Catalog System

`src/flext_oracle_wms/api_catalog.py` provides declarative API definitions:

- Categorized endpoints (inventory, shipping, receiving, etc.)
- Version-specific API paths
- Standardized request/response patterns

### Authentication Patterns

Multiple authentication methods supported:

- Basic Authentication
- Bearer Token Authentication
- API Key Authentication
- Enterprise SSO integration

### Error Handling

Comprehensive exception hierarchy in `src/flext_oracle_wms/exceptions.py`:

- `FlextOracleWmsError`: Base exception class
- `FlextOracleWmsConnectionError`: Connection-related errors
- `FlextOracleWmsAuthenticationError`: Authentication failures
- `FlextOracleWmsApiError`: API operation errors
- `FlextOracleWmsDataValidationError`: Data validation errors

## Testing Strategy

### Test Structure

```
tests/
├── test_authentication.py        # Authentication testing
├── test_client.py                # Core client functionality
├── test_client_class.py          # Client class testing
├── test_integration_declarative.py # Declarative integration tests
├── test_helpers.py               # Helper function tests
├── test_models.py                # Data model validation
└── conftest.py                   # Shared test fixtures
```

### Test Markers

The project uses pytest markers for test categorization:

- `unit`: Unit tests for individual components
- `integration`: Integration tests with external systems
- `declarative`: Declarative integration tests
- `lgf_api`: LGF API specific tests
- `automation`: Automation workflow tests
- `performance`: Performance benchmarking tests
- `slow`: Tests that take longer to execute

### Quality Requirements

- **90% minimum test coverage** (enforced by CI)
- **Zero MyPy errors** in strict mode
- **All Ruff rules enabled** for comprehensive linting
- **Security scanning** with bandit and pip-audit
- **Pre-commit hooks** for automated quality gates

## Development Workflow

### Before Making Changes

1. Run `make check` to ensure current state is clean
2. Create feature branch from main
3. Set up development environment with `make dev-install`

### During Development

1. Write tests first following TDD principles
2. Implement changes using established patterns from flext-core
3. Run `make validate` frequently during development
4. Use type hints throughout for better IDE support

### Before Committing

1. Run `make validate` to ensure all quality gates pass
2. Verify test coverage meets 90% requirement
3. Check that no sensitive information is included
4. Pre-commit hooks will run automatically

## Integration Points

### FLEXT Ecosystem Integration

This library integrates with the broader FLEXT ecosystem:

- **flext-core**: Provides foundational patterns and utilities
- **flext-api**: Enterprise API client patterns
- **flext-observability**: Monitoring and metrics collection
- Uses standard FLEXT configuration and logging patterns

### Oracle WMS Cloud APIs

Integration with Oracle WMS Cloud REST APIs:

- Inventory management operations
- Shipping and receiving workflows
- Warehouse operations (picking, putaway, cycle counting)
- Real-time data synchronization
- Performance-optimized batch operations

## Common Patterns

### Using the Client

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

config = FlextOracleWmsClientConfig(
    base_url="https://your-wms-instance.oraclecloud.com",
    username="your_username",
    password="your_password"
)

client = FlextOracleWmsClient(config)
result = await client.discover_entities()
```

### Error Handling

```python
from flext_oracle_wms import FlextOracleWmsClient

async def safe_operation():
    result = await client.get_inventory_data("entity_name")
    if result.is_success:
        return result.data
    else:
        logger.error(f"Operation failed: {result.error}")
        return None
```

### Configuration Patterns

Follow flext-core configuration standards with environment variable support and type validation.
