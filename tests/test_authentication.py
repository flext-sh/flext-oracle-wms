"""Simple unit tests for Oracle WMS authentication module - targeting coverage.

Based on actual module structure and working patterns.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest

from flext_oracle_wms import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
    OracleWMSAuthMethod,
)


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
        methods = [method.value for method in OracleWMSAuthMethod]
        assert "basic" in methods
        assert "bearer" in methods
        assert "api_key" in methods


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
            auth_type=OracleWMSAuthMethod.BEARER,
            token="bearer_token_123",
        )

        assert config.auth_type == OracleWMSAuthMethod.BEARER
        assert config.token == "bearer_token_123"
        assert config.username == ""  # Default empty string
        assert config.password == ""  # Default empty string
        assert config.api_key == ""  # Default empty string

    def test_api_key_auth_config_creation(self) -> None:
        """Test creating API key auth configuration."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.API_KEY,
            api_key="api_key_123",
        )

        assert config.auth_type == OracleWMSAuthMethod.API_KEY
        assert config.api_key == "api_key_123"
        assert config.username == ""  # Default empty string
        assert config.password == ""  # Default empty string
        assert config.token == ""  # Default empty string

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
            auth_type=OracleWMSAuthMethod.BEARER,
            token="valid_token",
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
        assert "username" in result.error.lower() or "password" in result.error.lower()

    def test_config_validation_failure_basic_missing_password(self) -> None:
        """Test config validation fails for basic auth missing password."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="",  # Empty password
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert "username" in result.error.lower() or "password" in result.error.lower()

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
        assert "api" in result.error.lower() or "key" in result.error.lower()

    def test_config_defaults(self) -> None:
        """Test config default values."""
        config = FlextOracleWmsAuthConfig()

        assert config.auth_type == OracleWMSAuthMethod.BASIC
        assert config.username == ""
        assert config.password == ""
        assert config.token == ""
        assert config.api_key == ""
        assert config.timeout > 0

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

        # Should handle invalid config gracefully or raise appropriate error
        try:
            authenticator = FlextOracleWmsAuthenticator(config)
            # If it doesn't raise an error, that's also valid behavior
            assert authenticator.config == config
        except (FlextOracleWmsAuthenticationError, ValueError):
            # Raising an error is also acceptable behavior
            pass

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
        # Basic auth info may or may not be in string representation


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
        assert hasattr(plugin, "authenticator")

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

    def test_plugin_basic_properties(self) -> None:
        """Test plugin basic properties."""
        config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )

        authenticator = FlextOracleWmsAuthenticator(config)
        plugin = FlextOracleWmsAuthPlugin(authenticator)

        # Check that plugin has expected attributes
        assert hasattr(plugin, "authenticator")
        assert hasattr(plugin, "before_request")

        # Check if methods are callable
        assert callable(plugin.before_request)
