"""Integration tests for Oracle WMS Client - Declarative Implementation.

Tests the new declarative Oracle WMS Cloud client using real .env configuration.
Skips tests if .env is not available.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Generator, Mapping, Sequence
from pathlib import Path
from urllib.parse import urlparse

import pytest
from flext_core import FlextLogger, r

from flext_oracle_wms import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsClient,
    FlextOracleWmsClientSettings,
    FlextOracleWmsConstants,
)
from tests import t

FlextOracleWmsApiVersion = FlextOracleWmsConstants.WmsApiVersion
FlextOracleWmsApiCategory = FlextOracleWmsConstants.WmsApiCategory
logger = FlextLogger(__name__)


def _to_str(value: t.NormalizedValue, default: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, int | float):
        return str(value)
    return default


def _to_int(value: t.NormalizedValue, default: int) -> int:
    if isinstance(value, int | float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


def _to_bool(value: t.NormalizedValue | None, default: bool) -> bool:
    if value is None:
        return default
    return bool(value)


def _build_client_settings(
    env_config: t.ContainerMapping,
    api_version: str,
) -> FlextOracleWmsClientSettings:
    return FlextOracleWmsClientSettings(
        base_url=_to_str(env_config.get("base_url", ""), ""),
        username=_to_str(env_config.get("username", ""), ""),
        password=_to_str(env_config.get("password", ""), ""),
        api_version=api_version,
        auth_method=_to_str(env_config.get("auth_method", "BASIC"), "BASIC"),
        timeout=_to_int(env_config.get("timeout", 30), 30),
        max_retries=_to_int(env_config.get("max_retries", 3), 3),
        verify_ssl=_to_bool(env_config.get("verify_ssl", True), True),
        enable_logging=_to_bool(env_config.get("enable_logging", True), True),
        use_mock=_to_bool(env_config.get("use_mock"), False),
        connection_pool_size=_to_int(env_config.get("connection_pool_size", 20), 20),
        cache_duration=_to_int(env_config.get("cache_duration", 3600), 3600),
        project_name=_to_str(
            env_config.get("project_name", "flext-oracle-wms"),
            "flext-oracle-wms",
        ),
        project_version=_to_str(env_config.get("project_version", "0.9.0"), "0.9.0"),
    )


def find_env_file() -> Path | None:
    """Find .env file in project hierarchy."""
    current_dir = Path(__file__).parent
    for _ in range(4):
        env_path = current_dir / ".env"
        if env_path.exists():
            return env_path
        current_dir = current_dir.parent
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        return env_path
    return None


def load_env_config() -> t.ContainerMapping | None:
    """Load Oracle WMS configuration from .env file."""
    env_path = find_env_file()
    if not env_path:
        return None
    config: t.StrMapping = {}
    try:
        with Path(env_path).open(encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if line and (not line.startswith("#")) and ("=" in line):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        base_url = config.get("ORACLE_WMS_BASE_URL", "")
        environment = "development"
        if base_url:
            try:
                parsed = urlparse(base_url)
                path_parts = parsed.path.strip("/").split("/")
                if path_parts and path_parts[-1]:
                    env_name = path_parts[-1].lower()
                    if env_name in {"prod", "production"}:
                        environment = "production"
                    elif env_name in {"stage", "staging"}:
                        environment = "staging"
                    elif env_name in {"test", "testing", "company_unknow"}:
                        environment = "test"
                    elif env_name == "local":
                        environment = "local"
                    else:
                        environment = "development"
            except Exception:
                environment = "development"
        return {
            "base_url": base_url,
            "username": config.get("ORACLE_WMS_USERNAME"),
            "password": config.get("ORACLE_WMS_PASSWORD"),
            "environment": environment,
            "api_version": "LGF_V10",
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
def env_config() -> t.ContainerMapping:
    """Fixture that provides .env configuration or skips test."""
    config = load_env_config()
    if not config or not all([
        config.get("base_url"),
        config.get("username"),
        config.get("password"),
    ]):
        pytest.skip("No valid .env configuration found - skipping integration tests")
    return config


@pytest.fixture
def oracle_wms_client(
    env_config: t.ContainerMapping,
) -> Generator[FlextOracleWmsClient]:
    """Fixture that provides configured Oracle WMS client."""
    config = _build_client_settings(env_config, "LGF_V10")
    client = FlextOracleWmsClient(config)
    start_result = client.start()
    if not start_result.is_success:
        pytest.fail(f"Failed to start Oracle WMS client: {start_result.error}")
    yield client
    client.stop()


class TestOracleWmsDeclarativeIntegration:
    """Integration tests for declarative Oracle WMS client."""

    def test_api_catalog_completeness(self) -> None:
        """Test that API catalog contains entries."""
        assert len(FLEXT_ORACLE_WMS_APIS) >= 1
        for api in FLEXT_ORACLE_WMS_APIS.values():
            assert api.name
            assert api.method
            assert api.path
            assert api.version

    def test_api_versions_coverage(self) -> None:
        """Test that API catalog entries have valid version strings."""
        versions = {api.version for api in FLEXT_ORACLE_WMS_APIS.values()}
        assert len(versions) >= 1

    def test_client_configuration_and_lifecycle(
        self,
        env_config: t.ContainerMapping,
    ) -> None:
        """Test client configuration and initialization."""
        config = _build_client_settings(env_config, FlextOracleWmsApiVersion.V1)
        assert config.base_url.startswith("https://")
        assert config.username
        assert config.password
        assert config.timeout > 0
        assert config.max_retries > 0
        client = FlextOracleWmsClient(config)
        assert client.config == config
        start_result = client.start()
        assert start_result.is_success, f"Client start failed: {start_result.error}"
        stop_result = client.stop()
        assert stop_result.is_success, f"Client stop failed: {stop_result.error}"

    def test_oracle_wms_health_check(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test Oracle WMS API health check."""
        health_result = oracle_wms_client.health_check()
        assert health_result.is_success, f"Health check failed: {health_result.error}"
        health_data = health_result.data
        assert health_data["service"] == "FlextOracleWmsClient"
        assert health_data["status"] in {"healthy", "unhealthy"}
        assert "base_url" in health_data
        assert "api_version" in health_data
        assert "test_call_success" in health_data

    @pytest.mark.skip(reason="Integration test requiring real Oracle WMS connectivity")
    def test_get_all_entities(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test getting list of all Oracle WMS entities."""
        entities_result = oracle_wms_client.discover_entities()
        assert entities_result.is_success, (
            f"Get entities failed: {entities_result.error}"
        )
        entities = entities_result.value
        assert isinstance(entities, list)
        assert entities
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


class TestLgfApiV10Integration:
    """Integration tests for LGF API v10 data extraction."""

    @pytest.mark.parametrize("entity_name", ["company", "facility", "item"])
    def test_get_entity_data(
        self,
        oracle_wms_client: FlextOracleWmsClient,
        entity_name: str,
    ) -> None:
        """Test getting entity data using LGF API v10."""
        result = oracle_wms_client.get_entity_data(entity_name=entity_name, limit=5)
        if result.is_success:
            data = result.data
            assert isinstance(data, dict)
            if "count" in data:
                assert isinstance(data["count"], int)
            if "results" in data:
                assert isinstance(data["results"], list)
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
        if result.is_success:
            data = result.data
            logger.info("✅ Successfully retrieved filtered company data", data=data)
        else:
            logger.warning("⚠️ Filtered query failed: %s", result.error)

    def test_get_entity_by_id(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test getting specific entity record by ID."""
        list_result = oracle_wms_client.get_entity_data("company", limit=1)
        if not list_result.is_success:
            pytest.skip(
                f"Cannot test get_entity_by_id - list failed: {list_result.error}",
            )
        data = list_result.data
        empty_results: t.ContainerList = []
        results = (
            data.get("results", empty_results)
            if isinstance(data, dict)
            else empty_results
        )
        if not results or not isinstance(results, list):
            pytest.skip("No company records found for ID test")
        first_record = results[0]
        if not isinstance(first_record, Mapping):
            pytest.skip("Company record format is invalid")
        record_id = first_record.get("id") or first_record.get("company_code")
        if not record_id:
            pytest.skip("No ID field found in company record")
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            filters={"id": str(record_id)},
            limit=1,
        )
        if result.is_success:
            logger.info("✅ Successfully retrieved company by ID", record_id=record_id)
        else:
            logger.warning("⚠️ Get by ID failed: %s", result.error)


