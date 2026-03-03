"""Unit tests for FlextOracleWmsClient class.

Tests the WMS client module against actual source API.
The client uses FlextApiClient internally via self._client.request(HttpRequest(...)).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

from flext_core import FlextResult

from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.wms_client import FlextOracleWmsClient


class TestFlextOracleWmsClient:
    """Test cases for FlextOracleWmsClient class."""

    def test_initialization_without_config(self) -> None:
        """Test initialization without explicit configuration uses global/default."""
        client = FlextOracleWmsClient()

        assert isinstance(client.config, FlextOracleWmsSettings)
        assert client._client is not None
        assert client._discovered_entities == []

    def test_initialization_with_config(self) -> None:
        """Test initialization with explicit configuration."""
        config = FlextOracleWmsSettings(
            base_url="https://custom-wms.example.com",
            timeout=60,
        )

        client = FlextOracleWmsClient(config=config)

        assert client.config is config
        assert client.config.base_url == "https://custom-wms.example.com"
        assert client.config.timeout == 60

    def test_get_method_success(self) -> None:
        """Test successful GET request via _client.request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": "test"}
        mock_response.body = {"data": "test"}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.get("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"data": "test"}

    def test_get_method_failure(self) -> None:
        """Test failed GET request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        client._client = MagicMock()
        client._client.request.return_value = FlextResult.fail("Network error")

        result = client.get("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.is_failure
        assert result.error is not None
        assert "GET /test-endpoint failed" in result.error

    def test_post_method_success(self) -> None:
        """Test successful POST request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.body = {"created": True}
        mock_response.body = {"created": True}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.post("/test-endpoint", body={"key": "value"})

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"created": True}

    def test_put_method_success(self) -> None:
        """Test successful PUT request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"updated": True}
        mock_response.body = {"updated": True}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.put("/test-endpoint", body={"key": "value"})

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"updated": True}

    def test_delete_method_success(self) -> None:
        """Test successful DELETE request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"deleted": True}
        mock_response.body = {"deleted": True}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.delete("/test-endpoint")

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"deleted": True}

    def test_health_check(self) -> None:
        """Test health check delegates to self.get('/health')."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"status": "healthy"}
        mock_response.body = {"status": "healthy"}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.health_check()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"status": "healthy"}

    def test_start_method(self) -> None:
        """Test client start method returns ok(True)."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        result = client.start()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value is True

    def test_stop_method(self) -> None:
        """Test client stop method returns ok(True)."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        result = client.stop()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value is True

    def test_discover_entities_success(self) -> None:
        """Test entity discovery extracts 'entities' key from response."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"entities": ["entity1", "entity2"]}
        mock_response.body = {"entities": ["entity1", "entity2"]}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.discover_entities()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == ["entity1", "entity2"]

    def test_get_entity_data_success(self) -> None:
        """Test entity data retrieval extracts 'data' key from response."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": [{"id": 1}, {"id": 2}]}
        mock_response.body = {"data": [{"id": 1}, {"id": 2}]}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.get_entity_data("test_entity", limit=10)

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == [{"id": 1}, {"id": 2}]

    def test_get_apis_by_category_success(self) -> None:
        """Test API discovery by category extracts 'apis' key."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"apis": [{"name": "api1"}, {"name": "api2"}]}
        mock_response.body = {"apis": [{"name": "api1"}, {"name": "api2"}]}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.get_apis_by_category("inventory")

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert len(result.value) == 2

    def test_call_api_success(self) -> None:
        """Test call_api delegates to self.get('/api/{api_name}')."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"result": "success"}
        mock_response.body = {"result": "success"}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.call_api("test_api")

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"result": "success"}

    def test_update_oblpn_tracking_number(self) -> None:
        """Test OBLPN tracking number update via PUT."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"updated": True}
        mock_response.body = {"updated": True}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.update_oblpn_tracking_number("oblpn123", "track456")

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"updated": True}

    def test_create_lpn(self) -> None:
        """Test LPN creation via POST."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.body = {"created": True}
        mock_response.body = {"created": True}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.create_lpn("lpn123", 5)

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == {"created": True}


__all__ = ["TestFlextOracleWmsClient"]
