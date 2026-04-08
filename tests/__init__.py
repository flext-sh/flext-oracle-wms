# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.constants import (
        TestsFlextOracleWmsConstants,
        TestsFlextOracleWmsConstants as c,
    )
    from tests.models import TestsFlextOracleWmsModels, TestsFlextOracleWmsModels as m
    from tests.protocols import (
        TestsFlextOracleWmsProtocols,
        TestsFlextOracleWmsProtocols as p,
    )
    from tests.typings import TestsFlextOracleWmsTypes, TestsFlextOracleWmsTypes as t
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
