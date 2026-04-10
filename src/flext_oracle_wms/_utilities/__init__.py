# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".auth": ("FlextOracleWmsUtilitiesAuth",),
        ".client": ("FlextOracleWmsUtilitiesClient",),
        ".discovery": (
            "DISCOVERY_FAILURE",
            "DISCOVERY_SUCCESS",
            "FlextOracleWmsUtilitiesDiscovery",
        ),
        ".filtering": (
            "FlextOracleWmsOperatorFilter",
            "FlextOracleWmsUtilitiesFiltering",
        ),
        ".http_client": ("FlextOracleWmsUtilitiesHttpClient",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
