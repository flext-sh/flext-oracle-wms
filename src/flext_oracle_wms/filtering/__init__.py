"""Advanced filtering module for Oracle WMS data processing.

This module provides comprehensive filtering capabilities for Oracle WMS data,
including advanced filter conditions, grouping, and query building functionality
with optimized performance for large datasets.
"""

from __future__ import annotations

from flext_oracle_wms.filtering.advanced import (
    # Filter structures
    FilterCondition,
    FilterGroup,
    FilterQuery,
    FilterResult,
    # Core filtering classes
    FlextOracleWmsAdvancedFilter,
    # Factory functions
    flext_oracle_wms_create_advanced_filter,
    # Convenience functions
    flext_oracle_wms_filter_by_id_range,
    flext_oracle_wms_filter_by_modification_time,
)

__all__ = [
    "FilterCondition",
    "FilterGroup",
    "FilterQuery",
    "FilterResult",
    "FlextOracleWmsAdvancedFilter",
    "flext_oracle_wms_create_advanced_filter",
    "flext_oracle_wms_filter_by_id_range",
    "flext_oracle_wms_filter_by_modification_time",
]
