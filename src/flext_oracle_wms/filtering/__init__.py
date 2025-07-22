"""Advanced filtering module for Oracle WMS data processing.

This module provides comprehensive filtering capabilities for Oracle WMS data,
including advanced filter conditions, grouping, and query building functionality
with optimized performance for large datasets.
"""

from __future__ import annotations

from flext_oracle_wms.common import create_standard_exports
from flext_oracle_wms.filtering.advanced import (
    # Filter structures
    FilterCondition,
    FilterGroup,
    FilterQuery,
    FilterResult,
    # Core filtering classes
    OracleWMSAdvancedFilter,
    # Factory functions
    create_advanced_filter,
    # Convenience functions
    filter_by_id_range,
    filter_by_modification_time,
)

# Use standardized export pattern
_exports = [
    "FilterCondition",
    "FilterGroup",
    "FilterQuery",
    "FilterResult",
    "OracleWMSAdvancedFilter",
    "create_advanced_filter",
    "filter_by_id_range",
    "filter_by_modification_time",
]

__all__, __doc__ = create_standard_exports("Filtering", _exports)
