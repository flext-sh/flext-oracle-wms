# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_api import TestsFlextOracleWmsApi
    from .test_authentication import TestsFlextOracleWmsAuthentication
    from .test_authentication_core import TestsFlextOracleWmsAuthenticationCore
    from .test_client import TestsFlextOracleWmsClient
    from .test_client_class import TestsFlextOracleWmsClientClass
    from .test_client_core import TestsFlextOracleWmsClientCore
    from .test_config import TestsFlextOracleWmsConfig
    from .test_config_domains import TestsFlextOracleWmsConfigDomains
    from .test_config_module import TestsFlextOracleWmsConfigModule
    from .test_connection import TestsFlextOracleWmsConnection
    from .test_constants import TestsFlextOracleWmsConstantsUnit
    from .test_discovery import TestsFlextOracleWmsDiscovery
    from .test_filtering import TestsFlextOracleWmsFiltering
    from .test_helpers import TestsFlextOracleWmsHelpers
    from .test_helpers_core import TestsFlextOracleWmsHelpersCore
    from .test_models import TestsFlextOracleWmsModelsUnit
    from .test_schema_dynamic import TestsFlextOracleWmsSchemaDynamic
    from .test_singer_flattening import TestsFlextOracleWmsSingerFlattening
    from .test_unified_config import TestsFlextOracleWmsUnifiedConfig
    from .test_wms_client import TestsFlextOracleWmsWmsClient
__all__: tuple[str, ...] = (
    "TestsFlextOracleWmsApi",
    "TestsFlextOracleWmsAuthentication",
    "TestsFlextOracleWmsAuthenticationCore",
    "TestsFlextOracleWmsClient",
    "TestsFlextOracleWmsClientClass",
    "TestsFlextOracleWmsClientCore",
    "TestsFlextOracleWmsConfig",
    "TestsFlextOracleWmsConfigDomains",
    "TestsFlextOracleWmsConfigModule",
    "TestsFlextOracleWmsConnection",
    "TestsFlextOracleWmsConstantsUnit",
    "TestsFlextOracleWmsDiscovery",
    "TestsFlextOracleWmsFiltering",
    "TestsFlextOracleWmsHelpers",
    "TestsFlextOracleWmsHelpersCore",
    "TestsFlextOracleWmsModelsUnit",
    "TestsFlextOracleWmsSchemaDynamic",
    "TestsFlextOracleWmsSingerFlattening",
    "TestsFlextOracleWmsUnifiedConfig",
    "TestsFlextOracleWmsWmsClient",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_api": ("TestsFlextOracleWmsApi",),
            ".test_authentication": ("TestsFlextOracleWmsAuthentication",),
            ".test_authentication_core": ("TestsFlextOracleWmsAuthenticationCore",),
            ".test_client": ("TestsFlextOracleWmsClient",),
            ".test_client_class": ("TestsFlextOracleWmsClientClass",),
            ".test_client_core": ("TestsFlextOracleWmsClientCore",),
            ".test_config": ("TestsFlextOracleWmsConfig",),
            ".test_config_domains": ("TestsFlextOracleWmsConfigDomains",),
            ".test_config_module": ("TestsFlextOracleWmsConfigModule",),
            ".test_connection": ("TestsFlextOracleWmsConnection",),
            ".test_constants": ("TestsFlextOracleWmsConstantsUnit",),
            ".test_discovery": ("TestsFlextOracleWmsDiscovery",),
            ".test_filtering": ("TestsFlextOracleWmsFiltering",),
            ".test_helpers": ("TestsFlextOracleWmsHelpers",),
            ".test_helpers_core": ("TestsFlextOracleWmsHelpersCore",),
            ".test_models": ("TestsFlextOracleWmsModelsUnit",),
            ".test_schema_dynamic": ("TestsFlextOracleWmsSchemaDynamic",),
            ".test_singer_flattening": ("TestsFlextOracleWmsSingerFlattening",),
            ".test_unified_config": ("TestsFlextOracleWmsUnifiedConfig",),
            ".test_wms_client": ("TestsFlextOracleWmsWmsClient",),
            "flext_tests": (
                "c",
                "d",
                "e",
                "h",
                "m",
                "p",
                "r",
                "s",
                "t",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "u",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
