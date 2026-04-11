# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.models import m
    from flext_core.result import r
    from flext_core.service import s
    from flext_oracle_wms.constants import c
    from flext_oracle_wms.protocols import p
    from flext_oracle_wms.typings import t
    from flext_oracle_wms.utilities import u
_LAZY_IMPORTS = merge_lazy_imports(
    (".tests",),
    build_lazy_import_map(
        {
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.models": ("m",),
            "flext_core.result": ("r",),
            "flext_core.service": ("s",),
            "flext_oracle_wms.constants": ("c",),
            "flext_oracle_wms.protocols": ("p",),
            "flext_oracle_wms.typings": ("t",),
            "flext_oracle_wms.utilities": ("u",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]
