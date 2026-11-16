# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._models.domain import FlextOracleWmsModelsDomain


__all__: tuple[str, ...] = ("FlextOracleWmsModelsDomain",)

install_lazy_exports(
    __name__,
    globals(),
    {"FlextOracleWmsModelsDomain": ".domain"},
    public_exports=__all__,
    deferred_members={
        "FlextOracleWmsModelsDomain": (
            "FlextOracleWmsOperatorFilter",
            "EnvironmentConfig",
            "Entity",
            "ApiEndpoint",
            "AuthSettings",
            "EntitiesResponse",
            "ApiCategoryResponse",
            "EntityDataResponse",
            "WmsEntity",
            "InventoryItem",
            "Shipment",
            "Location",
        ),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextOracleWmsModelsDomain": (
            ("flext_oracle_wms", "FlextOracleWmsModelsConfig"),
        ),
    },
)
