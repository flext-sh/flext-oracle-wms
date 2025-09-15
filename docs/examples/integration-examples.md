# Integration Examples

**FLEXT ecosystem integration examples for flext-oracle-wms**

**Version**: 0.9.0 | **Last Updated**: September 17, 2025 | **Status**: Framework integration patterns

---

## FLEXT Ecosystem Integration

### flext-core Integration

Current integration with flext-core patterns:

```python
from flext_core import FlextResult, FlextLogger
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

class OracleWmsService:
    """Example service using flext-core patterns."""

    def __init__(self):
        self.logger = FlextLogger(__name__)
        self.config = FlextOracleWmsModuleConfig.for_testing()
        self.client = FlextOracleWmsClient(self.config)

    async def get_entities_safely(self) -> FlextResult[list]:
        """Get entities using FlextResult pattern."""
        try:
            self.logger.info("Starting entity discovery")

            # All Oracle WMS operations return FlextResult
            result = self.client.discover_entities()

            if result.is_success:
                self.logger.info(f"Discovered {len(result.value)} entities")
                return result
            else:
                self.logger.error(f"Discovery failed: {result.error}")
                return result

        except Exception as e:
            self.logger.exception("Unexpected error in entity discovery")
            return FlextResult.fail(f"Service error: {e}")
```

### Required flext-api Integration

Current gap that requires implementation:

```python
# Current: Non-compliant httpx usage (FLEXT violation)
import httpx  # ❌ VIOLATION
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# Required: flext-api integration (not implemented)
from flext_api import FlextApiClient  # ✅ REQUIRED
client = FlextApiClient()
result = await client.get(url)
```

### Required flext-auth Integration

Authentication integration pattern that needs implementation:

```python
# Current: Custom authentication (FLEXT violation)
class CustomOracleAuth:  # ❌ VIOLATION
    pass

# Required: flext-auth integration (not implemented)
from flext_auth import FlextAuthenticator, FlextOAuth2Provider

class OracleWmsAuthenticator(FlextAuthenticator):
    """FLEXT-compliant Oracle WMS authentication."""

    def __init__(self):
        self.oauth2_provider = FlextOAuth2Provider(
            client_id="oracle_wms_client",
            token_url="https://oracle-wms.oraclecloud.com/oauth2/token"
        )

    async def authenticate(self) -> FlextResult[str]:
        """Authenticate with Oracle WMS using flext-auth."""
        return await self.oauth2_provider.get_access_token()
```

## Singer Protocol Integration

### Oracle WMS Tap Integration

Framework for Singer tap integration:

```python
import singer
from typing import Dict, Any, Iterator
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

class OracleWmsTap:
    """Singer tap for Oracle WMS data extraction."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.wms_config = FlextOracleWmsModuleConfig(**config)
        self.client = FlextOracleWmsClient(self.wms_config)

    def discover_catalog(self) -> Dict[str, Any]:
        """Discover Oracle WMS streams for Singer."""
        # This would use real Oracle WMS discovery
        result = self.client.discover_entities()

        if result.is_success:
            entities = result.value

            streams = []
            for entity in entities:
                stream = {
                    "tap_stream_id": entity.get("name"),
                    "schema": self._get_entity_schema(entity),
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {
                                "inclusion": "available",
                                "selected": False
                            }
                        }
                    ]
                }
                streams.append(stream)

            return {"streams": streams}
        else:
            # Handle discovery failure
            singer.write_message(
                singer.StateMessage(value={"error": result.error})
            )
            return {"streams": []}

    def _get_entity_schema(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Get JSON schema for Oracle WMS entity."""
        # Framework structure - would need Oracle WMS schema discovery
        return {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                # Additional properties based on Oracle WMS entity
            }
        }

    def sync_stream(self, stream_name: str) -> Iterator[Dict[str, Any]]:
        """Sync Oracle WMS stream data."""
        # Framework for data extraction
        result = self.client.get_entity_data(stream_name)

        if result.is_success:
            for record in result.value:
                yield {
                    "type": "RECORD",
                    "stream": stream_name,
                    "record": record
                }
        else:
            singer.write_message(
                singer.StateMessage(value={"error": result.error})
            )

# Example Singer tap usage:
def main():
    """Singer tap main function."""
    config = {
        "oracle_wms_base_url": "https://test.example.com",
        "oracle_wms_username": "test_user",
        "oracle_wms_password": "test_password"
    }

    tap = OracleWmsTap(config)

    # Discovery mode
    catalog = tap.discover_catalog()
    singer.write_message(singer.CatalogMessage(catalog=catalog))
```

### Oracle WMS Target Integration

Framework for Singer target integration:

