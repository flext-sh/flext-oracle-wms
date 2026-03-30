# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Oracle WMS utilities subpackage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_oracle_wms._utilities import (
        auth,
        client,
        discovery,
        filtering,
        http_client,
    )
    from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth
    from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient
    from flext_oracle_wms._utilities.discovery import (
        DISCOVERY_FAILURE,
        DISCOVERY_SUCCESS,
        FlextOracleWmsUtilitiesDiscovery,
    )
    from flext_oracle_wms._utilities.filtering import (
        FlextOracleWmsDataValidationError,
        FlextOracleWmsFilterOperator,
        FlextOracleWmsOperatorFilter,
        FlextOracleWmsUtilitiesFiltering,
    )
    from flext_oracle_wms._utilities.http_client import (
        FlextOracleWmsUtilitiesHttpClient,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "DISCOVERY_FAILURE": ["flext_oracle_wms._utilities.discovery", "DISCOVERY_FAILURE"],
    "DISCOVERY_SUCCESS": ["flext_oracle_wms._utilities.discovery", "DISCOVERY_SUCCESS"],
    "FlextOracleWmsDataValidationError": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsDataValidationError",
    ],
    "FlextOracleWmsFilterOperator": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsFilterOperator",
    ],
    "FlextOracleWmsOperatorFilter": [
        "flext_oracle_wms._utilities.filtering",
        "FlextOracleWmsOperatorFilter",
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
    "auth": ["flext_oracle_wms._utilities.auth", ""],
    "client": ["flext_oracle_wms._utilities.client", ""],
    "discovery": ["flext_oracle_wms._utilities.discovery", ""],
    "filtering": ["flext_oracle_wms._utilities.filtering", ""],
    "http_client": ["flext_oracle_wms._utilities.http_client", ""],
}

__all__ = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsFilterOperator",
    "FlextOracleWmsOperatorFilter",
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
    "auth",
    "client",
    "discovery",
    "filtering",
    "http_client",
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
