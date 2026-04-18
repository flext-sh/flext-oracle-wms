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
        ".test_api": ("TestFlextOracleWmsApi",),
        ".test_authentication": (
            "TestAuthenticationConfig",
            "TestAuthenticationMethod",
            "TestAuthenticator",
        ),
        ".test_authentication_core": (
            "TestAuthenticationConfigCore",
            "TestAuthenticationMethodCore",
            "TestAuthenticatorCore",
        ),
        ".test_client": ("TestClientSimpleNew",),
        ".test_client_class": ("test_client_class",),
        ".test_client_core": (
            "TestFlextOracleWmsClientCore",
            "TestGetLogger",
        ),
        ".test_config": ("test_config",),
        ".test_config_module": ("test_config_module",),
        ".test_connection": ("test_connection",),
        ".test_constants": ("Testc",),
        ".test_declarative": (
            "TestAutomationApisIntegration",
            "TestErrorHandlingIntegration",
            "TestLgfApiV10Integration",
            "TestOracleWmsDeclarativeIntegration",
            "TestPerformanceIntegration",
        ),
        ".test_discovery": (
            "TestDiscoveryConstants",
            "TestEndpointDiscoveryStrategyEnum",
            "TestFlextOracleWmsEntityDiscovery",
        ),
        ".test_filtering": (
            "TestApplyOperator",
            "TestConvenienceFunctions",
            "TestErrorHandling",
            "TestFactoryFunction",
            "TestFilterValidation",
            "TestFlextOracleWmsFilterConstruction",
            "TestMatchesCondition",
            "TestNestedValueAccess",
            "TestNormalize",
            "TestPerformanceAndEdgeCases",
            "TestRecordFiltering",
            "TestRecordSorting",
        ),
        ".test_helpers": ("TestFlextOracleWmsUtilities",),
        ".test_helpers_core": ("TestFlextOracleWmsUtilitiesCore",),
        ".test_models": ("test_models",),
        ".test_schema_dynamic": (
            "TestNestedConstants",
            "TestWmsEnums",
        ),
        ".test_singer_flattening": (
            "TestFlextOracleWmsApiResponse",
            "TestFlextOracleWmsEntity",
        ),
        ".test_unified_config": ("TestFlextOracleWmsSettings",),
        ".test_wms_api": ("TestFlextOracleWmsApiWms",),
        ".test_wms_client": ("TestFlextOracleWmsClient",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
