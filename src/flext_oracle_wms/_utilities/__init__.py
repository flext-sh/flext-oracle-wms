# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Utilities package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .auth import FlextOracleWmsUtilitiesAuth
    from .client import FlextOracleWmsUtilitiesClient
    from .discovery import FlextOracleWmsUtilitiesDiscovery
    from .filtering import FlextOracleWmsUtilitiesFiltering
    from .http_client import FlextOracleWmsUtilitiesHttpClient
__all__: tuple[str, ...] = (
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".auth": ("FlextOracleWmsUtilitiesAuth",),
            ".client": ("FlextOracleWmsUtilitiesClient",),
            ".discovery": ("FlextOracleWmsUtilitiesDiscovery",),
            ".filtering": ("FlextOracleWmsUtilitiesFiltering",),
            ".http_client": ("FlextOracleWmsUtilitiesHttpClient",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
