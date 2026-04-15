# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".complete_mock_pipeline": ("complete_mock_pipeline",),
        ".oracle_wms_complete_discovery": ("oracle_wms_complete_discovery",),
        ".oracle_wms_focused_discovery": ("oracle_wms_focused_discovery",),
        ".oracle_wms_optimized_discovery": ("oracle_wms_optimized_discovery",),
        ".sitecustomize": ("sitecustomize",),
        ".test_api": ("test_api",),
        ".test_authentication": ("test_authentication",),
        ".test_authentication_core": ("test_authentication_core",),
        ".test_client": ("test_client",),
        ".test_client_class": ("test_client_class",),
        ".test_client_core": ("test_client_core",),
        ".test_config": ("test_config",),
        ".test_config_module": ("test_config_module",),
        ".test_connection": ("test_connection",),
        ".test_constants": ("test_constants",),
        ".test_declarative": ("test_declarative",),
        ".test_discovery": ("test_discovery",),
        ".test_filtering": ("test_filtering",),
        ".test_helpers": ("test_helpers",),
        ".test_helpers_core": ("test_helpers_core",),
        ".test_models": ("test_models",),
        ".test_schema_dynamic": ("test_schema_dynamic",),
        ".test_singer_flattening": ("test_singer_flattening",),
        ".test_unified_config": ("test_unified_config",),
        ".test_wms_api": ("test_wms_api",),
        ".test_wms_client": ("test_wms_client",),
        "flext_oracle_wms": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
