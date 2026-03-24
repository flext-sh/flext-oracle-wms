# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Oracle WMS - Enterprise Oracle Warehouse Management System Integration.

 Oracle WMS integration with Clean Architecture, railway-oriented error handling,
and domain-driven design. Provides inventory, shipment, and picking operations with OAuth2 auth.

Usage: from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_oracle_wms.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_oracle_wms.api import FlextOracleWmsApi
    from flext_oracle_wms.constants import (
        FlextOracleWmsConstants,
        FlextOracleWmsConstants as c,
    )
    from flext_oracle_wms.filtering import (
        FlextOracleWmsFilter,
        FlextOracleWmsFilterOperator,
        FlextOracleWmsOperatorFilter,
    )
    from flext_oracle_wms.http_client import FlextHttpClient, create_flext_http_client
    from flext_oracle_wms.models import FlextOracleWmsModels, FlextOracleWmsModels as m
    from flext_oracle_wms.protocols import (
        FlextOracleWmsProtocols,
        FlextOracleWmsProtocols as p,
    )
    from flext_oracle_wms.settings import (
        FlextOracleWmsClientSettings,
        FlextOracleWmsSettings,
    )
    from flext_oracle_wms.typings import (
        FlextOracleWmsTypes,
        FlextOracleWmsTypes as t,
        HttpJsonObject,
    )
    from flext_oracle_wms.utilities import (
        FlextOracleWmsUtilities,
        FlextOracleWmsUtilities as u,
    )
    from flext_oracle_wms.wms_api import (
        FLEXT_ORACLE_WMS_APIS,
        FlextOracleWmsApiEndpoint,
    )
    from flext_oracle_wms.wms_auth import (
        FlextOracleWmsAuthenticator,
        FlextOracleWmsAuthSettings,
        create_oracle_wms_client,
    )
    from flext_oracle_wms.wms_client import FlextOracleWmsClient
    from flext_oracle_wms.wms_discovery import (
        DISCOVERY_FAILURE,
        DISCOVERY_SUCCESS,
        FlextOracleWmsEntityDiscovery,
    )
    from flext_oracle_wms.wms_exceptions import (
        FlextOracleWmsApiError,
        FlextOracleWmsAuthenticationError,
        FlextOracleWmsConnectionError,
        FlextOracleWmsDataValidationError,
        FlextOracleWmsEntityNotFoundError,
        FlextOracleWmsError,
        FlextOracleWmsExceptions,
        FlextOracleWmsInventoryError,
        FlextOracleWmsPickingError,
        FlextOracleWmsProcessingError,
        FlextOracleWmsSchemaError,
        FlextOracleWmsSchemaFlatteningError,
        FlextOracleWmsSettingsurationError,
        FlextOracleWmsShipmentError,
        FlextOracleWmsValidationError,
    )

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "DISCOVERY_FAILURE": ("flext_oracle_wms.wms_discovery", "DISCOVERY_FAILURE"),
    "DISCOVERY_SUCCESS": ("flext_oracle_wms.wms_discovery", "DISCOVERY_SUCCESS"),
    "FLEXT_ORACLE_WMS_APIS": ("flext_oracle_wms.wms_api", "FLEXT_ORACLE_WMS_APIS"),
    "FlextHttpClient": ("flext_oracle_wms.http_client", "FlextHttpClient"),
    "FlextOracleWmsApi": ("flext_oracle_wms.api", "FlextOracleWmsApi"),
    "FlextOracleWmsApiEndpoint": (
        "flext_oracle_wms.wms_api",
        "FlextOracleWmsApiEndpoint",
    ),
    "FlextOracleWmsApiError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsApiError",
    ),
    "FlextOracleWmsAuthSettings": (
        "flext_oracle_wms.wms_auth",
        "FlextOracleWmsAuthSettings",
    ),
    "FlextOracleWmsAuthenticationError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsAuthenticationError",
    ),
    "FlextOracleWmsAuthenticator": (
        "flext_oracle_wms.wms_auth",
        "FlextOracleWmsAuthenticator",
    ),
    "FlextOracleWmsClient": ("flext_oracle_wms.wms_client", "FlextOracleWmsClient"),
    "FlextOracleWmsClientSettings": (
        "flext_oracle_wms.settings",
        "FlextOracleWmsClientSettings",
    ),
    "FlextOracleWmsConnectionError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsConnectionError",
    ),
    "FlextOracleWmsConstants": (
        "flext_oracle_wms.constants",
        "FlextOracleWmsConstants",
    ),
    "FlextOracleWmsDataValidationError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsDataValidationError",
    ),
    "FlextOracleWmsEntityDiscovery": (
        "flext_oracle_wms.wms_discovery",
        "FlextOracleWmsEntityDiscovery",
    ),
    "FlextOracleWmsEntityNotFoundError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsEntityNotFoundError",
    ),
    "FlextOracleWmsError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsError"),
    "FlextOracleWmsExceptions": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsExceptions",
    ),
    "FlextOracleWmsFilter": ("flext_oracle_wms.filtering", "FlextOracleWmsFilter"),
    "FlextOracleWmsFilterOperator": (
        "flext_oracle_wms.filtering",
        "FlextOracleWmsFilterOperator",
    ),
    "FlextOracleWmsInventoryError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsInventoryError",
    ),
    "FlextOracleWmsModels": ("flext_oracle_wms.models", "FlextOracleWmsModels"),
    "FlextOracleWmsOperatorFilter": (
        "flext_oracle_wms.filtering",
        "FlextOracleWmsOperatorFilter",
    ),
    "FlextOracleWmsPickingError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsPickingError",
    ),
    "FlextOracleWmsProcessingError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsProcessingError",
    ),
    "FlextOracleWmsProtocols": (
        "flext_oracle_wms.protocols",
        "FlextOracleWmsProtocols",
    ),
    "FlextOracleWmsSchemaError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsSchemaError",
    ),
    "FlextOracleWmsSchemaFlatteningError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsSchemaFlatteningError",
    ),
    "FlextOracleWmsSettings": ("flext_oracle_wms.settings", "FlextOracleWmsSettings"),
    "FlextOracleWmsSettingsurationError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsSettingsurationError",
    ),
    "FlextOracleWmsShipmentError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsShipmentError",
    ),
    "FlextOracleWmsTypes": ("flext_oracle_wms.typings", "FlextOracleWmsTypes"),
    "FlextOracleWmsUtilities": (
        "flext_oracle_wms.utilities",
        "FlextOracleWmsUtilities",
    ),
    "FlextOracleWmsValidationError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsValidationError",
    ),
    "HttpJsonObject": ("flext_oracle_wms.typings", "HttpJsonObject"),
    "__all__": ("flext_oracle_wms.__version__", "__all__"),
    "__author__": ("flext_oracle_wms.__version__", "__author__"),
    "__author_email__": ("flext_oracle_wms.__version__", "__author_email__"),
    "__description__": ("flext_oracle_wms.__version__", "__description__"),
    "__license__": ("flext_oracle_wms.__version__", "__license__"),
    "__title__": ("flext_oracle_wms.__version__", "__title__"),
    "__url__": ("flext_oracle_wms.__version__", "__url__"),
    "__version__": ("flext_oracle_wms.__version__", "__version__"),
    "__version_info__": ("flext_oracle_wms.__version__", "__version_info__"),
    "c": ("flext_oracle_wms.constants", "FlextOracleWmsConstants"),
    "create_flext_http_client": (
        "flext_oracle_wms.http_client",
        "create_flext_http_client",
    ),
    "create_oracle_wms_client": (
        "flext_oracle_wms.wms_auth",
        "create_oracle_wms_client",
    ),
    "d": ("flext_core", "d"),
    "e": ("flext_core", "e"),
    "h": ("flext_core", "h"),
    "m": ("flext_oracle_wms.models", "FlextOracleWmsModels"),
    "p": ("flext_oracle_wms.protocols", "FlextOracleWmsProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "t": ("flext_oracle_wms.typings", "FlextOracleWmsTypes"),
    "u": ("flext_oracle_wms.utilities", "FlextOracleWmsUtilities"),
    "x": ("flext_core", "x"),
}

__all__ = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FLEXT_ORACLE_WMS_APIS",
    "FlextHttpClient",
    "FlextOracleWmsApi",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthSettings",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsClient",
    "FlextOracleWmsClientSettings",
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
    "FlextOracleWmsSettingsurationError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsValidationError",
    "HttpJsonObject",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "create_flext_http_client",
    "create_oracle_wms_client",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
