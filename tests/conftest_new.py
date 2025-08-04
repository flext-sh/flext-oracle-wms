"""Test fixtures for flext-oracle-wms based on WORKING code patterns."""

import os
from pathlib import Path

import pytest

from flext_oracle_wms import (
    FlextOracleWmsClientConfig,
)
from flext_oracle_wms.api_catalog import FlextOracleWmsApiVersion


@pytest.fixture(scope="session")
def load_test_env() -> bool:
    """Load test environment - EXACTLY like working basic_usage.py example."""
    try:
        from dotenv import load_dotenv

        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            return True
    except ImportError:
        pass
    return False


@pytest.fixture
def mock_config():
    """Mock configuration for unit testing."""
    return FlextOracleWmsClientConfig(
        base_url="https://test.wms.oraclecloud.com/test_env",
        username="test_user",
        password="test_password",
        environment="test_env",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )


@pytest.fixture
def real_config(load_test_env):
    """Real config from .env - EXACTLY like working basic_usage.py example."""
    base_url = os.getenv("ORACLE_WMS_BASE_URL") or os.getenv(
        "FLEXT_ORACLE_WMS_BASE_URL"
    )
    username = os.getenv("ORACLE_WMS_USERNAME") or os.getenv(
        "FLEXT_ORACLE_WMS_USERNAME"
    )
    password = os.getenv("ORACLE_WMS_PASSWORD") or os.getenv(
        "FLEXT_ORACLE_WMS_PASSWORD"
    )

    if not all([base_url, username, password]):
        pytest.skip("Real Oracle WMS credentials not available in .env")

    return FlextOracleWmsClientConfig(
        base_url=base_url,
        username=username,
        password=password,
        environment=os.getenv("ORACLE_WMS_ENVIRONMENT", "raizen_test"),
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=float(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
        max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
        verify_ssl=True,
        enable_logging=True,
    )


@pytest.fixture
def sample_entities():
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
def sample_entity_data():
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
def pytest_configure(config) -> None:
    """Configure pytest markers for test categorization."""
    config.addinivalue_line("markers", "unit: Unit tests (fast)")
    config.addinivalue_line(
        "markers", "integration: Integration tests with real Oracle"
    )
    config.addinivalue_line("markers", "real: Tests using real .env credentials")
    config.addinivalue_line("markers", "mock: Tests using mock data only")
    config.addinivalue_line("markers", "slow: Slow tests (may timeout)")
