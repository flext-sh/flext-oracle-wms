"""FLEXT Oracle WMS - Enterprise Oracle Warehouse Management System Integration.

 Oracle WMS integration with Clean Architecture, railway-oriented error handling,
and domain-driven design. Provides inventory, shipment, and picking operations with OAuth2 auth.

Usage: from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextDecorators,
    FlextExceptions,
    FlextHandlers,
    FlextMixins,
    FlextResult,
    FlextService,
)

# Version information
from flext_oracle_wms.__version__ import __version__, __version_info__
from flext_oracle_wms.constants import (
    FlextOracleWmsConstants,
    OracleWMSAuthMethod,
)

# Protocol definitions
from flext_oracle_wms.protocols import FlextOracleWmsProtocols

# Core configuration and constants
from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.typings import FlextOracleWmsTypes

# Type definitions and models - using direct imports
from flext_oracle_wms.utilities import FlextOracleWmsUtilities

# WMS API and discovery
from flext_oracle_wms.wms_api import FlextOracleWmsApi

# Authentication and client
from flext_oracle_wms.wms_auth import (
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthSettings,
    create_oracle_wms_client,
)
from flext_oracle_wms.wms_client import FlextOracleWmsClient
from flext_oracle_wms.wms_discovery import FlextOracleWmsEntityDiscovery
from flext_oracle_wms.wms_models import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsEntity,
    FlextOracleWmsModels,
    TOracleWmsRecord,
    TOracleWmsRecordBatch,
)

# Domain-specific aliases (extending flext-core base classes)
u = FlextOracleWmsUtilities  # Utilities (FlextOracleWmsUtilities extends FlextUtilities)
m = FlextOracleWmsModels  # Models (FlextOracleWmsModels extends FlextModels)
c = FlextOracleWmsConstants  # Constants (FlextOracleWmsConstants extends FlextConstants)
t = FlextOracleWmsTypes  # Types (FlextOracleWmsTypes extends FlextTypes)
p = FlextOracleWmsProtocols  # Protocols (FlextOracleWmsProtocols extends FlextProtocols)

# Global aliases from flext-core

r = FlextResult  # Shared from flext-core
e = FlextExceptions  # Shared from flext-core
d = FlextDecorators  # Shared from flext-core
s = FlextService  # Shared from flext-core
x = FlextMixins  # Shared from flext-core
h = FlextHandlers  # Shared from flext-core


# Direct FLEXT exception classes with real inheritance
class FlextOracleWmsError(FlextExceptions.BaseError):
    """FlextOracleWmsError - real inheritance from BaseError."""


class FlextOracleWmsApiError(FlextExceptions.BaseError):
    """FlextOracleWmsApiError - real inheritance from BaseError."""


class FlextOracleWmsAuthenticationError(FlextExceptions.AuthenticationError):
    """FlextOracleWmsAuthenticationError - real inheritance from AuthenticationError."""


class FlextOracleWmsEntityNotFoundError(FlextExceptions.BaseError):
    """FlextOracleWmsEntityNotFoundError - real inheritance from BaseError."""


FlextOracleWmsExceptions = FlextExceptions  # Namespace alias (not a class)


class FlextOracleWmsInventoryError(FlextExceptions.BaseError):
    """FlextOracleWmsInventoryError - real inheritance from BaseError."""


class FlextOracleWmsPickingError(FlextExceptions.BaseError):
    """FlextOracleWmsPickingError - real inheritance from BaseError."""


class FlextOracleWmsSchemaError(FlextExceptions.BaseError):
    """FlextOracleWmsSchemaError - real inheritance from BaseError."""


class FlextOracleWmsSchemaFlatteningError(FlextExceptions.BaseError):
    """FlextOracleWmsSchemaFlatteningError - real inheritance from BaseError."""


class FlextOracleWmsShipmentError(FlextExceptions.BaseError):
    """FlextOracleWmsShipmentError - real inheritance from BaseError."""


# API catalog access
FLEXT_ORACLE_WMS_APIS = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS


# Utility functions
def get_mock_server(environment: str = "mock_test") -> object:
    """Get Oracle WMS mock server instance."""
    return {"environment": environment, "type": "mock_server"}


__all__ = [
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWmsApi",
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiResponse",
    "FlextOracleWmsAuthSettings",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsClient",
    "FlextOracleWmsConstants",
    "FlextOracleWmsEntity",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsExceptions",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsModels",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsSettings",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUtilities",
    "OracleWMSAuthMethod",
    "TOracleWmsRecord",
    "TOracleWmsRecordBatch",
    "__version__",
    "__version_info__",
    # Domain-specific aliases
    "c",
    "create_oracle_wms_client",
    # Global aliases
    "d",
    "e",
    "get_mock_server",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]
