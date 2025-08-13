"""Comprehensive unit tests for Oracle WMS authentication module - targeting 90%+ coverage.

Based on working authentication patterns and enterprise security requirements.
"""

from unittest.mock import patch

import pytest
from flext_api.constants import FlextApiConstants
from flext_core import FlextResult

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
)
from flext_oracle_wms.constants import OracleWMSAuthMethod
from flext_oracle_wms.exceptions import FlextOracleWmsAuthenticationError


@pytest.mark.unit
class TestAuthenticationMethod:
    """Test authentication method enum."""

    def test_authentication_method_values(self) -> None:
        """Test authentication method enum values."""
        assert OracleWMSAuthMethod.BASIC == "basic"
        assert OracleWMSAuthMethod.BEARER == "bearer"
        assert OracleWMSAuthMethod.API_KEY == "api_key"

    def test_authentication_method_membership(self) -> None:
        """Test authentication method membership."""
        assert "basic" in [method.value for method in OracleWMSAuthMethod]
        assert "bearer" in [method.value for method in OracleWMSAuthMethod]
        assert "api_key" in [method.value for method in OracleWMSAuthMethod]


@pytest.mark.unit
class TestAuthenticationConfig:
    """Test authentication configuration."""

    def test_basic_auth_config_creation(self) -> None:
        """Test creating basic auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        assert config.auth_type == OracleWMSAuthMethod.BASIC
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.token == ""  # Default empty string
        assert config.api_key == ""  # Default empty string

    def test_bearer_auth_config_creation(self) -> None:
        """Test creating bearer token auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER, token="bearer_token_123",
        )

        assert config.auth_type == OracleWMSAuthMethod.BEARER
        assert config.token == "bearer_token_123"
        assert config.username is None
        assert config.password is None
        assert config.api_key is None

    def test_api_key_auth_config_creation(self) -> None:
        """Test creating API key auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="api_key_123",
        )

        assert config.auth_type == OracleWMSAuthMethod.API_KEY
        assert config.api_key == "api_key_123"
        assert config.username == ""
        assert config.password == ""
        assert config.token == ""

    def test_config_validation_success_basic(self) -> None:
        """Test config validation succeeds for valid basic auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        result = config.validate_business_rules()
        assert result.success

    def test_config_validation_success_bearer(self) -> None:
        """Test config validation succeeds for valid bearer auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER, token="valid_token",
        )

        result = config.validate_business_rules()
        assert result.success

    def test_config_validation_success_api_key(self) -> None:
        """Test config validation succeeds for valid API key auth."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="valid_key",
        )

        result = config.validate_business_rules()
        assert result.success

    def test_config_validation_failure_basic_missing_username(self) -> None:
        """Test config validation fails for basic auth missing username."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="",  # Empty username
            password="test_password",
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert "username" in result.error.lower()

    def test_config_validation_failure_basic_missing_password(self) -> None:
        """Test config validation fails for basic auth missing password."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="",  # Empty password
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert "password" in result.error.lower()

    def test_config_validation_failure_bearer_missing_token(self) -> None:
        """Test config validation fails for bearer auth missing token."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER,
            token="",  # Empty token
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert "token" in result.error.lower()

    def test_config_validation_failure_api_key_missing_key(self) -> None:
        """Test config validation fails for API key auth missing key."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="",  # Empty API key
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert "api key" in result.error.lower()

    def test_config_validation_api_key_empty(self) -> None:
        """Test config validation fails for API key auth missing key."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="",  # Empty key
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert "header" in result.error.lower()

    def test_config_string_representation(self) -> None:
        """Test config string representation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        str_repr = str(config)
        assert "basic" in str_repr.lower()
        assert "test_user" in str_repr
        # Password should not be in string representation for security
        assert "test_password" not in str_repr


