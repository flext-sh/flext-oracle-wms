"""Test fixtures for flext-oracle-wms based on WORKING code patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from flext_oracle_wms import FlextOracleWmsSettings


@pytest.fixture(scope="session")
def load_test_env() -> bool:
    """Load test environment - EXACTLY like working basic_usage.py example."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        return True
    return False


@pytest.fixture
def mock_config() -> FlextOracleWmsSettings:
    """Mock configuration for unit testing."""
    return FlextOracleWmsSettings.testing_config()


@pytest.fixture
def real_config(_load_test_env: bool) -> FlextOracleWmsSettings:
    """Real config from .env - EXACTLY like working basic_usage.py example."""
    base_url = os.getenv("ORACLE_WMS_BASE_URL") or os.getenv(
        "FLEXT_ORACLE_WMS_BASE_URL",
    )
    username = os.getenv("ORACLE_WMS_USERNAME") or os.getenv(
        "FLEXT_ORACLE_WMS_USERNAME",
    )
    password = os.getenv("ORACLE_WMS_PASSWORD") or os.getenv(
        "FLEXT_ORACLE_WMS_PASSWORD",
    )

    if not all([base_url, username, password]):
        pytest.skip("Real Oracle WMS credentials not available in .env")

    assert base_url is not None
    assert username is not None
    assert password is not None

    return FlextOracleWmsSettings(
        oracle_wms_base_url=base_url,
        oracle_wms_username=username,
        oracle_wms_password=password,
        oracle_wms_timeout=int(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
        oracle_wms_max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )


@pytest.fixture
def sample_entities() -> list[str]:
    """Sample entity names based on REAL discovery results."""
    return [
        "action_code",  # Real entity discovered
        "company",  # Real entity discovered
        "facility",  # Real entity discovered
        "item",  # Real entity discovered
        "order_hdr",  # Real entity discovered
        "order_dtl",  # Real entity discovered
    ]


@pytest.fixture
def sample_entity_data() -> dict[str, object]:
    """Sample entity response data based on REAL query results."""
    return {
        "result_count": 4,
        "page_count": 1,
        "page_nbr": 1,
        "next_page": None,
        "previous_page": None,
        "results": [
            {"id": 1, "code": "TEST_CODE", "description": "Test Record"},
            {"id": 2, "code": "TEST_CODE_2", "description": "Test Record 2"},
        ],
    }


# Configure pytest markers
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
