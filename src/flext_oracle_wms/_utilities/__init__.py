# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Oracle WMS utilities subpackage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._utilities import (
        auth as auth,
        client as client,
        discovery as discovery,
        filtering as filtering,
        http_client as http_client,
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

_EXPORTS: Sequence[str] = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
