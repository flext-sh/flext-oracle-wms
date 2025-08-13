"""Simple focused tests for authentication modules."""

import pytest

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
)
from flext_oracle_wms.constants import OracleWMSAuthMethod


class TestAuthenticationSimple:
    """Simple tests for authentication functionality."""

    def test_basic_auth_config_creation(self) -> None:
        """Test creating basic auth config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass",
        )
        assert config.auth_type == OracleWMSAuthMethod.BASIC
        assert config.username == "testuser"
        assert config.password == "testpass"

    def test_bearer_auth_config_creation(self) -> None:
        """Test creating bearer token auth config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="test_bearer_token",
        )
        assert config.auth_type == OracleWMSAuthMethod.BEARER
        assert config.token == "test_bearer_token"

    def test_api_key_auth_config_creation(self) -> None:
        """Test creating API key auth config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="test_api_key",
        )
        assert config.auth_type == OracleWMSAuthMethod.API_KEY
        assert config.api_key == "test_api_key"

    def test_authenticator_creation_with_valid_config(self) -> None:
        """Test creating authenticator with valid config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        assert authenticator.config == config

    def test_auth_plugin_creation(self) -> None:
        """Test creating auth plugin."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)
        assert plugin.authenticator == authenticator

    @pytest.mark.asyncio
    async def test_basic_auth_headers_generation(self) -> None:
        """Test basic auth headers are generated correctly."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.get_auth_headers()
        assert result.success
        headers = result.data
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")
        assert headers["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_bearer_auth_headers_generation(self) -> None:
        """Test bearer auth headers are generated correctly."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="test_token",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.get_auth_headers()
        assert result.success
        headers = result.data
        assert headers["Authorization"] == "Bearer test_token"

    @pytest.mark.asyncio
    async def test_api_key_headers_generation(self) -> None:
        """Test API key headers are generated correctly."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="test_api_key",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.get_auth_headers()
        assert result.success
        headers = result.data
        assert headers["X-API-Key"] == "test_api_key"

    def test_config_validation_success_basic(self) -> None:
        """Test config validation succeeds for valid basic auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="testuser",
            password="testpass",
        )
        result = config.validate_business_rules()
        assert result.success

    def test_config_validation_success_bearer(self) -> None:
        """Test config validation succeeds for valid bearer auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="valid_token",
        )
        result = config.validate_business_rules()
        assert result.success

    def test_config_validation_success_api_key(self) -> None:
        """Test config validation succeeds for valid API key auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="valid_api_key",
        )
        result = config.validate_business_rules()
        assert result.success
