# FLEXT Oracle WMS - Test Suite

This directory contains the comprehensive test suite for the **flext-oracle-wms** library, ensuring enterprise-grade quality and reliability for Oracle Warehouse Management System (WMS) Cloud integration.

## 📁 Test Structure

### 🎯 **Core Component Tests**

- **[test_client.py](test_client.py)** - Primary FlextOracleWmsClient functionality testing
- **[test_client_class.py](test_client_class.py)** - Client class-specific behavior and state management
- **[test_client_comprehensive.py](test_client_comprehensive.py)** - Comprehensive client integration scenarios
- **[test_client_main_coverage.py](test_client_main_coverage.py)** - Coverage-focused client testing
- **[test_client_simple.py](test_client_simple.py)** - Basic client functionality verification

### 🔧 **Configuration & Setup Tests**

- **[test_config_module.py](test_config_module.py)** - Configuration management and validation testing
- **[test_authentication.py](test_authentication.py)** - Multi-method authentication pattern testing
- **[test_authentication_coverage.py](test_authentication_coverage.py)** - Authentication coverage verification
- **[test_authentication_simple.py](test_authentication_simple.py)** - Basic authentication functionality

### 🏗️ **Infrastructure Tests**

- **[test_exceptions.py](test_exceptions.py)** - Exception hierarchy and error handling testing
- **[test_models.py](test_models.py)** - Data model validation and domain rule testing
- **[test_helpers.py](test_helpers.py)** - Utility function and helper method testing
- **[test_helpers_coverage.py](test_helpers_coverage.py)** - Helper function coverage verification
- **[test_helpers_real.py](test_helpers_real.py)** - Real-world helper function scenarios

### 🧪 **Integration & Advanced Tests**

- **[test_integration_declarative.py](test_integration_declarative.py)** - Declarative API integration testing
- **[test_real_connection.py](test_real_connection.py)** - Real Oracle WMS connection testing
- **[test_schema_dynamic.py](test_schema_dynamic.py)** - Dynamic schema discovery and processing
- **[test_singer_flattening_comprehensive.py](test_singer_flattening_comprehensive.py)** - Singer protocol compatibility testing

### ⚙️ **Test Configuration**

- **[conftest.py](conftest.py)** - Shared test fixtures, configuration, and utilities
- **[**init**.py](**init**.py)** - Test package initialization

## 🎯 **Test Categories & Markers**

### Test Markers

The test suite uses pytest markers for comprehensive test categorization:

```python
# Unit tests for individual components
pytest -m unit

# Integration tests with external systems
pytest -m integration

# Declarative integration tests
pytest -m declarative

# LGF API specific tests
pytest -m lgf_api

# Authentication pattern tests
pytest -m authentication

# Performance benchmarking tests
pytest -m performance

# Tests requiring real Oracle WMS credentials
pytest -m real_connection

# Coverage-focused tests
pytest -m coverage

# Slow tests (for CI optimization)
pytest -m slow
```

### Test Types

#### **Unit Tests**

- Individual component testing with mock dependencies
- Fast execution (< 1 second per test)
- No external dependencies or network calls
- High code coverage focus

#### **Integration Tests**

- Component interaction testing
- Mock Oracle WMS server integration
- FLEXT ecosystem integration verification
- Medium execution time (1-5 seconds per test)

#### **End-to-End Tests**

- Full workflow testing with realistic scenarios
- Real Oracle WMS Cloud API testing (when credentials available)
- Complete data pipeline verification
- Longer execution time (5-30 seconds per test)

## 🚀 **Running Tests**

### Basic Test Execution

```bash
# Run all tests with coverage
make test

# Run specific test categories
pytest -m unit -v                    # Unit tests only
pytest -m integration -v             # Integration tests only
pytest -m declarative -v             # Declarative integration tests
pytest -m authentication -v          # Authentication tests
pytest -m performance -v             # Performance benchmarks

# Run specific test files
pytest tests/test_client.py -v
pytest tests/test_authentication.py -v
pytest tests/test_integration_declarative.py -v
```

### Advanced Test Execution

```bash
# Run tests with specific coverage
pytest --cov=src/flext_oracle_wms --cov-report=html

# Run tests excluding slow tests
pytest -m "not slow" -v

# Run tests with detailed output
pytest -v -s --tb=short

# Run tests with specific environment
ORACLE_WMS_ENVIRONMENT=test pytest -v

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Quality Gate Testing

```bash
# Complete validation (includes tests)
make validate

# Test-specific quality gates
make test-unit              # Unit tests with coverage
make test-integration       # Integration tests
make test-performance       # Performance benchmarks
make coverage-html          # Generate HTML coverage report
```

## 🔧 **Test Configuration**

### Environment Variables

Tests support configuration via environment variables:

```bash
# Oracle WMS connection (for real connection tests)
export ORACLE_WMS_BASE_URL="https://test-wms.oraclecloud.com"
export ORACLE_WMS_USERNAME="test_user"
export ORACLE_WMS_PASSWORD="test_password"
export ORACLE_WMS_ENVIRONMENT="test"

