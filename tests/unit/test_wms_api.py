"""Unit tests for FlextOracleWmsApi class.

Tests the WMS API module following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms.wms_api import FlextOracleWmsApi


    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    FlextOracleWmsApiVersion,
)


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi class."""

    def test_api_catalog_exists(self) -> None:
        """Test that API catalog is properly defined."""
        assert hasattr(FlextOracleWmsApi, "FLEXT_ORACLE_WMS_APIS")
        assert isinstance(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS, dict)
        assert len(FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS) > 0

    def test_api_catalog_entries(self) -> None:
        """Test that API catalog entries have correct structure."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS

        # Check that all entries are FlextOracleWmsApiEndpoint instances
        for api_name, api_endpoint in apis.items():
            assert isinstance(api_endpoint, FlextOracleWmsApiEndpoint)
            assert isinstance(api_name, str)
            assert len(api_name) > 0

    def test_common_api_endpoints(self) -> None:
        """Test that common API endpoints are defined."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS

        # Test some known API endpoints
        assert "lgf_init_stage_interface" in apis
        assert "run_stage_interface" in apis
        assert "update_oblpn_tracking_number" in apis
        assert "get_status" in apis

    def test_api_endpoint_properties(self) -> None:
        """Test API endpoint properties."""
        apis = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS

        # Test a specific endpoint
        init_stage_api = apis["lgf_init_stage_interface"]
        assert init_stage_api.name == "lgf_init_stage_interface"
        assert init_stage_api.method == "POST"
        assert init_stage_api.version == FlextOracleWmsApiVersion.LGF_V10
        assert init_stage_api.category == FlextOracleWmsApiCategory.SETUP_TRANSACTIONAL
        assert "since_version" in init_stage_api.__dict__

    def test_mock_server_creation(self) -> None:
        """Test mock server creation."""
        mock_server = FlextOracleWmsApi.get_mock_server()
        assert mock_server is not None
        assert hasattr(mock_server, "environment")
        assert mock_server.environment == "mock_test"

    def test_mock_server_custom_environment(self) -> None:
        """Test mock server with custom environment."""
        mock_server = FlextOracleWmsApi.get_mock_server("production_mock")
        assert mock_server.environment == "production_mock"

    def test_mock_server_has_mock_data(self) -> None:
        """Test that mock server initializes with mock data."""
        mock_server = FlextOracleWmsApi.get_mock_server()

        # Check that mock data is initialized
        assert hasattr(mock_server, "mock_data")
        assert isinstance(mock_server.mock_data, dict)
        assert "entities" in mock_server.mock_data

    def test_mock_server_entities_list(self) -> None:
        """Test that mock server has expected entities."""
        mock_server = FlextOracleWmsApi.get_mock_server()

        entities = mock_server.mock_data["entities"]
        assert isinstance(entities, list)
        assert len(entities) > 0

        # Check for common WMS entities
        expected_entities = ["company", "facility", "item", "inventory", "location"]
        for entity in expected_entities:
            assert entity in entities

    def test_mock_server_company_data(self) -> None:
        """Test that mock server has company data."""
        mock_server = FlextOracleWmsApi.get_mock_server()

        assert "company_data" in mock_server.mock_data
        company_data = mock_server.mock_data["company_data"]
        assert isinstance(company_data, list)
        assert len(company_data) > 0

        # Check structure of first company record
        first_company = company_data[0]
        assert "company_code" in first_company
        assert "company_name" in first_company
        assert "status" in first_company

    def test_mock_server_methods_exist(self) -> None:
        """Test that mock server has expected methods."""
        mock_server = FlextOracleWmsApi.get_mock_server()

        # Test that key methods exist
        methods_to_check = [
            "get_entity_data",
            "get_entity_metadata",
            "get_apis_by_category",
            "call_api",
        ]

        for method in methods_to_check:
            assert hasattr(mock_server, method)
            assert callable(getattr(mock_server, method))


__all__ = ["TestFlextOracleWmsApi"]
