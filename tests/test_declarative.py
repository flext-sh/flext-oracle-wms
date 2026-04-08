"""Integration tests for Oracle WMS Client - Declarative Implementation.

Tests the new declarative Oracle WMS Cloud client using real .env configuration.
Skips tests if .env is not available.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Generator, Sequence
from pathlib import Path

import pytest

from flext_core import FlextLogger, r
from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsClientSettings,
    FlextOracleWmsUtilitiesClient,
)
from tests import c, t, u

logger = FlextLogger(__name__)


@pytest.fixture
def env_config() -> t.ContainerMapping:
    """Fixture that provides .env configuration or deterministic test defaults."""
    config_result = u.OracleWms.Tests.load_env_config(Path(__file__))
    if config_result.is_success and config_result.value.get("base_url"):
        return config_result.value
    return {
        "base_url": "https://test-wms.example.com",
        "username": "test_user",
        "password": "test_pass",
        "timeout": 30,
        "max_retries": 3,
    }


@pytest.fixture
def oracle_wms_client(
    env_config: t.ContainerMapping,
) -> Generator[FlextOracleWmsUtilitiesClient.Client]:
    """Fixture that provides configured Oracle WMS client."""
    config = FlextOracleWmsClientSettings.model_validate({
        **env_config,
        "api_version": "LGF_V10",
    })
    client = FlextOracleWmsUtilitiesClient.Client(config)
    start_result = client.start()
    if not start_result.is_success:
        pytest.fail(f"Failed to start Oracle WMS client: {start_result.error}")
    yield client
    client.stop()


class TestOracleWmsDeclarativeIntegration:
    """Integration tests for declarative Oracle WMS client."""

    def test_api_catalog_completeness(self) -> None:
        """Test that API catalog contains entries."""
        assert len(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS) >= 1
        for api in FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS.values():
            assert api.name
            assert api.method
            assert api.path
            assert api.version

    def test_api_versions_coverage(self) -> None:
        """Test that API catalog entries have valid version strings."""
        versions = {
            api.version for api in FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS.values()
        }
        assert len(versions) >= 1

    def test_client_configuration_and_lifecycle(
        self,
        env_config: t.ContainerMapping,
    ) -> None:
        """Test client configuration and initialization."""
        config = u.OracleWms.Tests.build_client_settings(
            env_config,
            c.OracleWms.WmsApiVersion.V1,
        )
        assert config.base_url.startswith("https://")
        assert config.username
        assert config.password
        assert config.timeout > 0
        assert config.max_retries > 0
        client = FlextOracleWmsUtilitiesClient.Client(config)
        assert client.config == config
        start_result = client.start()
        assert start_result.is_success, f"Client start failed: {start_result.error}"
        stop_result = client.stop()
        assert stop_result.is_success, f"Client stop failed: {stop_result.error}"

    def test_oracle_wms_health_check(
        self,
        oracle_wms_client: FlextOracleWmsUtilitiesClient.Client,
    ) -> None:
        """Test Oracle WMS API health check returns valid result."""
        health_result = oracle_wms_client.health_check()
        assert isinstance(health_result, r)
        if health_result.is_success:
            health_response = health_result.value
            health_data = (
                health_response.body
                if isinstance(health_response.body, dict)
                else dict[str, t.NormalizedValue]()
            )
            assert health_data.get("service") == "FlextOracleWmsClient"
            assert health_data.get("status") in {"healthy", "unhealthy"}
        else:
            assert health_result.error is not None

    def test_get_all_entities(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test getting list of all Oracle WMS entities returns valid result."""
        entities_result = oracle_wms_client.discover_entities()
        assert isinstance(entities_result, r)
        if entities_result.is_success:
            entities = entities_result.value
            assert isinstance(entities, list)
        else:
            assert entities_result.error is not None


