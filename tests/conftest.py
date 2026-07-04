"""Test fixtures for flext-oracle-wms.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os

import pytest

from flext_oracle_wms import FlextOracleWmsSettings
from tests.typings import t

_ORACLE_WMS_ENV_PREFIX = "FLEXT_ORACLE_WMS_"
_ORACLE_WMS_ENV_SNAPSHOTS: t.MutableMappingKV[str, t.StrMapping] = {}


@pytest.fixture
def mock_config() -> FlextOracleWmsSettings:
    """Mock configuration for unit testing."""
    return FlextOracleWmsSettings.testing_config()


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Keep unit tests deterministic before each test."""
    FlextOracleWmsSettings.reset_for_testing()
    if _uses_real_or_integration_marker(item):
        return
    snapshot: t.MutableStrMapping = {
        key: value
        for key, value in os.environ.items()
        if key.startswith(_ORACLE_WMS_ENV_PREFIX)
    }
    _ORACLE_WMS_ENV_SNAPSHOTS[item.nodeid] = dict(snapshot)
    for key in snapshot:
        os.environ.pop(key, None)


def pytest_runtest_teardown(
    item: pytest.Item,
    nextitem: pytest.Item | None,
) -> None:
    """Restore Oracle WMS test isolation state after each test."""
    del nextitem
    snapshot = _ORACLE_WMS_ENV_SNAPSHOTS.pop(item.nodeid, None)
    if snapshot is not None:
        for key in [
            key for key in os.environ if key.startswith(_ORACLE_WMS_ENV_PREFIX)
        ]:
            os.environ.pop(key, None)
        os.environ.update(snapshot)
    FlextOracleWmsSettings.reset_for_testing()


def _uses_real_or_integration_marker(item: pytest.Item) -> bool:
    """Return whether a test intentionally uses real integration configuration."""
    return bool(
        item.get_closest_marker("real") or item.get_closest_marker("integration"),
    )
