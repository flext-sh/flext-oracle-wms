"""FLEXT Oracle WMS Client module -- backward-compat re-export.

All logic moved to _utilities/client.py. Import via u.OracleWms.Client or this shim.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient

FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client

__all__ = ["FlextOracleWmsClient"]
