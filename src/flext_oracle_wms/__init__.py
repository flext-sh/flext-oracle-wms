"""FLEXT Oracle WMS - Enterprise Oracle Warehouse Management System Integration.

 Oracle WMS integration with Clean Architecture, railway-oriented error handling,
and domain-driven design. Provides inventory, shipment, and picking operations with OAuth2 auth.

Usage: from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import (
        FlextDecorators as d,
        FlextExceptions as FlextOracleWmsExceptions,
        FlextExceptions as e,
        FlextHandlers as h,
        r,
        x,
    )

    from flext_oracle_wms.__version__ import __version__, __version_info__
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
    from flext_oracle_wms.typings import t
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
    from flext_oracle_wms.wms_exceptions import (
        FlextOracleWmsApiError,
        FlextOracleWmsAuthenticationError,
        FlextOracleWmsEntityNotFoundError,
        FlextOracleWmsError,
        FlextOracleWmsInventoryError,
        FlextOracleWmsPickingError,
        FlextOracleWmsSchemaError,
        FlextOracleWmsSchemaFlatteningError,
        FlextOracleWmsShipmentError,
    )
    from flext_oracle_wms.wms_models import (
        FlextOracleWmsApiResponse,
        FlextOracleWmsEntity,
        FlextOracleWmsModels,
        FlextOracleWmsModels as m,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FLEXT_ORACLE_WMS_APIS": ("flext_oracle_wms.wms_api", "FLEXT_ORACLE_WMS_APIS"),
    "FlextOracleWmsApi": ("flext_oracle_wms.wms_api", "FlextOracleWmsApi"),
    "FlextOracleWmsApiError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsApiError"),
    "FlextOracleWmsApiResponse": (
        "flext_oracle_wms.wms_models",
        "FlextOracleWmsApiResponse",
    ),
    "FlextOracleWmsAuthSettings": (
        "flext_oracle_wms.wms_auth",
        "FlextOracleWmsAuthSettings",
    ),
    "FlextOracleWmsAuthenticationError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsAuthenticationError"),
    "FlextOracleWmsAuthenticator": (
        "flext_oracle_wms.wms_auth",
        "FlextOracleWmsAuthenticator",
    ),
    "FlextOracleWmsClient": ("flext_oracle_wms.wms_client", "FlextOracleWmsClient"),
    "FlextOracleWmsConstants": (
        "flext_oracle_wms.constants",
        "FlextOracleWmsConstants",
    ),
    "FlextOracleWmsEntity": ("flext_oracle_wms.wms_models", "FlextOracleWmsEntity"),
    "FlextOracleWmsEntityDiscovery": (
        "flext_oracle_wms.wms_discovery",
        "FlextOracleWmsEntityDiscovery",
    ),
    "FlextOracleWmsEntityNotFoundError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsEntityNotFoundError"),
    "FlextOracleWmsError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsError"),
    "FlextOracleWmsExceptions": ("flext_core", "FlextExceptions"),
    "FlextOracleWmsInventoryError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsInventoryError"),
    "FlextOracleWmsModels": ("flext_oracle_wms.wms_models", "FlextOracleWmsModels"),
    "FlextOracleWmsPickingError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsPickingError"),
    "FlextOracleWmsProtocols": (
        "flext_oracle_wms.protocols",
        "FlextOracleWmsProtocols",
    ),
    "FlextOracleWmsSchemaError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsSchemaError"),
    "FlextOracleWmsSchemaFlatteningError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsSchemaFlatteningError"),
    "FlextOracleWmsSettings": ("flext_oracle_wms.settings", "FlextOracleWmsSettings"),
    "FlextOracleWmsShipmentError": ("flext_oracle_wms.wms_exceptions", "FlextOracleWmsShipmentError"),
    "FlextOracleWmsUtilities": (
        "flext_oracle_wms.utilities",
        "FlextOracleWmsUtilities",
    ),
    "OracleWMSAuthMethod": ("flext_oracle_wms.constants", "OracleWMSAuthMethod"),
    "__version__": ("flext_oracle_wms.__version__", "__version__"),
    "__version_info__": ("flext_oracle_wms.__version__", "__version_info__"),
    "c": ("flext_oracle_wms.constants", "FlextOracleWmsConstants"),
    "create_oracle_wms_client": (
        "flext_oracle_wms.wms_auth",
        "create_oracle_wms_client",
    ),
    "d": ("flext_core", "FlextDecorators"),
    "e": ("flext_core", "FlextExceptions"),
    "h": ("flext_core", "FlextHandlers"),
    "m": ("flext_oracle_wms.wms_models", "FlextOracleWmsModels"),
    "p": ("flext_oracle_wms.protocols", "FlextOracleWmsProtocols"),
    "r": ("flext_core", "r"),
    "t": ("flext_oracle_wms.typings", "t"),
    "u": ("flext_oracle_wms.utilities", "FlextOracleWmsUtilities"),
    "x": ("flext_core", "x"),
}

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
    "h",
    "m",
    "p",
    "r",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
