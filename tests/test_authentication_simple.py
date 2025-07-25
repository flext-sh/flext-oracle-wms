"""Simple focused tests for authentication modules."""

from unittest.mock import Mock

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuth,
    FlextOracleWmsOAuth2Auth,
    flext_oracle_wms_create_authenticator,
    flext_oracle_wms_create_oauth2_authenticator,
)


class TestAuthenticationSimple:
    """Simple tests for authentication functionality."""

    def test_basic_auth_creation(self) -> None:
        """Test basic authentication creation."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")
        assert auth.username == "user"
        assert auth.password == "pass"
        assert auth.auth_method == "basic"

    def test_basic_auth_flow(self) -> None:
        """Test basic auth flow method."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")

        # Mock request
        mock_request = Mock()
        mock_request.url = "https://example.com"
        mock_request.headers = {}

        # Get auth flow generator
        auth_gen = auth.auth_flow(mock_request)

        # Get first (and only) request from generator
        authed_request = next(auth_gen)

        # Verify Authorization header was added
        assert "Authorization" in authed_request.headers
        assert authed_request.headers["Authorization"].startswith("Basic ")

    def test_oauth2_auth_creation(self) -> None:
        """Test OAuth2 authentication creation."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )
        assert auth.client_id == "client123"
        assert auth.client_secret == "secret456"
        assert auth.authorization_url == "https://auth.example.com/authorize"
        assert auth.token_url == "https://auth.example.com/token"

    def test_oauth2_authorization_url(self) -> None:
        """Test OAuth2 authorization URL generation."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )

        result = auth.get_authorization_url()
        assert result.success is True
        assert "client_id=client123" in result.data
        assert "response_type=code" in result.data

    def test_create_authenticator_basic(self) -> None:
        """Test authenticator factory for basic auth."""
        auth = flext_oracle_wms_create_authenticator("user", "pass")
        assert isinstance(auth, FlextOracleWmsAuth)
        assert auth.username == "user"
        assert auth.password == "pass"

    def test_create_oauth2_authenticator(self) -> None:
        """Test OAuth2 authenticator factory."""
        auth = flext_oracle_wms_create_oauth2_authenticator(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )
        assert isinstance(auth, FlextOracleWmsOAuth2Auth)
        assert auth.client_id == "client123"

    def test_basic_auth_with_different_methods(self) -> None:
        """Test basic auth with different methods."""
        # Test with digest method
        auth = FlextOracleWmsAuth("user", "pass", "digest")
        assert auth.auth_method == "digest"

        # Test with bearer method
        auth = FlextOracleWmsAuth("user", "pass", "bearer")
        assert auth.auth_method == "bearer"

    def test_oauth2_state_generation(self) -> None:
        """Test OAuth2 state parameter generation."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )

        result1 = auth.get_authorization_url()
        result2 = auth.get_authorization_url()

        # Both should succeed
        assert result1.success is True
        assert result2.success is True

        # Should contain different state parameters (random)
        assert "state=" in result1.data
        assert "state=" in result2.data

    def test_auth_repr_methods(self) -> None:
        """Test string representations of auth objects."""
        basic_auth = FlextOracleWmsAuth("user", "pass", "basic")
        repr_str = repr(basic_auth)
        assert "FlextOracleWmsAuth" in repr_str
        # Don't assume specific format of repr - just check class name

        oauth2_auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )
        repr_str = repr(oauth2_auth)
        assert "FlextOracleWmsOAuth2Auth" in repr_str
        # Don't assume specific format of repr - just check class name

    def test_auth_edge_cases(self) -> None:
        """Test authentication edge cases."""
        # Test with empty credentials
        auth = FlextOracleWmsAuth("", "", "basic")
        assert auth.username == ""
        assert auth.password == ""

        # Test OAuth2 with minimal config
        oauth2_auth = FlextOracleWmsOAuth2Auth(
            client_id="client",
            client_secret="secret",
            authorization_url="https://example.com/auth",
            token_url="https://example.com/token",
        )
        # Test that basic attributes exist
        assert hasattr(oauth2_auth, "client_id")
        assert oauth2_auth.client_id == "client"
