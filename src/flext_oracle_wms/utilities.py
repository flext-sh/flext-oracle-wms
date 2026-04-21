"""Oracle WMS utilities extending u via MRO composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import u

from flext_oracle_wms import (
    FlextOracleWmsUtilitiesAuth,
    FlextOracleWmsUtilitiesClient,
    FlextOracleWmsUtilitiesDiscovery,
    FlextOracleWmsUtilitiesFiltering,
    FlextOracleWmsUtilitiesHttpClient,
)


class FlextOracleWmsUtilities(u):
    """Oracle WMS utilities composing all domain-specific utility mixins via MRO."""

    class OracleWms(
        FlextOracleWmsUtilitiesAuth,
        FlextOracleWmsUtilitiesClient,
        FlextOracleWmsUtilitiesDiscovery,
        FlextOracleWmsUtilitiesFiltering,
        FlextOracleWmsUtilitiesHttpClient,
    ):
        """Oracle WMS utilities extending u via MRO composition."""


u = FlextOracleWmsUtilities
__all__: list[str] = ["FlextOracleWmsUtilities", "u"]
