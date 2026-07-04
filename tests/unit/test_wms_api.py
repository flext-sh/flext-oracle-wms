"""Unit tests for FlextOracleWmsApi (wms_api module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsApi
from flext_oracle_wms.utilities import FlextOracleWmsUtilitiesClient
from tests.models import m


class TestsFlextOracleWmsWmsApi:
    """Test cases for FlextOracleWmsApi class."""

    def test_api_catalog_exists(self) -> None:
        """Test that API catalog is properly defined."""
        assert isinstance(FlextOracleWmsApi.api_endpoints(), dict)
        assert FlextOracleWmsApi.api_endpoints()

    def test_api_catalog_entries_are_endpoints(self) -> None:
        """Test that API catalog entries are m.OracleWms.ApiEndpoint instances."""
        apis = FlextOracleWmsApi.api_endpoints()
        for api_name, api_endpoint in apis.items():
            assert isinstance(api_endpoint, m.OracleWms.ApiEndpoint)
            assert isinstance(api_name, str)
            assert api_name

    def test_test_endpoint_exists(self) -> None:
        """Test that the 'test' endpoint is defined in catalog."""
        apis = FlextOracleWmsApi.api_endpoints()
        assert "test" in apis

    def test_test_endpoint_properties(self) -> None:
        """Test properties of the test endpoint."""
        endpoint = FlextOracleWmsApi.api_endpoints()["test"]
        assert endpoint.name == "test"
        assert endpoint.method == "GET"
        assert endpoint.path == "/test/"
        assert endpoint.version == "v1"
        assert endpoint.category == "test"
        assert isinstance(endpoint.description, str)
        assert endpoint.since_version == "6.1"

    def test_class_level_apis(self) -> None:
        """Test class-level FLEXT_ORACLE_WMS_APIS."""
        assert FlextOracleWmsApi.api_endpoints()

    def test_api_endpoint_model_fields(self) -> None:
        """Test m.OracleWms.ApiEndpoint Pydantic model fields."""
        ep = m.OracleWms.ApiEndpoint(
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
        """Test m.OracleWms.ApiEndpoint default since_version."""
        ep = m.OracleWms.ApiEndpoint(
            name="x",
            method="GET",
            path="/x/",
            version="v1",
            category="test",
            description="Test",
        )
        assert ep.since_version == "6.1"

    def test_create_runtime_client(self) -> None:
        """Test runtime client creation from auth settings."""
        result = FlextOracleWmsApi.create_oracle_wms_client(
            m.OracleWms.AuthSettings(
                username="test_user",
                password="test_password",
            ),
        )
        assert result.success
        assert isinstance(result.value, FlextOracleWmsUtilitiesClient.Client)


__all__: list[str] = []
