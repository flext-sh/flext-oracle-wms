"""Behavioral tests for Oracle WMS authentication utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import base64

import pytest

from flext_oracle_wms import FlextOracleWmsUtilitiesAuth, FlextOracleWmsUtilitiesClient
from flext_tests import tm
from tests import c, m

_AuthMethod = c.OracleWms.OracleWMSAuthMethod
_BASIC_TOKEN = base64.b64encode(b"test_user:test_password").decode("ascii")


@pytest.mark.unit
class TestsFlextOracleWmsAuthenticationCore:
    """Public-contract behavior of Oracle WMS auth settings, authenticator, client."""

    @pytest.fixture
    def basic_settings(self) -> m.OracleWms.AuthSettings:
        """Return valid BASIC auth settings."""
        return m.OracleWms.AuthSettings(
            method=_AuthMethod.BASIC, username="test_user", password="test_password"
        )

    # --- Auth method enum contract ---------------------------------------

    @pytest.mark.parametrize(
        ("member", "wire_value"),
        [
            (_AuthMethod.BASIC, "basic"),
            (_AuthMethod.BEARER, "bearer"),
            (_AuthMethod.API_KEY, "api_key"),
            (_AuthMethod.OAUTH2, "oauth2"),
        ],
    )
    def test_auth_method_serializes_to_stable_wire_value(
        self, member: c.OracleWms.OracleWMSAuthMethod, wire_value: str
    ) -> None:
        """Each auth method exposes its documented lowercase wire value."""
        tm.that(member, eq=wire_value)
        tm.that({method.value for method in _AuthMethod}, has=member)

    # --- AuthSettings model state ----------------------------------------

    def test_defaults_expose_documented_public_state(self) -> None:
        """A default AuthSettings advertises BASIC auth with empty credentials."""
        settings = m.OracleWms.AuthSettings()
        dumped = settings.model_dump()
        tm.that(dumped["method"], eq=_AuthMethod.BASIC)
        tm.that(dumped["username"], none=True)
        tm.that(dumped["password"], none=True)
        tm.that(dumped["oauth2_client_id"], none=True)
        tm.that(dumped["oauth2_client_secret"], none=True)
        tm.that(dumped["oauth2_scope"], eq="wms.read wms.write")
        tm.that(dumped["token_refresh_threshold"], eq=300)

    def test_supplied_credentials_are_retained(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """BASIC credentials round-trip through public fields."""
        tm.that(basic_settings.method, eq=_AuthMethod.BASIC)
        tm.that(basic_settings.username, eq="test_user")
        tm.that(basic_settings.password, eq="test_password")

    def test_oauth2_credentials_are_retained(self) -> None:
        """OAuth2 client credentials round-trip through public fields."""
        settings = m.OracleWms.AuthSettings(
            method=_AuthMethod.OAUTH2,
            oauth2_client_id="client_id",
            oauth2_client_secret="client_secret",
        )
        tm.that(settings.method, eq=_AuthMethod.OAUTH2)
        tm.that(settings.oauth2_client_id, eq="client_id")
        tm.that(settings.oauth2_client_secret, eq="client_secret")

    @pytest.mark.parametrize("raw", ["BASIC", " Basic ", "basic", "BaSiC"])
    def test_normalized_method_is_case_and_whitespace_insensitive(
        self, raw: str
    ) -> None:
        """normalized_method canonicalizes the configured method string."""
        settings = m.OracleWms.AuthSettings(method=raw)
        tm.that(settings.normalized_method, eq="basic")

    # --- validate_business_rules -----------------------------------------

    def test_validate_business_rules_accepts_complete_basic(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """Complete BASIC credentials pass business-rule validation."""
        result = FlextOracleWmsUtilitiesAuth.validate_auth_settings(basic_settings)
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_validate_business_rules_accepts_complete_oauth2(self) -> None:
        """Complete OAuth2 credentials pass business-rule validation."""
        settings = m.OracleWms.AuthSettings(
            method=_AuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        result = FlextOracleWmsUtilitiesAuth.validate_auth_settings(settings)
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    @pytest.mark.parametrize(
        ("settings", "expected_error"),
        [
            (
                m.OracleWms.AuthSettings(method=_AuthMethod.BASIC),
                "Basic auth requires username and password",
            ),
            (
                m.OracleWms.AuthSettings(
                    method=_AuthMethod.BASIC, username="only_user"
                ),
                "Basic auth requires username and password",
            ),
            (
                m.OracleWms.AuthSettings(method=_AuthMethod.OAUTH2),
                "OAuth2 requires client_id and client_secret",
            ),
            (
                m.OracleWms.AuthSettings(method=_AuthMethod.API_KEY),
                "Unsupported auth method: api_key",
            ),
        ],
    )
    def test_validate_business_rules_reports_specific_failure(
        self, settings: m.OracleWms.AuthSettings, expected_error: str
    ) -> None:
        """Incomplete/unsupported configs fail with a specific diagnostic."""
        result = FlextOracleWmsUtilitiesAuth.validate_auth_settings(settings)
        tm.fail(result)
        tm.that(result.error, eq=expected_error)

    # --- Authenticator.authenticate --------------------------------------

    def test_authenticator_behavior_reflects_its_settings(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """The authenticator's public behavior reflects the injected settings."""
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(basic_settings)
        # NOTE (multi-agent): auth lane keeps the injected settings private
        # (``_settings``); retention is asserted via observable public behavior.
        tm.that(authenticator.normalized_method, eq=basic_settings.normalized_method)
        tm.that(authenticator.authenticate().unwrap(), eq=_BASIC_TOKEN)

    def test_authenticate_basic_yields_decodable_credentials(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """BASIC authentication returns a base64 token decoding to user:password."""
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(basic_settings)
        result = authenticator.authenticate()
        tm.ok(result)
        token = result.unwrap()
        tm.that(token, eq=_BASIC_TOKEN)
        tm.that(base64.b64decode(token).decode(), eq="test_user:test_password")

    def test_authenticate_is_idempotent(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """Repeated authentication yields the same token for the same credentials."""
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(basic_settings)
        first = authenticator.authenticate()
        second = authenticator.authenticate()
        tm.ok(first)
        tm.ok(second)
        tm.that(first.unwrap(), eq=second.unwrap())

    @pytest.mark.parametrize(
        ("settings", "expected_error"),
        [
            (
                m.OracleWms.AuthSettings(method=_AuthMethod.BASIC),
                "Username and password required for basic auth",
            ),
            (
                m.OracleWms.AuthSettings(method=_AuthMethod.OAUTH2),
                "OAuth2 credentials required",
            ),
            (
                m.OracleWms.AuthSettings(
                    method=_AuthMethod.OAUTH2,
                    oauth2_client_id="id",
                    oauth2_client_secret="secret",
                ),
                "OAuth2 not configured",
            ),
            (
                m.OracleWms.AuthSettings(method=_AuthMethod.BEARER),
                "Unsupported auth method: bearer",
            ),
        ],
    )
    def test_authenticate_failure_carries_specific_error(
        self, settings: m.OracleWms.AuthSettings, expected_error: str
    ) -> None:
        """Every unauthenticatable configuration fails with a precise message."""
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        tm.fail(result)
        tm.that(result.error, eq=expected_error)

    # --- Authenticator.get_auth_headers ----------------------------------

    def test_get_auth_headers_basic_emits_basic_scheme(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """BASIC headers carry the token under an 'Authorization: Basic' entry."""
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(basic_settings)
        result = authenticator.get_auth_headers()
        tm.ok(result)
        headers = result.unwrap()
        tm.that(headers, eq={"Authorization": f"Basic {_BASIC_TOKEN}"})

    def test_get_auth_headers_propagates_authentication_failure(self) -> None:
        """Header derivation fails when the underlying authentication fails."""
        settings = m.OracleWms.AuthSettings(method=_AuthMethod.BASIC)
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.get_auth_headers()
        tm.fail(result)
        tm.that(result.error, none=False)

    # --- Client.from_auth_settings ---------------------------------------

    def test_from_auth_settings_builds_client_for_basic_auth(
        self, basic_settings: m.OracleWms.AuthSettings
    ) -> None:
        """Valid BASIC settings yield a concrete Oracle WMS client."""
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(basic_settings)
        tm.ok(result)
        tm.that(result.unwrap(), is_=FlextOracleWmsUtilitiesClient.Client)

    def test_from_auth_settings_rejects_invalid_credentials(self) -> None:
        """A client cannot be built from credentials that fail validation."""
        settings = m.OracleWms.AuthSettings(method=_AuthMethod.BASIC)
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(settings)
        tm.fail(result)
        tm.that(result.error, eq="Basic auth requires username and password")

    def test_from_auth_settings_rejects_non_basic_auth(self) -> None:
        """The runtime client only supports BASIC auth and refuses OAuth2."""
        settings = m.OracleWms.AuthSettings(
            method=_AuthMethod.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(settings)
        tm.fail(result)
        assert (
            result.error
            == "Oracle WMS runtime client currently supports BASIC auth only"
        )


__all__: list[str] = ["TestsFlextOracleWmsAuthenticationCore"]
