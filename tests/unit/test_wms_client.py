"""Behavioral unit tests for the Oracle WMS runtime client.

Exercises the PUBLIC contract of ``FlextOracleWmsUtilitiesClient.Client``:
return values, ``r[T]`` success/failure outcomes, error messages, HTTP
error propagation, entity/data extraction and lifecycle idempotence.

The only mocked seam is the genuine external boundary -- ``FlextApi.request``
(the network call). Everything else is driven through the public API with
real ``m.Api.HttpResponse`` models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_api import FlextApi
from flext_tests import tm

from flext_oracle_wms import (
    FlextOracleWmsSettings,
    FlextOracleWmsUtilitiesClient,
    m,
    p,
    r,
)
from tests import p, t


class TestsFlextOracleWmsWmsClient:
    """Behavioral contract tests for the Oracle WMS client."""

    @staticmethod
    def _response(
        status_code: int,
        body: t.Api.ResponseBody,
    ) -> p.Api.HttpResponse:
        """Build a real HTTP response model as the boundary would return."""
        return m.Api.HttpResponse.model_validate({
            "status_code": status_code,
            "body": body,
        })

    @classmethod
    def _stub_boundary(
        cls,
        monkeypatch: pytest.MonkeyPatch,
        outcome: p.Result[p.Api.HttpResponse],
    ) -> None:
        """Stub the external HTTP boundary FlextApi.request with an outcome."""

        def _request(
            _self: FlextApi,
            _request: p.Api.HttpRequest,
        ) -> p.Result[p.Api.HttpResponse]:
            return outcome

        monkeypatch.setattr(FlextApi, "request", _request)

    @classmethod
    def _stub_ok(
        cls,
        monkeypatch: pytest.MonkeyPatch,
        status_code: int,
        body: t.Api.ResponseBody,
    ) -> None:
        cls._stub_boundary(
            monkeypatch,
            r[p.Api.HttpResponse].ok(cls._response(status_code, body)),
        )

    @pytest.fixture
    def client(self) -> t.OracleWms.Tests.Client:
        """Return a client bound to the deterministic testing configuration."""
        return FlextOracleWmsUtilitiesClient.Client(
            FlextOracleWmsSettings.model_validate({
                "OracleWms": {
                    "base_url": "https://test-wms.example.com",
                    "timeout": 30.0,
                    "username": "test_user",
                    "password": "test_password",
                },
            }),
        )

    # -- construction contract ------------------------------------------

    def test_default_construction_exposes_settings_instance(self) -> None:
        client = FlextOracleWmsUtilitiesClient.Client()
        tm.that(client.settings, is_=FlextOracleWmsSettings)

    def test_explicit_settings_are_exposed_unchanged(self) -> None:
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://custom-wms.example.com",
                "timeout": 60,
            },
        })
        client = FlextOracleWmsUtilitiesClient.Client(settings=settings)
        assert client.settings is settings
        tm.that(client.settings.OracleWms.base_url, eq="https://custom-wms.example.com")
        tm.that(client.settings.OracleWms.timeout, eq=60)

    # -- verb methods return the response payload -----------------------

    def test_get_success_returns_response_body(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 200, {"data": "test"})
        result = client.get("/test-endpoint")
        tm.ok(result)
        tm.that(result.value.status_code, eq=200)
        tm.that(result.value.body, eq={"data": "test"})

    def test_get_boundary_failure_is_wrapped_with_context(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_boundary(
            monkeypatch,
            r[p.Api.HttpResponse].fail("Network error"),
        )
        result = client.get("/test-endpoint")
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="GET /test-endpoint failed")
        tm.that(result.error, has="Network error")

    @pytest.mark.parametrize("status_code", [400, 404, 500, 503])
    def test_http_error_status_becomes_failure(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
        status_code: int,
    ) -> None:
        self._stub_ok(monkeypatch, status_code, {"error": "boom"})
        result = client.get("/broken")
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has=f"HTTP {status_code}")

    @pytest.mark.parametrize(
        ("verb", "status_code", "body"),
        [
            ("post", 201, {"created": True}),
            ("put", 200, {"updated": True}),
            ("delete", 200, {"deleted": True}),
        ],
    )
    def test_write_verbs_return_response(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
        verb: str,
        status_code: int,
        body: t.Api.ResponseBody,
    ) -> None:
        self._stub_ok(monkeypatch, status_code, body)
        method = getattr(client, verb)
        result = method("/test-endpoint")
        tm.ok(result)
        tm.that(result.value.body, eq=body)

    def test_health_check_returns_health_payload(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 200, {"status": "healthy"})
        result = client.health_check()
        tm.ok(result)
        tm.that(result.value.body, eq={"status": "healthy"})

    def test_call_api_returns_response(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 200, {"result": "success"})
        result = client.call_api("test_api")
        tm.ok(result)
        tm.that(result.value.body, eq={"result": "success"})

    def test_update_oblpn_tracking_number_returns_response(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 200, {"updated": True})
        result = client.update_oblpn_tracking_number("oblpn123", "track456")
        tm.ok(result)
        tm.that(result.value.body, eq={"updated": True})

    def test_create_lpn_returns_response(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 201, {"created": True})
        result = client.create_lpn("lpn123", 5)
        tm.ok(result)
        tm.that(result.value.body, eq={"created": True})

    # -- discovery/extraction contract ----------------------------------

    def test_discover_entities_extracts_entity_names(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 200, {"entities": ["entity1", "entity2"]})
        result = client.discover_entities()
        tm.ok(result)
        tm.that(list(result.value), eq=["entity1", "entity2"])

    def test_discover_entities_propagates_boundary_failure(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_boundary(
            monkeypatch,
            r[p.Api.HttpResponse].fail("Network error"),
        )
        result = client.discover_entities()
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="GET /entities failed")

    def test_get_entity_data_extracts_data_rows(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(monkeypatch, 200, {"data": [{"id": "1"}, {"id": "2"}]})
        result = client.get_entity_data("test_entity", limit=10)
        tm.ok(result)
        tm.that(list(result.value), eq=[{"id": "1"}, {"id": "2"}])

    def test_get_apis_by_category_extracts_api_list(
        self,
        client: t.OracleWms.Tests.Client,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._stub_ok(
            monkeypatch,
            200,
            {"apis": [{"name": "api1"}, {"name": "api2"}]},
        )
        result = client.get_apis_by_category("inventory")
        tm.ok(result)
        tm.that([row["name"] for row in result.value], eq=["api1", "api2"])

    # -- lifecycle contract ---------------------------------------------

    def test_start_is_idempotent_and_reports_running(
        self,
        client: t.OracleWms.Tests.Client,
    ) -> None:
        first = client.start()
        second = client.start()
        tm.ok(first)
        tm.that(first.value, eq=True)
        tm.ok(second)
        tm.that(second.value, eq=True)

    def test_stop_is_idempotent_and_reports_stopped(
        self,
        client: t.OracleWms.Tests.Client,
    ) -> None:
        first = client.stop()
        second = client.stop()
        tm.ok(first)
        tm.that(first.value, eq=True)
        tm.ok(second)
        tm.that(second.value, eq=True)


__all__: list[str] = ["TestsFlextOracleWmsWmsClient"]
