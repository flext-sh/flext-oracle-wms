# Development Guide

**Development workflow and guidelines for flext-oracle-wms**

**Version**: 0.9.9 RC | **Last Updated**: September 17, 2025 | **Status**: Framework requiring implementation · 1.0.0 Release Preparation

---

## Development Setup

### Prerequisites

- **Python 3.13+** - Required for modern patterns and type safety
- **Poetry** - Dependency management
- **Oracle WMS Cloud access** - For real integration testing (not currently available)

### Installation

```bash
# Clone and setup
git clone <flext-oracle-wms-repo>
cd flext-oracle-wms
poetry install

# Verify installation
make validate  # Run all quality gates
```

## Development Commands

### Quality Gates

```bash
# Complete validation pipeline
make validate              # Lint + type + security + test

# Individual checks
make lint                  # Ruff linting
make type-check           # MyPy strict mode type checking
make security             # Bandit + pip-audit security scan
make test                 # Test suite execution
make format               # Code formatting
```

### Testing

```bash
# Run test suite
make test                 # All tests
pytest tests/             # Direct pytest execution

# Test with coverage
pytest --cov=src --cov-report=term-missing
```

### Type Safety

```bash
# MyPy strict mode (zero tolerance)
make type-check
mypy src/                 # Direct mypy execution

# PyRight for additional validation
pyright
```

## Code Standards

### FLEXT Compliance Requirements

Current compliance gaps requiring implementation:

#### 1. HTTP Client Compliance (Critical)

```python
# Current: Non-compliant httpx usage
import httpx  # ❌ VIOLATION
client = httpx.Client()

# Required: flext-api integration
from flext_api import FlextApiClient  # ✅ REQUIRED
client = FlextApiClient()
```

#### 2. Class Architecture Compliance (Critical)

```python
# Current: Multiple classes per module (71 classes total)
class WmsClient: pass
class WmsHelper: pass     # ❌ VIOLATION

# Required: Single unified class per module
class FlextOracleWmsClient(FlextService):
    class _ClientHelper:  # ✅ NESTED HELPER
        pass
```

#### 3. Authentication Integration (High Priority)

```python
# Current: Custom authentication
class CustomAuth: pass   # ❌ VIOLATION

# Required: flext-auth integration
from flext_auth import FlextAuthenticator  # ✅ REQUIRED
```

### Error Handling Standards

All operations must use FlextResult pattern:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities

def operation() -> FlextResult[ReturnType]:
    try:
        # Operation logic
        return FlextResult.ok(result)
    except Exception as e:
        return FlextResult.fail(f"Operation failed: {e}")
```

### Type Safety Requirements

- **100% MyPy compliance** - Zero type errors tolerated
- **Pydantic models** - All data structures validated
- **No `object` types** - Explicit typing required
- **No `type: ignore`** - Fix types at source

## Testing Strategy

### Current Test Structure

```
tests/
├── test_client.py         # Client functionality tests
├── test_config.py         # Configuration tests
├── test_discovery.py      # Entity discovery tests
├── test_exceptions.py     # Exception handling tests
├── test_filtering.py      # Data filtering tests
└── ...                    # Additional test modules
```

### Test Requirements

- **90%+ coverage** - Minimum coverage target
- **Real integration preferred** - Minimize mocking
- **FlextResult validation** - Test error handling
- **Type safety testing** - Validate type annotations

### Current Test Limitations

Tests currently use fake URLs and expect failures:

```python
def test_real_connection():
    config = FlextOracleWmsModuleConfig.for_testing()  # Uses test.example.com
    # Connection tests expect network failures with test config
```

## Implementation Priorities

### Phase 1: FLEXT Compliance (Weeks 1-2)

1. **Replace httpx with flext-api patterns**
   - Migrate `http_client.py` and `wms_discovery.py`
   - Update all HTTP client usage

2. **Consolidate class architecture**
   - Reduce from 71 classes to unified classes per module
   - Implement nested helper pattern

3. **Integrate flext-auth**
   - Replace custom authentication classes
   - Add OAuth2 support for Oracle WMS Cloud

### Phase 2: Oracle WMS Integration (Weeks 3-4)

1. **Add missing LGF v10 APIs**
   - Implement modern pick_confirm API
   - Add bulk_update_inventory_attributes endpoint
   - Add object store data extraction capabilities

2. **Establish real connectivity**
   - Replace fake test URLs with actual Oracle WMS Cloud testing
   - Implement proper authentication testing
   - Validate against real Oracle WMS instances

### Phase 3: Enhanced Features (Weeks 5-6)

1. **Complete Singer protocol implementation**
   - Enhanced tap/target functionality
   - Real-time streaming capabilities

2. **Performance optimization**
   - Connection pooling
   - Intelligent caching strategies

## Code Review Guidelines

### Pre-commit Requirements

```bash
# Required before committing
make validate              # All quality gates must pass
make test                  # All tests must pass
```

### Review Checklist

- [ ] **FLEXT compliance** - No httpx usage, unified classes
- [ ] **Type safety** - Zero MyPy errors
- [ ] **Error handling** - FlextResult patterns used
- [ ] **Test coverage** - New code has tests
- [ ] **Documentation** - API changes documented

## Development Environment

### IDE Configuration

Recommended VS Code settings:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black"
}
```

### Environment Variables

```bash
# Development environment
export FLEXT_DEBUG_MODE="true"
export FLEXT_LOG_LEVEL="debug"
export PYTHONPATH="src"
```

## Troubleshooting

### Common Issues

1. **Import errors** - Ensure `PYTHONPATH=src` is set
2. **Type errors** - Run `mypy src/` for detailed error messages
3. **Test failures** - Check if using correct test configuration
4. **FLEXT compliance** - Review class architecture and HTTP client usage

### Development Tools

```bash
# Debug tools
python -m pdb script.py    # Python debugger
python -v script.py        # Verbose imports
```

---

**Last Updated**: September 17, 2025 | **Status**: Framework requiring FLEXT compliance and Oracle WMS implementation · 1.0.0 Release Preparation
