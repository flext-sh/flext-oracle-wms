"""Behavioral tests for Oracle WMS authentication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Asserts the observable public contract of the Oracle WMS auth surface:
``m.OracleWms.AuthSettings`` (fields, defaults, ``normalized_method``,
``validate_business_rules``), the ``Authenticator`` (``authenticate`` /
``get_auth_headers`` returning ``r[T]``), and ``Client.from_auth_settings``.
No private attribute access, no patching of the unit under test.

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_oracle_wms import (
    FlextOracleWmsUtilitiesAuth,
    FlextOracleWmsUtilitiesClient,
)
from tests import c, m

# Method enum reused across cases.
_Method = c.OracleWms.OracleWMSAuthMethod

# base64("test_user:test_password") -- the deterministic Basic-auth token contract.
_BASIC_TOKEN = "dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ="


@pytest.mark.unit
class TestsFlextOracleWmsAuthentication:
    """Public-contract behavior of Oracle WMS authentication."""

    # ---- Auth method enum contract --------------------------------------

    @pytest.mark.parametrize(
        ("member", "expected_value"),
        [
            (_Method.BASIC, "basic"),
            (_Method.OAUTH2, "oauth2"),
            (_Method.API_KEY, "api_key"),
            (_Method.BEARER, "bearer"),
        ],
    )
    def test_auth_method_exposes_wire_value(
        self,
        member: c.OracleWms.OracleWMSAuthMethod,
        expected_value: str,
    ) -> None:
        """Each auth method serializes to its documented wire string."""
        tm.that(member.value, eq=expected_value)

    def test_auth_method_enumeration_is_complete(self) -> None:
        """Iterating the enum yields exactly the four supported methods."""
        tm.that(
            {member.value for member in _Method},
            eq={
                "basic",
                "oauth2",
                "api_key",
                "bearer",
            },
        )

    # ---- AuthSettings model contract ------------------------------------

    def test_defaults_produce_basic_method_and_documented_values(self) -> None:
        """A bare AuthSettings defaults to basic auth with documented values."""
        settings = m.OracleWms.AuthSettings()
        tm.that(settings.method, eq=_Method.BASIC)
        tm.that(settings.username, none=True)
        tm.that(settings.password, none=True)
        tm.that(settings.oauth2_scope, eq="wms.read wms.write")
        tm.that(settings.token_refresh_threshold, eq=300)

    def test_basic_settings_retain_supplied_credentials(self) -> None:
        """Basic credentials are exposed unchanged through public fields."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        tm.that(settings.method, eq=_Method.BASIC)
        tm.that(settings.username, eq="test_user")
        tm.that(settings.password, eq="test_password")

    def test_oauth2_settings_retain_supplied_credentials(self) -> None:
        """OAuth2 credentials are exposed unchanged through public fields."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.OAUTH2,
            oauth2_client_id="client_id_123",
            oauth2_client_secret="client_secret_456",
        )
        tm.that(settings.method, eq=_Method.OAUTH2)
        tm.that(settings.oauth2_client_id, eq="client_id_123")
        tm.that(settings.oauth2_client_secret, eq="client_secret_456")

    @pytest.mark.parametrize(
        ("supplied", "expected"),
        [
            (_Method.BASIC, "basic"),
            (" BASIC ", "basic"),
            (_Method.OAUTH2, "oauth2"),
            ("OAuth2", "oauth2"),
        ],
    )
    def test_normalized_method_is_canonical_lowercase(
        self,
        supplied: str,
        expected: str,
    ) -> None:
        """normalized_method canonicalizes casing and whitespace."""
        settings = m.OracleWms.AuthSettings(method=supplied)
        tm.that(settings.normalized_method, eq=expected)

    # ---- validate_business_rules contract -------------------------------

    def test_validate_business_rules_accepts_complete_basic(self) -> None:
        """Complete basic credentials validate successfully."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        assert (
            FlextOracleWmsUtilitiesAuth.validate_auth_settings(settings).unwrap()
            is True
        )

    def test_validate_business_rules_accepts_complete_oauth2(self) -> None:
        """Complete OAuth2 credentials validate successfully."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        assert (
            FlextOracleWmsUtilitiesAuth.validate_auth_settings(settings).unwrap()
            is True
        )

    @pytest.mark.parametrize(
        ("settings", "expected_fragment"),
        [
            (
                m.OracleWms.AuthSettings(method=_Method.BASIC),
                "username and password",
            ),
            (
                m.OracleWms.AuthSettings(method=_Method.BASIC, username="only_user"),
                "username and password",
            ),
            (
                m.OracleWms.AuthSettings(method=_Method.OAUTH2),
                "client_id and client_secret",
            ),
            (
                m.OracleWms.AuthSettings(method=_Method.API_KEY),
                "unsupported auth method",
            ),
        ],
    )
    def test_validate_business_rules_reports_specific_failure(
        self,
        settings: m.OracleWms.AuthSettings,
        expected_fragment: str,
    ) -> None:
        """Incomplete/unsupported configs fail with an explanatory error."""
        result = FlextOracleWmsUtilitiesAuth.validate_auth_settings(settings)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error.lower(), has=expected_fragment)

    # ---- Authenticator.authenticate contract ----------------------------

    def test_authenticator_behavior_reflects_its_settings(self) -> None:
        """The authenticator's public behavior reflects the injected settings."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        # NOTE (multi-agent): auth lane keeps the injected settings private
        # (``_settings``); retention is asserted via observable public behavior.
        tm.that(authenticator.normalized_method, eq=settings.normalized_method)
        tm.that(authenticator.authenticate().unwrap(), eq=_BASIC_TOKEN)

    def test_basic_authenticate_returns_deterministic_token(self) -> None:
        """Basic auth yields the base64 user:password token."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        tm.ok(result)
        tm.that(result.unwrap(), eq=_BASIC_TOKEN)

    def test_basic_authenticate_is_idempotent(self) -> None:
        """Repeated basic authentication yields the same token."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        first = authenticator.authenticate()
        second = authenticator.authenticate()
        tm.that(first.unwrap(), eq=second.unwrap())

    @pytest.mark.parametrize(
        ("settings", "expected_error"),
        [
            (
                m.OracleWms.AuthSettings(method=_Method.BASIC),
                "Username and password required for basic auth",
            ),
            (
                m.OracleWms.AuthSettings(method=_Method.OAUTH2),
                "OAuth2 credentials required",
            ),
            (
                m.OracleWms.AuthSettings(
                    method=_Method.OAUTH2,
                    oauth2_client_id="id",
                    oauth2_client_secret="secret",
                ),
                "OAuth2 not configured",
            ),
        ],
    )
    def test_authenticate_failure_carries_reason(
        self,
        settings: m.OracleWms.AuthSettings,
        expected_error: str,
    ) -> None:
        """Failed authentication surfaces the precise reason."""
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.authenticate()
        tm.fail(result)
        tm.that(result.error, eq=expected_error)

    def test_authenticate_rejects_unsupported_method(self) -> None:
        """A method that is neither basic nor oauth2 is rejected."""
        settings = m.OracleWms.AuthSettings(method=_Method.API_KEY)
        result = FlextOracleWmsUtilitiesAuth.Authenticator(settings).authenticate()
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error.lower(), has="unsupported auth method")

    # ---- Authenticator.get_auth_headers contract ------------------------

    def test_basic_headers_carry_basic_authorization(self) -> None:
        """Successful basic auth builds a Basic Authorization header."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.get_auth_headers()
        tm.ok(result)
        tm.that(result.unwrap(), eq={"Authorization": f"Basic {_BASIC_TOKEN}"})

    def test_headers_fail_when_authentication_fails(self) -> None:
        """Header building propagates the underlying auth failure."""
        settings = m.OracleWms.AuthSettings(method=_Method.BASIC)
        authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(settings)
        result = authenticator.get_auth_headers()
        tm.fail(result)
        tm.that(result.error, none=False)

    # ---- Client.from_auth_settings contract -----------------------------

    def test_client_builds_from_valid_basic_settings(self) -> None:
        """Valid basic settings produce a concrete Client instance."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.BASIC,
            username="test_user",
            password="test_password",
        )
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(settings)
        tm.ok(result)
        tm.that(result.unwrap(), is_=FlextOracleWmsUtilitiesClient.Client)

    def test_client_rejects_invalid_basic_settings(self) -> None:
        """Basic settings missing credentials cannot build a client."""
        settings = m.OracleWms.AuthSettings(method=_Method.BASIC)
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(settings)
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_client_rejects_non_basic_method(self) -> None:
        """Only basic auth is supported by the runtime client today."""
        settings = m.OracleWms.AuthSettings(
            method=_Method.OAUTH2,
            oauth2_client_id="id",
            oauth2_client_secret="secret",
        )
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(settings)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error.lower(), has="basic auth only")


__all__: list[str] = ["TestsFlextOracleWmsAuthentication"]
