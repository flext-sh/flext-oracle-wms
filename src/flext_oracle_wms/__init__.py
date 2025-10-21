"""FLEXT Oracle WMS - Enterprise Oracle Warehouse Management System Integration.

 Oracle WMS integration with Clean Architecture, railway-oriented error handling,
and domain-driven design. Provides inventory, shipment, and picking operations with OAuth2 auth.

Usage: from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsConfig

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Exception hierarchy - using FlextExceptions directly
from flext_core import FlextExceptions

# Version information
from flext_oracle_wms.__version__ import __version__, __version_info__

# Core configuration and constants
from flext_oracle_wms.config import FlextOracleWmsConfig
from flext_oracle_wms.constants import (
    FlextOracleWmsConstants,
    OracleWMSAuthMethod,
)

# Protocol definitions
from flext_oracle_wms.protocols import FlextOracleWmsProtocols

# WMS API and discovery
from flext_oracle_wms.wms_api import FlextOracleWmsApi

# Authentication and client
from flext_oracle_wms.wms_auth import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    create_oracle_wms_client,
)
from flext_oracle_wms.wms_client import FlextOracleWmsClient
from flext_oracle_wms.wms_discovery import FlextOracleWmsEntityDiscovery

# Type definitions and models - using direct imports
from flext_oracle_wms.wms_models import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsEntity,
    TOracleWmsRecord,
    TOracleWmsRecordBatch,
)

# Direct FLEXT exception usage - no custom wrappers
FlextOracleWmsError = FlextExceptions.BaseError
FlextOracleWmsApiError = FlextExceptions.BaseError
FlextOracleWmsAuthenticationError = FlextExceptions.AuthenticationError
FlextOracleWmsEntityNotFoundError = FlextExceptions.BaseError
FlextOracleWmsExceptions = FlextExceptions
FlextOracleWmsInventoryError = FlextExceptions.BaseError
FlextOracleWmsPickingError = FlextExceptions.BaseError
FlextOracleWmsSchemaError = FlextExceptions.BaseError
FlextOracleWmsSchemaFlatteningError = FlextExceptions.BaseError
FlextOracleWmsShipmentError = FlextExceptions.BaseError

# API catalog access
FLEXT_ORACLE_WMS_APIS = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS


# Utility functions
def get_mock_server(environment: str = "mock_test") -> object:
    """Get Oracle WMS mock server instance."""
    return FlextOracleWmsApi.OracleWmsMockServer.get_mock_server(environment)


__all__ = [
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWmsApi",
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiResponse",
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsClient",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConstants",
    "FlextOracleWmsEntity",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsExceptions",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "OracleWMSAuthMethod",
    "TOracleWmsRecord",
    "TOracleWmsRecordBatch",
    "__version__",
    "__version_info__",
    "create_oracle_wms_client",
    "get_mock_server",
]
