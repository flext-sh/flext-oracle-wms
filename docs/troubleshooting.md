# Troubleshooting Guide

**Common issues and solutions for flext-oracle-wms**

**Version**: 0.9.9 RC | **Last Updated**: September 17, 2025 | **Status**: Framework troubleshooting · 1.0.0 Release Preparation

---

## Common Issues

### Connection Issues

#### "Connection failed with test config"

**Symptom**: Connection tests fail with network errors

```python
# Expected behavior with current implementation
config = FlextOracleWmsModuleConfig.for_testing()
client = FlextOracleWmsClient(config)
result = client.test_connection()  # Expected to fail
```

**Cause**: Tests use fake URL `"https://test.example.com"`

**Solution**: This is expected behavior. For real Oracle WMS connectivity:

1. Obtain actual Oracle WMS Cloud instance URL
2. Configure proper authentication credentials
3. Implement real Oracle WMS integration (currently not available)

#### "Import errors from flext_core"

**Symptom**: Cannot import flext_core components

```python
from flext_core import get_logger  # ImportError
```

**Cause**: `get_logger` doesn't exist in flext_core

**Solution**: Use correct flext_core imports:

```python
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
from flext_core import
logger = FlextLogger(__name__)
```

### Type Safety Issues

#### MyPy errors with dynamic attributes

**Symptom**: MyPy reports missing attributes on exception classes

```python
error = FlextOracleWmsError("message", field="username")
assert error.field == "username"  # MyPy error: attribute not found
```

**Solution**: Exception classes now declare attributes explicitly:

```python
# Exception classes have been updated with proper type annotations
error = FlextOracleWmsError("message", field="username")
assert error.field == "username"  # Now works with MyPy
```

#### Configuration type mismatches

**Symptom**: Type errors with configuration objects

**Solution**: Use proper configuration types:

```python
from flext_oracle_wms import FlextOracleWmsModuleConfig, FlextOracleWmsApiVersion

config = FlextOracleWmsModuleConfig(
    api_version=FlextOracleWmsApiVersion.V1,  # Use enum, not string
    oracle_wms_timeout=30,                    # Use int, not float
)
```

### FLEXT Compliance Issues

#### httpx usage violations

**Symptom**: Code uses httpx directly instead of flext-api

```python
import httpx  # FLEXT compliance violation
```

**Solution**: This requires implementation work:

1. Replace httpx imports with flext-api
2. Migrate HTTP client patterns
3. Update authentication mechanisms

**Current Status**: Known violation requiring architectural changes

#### Multiple classes per module

**Symptom**: Modules contain multiple classes (71 total)

**Solution**: This requires architectural refactoring:

1. Consolidate to single unified class per module
2. Convert standalone classes to nested helpers
3. Follow FLEXT domain service patterns

**Current Status**: Known violation requiring significant refactoring

### Testing Issues

#### Tests expecting failures

**Symptom**: Tests are designed to expect network failures

```python
def test_real_connection():
    # This test expects to fail with test config
    try:
        result = client.test_connection()
    except Exception:
        pass  # Expected with fake URLs
```

**Solution**: This is expected behavior with current test configuration

#### Invalid type arguments in tests

**Symptom**: Tests intentionally pass wrong types to test validation

```python
filter_engine.filter_records("not_a_list", {})  # Intentionally wrong type
```

**Solution**: These are negative tests. Use `# type: ignore` if needed for intentional type violations in tests

### Development Environment Issues

#### Poetry installation problems

**Symptom**: Poetry install fails or dependencies conflict

**Solution**:

```bash
# Clean installation
rm -rf .venv poetry.lock
poetry install
```

#### PYTHONPATH issues

**Symptom**: Cannot import project modules

**Solution**: Set correct PYTHONPATH:

```bash
export PYTHONPATH=src
# Or use make commands which set this automatically
make test
```

### Oracle WMS Specific Issues

#### Missing modern API endpoints

**Symptom**: Cannot access LGF v10 APIs

**Current Status**: Known limitation

- Only 22 legacy API endpoints implemented
- Missing modern LGF v10 APIs like `pick_confirm`, `bulk_update_inventory_attributes`
- Requires implementation work

#### Authentication limitations

**Symptom**: Cannot authenticate with real Oracle WMS Cloud

**Current Status**: Known limitation

- Only test authentication implemented
- No OAuth2 implementation
- No real Oracle WMS Cloud connectivity

### Performance Issues

#### Slow test execution

**Solution**: Use faster test commands:

```bash
pytest -x --tb=short  # Stop on first failure, short traceback
pytest --maxfail=1    # Stop after one failure
```

#### Memory usage during development

**Solution**: Use efficient development practices:

```bash
# Use make commands which are optimized
make test
make validate
```

## Error Messages Reference

### Common Error Patterns

#### "ValidationError in configuration"

```python
# Pydantic validation error
ValidationError: field required (type=value_error.missing)
```

**Solution**: Ensure all required configuration fields are provided

#### "FlextOracleWmsConnectionError with retry_count"

```python
error = FlextOracleWmsConnectionError("failed", retry_count=3)
assert error.retry_count == 3  # Now works after exception class updates
```

#### "Entity not found" errors

```python
error = FlextOracleWmsEntityNotFoundError("Entity missing", entity_name="test")
assert error.entity_name == "test"  # Properly handled
```

## Debugging Tips

### Enable Debug Logging

```python
logging.basicConfig(level=logging.DEBUG)

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
logger = FlextLogger(__name__)
logger.debug("Debug message")
```

### Type Checking

```bash
# Comprehensive type checking
mypy src/
pyright

# Check specific file
mypy src/flext_oracle_wms/wms_client.py
```

### Test Debugging

```bash
# Run specific test with verbose output
pytest tests/test_client.py::test_specific_function -v

# Debug test with pdb
pytest --pdb tests/test_client.py
```

## Getting Help

### Documentation Resources

- **[Getting Started](getting-started.md)** - Installation and setup
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Configuration](configuration.md)** - Settings and environment
- **[Development](development.md)** - Development guidelines

### Known Limitations

This is a framework requiring implementation:

1. **No real Oracle WMS connectivity** - Tests use fake URLs
2. **Missing modern APIs** - LGF v10 endpoints not implemented
3. **FLEXT compliance gaps** - httpx usage, class architecture violations
4. **Limited authentication** - No OAuth2 implementation

### Reporting Issues

When reporting issues, include:

1. **Error message** - Full error text
2. **Environment** - Python version, OS
3. **Configuration** - Sanitized configuration (no passwords)
4. **Steps to reproduce** - Minimal example
5. **Expected vs actual behavior**

---

**Last Updated**: September 17, 2025 | **Status**: Framework troubleshooting guide · 1.0.0 Release Preparation
