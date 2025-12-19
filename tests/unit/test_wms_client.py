"""Unit tests for FlextOracleWmsClient class.

Tests the WMS client module following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from flext_core import FlextResult

from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.wms_client import FlextOracleWmsClient


class TestFlextOracleWmsClient:
    """Test cases for FlextOracleWmsClient class."""

    def test_initialization_without_config(self) -> None:
        """Test initialization without explicit configuration."""
        with patch("flext_oracle_wms.wms_client.FlextApiClient") as mock_api_client:
            client = FlextOracleWmsClient()

            # Should create default config
            assert isinstance(client.config, FlextOracleWmsSettings)

            # Should initialize API client with correct parameters
            mock_api_client.assert_called_once_with(
                base_url="https://wms.oraclecloud.com",
                timeout=30,
            )

    def test_initialization_with_config(self) -> None:
        """Test initialization with explicit configuration."""
        config = FlextOracleWmsSettings(
            base_url="https://custom-wms.example.com",
            timeout=60,
        )

        with patch("flext_oracle_wms.wms_client.FlextApiClient") as mock_api_client:
            client = FlextOracleWmsClient(config=config)

            assert client.config is config

            # Should initialize API client with config parameters
            mock_api_client.assert_called_once_with(
                base_url="https://custom-wms.example.com",
                timeout=60,
            )

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_get_method_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful GET request."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.return_value = {"data": "test"}

        client = FlextOracleWmsClient()
        result = client.get("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"data": "test"}
        mock_api_client.get.assert_called_once_with("/test-endpoint")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_get_method_failure(self, mock_api_client_class: MagicMock) -> None:
        """Test failed GET request."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.side_effect = Exception("Network error")

        client = FlextOracleWmsClient()
        result = client.get("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert not result.success
        assert "GET /test-endpoint failed: Network error" in result.error

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_post_method_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful POST request."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.post.return_value = {"created": True}

        client = FlextOracleWmsClient()
        result = client.post("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"created": True}
        mock_api_client.post.assert_called_once_with("/test-endpoint")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_put_method_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful PUT request."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.put.return_value = {"updated": True}

        client = FlextOracleWmsClient()
        result = client.put("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"updated": True}
        mock_api_client.put.assert_called_once_with("/test-endpoint")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_delete_method_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful DELETE request."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.delete.return_value = {"deleted": True}

        client = FlextOracleWmsClient()
        result = client.delete("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"deleted": True}
        mock_api_client.delete.assert_called_once_with("/test-endpoint")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_health_check(self, mock_api_client_class: MagicMock) -> None:
        """Test health check endpoint."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.return_value = {"status": "healthy"}

        client = FlextOracleWmsClient()
        result = client.health_check()

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"status": "healthy"}
        mock_api_client.get.assert_called_once_with("/health")

    def test_start_method(self) -> None:
        """Test client start method."""
        with patch("flext_oracle_wms.wms_client.FlextApiClient"):
            client = FlextOracleWmsClient()
            result = client.start()

            assert isinstance(result, FlextResult)
            assert result.success
            assert result.value is True

    def test_stop_method(self) -> None:
        """Test client stop method."""
        with patch("flext_oracle_wms.wms_client.FlextApiClient"):
            client = FlextOracleWmsClient()
            result = client.stop()

            assert isinstance(result, FlextResult)
            assert result.success
            assert result.value is True

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_discover_entities_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful entity discovery."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.return_value = {"entities": ["entity1", "entity2"]}

        client = FlextOracleWmsClient()
        result = client.discover_entities()

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == ["entity1", "entity2"]
        mock_api_client.get.assert_called_once_with("/entities")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_get_entity_data_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful entity data retrieval."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.return_value = {"data": ["item1", "item2"]}

        client = FlextOracleWmsClient()
        result = client.get_entity_data("test_entity", limit=10)

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == ["item1", "item2"]
        mock_api_client.get.assert_called_once_with(
            "/entities/test_entity",
            limit=10,
        )

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_get_apis_by_category_success(
        self,
        mock_api_client_class: MagicMock,
    ) -> None:
        """Test successful API discovery by category."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.return_value = {"apis": ["api1", "api2"]}

        client = FlextOracleWmsClient()
        result = client.get_apis_by_category("inventory")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == ["api1", "api2"]
        mock_api_client.get.assert_called_once_with("/apis/category/inventory")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_call_api_success(self, mock_api_client_class: MagicMock) -> None:
        """Test successful API call."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.get.return_value = {"result": "success"}

        client = FlextOracleWmsClient()
        result = client.call_api("test_api", param="value")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"result": "success"}
        mock_api_client.get.assert_called_once_with("/api/test_api", param="value")

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_update_oblpn_tracking_number(
        self,
        mock_api_client_class: MagicMock,
    ) -> None:
        """Test OBLPN tracking number update."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.put.return_value = {"updated": True}

        client = FlextOracleWmsClient()
        result = client.update_oblpn_tracking_number("oblpn123", "track456")

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"updated": True}
        mock_api_client.put.assert_called_once_with(
            "/oblpn/oblpn123/tracking",
            json={"tracking_number": "track456"},
        )

    @patch("flext_oracle_wms.wms_client.FlextApiClient")
    def test_create_lpn(self, mock_api_client_class: MagicMock) -> None:
        """Test LPN creation."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value = mock_api_client
        mock_api_client.post.return_value = {"created": True}

        client = FlextOracleWmsClient()
        result = client.create_lpn("lpn123", 5)

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value == {"created": True}
        mock_api_client.post.assert_called_once_with(
            "/lpn",
            json={"lpn_nbr": "lpn123", "qty": 5},
        )


__all__ = ["TestFlextOracleWmsClient"]
