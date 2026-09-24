# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, c, d, e, h, r, td, tf, tk, tm, tv, x

    from . import unit
    from .base import (
        TestsFlextOracleWmsServiceBase,
        TestsFlextOracleWmsServiceBase as s,
    )
    from .constants import TestsFlextOracleWmsConstants
    from .models import TestsFlextOracleWmsModels, m
    from .protocols import TestsFlextOracleWmsProtocols, p
    from .settings import TestsFlextOracleWmsSettings
    from .typings import TestsFlextOracleWmsTypes, t
    from .utilities import TestsFlextOracleWmsUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsServiceBase",
    "TestsFlextOracleWmsSettings",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
    "api",
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
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextOracleWmsServiceBase", "s"),
            ".constants": ("TestsFlextOracleWmsConstants",),
            ".models": ("TestsFlextOracleWmsModels", "m"),
            ".protocols": ("TestsFlextOracleWmsProtocols", "p"),
            ".settings": ("TestsFlextOracleWmsSettings",),
            ".typings": ("TestsFlextOracleWmsTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextOracleWmsUtilities", "u"),
            "flext_tests": (
                "api",
                "c",
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
