# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Oracle WMS utilities subpackage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_oracle_wms._utilities.auth import *
    from flext_oracle_wms._utilities.client import *
    from flext_oracle_wms._utilities.discovery import *
    from flext_oracle_wms._utilities.filtering import *
    from flext_oracle_wms._utilities.http_client import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "DISCOVERY_FAILURE": "flext_oracle_wms._utilities.discovery",
    "DISCOVERY_SUCCESS": "flext_oracle_wms._utilities.discovery",
    "FlextOracleWmsDataValidationError": "flext_oracle_wms._utilities.filtering",
    "FlextOracleWmsFilterOperator": "flext_oracle_wms._utilities.filtering",
    "FlextOracleWmsOperatorFilter": "flext_oracle_wms._utilities.filtering",
    "FlextOracleWmsUtilitiesAuth": "flext_oracle_wms._utilities.auth",
    "FlextOracleWmsUtilitiesClient": "flext_oracle_wms._utilities.client",
    "FlextOracleWmsUtilitiesDiscovery": "flext_oracle_wms._utilities.discovery",
    "FlextOracleWmsUtilitiesFiltering": "flext_oracle_wms._utilities.filtering",
    "FlextOracleWmsUtilitiesHttpClient": "flext_oracle_wms._utilities.http_client",
    "auth": "flext_oracle_wms._utilities.auth",
    "client": "flext_oracle_wms._utilities.client",
    "discovery": "flext_oracle_wms._utilities.discovery",
    "filtering": "flext_oracle_wms._utilities.filtering",
    "http_client": "flext_oracle_wms._utilities.http_client",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
