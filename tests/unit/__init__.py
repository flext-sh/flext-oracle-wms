# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit tests for flext-oracle-wms modules.

Each test file corresponds to a specific module following the pattern:
test_[module].py for the FlextOracleWms[Module] class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import (
        test_api as test_api,
        test_config as test_config,
        test_constants as test_constants,
        test_wms_api as test_wms_api,
        test_wms_client as test_wms_client,
    )
    from tests.unit.test_api import TestFlextOracleWmsApi as TestFlextOracleWmsApi
    from tests.unit.test_config import (
        TestFlextOracleWmsSettings as TestFlextOracleWmsSettings,
    )
    from tests.unit.test_constants import (
        TestFlextOracleWmsConstants as TestFlextOracleWmsConstants,
    )
    from tests.unit.test_wms_client import (
        TestFlextOracleWmsClient as TestFlextOracleWmsClient,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestFlextOracleWmsApi": ["tests.unit.test_api", "TestFlextOracleWmsApi"],
    "TestFlextOracleWmsClient": [
        "tests.unit.test_wms_client",
        "TestFlextOracleWmsClient",
    ],
    "TestFlextOracleWmsConstants": [
        "tests.unit.test_constants",
        "TestFlextOracleWmsConstants",
    ],
    "TestFlextOracleWmsSettings": [
        "tests.unit.test_config",
        "TestFlextOracleWmsSettings",
    ],
    "test_api": ["tests.unit.test_api", ""],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_wms_api": ["tests.unit.test_wms_api", ""],
    "test_wms_client": ["tests.unit.test_wms_client", ""],
}

_EXPORTS: Sequence[str] = [
    "TestFlextOracleWmsApi",
    "TestFlextOracleWmsClient",
    "TestFlextOracleWmsConstants",
    "TestFlextOracleWmsSettings",
    "test_api",
    "test_config",
    "test_constants",
    "test_wms_api",
    "test_wms_client",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
