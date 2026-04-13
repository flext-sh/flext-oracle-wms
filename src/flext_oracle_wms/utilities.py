"""FLEXT Oracle WMS Utilities - Domain-specific utilities extending u.

This module provides Oracle WMS-specific utility functions extending u
from flext-core. Uses advanced builder patterns and composition for clean code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import u

from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth
from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient
from flext_oracle_wms._utilities.discovery import FlextOracleWmsUtilitiesDiscovery
from flext_oracle_wms._utilities.filtering import FlextOracleWmsUtilitiesFiltering
from flext_oracle_wms._utilities.http_client import FlextOracleWmsUtilitiesHttpClient


class FlextOracleWmsUtilities(u):
    """Oracle WMS utilities extending u with domain-specific helpers.

    Architecture: Extends u with Oracle WMS-specific operations.
    Uses composition and delegation to maximize reuse of base utilities.
    """

    class OracleWms:
        """OracleWms domain namespace -- u.OracleWms.*."""

        Auth = FlextOracleWmsUtilitiesAuth
        Client = FlextOracleWmsUtilitiesClient
        Discovery = FlextOracleWmsUtilitiesDiscovery
        Filtering = FlextOracleWmsUtilitiesFiltering
        HttpClient = FlextOracleWmsUtilitiesHttpClient


u = FlextOracleWmsUtilities
__all__: list[str] = ["FlextOracleWmsUtilities", "u"]
