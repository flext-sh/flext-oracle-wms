# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.complete_mock_pipeline as _tests_complete_mock_pipeline

    complete_mock_pipeline = _tests_complete_mock_pipeline
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        TestsFlextOracleWmsConstants,
        TestsFlextOracleWmsConstants as c,
    )

    models = _tests_models
    import tests.oracle_wms_complete_discovery as _tests_oracle_wms_complete_discovery
    from tests.models import TestsFlextOracleWmsModels, TestsFlextOracleWmsModels as m

    oracle_wms_complete_discovery = _tests_oracle_wms_complete_discovery
    import tests.oracle_wms_focused_discovery as _tests_oracle_wms_focused_discovery

    oracle_wms_focused_discovery = _tests_oracle_wms_focused_discovery
    import tests.oracle_wms_optimized_discovery as _tests_oracle_wms_optimized_discovery

    oracle_wms_optimized_discovery = _tests_oracle_wms_optimized_discovery
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.sitecustomize as _tests_sitecustomize
    from tests.protocols import (
        TestsFlextOracleWmsProtocols,
        TestsFlextOracleWmsProtocols as p,
    )

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
    from tests.typings import TestsFlextOracleWmsTypes, TestsFlextOracleWmsTypes as t

    unit = _tests_unit
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import (
        TestsFlextOracleWmsUtilities,
        TestsFlextOracleWmsUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.unit",),
    {
        "TestsFlextOracleWmsConstants": (
            "tests.constants",
            "TestsFlextOracleWmsConstants",
        ),
        "TestsFlextOracleWmsModels": ("tests.models", "TestsFlextOracleWmsModels"),
        "TestsFlextOracleWmsProtocols": (
            "tests.protocols",
            "TestsFlextOracleWmsProtocols",
        ),
        "TestsFlextOracleWmsTypes": ("tests.typings", "TestsFlextOracleWmsTypes"),
        "TestsFlextOracleWmsUtilities": (
            "tests.utilities",
            "TestsFlextOracleWmsUtilities",
        ),
        "c": ("tests.constants", "TestsFlextOracleWmsConstants"),
        "complete_mock_pipeline": "tests.complete_mock_pipeline",
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "TestsFlextOracleWmsModels"),
        "models": "tests.models",
        "oracle_wms_complete_discovery": "tests.oracle_wms_complete_discovery",
        "oracle_wms_focused_discovery": "tests.oracle_wms_focused_discovery",
        "oracle_wms_optimized_discovery": "tests.oracle_wms_optimized_discovery",
        "p": ("tests.protocols", "TestsFlextOracleWmsProtocols"),
        "protocols": "tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "sitecustomize": "tests.sitecustomize",
        "t": ("tests.typings", "TestsFlextOracleWmsTypes"),
        "test_authentication": "tests.test_authentication",
        "test_authentication_core": "tests.test_authentication_core",
        "test_client": "tests.test_client",
        "test_client_class": "tests.test_client_class",
        "test_client_core": "tests.test_client_core",
        "test_config": "tests.test_config",
        "test_config_module": "tests.test_config_module",
        "test_connection": "tests.test_connection",
        "test_declarative": "tests.test_declarative",
        "test_discovery": "tests.test_discovery",
        "test_filtering": "tests.test_filtering",
        "test_helpers": "tests.test_helpers",
        "test_helpers_core": "tests.test_helpers_core",
        "test_models": "tests.test_models",
        "test_schema_dynamic": "tests.test_schema_dynamic",
        "test_singer_flattening": "tests.test_singer_flattening",
        "test_unified_config": "tests.test_unified_config",
        "typings": "tests.typings",
        "u": ("tests.utilities", "TestsFlextOracleWmsUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
    "c",
    "complete_mock_pipeline",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "oracle_wms_complete_discovery",
    "oracle_wms_focused_discovery",
    "oracle_wms_optimized_discovery",
    "p",
    "protocols",
    "r",
    "s",
    "sitecustomize",
    "t",
    "test_authentication",
    "test_authentication_core",
    "test_client",
    "test_client_class",
    "test_client_core",
    "test_config",
    "test_config_module",
    "test_connection",
    "test_declarative",
    "test_discovery",
    "test_filtering",
    "test_helpers",
    "test_helpers_core",
    "test_models",
    "test_schema_dynamic",
    "test_singer_flattening",
    "test_unified_config",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
