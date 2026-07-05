"""Behavioral contract tests for the Oracle WMS utilities client.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_core import FlextResult
from flext_oracle_wms import FlextOracleWmsSettings
from flext_oracle_wms.models import FlextOracleWmsModels as m
from flext_oracle_wms.utilities import FlextOracleWmsUtilitiesClient

__all__ = ["TestsFlextOracleWmsConnection"]

Client = FlextOracleWmsUtilitiesClient.Client


class TestsFlextOracleWmsConnection:
    """Public contract of the WMS utilities client and its settings."""

    @pytest.fixture
    def settings(self) -> FlextOracleWmsSettings:
        """Deterministic testing settings from the public factory."""
        return FlextOracleWmsSettings.testing_config()

    @pytest.fixture
    def client(self, settings: FlextOracleWmsSettings) -> Client:
        """Client built from the public constructor."""
        return Client(settings)

    @pytest.mark.parametrize(
        ("field", "expected"),
        [
            ("base_url", "https://test-wms.example.com"),
            ("username", "test_user"),
            ("password", "test_password"),
            ("timeout", 30.0),
            ("retry_attempts", 3),
            ("api_version", "LGF_V10"),
            ("auth_method", "basic"),
        ],
    )
    def test_testing_config_exposes_expected_field(
        self,
        settings: FlextOracleWmsSettings,
        field: str,
        expected: str | float,
    ) -> None:
        """testing_config publishes stable, documented field values."""
        assert settings.model_dump()[field] == expected

    def test_testing_config_is_deterministic(self) -> None:
        """Two independent factory calls yield equal public state."""
        first = FlextOracleWmsSettings.testing_config()
        second = FlextOracleWmsSettings.testing_config()
        assert first.model_dump() == second.model_dump()

    def test_client_publishes_its_settings(
        self,
        client: Client,
        settings: FlextOracleWmsSettings,
    ) -> None:
        """The client exposes exactly the settings it was built with."""
        assert client.settings is settings

    def test_from_auth_settings_builds_client(self) -> None:
        """from_auth_settings returns a ready client carrying the credentials."""
        auth = m.OracleWms.AuthSettings(
            method="basic",
            username="alice",
            password="secret",
        )
        result = Client.from_auth_settings(auth)
        assert result.success
        built = result.unwrap()
        assert built.settings.username == "alice"
        assert built.settings.password == "secret"

    def test_discover_entities_returns_result_on_unreachable_host(
        self,
        client: Client,
    ) -> None:
        """Network discovery surfaces failure as r[T], never raises."""
        result = client.discover_entities()
        assert isinstance(result, FlextResult)
        assert result.failure
        assert isinstance(result.error, str)
        assert result.error

    def test_get_apis_by_category_returns_result_on_unreachable_host(
        self,
        client: Client,
    ) -> None:
        """Category lookup returns a failing result rather than throwing."""
        result = client.get_apis_by_category("entity")
        assert isinstance(result, FlextResult)
        assert result.failure
        assert isinstance(result.error, str)
        assert result.error
