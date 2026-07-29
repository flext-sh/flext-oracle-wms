# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .auth import FlextOracleWmsUtilitiesAuth as FlextOracleWmsUtilitiesAuth
    from .client import FlextOracleWmsUtilitiesClient as FlextOracleWmsUtilitiesClient
    from .discovery import (
        FlextOracleWmsUtilitiesDiscovery as FlextOracleWmsUtilitiesDiscovery,
    )
    from .filtering import (
        FlextOracleWmsUtilitiesFiltering as FlextOracleWmsUtilitiesFiltering,
    )
    from .http_client import (
        FlextOracleWmsUtilitiesHttpClient as FlextOracleWmsUtilitiesHttpClient,
    )

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".auth": ("FlextOracleWmsUtilitiesAuth",),
    ".client": ("FlextOracleWmsUtilitiesClient",),
    ".discovery": ("FlextOracleWmsUtilitiesDiscovery",),
    ".filtering": ("FlextOracleWmsUtilitiesFiltering",),
    ".http_client": ("FlextOracleWmsUtilitiesHttpClient",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
