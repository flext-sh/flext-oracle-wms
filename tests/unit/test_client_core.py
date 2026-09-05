"""Behavioral unit tests for the Oracle WMS client public contract.

Exercises the observable behavior of ``u.OracleWms.Client``
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

from flext_oracle_wms import FlextOracleWmsSettings, m, u
from flext_tests import tm
from tests._factories import _oauth_secret_dashed, _wms_password_underscore


@pytest.mark.unit
class TestsFlextOracleWmsClientCore:
    """Public-contract behavior of the Oracle WMS utilities client."""

    def test_init_preserves_supplied_settings(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        client = u.OracleWms.Client(oracle_wms_settings)
        assert client.settings is oracle_wms_settings
        tm.that(
            client.settings.OracleWms.base_url,
            eq=oracle_wms_settings.OracleWms.base_url,
        )
        tm.that(
            client.settings.OracleWms.timeout,
            eq=oracle_wms_settings.OracleWms.timeout,
        )

    def test_init_without_settings_resolves_global_config(self) -> None:
        client = u.OracleWms.Client(None)
        tm.that(client.settings, is_=FlextOracleWmsSettings)

    def test_start_reports_success(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        result = u.OracleWms.Client(oracle_wms_settings).start()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_start_is_idempotent(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        client = u.OracleWms.Client(oracle_wms_settings)
        tm.that(client.start().unwrap(), eq=True)
        tm.that(client.start().unwrap(), eq=True)

    def test_stop_reports_success(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        client = u.OracleWms.Client(oracle_wms_settings)
        client.start()
        result = client.stop()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_stop_before_start_still_succeeds(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        result = u.OracleWms.Client(oracle_wms_settings).stop()
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_restart_after_stop_succeeds(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        client = u.OracleWms.Client(oracle_wms_settings)
        client.start()
        client.stop()
        tm.that(client.start().unwrap(), eq=True)

    def test_from_auth_settings_builds_client_for_basic_auth(self) -> None:
        auth = m.OracleWms.AuthSettings(
            method="basic", username="wms_user", password=_wms_password_underscore()
        )
        result = u.OracleWms.Client.from_auth_settings(auth)
        tm.ok(result)
        tm.that(result.unwrap(), is_=u.OracleWms.Client)

    def test_from_auth_settings_rejects_non_basic_auth(self) -> None:
        auth = m.OracleWms.AuthSettings(
            method="oauth2",
            oauth2_client_id="client-id",
            oauth2_client_secret=_oauth_secret_dashed(),
        )
        result = u.OracleWms.Client.from_auth_settings(auth)
        tm.fail(result)
        tm.that((result.error or ""), has="BASIC")

    def test_from_auth_settings_rejects_invalid_business_rules(self) -> None:
        auth = m.OracleWms.AuthSettings(method="basic", username=None, password=None)
        result = u.OracleWms.Client.from_auth_settings(auth)
        tm.fail(result)
        assert result.error


__all__: list[str] = ["TestsFlextOracleWmsClientCore"]
