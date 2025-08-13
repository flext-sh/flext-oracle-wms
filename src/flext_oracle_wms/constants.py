"""Backward-compatibility constants shim.

Provides legacy import path `flext_oracle_wms.constants` by re-exporting
from the consolidated constants module.
"""
from __future__ import annotations

from .wms_constants import (
    FlextOracleWmsApiPaths,
    FlextOracleWmsApiVersion,
    FlextOracleWmsConstants,
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
    FlextOracleWmsResponseFields,
    OracleWMSAuthMethod,
)

__all__ = [
    "FlextOracleWmsApiPaths",
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsErrorMessages",
    "FlextOracleWmsResponseFields",
    "OracleWMSAuthMethod",
]
