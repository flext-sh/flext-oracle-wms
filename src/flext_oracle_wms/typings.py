"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import t


class FlextOracleWmsTypes(t):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    # Core types using advanced composition and unions
    type WmsConfig = dict[str, str | int | bool | dict[str, object]]
    type WmsEntity = dict[str, t.Core.JsonValue | dict[str, object]]
    type WmsRecord = dict[str, object]
    type WmsRecords = list[WmsRecord]

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
    type WmsProjectConfig = dict[str, t.Core.ConfigValue | object]
    type WarehouseConfig = dict[str, str | int | bool | list[str]]
    type InventoryConfig = dict[str, bool | str | dict[str, object]]


__all__ = ["FlextOracleWmsTypes"]
