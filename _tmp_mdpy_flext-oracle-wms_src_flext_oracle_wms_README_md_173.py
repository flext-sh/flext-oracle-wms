# from flext-oracle-wms_src/flext_oracle_wms/README.md:173
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsConnectionError

try:
    result = client.get_entity_data("inventory")
    if result.is_failure:
        # Handle business logic errors via r

        u.fetch_logger(__name__).error("Query failed", error=result.error)
    else:
        # Process successful result
        inventory_data = result.data

        u.fetch_logger(__name__).info("Retrieved inventory data", count=len(inventory_data))

except FlextOracleWmsConnectionError as e:
    # Handle connection-specific errors
from flext_cli import u
from flext_core import FlextSettings
    u.fetch_logger(__name__).error("Connection failed", error=str(e))
