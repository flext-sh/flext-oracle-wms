"""Behavioral unit tests for FlextOracleWmsApi (api.py facade).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsSettings,
    c,
    m,
    s,
    u,
)


class TestsFlextOracleWmsApi:
    """Behavioral contract tests for the FlextOracleWmsApi facade."""

    @pytest.fixture
    def api(self) -> FlextOracleWmsApi:
        """Return a facade built from explicit settings (no global lookup)."""
        return FlextOracleWmsApi(
            settings=FlextOracleWmsSettings(
                base_url="http://wms.example",
                username="user",
                password="secret",
            ),
        )

    def test_is_flext_service(self) -> None:
        """The facade honors the FlextService contract via subclassing."""
        assert issubclass(FlextOracleWmsApi, s)

    def test_execute_returns_ready_success(
        self,
        api: FlextOracleWmsApi,
    ) -> None:
        """execute() signals readiness as a successful r[bool] carrying True."""
        result = api.execute()

        assert result.success
        assert result.unwrap() is True

    def test_execute_is_idempotent(
        self,
        api: FlextOracleWmsApi,
    ) -> None:
        """Repeated execute() calls yield the same successful readiness value."""
        first = api.execute()
        second = api.execute()

        assert first.success
        assert second.success
        assert first.unwrap() == second.unwrap()

    def test_api_endpoints_keys_match_canonical_constants(self) -> None:
        """api_endpoints() exposes exactly the canonical endpoint names."""
        endpoints = FlextOracleWmsApi.api_endpoints()

        assert set(endpoints) == set(c.OracleWms.API_ENDPOINTS)

    def test_api_endpoints_returns_validated_models(self) -> None:
        """Each endpoint is an ApiEndpoint model whose name matches its key."""
        endpoints = FlextOracleWmsApi.api_endpoints()

        for name, endpoint in endpoints.items():
            assert isinstance(endpoint, m.OracleWms.ApiEndpoint)
            assert endpoint.name == name
            assert endpoint.path
            assert endpoint.method

    @pytest.mark.parametrize(
        ("base_url", "timeout", "verify_ssl"),
        [
            ("http://wms.example", 30.0, True),
            ("https://secure.wms", 5.5, False),
        ],
    )
    def test_create_flext_http_client_honors_arguments(
        self,
        base_url: str,
        timeout: float,
        *,
        verify_ssl: bool,
    ) -> None:
        """create_flext_http_client builds a client reflecting given config."""
        client = FlextOracleWmsApi.create_flext_http_client(
            base_url,
            timeout=timeout,
            verify_ssl=verify_ssl,
        )

        assert isinstance(client, u.OracleWms.HttpClient)
        assert client.base_url == base_url
        assert client.timeout == timeout

    def test_create_oracle_wms_client_succeeds_from_auth_settings(self) -> None:
        """create_oracle_wms_client returns a successful client result."""
        auth = m.OracleWms.AuthSettings(username="user", password="secret")

        result = FlextOracleWmsApi.create_oracle_wms_client(auth)

        assert result.success
        assert isinstance(result.unwrap(), u.OracleWms.Client)


__all__: list[str] = ["TestsFlextOracleWmsApi"]
