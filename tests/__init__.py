# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
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
from tests.test_schema_dynamic import Testc, TestNestedConstants, TestWmsEnums
from tests.test_singer_flattening import (
    TestFlextOracleWmsApiResponse,
    TestFlextOracleWmsEntity,
)
from tests.typings import FlextOracleWmsTestTypes, FlextOracleWmsTestTypes as t
from tests.unit.test_api import TestFlextOracleWmsApi
from tests.unit.test_config import TestFlextOracleWmsSettings
from tests.unit.test_wms_client import TestFlextOracleWmsClient
from tests.utilities import (
    FlextOracleWmsTestUtilities,
    FlextOracleWmsTestUtilities as u,
)

if _t.TYPE_CHECKING:
    import tests.complete_mock_pipeline as _tests_complete_mock_pipeline

    complete_mock_pipeline = _tests_complete_mock_pipeline
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models

    models = _tests_models
    import tests.oracle_wms_complete_discovery as _tests_oracle_wms_complete_discovery

    oracle_wms_complete_discovery = _tests_oracle_wms_complete_discovery
    import tests.oracle_wms_focused_discovery as _tests_oracle_wms_focused_discovery

    oracle_wms_focused_discovery = _tests_oracle_wms_focused_discovery
    import tests.oracle_wms_optimized_discovery as _tests_oracle_wms_optimized_discovery

    oracle_wms_optimized_discovery = _tests_oracle_wms_optimized_discovery
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.sitecustomize as _tests_sitecustomize

    sitecustomize = _tests_sitecustomize
    import tests.test_authentication as _tests_test_authentication

    test_authentication = _tests_test_authentication
    import tests.test_authentication_core as _tests_test_authentication_core

    test_authentication_core = _tests_test_authentication_core
    import tests.test_client as _tests_test_client

    test_client = _tests_test_client
    import tests.test_client_class as _tests_test_client_class

    test_client_class = _tests_test_client_class
    import tests.test_client_core as _tests_test_client_core

    test_client_core = _tests_test_client_core
    import tests.test_config as _tests_test_config

    test_config = _tests_test_config
    import tests.test_config_module as _tests_test_config_module

    test_config_module = _tests_test_config_module
    import tests.test_connection as _tests_test_connection

    test_connection = _tests_test_connection
    import tests.test_declarative as _tests_test_declarative

    test_declarative = _tests_test_declarative
    import tests.test_discovery as _tests_test_discovery

    test_discovery = _tests_test_discovery
    import tests.test_filtering as _tests_test_filtering

    test_filtering = _tests_test_filtering
    import tests.test_helpers as _tests_test_helpers

    test_helpers = _tests_test_helpers
    import tests.test_helpers_core as _tests_test_helpers_core

    test_helpers_core = _tests_test_helpers_core
    import tests.test_models as _tests_test_models

    test_models = _tests_test_models
    import tests.test_schema_dynamic as _tests_test_schema_dynamic

    test_schema_dynamic = _tests_test_schema_dynamic
    import tests.test_singer_flattening as _tests_test_singer_flattening

    test_singer_flattening = _tests_test_singer_flattening
    import tests.test_unified_config as _tests_test_unified_config

    test_unified_config = _tests_test_unified_config
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit

    unit = _tests_unit
    import tests.unit.test_api as _tests_unit_test_api

    test_api = _tests_unit_test_api
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_wms_api as _tests_unit_test_wms_api

    test_wms_api = _tests_unit_test_wms_api
    import tests.unit.test_wms_client as _tests_unit_test_wms_client

    test_wms_client = _tests_unit_test_wms_client
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        CompleteMockPipeline,
        FlextOracleWmsTestConstants,
        FlextOracleWmsTestModels,
        FlextOracleWmsTestProtocols,
        FlextOracleWmsTestTypes,
        FlextOracleWmsTestUtilities,
        FocusedOracleWmsDiscovery,
        OptimizedOracleWmsDiscovery,
        OracleWmsCompleteDiscovery,
        TestApplyOperator,
        TestAuthenticationConfig,
        TestAuthenticationMethod,
        TestAuthenticator,
        TestAutomationApisIntegration,
        TestClientSimpleNew,
        TestConvenienceFunctions,
        TestDiscoveryConstants,
        TestEndpointDiscoveryStrategyEnum,
        TestErrorHandling,
        TestErrorHandlingIntegration,
        TestFactoryFunction,
        TestFilterValidation,
        TestFlextOracleWmsApi,
        TestFlextOracleWmsApiResponse,
        TestFlextOracleWmsClient,
        TestFlextOracleWmsClientCore,
        TestFlextOracleWmsEntity,
        TestFlextOracleWmsEntityDiscovery,
        TestFlextOracleWmsFilterConstruction,
        TestFlextOracleWmsSettings,
        TestFlextOracleWmsUtilities,
        TestGetLogger,
        TestLgfApiV10Integration,
        TestMatchesCondition,
        TestNestedConstants,
        TestNestedValueAccess,
        TestNormalize,
        TestOracleWmsDeclarativeIntegration,
        TestPerformanceAndEdgeCases,
        TestPerformanceIntegration,
        TestRecordFiltering,
        TestRecordSorting,
        TestWmsEnums,
        Testc,
        c,
        complete_mock_pipeline,
        conftest,
        constants,
        d,
        e,
        env_config,
        h,
        load_test_env,
        logger,
        m,
        main,
        mock_config,
        models,
        oracle_wms_client,
        oracle_wms_complete_discovery,
        oracle_wms_focused_discovery,
        oracle_wms_optimized_discovery,
        p,
        protocols,
        pytest_configure,
        pytestmark,
        r,
        real_config,
        reset_settings_singleton,
        run_complete_discovery,
        run_optimized_discovery,
        s,
        sample_entities,
        sample_entity_data,
        sitecustomize,
        t,
        test_api,
        test_api_response_creation,
        test_api_response_defaults,
        test_api_response_error,
        test_api_response_validate_response_failure,
        test_api_response_validate_response_success,
        test_api_response_with_nested_data,
        test_authentication,
        test_authentication_core,
        test_client,
        test_client_class,
        test_client_class_creation,
        test_client_config_access,
        test_client_core,
        test_client_has_discovery_methods,
        test_client_has_http_methods,
        test_client_has_lifecycle_methods,
        test_client_has_wms_operations,
        test_client_internal_state,
        test_config,
        test_config_auth_fields_default_empty,
        test_config_creation,
        test_config_creation_valid,
        test_config_custom_values,
        test_config_defaults,
        test_config_module,
        test_config_reset_functionality,
        test_config_singleton_behavior,
        test_config_testing_factory,
        test_config_validate_config_success,
        test_config_validation,
        test_connection,
        test_constants,
        test_declarative,
        test_discovery,
        test_entity_creation,
        test_entity_defaults,
        test_entity_validate_entity_success,
        test_entity_validation_bad_endpoint_raises,
        test_entity_validation_empty_name_raises,
        test_filtering,
        test_helpers,
        test_helpers_core,
        test_models,
        test_real_connection,
        test_schema_dynamic,
        test_singer_flattening,
        test_unified_config,
        test_wms_api,
        test_wms_client,
        typings,
        u,
        unit,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.unit",),
    {
        "CompleteMockPipeline": "tests.complete_mock_pipeline",
        "FlextOracleWmsTestConstants": "tests.constants",
        "FlextOracleWmsTestModels": "tests.models",
        "FlextOracleWmsTestProtocols": "tests.protocols",
        "FlextOracleWmsTestTypes": "tests.typings",
        "FlextOracleWmsTestUtilities": "tests.utilities",
        "FocusedOracleWmsDiscovery": "tests.oracle_wms_focused_discovery",
        "OptimizedOracleWmsDiscovery": "tests.oracle_wms_optimized_discovery",
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
        "TestFlextOracleWmsApiResponse": "tests.test_singer_flattening",
        "TestFlextOracleWmsClientCore": "tests.test_client_core",
        "TestFlextOracleWmsEntity": "tests.test_singer_flattening",
        "TestFlextOracleWmsEntityDiscovery": "tests.test_discovery",
        "TestFlextOracleWmsFilterConstruction": "tests.test_filtering",
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
        "Testc": "tests.test_schema_dynamic",
        "c": ("tests.constants", "FlextOracleWmsTestConstants"),
        "complete_mock_pipeline": "tests.complete_mock_pipeline",
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "env_config": "tests.test_declarative",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "load_test_env": "tests.conftest",
        "logger": "tests.test_declarative",
        "m": ("tests.models", "FlextOracleWmsTestModels"),
        "main": "tests.oracle_wms_focused_discovery",
        "mock_config": "tests.conftest",
        "models": "tests.models",
        "oracle_wms_client": "tests.test_declarative",
        "oracle_wms_complete_discovery": "tests.oracle_wms_complete_discovery",
        "oracle_wms_focused_discovery": "tests.oracle_wms_focused_discovery",
        "oracle_wms_optimized_discovery": "tests.oracle_wms_optimized_discovery",
        "p": ("tests.protocols", "FlextOracleWmsTestProtocols"),
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "pytestmark": "tests.test_declarative",
        "r": ("flext_core.result", "FlextResult"),
        "real_config": "tests.conftest",
        "reset_settings_singleton": "tests.conftest",
        "run_complete_discovery": "tests.oracle_wms_complete_discovery",
        "run_optimized_discovery": "tests.oracle_wms_optimized_discovery",
        "s": ("flext_core.service", "FlextService"),
        "sample_entities": "tests.conftest",
        "sample_entity_data": "tests.conftest",
        "sitecustomize": "tests.sitecustomize",
        "t": ("tests.typings", "FlextOracleWmsTestTypes"),
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
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextOracleWmsTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "CompleteMockPipeline",
    "FlextOracleWmsTestConstants",
    "FlextOracleWmsTestModels",
    "FlextOracleWmsTestProtocols",
    "FlextOracleWmsTestTypes",
    "FlextOracleWmsTestUtilities",
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
    "Testc",
    "c",
    "complete_mock_pipeline",
    "conftest",
    "constants",
    "d",
    "e",
    "env_config",
    "h",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
