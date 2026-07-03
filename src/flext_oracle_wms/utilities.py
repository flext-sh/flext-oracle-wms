"""Oracle WMS utilities extending u via MRO composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import u

from flext_core import FlextUtilitiesConversion, FlextUtilitiesReliability
from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth
from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient
from flext_oracle_wms._utilities.discovery import FlextOracleWmsUtilitiesDiscovery
from flext_oracle_wms._utilities.filtering import FlextOracleWmsUtilitiesFiltering
from flext_oracle_wms._utilities.http_client import FlextOracleWmsUtilitiesHttpClient


class FlextOracleWmsUtilities(u, FlextUtilitiesConversion, FlextUtilitiesReliability):
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
