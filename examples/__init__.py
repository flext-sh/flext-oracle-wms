# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_api import s

    from flext_oracle_wms import (
        api,
        c,
        config,
        d,
        e,
        h,
        m,
        main,
        oracle_wms,
        p,
        r,
        settings,
        t,
        u,
        web,
        x,
    )


__all__: tuple[str, ...] = (
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
        "api": "flext_oracle_wms",
        "c": "flext_oracle_wms",
        "config": "flext_oracle_wms",
        "d": "flext_oracle_wms",
        "e": "flext_oracle_wms",
        "h": "flext_oracle_wms",
        "m": "flext_oracle_wms",
        "main": "flext_oracle_wms",
        "oracle_wms": "flext_oracle_wms",
        "p": "flext_oracle_wms",
        "r": "flext_oracle_wms",
        "s": "flext_api",
        "settings": "flext_oracle_wms",
        "t": "flext_oracle_wms",
        "u": "flext_oracle_wms",
        "web": "flext_oracle_wms",
        "x": "flext_oracle_wms",
    }),
    public_exports=__all__,
)
