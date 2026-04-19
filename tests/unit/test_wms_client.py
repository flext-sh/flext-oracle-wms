"""Unit tests for FlextOracleWmsClient class.

Tests the WMS client module against actual source API.
The client uses FlextApiClient internally via self._client.request(HttpRequest(...)).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from flext_api import FlextApiClient

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient
from tests import r


class TestFlextOracleWmsClient:
    """Test cases for FlextOracleWmsClient class."""

    @staticmethod
    def _patch_request(
        monkeypatch: pytest.MonkeyPatch,
        result: object,
    ) -> None:
        def _request(
            _self: FlextApiClient,
            _http_request: object,
        ) -> object:
            return result

        monkeypatch.setattr(FlextApiClient, "request", _request)

    def test_initialization_without_config(self) -> None:
        """Test initialization without explicit configuration uses global/default."""
        client = FlextOracleWmsUtilitiesClient.Client()
        assert isinstance(client.settings, FlextOracleWmsSettings)

    def test_initialization_with_config(self) -> None:
        """Test initialization with explicit configuration."""
        settings = FlextOracleWmsSettings(
            base_url="https://custom-wms.example.com",
            timeout=60,
        )
        client = FlextOracleWmsUtilitiesClient.Client(settings=settings)
        assert client.settings is settings
        assert client.settings.base_url == "https://custom-wms.example.com"
        assert client.settings.timeout == 60

    def test_get_method_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test successful GET request via _client.request."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": "test"}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.get("/test-endpoint")
        assert result.success
        assert result.value.body == {"data": "test"}

    def test_get_method_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test failed GET request."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        self._patch_request(monkeypatch, r[MagicMock].fail("Network error"))
        result = client.get("/test-endpoint")
        assert result.failure
        assert result.error is not None
        assert "GET /test-endpoint failed" in str(result.error)

    def test_post_method_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test successful POST request."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.body = {"created": True}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.post("/test-endpoint", body={"key": "value"})
        assert result.success

    def test_put_method_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test successful PUT request."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"updated": True}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.put("/test-endpoint", body={"key": "value"})
        assert result.success

    def test_delete_method_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test successful DELETE request."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"deleted": True}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.delete("/test-endpoint")
        assert result.success

    def test_health_check(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test health check delegates to self.get('/health')."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"status": "healthy"}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.health_check()
        assert result.success

    def test_start_method(self) -> None:
        """Test client start method returns ok(True)."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        result = client.start()
        assert result.success
        assert result.value is True

    def test_stop_method(self) -> None:
        """Test client stop method returns ok(True)."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        result = client.stop()
        assert result.success
        assert result.value is True

    def test_discover_entities_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test entity discovery extracts 'entities' key from response."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"entities": ["entity1", "entity2"]}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.discover_entities()
        assert result.success
        assert result.value == ["entity1", "entity2"]

    def test_get_entity_data_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test entity data retrieval extracts 'data' key from response."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": [{"id": "1"}, {"id": "2"}]}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.get_entity_data("test_entity", limit=10)
        assert result.success
        assert result.value == [{"id": "1"}, {"id": "2"}]

    def test_get_apis_by_category_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test API discovery by category extracts 'apis' key."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"apis": [{"name": "api1"}, {"name": "api2"}]}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.get_apis_by_category("inventory")
        assert result.success
        assert len(result.value) == 2

    def test_call_api_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test call_api delegates to self.get('/api/{api_name}')."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"result": "success"}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.call_api("test_api")
        assert result.success

    def test_update_oblpn_tracking_number(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test OBLPN tracking number update via PUT."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"updated": True}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.update_oblpn_tracking_number("oblpn123", "track456")
        assert result.success

    def test_create_lpn(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test LPN creation via POST."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.body = {"created": True}
        self._patch_request(monkeypatch, r[MagicMock].ok(mock_response))
        result = client.create_lpn("lpn123", 5)
        assert result.success


__all__: list[str] = ["TestFlextOracleWmsClient"]
