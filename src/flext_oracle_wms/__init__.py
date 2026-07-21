# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package."""

from __future__ import annotations

from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from flext_api import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_oracle_wms._config import (
        FlextOracleWmsConfig as FlextOracleWmsConfig,
        config as config,
    )
    from flext_oracle_wms._settings import (
        FlextOracleWmsSettings as FlextOracleWmsSettings,
        settings as settings,
    )
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
        p,
    )
    from flext_oracle_wms.typings import (
        FlextOracleWmsTypes as FlextOracleWmsTypes,
        t as t,
    )
    from flext_oracle_wms.utilities import (
        FlextOracleWmsUtilities as FlextOracleWmsUtilities,
        FlextOracleWmsUtilitiesAuth as FlextOracleWmsUtilitiesAuth,
        FlextOracleWmsUtilitiesClient as FlextOracleWmsUtilitiesClient,
        FlextOracleWmsUtilitiesDiscovery as FlextOracleWmsUtilitiesDiscovery,
        FlextOracleWmsUtilitiesFiltering as FlextOracleWmsUtilitiesFiltering,
        FlextOracleWmsUtilitiesHttpClient as FlextOracleWmsUtilitiesHttpClient,
        u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._config": ("FlextOracleWmsConfig", "config"),
        "._settings": ("FlextOracleWmsSettings", "settings"),
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
        ".typings": (
            "FlextOracleWmsTypes",
            "t",
        ),
        ".utilities": (
            "FlextOracleWmsUtilities",
            "FlextOracleWmsUtilitiesAuth",
            "FlextOracleWmsUtilitiesClient",
            "FlextOracleWmsUtilitiesDiscovery",
            "FlextOracleWmsUtilitiesFiltering",
            "FlextOracleWmsUtilitiesHttpClient",
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
    "FlextOracleWmsConfig",
    "FlextOracleWmsConstants",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
