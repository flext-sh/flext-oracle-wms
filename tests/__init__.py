# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import (
        d as d,
        e as e,
        h as h,
        r as r,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        x as x,
    )
    from tests.base import (
        TestsFlextOracleWmsServiceBase as TestsFlextOracleWmsServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextOracleWmsConstants as TestsFlextOracleWmsConstants,
        c as c,
    )
    from tests.models import (
        TestsFlextOracleWmsModels as TestsFlextOracleWmsModels,
        m as m,
    )
    from tests.protocols import (
        TestsFlextOracleWmsProtocols as TestsFlextOracleWmsProtocols,
        p,
    )
    from tests.settings import (
        TestsFlextOracleWmsSettings as TestsFlextOracleWmsSettings,
    )
    from tests.typings import (
        TestsFlextOracleWmsTypes as TestsFlextOracleWmsTypes,
        t as t,
    )
    from tests.unit.complete_mock_pipeline import (
        CompleteMockPipeline as CompleteMockPipeline,
    )
    from tests.unit.oracle_wms_complete_discovery import (
        OracleWmsCompleteDiscovery as OracleWmsCompleteDiscovery,
        OracleWmsCompleteDiscoveryRunner as OracleWmsCompleteDiscoveryRunner,
    )
    from tests.unit.oracle_wms_focused_discovery import (
        FocusedOracleWmsDiscovery as FocusedOracleWmsDiscovery,
    )
    from tests.unit.oracle_wms_optimized_discovery import (
        OptimizedOracleWmsDiscovery as OptimizedOracleWmsDiscovery,
        OptimizedOracleWmsDiscoveryRunner as OptimizedOracleWmsDiscoveryRunner,
    )
    from tests.unit.test_api import TestsFlextOracleWmsApi as TestsFlextOracleWmsApi
    from tests.unit.test_authentication import (
        TestsFlextOracleWmsAuthentication as TestsFlextOracleWmsAuthentication,
    )
    from tests.unit.test_authentication_core import (
        TestsFlextOracleWmsAuthenticationCore as TestsFlextOracleWmsAuthenticationCore,
    )
    from tests.unit.test_client import (
        TestsFlextOracleWmsClient as TestsFlextOracleWmsClient,
    )
    from tests.unit.test_client_class import (
        TestsFlextOracleWmsClientClass as TestsFlextOracleWmsClientClass,
    )
    from tests.unit.test_client_core import (
        TestsFlextOracleWmsClientCore as TestsFlextOracleWmsClientCore,
    )
    from tests.unit.test_config import (
        TestsFlextOracleWmsConfig as TestsFlextOracleWmsConfig,
    )
    from tests.unit.test_config_module import (
        TestsFlextOracleWmsConfigModule as TestsFlextOracleWmsConfigModule,
    )
    from tests.unit.test_connection import (
        TestsFlextOracleWmsConnection as TestsFlextOracleWmsConnection,
    )
    from tests.unit.test_constants import (
        TestsFlextOracleWmsConstantsUnit as TestsFlextOracleWmsConstantsUnit,
    )
    from tests.unit.test_declarative import (
        TestsFlextOracleWmsDeclarative as TestsFlextOracleWmsDeclarative,
    )
    from tests.unit.test_discovery import (
        TestsFlextOracleWmsDiscovery as TestsFlextOracleWmsDiscovery,
    )
    from tests.unit.test_filtering import (
        TestsFlextOracleWmsFiltering as TestsFlextOracleWmsFiltering,
    )
    from tests.unit.test_helpers import (
        TestsFlextOracleWmsHelpers as TestsFlextOracleWmsHelpers,
    )
    from tests.unit.test_helpers_core import (
        TestsFlextOracleWmsHelpersCore as TestsFlextOracleWmsHelpersCore,
    )
    from tests.unit.test_models import (
        TestsFlextOracleWmsModelsUnit as TestsFlextOracleWmsModelsUnit,
    )
    from tests.unit.test_schema_dynamic import (
        TestsFlextOracleWmsSchemaDynamic as TestsFlextOracleWmsSchemaDynamic,
    )
    from tests.unit.test_singer_flattening import (
        TestsFlextOracleWmsSingerFlattening as TestsFlextOracleWmsSingerFlattening,
    )
    from tests.unit.test_unified_config import (
        TestsFlextOracleWmsUnifiedConfig as TestsFlextOracleWmsUnifiedConfig,
    )
    from tests.unit.test_wms_client import (
        TestsFlextOracleWmsWmsClient as TestsFlextOracleWmsWmsClient,
    )
    from tests.utilities import (
        TestsFlextOracleWmsUtilities as TestsFlextOracleWmsUtilities,
        u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map({
        ".base": ("TestsFlextOracleWmsServiceBase", "s"),
        ".conftest": ("conftest",),
        ".constants": ("TestsFlextOracleWmsConstants", "c"),
        ".models": ("TestsFlextOracleWmsModels", "m"),
        ".protocols": ("TestsFlextOracleWmsProtocols", "p"),
        ".settings": ("TestsFlextOracleWmsSettings",),
        ".typings": ("TestsFlextOracleWmsTypes", "t"),
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
        ".utilities": ("TestsFlextOracleWmsUtilities", "u"),
        "flext_tests": ("d", "e", "h", "r", "td", "tf", "tk", "tm", "tv", "x"),
    }),
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
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
