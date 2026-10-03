# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
from flext_oracle_wms.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_api import d, h, r, s, x

    from flext_oracle_wms._config import FlextOracleWmsConfig, config
    from flext_oracle_wms._settings import FlextOracleWmsSettings, settings
    from flext_oracle_wms.api import FlextOracleWmsApi, oracle_wms
    from flext_oracle_wms.cli import main
    from flext_oracle_wms.constants import FlextOracleWmsConstants, c
    from flext_oracle_wms.errors import FlextOracleWmsErrors, e
    from flext_oracle_wms.models import FlextOracleWmsModels, m
    from flext_oracle_wms.protocols import FlextOracleWmsProtocols, p
    from flext_oracle_wms.typings import FlextOracleWmsTypes, t
    from flext_oracle_wms.utilities import (
        FlextOracleWmsUtilities,
        FlextOracleWmsUtilitiesAuth,
        FlextOracleWmsUtilitiesClient,
        FlextOracleWmsUtilitiesDiscovery,
        FlextOracleWmsUtilitiesFiltering,
        FlextOracleWmsUtilitiesHttpClient,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextOracleWmsApi",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConstants",
    "FlextOracleWmsErrors",
    "FlextOracleWmsModels",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSettings",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "oracle_wms",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextOracleWmsConfig", "config"),
            "._settings": ("FlextOracleWmsSettings", "settings"),
            ".api": ("FlextOracleWmsApi", "oracle_wms"),
            ".cli": ("main",),
            ".constants": ("FlextOracleWmsConstants", "c"),
            ".errors": ("FlextOracleWmsErrors", "e"),
            ".models": ("FlextOracleWmsModels", "m"),
            ".protocols": ("FlextOracleWmsProtocols", "p"),
            ".typings": ("FlextOracleWmsTypes", "t"),
            ".utilities": (
                "FlextOracleWmsUtilities",
                "FlextOracleWmsUtilitiesAuth",
                "FlextOracleWmsUtilitiesClient",
                "FlextOracleWmsUtilitiesDiscovery",
                "FlextOracleWmsUtilitiesFiltering",
                "FlextOracleWmsUtilitiesHttpClient",
                "u",
            ),
            "flext_api": ("d", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
