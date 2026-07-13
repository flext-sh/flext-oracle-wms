"""Behavioral unit tests for FlextOracleWmsApi (api module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsUtilitiesClient, m
from tests import m as tm, t


class TestsFlextOracleWmsWmsApi:
    """Behavioral contract tests for the FlextOracleWmsApi public surface."""

    # ------------------------------------------------------------------
    # api_endpoints() published catalog contract
    # ------------------------------------------------------------------

    def test_api_endpoints_returns_typed_endpoint_mapping(self) -> None:
        """api_endpoints() publishes a non-empty name -> ApiEndpoint mapping."""
        endpoints = FlextOracleWmsApi.api_endpoints()

        assert endpoints, "expected a non-empty endpoint catalog"
        for name, endpoint in endpoints.items():
            assert isinstance(name, str)
            assert name
            assert isinstance(endpoint, tm.OracleWms.ApiEndpoint)
            assert endpoint.name == name

    def test_api_endpoints_publishes_documented_test_endpoint(self) -> None:
        """The catalog exposes the documented 'test' probe endpoint verbatim."""
        endpoint = FlextOracleWmsApi.api_endpoints()["test"]

        assert endpoint.model_dump() == {
            "name": "test",
            "method": "GET",
            "path": "/test/",
            "version": "v1",
            "category": "test",
            "description": endpoint.description,
            "since_version": "6.1",
        }
        assert isinstance(endpoint.description, str)

    def test_api_endpoints_returns_equivalent_snapshot_each_call(self) -> None:
        """Repeated calls yield equal catalogs (idempotent, no shared drift)."""
        first = FlextOracleWmsApi.api_endpoints()
        second = FlextOracleWmsApi.api_endpoints()

        assert first.keys() == second.keys()
        assert all(first[k].model_dump() == second[k].model_dump() for k in first)

    # ------------------------------------------------------------------
    # m.OracleWms.ApiEndpoint model contract
    # ------------------------------------------------------------------

    def test_api_endpoint_round_trips_supplied_fields(self) -> None:
        """An ApiEndpoint preserves every field it was constructed with."""
        endpoint = m.OracleWms.ApiEndpoint(
            name="custom",
            method="POST",
            path="/custom/",
            version="v2",
            category="inventory",
            description="Custom endpoint",
            since_version="7.0",
        )

        assert endpoint.model_dump() == {
            "name": "custom",
            "method": "POST",
            "path": "/custom/",
            "version": "v2",
            "category": "inventory",
            "description": "Custom endpoint",
            "since_version": "7.0",
        }

    def test_api_endpoint_applies_documented_defaults(self) -> None:
        """Description field defaults to '' and since_version to '6.1' baseline."""
        endpoint = m.OracleWms.ApiEndpoint(
            name="x",
            method="GET",
            path="/x/",
            version="v1",
            category="test",
        )

        assert endpoint.description == ""
        assert endpoint.since_version == "6.1"

    @pytest.mark.parametrize(
        "blank_field",
        ["name", "method", "path", "version", "category"],
    )
    def test_api_endpoint_rejects_blank_required_field(self, blank_field: str) -> None:
        """Each required identifier field must be non-empty (min_length=1)."""
        fields: t.MutableMappingKV[str, str] = {
            "name": "n",
            "method": "GET",
            "path": "/n/",
            "version": "v1",
            "category": "test",
        }
        fields[blank_field] = ""

        with pytest.raises(m.ValidationError):
            m.OracleWms.ApiEndpoint(**fields)

    # ------------------------------------------------------------------
    # create_oracle_wms_client() runtime client contract
    # ------------------------------------------------------------------

    def test_create_client_succeeds_for_basic_auth_with_credentials(self) -> None:
        """Valid BASIC credentials yield a success result carrying a Client."""
        result = FlextOracleWmsApi.create_oracle_wms_client(
            m.OracleWms.AuthSettings(username="test_user", password="test_password"),
        )

        assert result.success
        assert isinstance(result.unwrap(), FlextOracleWmsUtilitiesClient.Client)

    def test_create_client_fails_when_basic_credentials_incomplete(self) -> None:
        """BASIC auth without a password fails with the business-rule error."""
        result = FlextOracleWmsApi.create_oracle_wms_client(
            m.OracleWms.AuthSettings(username="only_user"),
        )

        assert result.failure
        assert result.error == "Basic auth requires username and password"

    def test_create_client_rejects_unsupported_oauth2_method(self) -> None:
        """A valid OAuth2 config is refused: runtime supports BASIC auth only."""
        result = FlextOracleWmsApi.create_oracle_wms_client(
            m.OracleWms.AuthSettings(
                method="oauth2",
                oauth2_client_id="client",
                oauth2_client_secret="secret",
            ),
        )

        assert result.failure
        assert result.error is not None
        assert "BASIC" in result.error

    # ------------------------------------------------------------------
    # execute() default readiness surface
    # ------------------------------------------------------------------

    def test_execute_signals_ready_with_success_true(self) -> None:
        """The default execute() surface reports readiness as ok(True)."""
        api = FlextOracleWmsApi()

        result = api.execute()

        assert result.success
        assert result.unwrap() is True


__all__: list[str] = []
