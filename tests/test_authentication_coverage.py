"""Tests for authentication modules - focusing on coverage improvement."""

from unittest.mock import Mock

import pytest

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
)
from flext_oracle_wms.constants import OracleWMSAuthMethod
from flext_oracle_wms.exceptions import FlextOracleWmsAuthenticationError


class TestFlextOracleWmsAuthConfig:
    """Test authentication configuration."""

    def test_basic_auth_config(self) -> None:
        """Test basic auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        assert config.auth_type == OracleWMSAuthMethod.BASIC
        assert config.username == "test_user"
        assert config.password == "test_pass"

    def test_bearer_auth_config(self) -> None:
        """Test bearer auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="test_token",
        )
        assert config.auth_type == OracleWMSAuthMethod.BEARER
        assert config.token == "test_token"

    def test_api_key_auth_config(self) -> None:
        """Test API key auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="test_api_key",
        )
        assert config.auth_type == OracleWMSAuthMethod.API_KEY
        assert config.api_key == "test_api_key"

    def test_validation_basic_auth_missing_username(self) -> None:
        """Test validation fails for basic auth without username."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="",
            password="test_pass",
        )
        result = config.validate_business_rules()
        assert not result.success
        assert "Username and password required" in result.error

    def test_validation_basic_auth_missing_password(self) -> None:
        """Test validation fails for basic auth without password."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="",
        )
        result = config.validate_business_rules()
        assert not result.success
        assert "Username and password required" in result.error

    def test_validation_bearer_auth_missing_token(self) -> None:
        """Test validation fails for bearer auth without token."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="",
        )
        result = config.validate_business_rules()
        assert not result.success
        assert "Token required" in result.error

    def test_validation_api_key_missing(self) -> None:
        """Test validation fails for API key auth without key."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="",
        )
        result = config.validate_business_rules()
        assert not result.success
        assert "API key required" in result.error

    def test_validation_success(self) -> None:
        """Test validation succeeds with valid config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        result = config.validate_business_rules()
        assert result.success


class TestFlextOracleWmsAuthenticator:
    """Test authenticator functionality."""

    def test_authenticator_initialization_valid_config(self) -> None:
        """Test authenticator initializes with valid config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        assert authenticator.config == config

    def test_authenticator_initialization_invalid_config(self) -> None:
        """Test authenticator raises error with invalid config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="",  # Invalid
            password="test_pass",
        )
        with pytest.raises(FlextOracleWmsAuthenticationError):
            FlextOracleWmsAuthenticator(config)

    @pytest.mark.asyncio
    async def test_get_auth_headers_basic(self) -> None:
        """Test basic auth headers generation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.get_auth_headers()
        assert result.success
        headers = result.data
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"

    @pytest.mark.asyncio
    async def test_get_auth_headers_bearer(self) -> None:
        """Test bearer auth headers generation."""
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
    async def test_get_auth_headers_api_key(self) -> None:
        """Test API key auth headers generation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="test_api_key",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.get_auth_headers()
        assert result.success
        headers = result.data
        assert headers["X-API-Key"] == "test_api_key"

    @pytest.mark.asyncio
    async def test_validate_credentials_basic_valid(self) -> None:
        """Test credential validation succeeds for valid basic auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.validate_credentials()
        assert result.success
        assert result.data is True

    @pytest.mark.asyncio
    async def test_validate_credentials_bearer_valid(self) -> None:
        """Test credential validation succeeds for valid bearer token."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="valid_long_token_string",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.validate_credentials()
        assert result.success
        assert result.data is True

    @pytest.mark.asyncio
    async def test_validate_credentials_bearer_too_short(self) -> None:
        """Test credential validation fails for short bearer token."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="short",  # Too short
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.validate_credentials()
        assert not result.success
        assert "Invalid bearer token" in result.error

    @pytest.mark.asyncio
    async def test_validate_credentials_api_key_valid(self) -> None:
        """Test credential validation succeeds for valid API key."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="valid_long_api_key_string",
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.validate_credentials()
        assert result.success
        assert result.data is True

    @pytest.mark.asyncio
    async def test_validate_credentials_api_key_too_short(self) -> None:
        """Test credential validation fails for short API key."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="short",  # Too short
        )
        authenticator = FlextOracleWmsAuthenticator(config)

        result = await authenticator.validate_credentials()
        assert not result.success
        assert "Invalid API key" in result.error


class TestFlextOracleWmsAuthPlugin:
    """Test authentication plugin."""

    def test_auth_plugin_initialization(self) -> None:
        """Test auth plugin initialization."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        assert plugin.authenticator == authenticator

    @pytest.mark.asyncio
    async def test_before_request_success(self) -> None:
        """Test before_request adds headers successfully."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock request object
        mock_request = Mock()
        mock_request.headers = {}

        result = await plugin.before_request(mock_request)

        # Check that headers were added
        assert "Authorization" in mock_request.headers
        assert result == mock_request

    @pytest.mark.asyncio
    async def test_after_response_success(self) -> None:
        """Test after_response passes through successful response."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200

        result = await plugin.after_response(mock_response)
        assert result == mock_response

    @pytest.mark.asyncio
    async def test_after_response_auth_error(self) -> None:
        """Test after_response raises error for auth failure status codes."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_pass",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock response with auth error status code
        mock_response = Mock()
        mock_response.status_code = 401  # Unauthorized

        with pytest.raises(FlextOracleWmsAuthenticationError):
            await plugin.after_response(mock_response)