# Test behavior configuration
export ORACLE_WMS_TEST_MODE="mock"          # mock or real
export ORACLE_WMS_TEST_TIMEOUT="30"         # Test timeout seconds
export ORACLE_WMS_LOG_LEVEL="debug"         # Logging level for tests
export ORACLE_WMS_ENABLE_SLOW_TESTS="false" # Enable/disable slow tests
```

### Test Data Management

```bash
# Test data configuration
export ORACLE_WMS_TEST_DATA_DIR="tests/data"
export ORACLE_WMS_MOCK_DATA_DIR="tests/mock_data"
export ORACLE_WMS_FIXTURES_DIR="tests/fixtures"
```

## 📊 **Coverage Requirements**

### Coverage Targets

- **Overall Coverage**: 90% minimum (enforced by CI)
- **Unit Test Coverage**: 95% minimum for core modules
- **Integration Coverage**: 80% minimum for integration scenarios
- **Branch Coverage**: 85% minimum for critical paths

### Coverage Reporting

```bash
# Generate detailed coverage report
make coverage

# Generate HTML coverage report
make coverage-html

# View coverage summary
pytest --cov=src/flext_oracle_wms --cov-report=term-missing

# Generate XML coverage for CI
pytest --cov=src/flext_oracle_wms --cov-report=xml
```

## 🧪 **Test Development Guidelines**

### Test Structure Standards

```python
"""Test module following enterprise standards."""

import pytest
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

class TestComponentName:
    """Test class for ComponentName with comprehensive scenarios."""

    def test_basic_functionality(self):
        """Test basic functionality with clear assertions."""
        # Arrange
        config = FlextOracleWmsClientConfig(...)

        # Act
        result = component.operation()

        # Assert
        assert result.success
        assert result.data is not None

    def test_error_scenarios(self):
        """Test error handling with comprehensive coverage."""
        # Test implementation
        pass

    @pytest.mark.integration
    def test_integration_scenario(self):
        """Test integration scenarios with external dependencies."""
        # Test implementation
        pass
```

### Test Quality Standards

- **Clear Test Names**: Descriptive test method names explaining what is being tested
- **AAA Pattern**: Arrange, Act, Assert structure for test clarity
- **Comprehensive Assertions**: Multiple assertions to verify complete behavior
- **Error Scenario Coverage**: Test both success and failure paths
- **Mock Usage**: Appropriate use of mocks for external dependencies
- **Test Data Management**: Proper test data setup and cleanup

### Performance Testing

```python
@pytest.mark.performance
def test_performance_benchmark():
    """Performance benchmark with timing assertions."""
    import time

    start_time = time.time()
    result = perform_operation()
    execution_time = time.time() - start_time

    assert result.success
    assert execution_time < 2.0  # Performance requirement
```

## 🔗 **Test Dependencies**

### Testing Framework

- **pytest v7.4.0+** - Primary testing framework with advanced features
- **pytest-cov v4.1.0+** - Coverage reporting and analysis
- **pytest-asyncio v0.21.0+** - Async test support for client operations
- **pytest-mock v3.11.0+** - Mock object support for unit testing

### Additional Testing Tools

- **factory-boy v3.3.0+** - Test data factory patterns
- **faker v19.0.0+** - Realistic test data generation
- **responses v0.23.0+** - HTTP request mocking for API tests
- **freezegun v1.2.0+** - Time-based testing utilities

### Development Dependencies

- **black v23.7.0+** - Code formatting for test files
- **ruff v0.0.280+** - Linting for test code quality
- **mypy v1.5.0+** - Type checking for test code

## 📚 **Test Documentation**

### Test Case Documentation

Each test file includes comprehensive docstrings explaining:

- **Purpose**: What functionality is being tested
- **Scope**: Which components and scenarios are covered
- **Requirements**: object special setup or dependencies needed
- **Expected Behavior**: What constitutes success for each test

### Integration Test Requirements

- **Oracle WMS Access**: Valid Oracle WMS Cloud instance for integration tests
- **Network Connectivity**: Stable internet connection for API testing
- **Authentication**: Valid credentials for real connection tests
- **Test Environment**: Isolated test environment to prevent data corruption

## 🚨 **Troubleshooting Tests**

### Common Test Issues

```bash
# Test environment issues
pytest --collect-only              # Verify test discovery
pytest --markers                   # List available markers
pytest --fixtures                  # List available fixtures

# Coverage issues
pytest --cov-report=term-missing   # Show missing coverage lines
pytest --cov-fail-under=90         # Fail if coverage below threshold

# Performance issues
pytest --benchmark-only            # Run only performance tests
pytest --benchmark-sort=mean       # Sort performance results
```

### Debugging Failed Tests

```bash
# Verbose output with debugging
pytest -v -s --tb=long

# Stop on first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run tests with pdb debugger
pytest --pdb
```

---

**Test Suite Status**: Production Ready  
**Coverage**: 90%+ (Enforced)  
**Test Count**: 150+ comprehensive tests  
**Test Categories**: Unit, Integration, E2E, Performance  
**CI Integration**: Complete with quality gates  
**Last Updated**: January 4, 2025
