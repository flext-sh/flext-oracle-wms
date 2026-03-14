# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit tests for flext-oracle-wms modules.

Each test file corresponds to a specific module following the pattern:
test_[module].py for the FlextOracleWms[Module] class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from tests.unit.test_config import TestFlextOracleWmsSettings
    from tests.unit.test_constants import (
        TestFlextOracleWmsConstants,
        TestFlextOracleWmsConstants as c,
    )
    from tests.unit.test_wms_api import TestFlextOracleWmsApi
    from tests.unit.test_wms_client import TestFlextOracleWmsClient

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestFlextOracleWmsApi": ("tests.unit.test_wms_api", "TestFlextOracleWmsApi"),
    "TestFlextOracleWmsClient": (
        "tests.unit.test_wms_client",
        "TestFlextOracleWmsClient",
    ),
    "TestFlextOracleWmsConstants": (
        "tests.unit.test_constants",
        "TestFlextOracleWmsConstants",
    ),
    "TestFlextOracleWmsSettings": (
        "tests.unit.test_config",
        "TestFlextOracleWmsSettings",
    ),
    "c": ("tests.unit.test_constants", "TestFlextOracleWmsConstants"),
}

__all__ = [
    "TestFlextOracleWmsApi",
    "TestFlextOracleWmsClient",
    "TestFlextOracleWmsConstants",
    "TestFlextOracleWmsSettings",
    "c",
]


def __getattr__(name: str) -> t.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
