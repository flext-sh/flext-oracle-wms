# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._protocols.config import FlextOracleWmsProtocolsConfig


__all__: tuple[str, ...] = ("FlextOracleWmsProtocolsConfig",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextOracleWmsProtocolsConfig": ".config"}),
    public_exports=__all__,
)
