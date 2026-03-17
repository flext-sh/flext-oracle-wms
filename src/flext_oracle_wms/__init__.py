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

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

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
    from flext_oracle_wms.constants import (
        FlextOracleWmsConstants,
        FlextOracleWmsConstants as c,
    )
    from flext_oracle_wms.filtering import (
        FilterOperator,
        FlextOracleWmsFilter,
        OperatorFilter,
    )
    from flext_oracle_wms.http_client import FlextHttpClient, create_flext_http_client
    from flext_oracle_wms.protocols import FlextOracleWmsProtocols, p
    from flext_oracle_wms.settings import (
        FlextOracleWmsClientSettings,
        FlextOracleWmsSettings,
    )
    from flext_oracle_wms.typings import FlextOracleWmsTypes, t
    from flext_oracle_wms.utilities import FlextOracleWmsUtilities, u
    from flext_oracle_wms.wms_api import (
        FLEXT_ORACLE_WMS_APIS,
        FlextOracleWmsApi,
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
        FlextOracleWmsExceptions as e,
        FlextOracleWmsInventoryError,
        FlextOracleWmsPickingError,
        FlextOracleWmsProcessingError,
        FlextOracleWmsSchemaError,
        FlextOracleWmsSchemaFlatteningError,
        FlextOracleWmsSettingsurationError,
        FlextOracleWmsShipmentError,
        FlextOracleWmsValidationError,
    )
    from flext_oracle_wms.wms_models import (
        FlextOracleWmsModels,
        FlextOracleWmsModels as m,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "DISCOVERY_FAILURE": ("flext_oracle_wms.wms_discovery", "DISCOVERY_FAILURE"),
    "DISCOVERY_SUCCESS": ("flext_oracle_wms.wms_discovery", "DISCOVERY_SUCCESS"),
    "FLEXT_ORACLE_WMS_APIS": ("flext_oracle_wms.wms_api", "FLEXT_ORACLE_WMS_APIS"),
    "FilterOperator": ("flext_oracle_wms.filtering", "FilterOperator"),
    "FlextHttpClient": ("flext_oracle_wms.http_client", "FlextHttpClient"),
    "FlextOracleWmsApi": ("flext_oracle_wms.wms_api", "FlextOracleWmsApi"),
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
    "FlextOracleWmsInventoryError": (
        "flext_oracle_wms.wms_exceptions",
        "FlextOracleWmsInventoryError",
    ),
    "FlextOracleWmsModels": ("flext_oracle_wms.wms_models", "FlextOracleWmsModels"),
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
    "OperatorFilter": ("flext_oracle_wms.filtering", "OperatorFilter"),
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
    "e": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsExceptions"),
    "m": ("flext_oracle_wms.wms_models", "FlextOracleWmsModels"),
    "p": ("flext_oracle_wms.protocols", "p"),
    "t": ("flext_oracle_wms.typings", "t"),
    "u": ("flext_oracle_wms.utilities", "u"),
}

__all__ = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FLEXT_ORACLE_WMS_APIS",
    "FilterOperator",
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
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsModels",
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
    "OperatorFilter",
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
    "e",
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
