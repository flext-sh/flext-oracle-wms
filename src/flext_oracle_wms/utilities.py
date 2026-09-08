"""Oracle WMS utilities extending u via MRO composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import u

from ._utilities.auth import FlextOracleWmsUtilitiesAuth
from ._utilities.client import FlextOracleWmsUtilitiesClient
from ._utilities.discovery import FlextOracleWmsUtilitiesDiscovery
from ._utilities.filtering import FlextOracleWmsUtilitiesFiltering
from ._utilities.http_client import FlextOracleWmsUtilitiesHttpClient


class FlextOracleWmsUtilities(
    u,
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
