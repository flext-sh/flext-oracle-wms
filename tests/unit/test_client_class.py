"""Behavioral contract tests for the Oracle WMS runtime client.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient, m

Client = FlextOracleWmsUtilitiesClient.Client

__all__: list[str] = ["TestsFlextOracleWmsClientClass"]


class TestsFlextOracleWmsClientClass:
    """Observable public behavior of FlextOracleWmsUtilitiesClient.Client."""

    @pytest.fixture
    def settings(self) -> FlextOracleWmsSettings:
        """Deterministic runtime settings for the client under test."""
        return FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://test-wms.example.com",
                "timeout": 30.0,
                "username": "test_user",
                "password": "test_password",
            },
        })

    def test_construction_exposes_supplied_settings(
        self,
        settings: FlextOracleWmsSettings,
    ) -> None:
        """Constructing with explicit settings surfaces them on the public field."""
        client = Client(settings)

        assert isinstance(client, Client)
        assert client.settings is settings
        assert client.settings.OracleWms.base_url == "https://test-wms.example.com"

    def test_construction_without_settings_resolves_defaults(self) -> None:
        """Constructing without settings yields a usable settings contract."""
        client = Client()

        assert isinstance(client.settings, FlextOracleWmsSettings)
        assert client.settings.OracleWms.base_url

    def test_start_reports_success(
        self,
        settings: FlextOracleWmsSettings,
    ) -> None:
        """start() returns a successful result carrying True."""
        result = Client(settings).start()

        assert result.success
        assert result.unwrap() is True

    def test_stop_reports_success(
        self,
        settings: FlextOracleWmsSettings,
    ) -> None:
        """stop() returns a successful result carrying True."""
        result = Client(settings).stop()

        assert result.success
        assert result.unwrap() is True

    def test_lifecycle_is_idempotent(
        self,
        settings: FlextOracleWmsSettings,
    ) -> None:
        """Repeated start/stop cycles keep reporting success."""
        client = Client(settings)

        for _ in range(2):
            assert client.start().success
            assert client.stop().success

    def test_from_auth_settings_rejects_basic_without_credentials(self) -> None:
        """BASIC auth missing username/password fails business-rule validation."""
        auth = m.OracleWms.AuthSettings(method="basic")

        result = Client.from_auth_settings(auth)

        assert result.failure
        assert "username and password" in (result.error or "")

    def test_from_auth_settings_rejects_non_basic_method(self) -> None:
        """A valid non-BASIC method is refused by the runtime client."""
        auth = m.OracleWms.AuthSettings(
            method="oauth2",
            oauth2_client_id="client-id",
            oauth2_client_secret="client-secret",
        )

        result = Client.from_auth_settings(auth)

        assert result.failure
        assert "BASIC" in (result.error or "")

    def test_from_auth_settings_builds_client_for_valid_basic(self) -> None:
        """Valid BASIC auth produces a client that adopts the supplied credentials."""
        auth = m.OracleWms.AuthSettings(
            method="basic",
            username="wms-user",
            password="wms-secret",
        )

        result = Client.from_auth_settings(auth)

        assert result.success
        built = result.unwrap()
        assert isinstance(built, Client)
        assert built.settings.OracleWms.username == "wms-user"
        assert built.settings.OracleWms.password == "wms-secret"

    @pytest.mark.parametrize(
        ("method", "expected_fragment"),
        [
            ("basic", "username and password"),
            ("api_key", "Unsupported auth method"),
            ("bearer", "Unsupported auth method"),
        ],
    )
    def test_from_auth_settings_failure_messages(
        self,
        method: str,
        expected_fragment: str,
    ) -> None:
        """Invalid auth configurations report a descriptive, method-specific error."""
        auth = m.OracleWms.AuthSettings(method=method)

        result = Client.from_auth_settings(auth)

        assert result.failure
        assert expected_fragment in (result.error or "")
