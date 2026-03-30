"""FLEXT Oracle WMS Authentication module -- backward-compat re-export.

All logic moved to _utilities/auth.py. Import via u.OracleWms.Auth or this shim.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsUtilitiesAuth

FlextOracleWmsAuthenticator = FlextOracleWmsUtilitiesAuth.Authenticator

__all__ = [
    "FlextOracleWmsAuthenticator",
]
