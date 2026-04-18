"""Tests for Oracle WMS authentication module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsUtilitiesAuth, FlextOracleWmsUtilitiesClient
from tests import c, m


@pytest.mark.unit
class TestAuthenticationMethodCore:
    """Test authentication method enum."""

    def test_authentication_method_values(self) -> None:
        """Test authentication method enum values."""
        assert c.OracleWms.OracleWMSAuthMethod.BASIC == "basic"
        assert c.OracleWms.OracleWMSAuthMethod.BEARER == "bearer"
        assert c.OracleWms.OracleWMSAuthMethod.API_KEY == "api_key"
        assert c.OracleWms.OracleWMSAuthMethod.OAUTH2 == "oauth2"

    def test_authentication_method_membership(self) -> None:
        """Test authentication method membership."""
        values = [method.value for method in c.OracleWms.OracleWMSAuthMethod]
        assert "basic" in values
        assert "bearer" in values
        assert "api_key" in values
        assert "oauth2" in values


@pytest.mark.unit
class TestAuthenticationConfigCore:
    """Test authentication configuration."""

    def test_basic_auth_config_creation(self) -> None:
        """Test creating basic auth configuration."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        assert settings.method == c.OracleWms.OracleWMSAuthMethod.BASIC
        assert settings.username == "test_user"
        assert settings.password == "test_password"

    def test_oauth2_auth_config_creation(self) -> None:
        """Test creating OAuth2 auth configuration."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="client_id",
            oauth2_client_secret="client_secret",
        )
        assert settings.method == c.OracleWms.OracleWMSAuthMethod.OAUTH2
        assert settings.oauth2_client_id == "client_id"
        assert settings.oauth2_client_secret == "client_secret"

    def test_config_defaults(self) -> None:
        """Test settings default values."""
        settings = m.OracleWms.AuthSettings()
        assert settings.method == c.OracleWms.OracleWMSAuthMethod.BASIC
        assert settings.username is None
        assert settings.password is None
        assert settings.oauth2_client_id is None
        assert settings.oauth2_client_secret is None
        assert settings.oauth2_scope == "wms.read wms.write"
        assert settings.token_refresh_threshold == 300

    def test_config_validation_success_basic(self) -> None:
        """Test validate_business_rules succeeds for valid basic auth."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        result = settings.validate_business_rules()
        assert result.success

    def test_config_validation_failure_basic_no_credentials(self) -> None:
        """Test validate_business_rules fails for basic auth without credentials."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC
        )
        result = settings.validate_business_rules()
        assert result.failure
        assert result.error is not None

    def test_config_validation_failure_oauth2_no_credentials(self) -> None:
        """Test validate_business_rules fails for oauth2 without credentials."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.OAUTH2
        )
        result = settings.validate_business_rules()
        assert result.failure
        assert result.error is not None

    def test_config_validation_success_oauth2(self) -> None:
        """Test validate_business_rules succeeds for valid oauth2."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        result = settings.validate_business_rules()
        assert result.success


@pytest.mark.unit
class TestAuthenticatorCore:
    """Test authenticator class."""

    def test_authenticator_creation(self) -> None:
        """Test creating authenticator with valid settings."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        assert authenticator.settings is settings

    def test_authenticate_basic_success(self) -> None:
        """Test basic auth authenticate returns success."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        assert result.success
        assert result.value == "dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ="

    def test_authenticate_basic_failure(self) -> None:
        """Test basic auth authenticate fails without credentials."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        assert result.failure

    def test_authenticate_oauth2_not_configured(self) -> None:
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        assert result.failure
        assert result.error == "OAuth2 not configured"

    def test_authenticate_oauth2_failure(self) -> None:
        """Test oauth2 authenticate fails without credentials."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.OAUTH2
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        assert result.failure

    def test_get_auth_headers_success(self) -> None:
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.get_auth_headers()
        assert result.success
        headers = result.value
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

    def test_create_oracle_wms_client(self) -> None:
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC,
            username="test_user",
            password="test_password",
        )
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(settings)
        assert result.success
        assert isinstance(result.value, FlextOracleWmsUtilitiesClient.Client)

    def test_get_auth_headers_failure(self) -> None:
        """Test get_auth_headers fails without credentials."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BASIC
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.get_auth_headers()
        assert result.failure

    def test_unsupported_auth_method(self) -> None:
        """Test authenticate fails with unsupported method."""
        settings = m.OracleWms.AuthSettings(
            method=c.OracleWms.OracleWMSAuthMethod.BEARER
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        assert result.failure
