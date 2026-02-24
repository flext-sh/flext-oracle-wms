"""Tests for Oracle WMS authentication module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest

from flext_oracle_wms import (
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthSettings,
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
        assert OracleWMSAuthMethod.OAUTH2 == "oauth2"

    def test_authentication_method_membership(self) -> None:
        """Test authentication method membership."""
        values = [method.value for method in OracleWMSAuthMethod]
        assert "basic" in values
        assert "bearer" in values
        assert "api_key" in values
        assert "oauth2" in values


@pytest.mark.unit
class TestAuthenticationConfig:
    """Test authentication configuration."""

    def test_basic_auth_config_creation(self) -> None:
        """Test creating basic auth configuration."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        assert config.method == OracleWMSAuthMethod.BASIC
        assert config.username == "test_user"
        assert config.password == "test_password"

    def test_oauth2_auth_config_creation(self) -> None:
        """Test creating OAuth2 auth configuration."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="client_id",
            oauth2_client_secret="client_secret",
        )
        assert config.method == OracleWMSAuthMethod.OAUTH2
        assert config.oauth2_client_id == "client_id"
        assert config.oauth2_client_secret == "client_secret"

    def test_config_defaults(self) -> None:
        """Test config default values."""
        config = FlextOracleWmsAuthSettings()
        assert config.method == OracleWMSAuthMethod.BASIC
        assert config.username is None
        assert config.password is None
        assert config.oauth2_client_id is None
        assert config.oauth2_client_secret is None
        assert config.oauth2_scope == "wms.read wms.write"
        assert config.token_refresh_threshold == 300

    def test_config_validation_success_basic(self) -> None:
        """Test validate_business_rules succeeds for valid basic auth."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        result = config.validate_business_rules()
        assert result.is_success

    def test_config_validation_failure_basic_no_credentials(self) -> None:
        """Test validate_business_rules fails for basic auth without credentials."""
        config = FlextOracleWmsAuthSettings(method=OracleWMSAuthMethod.BASIC)
        result = config.validate_business_rules()
        assert result.is_failure
        assert result.error is not None

    def test_config_validation_failure_oauth2_no_credentials(self) -> None:
        """Test validate_business_rules fails for oauth2 without credentials."""
        config = FlextOracleWmsAuthSettings(method=OracleWMSAuthMethod.OAUTH2)
        result = config.validate_business_rules()
        assert result.is_failure
        assert result.error is not None

    def test_config_validation_success_oauth2(self) -> None:
        """Test validate_business_rules succeeds for valid oauth2."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        result = config.validate_business_rules()
        assert result.is_success


@pytest.mark.unit
class TestAuthenticator:
    """Test authenticator class."""

    def test_authenticator_creation(self) -> None:
        """Test creating authenticator with valid config."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        assert authenticator.config is config

    def test_authenticate_basic_success(self) -> None:
        """Test basic auth authenticate returns success."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_success

    def test_authenticate_basic_failure(self) -> None:
        """Test basic auth authenticate fails without credentials."""
        config = FlextOracleWmsAuthSettings(method=OracleWMSAuthMethod.BASIC)
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_failure

    def test_authenticate_oauth2_success(self) -> None:
        """Test oauth2 authenticate returns success."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_success

    def test_authenticate_oauth2_failure(self) -> None:
        """Test oauth2 authenticate fails without credentials."""
        config = FlextOracleWmsAuthSettings(method=OracleWMSAuthMethod.OAUTH2)
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_failure

    def test_get_auth_headers_success(self) -> None:
        """Test get_auth_headers returns Authorization header."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.get_auth_headers()
        assert result.is_success
        headers = result.value
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Bearer ")

    def test_get_auth_headers_failure(self) -> None:
        """Test get_auth_headers fails without credentials."""
        config = FlextOracleWmsAuthSettings(method=OracleWMSAuthMethod.BASIC)
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.get_auth_headers()
        assert result.is_failure

    def test_unsupported_auth_method(self) -> None:
        """Test authenticate fails with unsupported method."""
        config = FlextOracleWmsAuthSettings(method=OracleWMSAuthMethod.BEARER)
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_failure
