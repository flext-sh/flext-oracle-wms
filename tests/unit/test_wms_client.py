"""Unit tests for FlextOracleWmsClient class.

Tests the WMS client module against actual source API.
The client uses FlextApiClient internally via self._client.request(HttpRequest(...)).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

from flext_core import r
from flext_tests import u

from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.wms_client import FlextOracleWmsClient


class TestFlextOracleWmsClient:
    """Test cases for FlextOracleWmsClient class."""

    def test_initialization_without_config(self) -> None:
        """Test initialization without explicit configuration uses global/default."""
        client = FlextOracleWmsClient()
        u.Tests.Matchers.that(
            isinstance(client.config, FlextOracleWmsSettings), eq=True
        )
        u.Tests.Matchers.that(client._client is not None, eq=True)
        u.Tests.Matchers.that(client._discovered_entities == [], eq=True)

    def test_initialization_with_config(self) -> None:
        """Test initialization with explicit configuration."""
        config = FlextOracleWmsSettings(
            base_url="https://custom-wms.example.com", timeout=60
        )
        client = FlextOracleWmsClient(config=config)
        u.Tests.Matchers.that(client.config is config, eq=True)
        u.Tests.Matchers.that(
            client.config.base_url == "https://custom-wms.example.com", eq=True
        )
        u.Tests.Matchers.that(client.config.timeout == 60, eq=True)

    def test_get_method_success(self) -> None:
        """Test successful GET request via _client.request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": "test"}
        mock_response.body = {"data": "test"}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.get("/test-endpoint")
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"data": "test"}, eq=True)

    def test_get_method_failure(self) -> None:
        """Test failed GET request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        client._client = MagicMock()
        client._client.request.return_value = r.fail("Network error")
        result = client.get("/test-endpoint")
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_failure, eq=True)
        u.Tests.Matchers.that(result.error is not None, eq=True)
        u.Tests.Matchers.that("GET /test-endpoint failed" in result.error, eq=True)

    def test_post_method_success(self) -> None:
        """Test successful POST request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.body = {"created": True}
        mock_response.body = {"created": True}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.post("/test-endpoint", body={"key": "value"})
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"created": True}, eq=True)

    def test_put_method_success(self) -> None:
        """Test successful PUT request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"updated": True}
        mock_response.body = {"updated": True}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.put("/test-endpoint", body={"key": "value"})
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"updated": True}, eq=True)

    def test_delete_method_success(self) -> None:
        """Test successful DELETE request."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"deleted": True}
        mock_response.body = {"deleted": True}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.delete("/test-endpoint")
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"deleted": True}, eq=True)

    def test_health_check(self) -> None:
        """Test health check delegates to self.get('/health')."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"status": "healthy"}
        mock_response.body = {"status": "healthy"}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.health_check()
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"status": "healthy"}, eq=True)

    def test_start_method(self) -> None:
        """Test client start method returns ok(True)."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        result = client.start()
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value is True, eq=True)

    def test_stop_method(self) -> None:
        """Test client stop method returns ok(True)."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        result = client.stop()
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value is True, eq=True)

    def test_discover_entities_success(self) -> None:
        """Test entity discovery extracts 'entities' key from response."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"entities": ["entity1", "entity2"]}
        mock_response.body = {"entities": ["entity1", "entity2"]}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.discover_entities()
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == ["entity1", "entity2"], eq=True)

    def test_get_entity_data_success(self) -> None:
        """Test entity data retrieval extracts 'data' key from response."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": [{"id": 1}, {"id": 2}]}
        mock_response.body = {"data": [{"id": 1}, {"id": 2}]}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.get_entity_data("test_entity", limit=10)
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == [{"id": 1}, {"id": 2}], eq=True)

    def test_get_apis_by_category_success(self) -> None:
        """Test API discovery by category extracts 'apis' key."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"apis": [{"name": "api1"}, {"name": "api2"}]}
        mock_response.body = {"apis": [{"name": "api1"}, {"name": "api2"}]}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.get_apis_by_category("inventory")
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(len(result.value) == 2, eq=True)

    def test_call_api_success(self) -> None:
        """Test call_api delegates to self.get('/api/{api_name}')."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"result": "success"}
        mock_response.body = {"result": "success"}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.call_api("test_api")
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"result": "success"}, eq=True)

    def test_update_oblpn_tracking_number(self) -> None:
        """Test OBLPN tracking number update via PUT."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"updated": True}
        mock_response.body = {"updated": True}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.update_oblpn_tracking_number("oblpn123", "track456")
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"updated": True}, eq=True)

    def test_create_lpn(self) -> None:
        """Test LPN creation via POST."""
        config = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsClient(config)
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.body = {"created": True}
        mock_response.body = {"created": True}
        client._client = MagicMock()
        client._client.request.return_value = r.ok(mock_response)
        result = client.create_lpn("lpn123", 5)
        u.Tests.Matchers.that(isinstance(result, r), eq=True)
        u.Tests.Matchers.that(result.is_success, eq=True)
        u.Tests.Matchers.that(result.value == {"created": True}, eq=True)


__all__ = ["TestFlextOracleWmsClient"]
