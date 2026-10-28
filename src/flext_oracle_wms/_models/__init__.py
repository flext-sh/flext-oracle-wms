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
    from flext_oracle_wms._models.config import FlextModelsOracleWmsConfig
    from flext_oracle_wms._models.domain import FlextModelsOracleWmsDomain


__all__: tuple[str, ...] = ("FlextModelsOracleWmsConfig", "FlextModelsOracleWmsDomain")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextModelsOracleWmsConfig": ".config",
        "FlextModelsOracleWmsDomain": ".domain",
    }),
    public_exports=__all__,
)
