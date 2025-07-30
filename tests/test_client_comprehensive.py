"""Comprehensive test for Oracle WMS client functionality."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from flext_core import get_logger

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
)
from flext_oracle_wms.client import FlextOracleWmsClient, FlextOracleWmsPlugin
from flext_oracle_wms.config import FlextOracleWmsClientConfig
from flext_oracle_wms.constants import OracleWMSAuthMethod
from flext_oracle_wms.exceptions import (
    FlextOracleWmsConnectionError,
)


class TestUtilityFunctions:
    """Test utility functions in client module."""

    def test_get_logger(self) -> None:
        """Test logger creation function."""
        logger = get_logger("test_logger")
        assert logger is not None
        assert logger.name == "test_logger"

    def test_logger_caching(self) -> None:
        """Test that loggers are cached."""
        logger1 = get_logger("existing_logger")
        logger2 = get_logger("existing_logger")
        assert logger1 is logger2


class TestFlextOracleWmsAuth:
    """Test the Oracle WMS authentication system."""

    def test_auth_config_creation(self) -> None:
        """Test auth config object creation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass"
        )
        assert config.username == "test_user"
        assert config.password == "test_pass"
        assert config.auth_type == OracleWMSAuthMethod.BASIC

    def test_authenticator_creation(self) -> None:
        """Test authenticator creation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass"
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        assert authenticator.config == config

    @pytest.mark.asyncio
    async def test_get_basic_auth_headers(self) -> None:
        """Test basic auth header generation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass"
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        headers_result = await authenticator.get_headers()
        assert headers_result.is_success is True

        headers = headers_result.data
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

    def test_auth_validation_empty_credentials(self) -> None:
        """Test auth validation with empty credentials."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="",
            password=""
        )
        result = config.validate_domain_rules()
        assert result.is_success is False


class TestFlextOracleWmsClient:
    """Test the Oracle WMS client functionality."""

    def test_client_creation(self) -> None:
        """Test client object creation."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)
        assert client.config == config

    @pytest.mark.asyncio
    async def test_client_start_stop(self) -> None:
        """Test client start and stop lifecycle."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        with patch.object(client, "_client", new_callable=AsyncMock) as mock_client:
            mock_client.start.return_value.is_success = True
            mock_client.close = AsyncMock()

            start_result = await client.start()
            assert start_result.is_success is True

            stop_result = await client.stop()
            assert stop_result.is_success is True

    @pytest.mark.asyncio
    async def test_discover_entities(self) -> None:
        """Test entity discovery functionality."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        with patch.object(client, "_call_api_direct") as mock_call:
            mock_call.return_value.is_success = True
            mock_call.return_value.data = {
                "entities": ["company", "facility", "item"]
            }

            result = await client.discover_entities()
            assert result.is_success is True
            assert len(result.data) >= 3

    @pytest.mark.asyncio
    async def test_get_entity_data(self) -> None:
        """Test getting entity data."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        with patch.object(client, "call_api") as mock_call:
            mock_call.return_value.is_success = True
            mock_call.return_value.data = {
                "results": [{"id": "1", "name": "Test Company"}]
            }

            result = await client.get_entity_data("company", limit=10)
            assert result.is_success is True

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        """Test client health check."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        with (
            patch.object(client, "discover_entities") as mock_discover,
            patch.object(client, "get_entity_data") as mock_get,
        ):
                mock_discover.return_value.is_success = True
                mock_discover.return_value.data = ["company"]
                mock_get.return_value.is_success = True

                result = await client.health_check()
                assert result.is_success is True
                assert result.data["service"] == "FlextOracleWmsClient"

    def test_get_available_apis(self) -> None:
        """Test getting available APIs."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        apis = client.get_available_apis()
        assert isinstance(apis, dict)
        assert len(apis) > 0


class TestFlextOracleWmsPlugin:
    """Test the Oracle WMS plugin functionality."""

    def test_plugin_creation(self) -> None:
        """Test plugin creation."""
        config = Mock()
        plugin = FlextOracleWmsPlugin(config)
        assert plugin.config == config

    @pytest.mark.asyncio
    async def test_plugin_lifecycle(self) -> None:
        """Test plugin start and stop."""
        config = Mock()
        plugin = FlextOracleWmsPlugin(config)

        start_result = await plugin.start()
        assert start_result.is_success is True

        stop_result = await plugin.stop()
        assert stop_result.is_success is True

    @pytest.mark.asyncio
    async def test_plugin_execute(self) -> None:
        """Test plugin execute method."""
        config = Mock()
        plugin = FlextOracleWmsPlugin(config)

        # Test without client initialized
        result = await plugin.execute("discover_entities")
        assert result.is_success is False

        # Test with mock client
        plugin._client = Mock()
        plugin._client.discover_entities = AsyncMock()
        plugin._client.discover_entities.return_value.is_success = True
        plugin._client.discover_entities.return_value.data = ["entity1"]

        result = await plugin.execute("discover_entities")
        assert result.is_success is True


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_connection_error_handling(self) -> None:
        """Test connection error handling."""
        config = FlextOracleWmsClientConfig(
            base_url="https://invalid.url.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        with patch.object(client, "_client") as mock_client:
            mock_client.start.side_effect = Exception("Connection failed")

            with pytest.raises(FlextOracleWmsConnectionError):
                await client.start()

    @pytest.mark.asyncio
    async def test_api_error_handling(self) -> None:
        """Test API error handling."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.wms.com",
            username="user",
            password="pass",
            environment="test_env"
        )
        client = FlextOracleWmsClient(config)

        with patch.object(client, "_call_api_direct") as mock_call:
            mock_call.return_value.is_success = False
            mock_call.return_value.error = "API Error"

            result = await client.discover_entities()
            # Should fallback to known entities rather than fail
            assert result.is_success is True
