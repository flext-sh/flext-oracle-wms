# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._utilities.auth import (
        FlextOracleWmsUtilitiesAuth as FlextOracleWmsUtilitiesAuth,
    )
    from flext_oracle_wms._utilities.client import (
        FlextOracleWmsUtilitiesClient as FlextOracleWmsUtilitiesClient,
    )
    from flext_oracle_wms._utilities.discovery import (
        FlextOracleWmsUtilitiesDiscovery as FlextOracleWmsUtilitiesDiscovery,
    )
    from flext_oracle_wms._utilities.filtering import (
        FlextOracleWmsUtilitiesFiltering as FlextOracleWmsUtilitiesFiltering,
    )
    from flext_oracle_wms._utilities.http_client import (
        FlextOracleWmsUtilitiesHttpClient as FlextOracleWmsUtilitiesHttpClient,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".auth": ("FlextOracleWmsUtilitiesAuth",),
        ".client": ("FlextOracleWmsUtilitiesClient",),
        ".discovery": ("FlextOracleWmsUtilitiesDiscovery",),
        ".filtering": ("FlextOracleWmsUtilitiesFiltering",),
        ".http_client": ("FlextOracleWmsUtilitiesHttpClient",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
