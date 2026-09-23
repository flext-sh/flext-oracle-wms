# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_api import api, cli, core, d, h, lazy_attribute, r, s, services, web, x

    from flext_oracle_wms import c, config, e, m, main, oracle_wms, p, settings, t, u


__all__: tuple[str, ...] = (
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "lazy_attribute",
    "m",
    "main",
    "oracle_wms",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "web",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "flext_api": (
                "api",
                "cli",
                "core",
                "d",
                "h",
                "lazy_attribute",
                "r",
                "s",
                "services",
                "web",
                "x",
            ),
            "flext_oracle_wms": (
                "c",
                "config",
                "e",
                "m",
                "main",
                "oracle_wms",
                "p",
                "settings",
                "t",
                "u",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