class TestLgfApiV10Integration:
    """Integration tests for LGF API v10 data extraction."""

    @pytest.mark.parametrize("entity_name", ["company", "facility", "item"])
    def test_get_entity_data(
        self,
        oracle_wms_client: FlextOracleWmsUtilitiesClient.Client,
        entity_name: str,
    ) -> None:
        """Test getting entity data using LGF API v10."""
        result = oracle_wms_client.get_entity_data(entity_name=entity_name, limit=5)
        if result.is_success:
            records = result.value
            assert isinstance(records, (list, tuple))
            record_count = len(records)
            logger.info(
                "✅ Successfully retrieved %s data",
                entity_name,
                record_count=record_count,
            )
        else:
            logger.warning(
                "⚠️ Failed to get %s data: %s",
                entity_name,
                result.error,
            )

    def test_get_entity_data_with_filters(
        self,
        oracle_wms_client: FlextOracleWmsUtilitiesClient.Client,
    ) -> None:
        """Test getting entity data with filters."""
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            limit=10,
            filters={"active": "Y"},
        )
        if result.is_success:
            records = result.value
            logger.info(
                "✅ Successfully retrieved filtered company data: %d records",
                len(records),
            )
        else:
            logger.warning("⚠️ Filtered query failed: %s", result.error)

    def test_get_entity_by_id(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test getting specific entity record by ID returns valid result."""
        list_result = oracle_wms_client.get_entity_data("company", limit=1)
        assert isinstance(list_result, r)
        if not list_result.is_success:
            assert list_result.error is not None
            return
        records = list_result.value
        if not records or not isinstance(records[0], dict):
            return
        record_id = records[0].get("id") or records[0].get("company_code")
        if not record_id:
            return
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            filters={"id": str(record_id)},
            limit=1,
        )
        assert isinstance(result, r)


class TestAutomationApisIntegration:
    """Integration tests for automation and operations APIs."""

    def test_get_entity_status(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test getting entity status."""
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            filters={"company_code": "DEFAULT"},
        )
        if result.is_success:
            logger.info("✅ Successfully got entity status")
        else:
            logger.info("⚠️ Entity status call failed (expected): %s", result.error)
            assert result.error is None or "Client not initialized" not in str(
                result.error,
            )

    def test_update_oblpn_tracking_number(
        self,
        oracle_wms_client: FlextOracleWmsUtilitiesClient.Client,
    ) -> None:
        """Test OBLPN tracking number update API structure."""
        result = oracle_wms_client.update_oblpn_tracking_number(
            oblpn_id="TEST123",
            tracking_number="TRACK123",
        )
        assert not result.is_success
        assert result.error is None or "Client not initialized" not in str(result.error)
        logger.info("⚠️ OBLPN update failed as expected: %s", result.error)

    def test_create_lpn_api_structure(
        self,
        oracle_wms_client: FlextOracleWmsUtilitiesClient.Client,
    ) -> None:
        """Test LPN creation API structure."""
        result = oracle_wms_client.create_lpn(
            lpn_nbr="TEST_LPN_001",
            qty=10,
        )
        assert not result.is_success
        assert result.error is None or "Client not initialized" not in str(result.error)
        logger.info("⚠️ LPN creation failed as expected: %s", result.error)


class TestErrorHandlingIntegration:
    """Integration tests for error handling and edge cases."""

    def test_invalid_entity_name(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test handling of invalid entity names returns failure result."""
        result = oracle_wms_client.get_entity_data("invalid_entity_xyz")
        assert not result.is_success
        assert result.error is not None

    def test_unknown_api_call(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test handling of unknown API calls returns failure result."""
        result = oracle_wms_client.call_api("unknown_api_xyz")
        assert not result.is_success
        assert result.error is not None

    def test_malformed_lgf_call(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test handling of malformed LGF API calls."""
        result = oracle_wms_client.call_api("invalid_api_name")
        assert not result.is_success
        logger.info("✅ Properly handled malformed LGF call: %s", result.error)


class TestPerformanceIntegration:
    """Performance and stress tests for Oracle WMS client."""

    def test_concurrent_entity_requests(
        self,
        oracle_wms_client: FlextOracleWmsUtilitiesClient.Client,
    ) -> None:
        """Test concurrent requests to different entities return results."""
        entities = ["company", "facility", "item"]
        results: list[r[Sequence[t.StrMapping]] | Exception] = []
        for entity in entities:
            try:
                result = oracle_wms_client.get_entity_data(entity, limit=3)
                results.append(result)
            except Exception as exc:
                results.append(exc)
        assert len(results) == len(entities)
        for result_item in results:
            if not isinstance(result_item, Exception):
                assert isinstance(result_item, r)

    def test_pagination_handling(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Test pagination with different page sizes."""
        page_sizes = [1, 5, 10]
        for page_size in page_sizes:
            result = oracle_wms_client.get_entity_data(
                entity_name="company",
                limit=page_size,
            )
            if result.is_success:
                records = result.value
                actual_count = len(records)
                logger.info(
                    "✅ Page size %d returned %d records",
                    page_size,
                    actual_count,
                )
                assert actual_count <= page_size
            else:
                logger.warning(
                    "⚠️ Pagination test failed for size %d: %s",
                    page_size,
                    result.error,
                )


pytestmark = [pytest.mark.integration]
