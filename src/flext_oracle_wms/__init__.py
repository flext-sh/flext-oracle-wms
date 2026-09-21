# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_api import s

    from flext_core import d, h, r, x

    from .__version__ import FlextOracleWmsVersion
    from ._config import FlextOracleWmsConfig, config
    from ._settings import FlextOracleWmsSettings, settings
    from .api import FlextOracleWmsApi, oracle_wms
    from .constants import FlextOracleWmsConstants, FlextOracleWmsConstants as c
    from .errors import FlextOracleWmsErrors, e
    from .models import FlextOracleWmsModels, FlextOracleWmsModels as m
    from .protocols import FlextOracleWmsProtocols, FlextOracleWmsProtocols as p
    from .typings import FlextOracleWmsTypes, FlextOracleWmsTypes as t
    from .utilities import (
        FlextOracleWmsUtilities,
        FlextOracleWmsUtilities as u,
        FlextOracleWmsUtilitiesAuth,
        FlextOracleWmsUtilitiesClient,
        FlextOracleWmsUtilitiesDiscovery,
        FlextOracleWmsUtilitiesFiltering,
        FlextOracleWmsUtilitiesHttpClient,
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
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
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
            ".__version__": ("FlextOracleWmsVersion",),
            "._config": ("FlextOracleWmsConfig", "config"),
            "._settings": ("FlextOracleWmsSettings", "settings"),
            ".api": ("FlextOracleWmsApi", "oracle_wms"),
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
            "flext_api": ("s",),
            "flext_core": ("d", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
