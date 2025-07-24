"""Singer SDK integration module for Oracle WMS data processing.

This module provides Singer SDK-compatible data flattening and deflattening
capabilities for Oracle WMS data structures, enabling seamless integration
with the Singer ecosystem for ETL operations.
"""

from __future__ import annotations

from flext_oracle_wms.singer.flattening import (
    # Result types
    FlatteningResult,
    FlextOracleWmsDeflattener,
    FlextOracleWmsDeflatteningResult,
    # Core flattening/deflattening classes
    FlextOracleWmsFlattener,
    flext_oracle_wms_create_deflattener,
    # Factory functions
    flext_oracle_wms_create_flattener,
    flext_oracle_wms_deflattened_wms_record,
    # Convenience functions
    flext_oracle_wms_flatten_wms_record,
)

__all__ = [
    "FlatteningResult",
    "FlextOracleWmsDeflattener",
    "FlextOracleWmsDeflatteningResult",
    "FlextOracleWmsFlattener",
    "flext_oracle_wms_create_deflattener",
    "flext_oracle_wms_create_flattener",
    "flext_oracle_wms_deflattened_wms_record",
    "flext_oracle_wms_flatten_wms_record",
]
