# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**flext-oracle-wms** is an enterprise Oracle Warehouse Management System (WMS) integration library built with Python 3.13 and designed for the FLEXT data integration platform. It provides a comprehensive client library for Oracle WMS Cloud REST API integration with support for entity discovery, schema processing, and data operations.

## Architecture

### Core Design Patterns

- **Clean Architecture**: Domain-driven design with clear layer separation using flext-core patterns
- **Enterprise Integration**: Built on flext-api and flext-core foundation libraries
- **Declarative APIs**: API catalog-driven approach for endpoint discovery and management
- **FlextResult Pattern**: Railway-oriented programming for error handling (from flext-core)
- **Type Safety**: Strict MyPy configuration with comprehensive type annotations

### Key Components

- **Client Layer**: `FlextOracleWmsClient` in `src/flext_oracle_wms/wms_client.py` - Main client interface
- **API Catalog**: `src/flext_oracle_wms/wms_api.py` - Declarative API endpoint definitions and mock server
- **Authentication**: Integrated in `src/flext_oracle_wms/wms_client.py` - Multiple auth methods (basic, bearer, API key)
- **Configuration**: `src/flext_oracle_wms/wms_config.py` - Unified config management with Pydantic
- **Discovery**: `src/flext_oracle_wms/wms_discovery.py` - Automatic entity discovery and schema processing
- **Data Operations**: `src/flext_oracle_wms/wms_operations.py` - WMS data operations and utilities
- **Models**: `src/flext_oracle_wms/wms_models.py` - WMS-specific data models and value objects
- **Constants**: `src/flext_oracle_wms/wms_constants.py` - WMS enums and constants
- **Error Handling**: `src/flext_oracle_wms/wms_exceptions.py` - Comprehensive exception hierarchy

### Source Structure

```
src/flext_oracle_wms/
├── __init__.py           # Public API exports (comprehensive)
├── wms_client.py         # Main WMS client implementation
├── wms_api.py           # API catalog and mock server
├── authentication.py    # Authentication providers (legacy)
├── wms_config.py        # WMS-specific configuration with Pydantic
├── wms_discovery.py     # WMS entity discovery functionality
├── cache.py             # Caching implementation (legacy)
├── dynamic.py           # Dynamic schema processing (legacy)
├── filtering.py         # Record filtering utilities (legacy)
├── flattening.py        # Nested data flattening (legacy)
├── helpers.py           # Utility functions (legacy)
├── helpers_compat.py    # Compatibility helpers
├── wms_models.py        # WMS data models and value objects
├── typings.py           # Type definitions and aliases
├── wms_constants.py     # WMS enums and constants
├── wms_exceptions.py    # WMS exception hierarchy
├── wms_operations.py    # WMS data operations and utilities
├── legacy.py            # Legacy code compatibility
├── client.py            # Legacy client (deprecated)
├── config.py            # Legacy config (deprecated)
├── models.py            # Legacy models (deprecated)
├── constants.py         # Legacy constants (deprecated)
├── exceptions.py        # Legacy exceptions (deprecated)
├── discovery.py         # Legacy discovery (deprecated)
├── api_catalog.py       # Legacy API catalog (deprecated)
└── py.typed             # Type annotations marker
```

### Dependencies

**FLEXT Ecosystem Dependencies (Local Development):**
- `flext-core`: Base patterns, logging, result handling, dependency injection (path: ../flext-core)
- `flext-api`: API client patterns and enterprise authentication (path: ../flext-api)
- `flext-observability`: Monitoring and observability features (path: ../flext-observability)

**Core Dependencies:**
- `pydantic` (≥2.11.7): Data validation and settings management
- `httpx` (≥0.28.1): Async HTTP client for API communications
- `pydantic-settings` (≥2.10.1): Settings management
- `python-dotenv` (≥1.1.1): Environment variable loading

**Development Dependencies:**
- `ruff` (≥0.12.3): Linting and formatting
- `mypy` (≥1.13.0): Type checking
- `pytest` (≥8.4.0): Testing framework
- `bandit` (≥1.8.0): Security scanning
- `pre-commit` (≥4.0.1): Git hooks

## Development Commands

### Essential Quality Gates (Zero Tolerance)

```bash
make validate          # Complete validation: lint + type + security + test (90% coverage minimum)
make check            # Essential checks: lint + type + test (pre-commit standard)
make test             # Run tests with 90% coverage requirement
```

### Code Quality

