"""Behavioral tests for the Oracle WMS runtime client.

Asserts the observable public contract: constructor settings resolution,
the ``r[bool]`` outcomes of the start/stop lifecycle, and the ``r[Client]``
outcomes of ``from_auth_settings`` across valid and invalid auth inputs.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient, m
from flext_tests import tm


class TestsFlextOracleWmsClient:
    """Public-contract tests for ``FlextOracleWmsUtilitiesClient.Client``."""

    @pytest.fixture
    def settings(self) -> FlextOracleWmsSettings:
        """Deterministic runtime settings for a BASIC-auth client."""
        return FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://test.wms.com",
                "username": "test_user",
                "password": "test_pass",
                "timeout": 30,
            }
        })

    # ---- constructor settings resolution -----------------------------------

    def test_constructor_honors_provided_settings(
        self, settings: FlextOracleWmsSettings
    ) -> None:
        """The client exposes exactly the settings object it was built with."""
        client = FlextOracleWmsUtilitiesClient.Client(settings)

        assert client.settings is settings
        tm.that(client.settings.OracleWms.base_url, eq="https://test.wms.com")
        tm.that(client.settings.OracleWms.username, eq="test_user")

    def test_constructor_preserves_custom_configuration_fields(self) -> None:
        """Custom configuration fields survive on the public settings state."""
        custom = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://custom.wms.com",
                "username": "custom_user",
                "password": "custom_pass",
                "timeout": 60,
                "retry_attempts": 5,
            }
        })

        client = FlextOracleWmsUtilitiesClient.Client(custom)

        tm.that(client.settings.OracleWms.timeout, eq=pytest.approx(60.0))
        tm.that(client.settings.OracleWms.retry_attempts, eq=5)
        tm.that(client.settings.OracleWms.base_url, eq="https://custom.wms.com")

    def test_constructor_without_settings_yields_valid_settings(self) -> None:
        """Omitting settings resolves the global runtime settings contract."""
        client = FlextOracleWmsUtilitiesClient.Client()

        tm.that(client.settings, is_=FlextOracleWmsSettings)
        assert client.settings.OracleWms.base_url

    # ---- start/stop lifecycle ----------------------------------------------

    def test_start_returns_success(self, settings: FlextOracleWmsSettings) -> None:
        """``start`` reports a successful ``r[bool]`` carrying ``True``."""
        client = FlextOracleWmsUtilitiesClient.Client(settings)

        result = client.start()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_stop_returns_success(self, settings: FlextOracleWmsSettings) -> None:
        """``stop`` reports a successful ``r[bool]`` carrying ``True``."""
        client = FlextOracleWmsUtilitiesClient.Client(settings)

        result = client.stop()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_start_stop_lifecycle_is_idempotent(
        self, settings: FlextOracleWmsSettings
    ) -> None:
        """Repeated start/stop cycles keep succeeding without error."""
        client = FlextOracleWmsUtilitiesClient.Client(settings)

        tm.ok(client.start())
        tm.ok(client.stop())
        tm.ok(client.start())
        tm.ok(client.stop())
        # A second stop with no live client still succeeds (idempotent release).
        tm.ok(client.stop())

    # ---- from_auth_settings contract ---------------------------------------

    def test_from_auth_settings_valid_basic_builds_client(self) -> None:
        """Valid BASIC auth settings produce a usable client honoring creds."""
        auth = m.OracleWms.AuthSettings(
            method="basic", username="alice", password="secret"
        )

        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)

        tm.ok(result)
        client = result.unwrap()
        tm.that(client, is_=FlextOracleWmsUtilitiesClient.Client)
        tm.that(client.settings.OracleWms.username, eq="alice")
        tm.that(client.settings.OracleWms.password, eq="secret")

    def test_from_auth_settings_basic_missing_credentials_fails(self) -> None:
        """BASIC auth without credentials fails business-rule validation."""
        auth = m.OracleWms.AuthSettings(method="basic")

        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="username and password")

    def test_from_auth_settings_oauth2_rejected_as_unsupported_runtime(self) -> None:
        """A validly-configured OAuth2 method is rejected: runtime is BASIC-only."""
        auth = m.OracleWms.AuthSettings(
            method="oauth2",
            oauth2_client_id="client-id",
            oauth2_client_secret="client-secret",
        )

        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="BASIC auth only")

    def test_from_auth_settings_unknown_method_fails(self) -> None:
        """An unsupported auth method fails validation before client creation."""
        auth = m.OracleWms.AuthSettings(
            method="kerberos", username="bob", password="pw"
        )

        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="Unsupported auth method")


__all__: list[str] = ["TestsFlextOracleWmsClient"]