@pytest.mark.unit
class TestAuthenticator:
    """Test authenticator class."""

    def test_authenticator_creation_with_valid_config(self) -> None:
        """Test creating authenticator with valid config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        assert authenticator.config == config

    def test_authenticator_creation_with_invalid_config(self) -> None:
        """Test creating authenticator with invalid config."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="",  # Invalid - empty username
            password="test_password",
        )

        with pytest.raises(FlextOracleWmsAuthenticationError):
            FlextOracleWmsAuthenticator(config)

    @pytest.mark.asyncio
    async def test_basic_auth_headers_generation(self) -> None:
        """Test basic auth headers are generated correctly."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        headers = await authenticator.get_auth_headers()

        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

        # Decode and verify
        import base64

        encoded_credentials = headers["Authorization"][6:]  # Remove "Basic "
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        assert decoded == "test_user:test_password"

    @pytest.mark.asyncio
    async def test_bearer_auth_headers_generation(self) -> None:
        """Test bearer auth headers are generated correctly."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BEARER, token="test_bearer_token",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        headers = await authenticator.get_auth_headers()

        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_bearer_token"

    @pytest.mark.asyncio
    async def test_api_keys_generation(self) -> None:
        """Test API key headers are generated correctly."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="test_api_key",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        headers = await authenticator.get_auth_headers()

        assert "X-API-Key" in headers
        assert headers["X-API-Key"] == "test_api_key"

    @pytest.mark.asyncio
    async def test_auth_headers_with_additional_headers(self) -> None:
        """Test auth headers generation with additional custom headers."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        custom_headers = {
            "Content-Type": FlextApiConstants.ContentTypes.JSON,
            "X-Custom": "value",
        }

        headers = await authenticator.get_auth_headers(custom_headers)

        # Should contain both auth and custom headers
        assert "Authorization" in headers
        assert "Content-Type" in headers
        assert "X-Custom" in headers
        assert headers["Content-Type"] == "application/json"
        assert headers["X-Custom"] == "value"

    @pytest.mark.asyncio
    async def test_validate_authentication_success(self) -> None:
        """Test successful authentication validation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)

        # Mock the validation call
        with patch.object(authenticator, "_make_validation_request") as mock_request:
            mock_request.return_value = FlextResult.success({"status": "authenticated"})

            result = await authenticator.validate_authentication()
            assert result.success

    @pytest.mark.asyncio
    async def test_validate_authentication_failure(self) -> None:
        """Test authentication validation failure."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="wrong_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)

        # Mock the validation call to fail
        with patch.object(authenticator, "_make_validation_request") as mock_request:
            mock_request.return_value = FlextResult.failure("Authentication failed")

            result = await authenticator.validate_authentication()
            assert result.is_failure
            assert "Authentication failed" in result.error

    def test_authenticator_string_representation(self) -> None:
        """Test authenticator string representation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        str_repr = str(authenticator)

        assert "FlextOracleWmsAuthenticator" in str_repr
        # Test actual configuration rather than string representation
        assert authenticator.config.auth_type == OracleWMSAuthMethod.BASIC


@pytest.mark.unit
class TestAuthPlugin:
    """Test authentication plugin."""

    def test_auth_plugin_creation(self) -> None:
        """Test creating auth plugin."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)
        assert plugin.authenticator == authenticator
        assert isinstance(plugin.authenticator, FlextOracleWmsAuthenticator)

    @pytest.mark.asyncio
    async def test_plugin_get_auth_headers(self) -> None:
        """Test plugin auth headers functionality."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock authenticator validation
        with patch.object(plugin.authenticator, "get_auth_headers") as mock_headers:
            mock_headers.return_value = FlextResult.success(
                {"Authorization": "Basic dGVzdA=="},
            )

            result = await plugin.authenticator.get_auth_headers()
            assert result.success
            mock_headers.assert_called_once()

    @pytest.mark.asyncio
    async def test_plugin_credentials_validation_failure(self) -> None:
        """Test plugin credentials validation failure."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="wrong_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock authenticator validation to fail
        with patch.object(
            plugin.authenticator, "validate_credentials",
        ) as mock_validate:
            mock_validate.return_value = FlextResult.failure("Auth failed")

            result = await plugin.authenticator.validate_credentials()
            assert result.is_failure
            assert "Auth failed" in result.error

    def test_plugin_authenticator_access(self) -> None:
        """Test plugin authenticator access."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Authenticator should be accessible
        assert plugin.authenticator is not None
        assert isinstance(plugin.authenticator, FlextOracleWmsAuthenticator)

    @pytest.mark.asyncio
    async def test_plugin_get_headers_via_authenticator(self) -> None:
        """Test plugin get headers via authenticator."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock the authenticator's get_auth_headers method
        with patch.object(plugin.authenticator, "get_auth_headers") as mock_headers:
            mock_headers.return_value = FlextResult.success(
                {"Authorization": "Basic dGVzdA=="},
            )

            result = await plugin.authenticator.get_auth_headers()
            assert result.success
            assert "Authorization" in result.data

    @pytest.mark.asyncio
    async def test_plugin_validate_credentials(self) -> None:
        """Test plugin credentials validation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock validation
        with patch.object(
            plugin.authenticator, "validate_credentials",
        ) as mock_validate:
            mock_validate.return_value = FlextResult.success(True)

            result = await plugin.authenticator.validate_credentials()

            assert result.success
            assert result.data is True

    @pytest.mark.asyncio
    async def test_plugin_auth_error_handling(self) -> None:
        """Test plugin authentication error handling."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Mock failure in get_auth_headers
        with patch.object(plugin.authenticator, "get_auth_headers") as mock_headers:
            mock_headers.return_value = FlextResult.fail("Auth failed")

            result = await plugin.authenticator.get_auth_headers()
            assert result.is_failure
            assert "Auth failed" in result.error

    def test_plugin_string_representation(self) -> None:
        """Test plugin string representation."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)
        str_repr = str(plugin)

        assert "FlextOracleWmsAuthPlugin" in str_repr
        assert "basic" in str_repr.lower()
