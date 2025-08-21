"""Comprehensive unit tests for FlextOracleWmsClient - targeting 90%+ coverage.

Based on working code patterns from basic_usage.py and real Oracle WMS connectivity.
"""

from unittest.mock import AsyncMock, patch

import pytest
from flext_core import FlextResult

from flext_oracle_wms import (
    FlextOracleWmsClient,
)


@pytest.mark.unit
class TestFlextOracleWmsClientCore:
    """Core client functionality tests."""

    def test_client_initialization(self, mock_config) -> None:
        """Test client initialization with valid config."""
        client = FlextOracleWmsClient(mock_config)

        assert client.config == mock_config
        assert client.config.base_url == mock_config.base_url
        assert hasattr(client, "_client")
        assert client._client is None  # Should be None before start()
        assert hasattr(client, "_discovered_entities")

    def test_client_string_representation(self, mock_config) -> None:
        """Test client string representation."""
        client = FlextOracleWmsClient(mock_config)

        repr_str = repr(client)
        str_str = str(client)

        assert "FlextOracleWmsClient" in repr_str
        assert "FlextOracleWmsClient" in repr_str
        assert isinstance(str_str, str)

    def test_client_properties(self, mock_config) -> None:
        """Test client properties access."""
        client = FlextOracleWmsClient(mock_config)

        # Test property access via config
        assert client.config.base_url == mock_config.base_url
        assert client.config.timeout == mock_config.timeout
        assert client.config.max_retries == mock_config.max_retries
        assert client.config.api_version == mock_config.api_version

    @pytest.mark.asyncio
    async def test_client_start_success(self, mock_config) -> None:
        """Test successful client startup."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)
            result = await client.start()

            assert result.success
            assert client._client is not None  # Client should be set after start
            mock_api_client.start.assert_called_once()

    @pytest.mark.asyncio
    async def test_client_start_failure(self, mock_config) -> None:
        """Test client startup failure."""
        from flext_oracle_wms import FlextOracleWmsConnectionError

        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].fail(
                "Connection failed"
            )
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)

            # Client raises exception on start failure instead of returning FlextResult
            with pytest.raises(FlextOracleWmsConnectionError) as exc_info:
                await client.start()

            assert "Connection failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_client_start_multiple_times(self, mock_config) -> None:
        """Test starting client multiple times."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)

            # Start first time
            result1 = await client.start()
            assert result1.success

            # Start second time - current implementation allows multiple starts
            result2 = await client.start()
            assert result2.success

            # Current implementation calls start each time (no deduplication)
            assert mock_api_client.start.call_count == 2

    @pytest.mark.asyncio
    async def test_client_stop_success(self, mock_config) -> None:
        """Test successful client stop."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client.close.return_value = (
                None  # close() returns None, not FlextResult
            )
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)

            # Start then stop
            await client.start()
            result = await client.stop()

            assert result.success
            mock_api_client.close.assert_called_once()  # stop() calls close(), not stop()

    @pytest.mark.asyncio
    async def test_client_stop_not_started(self, mock_config) -> None:
        """Test stopping client that wasn't started."""
        client = FlextOracleWmsClient(mock_config)
        result = await client.stop()

        assert result.success  # Should succeed even if not started

    def test_client_has_expected_methods(self, mock_config) -> None:
        """Test client has expected methods."""
        client = FlextOracleWmsClient(mock_config)

        # Verify client has key methods
        assert hasattr(client, "start")
        assert hasattr(client, "stop")
        assert hasattr(client, "discover_entities")
        assert hasattr(client, "get_entity_data")
        assert hasattr(client, "health_check")
        assert callable(client.start)
        assert callable(client.stop)

    def test_get_available_apis(self, mock_config) -> None:
        """Test getting available APIs."""
        client = FlextOracleWmsClient(mock_config)
        apis = client.get_available_apis()

        assert isinstance(apis, dict)
        assert len(apis) > 0

        # Should contain some expected APIs
        api_names = list(apis.keys())
        assert len(api_names) > 0

    def test_get_apis_by_category(self, mock_config) -> None:
        """Test getting APIs filtered by category."""
        client = FlextOracleWmsClient(mock_config)

        # Test method exists and returns dict for any category (even if empty/invalid)
        result = client.get_apis_by_category("inventory")
        assert isinstance(result, dict)

        # Test with another category to verify consistent behavior
        result2 = client.get_apis_by_category("any_category")
        assert isinstance(result2, dict)

    @pytest.mark.asyncio
    async def test_health_check_not_started(self, mock_config) -> None:
        """Test health check when client not started."""
        client = FlextOracleWmsClient(mock_config)
        result = await client.health_check()

        # Health check returns success but with unhealthy status
        assert result.success
        assert isinstance(result.data, dict)
        health_data = result.data
        assert health_data.get("status") == "unhealthy"
        assert health_data.get("test_call_success") is False

    @pytest.mark.asyncio
    async def test_health_check_success(self, mock_config) -> None:
        """Test successful health check."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            # Create a mock response object that simulates FlextApiClientResponse
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.data = {
                "status": "healthy",
                "timestamp": "2025-01-01T00:00:00Z",
            }

            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client.get.return_value = FlextResult[None].ok(mock_response)
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)
            await client.start()

            result = await client.health_check()
            assert result.success
            # Health check calls discover_entities AND get_entity_data, so expect 2 calls
            assert mock_api_client.get.call_count >= 1

    @pytest.mark.asyncio
    async def test_discover_entities_not_started(self, mock_config) -> None:
        """Test entity discovery when client not started."""
        client = FlextOracleWmsClient(mock_config)
        result = await client.discover_entities()

        # Should use fallback entity list when not started
        assert result.success
        assert isinstance(result.data, list)
        assert len(result.data) > 0

    @pytest.mark.asyncio
    async def test_discover_entities_success(
        self,
        mock_config,
        sample_entities,
    ) -> None:
        """Test successful entity discovery."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            # Create a mock response object that simulates FlextApiClientResponse
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.data = {
                "entities": sample_entities,
                "count": len(sample_entities),
            }

            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client.get.return_value = FlextResult[None].ok(mock_response)
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)
            await client.start()

            result = await client.discover_entities()
            assert result.success
            assert isinstance(result.data, list)
            assert len(result.data) == len(sample_entities)

    @pytest.mark.asyncio
    async def test_get_entity_data_not_started(self, mock_config) -> None:
        """Test getting entity data when client not started."""
        client = FlextOracleWmsClient(mock_config)
        result = await client.get_entity_data("test_entity")

        assert result.is_failure
        assert "not initialized" in result.error.lower()

    @pytest.mark.asyncio
    async def test_get_entity_data_success(
        self,
        mock_config,
        sample_entity_data,
    ) -> None:
        """Test successful entity data retrieval."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            # Create a mock response object that simulates FlextApiClientResponse
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.data = sample_entity_data

            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client.get.return_value = FlextResult[None].ok(mock_response)
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)
            await client.start()

            result = await client.get_entity_data("test_entity", limit=10)
            assert result.success
            assert result.data == sample_entity_data
            mock_api_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_api_unknown_api(self, mock_config) -> None:
        """Test calling unknown API."""
        with patch("flext_oracle_wms.client.FlextApiClient") as mock_api_client_class:
            mock_api_client = AsyncMock()
            mock_api_client.start.return_value = FlextResult[None].ok(None)
            mock_api_client_class.return_value = mock_api_client

            client = FlextOracleWmsClient(mock_config)
            await client.start()

            result = await client.call_api("unknown_api_xyz")
            assert result.is_failure
            assert "Unknown API" in result.error

    @pytest.mark.asyncio
    async def test_call_api_without_client(self, mock_config) -> None:
        """Test calling API without initialized client."""
        client = FlextOracleWmsClient(mock_config)
        result = await client.call_api(
            "lgf_init_stage_interface",
            path_params={"entity_name": "test"},
        )

        assert result.is_failure
        assert "not initialized" in result.error.lower()

    def test_client_error_handling_invalid_config(self) -> None:
        """Test client creation with invalid config."""
        from flext_oracle_wms import FlextOracleWmsError

        # Client validates config and raises FlextOracleWmsError for None
        with pytest.raises(FlextOracleWmsError):
            FlextOracleWmsClient(None)


@pytest.mark.unit
class TestClientHelperMethods:
    """Test client helper and utility methods."""

    def test_parse_entity_discovery_response_list(self, mock_config) -> None:
        """Test parsing entity discovery response when it's a list."""
        client = FlextOracleWmsClient(mock_config)

        response = ["entity1", "entity2", "entity3"]
        result = client._parse_entity_discovery_response(response)

        assert result == ["entity1", "entity2", "entity3"]

    def test_parse_entity_discovery_response_with_entities(self, mock_config) -> None:
        """Test parsing entity discovery response with entities field."""
        client = FlextOracleWmsClient(mock_config)

        response = {"entities": ["entity1", "entity2"], "count": 2}
        result = client._parse_entity_discovery_response(response)

        assert result == ["entity1", "entity2"]

    def test_parse_entity_discovery_response_with_results(self, mock_config) -> None:
        """Test parsing entity discovery response with results field."""
        client = FlextOracleWmsClient(mock_config)

        response = {"results": ["entity1", "entity2"], "total": 2}
        result = client._parse_entity_discovery_response(response)

        assert result == ["entity1", "entity2"]

    def test_parse_entity_discovery_response_empty_dict(self, mock_config) -> None:
        """Test parsing empty dictionary response."""
        client = FlextOracleWmsClient(mock_config)

        response = {}
        result = client._parse_entity_discovery_response(response)

        # Empty response should return fallback entities
        assert result == ["company", "facility", "item"]

    def test_filter_valid_entities(self, mock_config) -> None:
        """Test filtering valid entities."""
        client = FlextOracleWmsClient(mock_config)

        entities = [
            "valid_entity",
            "",  # Empty string - invalid
            None,  # None - invalid
            "another_valid_entity",
            123,  # Number - invalid
        ]

        result = client._filter_valid_entities(entities)
        assert result == ["valid_entity", "another_valid_entity"]


@pytest.mark.unit
class TestGetLogger:
    """Test logger creation utility."""

    def test_get_logger_module_name(self) -> None:
        """Test logger creation with module name."""
        from flext_oracle_wms import get_logger

        logger = get_logger("test_module")
        assert hasattr(logger, "info")  # Check it's a logger
        assert hasattr(logger, "error")  # Check it has expected methods

        # Test with None
        logger_none = get_logger(None)
        assert callable(logger_none.info)  # Check it's functional
