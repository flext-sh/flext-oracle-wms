# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".complete_mock_pipeline": ("CompleteMockPipeline",),
        ".oracle_wms_complete_discovery": ("OracleWmsCompleteDiscovery",),
        ".oracle_wms_focused_discovery": ("FocusedOracleWmsDiscovery",),
        ".oracle_wms_optimized_discovery": ("OptimizedOracleWmsDiscovery",),
        ".sitecustomize": ("sitecustomize",),
        ".test_api": ("test_api",),
        ".test_authentication": ("TestsFlextOracleWmsAuthentication",),
        ".test_authentication_core": ("TestsFlextOracleWmsAuthenticationCore",),
        ".test_client": ("TestsFlextOracleWmsClient",),
        ".test_client_class": ("TestsFlextOracleWmsClientClass",),
        ".test_client_core": ("TestsFlextOracleWmsClientCore",),
        ".test_config": ("TestsFlextOracleWmsConfig",),
        ".test_config_module": ("TestsFlextOracleWmsConfigModule",),
        ".test_connection": ("TestsFlextOracleWmsConnection",),
        ".test_constants": ("test_constants",),
        ".test_declarative": ("TestsFlextOracleWmsDeclarative",),
        ".test_discovery": ("TestsFlextOracleWmsDiscovery",),
        ".test_filtering": ("TestsFlextOracleWmsFiltering",),
        ".test_helpers": ("TestsFlextOracleWmsHelpers",),
        ".test_helpers_core": ("TestsFlextOracleWmsHelpersCore",),
        ".test_models": ("TestsFlextOracleWmsModelsUnit",),
        ".test_schema_dynamic": ("TestsFlextOracleWmsSchemaDynamic",),
        ".test_singer_flattening": ("TestsFlextOracleWmsSingerFlattening",),
        ".test_unified_config": ("TestsFlextOracleWmsUnifiedConfig",),
        ".test_wms_api": ("test_wms_api",),
        ".test_wms_client": ("test_wms_client",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
