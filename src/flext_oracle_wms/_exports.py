# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._utilities": ("_utilities",),
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
        "flext_api": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)

FLEXT_ORACLE_WMS_LAZY_IMPORTS = merge_lazy_imports(
    (),
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
    module_name="flext_oracle_wms",
)

__all__: list[str] = ["FLEXT_ORACLE_WMS_LAZY_IMPORTS"]
