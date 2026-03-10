"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from flext_core import FlextTypes
from pydantic import BaseModel


class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

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
        type WmsProjectConfig = dict[str, FlextTypes.ContainerValue]
        type WarehouseConfig = dict[str, str | int | bool | list[str]]
        type InventoryConfig = dict[
            str, bool | str | dict[str, FlextTypes.ContainerValue]
        ]

    type WmsConfig = dict[str, str | int | bool | dict[str, FlextTypes.ContainerValue]]
    type WmsEntity = dict[
        str, FlextTypes.JsonValue | dict[str, FlextTypes.ContainerValue]
    ]
    type WmsRecord = dict[str, FlextTypes.ContainerValue]
    type WmsRecords = list[dict[str, FlextTypes.ContainerValue]]

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextOracleWmsTypes.
        """

        type Dict = dict[str, FlextTypes.ContainerValue]
        "Type alias for generic dictionary (attribute name to value mapping)."
        type FilterScalar = t.Scalar | None
        type FilterList = list[t.Core.FilterScalar]
        type FilterRecordValue = (
            t.Core.FilterScalar | t.Core.FilterList | Mapping[str, FilterRecordValue]
        )
        type FilterRecord = Mapping[str, t.Core.FilterRecordValue]


t = FlextOracleWmsTypes
__all__ = ["FlextOracleWmsTypes", "t"]


class OperatorFilter(BaseModel):
    operator: str
    value: t.Core.FilterScalar | t.Core.FilterList
