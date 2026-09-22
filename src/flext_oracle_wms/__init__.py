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
    from flext_api import api, s
    from flext_cli import cli
    from flext_web import main, web
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import core, d, h, lazy_attribute, r, x

    from ._config import FlextOracleWmsConfig, config
    from ._settings import FlextOracleWmsSettings, settings
    from .api import FlextOracleWmsApi, oracle_wms
    from .constants import FlextOracleWmsConstants, c
    from .errors import FlextOracleWmsErrors, e
    from .models import FlextOracleWmsModels, m
    from .protocols import FlextOracleWmsProtocols, p
    from .typings import FlextOracleWmsTypes, t
    from .utilities import FlextOracleWmsUtilities, u
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
    "cli",
    "config",
    "core",
    "d",
    "e",
    "from_json",
    "h",
    "lazy_attribute",
    "m",
    "main",
    "oracle_wms",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "to_json",
    "to_jsonable_python",
    "u",
    "web",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextOracleWmsConfig", "config"),
            "._settings": ("FlextOracleWmsSettings", "settings"),
            ".api": ("FlextOracleWmsApi", "oracle_wms"),
            ".constants": ("FlextOracleWmsConstants", "c"),
            ".errors": ("FlextOracleWmsErrors", "e"),
            ".models": ("FlextOracleWmsModels", "m"),
            ".protocols": ("FlextOracleWmsProtocols", "p"),
            ".typings": ("FlextOracleWmsTypes", "t"),
            ".utilities": ("FlextOracleWmsUtilities", "u"),
            "flext_api": ("api", "s"),
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "h", "lazy_attribute", "r", "x"),
            "flext_web": ("main", "web"),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