```bash
make lint             # Ruff linting (comprehensive rule set)
make type-check       # MyPy strict mode type checking (zero errors tolerated)
make security         # Security scans: bandit + pip-audit
make format           # Format code with ruff
make fix              # Auto-fix all issues: format + imports + lint
```

### Testing Commands

```bash
# Core testing
make test             # Full test suite with coverage (90% minimum)
make test-unit        # Unit tests (pytest -m "not integration")
make test-integration # Integration tests (pytest -m integration)
make test-fast        # Run tests without coverage for quick feedback
make coverage-html    # Generate HTML coverage report

# Advanced testing patterns
pytest tests/test_client.py -v                    # Test specific file
pytest tests/test_client.py::TestClass::test_method -v -s  # Single test with output
pytest -k "authentication" -v                     # Tests matching pattern
pytest --lf                                       # Run only last failed tests
```

### Development Workflow Commands

```bash
# Environment setup
make setup            # Complete development setup (install + pre-commit)
make install          # Install dependencies with Poetry
make pre-commit       # Run pre-commit hooks on all files

# Build and package
make build            # Build package with Poetry
make build-clean      # Clean and build
make clean            # Clean build artifacts
make clean-all        # Deep clean including virtual environment

# WMS-specific operations
make wms-test         # Test WMS connectivity
make wms-schema       # Validate WMS schema
make wms-inventory    # Test inventory operations
make wms-shipping     # Test shipping operations
make oracle-connect   # Test Oracle connection
make oracle-schema    # Validate Oracle schema

# Docker operations (Maximum Container Usage)
make docker-build     # Build Docker images
make docker-up        # Start all Docker services
make docker-down      # Stop all Docker services
make docker-examples  # Run Oracle WMS examples in Docker
make docker-test      # Run complete test suite in Docker with real Oracle WMS
make docker-validate  # Complete Oracle WMS validation using Docker
make docker-full-validation  # Complete Docker validation workflow
./docker-run.sh examples     # Run examples in Docker
./docker-run.sh test         # Run tests in Docker
./docker-run.sh all          # Complete validation

# Diagnostics and maintenance
make diagnose         # Project diagnostics (Python, Poetry, dependencies)
make doctor           # Health check combining diagnose + check
make deps-show        # Show dependency tree
make deps-update      # Update dependencies
make deps-audit       # Security audit of dependencies
```

### Actual Test Structure

The test suite uses pytest with these actual markers:

```bash
# Available test markers (from pyproject.toml)
pytest -m unit              # Unit tests
pytest -m integration       # Integration tests
pytest -m slow              # Slow tests
pytest -m smoke             # Smoke tests
pytest -m e2e               # End-to-end tests
pytest -m declarative       # Declarative integration tests
pytest -m lgf_api           # LGF API specific tests
pytest -m automation        # Automation tests
pytest -m performance       # Performance tests

# WMS-specific test markers (from Makefile)
pytest -m wms               # WMS specific tests
pytest -m oracle            # Oracle database tests
pytest -m inventory         # Inventory management tests
pytest -m shipping          # Shipping operation tests
```

## Code Architecture

### Main Client Interface

The `FlextOracleWmsClient` in `src/flext_oracle_wms/wms_client.py` is the primary interface:

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# Create configuration
config = FlextOracleWmsClientConfig(
    base_url="https://your-wms-instance.oraclecloud.com",
    username="your_username",
    password="your_password"
)

# Initialize client
client = FlextOracleWmsClient(config)

# Discover entities (returns FlextResult from flext-core)
result = await client.discover_entities()
if result.success:
    entities = result.data
