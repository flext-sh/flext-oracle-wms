"""Public Oracle WMS client projection contracts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_oracle_wms import FlextOracleWmsApi, config, m
from flext_tests import tm

if TYPE_CHECKING:
    from flext_oracle_wms import FlextOracleWmsSettings, u


class TestsFlextOracleWmsWmsClient:
    """Observable client behavior exposed by the public API facade."""

    def test_http_client_projects_runtime_settings(
        self,
        oracle_wms_settings: FlextOracleWmsSettings,
        oracle_wms_http_client: u.OracleWms.HttpClient,
    ) -> None:
        """The public factory consumes the typed runtime settings owner."""
        runtime = oracle_wms_settings.OracleWms

        tm.that(oracle_wms_http_client.base_url, eq=runtime.base_url.rstrip("/"))
        tm.that(oracle_wms_http_client.timeout, eq=runtime.timeout)
        tm.that(oracle_wms_http_client.verify_ssl, eq=runtime.verify_ssl)

    def test_endpoint_catalog_projects_validated_config(self) -> None:
        """The public endpoint catalog is a typed projection of config."""
        endpoints = FlextOracleWmsApi.api_endpoints()
        configured = config.oracle_wms.api_endpoints

        tm.that(tuple(endpoints), eq=tuple(configured))
        for name, expected in configured.items():
            observed = endpoints[name]
            tm.that(observed, is_=m.OracleWms.ApiEndpoint)
            tm.that(observed.name, eq=expected.name)
            tm.that(observed.method, eq=expected.method)
            tm.that(observed.path, eq=expected.path)
            tm.that(observed.version, eq=expected.version)
            tm.that(observed.category, eq=expected.category)
            tm.that(observed.description, eq=expected.description)
            tm.that(observed.since_version, eq=expected.since_version)


__all__: list[str] = ["TestsFlextOracleWmsWmsClient"]
