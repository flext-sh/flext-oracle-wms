# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "test_api": "tests.unit.test_api",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_wms_api": "tests.unit.test_wms_api",
    "test_wms_client": "tests.unit.test_wms_client",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
