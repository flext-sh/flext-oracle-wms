"""Behavioral unit tests for FlextOracleWmsApi (api.py facade).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsSettings, m, s, u
from tests import _secret, c, tm


class TestsFlextOracleWmsApi:
    """Behavioral contract tests for the FlextOracleWmsApi facade."""

    @pytest.fixture
    @staticmethod
    def api() -> FlextOracleWmsApi:
        """Return a facade built from explicit settings (no global lookup)."""
        return FlextOracleWmsApi(
            settings=FlextOracleWmsSettings.model_validate({
                "OracleWms": {
                    "base_url": "http://wms.example",
                    "username": c.ContextScope.USER,
                    "password": _secret(),
                },
            }),
        )

    @staticmethod
    def test_is_flext_service() -> None:
        """The facade honors the FlextService contract via subclassing."""
        tm.that(issubclass(FlextOracleWmsApi, s), truth=True)

    @staticmethod
    def test_execute_returns_ready_success(api: FlextOracleWmsApi) -> None:
        """execute() signals readiness as a successful r[bool] carrying True."""
        result = api.execute()

        tm.ok(result)
        tm.ok(result.unwrap())

    @staticmethod
    def test_execute_is_idempotent(api: FlextOracleWmsApi) -> None:
        """Repeated execute() calls yield the same successful readiness value."""
        first = api.execute()
        second = api.execute()

        tm.ok(first)
        tm.ok(second)
        tm.that(first.unwrap(), eq=second.unwrap())

    @staticmethod
    def test_api_endpoints_keys_match_canonical_constants() -> None:
        """api_endpoints() exposes exactly the canonical endpoint names."""
        endpoints = FlextOracleWmsApi.api_endpoints()

        tm.that(set(endpoints), eq=set(c.OracleWms.API_ENDPOINTS))

    @staticmethod
    def test_api_endpoints_returns_validated_models() -> None:
        """Each endpoint is an ApiEndpoint model whose name matches its key."""
        endpoints = FlextOracleWmsApi.api_endpoints()

        for name, endpoint in endpoints.items():
            tm.that(endpoint, is_=m.OracleWms.ApiEndpoint)
            tm.that(endpoint.name, eq=name)
            tm.that(endpoint.path, truth=True)
            tm.that(endpoint.method, truth=True)

    @staticmethod
    @pytest.mark.parametrize(
        ("base_url", "timeout", "verify_ssl"),
        [("http://wms.example", 30.0, True), ("https://secure.wms", 5.5, False)],
    )
    def test_create_flext_http_client_honors_arguments(
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

        tm.that(client, is_=u.OracleWms.HttpClient)
        tm.that(client.base_url, eq=base_url)
        tm.that(client.timeout, eq=timeout)

    @staticmethod
    def test_create_oracle_wms_client_succeeds_from_auth_settings() -> None:
        """create_oracle_wms_client returns a successful client result."""
        auth = m.OracleWms.AuthSettings(
            username=c.ContextScope.USER, password=_secret()
        )

        result = FlextOracleWmsApi.create_oracle_wms_client(auth)

        tm.ok(result)
        tm.that(result.unwrap(), is_=u.OracleWms.Client)
