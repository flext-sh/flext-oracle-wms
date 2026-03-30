# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Oracle WMS - Enterprise Oracle Warehouse Management System Integration.

 Oracle WMS integration with Clean Architecture, railway-oriented error handling,
and domain-driven design. Provides inventory, shipment, and picking operations with OAuth2 auth.

Usage: from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_oracle_wms.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import *

    from flext_oracle_wms import (
        _utilities,
        api,
        constants,
        errors,
        filtering,
        http_client,
        models,
        protocols,
        settings,
        typings,
        utilities,
        wms_api,
        wms_auth,
        wms_client,
        wms_discovery,
        wms_exceptions,
    )
    from flext_oracle_wms._utilities import auth, client, discovery
    from flext_oracle_wms._utilities.auth import *
    from flext_oracle_wms._utilities.client import *
    from flext_oracle_wms._utilities.discovery import *
    from flext_oracle_wms._utilities.filtering import *
    from flext_oracle_wms._utilities.http_client import *
    from flext_oracle_wms.api import *
    from flext_oracle_wms.constants import *
    from flext_oracle_wms.errors import *
    from flext_oracle_wms.filtering import *
    from flext_oracle_wms.http_client import *
    from flext_oracle_wms.models import *
    from flext_oracle_wms.protocols import *
    from flext_oracle_wms.settings import *
    from flext_oracle_wms.typings import *
    from flext_oracle_wms.utilities import *
    from flext_oracle_wms.wms_auth import *
    from flext_oracle_wms.wms_client import *
    from flext_oracle_wms.wms_discovery import *

from flext_oracle_wms._utilities import _LAZY_IMPORTS as __UTILITIES_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **__UTILITIES_LAZY,
    "FlextHttpClient": "flext_oracle_wms.http_client",
    "FlextOracleWmsApi": "flext_oracle_wms.api",
    "FlextOracleWmsApiError": "flext_oracle_wms.errors",
    "FlextOracleWmsAuthenticationError": "flext_oracle_wms.errors",
    "FlextOracleWmsAuthenticator": "flext_oracle_wms.wms_auth",
    "FlextOracleWmsClient": "flext_oracle_wms.wms_client",
    "FlextOracleWmsClientSettings": "flext_oracle_wms.settings",
    "FlextOracleWmsConfigurationError": "flext_oracle_wms.errors",
    "FlextOracleWmsConnectionError": "flext_oracle_wms.errors",
    "FlextOracleWmsConstants": "flext_oracle_wms.constants",
    "FlextOracleWmsEntityDiscovery": "flext_oracle_wms.wms_discovery",
    "FlextOracleWmsEntityNotFoundError": "flext_oracle_wms.errors",
    "FlextOracleWmsError": "flext_oracle_wms.errors",
    "FlextOracleWmsExceptions": "flext_oracle_wms.errors",
    "FlextOracleWmsFilter": "flext_oracle_wms.filtering",
    "FlextOracleWmsInventoryError": "flext_oracle_wms.errors",
    "FlextOracleWmsModels": "flext_oracle_wms.models",
    "FlextOracleWmsPickingError": "flext_oracle_wms.errors",
    "FlextOracleWmsProcessingError": "flext_oracle_wms.errors",
    "FlextOracleWmsProtocols": "flext_oracle_wms.protocols",
    "FlextOracleWmsSchemaError": "flext_oracle_wms.errors",
    "FlextOracleWmsSchemaFlatteningError": "flext_oracle_wms.errors",
    "FlextOracleWmsSettings": "flext_oracle_wms.settings",
    "FlextOracleWmsShipmentError": "flext_oracle_wms.errors",
    "FlextOracleWmsTypes": "flext_oracle_wms.typings",
    "FlextOracleWmsUtilities": "flext_oracle_wms.utilities",
    "FlextOracleWmsValidationError": "flext_oracle_wms.errors",
    "_utilities": "flext_oracle_wms._utilities",
    "api": "flext_oracle_wms.api",
    "c": ["flext_oracle_wms.constants", "FlextOracleWmsConstants"],
    "constants": "flext_oracle_wms.constants",
    "create_flext_http_client": "flext_oracle_wms.http_client",
    "d": "flext_core",
    "e": "flext_core",
    "errors": "flext_oracle_wms.errors",
    "filtering": "flext_oracle_wms.filtering",
    "h": "flext_core",
    "http_client": "flext_oracle_wms.http_client",
    "m": ["flext_oracle_wms.models", "FlextOracleWmsModels"],
    "models": "flext_oracle_wms.models",
    "p": ["flext_oracle_wms.protocols", "FlextOracleWmsProtocols"],
    "protocols": "flext_oracle_wms.protocols",
    "r": "flext_core",
    "s": "flext_core",
    "settings": "flext_oracle_wms.settings",
    "t": ["flext_oracle_wms.typings", "FlextOracleWmsTypes"],
    "typings": "flext_oracle_wms.typings",
    "u": ["flext_oracle_wms.utilities", "FlextOracleWmsUtilities"],
    "utilities": "flext_oracle_wms.utilities",
    "wms_api": "flext_oracle_wms.wms_api",
    "wms_auth": "flext_oracle_wms.wms_auth",
    "wms_client": "flext_oracle_wms.wms_client",
    "wms_discovery": "flext_oracle_wms.wms_discovery",
    "wms_exceptions": "flext_oracle_wms.wms_exceptions",
    "x": "flext_core",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