```

### Key Architecture Components

#### Configuration Management

- `FlextOracleWmsClientConfig`: Main client configuration using Pydantic
- `FlextOracleWmsModuleConfig`: Module-level configuration
- Environment variable support with `FLEXT_ORACLE_WMS_*` prefix
- Type-safe configuration validation

#### Authentication System

Multiple authentication methods in `src/flext_oracle_wms/wms_client.py`:

- `FlextOracleWmsAuthenticator`: Main authenticator interface
- `FlextOracleWmsAuthPlugin`: Pluggable authentication system
- Basic Authentication, Bearer Token, API Key support
- Factory functions for creating auth providers

#### API Catalog System

Declarative API definitions in `src/flext_oracle_wms/wms_api.py`:

- `FLEXT_ORACLE_WMS_APIS`: Centralized API endpoint catalog
- `FlextOracleWmsApiCategory`: Categorized endpoints
- `FlextOracleWmsApiEndpoint`: Individual endpoint definitions
- `OracleWmsMockServer`: Mock server for testing

#### Entity Discovery

`src/flext_oracle_wms/wms_discovery.py` provides:

- `FlextOracleWmsEntityDiscovery`: Automatic entity discovery
- `FlextOracleWmsDynamicSchemaProcessor`: Schema processing and validation
- `FlextOracleWmsCacheManager`: Enterprise caching
- Integration with flext-core patterns

#### Error Handling

Comprehensive exception hierarchy in `src/flext_oracle_wms/wms_exceptions.py`:

- `FlextOracleWmsError`: Base exception class
- `FlextOracleWmsConnectionError`: Connection-related errors
- `FlextOracleWmsAuthenticationError`: Authentication failures
- `FlextOracleWmsApiError`: API operation errors
- `FlextOracleWmsDataValidationError`: Data validation errors
- `FlextOracleWmsEntityNotFoundError`: Entity not found errors
- `FlextOracleWmsSchemaError`: Schema processing errors

## Testing Strategy

### Actual Test Structure

The test suite contains these key test files:

```
tests/
├── conftest.py                           # Shared test fixtures and configuration
├── test_authentication.py               # Authentication testing
├── test_authentication_coverage.py      # Extended authentication coverage
├── test_authentication_simple.py        # Simple authentication tests
├── test_client.py                       # Core client functionality
├── test_client_class.py                 # Client class testing
├── test_client_comprehensive.py         # Comprehensive client tests
├── test_client_main_coverage.py         # Main client coverage tests
├── test_client_simple.py               # Simple client tests
├── test_config_module.py                # Configuration module tests
├── test_exceptions.py                   # Exception handling tests
├── test_helpers.py                      # Helper function tests
├── test_helpers_coverage.py            # Extended helper coverage
├── test_helpers_real.py                # Real helper tests
├── test_integration_declarative.py     # Declarative integration tests
├── test_models.py                       # Data model validation
├── test_real_connection.py             # Real connection tests
├── test_schema_dynamic.py              # Dynamic schema tests
└── test_singer_flattening_comprehensive.py # Singer flattening tests
```

### Quality Requirements

- **90% minimum test coverage** (enforced by pytest with `--cov-fail-under=90`)
- **Strict MyPy configuration** (zero errors tolerated)
- **Comprehensive Ruff linting** (all rule categories enabled)
- **Security scanning** with bandit and pip-audit
- **Pre-commit hooks** for automated quality gates

## Development Workflow

### Before Making Changes

1. Run `make check` to ensure current state is clean
2. Create feature branch from main
3. Set up development environment: `make setup`

### During Development

1. Write tests first following TDD principles
2. Implement changes using established patterns from flext-core
3. Run `make validate` frequently during development
4. Use type hints throughout (required by strict MyPy)
5. Test with Docker: `make docker-test` for complete validation

### Before Committing

1. Run `make validate` to ensure all quality gates pass
2. Verify test coverage meets 90% requirement
3. Run `make docker-validate` for complete Docker validation
4. Pre-commit hooks will run automatically

## Docker Integration

### Maximum Container Usage

The project provides extensive Docker integration as requested:

```bash
# Complete Docker workflow
make docker-full-validation  # Build + validate + examples + tests

# Individual Docker operations
make docker-build           # Build all Docker images
make docker-up              # Start all services (PostgreSQL, Redis, etc.)
make docker-examples        # Run all examples in Docker
make docker-test            # Run complete test suite in Docker
make docker-validate        # Complete Oracle WMS validation

# Direct script usage
./docker-run.sh examples    # Run examples directly
./docker-run.sh test        # Run tests directly
./docker-run.sh all         # Complete validation workflow
./docker-run.sh clean       # Clean Docker resources
```

### Docker Environment

The Docker setup provides:

- Complete Oracle WMS testing environment
- Real Oracle database connectivity testing
- Isolated dependency management
- Reproducible validation results
- Full coverage reporting in Docker

## Legacy Code Handling

### File Organization

The codebase contains both current WMS-prefixed modules and legacy modules:

**Current Implementation (use these):**
- `wms_client.py` - Main client (replaces `client.py`)
- `wms_config.py` - Configuration (replaces `config.py`)
- `wms_models.py` - Data models (replaces `models.py`)
- `wms_exceptions.py` - Exceptions (replaces `exceptions.py`)
- `wms_constants.py` - Constants (replaces `constants.py`)

**Legacy Files (being phased out):**
- `client.py`, `config.py`, `models.py`, `exceptions.py`, `constants.py`
- `discovery.py`, `api_catalog.py` - Use WMS equivalents
- `legacy.py` - Compatibility layer
- `helpers_compat.py` - Compatibility helpers

**When Developing:**
1. Always use WMS-prefixed files for new features
2. Don't modify legacy files unless absolutely necessary
3. Migrate functionality from legacy to WMS modules when possible
4. Use compatibility layer (`legacy.py`) for backward compatibility

## Key Integration Patterns

### FlextResult Pattern Usage

All operations return `FlextResult` from flext-core for type-safe error handling:

```python
from flext_oracle_wms import FlextOracleWmsClient
from flext_core import FlextResult

