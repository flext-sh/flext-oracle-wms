"""Unit tests for FlextOracleWmsApi (wms_api module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApi,
    FlextOracleWmsApiEndpoint,
)


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi class."""

    def test_api_catalog_exists(self) -> None:
        """Test that API catalog is properly defined."""
        tm.that(hasattr(FlextOracleWmsApi, "FLEXT_ORACLE_WMS_APIS"), eq=True)
        tm.that(isinstance(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS, dict), eq=True)
        tm.that(len(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS) > 0, eq=True)

    def test_api_catalog_entries_are_endpoints(self) -> None:
        """Test that API catalog entries are FlextOracleWmsApiEndpoint instances."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
        for api_name, api_endpoint in apis.items():
            tm.that(isinstance(api_endpoint, FlextOracleWmsApiEndpoint), eq=True)
            tm.that(isinstance(api_name, str), eq=True)
            tm.that(len(api_name) > 0, eq=True)

    def test_test_endpoint_exists(self) -> None:
        """Test that the 'test' endpoint is defined in catalog."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
        tm.that("test" in apis, eq=True)

    def test_test_endpoint_properties(self) -> None:
        """Test properties of the test endpoint."""
        endpoint = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS["test"]
        tm.that(endpoint.name == "test", eq=True)
        tm.that(endpoint.method == "GET", eq=True)
        tm.that(endpoint.path == "/test/", eq=True)
        tm.that(endpoint.version == "v1", eq=True)
        tm.that(endpoint.category == "test", eq=True)
        tm.that(isinstance(endpoint.description, str), eq=True)
        tm.that(endpoint.since_version == "6.1", eq=True)

    def test_module_level_apis_alias(self) -> None:
        """Test module-level FLEXT_ORACLE_WMS_APIS alias."""
        tm.that(
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
        tm.that(ep.name == "custom", eq=True)
        tm.that(ep.method == "POST", eq=True)
        tm.that(ep.path == "/custom/", eq=True)
        tm.that(ep.version == "v2", eq=True)
        tm.that(ep.category == "inventory", eq=True)
        tm.that(ep.description == "Custom endpoint", eq=True)
        tm.that(ep.since_version == "7.0", eq=True)

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
        tm.that(ep.since_version == "6.1", eq=True)

    def test_mock_server_inner_class_exists(self) -> None:
        """Test OracleWmsMockServer inner class exists."""
        tm.that(hasattr(FlextOracleWmsApi, "OracleWmsMockServer"), eq=True)

    def test_create_mock_server(self) -> None:
        """Test create_mock_server classmethod."""
        mock = FlextOracleWmsApi.create_mock_server()
        tm.that(isinstance(mock, FlextOracleWmsApi.OracleWmsMockServer), eq=True)


__all__ = ["TestFlextOracleWmsApi"]
