# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
<<<<<<< HEAD
    from flext_api import api, s
    from flext_cli import cli
    from flext_web import web

    from flext_core import (
        core,
        d,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        x,
    )
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
    "lazy",
    "lazy_attribute",
    "m",
    "main",
    "normalize_lazy_imports",
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
=======
    from flext_oracle_wms import c, d, e, h, m, p, r, s, t, u, x


__all__: tuple[str, ...] = ("c", "d", "e", "h", "m", "p", "r", "s", "t", "u", "x")
>>>>>>> recovery/rope-automation-20260921

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
<<<<<<< HEAD
            "flext_api": ("api", "s"),
            "flext_cli": ("cli",),
            "flext_core": (
                "core",
                "d",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
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
            "flext_web": ("web",),
=======
            "flext_oracle_wms": ("c", "d", "e", "h", "m", "p", "r", "s", "t", "u", "x")
>>>>>>> recovery/rope-automation-20260921
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
