# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_api import api, d, h, r, s, web, x

    from flext_oracle_wms.__version__ import (
        FlextOracleWmsVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
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
    "FlextOracleWmsVersion",
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
    "u",
    "web",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextOracleWmsApi": ".api",
        "FlextOracleWmsConfig": "._config",
        "FlextOracleWmsConstants": ".constants",
        "FlextOracleWmsErrors": ".errors",
        "FlextOracleWmsModels": ".models",
        "FlextOracleWmsProtocols": ".protocols",
        "FlextOracleWmsSettings": "._settings",
        "FlextOracleWmsTypes": ".typings",
        "FlextOracleWmsUtilities": ".utilities",
        "FlextOracleWmsUtilitiesAuth": ".utilities",
        "FlextOracleWmsUtilitiesClient": ".utilities",
        "FlextOracleWmsUtilitiesDiscovery": ".utilities",
        "FlextOracleWmsUtilitiesFiltering": ".utilities",
        "FlextOracleWmsUtilitiesHttpClient": ".utilities",
        "FlextOracleWmsVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "api": "flext_api",
        "c": ".constants",
        "config": "._config",
        "d": "flext_api",
        "e": ".errors",
        "h": "flext_api",
        "m": ".models",
        "main": ".cli",
        "oracle_wms": ".api",
        "p": ".protocols",
        "r": "flext_api",
        "s": "flext_api",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "web": "flext_api",
        "x": "flext_api",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_oracle_wms.__version__ import __version__
