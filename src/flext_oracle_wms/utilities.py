"""FLEXT Oracle WMS Utilities - Domain-specific utilities extending FlextUtilities.

This module provides Oracle WMS-specific utility functions extending FlextUtilities
from flext-core. Uses advanced builder patterns and composition for clean code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextUtilities

from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth
from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient
from flext_oracle_wms._utilities.discovery import FlextOracleWmsUtilitiesDiscovery
from flext_oracle_wms._utilities.filtering import FlextOracleWmsUtilitiesFiltering
from flext_oracle_wms._utilities.http_client import FlextOracleWmsUtilitiesHttpClient


class FlextOracleWmsUtilities(FlextUtilities):
    """Oracle WMS utilities extending FlextUtilities with domain-specific helpers.

    Architecture: Extends FlextUtilities with Oracle WMS-specific operations.
    Uses composition and delegation to maximize reuse of base utilities.
    """

    class OracleWms:
        """OracleWms domain namespace -- u.OracleWms.*."""

        Auth = FlextOracleWmsUtilitiesAuth
        Client = FlextOracleWmsUtilitiesClient
        Discovery = FlextOracleWmsUtilitiesDiscovery
        Filtering = FlextOracleWmsUtilitiesFiltering
        HttpClient = FlextOracleWmsUtilitiesHttpClient


__all__ = ["FlextOracleWmsUtilities", "u"]

u = FlextOracleWmsUtilities
