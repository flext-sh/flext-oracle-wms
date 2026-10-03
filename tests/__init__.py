# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, h, r, td, tf, tk, tm, x

    from flext_oracle_wms import e
    from tests import unit
    from tests.base import TestsFlextOracleWmsServiceBase, s
    from tests.constants import TestsFlextOracleWmsConstants, c
    from tests.models import TestsFlextOracleWmsModels, m
    from tests.protocols import TestsFlextOracleWmsProtocols, p
    from tests.settings import TestsFlextOracleWmsSettings
    from tests.typings import TestsFlextOracleWmsTypes, t
    from tests.utilities import TestsFlextOracleWmsUtilities, u


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
    "u",
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
            "flext_oracle_wms": ("e",),
            "flext_tests": ("api", "d", "h", "r", "td", "tf", "tk", "tm", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
