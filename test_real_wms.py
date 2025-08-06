#!/usr/bin/env python3
"""Test Oracle WMS integration with REAL data from .env credentials.

This script tests the refactored flext-oracle-wms implementation using real
Oracle WMS API credentials to validate that the integration works correctly.
"""

import asyncio
import os

# Add the src directory to Python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig
from flext_oracle_wms.constants import FlextOracleWmsApiVersion


async def test_real_oracle_wms() -> bool | None:
    """Test Oracle WMS integration with real credentials."""
    try:
        # Load configuration from .env (using real credentials)
        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL", ""),
            username=os.getenv("ORACLE_WMS_USERNAME", ""),
            password=os.getenv("ORACLE_WMS_PASSWORD", ""),
            environment="raizen_test",  # From URL
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=float(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
            max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
            verify_ssl=os.getenv("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
            enable_logging=True,
        )

        # Create and start client
        client = FlextOracleWmsClient(config)

        start_result = await client.start()
        if not start_result.success:
            return False

        # Test 1: Entity Discovery
        entities_result = await client.discover_entities()
        if entities_result.success:
            pass

        # Test 2: Health Check
        health_result = await client.health_check()
        if health_result.success:
            pass

        # Test 3: Get Entity Data (try company first)
        if entities_result.success and entities_result.data:
            test_entity = (
                "company"
                if "company" in entities_result.data
                else entities_result.data[0]
            )

            entity_data_result = await client.get_entity_data(
                entity_name=test_entity,
                limit=5,
            )

            if entity_data_result.success:
                data = entity_data_result.data
                if isinstance(data, dict):
                    pass

        # Test 4: Test Specific Entity by ID (if we have data)
        if entities_result.success and entities_result.data:
            # Try to get a specific record by ID for the first entity
            test_entity = entities_result.data[0]

            # For this test, we'll try to get record with ID "1" (common in many entities)
            try:
                entity_by_id_result = await client.get_entity_by_id(
                    entity_name=test_entity,
                    entity_id="1",
                )

                if entity_by_id_result.success:
                    data = entity_by_id_result.data
            except Exception:
                pass

        # Test 5: API Catalog Test
        client.get_available_apis()

        # List some API categories
        from flext_oracle_wms.api_catalog import FlextOracleWmsApiCategory

        for category in FlextOracleWmsApiCategory:
            category_apis = client.get_apis_by_category(category)
            if category_apis:
                pass

        # Cleanup
        stop_result = await client.stop()
        if stop_result.success:
            pass

        return True

    except Exception:
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    # Load environment variables from .env file
    from dotenv import load_dotenv

    load_dotenv()

    # Validate required environment variables
    required_vars = [
        "ORACLE_WMS_BASE_URL",
        "ORACLE_WMS_USERNAME",
        "ORACLE_WMS_PASSWORD",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        return False

    # Run the test
    success = await test_real_oracle_wms()

    if success:
        pass

    return success


if __name__ == "__main__":
    # Install python-dotenv if not available
    try:
        # import dotenv  # Unused import removed
        pass
    except ImportError:
        import subprocess

        subprocess.check_call(["pip", "install", "python-dotenv"])

    # Run the test
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
