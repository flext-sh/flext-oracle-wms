# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td, tf, tk, tm, tv

    from flext_oracle_wms import d, e, h, r, s, x
    from tests.constants import TestsFlextOracleWmsConstants, c
    from tests.models import TestsFlextOracleWmsModels, m
    from tests.protocols import TestsFlextOracleWmsProtocols, p
    from tests.typings import TestsFlextOracleWmsTypes, t
    from tests.unit.complete_mock_pipeline import CompleteMockPipeline
    from tests.unit.oracle_wms_complete_discovery import OracleWmsCompleteDiscovery
    from tests.unit.oracle_wms_focused_discovery import FocusedOracleWmsDiscovery
    from tests.unit.oracle_wms_optimized_discovery import OptimizedOracleWmsDiscovery
    from tests.unit.test_api import TestsFlextOracleWmsApi
    from tests.unit.test_authentication import TestsFlextOracleWmsAuthentication
    from tests.unit.test_authentication_core import (
        TestsFlextOracleWmsAuthenticationCore,
    )
    from tests.unit.test_client import TestsFlextOracleWmsClient
    from tests.unit.test_client_core import TestsFlextOracleWmsClientCore
    from tests.unit.test_constants import TestsFlextOracleWmsConstantsUnit
    from tests.unit.test_declarative import TestsFlextOracleWmsDeclarative
    from tests.unit.test_discovery import TestsFlextOracleWmsDiscovery
    from tests.unit.test_filtering import TestsFlextOracleWmsFiltering
    from tests.unit.test_helpers import TestsFlextOracleWmsHelpers
    from tests.unit.test_helpers_core import TestsFlextOracleWmsHelpersCore
    from tests.unit.test_schema_dynamic import TestsFlextOracleWmsSchemaDynamic
    from tests.unit.test_singer_flattening import TestsFlextOracleWmsSingerFlattening
    from tests.unit.test_unified_config import TestsFlextOracleWmsUnifiedConfig
    from tests.unit.test_wms_api import TestsFlextOracleWmsWmsApi
    from tests.unit.test_wms_client import TestsFlextOracleWmsWmsClient
    from tests.utilities import TestsFlextOracleWmsUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
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
            ".typings": (
                "TestsFlextOracleWmsTypes",
                "t",
            ),
            ".unit.complete_mock_pipeline": ("CompleteMockPipeline",),
            ".unit.oracle_wms_complete_discovery": ("OracleWmsCompleteDiscovery",),
            ".unit.oracle_wms_focused_discovery": ("FocusedOracleWmsDiscovery",),
            ".unit.oracle_wms_optimized_discovery": ("OptimizedOracleWmsDiscovery",),
            ".unit.test_api": ("TestsFlextOracleWmsApi",),
            ".unit.test_authentication": ("TestsFlextOracleWmsAuthentication",),
            ".unit.test_authentication_core": (
                "TestsFlextOracleWmsAuthenticationCore",
            ),
            ".unit.test_client": ("TestsFlextOracleWmsClient",),
            ".unit.test_client_core": ("TestsFlextOracleWmsClientCore",),
            ".unit.test_constants": ("TestsFlextOracleWmsConstantsUnit",),
            ".unit.test_declarative": ("TestsFlextOracleWmsDeclarative",),
            ".unit.test_discovery": ("TestsFlextOracleWmsDiscovery",),
            ".unit.test_filtering": ("TestsFlextOracleWmsFiltering",),
            ".unit.test_helpers": ("TestsFlextOracleWmsHelpers",),
            ".unit.test_helpers_core": ("TestsFlextOracleWmsHelpersCore",),
            ".unit.test_schema_dynamic": ("TestsFlextOracleWmsSchemaDynamic",),
            ".unit.test_singer_flattening": ("TestsFlextOracleWmsSingerFlattening",),
            ".unit.test_unified_config": ("TestsFlextOracleWmsUnifiedConfig",),
            ".unit.test_wms_api": ("TestsFlextOracleWmsWmsApi",),
            ".unit.test_wms_client": ("TestsFlextOracleWmsWmsClient",),
            ".utilities": (
                "TestsFlextOracleWmsUtilities",
                "u",
            ),
            "flext_oracle_wms": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "CompleteMockPipeline",
    "FocusedOracleWmsDiscovery",
    "OptimizedOracleWmsDiscovery",
    "OracleWmsCompleteDiscovery",
    "TestsFlextOracleWmsApi",
    "TestsFlextOracleWmsAuthentication",
    "TestsFlextOracleWmsAuthenticationCore",
    "TestsFlextOracleWmsClient",
    "TestsFlextOracleWmsClientCore",
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsConstantsUnit",
    "TestsFlextOracleWmsDeclarative",
    "TestsFlextOracleWmsDiscovery",
    "TestsFlextOracleWmsFiltering",
    "TestsFlextOracleWmsHelpers",
    "TestsFlextOracleWmsHelpersCore",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsSchemaDynamic",
    "TestsFlextOracleWmsSingerFlattening",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUnifiedConfig",
    "TestsFlextOracleWmsUtilities",
    "TestsFlextOracleWmsWmsApi",
    "TestsFlextOracleWmsWmsClient",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
