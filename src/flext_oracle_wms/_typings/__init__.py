# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._typings.domain import FlextOracleWmsTypesDomain


__all__: tuple[str, ...] = ("FlextOracleWmsTypesDomain",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextOracleWmsTypesDomain": ".domain"}),
    public_exports=__all__,
)
