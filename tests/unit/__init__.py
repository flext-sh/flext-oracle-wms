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
    from flext_core.typings import FlextTypes

    from .test_config import TestFlextOracleWmsSettings
    from .test_constants import TestFlextOracleWmsConstants
    from .test_wms_api import TestFlextOracleWmsApi
    from .test_wms_client import TestFlextOracleWmsClient

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
}

__all__ = [
    "TestFlextOracleWmsApi",
    "TestFlextOracleWmsClient",
    "TestFlextOracleWmsConstants",
    "TestFlextOracleWmsSettings",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