# All client operations return FlextResult
result: FlextResult = await client.discover_entities()
if result.success:
    entities = result.data
    print(f"Found {len(entities)} entities")
else:
    logger.error(f"Discovery failed: {result.error}")
```

### FLEXT Ecosystem Integration

This library integrates with the broader FLEXT ecosystem:

- **flext-core**: FlextResult pattern, logging, dependency injection
- **flext-api**: Enterprise API client patterns and authentication
- **flext-observability**: Monitoring and metrics collection
- Standard FLEXT configuration and logging patterns

### Oracle WMS Integration Architecture

The library provides these integration layers:

1. **API Client Layer**: HTTP client with retry logic and connection pooling
2. **Authentication Layer**: Multiple auth methods (basic, bearer, API key)
3. **Discovery Layer**: Automatic entity and schema discovery
4. **Processing Layer**: Data transformation and flattening
5. **Caching Layer**: Enterprise caching for performance optimization

## Common Development Patterns

### Configuration with Environment Variables

```python
import os
from flext_oracle_wms import FlextOracleWmsClientConfig

# Configuration can be loaded from environment
config = FlextOracleWmsClientConfig(
    base_url=os.getenv("FLEXT_ORACLE_WMS_BASE_URL"),
    username=os.getenv("FLEXT_ORACLE_WMS_USERNAME"),
    password=os.getenv("FLEXT_ORACLE_WMS_PASSWORD"),
    timeout=int(os.getenv("FLEXT_ORACLE_WMS_TIMEOUT", "30"))
)
```

### Error Handling Patterns

```python
from flext_oracle_wms.exceptions import (
    FlextOracleWmsError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsAuthenticationError
)

try:
    result = await client.discover_entities()
    if result.is_failure:
        # Handle business logic errors via FlextResult
        logger.error(f"Discovery failed: {result.error}")
except FlextOracleWmsConnectionError:
    # Handle connection issues
    logger.error("Failed to connect to Oracle WMS")
except FlextOracleWmsAuthenticationError:
    # Handle authentication failures
    logger.error("Authentication failed")
```

## Architecture Gaps - High Priority Items

### 🚨 GAP 1: Oracle Database Integration Duplication

**Status**: HIGH - Pattern duplication with flext-db-oracle
**Problem**:

- WMS-specific Oracle patterns do not reuse flext-db-oracle
- Duplicated connection management code
- Oracle type handling not shared across ecosystem

**Required Actions**:

- [ ] Integrate with flext-db-oracle as base library
- [ ] Reuse Oracle connection patterns from flext-db-oracle
- [ ] Extend flext-db-oracle with WMS-specific optimizations
- [ ] Document Oracle WMS specialization strategy

### 🚨 GAP 2: Singer Integration Incomplete

**Status**: HIGH - WMS operations not exposed via Singer
**Problem**:

- Limited integration with flext-tap-oracle-wms and flext-target-oracle-wms
- WMS catalog not generated via Singer patterns
- Real-time inventory streaming not implemented

**Required Actions**:

- [ ] Complete integration with WMS Singer projects
- [ ] Implement WMS catalog generation
- [ ] Create real-time inventory Singer streams
- [ ] Document WMS Singer integration patterns

### 🚨 GAP 3: Business Logic vs Infrastructure Mix

**Status**: HIGH - WMS business logic mixed with infrastructure
**Problem**:

- Inventory management, shipping, picking are business domains
- API client patterns mixed with business rules
- Domain entities not clearly separated

**Required Actions**:

- [ ] Refactor to separate WMS domain logic from infrastructure
- [ ] Create WMS domain entities (Inventory, Shipment, Pick, etc.)
- [ ] Implement WMS business services using Clean Architecture
- [ ] Document WMS domain model

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
    if result.success:
        return result.data
    else:
        logger.error(f"Operation failed: {result.error}")
        return None
```

### Configuration Patterns

Follow flext-core configuration standards with environment variable support and type validation.
