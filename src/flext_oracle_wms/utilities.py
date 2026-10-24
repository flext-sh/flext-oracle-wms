# AUTO-GENERATED FILE — Regenerate with: make gen
"""Oracle WMS utilities extending u via MRO composition.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import FlextApiUtilities

from flext_oracle_wms._utilities import (
    FlextOracleWmsUtilitiesAuth,
    FlextOracleWmsUtilitiesClient,
    FlextOracleWmsUtilitiesDiscovery,
    FlextOracleWmsUtilitiesFiltering,
    FlextOracleWmsUtilitiesHttpClient,
)


class FlextOracleWmsUtilities(
    FlextApiUtilities,
    FlextOracleWmsUtilitiesAuth,
    FlextOracleWmsUtilitiesClient,
    FlextOracleWmsUtilitiesDiscovery,
    FlextOracleWmsUtilitiesFiltering,
    FlextOracleWmsUtilitiesHttpClient,
):
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
__all__: list[str] = [
    "FlextOracleWmsUtilities",
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
    "u",
]
