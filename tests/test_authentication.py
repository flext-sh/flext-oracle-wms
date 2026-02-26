"""Tests for Oracle WMS authentication module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest
from flext_oracle_wms import (
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthSettings,
    OracleWMSAuthMethod,
    create_oracle_wms_client,
)


@pytest.mark.unit
class TestAuthenticationMethod:
    """Test authentication method enum."""

    def test_authentication_method_values(self) -> None:
        """Test authentication method enum values."""
        assert OracleWMSAuthMethod.BASIC.value == "basic"
        assert OracleWMSAuthMethod.OAUTH2.value == "oauth2"
        assert OracleWMSAuthMethod.API_KEY.value == "api_key"
        assert OracleWMSAuthMethod.BEARER.value == "bearer"

    def test_authentication_method_membership(self) -> None:
        """Test authentication method membership."""
        methods = [method.value for method in OracleWMSAuthMethod]
        assert "basic" in methods
        assert "bearer" in methods
        assert "api_key" in methods
        assert "oauth2" in methods


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
            oauth2_client_id="client_id_123",
            oauth2_client_secret="client_secret_456",
        )
        assert config.method == OracleWMSAuthMethod.OAUTH2
        assert config.oauth2_client_id == "client_id_123"
        assert config.oauth2_client_secret == "client_secret_456"

    def test_config_validation_success_basic(self) -> None:
        """Test validate_business_rules succeeds for valid basic auth."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        result = config.validate_business_rules()
        assert result.is_success

    def test_config_validation_failure_basic_missing_credentials(self) -> None:
        """Test validate_business_rules fails for basic auth with no credentials."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
        )
        result = config.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "username" in result.error.lower() or "password" in result.error.lower()

    def test_config_validation_failure_oauth2_missing_credentials(self) -> None:
        """Test validate_business_rules fails for oauth2 with no credentials."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.OAUTH2,
        )
        result = config.validate_business_rules()
        assert result.is_failure
        assert result.error is not None

    def test_config_defaults(self) -> None:
        """Test config default values."""
        config = FlextOracleWmsAuthSettings()
        assert config.method == OracleWMSAuthMethod.BASIC
        assert config.username is None
        assert config.password is None
        assert config.oauth2_scope == "wms.read wms.write"
        assert config.token_refresh_threshold == 300


@pytest.mark.unit
class TestAuthenticator:
    """Test authenticator class."""

    def test_authenticator_creation(self) -> None:
        """Test creating authenticator with config."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        assert authenticator.config == config

    def test_authenticate_basic_success(self) -> None:
        """Test basic auth returns success token."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_success
        assert result.value == "dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ="

    def test_authenticate_oauth2_not_configured(self) -> None:
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.authenticate()
        assert result.is_failure
        assert result.error == "OAuth2 not configured"

    def test_authenticate_basic_failure(self) -> None:
        """Test basic auth fails without credentials."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
        )
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
        assert headers["Authorization"].startswith("Basic ")

    def test_get_auth_headers_failure(self) -> None:
        """Test get_auth_headers fails without credentials."""
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
        )
        authenticator = FlextOracleWmsAuthenticator(config)
        result = authenticator.get_auth_headers()
        assert result.is_failure

    def test_create_oracle_wms_client_not_configured(self) -> None:
        config = FlextOracleWmsAuthSettings(
            method=OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        result = create_oracle_wms_client(config)
        assert result.is_failure
        assert result.error == "Oracle WMS client creation not configured"
