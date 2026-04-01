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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.unit.test_api import *
    from tests.unit.test_config import *
    from tests.unit.test_constants import *
    from tests.unit.test_wms_client import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestFlextOracleWmsApi": "tests.unit.test_api",
    "TestFlextOracleWmsClient": "tests.unit.test_wms_client",
    "TestFlextOracleWmsConstants": "tests.unit.test_constants",
    "TestFlextOracleWmsSettings": "tests.unit.test_config",
    "test_api": "tests.unit.test_api",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_wms_api": "tests.unit.test_wms_api",
    "test_wms_client": "tests.unit.test_wms_client",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
