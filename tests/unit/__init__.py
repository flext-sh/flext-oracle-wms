# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from tests.unit.test_api import TestsFlextOracleWmsApi
    from tests.unit.test_authentication import TestsFlextOracleWmsAuthentication
    from tests.unit.test_authentication_core import (
        TestsFlextOracleWmsAuthenticationCore,
    )
    from tests.unit.test_client import TestsFlextOracleWmsClient
    from tests.unit.test_client_class import TestsFlextOracleWmsClientClass
    from tests.unit.test_client_core import TestsFlextOracleWmsClientCore
    from tests.unit.test_config import TestsFlextOracleWmsConfig
    from tests.unit.test_config_domains import TestsFlextOracleWmsConfigDomains
    from tests.unit.test_config_module import TestsFlextOracleWmsConfigModule
    from tests.unit.test_connection import TestsFlextOracleWmsConnection
    from tests.unit.test_constants import TestsFlextOracleWmsConstantsUnit
    from tests.unit.test_discovery import TestsFlextOracleWmsDiscovery
    from tests.unit.test_filtering import TestsFlextOracleWmsFiltering
    from tests.unit.test_helpers import TestsFlextOracleWmsHelpers
    from tests.unit.test_helpers_core import TestsFlextOracleWmsHelpersCore
    from tests.unit.test_models import TestsFlextOracleWmsModelsUnit
    from tests.unit.test_schema_dynamic import TestsFlextOracleWmsSchemaDynamic
    from tests.unit.test_singer_flattening import TestsFlextOracleWmsSingerFlattening
    from tests.unit.test_unified_config import TestsFlextOracleWmsUnifiedConfig
    from tests.unit.test_wms_client import TestsFlextOracleWmsWmsClient


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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
