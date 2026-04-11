"""Unit tests for FlextOracleWmsClient -- core functionality coverage.

Tests against actual wms_client.py source API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from flext_core import r
from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient
from tests import u


@pytest.mark.unit
class TestFlextOracleWmsClientCore:
    """Core client functionality tests."""

    def test_client_initialization(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        assert client.config == mock_config
        assert client.config.base_url == mock_config.base_url
        assert client._client is not None

    def test_client_string_representation(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        repr_str = repr(client)
        str_str = str(client)
        assert "FlextOracleWmsClient" in repr_str or "Client" in repr_str
        assert isinstance(str_str, str)

    def test_client_config_properties(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        assert client.config.base_url == mock_config.base_url
        assert client.config.timeout == mock_config.timeout

    def test_client_start_success(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        result = client.start()
        assert result.success
        assert result.value is True

    def test_client_start_multiple_times(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        result1 = client.start()
        assert result1.success
        result2 = client.start()
        assert result2.success

    def test_client_stop_success(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client.start()
        result = client.stop()
        assert result.success
        assert result.value is True

    def test_client_stop_not_started(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        result = client.stop()
        assert result.success

    def test_client_has_expected_methods(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        assert callable(client.start)
        assert callable(client.stop)

    def test_get_apis_by_category(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"apis": [{"name": "test_api"}]}
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].ok(mock_response)
        result = client.get_apis_by_category("inventory")
        assert result.success

    def test_health_check_delegates_to_get(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"status": "healthy"}
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].ok(mock_response)
        result = client.health_check()
        assert result.success

    def test_discover_entities_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"entities": ["company", "facility", "item"]}
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].ok(mock_response)
        result = client.discover_entities()
        assert result.success
        assert isinstance(result.value, list)
        assert len(result.value) == 3

    def test_discover_entities_failure(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].fail("Connection refused")
        result = client.discover_entities()
        assert result.failure

    def test_get_entity_data_success(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"data": [{"id": "1"}, {"id": "2"}]}
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].ok(mock_response)
        result = client.get_entity_data("test_entity", limit=10)
        assert result.success
        assert result.value == [{"id": "1"}, {"id": "2"}]

    def test_get_entity_data_failure(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].fail("Not found")
        result = client.get_entity_data("test_entity")
        assert result.failure

    def test_call_api_success(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.body = {"result": "ok"}
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].ok(mock_response)
        result = client.call_api("test_api")
        assert result.success

    def test_call_api_failure(self, mock_config: FlextOracleWmsSettings) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(mock_config)
        client._client = MagicMock()
        client._client.request.return_value = r[MagicMock].fail("API error")
        result = client.call_api("test_api")
        assert result.failure

    def test_client_error_handling_none_config(self) -> None:
        client = FlextOracleWmsUtilitiesClient.Client(None)
        assert client.config is not None
        assert isinstance(client.config, FlextOracleWmsSettings)


@pytest.mark.unit
class TestGetLogger:
    """Tests for FlextLogger utility within WMS package."""

    def test_get_logger_module_name(self) -> None:
        u.fetch_logger("test_module")
        logger_empty = u.fetch_logger("")
        assert callable(logger_empty.info)
