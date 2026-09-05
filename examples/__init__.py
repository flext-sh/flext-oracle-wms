# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import tests as tests
    # Why: mro-4p0t — these are flext_oracle_wms's own re-exports, not
    # flext_core's (flext-oracle-wms-1sm3w toolchain sync fix).
    from flext_oracle_wms import (
        FlextOracleWmsConstants,
        FlextOracleWmsConstants as c,
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        t,
        u,
        x,
    )

    from .constants import ExamplesFlextOracleWmsConstants
    from .models import ExamplesFlextOracleWmsModels
    from .protocols import ExamplesFlextOracleWmsProtocols
    from .typings import ExamplesFlextOracleWmsTypes
    from .utilities import ExamplesFlextOracleWmsUtilities
__all__: tuple[str, ...] = (
    "ExamplesFlextOracleWmsConstants",
    "ExamplesFlextOracleWmsModels",
    "ExamplesFlextOracleWmsProtocols",
    "ExamplesFlextOracleWmsTypes",
    "ExamplesFlextOracleWmsUtilities",
    "FlextOracleWmsConstants",
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
            ".constants": ("ExamplesFlextOracleWmsConstants",),
            ".models": ("ExamplesFlextOracleWmsModels",),
            ".protocols": ("ExamplesFlextOracleWmsProtocols",),
            ".tests": ("tests",),
            ".typings": ("ExamplesFlextOracleWmsTypes",),
            ".utilities": ("ExamplesFlextOracleWmsUtilities",),
            "flext_oracle_wms": (
                "FlextOracleWmsConstants",
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
