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
    from flext_oracle_wms._models.domain import FlextOracleWmsModelsDomain


__all__: tuple[str, ...] = ("FlextOracleWmsConfigModels", "FlextOracleWmsModelsDomain")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextOracleWmsConfigModels": ".config",
        "FlextOracleWmsModelsDomain": ".domain",
    }),
    public_exports=__all__,
)
