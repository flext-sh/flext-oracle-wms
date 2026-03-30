# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import (
        complete_mock_pipeline,
        conftest,
        constants,
        models,
        oracle_wms_complete_discovery,
        oracle_wms_focused_discovery,
        oracle_wms_optimized_discovery,
        protocols,
        sitecustomize,
        test_authentication,
        test_authentication_core,
        test_client,
        test_client_class,
        test_client_core,
        test_config,
        test_config_module,
        test_connection,
        test_declarative,
        test_discovery,
        test_filtering,
        test_helpers,
        test_helpers_core,
        test_models,
        test_schema_dynamic,
        test_singer_flattening,
        test_unified_config,
        typings,
        unit,
        utilities,
    )
    from tests.complete_mock_pipeline import CompleteMockPipeline
    from tests.conftest import (
        load_test_env,
        mock_config,
        pytest_configure,
        real_config,
        reset_settings_singleton,
        sample_entities,
        sample_entity_data,
    )
    from tests.constants import (
        FlextOracleWmsTestConstants,
        FlextOracleWmsTestConstants as c,
    )
    from tests.models import FlextOracleWmsTestModels, FlextOracleWmsTestModels as m
    from tests.oracle_wms_complete_discovery import (
        OracleWmsCompleteDiscovery,
        run_complete_discovery,
    )
    from tests.oracle_wms_focused_discovery import FocusedOracleWmsDiscovery, main
    from tests.oracle_wms_optimized_discovery import (
        OptimizedOracleWmsDiscovery,
        run_optimized_discovery,
    )
    from tests.protocols import (
        FlextOracleWmsTestProtocols,
        FlextOracleWmsTestProtocols as p,
    )
    from tests.test_authentication import (
        FlextOracleWmsAuthSettings,
        create_oracle_wms_client,
    )
    from tests.test_authentication_core import (
        TestAuthenticationConfig,
        TestAuthenticationMethod,
        TestAuthenticator,
    )
    from tests.test_client import TestClientSimpleNew
    from tests.test_client_class import (
        test_client_class_creation,
        test_client_config_access,
        test_client_has_discovery_methods,
        test_client_has_http_methods,
        test_client_has_lifecycle_methods,
        test_client_has_wms_operations,
        test_client_internal_state,
    )
    from tests.test_client_core import TestFlextOracleWmsClientCore, TestGetLogger
    from tests.test_config import (
        test_config_auth_fields_default_empty,
        test_config_creation_valid,
        test_config_defaults,
        test_config_validate_config_success,
    )
    from tests.test_config_module import (
        test_config_creation,
        test_config_custom_values,
        test_config_reset_functionality,
        test_config_singleton_behavior,
        test_config_testing_factory,
        test_config_validation,
    )
    from tests.test_connection import test_real_connection
    from tests.test_declarative import (
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
    from tests.test_discovery import (
        TestDiscoveryConstants,
        TestEndpointDiscoveryStrategyEnum,
        TestFlextOracleWmsEntityDiscovery,
    )
    from tests.test_filtering import (
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
    from tests.test_helpers_core import TestFlextOracleWmsUtilities
    from tests.test_models import (
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
    from tests.test_schema_dynamic import (
        OracleWMSAuthMethod,
        TestFlextOracleWmsConstants,
        TestNestedConstants,
        TestWmsEnums,
    )
    from tests.test_singer_flattening import (
        TestFlextOracleWmsApiResponse,
        TestFlextOracleWmsEntity,
    )
    from tests.typings import FlextOracleWmsTestTypes, FlextOracleWmsTestTypes as t
    from tests.unit import test_api, test_constants, test_wms_api, test_wms_client
    from tests.unit.test_api import TestFlextOracleWmsApi
    from tests.unit.test_config import TestFlextOracleWmsSettings
    from tests.unit.test_wms_client import TestFlextOracleWmsClient
    from tests.utilities import (
        FlextOracleWmsTestUtilities,
        FlextOracleWmsTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "CompleteMockPipeline": ["tests.complete_mock_pipeline", "CompleteMockPipeline"],
    "FlextOracleWmsAuthSettings": [
        "tests.test_authentication",
        "FlextOracleWmsAuthSettings",
    ],
    "FlextOracleWmsTestConstants": ["tests.constants", "FlextOracleWmsTestConstants"],
    "FlextOracleWmsTestModels": ["tests.models", "FlextOracleWmsTestModels"],
    "FlextOracleWmsTestProtocols": ["tests.protocols", "FlextOracleWmsTestProtocols"],
    "FlextOracleWmsTestTypes": ["tests.typings", "FlextOracleWmsTestTypes"],
    "FlextOracleWmsTestUtilities": ["tests.utilities", "FlextOracleWmsTestUtilities"],
    "FocusedOracleWmsDiscovery": [
        "tests.oracle_wms_focused_discovery",
        "FocusedOracleWmsDiscovery",
    ],
    "OptimizedOracleWmsDiscovery": [
        "tests.oracle_wms_optimized_discovery",
        "OptimizedOracleWmsDiscovery",
    ],
    "OracleWMSAuthMethod": ["tests.test_schema_dynamic", "OracleWMSAuthMethod"],
    "OracleWmsCompleteDiscovery": [
        "tests.oracle_wms_complete_discovery",
        "OracleWmsCompleteDiscovery",
    ],
    "TestApplyOperator": ["tests.test_filtering", "TestApplyOperator"],
    "TestAuthenticationConfig": [
        "tests.test_authentication_core",
        "TestAuthenticationConfig",
    ],
    "TestAuthenticationMethod": [
        "tests.test_authentication_core",
        "TestAuthenticationMethod",
    ],
    "TestAuthenticator": ["tests.test_authentication_core", "TestAuthenticator"],
    "TestAutomationApisIntegration": [
        "tests.test_declarative",
        "TestAutomationApisIntegration",
    ],
    "TestClientSimpleNew": ["tests.test_client", "TestClientSimpleNew"],
    "TestConvenienceFunctions": ["tests.test_filtering", "TestConvenienceFunctions"],
    "TestDiscoveryConstants": ["tests.test_discovery", "TestDiscoveryConstants"],
    "TestEndpointDiscoveryStrategyEnum": [
        "tests.test_discovery",
        "TestEndpointDiscoveryStrategyEnum",
    ],
    "TestErrorHandling": ["tests.test_filtering", "TestErrorHandling"],
    "TestErrorHandlingIntegration": [
        "tests.test_declarative",
        "TestErrorHandlingIntegration",
    ],
    "TestFactoryFunction": ["tests.test_filtering", "TestFactoryFunction"],
    "TestFilterValidation": ["tests.test_filtering", "TestFilterValidation"],
    "TestFlextOracleWmsApi": ["tests.unit.test_api", "TestFlextOracleWmsApi"],
    "TestFlextOracleWmsApiResponse": [
        "tests.test_singer_flattening",
        "TestFlextOracleWmsApiResponse",
    ],
    "TestFlextOracleWmsClient": [
        "tests.unit.test_wms_client",
        "TestFlextOracleWmsClient",
    ],
    "TestFlextOracleWmsClientCore": [
        "tests.test_client_core",
        "TestFlextOracleWmsClientCore",
    ],
    "TestFlextOracleWmsConstants": [
        "tests.test_schema_dynamic",
        "TestFlextOracleWmsConstants",
    ],
    "TestFlextOracleWmsEntity": [
        "tests.test_singer_flattening",
        "TestFlextOracleWmsEntity",
    ],
    "TestFlextOracleWmsEntityDiscovery": [
        "tests.test_discovery",
        "TestFlextOracleWmsEntityDiscovery",
    ],
    "TestFlextOracleWmsFilterConstruction": [
        "tests.test_filtering",
        "TestFlextOracleWmsFilterConstruction",
    ],
    "TestFlextOracleWmsSettings": [
        "tests.unit.test_config",
        "TestFlextOracleWmsSettings",
    ],
    "TestFlextOracleWmsUtilities": [
        "tests.test_helpers_core",
        "TestFlextOracleWmsUtilities",
    ],
    "TestGetLogger": ["tests.test_client_core", "TestGetLogger"],
    "TestLgfApiV10Integration": ["tests.test_declarative", "TestLgfApiV10Integration"],
    "TestMatchesCondition": ["tests.test_filtering", "TestMatchesCondition"],
    "TestNestedConstants": ["tests.test_schema_dynamic", "TestNestedConstants"],
    "TestNestedValueAccess": ["tests.test_filtering", "TestNestedValueAccess"],
    "TestNormalize": ["tests.test_filtering", "TestNormalize"],
    "TestOracleWmsDeclarativeIntegration": [
        "tests.test_declarative",
        "TestOracleWmsDeclarativeIntegration",
    ],
    "TestPerformanceAndEdgeCases": [
        "tests.test_filtering",
        "TestPerformanceAndEdgeCases",
    ],
    "TestPerformanceIntegration": [
        "tests.test_declarative",
        "TestPerformanceIntegration",
    ],
    "TestRecordFiltering": ["tests.test_filtering", "TestRecordFiltering"],
    "TestRecordSorting": ["tests.test_filtering", "TestRecordSorting"],
    "TestWmsEnums": ["tests.test_schema_dynamic", "TestWmsEnums"],
    "c": ["tests.constants", "FlextOracleWmsTestConstants"],
    "complete_mock_pipeline": ["tests.complete_mock_pipeline", ""],
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "create_oracle_wms_client": [
        "tests.test_authentication",
        "create_oracle_wms_client",
    ],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "env_config": ["tests.test_declarative", "env_config"],
    "find_env_file": ["tests.test_declarative", "find_env_file"],
    "h": ["flext_tests", "h"],
    "load_env_config": ["tests.test_declarative", "load_env_config"],
    "load_test_env": ["tests.conftest", "load_test_env"],
    "logger": ["tests.test_declarative", "logger"],
    "m": ["tests.models", "FlextOracleWmsTestModels"],
    "main": ["tests.oracle_wms_focused_discovery", "main"],
    "mock_config": ["tests.conftest", "mock_config"],
    "models": ["tests.models", ""],
    "oracle_wms_client": ["tests.test_declarative", "oracle_wms_client"],
    "oracle_wms_complete_discovery": ["tests.oracle_wms_complete_discovery", ""],
    "oracle_wms_focused_discovery": ["tests.oracle_wms_focused_discovery", ""],
    "oracle_wms_optimized_discovery": ["tests.oracle_wms_optimized_discovery", ""],
    "p": ["tests.protocols", "FlextOracleWmsTestProtocols"],
    "protocols": ["tests.protocols", ""],
    "pytest_configure": ["tests.conftest", "pytest_configure"],
    "pytestmark": ["tests.test_declarative", "pytestmark"],
    "r": ["flext_tests", "r"],
    "real_config": ["tests.conftest", "real_config"],
    "reset_settings_singleton": ["tests.conftest", "reset_settings_singleton"],
    "run_complete_discovery": [
        "tests.oracle_wms_complete_discovery",
        "run_complete_discovery",
    ],
    "run_optimized_discovery": [
        "tests.oracle_wms_optimized_discovery",
        "run_optimized_discovery",
    ],
    "s": ["flext_tests", "s"],
    "sample_entities": ["tests.conftest", "sample_entities"],
    "sample_entity_data": ["tests.conftest", "sample_entity_data"],
    "sitecustomize": ["tests.sitecustomize", ""],
    "t": ["tests.typings", "FlextOracleWmsTestTypes"],
    "test_api": ["tests.unit.test_api", ""],
    "test_api_response_creation": ["tests.test_models", "test_api_response_creation"],
    "test_api_response_defaults": ["tests.test_models", "test_api_response_defaults"],
    "test_api_response_error": ["tests.test_models", "test_api_response_error"],
    "test_api_response_validate_response_failure": [
        "tests.test_models",
        "test_api_response_validate_response_failure",
    ],
    "test_api_response_validate_response_success": [
        "tests.test_models",
        "test_api_response_validate_response_success",
    ],
    "test_api_response_with_nested_data": [
        "tests.test_models",
        "test_api_response_with_nested_data",
    ],
    "test_authentication": ["tests.test_authentication", ""],
    "test_authentication_core": ["tests.test_authentication_core", ""],
    "test_client": ["tests.test_client", ""],
    "test_client_class": ["tests.test_client_class", ""],
    "test_client_class_creation": [
        "tests.test_client_class",
        "test_client_class_creation",
    ],
    "test_client_config_access": [
        "tests.test_client_class",
        "test_client_config_access",
    ],
    "test_client_core": ["tests.test_client_core", ""],
    "test_client_has_discovery_methods": [
        "tests.test_client_class",
        "test_client_has_discovery_methods",
    ],
    "test_client_has_http_methods": [
        "tests.test_client_class",
        "test_client_has_http_methods",
    ],
    "test_client_has_lifecycle_methods": [
        "tests.test_client_class",
        "test_client_has_lifecycle_methods",
    ],
    "test_client_has_wms_operations": [
        "tests.test_client_class",
        "test_client_has_wms_operations",
    ],
    "test_client_internal_state": [
        "tests.test_client_class",
        "test_client_internal_state",
    ],
    "test_config": ["tests.test_config", ""],
    "test_config_auth_fields_default_empty": [
        "tests.test_config",
        "test_config_auth_fields_default_empty",
    ],
    "test_config_creation": ["tests.test_config_module", "test_config_creation"],
    "test_config_creation_valid": ["tests.test_config", "test_config_creation_valid"],
    "test_config_custom_values": [
        "tests.test_config_module",
        "test_config_custom_values",
    ],
    "test_config_defaults": ["tests.test_config", "test_config_defaults"],
    "test_config_module": ["tests.test_config_module", ""],
    "test_config_reset_functionality": [
        "tests.test_config_module",
        "test_config_reset_functionality",
    ],
    "test_config_singleton_behavior": [
        "tests.test_config_module",
        "test_config_singleton_behavior",
    ],
    "test_config_testing_factory": [
        "tests.test_config_module",
        "test_config_testing_factory",
    ],
    "test_config_validate_config_success": [
        "tests.test_config",
        "test_config_validate_config_success",
    ],
    "test_config_validation": ["tests.test_config_module", "test_config_validation"],
    "test_connection": ["tests.test_connection", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_declarative": ["tests.test_declarative", ""],
    "test_discovery": ["tests.test_discovery", ""],
    "test_entity_creation": ["tests.test_models", "test_entity_creation"],
    "test_entity_defaults": ["tests.test_models", "test_entity_defaults"],
    "test_entity_validate_entity_success": [
        "tests.test_models",
        "test_entity_validate_entity_success",
    ],
    "test_entity_validation_bad_endpoint_raises": [
        "tests.test_models",
        "test_entity_validation_bad_endpoint_raises",
    ],
    "test_entity_validation_empty_name_raises": [
        "tests.test_models",
        "test_entity_validation_empty_name_raises",
    ],
    "test_filtering": ["tests.test_filtering", ""],
    "test_helpers": ["tests.test_helpers", ""],
    "test_helpers_core": ["tests.test_helpers_core", ""],
    "test_models": ["tests.test_models", ""],
    "test_real_connection": ["tests.test_connection", "test_real_connection"],
    "test_schema_dynamic": ["tests.test_schema_dynamic", ""],
    "test_singer_flattening": ["tests.test_singer_flattening", ""],
    "test_unified_config": ["tests.test_unified_config", ""],
    "test_wms_api": ["tests.unit.test_wms_api", ""],
    "test_wms_client": ["tests.unit.test_wms_client", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextOracleWmsTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

__all__ = [
    "CompleteMockPipeline",
    "FlextOracleWmsAuthSettings",
    "FlextOracleWmsTestConstants",
    "FlextOracleWmsTestModels",
    "FlextOracleWmsTestProtocols",
    "FlextOracleWmsTestTypes",
    "FlextOracleWmsTestUtilities",
    "FocusedOracleWmsDiscovery",
    "OptimizedOracleWmsDiscovery",
    "OracleWMSAuthMethod",
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
    "c",
    "complete_mock_pipeline",
    "conftest",
    "constants",
    "create_oracle_wms_client",
    "d",
    "e",
    "env_config",
    "find_env_file",
    "h",
    "load_env_config",
    "load_test_env",
    "logger",
    "m",
    "main",
    "mock_config",
    "models",
    "oracle_wms_client",
    "oracle_wms_complete_discovery",
    "oracle_wms_focused_discovery",
    "oracle_wms_optimized_discovery",
    "p",
    "protocols",
    "pytest_configure",
    "pytestmark",
    "r",
    "real_config",
    "reset_settings_singleton",
    "run_complete_discovery",
    "run_optimized_discovery",
    "s",
    "sample_entities",
    "sample_entity_data",
    "sitecustomize",
    "t",
    "test_api",
    "test_api_response_creation",
    "test_api_response_defaults",
    "test_api_response_error",
    "test_api_response_validate_response_failure",
    "test_api_response_validate_response_success",
    "test_api_response_with_nested_data",
    "test_authentication",
    "test_authentication_core",
    "test_client",
    "test_client_class",
    "test_client_class_creation",
    "test_client_config_access",
    "test_client_core",
    "test_client_has_discovery_methods",
    "test_client_has_http_methods",
    "test_client_has_lifecycle_methods",
    "test_client_has_wms_operations",
    "test_client_internal_state",
    "test_config",
    "test_config_auth_fields_default_empty",
    "test_config_creation",
    "test_config_creation_valid",
    "test_config_custom_values",
    "test_config_defaults",
    "test_config_module",
    "test_config_reset_functionality",
    "test_config_singleton_behavior",
    "test_config_testing_factory",
    "test_config_validate_config_success",
    "test_config_validation",
    "test_connection",
    "test_constants",
    "test_declarative",
    "test_discovery",
    "test_entity_creation",
    "test_entity_defaults",
    "test_entity_validate_entity_success",
    "test_entity_validation_bad_endpoint_raises",
    "test_entity_validation_empty_name_raises",
    "test_filtering",
    "test_helpers",
    "test_helpers_core",
    "test_models",
    "test_real_connection",
    "test_schema_dynamic",
    "test_singer_flattening",
    "test_unified_config",
    "test_wms_api",
    "test_wms_client",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
