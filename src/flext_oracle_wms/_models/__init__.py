# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._models.config import FlextOracleWmsConfigModels
    from flext_oracle_wms._models.domain import (
        ApiCategoryResponse,
        ApiEndpoint,
        AuthSettings,
        EntitiesResponse,
        Entity,
        EntityDataResponse,
        EnvironmentConfig,
        FlextOracleWmsModelsDomain,
        FlextOracleWmsOperatorFilter,
        InventoryItem,
        Location,
        Shipment,
        WmsEntity,
    )


__all__: tuple[str, ...] = (
    "ApiCategoryResponse",
    "ApiEndpoint",
    "AuthSettings",
    "EntitiesResponse",
    "Entity",
    "EntityDataResponse",
    "EnvironmentConfig",
    "FlextOracleWmsConfigModels",
    "FlextOracleWmsModelsDomain",
    "FlextOracleWmsOperatorFilter",
    "InventoryItem",
    "Location",
    "Shipment",
    "WmsEntity",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ApiCategoryResponse": ".domain",
        "ApiEndpoint": ".domain",
        "AuthSettings": ".domain",
        "EntitiesResponse": ".domain",
        "Entity": ".domain",
        "EntityDataResponse": ".domain",
        "EnvironmentConfig": ".domain",
        "FlextOracleWmsConfigModels": ".config",
        "FlextOracleWmsModelsDomain": ".domain",
        "FlextOracleWmsOperatorFilter": ".domain",
        "InventoryItem": ".domain",
        "Location": ".domain",
        "Shipment": ".domain",
        "WmsEntity": ".domain",
    }),
    public_exports=__all__,
)
