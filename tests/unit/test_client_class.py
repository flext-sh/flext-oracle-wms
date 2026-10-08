"""Behavioral contract tests for the Oracle WMS runtime client.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_oracle_wms import FlextOracleWmsSettings, m, u
from tests._factories import _oauth_secret_dashed, _wms_password

# Why: mro-4p0t — public facade access is u.OracleWms.Client, not the private
# _utilities.client module (flext-oracle-wms-1sm3w sync fix).
Client = u.OracleWms.Client


class TestsFlextOracleWmsClientClass:
    """Observable public behavior of u.OracleWms.Client."""

    @staticmethod
    def test_construction_exposes_supplied_settings(
        settings: FlextOracleWmsSettings,
    ) -> None:
        """Constructing with explicit settings surfaces them on the public field."""
        client = Client(settings)

        tm.that(client, is_=Client)
        assert client.settings is settings
        tm.that(client.settings.OracleWms.base_url, eq="https://test-wms.example.com")

    @staticmethod
    def test_construction_without_settings_resolves_defaults() -> None:
        """Constructing without settings yields a usable settings contract."""
        client = Client()

        tm.that(client.settings, is_=FlextOracleWmsSettings)
        assert client.settings.OracleWms.base_url

    @staticmethod
    def test_start_reports_success(settings: FlextOracleWmsSettings) -> None:
        """start() returns a successful result carrying True."""
        result = Client(settings).start()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    @staticmethod
    def test_stop_reports_success(settings: FlextOracleWmsSettings) -> None:
        """stop() returns a successful result carrying True."""
        result = Client(settings).stop()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    @staticmethod
    def test_lifecycle_is_idempotent(settings: FlextOracleWmsSettings) -> None:
        """Repeated start/stop cycles keep reporting success."""
        client = Client(settings)

        for _ in range(2):
            tm.ok(client.start())
            tm.ok(client.stop())

    @staticmethod
    def test_from_auth_settings_rejects_basic_without_credentials() -> None:
        """BASIC auth missing username/password fails business-rule validation."""
        auth = m.OracleWms.AuthSettings(method="basic")

        result = Client.from_auth_settings(auth)

        tm.fail(result)
        tm.that((result.error or ""), has="username and password")

    @staticmethod
    def test_from_auth_settings_rejects_non_basic_method() -> None:
        """A valid non-BASIC method is refused by the runtime client."""
        auth = m.OracleWms.AuthSettings(
            method="oauth2",
            oauth2_client_id="client-id",
            oauth2_client_secret=_oauth_secret_dashed(),
        )

        result = Client.from_auth_settings(auth)

        tm.fail(result)
        tm.that((result.error or ""), has="BASIC")

    @staticmethod
    def test_from_auth_settings_builds_client_for_valid_basic() -> None:
        """Valid BASIC auth produces a client that adopts the supplied credentials."""
        auth = m.OracleWms.AuthSettings(
            method="basic",
            username="wms-user",
            password=_wms_password(),
        )

        result = Client.from_auth_settings(auth)

        tm.ok(result)
        built = result.unwrap()
        tm.that(built, is_=Client)
        tm.that(built.settings.OracleWms.username, eq="wms-user")
        tm.that(built.settings.OracleWms.password, eq="wms-secret")

    @staticmethod
    @pytest.mark.parametrize(
        ("method", "expected_fragment"),
        [
            ("basic", "username and password"),
            ("api_key", "Unsupported auth method"),
            ("bearer", "Unsupported auth method"),
        ],
    )
    def test_from_auth_settings_failure_messages(
        method: str,
        expected_fragment: str,
    ) -> None:
        """Invalid auth configurations report a descriptive, method-specific error."""
        auth = m.OracleWms.AuthSettings(method=method)

        result = Client.from_auth_settings(auth)

        tm.fail(result)
        tm.that((result.error or ""), has=expected_fragment)
