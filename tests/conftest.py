"""Test fixtures for flext-oracle-wms.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from flext_oracle_wms import FlextOracleWmsSettings


@pytest.fixture
def mock_config() -> FlextOracleWmsSettings:
    """Mock configuration for unit testing."""
    return FlextOracleWmsSettings.testing_config()


@pytest.fixture(autouse=True)
def isolate_oracle_wms_env(
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    """Keep unit tests deterministic regardless of host FLEXT_ORACLE_WMS_* env."""
    if request.node.get_closest_marker("real") or request.node.get_closest_marker(
        "integration"
    ):
        return
    for key in [key for key in os.environ if key.startswith("FLEXT_ORACLE_WMS_")]:
        monkeypatch.delenv(key, raising=False)


@pytest.fixture(autouse=True)
def isolate_oracle_wms_settings_singleton() -> Iterator[None]:
    """Reset FlextOracleWmsSettings singleton state for each test."""
    FlextOracleWmsSettings._reset_instance()
    yield
    FlextOracleWmsSettings._reset_instance()
