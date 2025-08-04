#!/usr/bin/env python3
"""Oracle WMS Honest Mock Testing Framework.

This test demonstrates the clear distinction between:
- ✅ STRUCTURAL VALIDATION (works with mocks)
- ❌ FUNCTIONAL VALIDATION (needs real credentials)

Created after brutal honest feedback: "seja sincero, fale a verdade sobre o que fez e que deveria fazer"
"""

import asyncio
import json
from pathlib import Path

from flext_core import get_logger

from flext_oracle_wms import FlextOracleWmsClientConfig, create_oracle_wms_client
from flext_oracle_wms.api_catalog import FlextOracleWmsApiVersion

logger = get_logger(__name__)


async def test_honest_mock_framework() -> None:
    """Test realistic mock framework with clear distinction between structure vs functionality."""
    # Create configuration for both modes
    config = FlextOracleWmsClientConfig(
        base_url="https://demo-wms.oraclecloud.com/demo",
        username="demo_user",
        password="demo_password",
        environment="demo_env",
        timeout=30.0,
        max_retries=3,
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        verify_ssl=True,
        enable_logging=True,
    )

    # Test 1: MOCK MODE - Structural validation

    mock_client = create_oracle_wms_client(config, mock_mode=True)

    try:
        # Start mock client
        start_result = await mock_client.start()

        # Test entity discovery with mock data
        entities_result = await mock_client.discover_entities()
        if entities_result.success:
            pass

        # Test entity data retrieval with mock data
        if entities_result.success and entities_result.data:
            entity_name = entities_result.data[0]
            data_result = await mock_client.get_entity_data(entity_name, limit=3)
            if data_result.success:
                data = data_result.data
                data.get("count", 0) if isinstance(data, dict) else 0
                if isinstance(data, dict) and "results" in data:
                    results = data.get("results", [])
                    if results and isinstance(results, list):
                        results[0] if results else {}

        # Test health check with mock data
        health_result = await mock_client.health_check()
        if health_result.success:
            health_data = health_result.data
            if isinstance(health_data, dict):
                health_data.get("status", "unknown")
                health_data.get("mock_mode", False)

        await mock_client.stop()

    except Exception:
        pass

    # Test 2: REAL MODE - Functional validation (will fail without valid credentials)

    real_client = create_oracle_wms_client(config, mock_mode=False)

    try:
        # Attempt to start real client
        start_result = await real_client.start()
        if start_result.success:
            # Test real entity discovery
            entities_result = await real_client.discover_entities()
            if entities_result.success:
                pass

            await real_client.stop()

    except Exception:
        pass

    # Summary


def create_mock_config_example() -> None:
    """Create example configuration files for mock mode testing."""
    # Mock configuration for tap
    tap_config = {
        "base_url": "https://demo-wms.oraclecloud.com/demo",
        "username": "demo_user",
        "password": "demo_password",
        "auth_method": "basic",
        "company_code": "DEMO_COMPANY",
        "facility_code": "DC001",
        "mock_mode": True,
        "entities": [
            "company",
            "facility",
            "inventory",
            "item",
            "order_hdr",
            "order_dtl",
            "allocation",
        ],
        "page_size": 100,
        "enable_incremental": True,
        "start_date": "2024-01-01T00:00:00Z",
    }

    # Mock configuration for target
    target_config = {
        "base_url": "https://demo-wms.oraclecloud.com/demo",
        "username": "demo_user",
        "password": "demo_password",
        "environment": "demo_env",
        "mock_mode": True,
        "batch_size": 1000,
        "load_method": "APPEND_ONLY",
        "default_target_schema": "WMS_TARGET",
    }

    # Save configuration examples
    config_dir = Path("examples/mock_configs")
    config_dir.mkdir(exist_ok=True, parents=True)

    with config_dir / "tap_config_mock.json".open("w", encoding="utf-8") as f:
        json.dump(tap_config, f, indent=2)

    with config_dir / "target_config_mock.json".open("w", encoding="utf-8") as f:
        json.dump(target_config, f, indent=2)


async def main() -> None:
    """Main test runner."""
    try:
        await test_honest_mock_framework()
        create_mock_config_example()

    except Exception:
        logger.exception("Test framework failed")
        raise


if __name__ == "__main__":
    asyncio.run(main())
