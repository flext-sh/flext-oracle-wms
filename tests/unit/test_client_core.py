"""Behavioral unit tests for the Oracle WMS client public contract.

Exercises the observable behavior of ``FlextOracleWmsUtilitiesClient.Client``
that does not require the external Oracle WMS service: settings resolution,
lifecycle (start/stop) idempotence, and ``from_auth_settings`` construction
rules. The request-based operations (health_check, call_api, discover_entities,
get_entity_data, get_apis_by_category) reach a live Oracle WMS Cloud endpoint;
there is no local container or self-contained service to exercise them against,
so per the no-mock law they are covered by real end-to-end runs against a
provisioned WMS environment, not by substituting the HTTP boundary here.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient, m
from flext_tests import tm


@pytest.mark.unit
class TestsFlextOracleWmsClientCore:
    """Public-contract behavior of the Oracle WMS utilities client."""

    def test_init_preserves_supplied_settings(
        self, mock_config: FlextOracleWmsSettings
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        assert client.settings is mock_config
        tm.that(client.settings.OracleWms.base_url, eq=mock_config.OracleWms.base_url)
        tm.that(client.settings.OracleWms.timeout, eq=mock_config.OracleWms.timeout)

    def test_init_without_settings_resolves_global_config(self) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(None)
        tm.that(client.settings, is_=FlextOracleWmsSettings)

    def test_start_reports_success(self, mock_config: FlextOracleWmsSettings) -> None:
        result = FlextOracleWmsUtilitiesClient.Client(mock_config).start()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_start_is_idempotent(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        tm.that(client.start().unwrap(), eq=True)
        tm.that(client.start().unwrap(), eq=True)

    def test_stop_reports_success(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client.start()
        result = client.stop()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_stop_before_start_still_succeeds(
        self, mock_config: FlextOracleWmsSettings
    ) -> None:
        result = FlextOracleWmsUtilitiesClient.Client(mock_config).stop()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_restart_after_stop_succeeds(
        self, mock_config: FlextOracleWmsSettings
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client.start()
        client.stop()
        tm.that(client.start().unwrap(), eq=True)

    def test_from_auth_settings_builds_client_for_basic_auth(self) -> None:
        auth = m.OracleWms.AuthSettings(
            method="basic", username="wms_user", password="wms_pass"
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


__all__: list[str] = ["TestsFlextOracleWmsClientCore"]