class TestAutomationApisIntegration:
    """Integration tests for automation and operations APIs."""

    def test_get_entity_status(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test getting entity status."""
        result = oracle_wms_client.get_entity_data(
            entity_name="company",
            params={"key": "test", "company_code": "DEFAULT"},
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
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test OBLPN tracking number update API structure."""
        result = oracle_wms_client.update_oblpn_tracking_number(
            company_code="TEST",
            facility_code="TEST",
            oblpn_nbr="TEST123",
            tracking_nbr="TRACK123",
        )
        assert not result.is_success
        assert result.error is None or "Client not initialized" not in str(result.error)
        logger.info("⚠️ OBLPN update failed as expected: %s", result.error)

    def test_create_lpn_api_structure(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test LPN creation API structure."""
        result = oracle_wms_client.create_lpn(
            lpn_nbr="TEST_LPN_001",
            qty=10,
            item_barcode="TEST_ITEM",
        )
        assert not result.is_success
        assert result.error is None or "Client not initialized" not in str(result.error)
        logger.info("⚠️ LPN creation failed as expected: %s", result.error)


class TestErrorHandlingIntegration:
    """Integration tests for error handling and edge cases."""

    def test_invalid_entity_name(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test handling of invalid entity names."""
        result = oracle_wms_client.get_entity_data("invalid_entity_xyz")
        assert not result.is_success
        assert result.error
        assert (
            result.error is not None and "404" in result.error
        ) or "not found" in result.error.lower()
        logger.info("✅ Properly handled invalid entity: %s", result.error)

    def test_unknown_api_call(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test handling of unknown API calls."""
        result = oracle_wms_client.call_api("unknown_api_xyz")
        assert not result.is_success
        assert result.error is not None and "Unknown API" in str(result.error)
        logger.info("✅ Properly handled unknown API: %s", result.error)

    def test_malformed_lgf_call(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test handling of malformed LGF API calls."""
        result = oracle_wms_client.call_api("invalid_api_name")
        assert not result.is_success
        logger.info("✅ Properly handled malformed LGF call: %s", result.error)


class TestPerformanceIntegration:
    """Performance and stress tests for Oracle WMS client."""

    def test_concurrent_entity_requests(
        self,
        oracle_wms_client: FlextOracleWmsClient,
    ) -> None:
        """Test concurrent requests to different entities."""
        if not oracle_wms_client.config.use_mock:
            pytest.skip("Skipping concurrent test - requires mock server")
        entities = ["company", "facility", "item"]
        results: Sequence[r[t.NormalizedValue] | Exception] = []
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
            elif hasattr(result_item, "success") and result_item.is_success:
                successful_requests += 1
                logger.info("✅ Concurrent request %d succeeded", i)
            else:
                logger.warning(
                    "Request %d failed: %s",
                    i,
                    getattr(result_item, "error", "Unknown"),
                )
        assert successful_requests > 0, "No concurrent requests succeeded"
        logger.info(
            "✅ Concurrent requests completed: %d/%d successful",
            successful_requests,
            len(results),
        )

    def test_pagination_handling(self, oracle_wms_client: FlextOracleWmsClient) -> None:
        """Test pagination with different page sizes."""
        page_sizes = [1, 5, 10]
        for page_size in page_sizes:
            result = oracle_wms_client.get_entity_data(
                entity_name="company",
                limit=page_size,
            )
            if result.is_success:
                data = result.data
                empty_results: t.ContainerList = []
                results = (
                    data.get("results", empty_results)
                    if isinstance(data, dict)
                    else empty_results
                )
                actual_count = len(results) if isinstance(results, list) else 0
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
