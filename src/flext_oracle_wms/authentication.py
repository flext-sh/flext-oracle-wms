"""Backward-compatibility authentication shim.

Provides legacy import path `flext_oracle_wms.authentication` by re-exporting
authentication components from the consolidated client module `wms_client`.
"""
from __future__ import annotations

from .wms_client import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthPlugin,
    FlextOracleWmsAuthenticator,
)

__all__ = [
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsAuthPlugin",
]
