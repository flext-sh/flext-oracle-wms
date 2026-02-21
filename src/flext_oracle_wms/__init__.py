"""FLEXT Oracle WMS - Enterprise Oracle Warehouse Management System Integration.

 Oracle WMS integration with Clean Architecture, railway-oriented error handling,
and domain-driven design. Provides inventory, shipment, and picking operations with OAuth2 auth.

Usage: from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextDecorators as d,
    FlextExceptions as FlextOracleWmsExceptions,
    FlextExceptions as e,
    FlextHandlers as h,
    FlextMixins as x,
    FlextService as s,
    r,
)

from flext_oracle_wms.__version__ import __version__, __version_info__
from flext_oracle_wms._backward_compat import (
    FlextOracleWmsApiError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsEntityNotFoundError,
    FlextOracleWmsError,
    FlextOracleWmsInventoryError,
    FlextOracleWmsPickingError,
    FlextOracleWmsSchemaError,
    FlextOracleWmsSchemaFlatteningError,
    FlextOracleWmsShipmentError,
    get_mock_server,
)
from flext_oracle_wms.constants import (
    FlextOracleWmsConstants,
    FlextOracleWmsConstants as c,
    OracleWMSAuthMethod,
)
from flext_oracle_wms.protocols import (
    FlextOracleWmsProtocols,
    FlextOracleWmsProtocols as p,
)
from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.typings import FlextOracleWmsTypes, FlextOracleWmsTypes as t
from flext_oracle_wms.utilities import (
    FlextOracleWmsUtilities,
    FlextOracleWmsUtilities as u,
)
from flext_oracle_wms.wms_api import FLEXT_ORACLE_WMS_APIS, FlextOracleWmsApi
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
    FlextOracleWmsModels as m,
)

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
    "__version__",
    "__version_info__",
    "c",
    "create_oracle_wms_client",
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
