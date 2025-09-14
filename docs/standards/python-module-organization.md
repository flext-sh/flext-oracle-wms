# Python Module Organization Standards

**Version 0.9.0 | September 17, 2025 | Status: Framework requiring implementation**

## Current Module Structure

Based on actual source code analysis:

```
src/flext_oracle_wms/
├── __init__.py            # 249 exported items
├── wms_client.py          # Main Oracle WMS client implementation
├── wms_discovery.py       # Entity discovery functionality
├── wms_api.py             # API endpoint definitions (22 endpoints)
├── wms_config.py          # Configuration classes
├── wms_constants.py       # Constants and enums
├── http_client.py         # HTTP client wrapper (uses httpx)
├── authentication.py      # Authentication support
├── wms_operations.py      # Operations utilities
├── wms_models.py          # Pydantic models
├── wms_exceptions.py      # Exception hierarchy
└── [additional modules]   # Various utility modules
```

## Implementation Status

### Current Structure Issues
- **71 classes across modules** - violates FLEXT unified class pattern
- **httpx direct usage** - non-compliant with flext-api requirements
- **No flext-auth integration** - custom authentication implementation
- **Mixed architectural concerns** - infrastructure mixed with domain logic

### Required FLEXT Compliance Changes

#### 1. Unified Class Architecture
Each module should contain single unified class with nested helpers:

```python
class FlextOracleWmsConstants(FlextDomainService):
    """Unified constants class with nested specializations."""

    class _AuthMethods:
        BASIC = "basic"
        OAUTH2 = "oauth2"
        API_KEY = "api_key"

    class _ApiVersions:
        LGF_V10 = "v10"
        LEGACY = "legacy"
```

#### 2. HTTP Client Compliance
Replace httpx usage with flext-api patterns:

```python
# Current (non-compliant):
import httpx
client = httpx.AsyncClient()

# Required (FLEXT-compliant):
from flext_api import FlextApiClient
client = FlextApiClient()
```

#### 3. Authentication Integration
Integrate with flext-auth instead of custom authentication:

```python
from flext_auth import FlextAuthenticator
class FlextOracleWmsAuthenticator(FlextAuthenticator):
    # Use ecosystem authentication patterns
```

## Module Organization Standards

### Public API Naming
All public exports use `FlextOracleWms` prefix:
- `FlextOracleWmsClient` - Main client interface
- `FlextOracleWmsConfig` - Configuration class
- `FlextOracleWmsEntity` - Domain entities

### Import Patterns
Recommended user import pattern:
```python
from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsConfig
)
```

### Internal Organization
- Use underscore prefix for internal implementations
- Implement nested helper classes instead of multiple classes per module
- Follow FlextResult patterns for all operations

---

**Last Updated**: September 17, 2025 | **Status**: Framework requiring FLEXT compliance implementation