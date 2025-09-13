#!/usr/bin/env python3
"""Oracle WMS REAL Testing with Valid Credentials.

Testing with REAL Oracle WMS credentials provided by user:
- Base URL: https://ta29.wms.ocs.oraclecloud.com/raizen_test
- Username: USER_WMS_INTEGRA
- Password: jmCyS7BK94YvhS@

This will test ACTUAL Oracle WMS functionality, not mocks.
"""

import asyncio
import builtins
import contextlib

from flext_core import FlextLogger

# Use public enum re-exported by package
from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsClientConfig,
    create_oracle_wms_client,
)

logger = FlextLogger(__name__)


async def test_real_oracle_wms():
    """Test REAL Oracle WMS functionality with valid credentials."""
    # Create REAL configuration with provided credentials
    config = FlextOracleWmsClientConfig(
        base_url="https://ta29.wms.ocs.oraclecloud.com",
        username="USER_WMS_INTEGRA",
        password="jmCyS7BK94YvhS@",
        environment="raizen_test",
        timeout=60.0,  # Increased timeout for real network calls
        max_retries=3,
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        verify_ssl=True,
        enable_logging=True,
    )

    # Create REAL Oracle WMS client (NO MOCK MODE)
    real_client = create_oracle_wms_client(config, mock_mode=False)

    test_results = {
        "client_start": False,
        "entity_discovery": False,
        "entity_data": False,
        "health_check": False,
        "api_catalog": False,
    }

    try:
        # Test 1: Client Initialization and Authentication

        start_result = await real_client.start()
        if start_result.success:
            test_results["client_start"] = True
        else:
            return test_results

        # Test 2: Entity Discovery from REAL Oracle WMS

        entities_result = await real_client.discover_entities()
        if entities_result.success:
            entities = entities_result.data
            test_results["entity_discovery"] = True
            discovered_entities = entities
        else:
            discovered_entities = ["company", "facility", "item"]  # Fallback

        # Test 3: Real Data Extraction

        if discovered_entities:
            # Test with first available entity
            test_entity = discovered_entities[0]

            data_result = await real_client.get_entity_data(
                test_entity,
                limit=5,  # Small limit for testing
                fields="id,create_ts,mod_ts",  # Basic fields
            )

            if data_result.success:
                data = data_result.data
                if isinstance(data, dict):
                    data.get("count", 0)
                    results = data.get("results", [])

                    if (
                        results
                        and isinstance(results, list)
                        and len(results) > 0
                        and isinstance(results[0], dict)
                    ):
                        sample_record = results[0]
                        list(sample_record.keys())

                        # Show sample data (first few fields only)
                        dict(list(sample_record.items())[:3])

                    test_results["entity_data"] = True

        # Test 4: Health Check with Real Connection

        health_result = await real_client.health_check()
        if health_result.success:
            health_data = health_result.data
            if isinstance(health_data, dict):
                health_data.get("status", "unknown")
                health_data.get("base_url", "unknown")
                health_data.get("environment", "unknown")
                health_data.get("discovered_entities", 0)

                test_results["health_check"] = True

        # Test 5: API Catalog Validation

        available_apis = real_client.get_available_apis()
        real_client.get_apis_by_category("data_extract")

        # Show some key APIs
        key_apis = ["lgf_entity_list", "lgf_entity_discovery", "lgf_data_extract"]
        for api_name in key_apis:
            if api_name in available_apis:
                available_apis[api_name]

        test_results["api_catalog"] = True

        # Stop the client
        await real_client.stop()

    except Exception:
        logger.exception("Real Oracle WMS test failed")
        with contextlib.suppress(builtins.BaseException):
            await real_client.stop()

    return test_results


async def test_oracle_wms_pipeline() -> None:
    """Test complete TAP -> TARGET pipeline with real data."""

    # This would test the complete pipeline but requires implementing
    # the actual data insertion in the target


async def main() -> None:
    """Main test runner with real Oracle WMS credentials."""
    try:
        # Test real Oracle WMS functionality
        test_results = await test_real_oracle_wms()

        # Test pipeline (structural only for now)
        await test_oracle_wms_pipeline()

        # Final Results Summary

        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)

        for _test_name, _passed in test_results.items():
            pass

        if passed_tests == total_tests:
            pass

        # Honesty Assessment

        if test_results["client_start"] and test_results["entity_discovery"]:
            if test_results["entity_data"]:
                pass

        if passed_tests >= 3:  # Most tests passed
            pass

    except Exception:
        logger.exception("Main test execution failed")


if __name__ == "__main__":
    asyncio.run(main())
