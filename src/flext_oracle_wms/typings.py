"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes


class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

        # Project types using Literal for advanced typing
        type ProjectType = Literal[
            "wms-service",
            "warehouse-management",
            "inventory-system",
            "shipping-service",
            "picking-system",
            "wms-integration",
            "warehouse-api",
            "logistics-platform",
            "inventory-tracker",
            "warehouse-monitor",
            "wms-connector",
            "fulfillment-engine",
            "warehouse-analytics",
            "wms-client",
            "logistics-service",
            "warehouse-optimizer",
        ]

        # Configuration types using dict composition
        type WmsProjectConfig = dict[str, FlextTypes.GeneralValueType]
        type WarehouseConfig = dict[str, str | int | bool | list[str]]
        type InventoryConfig = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]

    # Core types using advanced composition and unions
    type WmsConfig = dict[
        str, str | int | bool | dict[str, FlextTypes.GeneralValueType]
    ]
    type WmsEntity = dict[
        str, FlextTypes.JsonValue | dict[str, FlextTypes.GeneralValueType]
    ]
    type WmsRecord = dict[str, FlextTypes.GeneralValueType]
    type WmsRecords = list[dict[str, FlextTypes.GeneralValueType]]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Convenience aliases for common patterns
    # =========================================================================

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextOracleWmsTypes.
        """

        # Common dictionary types
        type Dict = dict[str, FlextTypes.GeneralValueType]
        """Type alias for generic dictionary (attribute name to value mapping)."""


# Alias for simplified usage
t = FlextOracleWmsTypes

# Namespace composition via class inheritance
# OracleWms namespace provides access to nested classes through inheritance
# Access patterns:
# - t.OracleWms.* for OracleWms-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

__all__ = ["FlextOracleWmsTypes", "t"]
