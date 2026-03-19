# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from . import unit as unit
    from .complete_mock_pipeline import CompleteMockPipeline
    from .conftest import (
        load_test_env,
        mock_config,
        pytest_configure,
        real_config,
        sample_entities,
        sample_entity_data,
    )
    from .constants import TestsFlextOracleWmsConstants, c
    from .models import TestsFlextOracleWmsModels, m, tm
    from .oracle_wms_complete_discovery import (
        OracleWmsCompleteDiscovery,
        run_complete_discovery,
    )
    from .oracle_wms_focused_discovery import FocusedOracleWmsDiscovery, main
    from .oracle_wms_optimized_discovery import (
        OptimizedOracleWmsDiscovery,
        run_optimized_discovery,
    )
    from .protocols import TestsFlextOracleWmsProtocols, p
    from .test_authentication_core import (
        TestAuthenticationConfig,
        TestAuthenticationMethod,
        TestAuthenticator,
    )
    from .test_client import TestClientSimpleNew
    from .test_client_class import (
        test_client_class_creation,
        test_client_config_access,
        test_client_has_discovery_methods,
        test_client_has_http_methods,
        test_client_has_lifecycle_methods,
        test_client_has_wms_operations,
        test_client_internal_state,
    )
    from .test_client_core import TestFlextOracleWmsClientCore, TestGetLogger
    from .test_config import (
        test_config_creation_valid,
        test_config_defaults_from_constants,
        test_config_enterprise_features,
        test_config_environment_from_url,
        test_config_optional_auth_fields,
        test_config_validate_config_success,
    )
    from .test_config_module import (
        test_config_creation,
        test_config_custom_values,
        test_config_reset_functionality,
        test_config_singleton_behavior,
        test_config_testing_factory,
        test_config_validation,
    )
    from .test_connection import test_real_connection
    from .test_declarative import (
        FlextOracleWmsApiCategory,
        FlextOracleWmsApiVersion,
        TestAutomationApisIntegration,
        TestErrorHandlingIntegration,
        TestLgfApiV10Integration,
        TestOracleWmsDeclarativeIntegration,
        TestPerformanceIntegration,
        env_config,
        find_env_file,
        load_env_config,
        logger,
        oracle_wms_client,
        pytestmark,
    )
    from .test_discovery import (
        TestDiscoveryConstants,
        TestEndpointDiscoveryStrategyEnum,
        TestFlextOracleWmsEntityDiscovery,
    )
    from .test_filtering import (
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
    from .test_helpers_core import TestFlextOracleWmsUtilities
    from .test_models import (
        test_api_response_creation,
        test_api_response_defaults,
        test_api_response_error,
        test_api_response_validate_response_failure,
        test_api_response_validate_response_success,
        test_api_response_with_nested_data,
        test_entity_creation,
        test_entity_defaults,
        test_entity_validate_entity_success,
        test_entity_validation_bad_endpoint_raises,
        test_entity_validation_empty_name_raises,
    )
    from .test_schema_dynamic import (
        TestFlextOracleWmsConstants,
        TestNestedConstants,
        TestWmsEnums,
    )
    from .test_singer_flattening import (
        TestFlextOracleWmsApiResponse,
        TestFlextOracleWmsEntity,
    )
    from .test_unified_config import TestFlextOracleWmsSettings
    from .typings import TestsFlextOracleWmsTypes, t
    from .unit.test_api import TestFlextOracleWmsApi
    from .unit.test_wms_client import TestFlextOracleWmsClient
    from .utilities import TestsFlextOracleWmsUtilities, u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "CompleteMockPipeline": ("tests.complete_mock_pipeline", "CompleteMockPipeline"),
    "FlextOracleWmsApiCategory": (
        "tests.test_declarative",
        "FlextOracleWmsApiCategory",
    ),
    "FlextOracleWmsApiVersion": ("tests.test_declarative", "FlextOracleWmsApiVersion"),
    "FocusedOracleWmsDiscovery": (
        "tests.oracle_wms_focused_discovery",
        "FocusedOracleWmsDiscovery",
    ),
    "OptimizedOracleWmsDiscovery": (
        "tests.oracle_wms_optimized_discovery",
        "OptimizedOracleWmsDiscovery",
    ),
    "OracleWmsCompleteDiscovery": (
        "tests.oracle_wms_complete_discovery",
        "OracleWmsCompleteDiscovery",
    ),
    "TestApplyOperator": ("tests.test_filtering", "TestApplyOperator"),
    "TestAuthenticationConfig": (
        "tests.test_authentication_core",
        "TestAuthenticationConfig",
    ),
    "TestAuthenticationMethod": (
        "tests.test_authentication_core",
        "TestAuthenticationMethod",
    ),
    "TestAuthenticator": ("tests.test_authentication_core", "TestAuthenticator"),
    "TestAutomationApisIntegration": (
        "tests.test_declarative",
        "TestAutomationApisIntegration",
    ),
    "TestClientSimpleNew": ("tests.test_client", "TestClientSimpleNew"),
    "TestConvenienceFunctions": ("tests.test_filtering", "TestConvenienceFunctions"),
    "TestDiscoveryConstants": ("tests.test_discovery", "TestDiscoveryConstants"),
    "TestEndpointDiscoveryStrategyEnum": (
        "tests.test_discovery",
        "TestEndpointDiscoveryStrategyEnum",
    ),
    "TestErrorHandling": ("tests.test_filtering", "TestErrorHandling"),
    "TestErrorHandlingIntegration": (
        "tests.test_declarative",
        "TestErrorHandlingIntegration",
    ),
    "TestFactoryFunction": ("tests.test_filtering", "TestFactoryFunction"),
    "TestFilterValidation": ("tests.test_filtering", "TestFilterValidation"),
    "TestFlextOracleWmsApi": ("tests.unit.test_api", "TestFlextOracleWmsApi"),
    "TestFlextOracleWmsApiResponse": (
        "tests.test_singer_flattening",
        "TestFlextOracleWmsApiResponse",
    ),
    "TestFlextOracleWmsClient": (
        "tests.unit.test_wms_client",
        "TestFlextOracleWmsClient",
    ),
    "TestFlextOracleWmsClientCore": (
        "tests.test_client_core",
        "TestFlextOracleWmsClientCore",
    ),
    "TestFlextOracleWmsConstants": (
        "tests.test_schema_dynamic",
        "TestFlextOracleWmsConstants",
    ),
    "TestFlextOracleWmsEntity": (
        "tests.test_singer_flattening",
        "TestFlextOracleWmsEntity",
    ),
    "TestFlextOracleWmsEntityDiscovery": (
        "tests.test_discovery",
        "TestFlextOracleWmsEntityDiscovery",
    ),
    "TestFlextOracleWmsFilterConstruction": (
        "tests.test_filtering",
        "TestFlextOracleWmsFilterConstruction",
    ),
    "TestFlextOracleWmsSettings": (
        "tests.test_unified_config",
        "TestFlextOracleWmsSettings",
    ),
    "TestFlextOracleWmsUtilities": (
        "tests.test_helpers_core",
        "TestFlextOracleWmsUtilities",
    ),
    "TestGetLogger": ("tests.test_client_core", "TestGetLogger"),
    "TestLgfApiV10Integration": ("tests.test_declarative", "TestLgfApiV10Integration"),
    "TestMatchesCondition": ("tests.test_filtering", "TestMatchesCondition"),
    "TestNestedConstants": ("tests.test_schema_dynamic", "TestNestedConstants"),
    "TestNestedValueAccess": ("tests.test_filtering", "TestNestedValueAccess"),
    "TestNormalize": ("tests.test_filtering", "TestNormalize"),
    "TestOracleWmsDeclarativeIntegration": (
        "tests.test_declarative",
        "TestOracleWmsDeclarativeIntegration",
    ),
    "TestPerformanceAndEdgeCases": (
        "tests.test_filtering",
        "TestPerformanceAndEdgeCases",
    ),
    "TestPerformanceIntegration": (
        "tests.test_declarative",
        "TestPerformanceIntegration",
    ),
    "TestRecordFiltering": ("tests.test_filtering", "TestRecordFiltering"),
    "TestRecordSorting": ("tests.test_filtering", "TestRecordSorting"),
    "TestWmsEnums": ("tests.test_schema_dynamic", "TestWmsEnums"),
    "TestsFlextOracleWmsConstants": ("tests.constants", "TestsFlextOracleWmsConstants"),
    "TestsFlextOracleWmsModels": ("tests.models", "TestsFlextOracleWmsModels"),
    "TestsFlextOracleWmsProtocols": ("tests.protocols", "TestsFlextOracleWmsProtocols"),
    "TestsFlextOracleWmsTypes": ("tests.typings", "TestsFlextOracleWmsTypes"),
    "TestsFlextOracleWmsUtilities": ("tests.utilities", "TestsFlextOracleWmsUtilities"),
    "c": ("tests.constants", "c"),
    "env_config": ("tests.test_declarative", "env_config"),
    "find_env_file": ("tests.test_declarative", "find_env_file"),
    "load_env_config": ("tests.test_declarative", "load_env_config"),
    "load_test_env": ("tests.conftest", "load_test_env"),
    "logger": ("tests.test_declarative", "logger"),
    "m": ("tests.models", "m"),
    "main": ("tests.oracle_wms_focused_discovery", "main"),
    "mock_config": ("tests.conftest", "mock_config"),
    "oracle_wms_client": ("tests.test_declarative", "oracle_wms_client"),
    "p": ("tests.protocols", "p"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "pytestmark": ("tests.test_declarative", "pytestmark"),
    "real_config": ("tests.conftest", "real_config"),
    "run_complete_discovery": (
        "tests.oracle_wms_complete_discovery",
        "run_complete_discovery",
    ),
    "run_optimized_discovery": (
        "tests.oracle_wms_optimized_discovery",
        "run_optimized_discovery",
    ),
    "sample_entities": ("tests.conftest", "sample_entities"),
    "sample_entity_data": ("tests.conftest", "sample_entity_data"),
    "t": ("tests.typings", "t"),
    "test_api_response_creation": ("tests.test_models", "test_api_response_creation"),
    "test_api_response_defaults": ("tests.test_models", "test_api_response_defaults"),
    "test_api_response_error": ("tests.test_models", "test_api_response_error"),
    "test_api_response_validate_response_failure": (
        "tests.test_models",
        "test_api_response_validate_response_failure",
    ),
    "test_api_response_validate_response_success": (
        "tests.test_models",
        "test_api_response_validate_response_success",
    ),
    "test_api_response_with_nested_data": (
        "tests.test_models",
        "test_api_response_with_nested_data",
    ),
    "test_client_class_creation": (
        "tests.test_client_class",
        "test_client_class_creation",
    ),
    "test_client_config_access": (
        "tests.test_client_class",
        "test_client_config_access",
    ),
    "test_client_has_discovery_methods": (
        "tests.test_client_class",
        "test_client_has_discovery_methods",
    ),
    "test_client_has_http_methods": (
        "tests.test_client_class",
        "test_client_has_http_methods",
    ),
    "test_client_has_lifecycle_methods": (
        "tests.test_client_class",
        "test_client_has_lifecycle_methods",
    ),
    "test_client_has_wms_operations": (
        "tests.test_client_class",
        "test_client_has_wms_operations",
    ),
    "test_client_internal_state": (
        "tests.test_client_class",
        "test_client_internal_state",
    ),
    "test_config_creation": ("tests.test_config_module", "test_config_creation"),
    "test_config_creation_valid": ("tests.test_config", "test_config_creation_valid"),
    "test_config_custom_values": (
        "tests.test_config_module",
        "test_config_custom_values",
    ),
    "test_config_defaults_from_constants": (
        "tests.test_config",
        "test_config_defaults_from_constants",
    ),
    "test_config_enterprise_features": (
        "tests.test_config",
        "test_config_enterprise_features",
    ),
    "test_config_environment_from_url": (
        "tests.test_config",
        "test_config_environment_from_url",
    ),
    "test_config_optional_auth_fields": (
        "tests.test_config",
        "test_config_optional_auth_fields",
    ),
    "test_config_reset_functionality": (
        "tests.test_config_module",
        "test_config_reset_functionality",
    ),
    "test_config_singleton_behavior": (
        "tests.test_config_module",
        "test_config_singleton_behavior",
    ),
    "test_config_testing_factory": (
        "tests.test_config_module",
        "test_config_testing_factory",
    ),
    "test_config_validate_config_success": (
        "tests.test_config",
        "test_config_validate_config_success",
    ),
    "test_config_validation": ("tests.test_config_module", "test_config_validation"),
    "test_entity_creation": ("tests.test_models", "test_entity_creation"),
    "test_entity_defaults": ("tests.test_models", "test_entity_defaults"),
    "test_entity_validate_entity_success": (
        "tests.test_models",
        "test_entity_validate_entity_success",
    ),
    "test_entity_validation_bad_endpoint_raises": (
        "tests.test_models",
        "test_entity_validation_bad_endpoint_raises",
    ),
    "test_entity_validation_empty_name_raises": (
        "tests.test_models",
        "test_entity_validation_empty_name_raises",
    ),
    "test_real_connection": ("tests.test_connection", "test_real_connection"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "u"),
    "unit": ("tests.unit", ""),
}

__all__ = [
    "CompleteMockPipeline",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiVersion",
    "FocusedOracleWmsDiscovery",
    "OptimizedOracleWmsDiscovery",
    "OracleWmsCompleteDiscovery",
    "TestApplyOperator",
    "TestAuthenticationConfig",
    "TestAuthenticationMethod",
    "TestAuthenticator",
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
    "TestFlextOracleWmsClient",
    "TestFlextOracleWmsClientCore",
    "TestFlextOracleWmsConstants",
    "TestFlextOracleWmsEntity",
    "TestFlextOracleWmsEntityDiscovery",
    "TestFlextOracleWmsFilterConstruction",
    "TestFlextOracleWmsSettings",
    "TestFlextOracleWmsUtilities",
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
    "TestWmsEnums",
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
    "c",
    "env_config",
    "find_env_file",
    "load_env_config",
    "load_test_env",
    "logger",
    "m",
    "main",
    "mock_config",
    "oracle_wms_client",
    "p",
    "pytest_configure",
    "pytestmark",
    "real_config",
    "run_complete_discovery",
    "run_optimized_discovery",
    "sample_entities",
    "sample_entity_data",
    "t",
    "test_api_response_creation",
    "test_api_response_defaults",
    "test_api_response_error",
    "test_api_response_validate_response_failure",
    "test_api_response_validate_response_success",
    "test_api_response_with_nested_data",
    "test_client_class_creation",
    "test_client_config_access",
    "test_client_has_discovery_methods",
    "test_client_has_http_methods",
    "test_client_has_lifecycle_methods",
    "test_client_has_wms_operations",
    "test_client_internal_state",
    "test_config_creation",
    "test_config_creation_valid",
    "test_config_custom_values",
    "test_config_defaults_from_constants",
    "test_config_enterprise_features",
    "test_config_environment_from_url",
    "test_config_optional_auth_fields",
    "test_config_reset_functionality",
    "test_config_singleton_behavior",
    "test_config_testing_factory",
    "test_config_validate_config_success",
    "test_config_validation",
    "test_entity_creation",
    "test_entity_defaults",
    "test_entity_validate_entity_success",
    "test_entity_validation_bad_endpoint_raises",
    "test_entity_validation_empty_name_raises",
    "test_real_connection",
    "tm",
    "u",
    "unit",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
