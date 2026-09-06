# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import unit as unit
    from enum import StrEnum, unique
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x
    from typing import Final

    from .base import (
        TestsFlextOracleWmsServiceBase,
        TestsFlextOracleWmsServiceBase as s,
    )
    from .conftest import mock_config
    from .constants import (
        TestsFlextOracleWmsConstants,
        TestsFlextOracleWmsConstants as c,
    )
    from .models import TestsFlextOracleWmsModels, TestsFlextOracleWmsModels as m
    from .protocols import (
        TestsFlextOracleWmsProtocols,
        TestsFlextOracleWmsProtocols as p,
    )
    from .settings import TestsFlextOracleWmsSettings
    from .typings import TestsFlextOracleWmsTypes, TestsFlextOracleWmsTypes as t
    from .unit.complete_mock_pipeline import CompleteMockPipeline, main
    from .unit.oracle_wms_complete_discovery import (
        OracleWmsCompleteDiscovery,
        OracleWmsCompleteDiscoveryRunner,
    )
    from .unit.oracle_wms_focused_discovery import FocusedOracleWmsDiscovery
    from .unit.oracle_wms_optimized_discovery import (
        OptimizedOracleWmsDiscovery,
        OptimizedOracleWmsDiscoveryRunner,
    )
    from .utilities import (
        TestsFlextOracleWmsUtilities,
        TestsFlextOracleWmsUtilities as u,
    )
__all__: tuple[str, ...] = (
    "CompleteMockPipeline",
    "Final",
    "FlextTestsConstants",
    "FocusedOracleWmsDiscovery",
    "OptimizedOracleWmsDiscovery",
    "OptimizedOracleWmsDiscoveryRunner",
    "OracleWmsCompleteDiscovery",
    "OracleWmsCompleteDiscoveryRunner",
    "StrEnum",
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsServiceBase",
    "TestsFlextOracleWmsSettings",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "mock_config",
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
    "unique",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextOracleWmsServiceBase", "s"),
            ".conftest": ("mock_config",),
            ".constants": ("TestsFlextOracleWmsConstants", "c"),
            ".models": ("TestsFlextOracleWmsModels", "m"),
            ".protocols": ("TestsFlextOracleWmsProtocols", "p"),
            ".settings": ("TestsFlextOracleWmsSettings",),
            ".typings": ("TestsFlextOracleWmsTypes", "t"),
            ".unit": ("unit",),
            ".unit.complete_mock_pipeline": ("CompleteMockPipeline", "main"),
            ".unit.oracle_wms_complete_discovery": (
                "OracleWmsCompleteDiscovery",
                "OracleWmsCompleteDiscoveryRunner",
            ),
            ".unit.oracle_wms_focused_discovery": ("FocusedOracleWmsDiscovery",),
            ".unit.oracle_wms_optimized_discovery": (
                "OptimizedOracleWmsDiscovery",
                "OptimizedOracleWmsDiscoveryRunner",
            ),
            ".utilities": ("TestsFlextOracleWmsUtilities", "u"),
            "enum": ("StrEnum", "unique"),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "typing": ("Final",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
