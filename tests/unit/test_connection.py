"""Behavioral contract tests for the Oracle WMS utilities client.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_core import r
from flext_oracle_wms import FlextOracleWmsModels as m, FlextOracleWmsSettings, u
from tests._factories import _basic_password, _secret


# Why: mro-4p0t — public facade access is u.OracleWms.Client, not the private
# _utilities.client module (flext-oracle-wms-1sm3w sync fix).
Client = u.OracleWms.Client


class TestsFlextOracleWmsConnection:
    """Public contract of the WMS utilities client and its settings."""

    @staticmethod
    @pytest.fixture
    def settings() -> FlextOracleWmsSettings:
        """Deterministic testing settings from the public factory.

        Returns:
            The resulting ``FlextOracleWmsSettings``.
        """
        return FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://test-wms.example.com",
                "timeout": 30.0,
                "username": "test_user",
                "password": _basic_password(),
            },
        })

    @staticmethod
    @pytest.fixture
    def client(settings: FlextOracleWmsSettings) -> Client:
        """Client built from the public constructor.

        Returns:
            The resulting ``Client``.
        """
        return Client(settings)

    @staticmethod
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
        settings: FlextOracleWmsSettings,
        field: str,
        expected: str | float,
    ) -> None:
        """Deterministic settings publish stable, documented field values."""
        tm.that(settings.model_dump()["OracleWms"][field], eq=expected)

    @staticmethod
    def test_testing_config_is_deterministic() -> None:
        """Two independent factory calls yield equal public state."""
        first = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"base_url": "https://test-wms.example.com"},
        })
        second = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"base_url": "https://test-wms.example.com"},
        })
        tm.that(first.model_dump(), eq=second.model_dump())

    @staticmethod
    def test_client_publishes_its_settings(
        client: Client,
        settings: FlextOracleWmsSettings,
    ) -> None:
        """The client exposes exactly the settings it was built with."""
        assert client.settings is settings

    @staticmethod
    def test_from_auth_settings_builds_client() -> None:
        """from_auth_settings returns a ready client carrying the credentials."""
        auth = m.OracleWms.AuthSettings(
            method="basic",
            username="alice",
            password=_secret(),
        )
        result = Client.from_auth_settings(auth)
        tm.ok(result)
        built = result.unwrap()
        tm.that(built.settings.OracleWms.username, eq="alice")
        tm.that(built.settings.OracleWms.password, eq="secret")

    @staticmethod
    def test_discover_entities_returns_result_on_unreachable_host(
        client: Client,
    ) -> None:
        """Network discovery surfaces failure as r[T], never raises."""
        result = client.discover_entities()
        tm.that(result, is_=r)
        tm.fail(result)
        tm.that(result.error, is_=str)
        assert result.error

    @staticmethod
    def test_get_apis_by_category_returns_result_on_unreachable_host(
        client: Client,
    ) -> None:
        """Category lookup returns a failing result rather than throwing."""
        result = client.get_apis_by_category("entity")
        tm.that(result, is_=r)
        tm.fail(result)
        tm.that(result.error, is_=str)
        assert result.error
