# API Reference

**Complete API documentation for flext-oracle-wms**

**Version**: 0.9.9 RC | **Last Updated**: September 17, 2025 | **Status**: Framework with implementation gaps · 1.0.0 Release Preparation

---

## Client API

### FlextOracleWmsClient

Main client interface for Oracle WMS integration.

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

# Initialize client
config = FlextOracleWmsModuleConfig.for_testing()
client = FlextOracleWmsClient(config)
```

#### Methods

##### `test_connection() -> FlextResult[bool]`

Tests connection to Oracle WMS (currently uses fake URLs).

```python
result = client.test_connection()
if result.is_success:
    print("Connection structure verified")
else:
    print(f"Connection failed: {result.error}")
```

##### `discover_entities() -> FlextResult[List[Dict]]`

Discovers available Oracle WMS entities.

```python
result = client.discover_entities()
if result.is_success:
    entities = result.value
    print(f"Found {len(entities)} entities")
```

## Configuration API

### FlextOracleWmsModuleConfig

Configuration class for Oracle WMS connection settings.

#### Class Methods

##### `for_testing() -> FlextOracleWmsModuleConfig`

Returns test configuration with fake URLs.

```python
config = FlextOracleWmsModuleConfig.for_testing()
# Uses "https://test.example.com" as base URL
```

## API Endpoints (Framework)

### Implemented Endpoints (22 total)

Based on source code analysis of `wms_api.py`:

#### Setup & Transactional Operations

- `lgf_init_stage_interface` - Initialize staging interface
- `run_stage_interface` - Execute staging operations
- `update_output_interface` - Update output interface

#### Automation & Warehouse Operations

- `update_oblpn_tracking_number` - Update tracking numbers
- `update_oblpn_dimensions` - Update package dimensions

#### Data Extract & Discovery

- `lgf_entity_extract` - Extract entity data
- `legacy_entity_extract` - Legacy data extraction
- `entity_discovery` - Entity discovery operations
- `entity_metadata` - Entity metadata retrieval

### Missing Modern APIs (LGF v10)

Based on Oracle WMS best practices research:

- `POST /lgfapi/v10/pick_confirm/` - Enhanced pick confirmation
- `POST /lgfapi/v10/entity/inventory/bulk_update_inventory_attributes/` - Bulk operations
- `POST /lgfapi/v10/data_extract/export_status` - Object store integration

## Error Handling

### Exception Hierarchy

```python
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsError,              # Base exception
    FlextOracleWmsConnectionError,    # Connection issues
    FlextOracleWmsAuthenticationError, # Auth failures
    FlextOracleWmsValidationError,    # Validation errors
    FlextOracleWmsApiError,           # API errors
    FlextOracleWmsEntityNotFoundError # Entity not found
)
```

### FlextResult Pattern

All operations return `FlextResult[T]` for type-safe error handling:

```python
result = client.some_operation()
if result.is_success:
    data = result.value  # Type-safe access
else:
    error = result.error  # Error message
```

## Models

### FlextOracleWmsEntity

Represents Oracle WMS entity with metadata.

```python
from flext_oracle_wms.wms_models import FlextOracleWmsEntity

entity = FlextOracleWmsEntity(
    name="inventory_item",
    description="Inventory item entity",
    # Additional metadata
)
```

## Implementation Status

### Completed Components

- ✅ **Client interface** - Basic structure implemented
- ✅ **Configuration** - Test configuration available
- ✅ **Error handling** - FlextResult patterns throughout
- ✅ **Type safety** - MyPy strict compliance

### Implementation Gaps

- ❌ **Real connectivity** - No proven Oracle WMS Cloud integration
- ❌ **Modern APIs** - Missing LGF v10 endpoints
- ❌ **Authentication** - Limited to test scenarios
- ❌ **FLEXT compliance** - Uses httpx instead of flext-api

---

**Last Updated**: September 17, 2025 | **Status**: Framework requiring Oracle WMS Cloud integration implementation · 1.0.0 Release Preparation
