# from flext-oracle-wms/src/README.md:143
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsErrors

try:
    result = client.query_entity_data("INVENTORY")
    if not result.success:
        # Handle business logic errors via FlextResult
        logger.error(f"Query failed: {result.error}")
except FlextOracleWmsErrors.ValidationError:
    # Handle validation issues
    logger.error("Oracle WMS validation failed")
except FlextOracleWmsErrors.Error:
    # Handle any Oracle WMS error
    logger.error("Oracle WMS operation failed")
