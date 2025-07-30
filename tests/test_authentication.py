"""Test Oracle WMS authentication functionality."""

import pytest

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
)
from flext_oracle_wms.constants import OracleWMSAuthMethod


def test_basic_auth_config_creation() -> None:
    """Test basic authentication config creation."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )
    assert config.auth_type == OracleWMSAuthMethod.BASIC
    assert config.username == "user"
    assert config.password == "pass"


def test_oauth2_auth_config_creation() -> None:
    """Test OAuth2 authentication config creation."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.OAUTH2,
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token"
    )
    assert config.auth_type == OracleWMSAuthMethod.OAUTH2
    assert config.client_id == "test_id"
    assert config.client_secret == "test_secret"


def test_authenticator_creation() -> None:
    """Test authenticator creation."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )
    authenticator = FlextOracleWmsAuthenticator(config)
    assert authenticator.config == config


def test_basic_auth_validation() -> None:
    """Test basic auth credential validation."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )
    result = config.validate_domain_rules()
    assert result.is_success is True


def test_basic_auth_validation_empty_credentials() -> None:
    """Test validation with empty credentials."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="",
        password=""
    )
    result = config.validate_domain_rules()
    assert result.is_success is False


def test_oauth2_validation_missing_fields() -> None:
    """Test OAuth2 validation with missing required fields."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.OAUTH2,
        client_id="test_id",
        # Missing client_secret, authorization_url, token_url
    )
    result = config.validate_domain_rules()
    assert result.is_success is False


@pytest.mark.asyncio
async def test_authenticator_get_headers() -> None:
    """Test getting authentication headers."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )
    authenticator = FlextOracleWmsAuthenticator(config)

    headers_result = await authenticator.get_headers()
    assert headers_result.is_success is True

    headers = headers_result.data
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ")


@pytest.mark.asyncio
async def test_authenticator_oauth2_headers() -> None:
    """Test OAuth2 authentication headers."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.OAUTH2,
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token"
    )
    authenticator = FlextOracleWmsAuthenticator(config)

    # OAuth2 implementation would need token management
    headers_result = await authenticator.get_headers()
    assert headers_result.is_success is True


def test_auth_plugin_creation() -> None:
    """Test authentication plugin creation."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )

    # FlextOracleWmsAuthPlugin follows FlextApiPlugin interface
    plugin = FlextOracleWmsAuthPlugin(config)
    assert plugin is not None


@pytest.mark.asyncio
async def test_plugin_request_processing() -> None:
    """Test plugin request processing."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )
    plugin = FlextOracleWmsAuthPlugin(config)

    # Mock request object would be needed for full testing
    # This tests the plugin instantiation and basic structure
    assert hasattr(plugin, "process_request")
    assert hasattr(plugin, "process_response")
