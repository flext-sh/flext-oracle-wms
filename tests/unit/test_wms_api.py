"""Unit tests for FlextOracleWmsApi (wms_api module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApi,
    FlextOracleWmsApiEndpoint,
)


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi class."""

    def test_api_catalog_exists(self) -> None:
        """Test that API catalog is properly defined."""
        assert hasattr(FlextOracleWmsApi, "FLEXT_ORACLE_WMS_APIS")
        assert isinstance(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS, dict)
        assert len(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS) > 0

    def test_api_catalog_entries_are_endpoints(self) -> None:
        """Test that API catalog entries are FlextOracleWmsApiEndpoint instances."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
        for api_name, api_endpoint in apis.items():
            assert isinstance(api_endpoint, FlextOracleWmsApiEndpoint)
            assert isinstance(api_name, str)
            assert len(api_name) > 0

    def test_test_endpoint_exists(self) -> None:
        """Test that the 'test' endpoint is defined in catalog."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
        assert "test" in apis

    def test_test_endpoint_properties(self) -> None:
        """Test properties of the test endpoint."""
        endpoint = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS["test"]
        assert endpoint.name == "test"
        assert endpoint.method == "GET"
        assert endpoint.path == "/test/"
        assert endpoint.version == "v1"
        assert endpoint.category == "test"
        assert isinstance(endpoint.description, str)
        assert endpoint.since_version == "6.1"

    def test_module_level_apis_alias(self) -> None:
        """Test module-level FLEXT_ORACLE_WMS_APIS alias."""
        assert FLEXT_ORACLE_WMS_APIS is FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS

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
        assert ep.name == "custom"
        assert ep.method == "POST"
        assert ep.path == "/custom/"
        assert ep.version == "v2"
        assert ep.category == "inventory"
        assert ep.description == "Custom endpoint"
        assert ep.since_version == "7.0"

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
        assert ep.since_version == "6.1"

    def test_mock_server_inner_class_exists(self) -> None:
        """Test OracleWmsMockServer inner class exists."""
        assert hasattr(FlextOracleWmsApi, "OracleWmsMockServer")

    def test_create_mock_server(self) -> None:
        """Test create_mock_server classmethod."""
        mock = FlextOracleWmsApi.create_mock_server()
        assert isinstance(mock, FlextOracleWmsApi.OracleWmsMockServer)


__all__ = ["TestFlextOracleWmsApi"]
