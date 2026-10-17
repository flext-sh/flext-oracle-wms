# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._protocols.config import FlextOracleWmsProtocolsConfig
    from flext_oracle_wms._protocols.domain import FlextOracleWmsProtocolsDomain


__all__: tuple[str, ...] = (
    "FlextOracleWmsProtocolsConfig",
    "FlextOracleWmsProtocolsDomain",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextOracleWmsProtocolsConfig": ".config",
        "FlextOracleWmsProtocolsDomain": ".domain",
    }),
    public_exports=__all__,
)
