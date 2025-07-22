"""Singer SDK integration module for Oracle WMS data processing.

This module provides Singer SDK-compatible data flattening and deflattening
capabilities for Oracle WMS data structures, enabling seamless integration
with the Singer ecosystem for ETL operations.
"""

from __future__ import annotations

from flext_oracle_wms.common import create_standard_exports
from flext_oracle_wms.singer.flattening import (
    DeflatteningResult,
    # Result types
    FlatteningResult,
    OracleWMSDeflattener,
    # Core flattening/deflattening classes
    OracleWMSFlattener,
    create_deflattener,
    # Factory functions
    create_flattener,
    deflattened_wms_record,
    # Convenience functions
    flatten_wms_record,
)

# Use standardized export pattern
_exports = [
    "DeflatteningResult",
    "FlatteningResult",
    "OracleWMSDeflattener",
    "OracleWMSFlattener",
    "create_deflattener",
    "create_flattener",
    "deflattened_wms_record",
    "flatten_wms_record",
]

__all__, __doc__ = create_standard_exports("Singer SDK", _exports)
