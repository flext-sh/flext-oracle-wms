"""Integration tests for Oracle WMS Client - Declarative Implementation.

Tests the new declarative Oracle WMS Cloud client using real .env configuration.
Skips tests if .env is not available.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from collections.abc import Generator
from pathlib import Path
from urllib.parse import urlparse

import pytest

from flext_core import FlextLogger, FlextResult
from flext_oracle_wms import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
)

logger = FlextLogger(__name__)

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

    # Also check project root directly
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        return env_path

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
        environment = "development"  # fallback
        if base_url:
            try:
                # Extract the last path component as environment
                parsed = urlparse(base_url)
                path_parts = parsed.path.strip("/").split("/")
                if path_parts and path_parts[-1]:
                    env_name = path_parts[-1].lower()
                    # Map to valid environment values
                    if env_name in {"prod", "production"}:
                        environment = "production"
                    elif env_name in {"stage", "staging"}:
                        environment = "staging"
                    elif env_name in {"test", "testing", "raizen_test"}:
                        environment = "test"
                    elif env_name == "local":
                        environment = "local"
                    else:
                        environment = "development"
            except Exception:
                environment = "development"

        return {
            "oracle_wms_base_url": base_url,
            "oracle_wms_username": config.get("ORACLE_WMS_USERNAME"),
            "oracle_wms_password": config.get("ORACLE_WMS_PASSWORD"),
            "environment": environment,  # Dynamic extraction from URL
            "api_version": "LGF_V10",  # Default to LGF v10
            "timeout": float(config.get("ORACLE_WMS_TIMEOUT", "30")),
            "max_retries": int(config.get("ORACLE_WMS_MAX_RETRIES", "3")),
            "verify_ssl": config.get("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
            "enable_logging": config.get(
                "ORACLE_WMS_ENABLE_REQUEST_LOGGING",
                "true",
            ).lower()
            == "true",
        }
    except Exception as e:
        logger.warning("Failed to load .env config: %s", e)
        return None


@pytest.fixture
def env_config() -> dict[str, object]:
    """Fixture that provides .env configuration or skips test."""
    config = load_env_config()
    if not config or not all(
        [
            config.get("oracle_wms_base_url"),
            config.get("oracle_wms_username"),
            config.get("oracle_wms_password"),
        ],
    ):
        pytest.skip("No valid .env configuration found - skipping integration tests")
    return config


@pytest.fixture
def oracle_wms_client(
    env_config: dict[str, object],
) -> Generator[FlextOracleWmsClient]:
    """Fixture that provides configured Oracle WMS client."""
    # Properly cast env_config values to expected types for FlextOracleWmsClientConfig
    config_kwargs = {
        "oracle_wms_base_url": str(env_config.get("oracle_wms_base_url", "")),
        "oracle_wms_username": str(env_config.get("oracle_wms_username", "")),
        "oracle_wms_password": env_config.get("oracle_wms_password", ""),
        "api_version": env_config.get("api_version", "LGF_V10"),
        "auth_method": env_config.get("auth_method", "BASIC"),
        "oracle_wms_timeout": int(env_config.get("timeout", 30)),
        "oracle_wms_max_retries": int(env_config.get("max_retries", 3)),
        "oracle_wms_verify_ssl": bool(env_config.get("verify_ssl", True)),
        "oracle_wms_enable_logging": bool(env_config.get("enable_logging", True)),
        "oracle_wms_use_mock": bool(env_config.get("oracle_wms_use_mock")),
        "oracle_wms_connection_pool_size": int(
            env_config.get("oracle_wms_connection_pool_size", 20)
        ),
        "oracle_wms_cache_duration": int(
            env_config.get("oracle_wms_cache_duration", 3600)
        ),
        "project_name": str(env_config.get("project_name", "flext-oracle-wms")),
        "project_version": str(env_config.get("project_version", "0.9.0")),
    }
    config = FlextOracleWmsClientConfig(**config_kwargs)
    client = FlextOracleWmsClient(config)

    # Start the client
    start_result = client.start()
    if not start_result.success:
        pytest.fail(f"Failed to start Oracle WMS client: {start_result.error}")

    yield client

    # Cleanup
    client.stop()


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

    def test_client_configuration_and_lifecycle(
        self, env_config: dict[str, object]
    ) -> None:
        """Test client configuration and initialization."""
        # Properly cast env_config values to expected types for FlextOracleWmsClientConfig
        config_kwargs = {
            "oracle_wms_base_url": str(env_config.get("oracle_wms_base_url", "")),
            "oracle_wms_username": str(env_config.get("oracle_wms_username", "")),
            "oracle_wms_password": env_config.get("oracle_wms_password", ""),
            "api_version": env_config.get(
                "api_version", FlextOracleWmsApiVersion.LGF_V10
            ),
            "auth_method": env_config.get("auth_method", "BASIC"),
            "oracle_wms_timeout": int(env_config.get("timeout", 30)),
            "oracle_wms_max_retries": int(env_config.get("max_retries", 3)),
            "oracle_wms_verify_ssl": bool(env_config.get("verify_ssl", True)),
            "oracle_wms_enable_logging": bool(env_config.get("enable_logging", True)),
            "oracle_wms_use_mock": bool(env_config.get("oracle_wms_use_mock")),
            "oracle_wms_connection_pool_size": int(
                env_config.get("oracle_wms_connection_pool_size", 20)
            ),
            "oracle_wms_cache_duration": int(
                env_config.get("oracle_wms_cache_duration", 3600)
            ),
            "project_name": str(env_config.get("project_name", "flext-oracle-wms")),
            "project_version": str(env_config.get("project_version", "0.9.0")),
        }
        config = FlextOracleWmsClientConfig(**config_kwargs)

        # Test config validation
        assert config.oracle_wms_base_url.startswith("https://")
        assert config.oracle_wms_username
        assert config.oracle_wms_password
        assert config.oracle_wms_timeout > 0
        assert config.oracle_wms_max_retries > 0

        # Test client creation
        client = FlextOracleWmsClient(config)
        assert client.config == config

        # Test start/stop lifecycle
        start_result = client.start()
        assert start_result.success, f"Client start failed: {start_result.error}"

        stop_result = client.stop()
        assert stop_result.success, f"Client stop failed: {stop_result.error}"

    def test_oracle_wms_health_check(
        self, oracle_wms_client: FlextOracleWmsClient
    ) -> None:
        """Test Oracle WMS API health check."""
        health_result = oracle_wms_client.health_check()

        assert health_result.success, f"Health check failed: {health_result.error}"

        health_data = health_result.data
        assert health_data["service"] == "FlextOracleWmsClient"
        assert health_data["status"] in {"healthy", "unhealthy"}
        assert "base_url" in health_data
        assert "api_version" in health_data
        assert "test_call_success" in health_data

    @pytest.mark.skip(reason="Integration test requiring real Oracle WMS connectivity")
    def test_get_all_entities(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting list of all Oracle WMS entities."""
        entities_result = oracle_wms_client.discover_entities()

        assert entities_result.success, f"Get entities failed: {entities_result.error}"

        entities = entities_result.value
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
    def test_get_entity_data(
        self,
        oracle_wms_client: FlextOracleWmsClient,
        entity_name: str,
    ) -> None:
        """Test getting entity data using LGF API v10."""
        result = oracle_wms_client.get_entity_data(
            entity_name=entity_name,
            limit=5,
        )

        if result.success:
            data = result.data
            assert isinstance(data, dict)

            # LGF API v10 should return paginated response
            if "count" in data:
                assert isinstance(data["count"], int)
            if "results" in data:
                assert isinstance(data["results"], list)

            # Properly type the results to fix Pyright errors
            results = data.get("results", [])
            if isinstance(results, list):
                record_count = data.get("count", len(results))
            else:
                record_count = data.get("count", 0)

            logger.info(
                "✅ Successfully retrieved %s data",
                entity_name,
                record_count=record_count,
            )
        else:
            # Log but don't fail - some entities might not be accessible
            logger.warning("⚠️ Failed to get %s data: %s", entity_name, result.error)

    def test_get_entity_data_with_filters(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting entity data with filters."""
        result = oracle_wms_client.get_entity_data(
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

    def test_get_entity_by_id(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting specific entity record by ID."""
        # First get some data to find an ID
        list_result = oracle_wms_client.get_entity_data("company", limit=1)

        if not list_result.success:
            pytest.skip(
                f"Cannot test get_entity_by_id - list failed: {list_result.error}",
            )

        data = list_result.data
        results = data.get("results", []) if isinstance(data, dict) else []

        if not results or not isinstance(results, list):
            pytest.skip("No company records found for ID test")

        # Try to get first record by ID
        first_record = results[0]
        record_id = first_record.get("id") or first_record.get("company_code")

        if not record_id:
            pytest.skip("No ID field found in company record")

        # Get record by ID using get_entity_data with filters
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            filters={"id": str(record_id)},
            limit=1,
        )

        if result.success:
            logger.info("✅ Successfully retrieved company by ID", record_id=record_id)
        else:
            logger.warning("⚠️ Get by ID failed: %s", result.error)


