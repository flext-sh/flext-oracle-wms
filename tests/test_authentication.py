"""Test Oracle WMS authentication functionality."""

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
)
from flext_oracle_wms.constants import OracleWMSAuthMethod


def test_basic_auth_creation() -> None:
    """Test basic authentication creation."""
    config = FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username="user",
        password="pass"
    )
    assert config.username == "user"
    assert config.password == "pass"
    assert config.auth_type == OracleWMSAuthMethod.BASIC


def test_basic_auth_validation() -> None:
    """Test credential validation."""
    auth = FlextOracleWmsAuth("user", "pass")
    result = auth.flext_oracle_wms_validate_credentials()
    assert result.is_success is True


def test_basic_auth_validation_empty() -> None:
    """Test validation with empty credentials."""
    auth = FlextOracleWmsAuth("", "")
    result = auth.flext_oracle_wms_validate_credentials()
    assert result.is_success is False


def test_basic_auth_encoding() -> None:
    """Test basic auth encoding."""
    auth = FlextOracleWmsAuth("user", "pass")
    encoded = auth._get_basic_auth()
    assert isinstance(encoded, str)
    assert len(encoded) > 0


def test_oauth2_auth_creation() -> None:
    """Test OAuth2 authentication creation."""
    oauth = FlextOracleWmsOAuth2Auth(
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token",
    )
    assert oauth.client_id == "test_id"
    assert oauth.client_secret == "test_secret"


def test_oauth2_authorization_url() -> None:
    """Test OAuth2 authorization URL generation."""
    oauth = FlextOracleWmsOAuth2Auth(
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token",
    )
    result = oauth.get_authorization_url()
    assert result.is_success is True
    assert "https://example.com/auth" in result.data


def test_oauth2_clear_tokens() -> None:
    """Test OAuth2 token clearing."""
    oauth = FlextOracleWmsOAuth2Auth(
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token",
    )
    oauth.clear_tokens()
    assert oauth._access_token is None
    assert oauth._refresh_token is None


def test_factory_function_basic() -> None:
    """Test basic authenticator factory function."""
    auth = flext_oracle_wms_create_authenticator("user", "pass")
    assert isinstance(auth, FlextOracleWmsAuth)
    assert auth.username == "user"


def test_factory_function_oauth2() -> None:
    """Test OAuth2 authenticator factory function."""
    oauth = flext_oracle_wms_create_oauth2_authenticator(
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token",
    )
    assert isinstance(oauth, FlextOracleWmsOAuth2Auth)
    assert oauth.client_id == "test_id"


def test_api_headers() -> None:
    """Test API headers generation."""
    headers = flext_oracle_wms_get_api_headers()
    assert "Accept" in headers
    assert "Content-Type" in headers
    assert "User-Agent" in headers
    assert headers["Accept"] == "application/json"


def test_api_headers_with_config() -> None:
    """Test API headers with custom config."""
    config = {"headers": {"Custom-Header": "custom-value"}}
    headers = flext_oracle_wms_get_api_headers(config)
    assert "Custom-Header" in headers
    assert headers["Custom-Header"] == "custom-value"


def test_auth_context_manager() -> None:
    """Test authentication context manager."""
    auth = FlextOracleWmsAuth("user", "pass")
    with auth as ctx_auth:
        assert ctx_auth is auth
    # Verify cleanup occurred
    assert auth._token_cache is None


def test_oauth2_context_manager() -> None:
    """Test OAuth2 authentication context manager."""
    oauth = FlextOracleWmsOAuth2Auth(
        client_id="test_id",
        client_secret="test_secret",
        authorization_url="https://example.com/auth",
        token_url="https://example.com/token",
    )
    with oauth as ctx_oauth:
        assert ctx_oauth is oauth
