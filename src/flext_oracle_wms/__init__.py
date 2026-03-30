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
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_oracle_wms import (
        _utilities as _utilities,
        api as api,
        constants as constants,
        errors as errors,
        filtering as filtering,
        http_client as http_client,
        models as models,
        protocols as protocols,
        settings as settings,
        typings as typings,
        utilities as utilities,
        wms_api as wms_api,
        wms_auth as wms_auth,
        wms_client as wms_client,
        wms_discovery as wms_discovery,
        wms_exceptions as wms_exceptions,
    )
    from flext_oracle_wms._utilities import (
        auth as auth,
        client as client,
        discovery as discovery,
    )
    from flext_oracle_wms._utilities.auth import (
        FlextOracleWmsUtilitiesAuth as FlextOracleWmsUtilitiesAuth,
    )
    from flext_oracle_wms._utilities.client import (
        FlextOracleWmsUtilitiesClient as FlextOracleWmsUtilitiesClient,
    )
    from flext_oracle_wms._utilities.discovery import (
        DISCOVERY_FAILURE as DISCOVERY_FAILURE,
        DISCOVERY_SUCCESS as DISCOVERY_SUCCESS,
        FlextOracleWmsUtilitiesDiscovery as FlextOracleWmsUtilitiesDiscovery,
    )
    from flext_oracle_wms._utilities.filtering import (
        FlextOracleWmsDataValidationError as FlextOracleWmsDataValidationError,
        FlextOracleWmsFilterOperator as FlextOracleWmsFilterOperator,
        FlextOracleWmsOperatorFilter as FlextOracleWmsOperatorFilter,
        FlextOracleWmsUtilitiesFiltering as FlextOracleWmsUtilitiesFiltering,
    )
    from flext_oracle_wms._utilities.http_client import (
        FlextOracleWmsUtilitiesHttpClient as FlextOracleWmsUtilitiesHttpClient,
    )
    from flext_oracle_wms.api import FlextOracleWmsApi as FlextOracleWmsApi
    from flext_oracle_wms.constants import (
        FlextOracleWmsConstants as FlextOracleWmsConstants,
        FlextOracleWmsConstants as c,
    )
    from flext_oracle_wms.errors import (
        FlextOracleWmsApiError as FlextOracleWmsApiError,
        FlextOracleWmsAuthenticationError as FlextOracleWmsAuthenticationError,
        FlextOracleWmsConfigurationError as FlextOracleWmsConfigurationError,
        FlextOracleWmsConnectionError as FlextOracleWmsConnectionError,
        FlextOracleWmsEntityNotFoundError as FlextOracleWmsEntityNotFoundError,
        FlextOracleWmsError as FlextOracleWmsError,
        FlextOracleWmsExceptions as FlextOracleWmsExceptions,
        FlextOracleWmsInventoryError as FlextOracleWmsInventoryError,
        FlextOracleWmsPickingError as FlextOracleWmsPickingError,
        FlextOracleWmsProcessingError as FlextOracleWmsProcessingError,
        FlextOracleWmsSchemaError as FlextOracleWmsSchemaError,
        FlextOracleWmsSchemaFlatteningError as FlextOracleWmsSchemaFlatteningError,
        FlextOracleWmsShipmentError as FlextOracleWmsShipmentError,
        FlextOracleWmsValidationError as FlextOracleWmsValidationError,
    )
    from flext_oracle_wms.filtering import FlextOracleWmsFilter as FlextOracleWmsFilter
    from flext_oracle_wms.http_client import (
        FlextHttpClient as FlextHttpClient,
        create_flext_http_client as create_flext_http_client,
    )
    from flext_oracle_wms.models import (
        FlextOracleWmsModels as FlextOracleWmsModels,
        FlextOracleWmsModels as m,
    )
    from flext_oracle_wms.protocols import (
        FlextOracleWmsProtocols as FlextOracleWmsProtocols,
        FlextOracleWmsProtocols as p,
    )
    from flext_oracle_wms.settings import (
        FlextOracleWmsClientSettings as FlextOracleWmsClientSettings,
        FlextOracleWmsSettings as FlextOracleWmsSettings,
    )
    from flext_oracle_wms.typings import (
        FlextOracleWmsTypes as FlextOracleWmsTypes,
        FlextOracleWmsTypes as t,
    )
    from flext_oracle_wms.utilities import (
        FlextOracleWmsUtilities as FlextOracleWmsUtilities,
        FlextOracleWmsUtilities as u,
    )
    from flext_oracle_wms.wms_auth import (
        FlextOracleWmsAuthenticator as FlextOracleWmsAuthenticator,
    )
    from flext_oracle_wms.wms_client import FlextOracleWmsClient as FlextOracleWmsClient
    from flext_oracle_wms.wms_discovery import (
        FlextOracleWmsEntityDiscovery as FlextOracleWmsEntityDiscovery,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "DISCOVERY_FAILURE": ["flext_oracle_wms._utilities.discovery", "DISCOVERY_FAILURE"],
    "DISCOVERY_SUCCESS": ["flext_oracle_wms._utilities.discovery", "DISCOVERY_SUCCESS"],
    "FlextHttpClient": ["flext_oracle_wms.http_client", "FlextHttpClient"],
    "FlextOracleWmsApi": ["flext_oracle_wms.api", "FlextOracleWmsApi"],
    "FlextOracleWmsApiError": ["flext_oracle_wms.errors", "FlextOracleWmsApiError"],
    "FlextOracleWmsAuthenticationError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsAuthenticationError",
    ],
    "FlextOracleWmsAuthenticator": [
        "flext_oracle_wms.wms_auth",
        "FlextOracleWmsAuthenticator",
    ],
    "FlextOracleWmsClient": ["flext_oracle_wms.wms_client", "FlextOracleWmsClient"],
    "FlextOracleWmsClientSettings": [
        "flext_oracle_wms.settings",
        "FlextOracleWmsClientSettings",
    ],
    "FlextOracleWmsConfigurationError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsConfigurationError",
    ],
    "FlextOracleWmsConnectionError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsConnectionError",
    ],
    "FlextOracleWmsConstants": [
        "flext_oracle_wms.constants",
        "FlextOracleWmsConstants",
    ],
    "FlextOracleWmsDataValidationError": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsDataValidationError",
    ],
    "FlextOracleWmsEntityDiscovery": [
        "flext_oracle_wms.wms_discovery",
        "FlextOracleWmsEntityDiscovery",
    ],
    "FlextOracleWmsEntityNotFoundError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsEntityNotFoundError",
    ],
    "FlextOracleWmsError": ["flext_oracle_wms.errors", "FlextOracleWmsError"],
    "FlextOracleWmsExceptions": ["flext_oracle_wms.errors", "FlextOracleWmsExceptions"],
    "FlextOracleWmsFilter": ["flext_oracle_wms.filtering", "FlextOracleWmsFilter"],
    "FlextOracleWmsFilterOperator": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsFilterOperator",
    ],
    "FlextOracleWmsInventoryError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsInventoryError",
    ],
    "FlextOracleWmsModels": ["flext_oracle_wms.models", "FlextOracleWmsModels"],
    "FlextOracleWmsOperatorFilter": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsOperatorFilter",
    ],
    "FlextOracleWmsPickingError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsPickingError",
    ],
    "FlextOracleWmsProcessingError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsProcessingError",
    ],
    "FlextOracleWmsProtocols": [
        "flext_oracle_wms.protocols",
        "FlextOracleWmsProtocols",
    ],
    "FlextOracleWmsSchemaError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsSchemaError",
    ],
    "FlextOracleWmsSchemaFlatteningError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsSchemaFlatteningError",
    ],
    "FlextOracleWmsSettings": ["flext_oracle_wms.settings", "FlextOracleWmsSettings"],
    "FlextOracleWmsShipmentError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsShipmentError",
    ],
    "FlextOracleWmsTypes": ["flext_oracle_wms.typings", "FlextOracleWmsTypes"],
    "FlextOracleWmsUtilities": [
        "flext_oracle_wms.utilities",
        "FlextOracleWmsUtilities",
    ],
    "FlextOracleWmsUtilitiesAuth": [
        "flext_oracle_wms._utilities.auth",
        "FlextOracleWmsUtilitiesAuth",
    ],
    "FlextOracleWmsUtilitiesClient": [
        "flext_oracle_wms._utilities.client",
        "FlextOracleWmsUtilitiesClient",
    ],
    "FlextOracleWmsUtilitiesDiscovery": [
        "flext_oracle_wms._utilities.discovery",
        "FlextOracleWmsUtilitiesDiscovery",
    ],
    "FlextOracleWmsUtilitiesFiltering": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsUtilitiesFiltering",
    ],
    "FlextOracleWmsUtilitiesHttpClient": [
        "flext_oracle_wms._utilities.http_client",
        "FlextOracleWmsUtilitiesHttpClient",
    ],
    "FlextOracleWmsValidationError": [
        "flext_oracle_wms.errors",
        "FlextOracleWmsValidationError",
    ],
    "_utilities": ["flext_oracle_wms._utilities", ""],
    "api": ["flext_oracle_wms.api", ""],
    "auth": ["flext_oracle_wms._utilities.auth", ""],
    "c": ["flext_oracle_wms.constants", "FlextOracleWmsConstants"],
    "client": ["flext_oracle_wms._utilities.client", ""],
    "constants": ["flext_oracle_wms.constants", ""],
    "create_flext_http_client": [
        "flext_oracle_wms.http_client",
        "create_flext_http_client",
    ],
    "d": ["flext_core", "d"],
    "discovery": ["flext_oracle_wms._utilities.discovery", ""],
    "e": ["flext_core", "e"],
    "errors": ["flext_oracle_wms.errors", ""],
    "filtering": ["flext_oracle_wms.filtering", ""],
    "h": ["flext_core", "h"],
    "http_client": ["flext_oracle_wms.http_client", ""],
    "m": ["flext_oracle_wms.models", "FlextOracleWmsModels"],
    "models": ["flext_oracle_wms.models", ""],
    "p": ["flext_oracle_wms.protocols", "FlextOracleWmsProtocols"],
    "protocols": ["flext_oracle_wms.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "settings": ["flext_oracle_wms.settings", ""],
    "t": ["flext_oracle_wms.typings", "FlextOracleWmsTypes"],
    "typings": ["flext_oracle_wms.typings", ""],
    "u": ["flext_oracle_wms.utilities", "FlextOracleWmsUtilities"],
    "utilities": ["flext_oracle_wms.utilities", ""],
    "wms_api": ["flext_oracle_wms.wms_api", ""],
    "wms_auth": ["flext_oracle_wms.wms_auth", ""],
    "wms_client": ["flext_oracle_wms.wms_client", ""],
    "wms_discovery": ["flext_oracle_wms.wms_discovery", ""],
    "wms_exceptions": ["flext_oracle_wms.wms_exceptions", ""],
    "x": ["flext_core", "x"],
}

_EXPORTS: Sequence[str] = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FlextHttpClient",
    "FlextOracleWmsApi",
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsClient",
    "FlextOracleWmsClientSettings",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsExceptions",
    "FlextOracleWmsFilter",
    "FlextOracleWmsFilterOperator",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsModels",
    "FlextOracleWmsOperatorFilter",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsSettings",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
    "FlextOracleWmsValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_utilities",
    "api",
    "auth",
    "c",
    "client",
    "constants",
    "create_flext_http_client",
    "d",
    "discovery",
    "e",
    "errors",
    "filtering",
    "h",
    "http_client",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "wms_api",
    "wms_auth",
    "wms_client",
    "wms_discovery",
    "wms_exceptions",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
