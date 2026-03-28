"""FLEXT Oracle WMS Discovery module -- backward-compat re-export.

All logic moved to _utilities/discovery.py. Import via u.OracleWms.Discovery or this shim.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms._utilities.discovery import (
    DISCOVERY_FAILURE,
    DISCOVERY_SUCCESS,
    FlextOracleWmsUtilitiesDiscovery,
)

FlextOracleWmsEntityDiscovery = FlextOracleWmsUtilitiesDiscovery.EntityDiscovery

__all__ = ["DISCOVERY_FAILURE", "DISCOVERY_SUCCESS", "FlextOracleWmsEntityDiscovery"]
