# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_oracle_wms import (
        complete_mock_pipeline,
        conftest,
        constants,
        models,
        oracle_wms_complete_discovery,
        oracle_wms_focused_discovery,
        oracle_wms_optimized_discovery,
        protocols,
        sitecustomize,
        test_api,
        test_authentication,
        test_authentication_core,
        test_client,
        test_client_class,
        test_client_core,
        test_config,
        test_config_module,
        test_connection,
        test_constants,
        test_declarative,
        test_discovery,
        test_filtering,
        test_helpers,
        test_helpers_core,
        test_models,
        test_schema_dynamic,
        test_singer_flattening,
        test_unified_config,
        test_wms_api,
        test_wms_client,
        typings,
        unit,
        utilities,
    )
    from flext_oracle_wms.conftest import (
        load_test_env,
        mock_config,
        real_config,
        reset_settings_singleton,
        sample_entities,
        sample_entity_data,
    )
    from flext_oracle_wms.constants import (
        FlextOracleWmsTestConstants,
        FlextOracleWmsTestConstants as c,
    )
    from flext_oracle_wms.models import (
        FlextOracleWmsTestModels,
        FlextOracleWmsTestModels as m,
    )
    from flext_oracle_wms.oracle_wms_complete_discovery import (
        OracleWmsCompleteDiscovery,
    )
    from flext_oracle_wms.oracle_wms_focused_discovery import FocusedOracleWmsDiscovery
    from flext_oracle_wms.oracle_wms_optimized_discovery import (
        OptimizedOracleWmsDiscovery,
    )
    from flext_oracle_wms.protocols import (
        FlextOracleWmsTestProtocols,
        FlextOracleWmsTestProtocols as p,
    )
    from flext_oracle_wms.test_authentication_core import (
        TestAuthenticationConfig,
        TestAuthenticationMethod,
        TestAuthenticator,
    )
    from flext_oracle_wms.test_client import TestClientSimpleNew
    from flext_oracle_wms.test_client_class import test_client_class_creation
    from flext_oracle_wms.test_client_core import (
        TestFlextOracleWmsClientCore,
        TestGetLogger,
    )
    from flext_oracle_wms.test_config import (
        test_config_auth_fields_default_empty,
        test_config_creation_valid,
        test_config_defaults,
        test_config_testing_factory,
        test_config_validate_config_success,
    )
    from flext_oracle_wms.test_config_module import test_config_creation
    from flext_oracle_wms.test_connection import test_real_connection
    from flext_oracle_wms.test_declarative import (
        TestOracleWmsDeclarativeIntegration,
        client,
        config,
        env_config,
        logger,
        oracle_wms_client,
        pytestmark,
        start_result,
    )
    from flext_oracle_wms.test_discovery import TestDiscoveryConstants
    from flext_oracle_wms.test_filtering import TestFlextOracleWmsFilterConstruction
    from flext_oracle_wms.test_helpers_core import TestFlextOracleWmsUtilities
    from flext_oracle_wms.test_models import test_entity_creation
    from flext_oracle_wms.test_schema_dynamic import Testc
    from flext_oracle_wms.test_singer_flattening import TestFlextOracleWmsEntity
    from flext_oracle_wms.typings import (
        FlextOracleWmsTestTypes,
        FlextOracleWmsTestTypes as t,
    )
    from flext_oracle_wms.unit import (
        TestFlextOracleWmsApi,
        TestFlextOracleWmsClient,
        TestFlextOracleWmsSettings,
    )
    from flext_oracle_wms.utilities import (
        FlextOracleWmsTestUtilities,
        FlextOracleWmsTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_oracle_wms.unit",),
    {
        "FlextOracleWmsTestConstants": "flext_oracle_wms.constants",
        "FlextOracleWmsTestModels": "flext_oracle_wms.models",
        "FlextOracleWmsTestProtocols": "flext_oracle_wms.protocols",
        "FlextOracleWmsTestTypes": "flext_oracle_wms.typings",
        "FlextOracleWmsTestUtilities": "flext_oracle_wms.utilities",
        "FocusedOracleWmsDiscovery": "flext_oracle_wms.oracle_wms_focused_discovery",
        "OptimizedOracleWmsDiscovery": "flext_oracle_wms.oracle_wms_optimized_discovery",
        "OracleWmsCompleteDiscovery": "flext_oracle_wms.oracle_wms_complete_discovery",
        "TestAuthenticationConfig": "flext_oracle_wms.test_authentication_core",
        "TestAuthenticationMethod": "flext_oracle_wms.test_authentication_core",
        "TestAuthenticator": "flext_oracle_wms.test_authentication_core",
        "TestClientSimpleNew": "flext_oracle_wms.test_client",
        "TestDiscoveryConstants": "flext_oracle_wms.test_discovery",
        "TestFlextOracleWmsClientCore": "flext_oracle_wms.test_client_core",
        "TestFlextOracleWmsEntity": "flext_oracle_wms.test_singer_flattening",
        "TestFlextOracleWmsFilterConstruction": "flext_oracle_wms.test_filtering",
        "TestFlextOracleWmsUtilities": "flext_oracle_wms.test_helpers_core",
        "TestGetLogger": "flext_oracle_wms.test_client_core",
        "TestOracleWmsDeclarativeIntegration": "flext_oracle_wms.test_declarative",
        "Testc": "flext_oracle_wms.test_schema_dynamic",
        "c": ("flext_oracle_wms.constants", "FlextOracleWmsTestConstants"),
        "client": "flext_oracle_wms.test_declarative",
        "complete_mock_pipeline": "flext_oracle_wms.complete_mock_pipeline",
        "config": "flext_oracle_wms.test_declarative",
        "conftest": "flext_oracle_wms.conftest",
        "constants": "flext_oracle_wms.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "env_config": "flext_oracle_wms.test_declarative",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "load_test_env": "flext_oracle_wms.conftest",
        "logger": "flext_oracle_wms.test_declarative",
        "m": ("flext_oracle_wms.models", "FlextOracleWmsTestModels"),
        "mock_config": "flext_oracle_wms.conftest",
        "models": "flext_oracle_wms.models",
        "oracle_wms_client": "flext_oracle_wms.test_declarative",
        "oracle_wms_complete_discovery": "flext_oracle_wms.oracle_wms_complete_discovery",
        "oracle_wms_focused_discovery": "flext_oracle_wms.oracle_wms_focused_discovery",
        "oracle_wms_optimized_discovery": "flext_oracle_wms.oracle_wms_optimized_discovery",
        "p": ("flext_oracle_wms.protocols", "FlextOracleWmsTestProtocols"),
        "protocols": "flext_oracle_wms.protocols",
        "pytestmark": "flext_oracle_wms.test_declarative",
        "r": ("flext_core.result", "FlextResult"),
        "real_config": "flext_oracle_wms.conftest",
        "reset_settings_singleton": "flext_oracle_wms.conftest",
        "s": ("flext_core.service", "FlextService"),
        "sample_entities": "flext_oracle_wms.conftest",
        "sample_entity_data": "flext_oracle_wms.conftest",
        "sitecustomize": "flext_oracle_wms.sitecustomize",
        "start_result": "flext_oracle_wms.test_declarative",
        "t": ("flext_oracle_wms.typings", "FlextOracleWmsTestTypes"),
        "test_api": "flext_oracle_wms.test_api",
        "test_authentication": "flext_oracle_wms.test_authentication",
        "test_authentication_core": "flext_oracle_wms.test_authentication_core",
        "test_client": "flext_oracle_wms.test_client",
        "test_client_class": "flext_oracle_wms.test_client_class",
        "test_client_class_creation": "flext_oracle_wms.test_client_class",
        "test_client_core": "flext_oracle_wms.test_client_core",
        "test_config": "flext_oracle_wms.test_config",
        "test_config_auth_fields_default_empty": "flext_oracle_wms.test_config",
        "test_config_creation": "flext_oracle_wms.test_config_module",
        "test_config_creation_valid": "flext_oracle_wms.test_config",
        "test_config_defaults": "flext_oracle_wms.test_config",
        "test_config_module": "flext_oracle_wms.test_config_module",
        "test_config_testing_factory": "flext_oracle_wms.test_config",
        "test_config_validate_config_success": "flext_oracle_wms.test_config",
        "test_connection": "flext_oracle_wms.test_connection",
        "test_constants": "flext_oracle_wms.test_constants",
        "test_declarative": "flext_oracle_wms.test_declarative",
        "test_discovery": "flext_oracle_wms.test_discovery",
        "test_entity_creation": "flext_oracle_wms.test_models",
        "test_filtering": "flext_oracle_wms.test_filtering",
        "test_helpers": "flext_oracle_wms.test_helpers",
        "test_helpers_core": "flext_oracle_wms.test_helpers_core",
        "test_models": "flext_oracle_wms.test_models",
        "test_real_connection": "flext_oracle_wms.test_connection",
        "test_schema_dynamic": "flext_oracle_wms.test_schema_dynamic",
        "test_singer_flattening": "flext_oracle_wms.test_singer_flattening",
        "test_unified_config": "flext_oracle_wms.test_unified_config",
        "test_wms_api": "flext_oracle_wms.test_wms_api",
        "test_wms_client": "flext_oracle_wms.test_wms_client",
        "typings": "flext_oracle_wms.typings",
        "u": ("flext_oracle_wms.utilities", "FlextOracleWmsTestUtilities"),
        "unit": "flext_oracle_wms.unit",
        "utilities": "flext_oracle_wms.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
