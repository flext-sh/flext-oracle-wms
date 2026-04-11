"""Test fixtures for flext-oracle-wms based on WORKING code patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_oracle_wms import FlextOracleWmsSettings
from tests import t, u

pytest_plugins = ["flext_tests.conftest_plugin"]


@pytest.fixture(scope="session")
def load_test_env() -> bool:
    """Load test environment - EXACTLY like working basic_usage.py example."""
    return u.OracleWms.Tests.load_test_env(Path(__file__).parent.parent)


@pytest.fixture
def mock_config() -> FlextOracleWmsSettings:
    """Mock configuration for unit testing."""
    return FlextOracleWmsSettings.testing_config()


@pytest.fixture
def real_config(load_test_env: bool) -> FlextOracleWmsSettings:
    """Real config from .env - EXACTLY like working basic_usage.py example."""
    _ = load_test_env
    settings_result = u.OracleWms.Tests.create_real_settings()
    if settings_result.failure:
        pytest.skip(settings_result.error or "Real Oracle WMS credentials unavailable")
    return settings_result.value


@pytest.fixture
def sample_entities() -> t.StrSequence:
    """Sample entity names based on REAL discovery results."""
    return u.OracleWms.Tests.sample_entities()


@pytest.fixture
def sample_entity_data() -> t.ContainerMapping:
    """Sample entity response data based on REAL query results."""
    return u.OracleWms.Tests.sample_entity_data()


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers for test categorization."""
    config.addinivalue_line("markers", "unit: Unit tests (fast)")
    config.addinivalue_line(
        "markers",
        "integration: Integration tests with real Oracle",
    )
    config.addinivalue_line("markers", "real: Tests using real .env credentials")
    config.addinivalue_line("markers", "mock: Tests using mock data only")
    config.addinivalue_line("markers", "slow: Slow tests (may timeout)")
