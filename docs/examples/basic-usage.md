# Basic Usage Examples

**Working code examples for flext-oracle-wms**

**Version**: 0.9.0 | **Last Updated**: September 17, 2025 | **Status**: Framework examples with test configuration

---

## Client Initialization

### Test Configuration

Current implementation uses test configuration with fake URLs:

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

# Test configuration (uses fake URLs)
config = FlextOracleWmsModuleConfig.for_testing()
print(f"Test Base URL: {config.oracle_wms_base_url}")  # "https://test.example.com"

# Initialize client
client = FlextOracleWmsClient(config)
```

### Connection Testing

Testing client structure (expects network failures with test config):

```python
def test_client_structure():
    """Test client structure with fake URLs."""
    config = FlextOracleWmsModuleConfig.for_testing()

    with FlextOracleWmsClient(config) as client:
        try:
            # This will fail with test config but tests code structure
            connection_result = client.test_connection()
            print("Connection test completed (expected to fail with test config)")
        except Exception as e:
            print(f"Expected network error: {str(e)[:100]}...")
```

## Entity Discovery

Framework structure for entity discovery:

```python
import asyncio
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

async def test_entity_discovery():
    """Test entity discovery structure."""
    config = FlextOracleWmsModuleConfig.for_testing()

    with FlextOracleWmsClient(config) as client:
        try:
            # Test discovery structure (will fail with fake URLs)
            discovery_result = client.discover_entities()

            if discovery_result.success:
                entities = discovery_result.data
                print(f"Discovered {len(entities)} entities")

                # Show entity structure
                for entity in entities[:3]:  # First 3 entities
                    print(f"Entity: {getattr(entity, 'name', 'unknown')}")
            else:
                print(f"Discovery failed (expected with test config): {discovery_result.error}")

        except Exception as e:
            print(f"Expected error with test config: {str(e)[:100]}...")

# Run example
asyncio.run(test_entity_discovery())
```

## Error Handling

Using FlextResult patterns for error handling:

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig
from flext_core import FlextResult

def handle_results_safely():
    """Demonstrate safe result handling."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # All operations return FlextResult
    result = client.test_connection()

    if result.is_success:
        # Success case (unlikely with test config)
        data = result.value
        print(f"Connection successful: {data}")
    else:
        # Error case (expected with test config)
        error_message = result.error
        print(f"Connection failed: {error_message}")

        # Check error type
        if result.error and "not found" in result.error.lower():
            print("Likely DNS/network error with test URL")
        elif result.error and "timeout" in result.error.lower():
            print("Connection timeout with test server")
```

## Exception Handling

Working with Oracle WMS exception hierarchy:

```python
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsValidationError
)

def demonstrate_exception_handling():
    """Show exception handling patterns."""
    try:
        # Simulate various error conditions

        # Connection error with context
        connection_error = FlextOracleWmsConnectionError(
            "Connection failed",
            retry_count=3
        )
        print(f"Connection error retry count: {connection_error.retry_count}")

        # Authentication error with method context
        auth_error = FlextOracleWmsAuthenticationError(
            "Auth failed",
            auth_method="oauth2"
        )
        print(f"Auth method: {auth_error.auth_method}")

        # Validation error with field context
        validation_error = FlextOracleWmsValidationError(
            "Validation failed",
            field_name="username"
        )
        print(f"Field name: {validation_error.field_name}")

    except FlextOracleWmsError as e:
        print(f"Oracle WMS error: {e}")
```

## Configuration Examples

### Environment Variables

```python
import os
from flext_oracle_wms import FlextOracleWmsModuleConfig

# Set test environment variables
os.environ.update({
    "FLEXT_ORACLE_WMS_BASE_URL": "https://test.example.com",
    "FLEXT_ORACLE_WMS_USERNAME": "test_user",
    "FLEXT_ORACLE_WMS_PASSWORD": "test_password",
    "FLEXT_ORACLE_WMS_TIMEOUT": "30"
})

# Load configuration from environment
config = FlextOracleWmsModuleConfig.for_testing()
print(f"Loaded config: {config.oracle_wms_base_url}")
```

### Programmatic Configuration

```python
from flext_oracle_wms import FlextOracleWmsClientConfig

# Direct configuration (framework structure)
try:
    config = FlextOracleWmsClientConfig(
        base_url="https://test.example.com",
        username="test_user",
        password="test_password",
        timeout=30
    )
    print("Configuration created successfully")
except Exception as e:
    print(f"Configuration error: {e}")
```

## Data Processing Examples

### Entity Data Processing

```python
def process_entity_data():
    """Example of processing entity data."""
    config = FlextOracleWmsModuleConfig.for_testing()

    with FlextOracleWmsClient(config) as client:
        try:
            # Get entity data (will fail with test config)
            result = client.get_entity_data("inventory_item", limit=10)

            if result.is_success:
                records = result.value

                # Process records
                for record in records:
                    print(f"Processing record: {record}")

            else:
                print(f"Data retrieval failed (expected): {result.error}")

        except Exception as e:
            print(f"Expected error with test configuration: {e}")
```

## API Endpoint Examples

### Available Endpoints

Based on source code analysis (`wms_api.py`):

```python
from flext_oracle_wms.wms_api import FLEXT_ORACLE_WMS_APIS

# Show available API endpoints (22 total)
print("Available API endpoints:")
for endpoint_name, endpoint_path in FLEXT_ORACLE_WMS_APIS.items():
    print(f"  {endpoint_name}: {endpoint_path}")

# Example endpoints:
# - lgf_init_stage_interface: POST /init_stage_interface/{entity}/
# - run_stage_interface: POST /run_stage_interface/
# - entity_discovery: GET /entity/
# - lgf_entity_extract: GET /entity/{entity_name}/
```

## Implementation Status Examples

### What Works (Framework)

```python
# These patterns work with current framework:

# 1. Configuration loading
config = FlextOracleWmsModuleConfig.for_testing()  # ✅ Works

# 2. Client initialization
client = FlextOracleWmsClient(config)  # ✅ Works

# 3. FlextResult patterns
result = client.test_connection()  # ✅ Works (fails gracefully)

# 4. Exception handling
try:
    operation()
except FlextOracleWmsError as e:
    print(f"Error: {e}")  # ✅ Works
```

### What Needs Implementation

```python
# These require implementation work:

# 1. Real Oracle WMS connectivity
# Currently: Uses "https://test.example.com"
# Required: Actual Oracle WMS Cloud URLs

# 2. Modern API endpoints (LGF v10)
# Currently: 22 legacy endpoints
# Required: pick_confirm, bulk_update_inventory_attributes, etc.

# 3. OAuth2 authentication
# Currently: Basic auth framework only
# Required: Token-based authentication

# 4. FLEXT compliance
# Currently: Uses httpx directly
# Required: flext-api integration
```

---

**Last Updated**: September 17, 2025 | **Status**: Framework examples requiring Oracle WMS Cloud implementation