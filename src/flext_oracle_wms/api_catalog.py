"""Backward-compatibility API catalog shim.

This module preserves the historical import path
`flext_oracle_wms.api_catalog` used by tests and external code by
re-exporting the consolidated API catalog and related types.
"""
from __future__ import annotations

from .wms_api import FLEXT_ORACLE_WMS_APIS, OracleWmsMockServer, get_mock_server
from .wms_models import (
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    FlextOracleWmsApiVersion,
)

__all__: list[str] = [
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiVersion",
    "OracleWmsMockServer",
    "get_mock_server",
]
