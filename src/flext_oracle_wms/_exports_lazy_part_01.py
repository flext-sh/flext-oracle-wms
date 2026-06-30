# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_ORACLE_WMS_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._utilities.auth": ("FlextOracleWmsUtilitiesAuth",),
        "._utilities.client": ("FlextOracleWmsUtilitiesClient",),
        "._utilities.discovery": ("FlextOracleWmsUtilitiesDiscovery",),
        "._utilities.filtering": ("FlextOracleWmsUtilitiesFiltering",),
        "._utilities.http_client": ("FlextOracleWmsUtilitiesHttpClient",),
        ".api": (
            "FlextOracleWmsApi",
            "oracle_wms",
        ),
        ".constants": (
            "FlextOracleWmsConstants",
            "c",
        ),
        ".models": (
            "FlextOracleWmsModels",
            "m",
        ),
        ".protocols": (
            "FlextOracleWmsProtocols",
            "p",
        ),
        ".settings": ("FlextOracleWmsSettings",),
        ".typings": (
            "FlextOracleWmsTypes",
            "t",
        ),
        ".utilities": (
            "FlextOracleWmsUtilities",
            "u",
        ),
    },
)

__all__: list[str] = ["FLEXT_ORACLE_WMS_LAZY_IMPORTS_PART_01"]
