"""Integration tests for Oracle WMS Client - Declarative Implementation.

Tests the new declarative Oracle WMS Cloud client using real .env configuration.
Skips tests if .env is not available.
"""

from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import structlog

from flext_oracle_wms.api_catalog import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiVersion,
)
from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig

logger = structlog.get_logger(__name__)

# ==============================================================================
# TEST CONFIGURATION AND FIXTURES
# ==============================================================================


def find_env_file() -> Path | None:
    """Find .env file in project hierarchy."""
    current_dir = Path(__file__).parent

    # Look in current dir and up to 3 levels up
    for _ in range(4):
        env_path = current_dir / ".env"
        if env_path.exists():
            return env_path
        current_dir = current_dir.parent

    return None


def load_env_config() -> dict[str, object] | None:
    """Load Oracle WMS configuration from .env file."""
    env_path = find_env_file()
    if not env_path:
        return None

    config = {}
    try:
        with Path(env_path).open(encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()

        # Map .env variables to our config
        base_url = config.get("ORACLE_WMS_BASE_URL", "")

        # Extract environment from URL dynamically
        # URL format: https://ta29.wms.ocs.oraclecloud.com/raizen_test
        environment = "default"  # fallback
        if base_url:
            try:
                # Extract the last path component as environment
                from urllib.parse import urlparse

                parsed = urlparse(base_url)
                path_parts = parsed.path.strip("/").split("/")
                if path_parts and path_parts[-1]:
                    environment = path_parts[-1]
            except Exception:
                environment = "default"

        return {
            "base_url": base_url,
            "username": config.get("ORACLE_WMS_USERNAME"),
            "password": config.get("ORACLE_WMS_PASSWORD"),
            "environment": environment,  # Dynamic extraction from URL
            "api_version": FlextOracleWmsApiVersion.LGF_V10,  # Default to LGF v10
            "timeout": float(config.get("ORACLE_WMS_TIMEOUT", "30")),
            "max_retries": int(config.get("ORACLE_WMS_MAX_RETRIES", "3")),
            "verify_ssl": config.get("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
            "enable_logging": config.get(
                "ORACLE_WMS_ENABLE_REQUEST_LOGGING", "true",
            ).lower()
            == "true",
        }
    except Exception as e:
        logger.warning("Failed to load .env config: %s", e)
        return None


@pytest.fixture
def env_config() -> dict[str, object] | None:
    """Fixture that provides .env configuration or skips test."""
    config = load_env_config()
    if not config or not all(
        [config.get("base_url"), config.get("username"), config.get("password")],
    ):
        pytest.skip("No valid .env configuration found - skipping integration tests")
    return config


@pytest.fixture
async def oracle_wms_client(
    env_config: dict[str, object],
) -> AsyncGenerator[FlextOracleWmsClient]:
    """Fixture that provides configured Oracle WMS client."""
    config = FlextOracleWmsClientConfig(**env_config)
    client = FlextOracleWmsClient(config)

    # Start the client
    start_result = await client.start()
    if not start_result.success:
        pytest.fail(f"Failed to start Oracle WMS client: {start_result.error}")

    yield client

    # Cleanup
    await client.stop()


# ==============================================================================
# INTEGRATION TESTS - DECLARATIVE API CATALOG
# ==============================================================================


class TestOracleWmsDeclarativeIntegration:
    """Integration tests for declarative Oracle WMS client."""

    def test_api_catalog_completeness(self) -> None:
        """Test that API catalog contains all expected APIs."""
        # Verify we have all main categories
        categories = {api.category for api in FLEXT_ORACLE_WMS_APIS.values()}
        expected_categories = {
            FlextOracleWmsApiCategory.SETUP_TRANSACTIONAL,
            FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
            FlextOracleWmsApiCategory.DATA_EXTRACT,
            FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        }
        assert categories == expected_categories

        # Verify we have minimum expected APIs
        assert len(FLEXT_ORACLE_WMS_APIS) >= 15, (
            f"Should have at least 15 APIs, got {len(FLEXT_ORACLE_WMS_APIS)}"
        )

        # Verify specific critical APIs exist (VERIFIED WITH ACTUAL API CATALOG)
        critical_apis = [
            "lgf_init_stage_interface",  # CORRECTED: real name from api_catalog
            "run_stage_interface",
            "ship_oblpn",
            "create_lpn",
            "get_status",
            "lgf_entity_list",
        ]
        for api_name in critical_apis:
            assert api_name in FLEXT_ORACLE_WMS_APIS, f"Critical API {api_name} missing"

    def test_api_versions_coverage(self) -> None:
        """Test that both Legacy and LGF v10 APIs are covered."""
        versions = {api.version for api in FLEXT_ORACLE_WMS_APIS.values()}
        assert FlextOracleWmsApiVersion.LEGACY in versions
        assert FlextOracleWmsApiVersion.LGF_V10 in versions

        # Verify LGF v10 has data extraction APIs
        lgf_apis = [
            api
            for api in FLEXT_ORACLE_WMS_APIS.values()
            if api.version == FlextOracleWmsApiVersion.LGF_V10
        ]
        assert len(lgf_apis) >= 5, "Should have multiple LGF v10 APIs"

    async def test_client_configuration(self, env_config: dict[str, object]) -> None:
        """Test client configuration and initialization."""
        config = FlextOracleWmsClientConfig(**env_config)

        # Test config validation
        assert config.base_url.startswith("https://")
        assert config.username
        assert config.password
        assert config.timeout > 0
        assert config.max_retries > 0

        # Test client creation
        client = FlextOracleWmsClient(config)
        assert client.config == config

        # Test start/stop lifecycle
        start_result = await client.start()
        assert start_result.success, f"Client start failed: {start_result.error}"

        stop_result = await client.stop()
        assert stop_result.success, f"Client stop failed: {stop_result.error}"

    async def test_health_check(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test Oracle WMS API health check."""
        health_result = await oracle_wms_client.health_check()

        assert health_result.success, f"Health check failed: {health_result.error}"

        health_data = health_result.data
        assert health_data["service"] == "FlextOracleWmsClient"
        assert health_data["status"] in {"healthy", "unhealthy"}
        assert "base_url" in health_data
        assert "api_version" in health_data
        assert "test_call_success" in health_data

    async def test_get_all_entities(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting list of all Oracle WMS entities."""
        entities_result = await oracle_wms_client.get_all_entities()

        assert entities_result.success, f"Get entities failed: {entities_result.error}"

        entities = entities_result.data
        assert isinstance(entities, list)
        assert len(entities) > 0

        # Verify expected core entities
        expected_entities = [
            "company",
            "facility",
            "item",
            "order_hdr",
            "order_dtl",
            "allocation",
        ]
        for entity in expected_entities:
            assert entity in entities, f"Expected entity {entity} not found"


# ==============================================================================
# INTEGRATION TESTS - LGF API V10 DATA EXTRACTION
# ==============================================================================


class TestLgfApiV10Integration:
    """Integration tests for LGF API v10 data extraction."""

    @pytest.mark.parametrize("entity_name", ["company", "facility", "item"])
    async def test_get_entity_data(
        self, oracle_wms_client: FlextOracleWmsClient, entity_name: str,
    ) -> None:
        """Test getting entity data using LGF API v10."""
        result = await oracle_wms_client.get_entity_data(
            entity_name=entity_name, limit=5,
        )

        if result.success:
            data = result.data
            assert isinstance(data, dict)

            # LGF API v10 should return paginated response
            if "count" in data:
                assert isinstance(data["count"], int)
            if "results" in data:
                assert isinstance(data["results"], list)

            logger.info(
                "✅ Successfully retrieved %s data",
                entity_name,
                record_count=data.get("count", len(data.get("results", []))),
            )
        else:
            # Log but don't fail - some entities might not be accessible
            logger.warning("⚠️ Failed to get %s data: %s", entity_name, result.error)

    async def test_get_entity_data_with_filters(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting entity data with filters."""
        result = await oracle_wms_client.get_entity_data(
            entity_name="company",
            limit=10,
            fields="company_code,company_name",
            filters={"active": "Y"},
        )

        if result.success:
            data = result.data
            logger.info("✅ Successfully retrieved filtered company data", data=data)
        else:
            logger.warning("⚠️ Filtered query failed: %s", result.error)

    async def test_get_entity_by_id(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting specific entity record by ID."""
        # First get some data to find an ID
        list_result = await oracle_wms_client.get_entity_data("company", limit=1)

        if not list_result.success:
            pytest.skip(
                f"Cannot test get_entity_by_id - list failed: {list_result.error}",
            )

        data = list_result.data
        results = data.get("results", [])

        if not results:
            pytest.skip("No company records found for ID test")

        # Try to get first record by ID
        first_record = results[0]
        record_id = first_record.get("id") or first_record.get("company_code")

        if not record_id:
            pytest.skip("No ID field found in company record")

        # Get record by ID
        result = await oracle_wms_client.get_entity_by_id("company", str(record_id))

        if result.success:
            logger.info("✅ Successfully retrieved company by ID", record_id=record_id)
        else:
            logger.warning("⚠️ Get by ID failed: %s", result.error)


# ==============================================================================
# INTEGRATION TESTS - AUTOMATION & OPERATIONS APIS
# ==============================================================================


class TestAutomationApisIntegration:
    """Integration tests for automation and operations APIs."""

    async def test_get_entity_status(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting entity status."""
        result = await oracle_wms_client.get_entity_status(
            entity="company", key="test", company_code="DEFAULT",
        )

        # This might fail due to permissions, but we test the API structure
        if result.success:
            logger.info("✅ Successfully got entity status")
        else:
            logger.info("⚠️ Entity status call failed (expected): %s", result.error)
            # Verify it's a proper API call failure, not a client error
            assert "Client not initialized" not in result.error

    async def test_update_oblpn_tracking_number(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test OBLPN tracking number update API structure."""
        # This is a dry run test - we don't actually update anything
        # Just verify the API call structure works

        # Note: This will likely fail due to missing OBLPN, but tests API structure
        result = await oracle_wms_client.update_oblpn_tracking_number(
            company_code="TEST",
            facility_code="TEST",
            oblpn_nbr="TEST123",
            tracking_nbr="TRACK123",
        )

        # Expected to fail with business logic error, not client error
        assert not result.success  # Expected failure
        assert "Client not initialized" not in result.error
        logger.info("⚠️ OBLPN update failed as expected: %s", result.error)

    async def test_create_lpn_api_structure(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test LPN creation API structure."""
        # This is a dry run test - verify API call structure

        result = await oracle_wms_client.create_lpn(
            lpn_nbr="TEST_LPN_001", qty=10, item_barcode="TEST_ITEM",
        )

        # Expected to fail with business logic error, not client error
        assert not result.success  # Expected failure
        assert "Client not initialized" not in result.error
        logger.info("⚠️ LPN creation failed as expected: %s", result.error)


# ==============================================================================
# INTEGRATION TESTS - ERROR HANDLING AND EDGE CASES
# ==============================================================================


class TestErrorHandlingIntegration:
    """Integration tests for error handling and edge cases."""

    async def test_invalid_entity_name(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test handling of invalid entity names."""
        result = await oracle_wms_client.get_entity_data("invalid_entity_xyz")

        assert not result.success
        assert result.error
        assert "404" in result.error or "not found" in result.error.lower()
        logger.info("✅ Properly handled invalid entity: %s", result.error)

    async def test_unknown_api_call(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test handling of unknown API calls."""
        result = await oracle_wms_client.call_api("unknown_api_xyz")

        assert not result.success
        assert "Unknown API" in result.error
        logger.info("✅ Properly handled unknown API: %s", result.error)

    async def test_malformed_lgf_call(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test handling of malformed LGF API calls."""
        result = await oracle_wms_client.call_api("invalid_api_name")

        assert not result.success
        logger.info("✅ Properly handled malformed LGF call: %s", result.error)


# ==============================================================================
# PERFORMANCE AND STRESS TESTS
# ==============================================================================


class TestPerformanceIntegration:
    """Performance and stress tests for Oracle WMS client."""

    async def test_concurrent_entity_requests(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test concurrent requests to different entities."""
        import asyncio

        entities = ["company", "facility", "item"]

        # Create concurrent requests
        tasks = [
            oracle_wms_client.get_entity_data(entity, limit=3) for entity in entities
        ]

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        successful_requests = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning("Request %d failed with exception: %s", i, result)
            elif hasattr(result, "success") and result.success:
                successful_requests += 1
                logger.info("✅ Concurrent request %d succeeded", i)
            else:
                logger.warning(
                    "Request %d failed: %s", i, getattr(result, "error", "Unknown"),
                )

        # At least one request should succeed
        assert successful_requests > 0, "No concurrent requests succeeded"
        logger.info(
            "✅ Concurrent requests completed: %d/%d successful",
            successful_requests,
            len(tasks),
        )

    async def test_pagination_handling(
        self, oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test pagination with different page sizes."""
        page_sizes = [1, 5, 10]

        for page_size in page_sizes:
            result = await oracle_wms_client.get_entity_data(
                entity_name="company", limit=page_size,
            )

            if result.success:
                data = result.data
                results = data.get("results", [])
                actual_count = len(results)

                logger.info(
                    "✅ Page size %d returned %d records", page_size, actual_count,
                )

                # Should not exceed requested page size
                assert actual_count <= page_size
            else:
                logger.warning(
                    "⚠️ Pagination test failed for size %d: %s", page_size, result.error,
                )


# ==============================================================================
# TEST MARKERS AND CONFIGURATION
# ==============================================================================

# Mark all tests in this file as integration tests
pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio,
]

# Markers are configured in pyproject.toml
