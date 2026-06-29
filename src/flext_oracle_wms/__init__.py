# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_oracle_wms.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _t.TYPE_CHECKING:
    from flext_api import d as d, e as e, h as h, r as r, s as s, x as x

    from flext_oracle_wms.api import (
        FlextOracleWmsApi as FlextOracleWmsApi,
        oracle_wms as oracle_wms,
    )
    from flext_oracle_wms.constants import (
        FlextOracleWmsConstants as FlextOracleWmsConstants,
        c as c,
    )
    from flext_oracle_wms.models import (
        FlextOracleWmsModels as FlextOracleWmsModels,
        m as m,
    )
    from flext_oracle_wms.protocols import (
        FlextOracleWmsProtocols as FlextOracleWmsProtocols,
        p as p,
    )
    from flext_oracle_wms.settings import (
        FlextOracleWmsSettings as FlextOracleWmsSettings,
    )
    from flext_oracle_wms.typings import (
        FlextOracleWmsTypes as FlextOracleWmsTypes,
        t as t,
    )
    from flext_oracle_wms.utilities import (
        FlextOracleWmsUtilities as FlextOracleWmsUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextOracleWmsApi",
            "oracle_wms",
        ),
        ".constants": (
            "FlextOracleWmsConstants",
            "c",
        ),
        ".models": (
            "FlextOracleWmsModels",
            "m",
        ),
        ".protocols": (
            "FlextOracleWmsProtocols",
            "p",
        ),
        ".settings": ("FlextOracleWmsSettings",),
        ".typings": (
            "FlextOracleWmsTypes",
            "t",
        ),
        ".utilities": (
            "FlextOracleWmsUtilities",
            "u",
        ),
        "flext_api": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextOracleWmsApi",
    "FlextOracleWmsConstants",
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
    "c",
    "d",
    "e",
    "h",
    "m",
    "oracle_wms",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
