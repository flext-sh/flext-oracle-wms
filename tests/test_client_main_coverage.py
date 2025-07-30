"""Comprehensive tests for client.py - targeting critical missing coverage."""

import pytest
from flext_core import get_logger

from flext_oracle_wms.client import FlextOracleWmsClient, FlextOracleWmsPlugin
from flext_oracle_wms.config import FlextOracleWmsModuleConfig
from flext_oracle_wms.exceptions import (
    FlextOracleWmsConnectionError,
)

logger = get_logger(__name__)


class TestGetLogger:
    """Test logger creation utility."""

    def test_get_logger_module_name(self) -> None:
        """Test logger creation with module name."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        # Test that different loggers are created
        assert logger1 is not None
        assert logger2 is not None
        assert logger1 != logger2


class TestFlextOracleWmsPlugin:
    """Test Oracle WMS plugin class."""

    def test_plugin_creation(self) -> None:
        """Test plugin instance creation."""
        plugin = FlextOracleWmsPlugin()
        assert plugin is not None

    @pytest.mark.asyncio
    async def test_plugin_start_without_client(self) -> None:
        """Test plugin start functionality without client."""
        plugin = FlextOracleWmsPlugin()
        result = await plugin.start()
        assert result.is_success

    @pytest.mark.asyncio
    async def test_plugin_stop_without_client(self) -> None:
        """Test plugin stop functionality without client."""
        plugin = FlextOracleWmsPlugin()
        result = await plugin.stop()
        assert result.is_success

    @pytest.mark.asyncio
    async def test_plugin_execute_without_client(self) -> None:
        """Test plugin execute fails without client."""
        plugin = FlextOracleWmsPlugin()
        result = await plugin.execute("discover_entities")
        assert not result.is_success
        assert "not initialized" in result.error


class TestFlextOracleWmsClient:
    """Test Oracle WMS client class."""

    def test_client_creation(self) -> None:
        """Test client instance creation."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)
        assert client.config == config

    @pytest.mark.asyncio
    async def test_client_start_fails_invalid_config(self) -> None:
        """Test client start fails with invalid config."""
        config = FlextOracleWmsModuleConfig(
            base_url="invalid_url",  # Invalid URL
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        with pytest.raises(FlextOracleWmsConnectionError):
            await client.start()

    @pytest.mark.asyncio
    async def test_client_stop_when_not_started(self) -> None:
        """Test client stop when not started."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = await client.stop()
        assert result.is_success

    @pytest.mark.asyncio
    async def test_discover_entities_not_started(self) -> None:
        """Test discover entities uses fallback when client not started."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = await client.discover_entities()
        # Client should succeed with fallback entities when API call fails
        assert result.is_success
        assert isinstance(result.data, list)
        assert len(result.data) > 0
        # Should contain known fallback entities
        assert "company" in result.data
        assert "facility" in result.data

    @pytest.mark.asyncio
    async def test_get_entity_data_not_started(self) -> None:
        """Test get entity data fails when client not started."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = await client.get_entity_data("test_entity")
        assert not result.is_success

    @pytest.mark.asyncio
    async def test_health_check_not_started(self) -> None:
        """Test health check when client not started."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = await client.health_check()
        assert not result.is_success
        assert "Health check failed" in result.error

    def test_get_available_apis(self) -> None:
        """Test getting available APIs."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        apis = client.get_available_apis()
        assert isinstance(apis, dict)
        assert len(apis) > 0

    def test_get_apis_by_category(self) -> None:
        """Test getting APIs filtered by category."""
        from flext_oracle_wms.api_catalog import FlextOracleWmsApiCategory

        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        setup_apis = client.get_apis_by_category(
            FlextOracleWmsApiCategory.SETUP_TRANSACTIONAL
        )
        assert isinstance(setup_apis, dict)

    @pytest.mark.asyncio
    async def test_call_api_without_client(self) -> None:
        """Test call API fails without initialized client."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = await client.call_api("non_existent_api")
        assert not result.is_success

    @pytest.mark.asyncio
    async def test_call_api_unknown_api(self) -> None:
        """Test call API with unknown API name."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = await client.call_api("non_existent_api")
        assert not result.is_success
        assert "Unknown API" in result.error


class TestClientHelperMethods:
    """Test client helper and private methods."""

    def test_parse_entity_discovery_response_empty_dict(self) -> None:
        """Test parsing empty dictionary response."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        result = client._parse_entity_discovery_response({})
        assert isinstance(result, list)
        assert len(result) == 3  # Fallback entities

    def test_parse_entity_discovery_response_with_entities(self) -> None:
        """Test parsing response with entities field."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        response_data = {"entities": ["entity1", "entity2", "entity3"]}
        result = client._parse_entity_discovery_response(response_data)
        assert isinstance(result, list)
        assert "entity1" in result
        assert "entity2" in result
        assert "entity3" in result

    def test_parse_entity_discovery_response_with_results(self) -> None:
        """Test parsing response with results field."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        response_data = {
            "results": [
                {"name": "entity1"},
                {"name": "entity2"},
                "entity3",  # String in results
            ]
        }
        result = client._parse_entity_discovery_response(response_data)
        assert isinstance(result, list)
        assert "entity1" in result
        assert "entity2" in result
        assert "entity3" in result

    def test_parse_entity_discovery_response_list(self) -> None:
        """Test parsing list response."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        response_data = ["entity1", "entity2", "entity3"]
        result = client._parse_entity_discovery_response(response_data)
        assert isinstance(result, list)
        assert "entity1" in result
        assert "entity2" in result
        assert "entity3" in result

    def test_filter_valid_entities(self) -> None:
        """Test filtering valid entities."""
        config = FlextOracleWmsModuleConfig(
            base_url="https://test.example.com",
            username="testuser",
            password="testpass",
            environment="test",
        )
        client = FlextOracleWmsClient(config)

        entities = ["valid_entity", "_internal_entity", "", "another_valid"]
        result = client._filter_valid_entities(entities)
        assert isinstance(result, list)
        assert "valid_entity" in result
        assert "another_valid" in result
        assert "_internal_entity" not in result  # Starts with underscore
        assert "" not in result  # Empty string
