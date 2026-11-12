# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, h, r, td, tf, tk, tm, x

    from flext_oracle_wms import (
        FlextOracleWmsApi,
        FlextOracleWmsConfig,
        FlextOracleWmsConstants,
        FlextOracleWmsErrors,
        FlextOracleWmsModels,
        FlextOracleWmsModelsConfig,
        FlextOracleWmsProtocols,
        FlextOracleWmsSettings,
        FlextOracleWmsTypes,
        FlextOracleWmsUtilities,
        FlextOracleWmsUtilitiesAuth,
        FlextOracleWmsUtilitiesClient,
        FlextOracleWmsUtilitiesDiscovery,
        FlextOracleWmsUtilitiesFiltering,
        FlextOracleWmsUtilitiesHttpClient,
        FlextOracleWmsVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        e,
        main,
        oracle_wms,
        settings,
    )
    from tests.base import TestsFlextOracleWmsServiceBase, s
    from tests.constants import TestsFlextOracleWmsConstants, c
    from tests.models import TestsFlextOracleWmsModels, m
    from tests.protocols import TestsFlextOracleWmsProtocols, p
    from tests.settings import TestsFlextOracleWmsSettings
    from tests.typings import TestsFlextOracleWmsTypes, t
    from tests.utilities import TestsFlextOracleWmsUtilities, u


__all__: tuple[str, ...] = (
    "FlextOracleWmsApi",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConstants",
    "FlextOracleWmsErrors",
    "FlextOracleWmsModels",
    "FlextOracleWmsModelsConfig",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSettings",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
    "FlextOracleWmsVersion",
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsServiceBase",
    "TestsFlextOracleWmsSettings",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
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
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextOracleWmsApi": "flext_oracle_wms",
        "FlextOracleWmsConfig": "flext_oracle_wms",
        "FlextOracleWmsConstants": "flext_oracle_wms",
        "FlextOracleWmsErrors": "flext_oracle_wms",
        "FlextOracleWmsModels": "flext_oracle_wms",
        "FlextOracleWmsModelsConfig": "flext_oracle_wms",
        "FlextOracleWmsProtocols": "flext_oracle_wms",
        "FlextOracleWmsSettings": "flext_oracle_wms",
        "FlextOracleWmsTypes": "flext_oracle_wms",
        "FlextOracleWmsUtilities": "flext_oracle_wms",
        "FlextOracleWmsUtilitiesAuth": "flext_oracle_wms",
        "FlextOracleWmsUtilitiesClient": "flext_oracle_wms",
        "FlextOracleWmsUtilitiesDiscovery": "flext_oracle_wms",
        "FlextOracleWmsUtilitiesFiltering": "flext_oracle_wms",
        "FlextOracleWmsUtilitiesHttpClient": "flext_oracle_wms",
        "FlextOracleWmsVersion": "flext_oracle_wms",
        "TestsFlextOracleWmsConstants": ".constants",
        "TestsFlextOracleWmsModels": ".models",
        "TestsFlextOracleWmsProtocols": ".protocols",
        "TestsFlextOracleWmsServiceBase": ".base",
        "TestsFlextOracleWmsSettings": ".settings",
        "TestsFlextOracleWmsTypes": ".typings",
        "TestsFlextOracleWmsUtilities": ".utilities",
        "__author__": "flext_oracle_wms",
        "__author_email__": "flext_oracle_wms",
        "__description__": "flext_oracle_wms",
        "__license__": "flext_oracle_wms",
        "__title__": "flext_oracle_wms",
        "__url__": "flext_oracle_wms",
        "__version__": "flext_oracle_wms",
        "__version_info__": "flext_oracle_wms",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_oracle_wms",
        "d": "flext_tests",
        "e": "flext_oracle_wms",
        "h": "flext_tests",
        "m": ".models",
        "main": "flext_oracle_wms",
        "oracle_wms": "flext_oracle_wms",
        "p": ".protocols",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_oracle_wms",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    },
    public_exports=__all__,
)
