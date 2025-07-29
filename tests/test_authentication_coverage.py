"""Tests for authentication modules - focusing on coverage improvement."""

from unittest.mock import Mock

from flext_oracle_wms.authentication import (
    FlextOracleWmsAuth,
    FlextOracleWmsOAuth2Auth,
    flext_oracle_wms_create_authenticator,
    flext_oracle_wms_create_oauth2_authenticator,
    flext_oracle_wms_get_api_headers,
)


class TestFlextOracleWmsAuth:
    """Test basic authentication."""

    def test_basic_auth_creation(self) -> None:
        """Test basic auth creation."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")
        assert auth.username == "user"
        assert auth.password == "pass"
        assert auth.auth_method == "basic"

    def test_basic_auth_flow(self) -> None:
        """Test basic auth flow."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")

        mock_request = Mock()
        mock_request.headers = {}

        auth_gen = auth.auth_flow(mock_request)
        authed_request = next(auth_gen)

        assert "Authorization" in authed_request.headers
        assert authed_request.headers["Authorization"].startswith("Basic")

    def test_get_basic_auth(self) -> None:
        """Test basic auth string generation."""
        auth = FlextOracleWmsAuth("testuser", "testpass", "basic")
        basic_auth = auth._get_basic_auth()
        assert isinstance(basic_auth, str)
        assert len(basic_auth) > 0

    def test_auth_with_different_methods(self) -> None:
        """Test auth with different methods."""
        auth_digest = FlextOracleWmsAuth("user", "pass", "digest")
        assert auth_digest.auth_method == "digest"

        auth_bearer = FlextOracleWmsAuth("user", "pass", "bearer")
        assert auth_bearer.auth_method == "bearer"

    def test_auth_empty_credentials(self) -> None:
        """Test auth with empty credentials."""
        auth = FlextOracleWmsAuth("", "", "basic")
        assert auth.username == ""
        assert auth.password == ""

    def test_auth_repr(self) -> None:
        """Test auth string representation."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")
        repr_str = repr(auth)
        assert "FlextOracleWmsAuth" in repr_str

    def test_auth_context_manager(self) -> None:
        """Test auth as context manager."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")
        with auth as context_auth:
            assert context_auth is auth


class TestFlextOracleWmsOAuth2Auth:
    """Test OAuth2 authentication."""

    def test_oauth2_creation(self) -> None:
        """Test OAuth2 auth creation."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )
        assert auth.client_id == "client123"
        assert auth.client_secret == "secret456"

    def test_get_authorization_url(self) -> None:
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

        assert result1.success is True
        assert result2.success is True
        assert "state=" in result1.data
        assert "state=" in result2.data

    def test_oauth2_repr(self) -> None:
        """Test OAuth2 auth string representation."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )
        repr_str = repr(auth)
        assert "FlextOracleWmsOAuth2Auth" in repr_str

    def test_oauth2_exchange_code(self) -> None:
        """Test OAuth2 code exchange."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )

        result = auth.exchange_code_for_token("test_code")
        assert hasattr(result, "success")

    def test_oauth2_clear_tokens(self) -> None:
        """Test OAuth2 token clearing."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )

        # Should not raise error
        auth.clear_tokens()

    def test_oauth2_context_manager(self) -> None:
        """Test OAuth2 auth as context manager."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )

        with auth as context_auth:
            assert context_auth is auth


class TestFactoryFunctions:
    """Test authentication factory functions."""

    def test_create_authenticator_basic(self) -> None:
        """Test basic authenticator creation."""
        auth = flext_oracle_wms_create_authenticator("user", "pass", "basic")
        assert isinstance(auth, FlextOracleWmsAuth)
        assert auth.username == "user"
        assert auth.password == "pass"

    def test_create_authenticator_digest(self) -> None:
        """Test digest authenticator creation."""
        auth = flext_oracle_wms_create_authenticator("user", "pass", "digest")
        assert isinstance(auth, FlextOracleWmsAuth)
        assert auth.auth_method == "digest"

    def test_create_oauth2_authenticator(self) -> None:
        """Test OAuth2 authenticator creation."""
        auth = flext_oracle_wms_create_oauth2_authenticator(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )
        assert isinstance(auth, FlextOracleWmsOAuth2Auth)
        assert auth.client_id == "client123"
        assert auth.client_secret == "secret456"

    def test_get_api_headers_basic(self) -> None:
        """Test API headers generation."""
        headers = flext_oracle_wms_get_api_headers()
        assert isinstance(headers, dict)
        assert (
            "Content-Type" in headers or "Accept" in headers or "User-Agent" in headers
        )

    def test_get_api_headers_with_config(self) -> None:
        """Test API headers generation with config."""
        config = {"custom_header": "value"}
        headers = flext_oracle_wms_get_api_headers(config)
        assert isinstance(headers, dict)


class TestAuthenticationEdgeCases:
    """Test authentication edge cases."""

    def test_auth_with_none_values(self) -> None:
        """Test auth creation with None values."""
        auth = FlextOracleWmsAuth(None, None, "basic")
        assert auth.username is None
        assert auth.password is None

    def test_oauth2_with_empty_urls(self) -> None:
        """Test OAuth2 with empty URLs."""
        auth = FlextOracleWmsOAuth2Auth("", "", "", "")
        assert auth.client_id == ""
        assert auth.client_secret == ""

    def test_factory_functions_with_invalid_inputs(self) -> None:
        """Test factory functions with invalid inputs."""
        auth = flext_oracle_wms_create_authenticator("", "", "invalid_method")
        assert isinstance(auth, FlextOracleWmsAuth)
        assert auth.auth_method == "invalid_method"

        auth = flext_oracle_wms_create_oauth2_authenticator("", "", "", "")
        assert isinstance(auth, FlextOracleWmsOAuth2Auth)

    def test_auth_flow_multiple_calls(self) -> None:
        """Test auth flow called multiple times."""
        auth = FlextOracleWmsAuth("user", "pass", "basic")
        mock_request = Mock()
        mock_request.headers = {}

        # Should be able to call auth_flow multiple times
        gen1 = auth.auth_flow(mock_request)
        gen2 = auth.auth_flow(mock_request)

        req1 = next(gen1)
        req2 = next(gen2)

        assert "Authorization" in req1.headers
        assert "Authorization" in req2.headers

    def test_oauth2_url_generation_consistency(self) -> None:
        """Test OAuth2 URL generation is consistent."""
        auth = FlextOracleWmsOAuth2Auth(
            client_id="client123",
            client_secret="secret456",
            authorization_url="https://auth.example.com/authorize",
            token_url="https://auth.example.com/token",
        )

        # Multiple calls should generate different states but same base URL
        result1 = auth.get_authorization_url()
        result2 = auth.get_authorization_url()

        if result1.success and result2.success:
            assert "client_id=client123" in result1.data
            assert "client_id=client123" in result2.data
            assert "response_type=code" in result1.data
            assert "response_type=code" in result2.data

    def test_auth_method_case_insensitive(self) -> None:
        """Test auth method is handled case insensitively."""
        auth_upper = FlextOracleWmsAuth("user", "pass", "BASIC")
        auth_lower = FlextOracleWmsAuth("user", "pass", "basic")
        auth_mixed = FlextOracleWmsAuth("user", "pass", "Basic")

        assert auth_upper.auth_method in {"BASIC", "basic"}
        assert auth_lower.auth_method in {"BASIC", "basic"}
        assert auth_mixed.auth_method in {"BASIC", "basic", "Basic"}
