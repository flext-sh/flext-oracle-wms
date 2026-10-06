# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth
    from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient
    from flext_oracle_wms._utilities.discovery import FlextOracleWmsUtilitiesDiscovery
    from flext_oracle_wms._utilities.filtering import FlextOracleWmsUtilitiesFiltering
    from flext_oracle_wms._utilities.http_client import (
        FlextOracleWmsUtilitiesHttpClient,
    )


__all__: tuple[str, ...] = (
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextOracleWmsUtilitiesAuth": ".auth",
        "FlextOracleWmsUtilitiesClient": ".client",
        "FlextOracleWmsUtilitiesDiscovery": ".discovery",
        "FlextOracleWmsUtilitiesFiltering": ".filtering",
        "FlextOracleWmsUtilitiesHttpClient": ".http_client",
    }),
    public_exports=__all__,
)