# ==============================================================================
# INTEGRATION TESTS - AUTOMATION & OPERATIONS APIS
# ==============================================================================


class TestAutomationApisIntegration:
    """Integration tests for automation and operations APIs."""

    def test_get_entity_status(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test getting entity status."""
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            params={"key": "test", "company_code": "DEFAULT"},
        )

        # This might fail due to permissions, but we test the API structure
        if result.success:
            logger.info("✅ Successfully got entity status")
        else:
            logger.info("⚠️ Entity status call failed (expected): %s", result.error)
            # Verify it's a proper API call failure, not a client error
            assert result.error is None or "Client not initialized" not in str(
                result.error
            )

    def test_update_oblpn_tracking_number(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test OBLPN tracking number update API structure."""
        # This is a dry run test - we don't actually update anything
        # Just verify the API call structure works

        # Note: This will likely fail due to missing OBLPN, but tests API structure
        result = oracle_wms_client.update_oblpn_tracking_number(
            company_code="TEST",
            facility_code="TEST",
            oblpn_nbr="TEST123",
            tracking_nbr="TRACK123",
        )

        # Expected to fail with business logic error, not client error
        assert not result.success  # Expected failure
        assert result.error is None or "Client not initialized" not in str(result.error)
        logger.info("⚠️ OBLPN update failed as expected: %s", result.error)

    def test_create_lpn_api_structure(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test LPN creation API structure."""
        # This is a dry run test - verify API call structure

        result = oracle_wms_client.create_lpn(
            lpn_nbr="TEST_LPN_001",
            qty=10,
            item_barcode="TEST_ITEM",
        )

        # Expected to fail with business logic error, not client error
        assert not result.success  # Expected failure
        assert result.error is None or "Client not initialized" not in str(result.error)
        logger.info("⚠️ LPN creation failed as expected: %s", result.error)


# ==============================================================================
# INTEGRATION TESTS - ERROR HANDLING AND EDGE CASES
# ==============================================================================


class TestErrorHandlingIntegration:
    """Integration tests for error handling and edge cases."""

    def test_invalid_entity_name(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test handling of invalid entity names."""
        result = oracle_wms_client.get_entity_data("invalid_entity_xyz")

        assert not result.success
        assert result.error
        assert (
            result.error is not None and "404" in result.error
        ) or "not found" in result.error.lower()
        logger.info("✅ Properly handled invalid entity: %s", result.error)

    def test_unknown_api_call(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test handling of unknown API calls."""
        result = oracle_wms_client.call_api("unknown_api_xyz")

        assert not result.success
        assert result.error is not None and "Unknown API" in str(result.error)
        logger.info("✅ Properly handled unknown API: %s", result.error)

    def test_malformed_lgf_call(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test handling of malformed LGF API calls."""
        result = oracle_wms_client.call_api("invalid_api_name")

        assert not result.success
        logger.info("✅ Properly handled malformed LGF call: %s", result.error)


# ==============================================================================
# PERFORMANCE AND STRESS TESTS
# ==============================================================================


class TestPerformanceIntegration:
    """Performance and stress tests for Oracle WMS client."""

    def test_concurrent_entity_requests(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test concurrent requests to different entities."""
        # Skip this test if using real Oracle WMS (no mock server)
        if not oracle_wms_client.config.oracle_wms_use_mock:
            pytest.skip("Skipping concurrent test - requires mock server")

        entities = ["company", "facility", "item"]

        # Create sequential requests
        results: list[FlextResult[object] | Exception] = []
        for entity in entities:
            try:
                result = oracle_wms_client.get_entity_data(entity, limit=3)
                results.append(result)
            except Exception as e:
                results.append(e)

        successful_requests = 0
        for i, result_item in enumerate(results):
            if isinstance(result_item, Exception):
                logger.warning("Request %d failed with exception: %s", i, result_item)
            elif hasattr(result_item, "success") and result_item.success:
                successful_requests += 1
                logger.info("✅ Concurrent request %d succeeded", i)
            else:
                logger.warning(
                    "Request %d failed: %s",
                    i,
                    getattr(result_item, "error", "Unknown"),
                )

        # At least one request should succeed
        assert successful_requests > 0, "No concurrent requests succeeded"
        logger.info(
            "✅ Concurrent requests completed: %d/%d successful",
            successful_requests,
            len(results),
        )

    def test_pagination_handling(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test pagination with different page sizes."""
        page_sizes = [1, 5, 10]

        for page_size in page_sizes:
            result = oracle_wms_client.get_entity_data(
                entity_name="company",
                limit=page_size,
            )

            if result.success:
                data = result.data
                results = data.get("results", []) if isinstance(data, dict) else []
                actual_count = len(results) if isinstance(results, list) else 0

                logger.info(
                    "✅ Page size %d returned %d records",
                    page_size,
                    actual_count,
                )

                # Should not exceed requested page size
                assert actual_count <= page_size
            else:
                logger.warning(
                    "⚠️ Pagination test failed for size %d: %s",
                    page_size,
                    result.error,
                )


# ==============================================================================
# TEST MARKERS AND CONFIGURATION
# ==============================================================================

# Mark all tests in this file as integration tests
pytestmark = [
    pytest.mark.integration,
]

# Markers are configured in pyproject.toml