```python
import singer
from typing import Dict, Any
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

class OracleWmsTarget:
    """Singer target for Oracle WMS data loading."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.wms_config = FlextOracleWmsModuleConfig(**config)
        self.client = FlextOracleWmsClient(self.wms_config)
        self.buffer = {}

    def process_record(self, record_message: singer.RecordMessage) -> None:
        """Process incoming record for Oracle WMS."""
        stream = record_message.stream
        record = record_message.record

        # Buffer records for batch processing
        if stream not in self.buffer:
            self.buffer[stream] = []

        self.buffer[stream].append(record)

        # Flush buffer when it reaches threshold
        if len(self.buffer[stream]) >= 100:
            self._flush_stream(stream)

    def _flush_stream(self, stream: str) -> None:
        """Flush buffered records to Oracle WMS."""
        if stream in self.buffer and self.buffer[stream]:
            records = self.buffer[stream]

            # This would use actual Oracle WMS bulk operations
            # Currently not implemented - requires LGF v10 bulk APIs
            result = self._bulk_upsert(stream, records)

            if result.is_success:
                singer.write_message(
                    singer.StateMessage(value={"stream": stream, "processed": len(records)})
                )
            else:
                singer.write_message(
                    singer.StateMessage(value={"error": result.error})
                )

            self.buffer[stream] = []

    def _bulk_upsert(self, stream: str, records: list) -> FlextResult:
        """Bulk upsert records to Oracle WMS."""
        # Requires implementation of LGF v10 bulk APIs
        # Current framework only has basic endpoint definitions
        return FlextResult.fail("Bulk operations not implemented")
```

## DBT Integration Examples

### Oracle WMS DBT Models

Framework for DBT transformations:

```yaml
# models/oracle_wms/sources.yml
version: 2

sources:
  - name: oracle_wms
    description: Oracle WMS source data
    tables:
      - name: inventory_items
        description: Oracle WMS inventory items
        columns:
          - name: item_id
            description: Unique item identifier
            tests:
              - unique
              - not_null

      - name: shipments
        description: Oracle WMS shipments
        columns:
          - name: shipment_id
            description: Unique shipment identifier
            tests:
              - unique
              - not_null
```

```sql
-- models/oracle_wms/dim_inventory.sql
{{ config(materialized='table') }}

SELECT
    item_id,
    item_name,
    item_category,
    current_quantity,
    last_updated,
    -- Oracle WMS specific transformations
    CASE
        WHEN current_quantity > 0 THEN 'In Stock'
        ELSE 'Out of Stock'
    END as stock_status

FROM {{ source('oracle_wms', 'inventory_items') }}
WHERE item_id IS NOT NULL
```

## FLEXT Web Integration

### Web Interface Integration

Framework for web application integration:

```python
from typing import Dict, Any
from flext_core import FlextResult
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig

class OracleWmsWebService:
    """Web service integration for Oracle WMS."""

    def __init__(self):
        self.config = FlextOracleWmsModuleConfig.for_testing()
        self.client = FlextOracleWmsClient(self.config)

    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get Oracle WMS data for web dashboard."""
        dashboard_data = {
            "status": "error",
            "entities": [],
            "error_message": None
        }

        try:
            # Entity discovery for dashboard
            result = self.client.discover_entities()

            if result.is_success:
                dashboard_data.update({
                    "status": "success",
                    "entities": result.value,
                    "entity_count": len(result.value),
                    "last_updated": "2025-09-17T00:00:00Z"
                })
            else:
                dashboard_data.update({
                    "error_message": result.error
                })

        except Exception as e:
            dashboard_data.update({
                "error_message": f"Service error: {e}"
            })

        return dashboard_data

    async def get_entity_details(self, entity_name: str) -> Dict[str, Any]:
        """Get detailed entity information for web interface."""
        try:
            # This would use actual Oracle WMS entity data
            result = self.client.get_entity_data(entity_name, limit=50)

            if result.is_success:
                return {
                    "status": "success",
                    "entity_name": entity_name,
                    "records": result.value,
                    "record_count": len(result.value)
                }
            else:
                return {
                    "status": "error",
                    "entity_name": entity_name,
                    "error_message": result.error
                }

        except Exception as e:
            return {
                "status": "error",
                "entity_name": entity_name,
                "error_message": f"Service error: {e}"
            }
```

## Integration Status Summary

### Current FLEXT Integration

| Component | Status | Implementation |
|-----------|--------|----------------|
| **flext-core** | ✅ Partial | FlextResult, FlextLogger patterns |
| **flext-api** | ❌ Missing | Requires httpx replacement |
| **flext-auth** | ❌ Missing | Requires OAuth2 implementation |
| **flext-cli** | ❌ Missing | No CLI operations support |
| **Singer protocol** | 🔄 Framework | Structure exists, needs real Oracle WMS |

### Required Implementation Work

1. **HTTP Client Migration** - Replace httpx with flext-api patterns
2. **Authentication Integration** - Implement flext-auth OAuth2 support
3. **Real Oracle WMS Connectivity** - Replace test URLs with actual endpoints
4. **Modern API Support** - Add LGF v10 endpoints for bulk operations
5. **Singer Protocol Completion** - Implement real data extraction/loading

---

**Last Updated**: September 17, 2025 | **Status**: Framework integration patterns requiring implementation