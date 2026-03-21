"""Unit tests for FlextOracleWmsApi (wms_api module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import u

from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApi,
    FlextOracleWmsApiEndpoint,
)


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi class."""

    def test_api_catalog_exists(self) -> None:
        """Test that API catalog is properly defined."""
        u.Tests.Matchers.that(
            hasattr(FlextOracleWmsApi, "FLEXT_ORACLE_WMS_APIS"), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS, dict), eq=True
        )
        u.Tests.Matchers.that(len(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS) > 0, eq=True)

    def test_api_catalog_entries_are_endpoints(self) -> None:
        """Test that API catalog entries are FlextOracleWmsApiEndpoint instances."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
        for api_name, api_endpoint in apis.items():
            u.Tests.Matchers.that(
                isinstance(api_endpoint, FlextOracleWmsApiEndpoint), eq=True
            )
            u.Tests.Matchers.that(isinstance(api_name, str), eq=True)
            u.Tests.Matchers.that(len(api_name) > 0, eq=True)

    def test_test_endpoint_exists(self) -> None:
        """Test that the 'test' endpoint is defined in catalog."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
        u.Tests.Matchers.that("test" in apis, eq=True)

    def test_test_endpoint_properties(self) -> None:
        """Test properties of the test endpoint."""
        endpoint = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS["test"]
        u.Tests.Matchers.that(endpoint.name == "test", eq=True)
        u.Tests.Matchers.that(endpoint.method == "GET", eq=True)
        u.Tests.Matchers.that(endpoint.path == "/test/", eq=True)
        u.Tests.Matchers.that(endpoint.version == "v1", eq=True)
        u.Tests.Matchers.that(endpoint.category == "test", eq=True)
        u.Tests.Matchers.that(isinstance(endpoint.description, str), eq=True)
        u.Tests.Matchers.that(endpoint.since_version == "6.1", eq=True)

    def test_module_level_apis_alias(self) -> None:
        """Test module-level FLEXT_ORACLE_WMS_APIS alias."""
        u.Tests.Matchers.that(
            FLEXT_ORACLE_WMS_APIS is FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS, eq=True
        )

    def test_api_endpoint_model_fields(self) -> None:
        """Test FlextOracleWmsApiEndpoint Pydantic model fields."""
        ep = FlextOracleWmsApiEndpoint(
            name="custom",
            method="POST",
            path="/custom/",
            version="v2",
            category="inventory",
            description="Custom endpoint",
            since_version="7.0",
        )
        u.Tests.Matchers.that(ep.name == "custom", eq=True)
        u.Tests.Matchers.that(ep.method == "POST", eq=True)
        u.Tests.Matchers.that(ep.path == "/custom/", eq=True)
        u.Tests.Matchers.that(ep.version == "v2", eq=True)
        u.Tests.Matchers.that(ep.category == "inventory", eq=True)
        u.Tests.Matchers.that(ep.description == "Custom endpoint", eq=True)
        u.Tests.Matchers.that(ep.since_version == "7.0", eq=True)

    def test_api_endpoint_default_since_version(self) -> None:
        """Test FlextOracleWmsApiEndpoint default since_version."""
        ep = FlextOracleWmsApiEndpoint(
            name="x",
            method="GET",
            path="/x/",
            version="v1",
            category="test",
            description="Test",
        )
        u.Tests.Matchers.that(ep.since_version == "6.1", eq=True)

    def test_mock_server_inner_class_exists(self) -> None:
        """Test OracleWmsMockServer inner class exists."""
        u.Tests.Matchers.that(
            hasattr(FlextOracleWmsApi, "OracleWmsMockServer"), eq=True
        )

    def test_create_mock_server(self) -> None:
        """Test create_mock_server classmethod."""
        mock = FlextOracleWmsApi.create_mock_server()
        u.Tests.Matchers.that(
            isinstance(mock, FlextOracleWmsApi.OracleWmsMockServer), eq=True
        )


__all__ = ["TestFlextOracleWmsApi"]
