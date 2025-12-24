"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext import FlextTypes


class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class Project:
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
        type WmsProjectConfig = dict[str, FlextTypes.GeneralValueType | object]
        type WarehouseConfig = dict[str, str | int | bool | list[str]]
        type InventoryConfig = dict[str, bool | str | dict[str, object]]

    # Core types using advanced composition and unions
    type WmsConfig = dict[str, str | int | bool | dict[str, object]]
    type WmsEntity = dict[str, FlextTypes.JsonValue | dict[str, object]]
    type WmsRecord = dict[str, object]
    type WmsRecords = list[WmsRecord]

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
        type Dict = dict[str, object]
        """Type alias for generic dictionary (attribute name to value mapping)."""

    class OracleWms:
        """OracleWms types namespace for cross-project access.

        Provides organized access to all OracleWms types for other FLEXT projects.
        Usage: Other projects can reference `t.OracleWms.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.

        Examples:
            from flext_oracle_wms.typings import t
            config: t.OracleWms.Project.WmsProjectConfig = ...
            entity: t.OracleWms.WmsEntity = ...

        Note: Namespace composition via inheritance - no aliases needed.
        Access parent namespaces directly through inheritance.

        """


# Alias for simplified usage
t = FlextOracleWmsTypes

# Namespace composition via class inheritance
# OracleWms namespace provides access to nested classes through inheritance
# Access patterns:
# - t.OracleWms.* for OracleWms-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

__all__ = ["FlextOracleWmsTypes", "t"]
