"""Behavioral unit tests for the Oracle WMS client public contract.

Exercises the observable behavior of ``FlextOracleWmsUtilitiesClient.Client``:
settings resolution, lifecycle (start/stop) idempotence, ``from_auth_settings``
construction rules, and the ``r[T]`` outcomes of the request-based operations.

The only collaborator substituted is the genuine external HTTP boundary
(``FlextApi``), stubbed with ``Mock(spec=FlextApi)`` and returning real
``m.Api.HttpResponse`` models. The client exposes no public dependency-injection
seam for that transport, so the stub is installed on the ``_client`` slot; every
assertion targets public return values / ``r[T]`` state, never internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from unittest.mock import Mock

import pytest
from flext_api import FlextApi
from flext_tests import r, tm

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient, c, m
from tests import t


def _http_response(*, status_code: int, body: dict[str, object]) -> p.Api.HttpResponse:
    """Build a real HTTP response model as returned by the transport boundary."""
    return m.Api.HttpResponse.model_validate({
        "status_code": status_code,
        "headers": {},
        "body": body,
        "request_id": "test-request",
    })


def _client_with_response(
    settings: FlextOracleWmsSettings,
    response: m.Api.HttpResponse,
) -> t.OracleWms.Tests.Client:
    """Create a client whose external HTTP boundary yields ``response``."""
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    transport = Mock(spec=FlextApi)
    transport.request.return_value = r[p.Api.HttpResponse].ok(response)
    client._client = transport  # inject external boundary (no public DI seam)
    return client


def _client_with_transport_failure(
    settings: FlextOracleWmsSettings,
    error: str,
) -> t.OracleWms.Tests.Client:
    """Create a client whose external HTTP boundary fails every request."""
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    transport = Mock(spec=FlextApi)
    transport.request.return_value = r[p.Api.HttpResponse].fail(error)
    client._client = transport
    return client


@pytest.mark.unit
class TestsFlextOracleWmsClientCore:
    """Public-contract behavior of the Oracle WMS utilities client."""

    def test_init_preserves_supplied_settings(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        assert client.settings is mock_config
        tm.that(client.settings.OracleWms.base_url, eq=mock_config.OracleWms.base_url)
        tm.that(client.settings.OracleWms.timeout, eq=mock_config.OracleWms.timeout)

    def test_init_without_settings_resolves_global_config(self) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(None)
        tm.that(client.settings, is_=FlextOracleWmsSettings)

    def test_start_reports_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        result = FlextOracleWmsUtilitiesClient.Client(mock_config).start()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_start_is_idempotent(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        tm.that(client.start().unwrap(), eq=True)
        tm.that(client.start().unwrap(), eq=True)

    def test_stop_reports_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client.start()
        result = client.stop()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_stop_before_start_still_succeeds(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        result = FlextOracleWmsUtilitiesClient.Client(mock_config).stop()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_restart_after_stop_succeeds(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client.start()
        client.stop()
        tm.that(client.start().unwrap(), eq=True)

    def test_from_auth_settings_builds_client_for_basic_auth(self) -> None:
        auth = m.OracleWms.AuthSettings(
            method="basic",
            username="wms_user",
            password="wms_pass",
        )
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)
        tm.ok(result)
        tm.that(result.unwrap(), is_=FlextOracleWmsUtilitiesClient.Client)

    def test_from_auth_settings_rejects_non_basic_auth(self) -> None:
        auth = m.OracleWms.AuthSettings(
            method="oauth2",
            oauth2_client_id="client-id",
            oauth2_client_secret="client-secret",
        )
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)
        tm.fail(result)
        tm.that((result.error or ""), has="BASIC")

    def test_from_auth_settings_rejects_invalid_business_rules(self) -> None:
        auth = m.OracleWms.AuthSettings(method="basic", username=None, password=None)
        result = FlextOracleWmsUtilitiesClient.Client.from_auth_settings(auth)
        tm.fail(result)
        assert result.error

    def test_health_check_returns_ok_response(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(status_code=200, body={"status": "healthy"}),
        )
        result = client.health_check()
        tm.ok(result)
        tm.that(result.unwrap().status_code, eq=200)

    def test_call_api_returns_ok_response(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(status_code=200, body={"result": "ok"}),
        )
        result = client.call_api("allocation")
        tm.ok(result)
        tm.that(result.unwrap().body, eq={"result": "ok"})

    def test_discover_entities_returns_parsed_entity_names(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(
                status_code=200,
                body={"entities": ["company", "facility", "item"]},
            ),
        )
        result = client.discover_entities()
        tm.ok(result)
        tm.that(list(result.unwrap()), eq=["company", "facility", "item"])

    def test_get_entity_data_returns_parsed_rows(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(status_code=200, body={"data": [{"id": "1"}, {"id": "2"}]}),
        )
        result = client.get_entity_data("item", limit=10)
        tm.ok(result)
        tm.that(list(result.unwrap()), eq=[{"id": "1"}, {"id": "2"}])

    def test_get_apis_by_category_returns_parsed_apis(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(status_code=200, body={"apis": [{"name": "test_api"}]}),
        )
        result = client.get_apis_by_category("inventory")
        tm.ok(result)
        tm.that(list(result.unwrap()), eq=[{"name": "test_api"}])

    @pytest.mark.parametrize(
        "operation",
        [
            lambda client: client.health_check(),
            lambda client: client.call_api("allocation"),
            lambda client: client.discover_entities(),
            lambda client: client.get_entity_data("item"),
            lambda client: client.get_apis_by_category("inventory"),
        ],
    )
    def test_transport_failure_propagates_to_result(
        self,
        mock_config: FlextOracleWmsSettings,
        operation: Callable[[t.OracleWms.Tests.Client], r[object]],
    ) -> None:
        client = _client_with_transport_failure(mock_config, "Connection refused")
        result = operation(client)
        tm.fail(result)
        assert result.error

    @pytest.mark.parametrize("status_code", [400, 404, 500])
    def test_http_error_status_yields_failure(
        self,
        mock_config: FlextOracleWmsSettings,
        status_code: int,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(status_code=status_code, body={"error": "boom"}),
        )
        result = client.health_check()
        tm.fail(result)
        tm.that((result.error or ""), has=str(status_code))

    def test_status_below_threshold_is_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        below = c.OracleWms.HTTP_BAD_REQUEST_THRESHOLD - 1
        client = _client_with_response(
            mock_config,
            _http_response(status_code=below, body={"ok": True}),
        )
        tm.ok(client.health_check())

    def test_discover_entities_defaults_to_empty_on_absent_entities(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = _client_with_response(
            mock_config,
            _http_response(status_code=200, body={"unexpected": "shape"}),
        )
        result = client.discover_entities()
        tm.ok(result)
        tm.that(list(result.unwrap()), eq=[])


__all__: list[str] = ["TestsFlextOracleWmsClientCore"]
