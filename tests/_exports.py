# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".base": (
            "TestsFlextOracleWmsServiceBase",
            "s",
        ),
        ".conftest": ("conftest",),
        ".constants": (
            "TestsFlextOracleWmsConstants",
            "c",
        ),
        ".models": (
            "TestsFlextOracleWmsModels",
            "m",
        ),
        ".protocols": (
            "TestsFlextOracleWmsProtocols",
            "p",
        ),
        ".settings": ("TestsFlextOracleWmsSettings",),
        ".typings": (
            "TestsFlextOracleWmsTypes",
            "t",
        ),
        ".unit": ("unit",),
        ".unit.complete_mock_pipeline": ("CompleteMockPipeline",),
        ".unit.oracle_wms_complete_discovery": (
            "OracleWmsCompleteDiscovery",
            "OracleWmsCompleteDiscoveryRunner",
        ),
        ".unit.oracle_wms_focused_discovery": ("FocusedOracleWmsDiscovery",),
        ".unit.oracle_wms_optimized_discovery": (
            "OptimizedOracleWmsDiscovery",
            "OptimizedOracleWmsDiscoveryRunner",
        ),
        ".unit.test_api": ("TestsFlextOracleWmsApi",),
        ".unit.test_authentication": ("TestsFlextOracleWmsAuthentication",),
        ".unit.test_authentication_core": ("TestsFlextOracleWmsAuthenticationCore",),
        ".unit.test_client": ("TestsFlextOracleWmsClient",),
        ".unit.test_client_class": ("TestsFlextOracleWmsClientClass",),
        ".unit.test_client_core": ("TestsFlextOracleWmsClientCore",),
        ".unit.test_config": ("TestsFlextOracleWmsConfig",),
        ".unit.test_config_module": ("TestsFlextOracleWmsConfigModule",),
        ".unit.test_connection": ("TestsFlextOracleWmsConnection",),
        ".unit.test_constants": ("TestsFlextOracleWmsConstantsUnit",),
        ".unit.test_declarative": ("TestsFlextOracleWmsDeclarative",),
        ".unit.test_discovery": ("TestsFlextOracleWmsDiscovery",),
        ".unit.test_filtering": ("TestsFlextOracleWmsFiltering",),
        ".unit.test_helpers": ("TestsFlextOracleWmsHelpers",),
        ".unit.test_helpers_core": ("TestsFlextOracleWmsHelpersCore",),
        ".unit.test_models": ("TestsFlextOracleWmsModelsUnit",),
        ".unit.test_schema_dynamic": ("TestsFlextOracleWmsSchemaDynamic",),
        ".unit.test_singer_flattening": ("TestsFlextOracleWmsSingerFlattening",),
        ".unit.test_unified_config": ("TestsFlextOracleWmsUnifiedConfig",),
        ".unit.test_wms_client": ("TestsFlextOracleWmsWmsClient",),
        ".utilities": (
            "TestsFlextOracleWmsUtilities",
            "u",
        ),
        "flext_tests": (
            "d",
            "e",
            "h",
            "r",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
            "x",
        ),
    },
)

TESTS_FLEXT_ORACLE_WMS_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    _LOCAL_LAZY_IMPORTS,
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name="tests",
)

__all__: list[str] = ["TESTS_FLEXT_ORACLE_WMS_LAZY_IMPORTS"]
