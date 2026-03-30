# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import *

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
        utilities,
    )
    from tests.complete_mock_pipeline import *
    from tests.conftest import *
    from tests.constants import *
    from tests.models import *
    from tests.oracle_wms_complete_discovery import *
    from tests.oracle_wms_focused_discovery import *
    from tests.oracle_wms_optimized_discovery import *
    from tests.protocols import *
    from tests.test_authentication import *
    from tests.test_authentication_core import *
    from tests.test_client import *
    from tests.test_client_class import *
    from tests.test_client_core import *
    from tests.test_config import *
    from tests.test_config_module import *
    from tests.test_connection import *
    from tests.test_declarative import *
    from tests.test_discovery import *
    from tests.test_filtering import *
    from tests.test_helpers_core import *
    from tests.test_models import *
    from tests.test_schema_dynamic import *
    from tests.test_singer_flattening import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "CompleteMockPipeline": "tests.complete_mock_pipeline",
    "FlextOracleWmsAuthSettings": "tests.test_authentication",
    "FlextOracleWmsTestConstants": "tests.constants",
    "FlextOracleWmsTestModels": "tests.models",
    "FlextOracleWmsTestProtocols": "tests.protocols",
    "FlextOracleWmsTestTypes": "tests.typings",
    "FlextOracleWmsTestUtilities": "tests.utilities",
    "FocusedOracleWmsDiscovery": "tests.oracle_wms_focused_discovery",
    "OptimizedOracleWmsDiscovery": "tests.oracle_wms_optimized_discovery",
    "OracleWMSAuthMethod": "tests.test_schema_dynamic",
    "OracleWmsCompleteDiscovery": "tests.oracle_wms_complete_discovery",
    "TestApplyOperator": "tests.test_filtering",
    "TestAuthenticationConfig": "tests.test_authentication_core",
    "TestAuthenticationMethod": "tests.test_authentication_core",
    "TestAuthenticator": "tests.test_authentication_core",
    "TestAutomationApisIntegration": "tests.test_declarative",
    "TestClientSimpleNew": "tests.test_client",
    "TestConvenienceFunctions": "tests.test_filtering",
    "TestDiscoveryConstants": "tests.test_discovery",
    "TestEndpointDiscoveryStrategyEnum": "tests.test_discovery",
    "TestErrorHandling": "tests.test_filtering",
    "TestErrorHandlingIntegration": "tests.test_declarative",
    "TestFactoryFunction": "tests.test_filtering",
    "TestFilterValidation": "tests.test_filtering",
    "TestFlextOracleWmsApi": "tests.unit.test_api",
    "TestFlextOracleWmsApiResponse": "tests.test_singer_flattening",
    "TestFlextOracleWmsClient": "tests.unit.test_wms_client",
    "TestFlextOracleWmsClientCore": "tests.test_client_core",
    "TestFlextOracleWmsConstants": "tests.test_schema_dynamic",
    "TestFlextOracleWmsEntity": "tests.test_singer_flattening",
    "TestFlextOracleWmsEntityDiscovery": "tests.test_discovery",
    "TestFlextOracleWmsFilterConstruction": "tests.test_filtering",
    "TestFlextOracleWmsSettings": "tests.unit.test_config",
    "TestFlextOracleWmsUtilities": "tests.test_helpers_core",
    "TestGetLogger": "tests.test_client_core",
    "TestLgfApiV10Integration": "tests.test_declarative",
    "TestMatchesCondition": "tests.test_filtering",
    "TestNestedConstants": "tests.test_schema_dynamic",
    "TestNestedValueAccess": "tests.test_filtering",
    "TestNormalize": "tests.test_filtering",
    "TestOracleWmsDeclarativeIntegration": "tests.test_declarative",
    "TestPerformanceAndEdgeCases": "tests.test_filtering",
    "TestPerformanceIntegration": "tests.test_declarative",
    "TestRecordFiltering": "tests.test_filtering",
    "TestRecordSorting": "tests.test_filtering",
    "TestWmsEnums": "tests.test_schema_dynamic",
    "c": ["tests.constants", "FlextOracleWmsTestConstants"],
    "complete_mock_pipeline": "tests.complete_mock_pipeline",
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "create_oracle_wms_client": "tests.test_authentication",
    "d": "flext_tests",
    "e": "flext_tests",
    "env_config": "tests.test_declarative",
    "find_env_file": "tests.test_declarative",
    "h": "flext_tests",
    "load_env_config": "tests.test_declarative",
    "load_test_env": "tests.conftest",
    "logger": "tests.test_declarative",
    "m": ["tests.models", "FlextOracleWmsTestModels"],
    "main": "tests.oracle_wms_focused_discovery",
    "mock_config": "tests.conftest",
    "models": "tests.models",
    "oracle_wms_client": "tests.test_declarative",
    "oracle_wms_complete_discovery": "tests.oracle_wms_complete_discovery",
    "oracle_wms_focused_discovery": "tests.oracle_wms_focused_discovery",
    "oracle_wms_optimized_discovery": "tests.oracle_wms_optimized_discovery",
    "p": ["tests.protocols", "FlextOracleWmsTestProtocols"],
    "protocols": "tests.protocols",
    "pytest_configure": "tests.conftest",
    "pytestmark": "tests.test_declarative",
    "r": "flext_tests",
    "real_config": "tests.conftest",
    "reset_settings_singleton": "tests.conftest",
    "run_complete_discovery": "tests.oracle_wms_complete_discovery",
    "run_optimized_discovery": "tests.oracle_wms_optimized_discovery",
    "s": "flext_tests",
    "sample_entities": "tests.conftest",
    "sample_entity_data": "tests.conftest",
    "sitecustomize": "tests.sitecustomize",
    "t": ["tests.typings", "FlextOracleWmsTestTypes"],
    "test_api": "tests.unit.test_api",
    "test_api_response_creation": "tests.test_models",
    "test_api_response_defaults": "tests.test_models",
    "test_api_response_error": "tests.test_models",
    "test_api_response_validate_response_failure": "tests.test_models",
    "test_api_response_validate_response_success": "tests.test_models",
    "test_api_response_with_nested_data": "tests.test_models",
    "test_authentication": "tests.test_authentication",
    "test_authentication_core": "tests.test_authentication_core",
    "test_client": "tests.test_client",
    "test_client_class": "tests.test_client_class",
    "test_client_class_creation": "tests.test_client_class",
    "test_client_config_access": "tests.test_client_class",
    "test_client_core": "tests.test_client_core",
    "test_client_has_discovery_methods": "tests.test_client_class",
    "test_client_has_http_methods": "tests.test_client_class",
    "test_client_has_lifecycle_methods": "tests.test_client_class",
    "test_client_has_wms_operations": "tests.test_client_class",
    "test_client_internal_state": "tests.test_client_class",
    "test_config": "tests.test_config",
    "test_config_auth_fields_default_empty": "tests.test_config",
    "test_config_creation": "tests.test_config_module",
    "test_config_creation_valid": "tests.test_config",
    "test_config_custom_values": "tests.test_config_module",
    "test_config_defaults": "tests.test_config",
    "test_config_module": "tests.test_config_module",
    "test_config_reset_functionality": "tests.test_config_module",
    "test_config_singleton_behavior": "tests.test_config_module",
    "test_config_testing_factory": "tests.test_config_module",
    "test_config_validate_config_success": "tests.test_config",
    "test_config_validation": "tests.test_config_module",
    "test_connection": "tests.test_connection",
    "test_constants": "tests.unit.test_constants",
    "test_declarative": "tests.test_declarative",
    "test_discovery": "tests.test_discovery",
    "test_entity_creation": "tests.test_models",
    "test_entity_defaults": "tests.test_models",
    "test_entity_validate_entity_success": "tests.test_models",
    "test_entity_validation_bad_endpoint_raises": "tests.test_models",
    "test_entity_validation_empty_name_raises": "tests.test_models",
    "test_filtering": "tests.test_filtering",
    "test_helpers": "tests.test_helpers",
    "test_helpers_core": "tests.test_helpers_core",
    "test_models": "tests.test_models",
    "test_real_connection": "tests.test_connection",
    "test_schema_dynamic": "tests.test_schema_dynamic",
    "test_singer_flattening": "tests.test_singer_flattening",
    "test_unified_config": "tests.test_unified_config",
    "test_wms_api": "tests.unit.test_wms_api",
    "test_wms_client": "tests.unit.test_wms_client",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextOracleWmsTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
