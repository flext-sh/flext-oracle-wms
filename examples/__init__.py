# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_api import s
    from flext_core import d, h, r, x
    from flext_oracle_wms import c, e, m, p, t, u

    from . import tests
__all__: tuple[str, ...] = (
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "tests",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".tests": ("tests",),
            "flext_api": ("s",),
            "flext_core": ("d", "h", "r", "x"),
            "flext_oracle_wms": ("c", "e", "m", "p", "t", "u"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
