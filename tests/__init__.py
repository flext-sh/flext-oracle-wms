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
    from tests.unit.test_api import TestFlextOracleWmsApi
    from tests.unit.test_authentication import (
        TestAuthenticationConfig,
        TestAuthenticationMethod,
        TestAuthenticator,
    )
    from tests.unit.test_authentication_core import (
        TestAuthenticationConfigCore,
        TestAuthenticationMethodCore,
        TestAuthenticatorCore,
    )
    from tests.unit.test_client import TestClientSimpleNew
    from tests.unit.test_client_core import TestFlextOracleWmsClientCore, TestGetLogger
    from tests.unit.test_constants import Testc
    from tests.unit.test_declarative import (
        TestAutomationApisIntegration,
        TestErrorHandlingIntegration,
        TestLgfApiV10Integration,
        TestOracleWmsDeclarativeIntegration,
        TestPerformanceIntegration,
    )
    from tests.unit.test_discovery import (
        TestDiscoveryConstants,
        TestEndpointDiscoveryStrategyEnum,
        TestFlextOracleWmsEntityDiscovery,
    )
    from tests.unit.test_filtering import (
        TestApplyOperator,
        TestConvenienceFunctions,
        TestErrorHandling,
        TestFactoryFunction,
        TestFilterValidation,
        TestFlextOracleWmsFilterConstruction,
        TestMatchesCondition,
        TestNestedValueAccess,
        TestNormalize,
        TestPerformanceAndEdgeCases,
        TestRecordFiltering,
        TestRecordSorting,
    )
    from tests.unit.test_helpers import TestFlextOracleWmsUtilities
    from tests.unit.test_helpers_core import TestFlextOracleWmsUtilitiesCore
    from tests.unit.test_schema_dynamic import (
        TestNestedConstants,
        TestSchemaConstants,
        TestWmsEnums,
    )
    from tests.unit.test_singer_flattening import (
        TestFlextOracleWmsApiResponse,
        TestFlextOracleWmsEntity,
    )
    from tests.unit.test_unified_config import TestFlextOracleWmsSettings
    from tests.unit.test_wms_api import TestFlextOracleWmsApiWms
    from tests.unit.test_wms_client import TestFlextOracleWmsClient
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
            ".unit.test_api": ("TestFlextOracleWmsApi",),
            ".unit.test_authentication": (
                "TestAuthenticationConfig",
                "TestAuthenticationMethod",
                "TestAuthenticator",
            ),
            ".unit.test_authentication_core": (
                "TestAuthenticationConfigCore",
                "TestAuthenticationMethodCore",
                "TestAuthenticatorCore",
            ),
            ".unit.test_client": ("TestClientSimpleNew",),
            ".unit.test_client_core": (
                "TestFlextOracleWmsClientCore",
                "TestGetLogger",
            ),
            ".unit.test_constants": ("Testc",),
            ".unit.test_declarative": (
                "TestAutomationApisIntegration",
                "TestErrorHandlingIntegration",
                "TestLgfApiV10Integration",
                "TestOracleWmsDeclarativeIntegration",
                "TestPerformanceIntegration",
            ),
            ".unit.test_discovery": (
                "TestDiscoveryConstants",
                "TestEndpointDiscoveryStrategyEnum",
                "TestFlextOracleWmsEntityDiscovery",
            ),
            ".unit.test_filtering": (
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
            ".unit.test_helpers": ("TestFlextOracleWmsUtilities",),
            ".unit.test_helpers_core": ("TestFlextOracleWmsUtilitiesCore",),
            ".unit.test_schema_dynamic": (
                "TestNestedConstants",
                "TestSchemaConstants",
                "TestWmsEnums",
            ),
            ".unit.test_singer_flattening": (
                "TestFlextOracleWmsApiResponse",
                "TestFlextOracleWmsEntity",
            ),
            ".unit.test_unified_config": ("TestFlextOracleWmsSettings",),
            ".unit.test_wms_api": ("TestFlextOracleWmsApiWms",),
            ".unit.test_wms_client": ("TestFlextOracleWmsClient",),
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
    "TestApplyOperator",
    "TestAuthenticationConfig",
    "TestAuthenticationConfigCore",
    "TestAuthenticationMethod",
    "TestAuthenticationMethodCore",
    "TestAuthenticator",
    "TestAuthenticatorCore",
    "TestAutomationApisIntegration",
    "TestClientSimpleNew",
    "TestConvenienceFunctions",
    "TestDiscoveryConstants",
    "TestEndpointDiscoveryStrategyEnum",
    "TestErrorHandling",
    "TestErrorHandlingIntegration",
    "TestFactoryFunction",
    "TestFilterValidation",
    "TestFlextOracleWmsApi",
    "TestFlextOracleWmsApiResponse",
    "TestFlextOracleWmsApiWms",
    "TestFlextOracleWmsClient",
    "TestFlextOracleWmsClientCore",
    "TestFlextOracleWmsEntity",
    "TestFlextOracleWmsEntityDiscovery",
    "TestFlextOracleWmsFilterConstruction",
    "TestFlextOracleWmsSettings",
    "TestFlextOracleWmsUtilities",
    "TestFlextOracleWmsUtilitiesCore",
    "TestGetLogger",
    "TestLgfApiV10Integration",
    "TestMatchesCondition",
    "TestNestedConstants",
    "TestNestedValueAccess",
    "TestNormalize",
    "TestOracleWmsDeclarativeIntegration",
    "TestPerformanceAndEdgeCases",
    "TestPerformanceIntegration",
    "TestRecordFiltering",
    "TestRecordSorting",
    "TestSchemaConstants",
    "TestWmsEnums",
    "Testc",
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
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
