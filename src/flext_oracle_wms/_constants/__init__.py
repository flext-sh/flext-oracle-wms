# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._constants.base import FlextOracleWmsConstantsBase
    from flext_oracle_wms._constants.values import FlextOracleWmsConstantsValues


__all__: tuple[str, ...] = (
    "FlextOracleWmsConstantsBase",
    "FlextOracleWmsConstantsValues",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextOracleWmsConstantsBase": ".base",
        "FlextOracleWmsConstantsValues": ".values",
    }),
    public_exports=__all__,
)
