# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from enum import StrEnum, unique
    from typing import Final

    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from . import unit as unit
    from .base import (
        TestsFlextOracleWmsServiceBase,
        TestsFlextOracleWmsServiceBase as s,
    )
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
    from .utilities import (
        TestsFlextOracleWmsUtilities,
        TestsFlextOracleWmsUtilities as u,
    )
__all__: tuple[str, ...] = (
    "Final",
    "FlextTestsConstants",
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
            ".constants": ("TestsFlextOracleWmsConstants", "c"),
            ".models": ("TestsFlextOracleWmsModels", "m"),
            ".protocols": ("TestsFlextOracleWmsProtocols", "p"),
            ".settings": ("TestsFlextOracleWmsSettings",),
            ".typings": ("TestsFlextOracleWmsTypes", "t"),
            ".unit": ("unit",),
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
