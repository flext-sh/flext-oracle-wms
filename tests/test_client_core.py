"""Unit tests for FlextOracleWmsClient — core functionality coverage.

Tests against actual wms_client.py source API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from unittest.mock import MagicMock

import pytest
from flext_core import FlextLogger, FlextResult
from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsSettings,
)


@pytest.mark.unit
class TestFlextOracleWmsClientCore:
    """Core client functionality tests."""

    def test_client_initialization(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        assert client.config == mock_config
        assert client.config.base_url == mock_config.base_url
        assert hasattr(client, "_client")
        assert client._client is not None
        assert hasattr(client, "_discovered_entities")

    def test_client_string_representation(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        repr_str = repr(client)
        str_str = str(client)

        assert "FlextOracleWmsClient" in repr_str
        assert isinstance(str_str, str)

    def test_client_config_properties(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        assert client.config.base_url == mock_config.base_url
        assert client.config.timeout == mock_config.timeout
        assert client.config.retry_attempts == mock_config.retry_attempts
        assert client.config.api_version == mock_config.api_version

    def test_client_start_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)
        result = client.start()

        assert result.is_success
        assert result.value is True

    def test_client_start_multiple_times(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        result1 = client.start()
        assert result1.is_success

        result2 = client.start()
        assert result2.is_success

    def test_client_stop_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)
        client.start()
        result = client.stop()

        assert result.is_success
        assert result.value is True

    def test_client_stop_not_started(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)
        result = client.stop()

        assert result.is_success

    def test_client_has_expected_methods(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        assert hasattr(client, "start")
        assert hasattr(client, "stop")
        assert hasattr(client, "discover_entities")
        assert hasattr(client, "get_entity_data")
        assert hasattr(client, "health_check")
        assert hasattr(client, "get")
        assert hasattr(client, "post")
        assert hasattr(client, "put")
        assert hasattr(client, "delete")
        assert hasattr(client, "get_apis_by_category")
        assert hasattr(client, "call_api")
        assert hasattr(client, "update_oblpn_tracking_number")
        assert hasattr(client, "create_lpn")
        assert callable(client.start)
        assert callable(client.stop)

    def test_get_apis_by_category(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        mock_response = MagicMock()
        mock_response.body = {"apis": [{"name": "test_api"}]}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.get_apis_by_category("inventory")
        assert isinstance(result, FlextResult)
        assert result.is_success

    def test_health_check_delegates_to_get(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        mock_response = MagicMock()
        mock_response.body = {"status": "healthy"}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.health_check()
        assert result.is_success
        assert isinstance(result.value, dict)

    def test_discover_entities_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        mock_response = MagicMock()
        mock_response.body = {"entities": ["company", "facility", "item"]}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.discover_entities()
        assert result.is_success
        assert isinstance(result.value, list)
        assert len(result.value) == 3

    def test_discover_entities_failure(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        client._client = MagicMock()
        client._client.request.return_value = FlextResult.fail("Connection refused")

        result = client.discover_entities()
        assert result.is_failure

    def test_get_entity_data_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        mock_response = MagicMock()
        mock_response.body = {"data": [{"id": 1}, {"id": 2}]}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.get_entity_data("test_entity", limit=10)
        assert result.is_success
        assert result.value == [{"id": 1}, {"id": 2}]

    def test_get_entity_data_failure(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        client._client = MagicMock()
        client._client.request.return_value = FlextResult.fail("Not found")

        result = client.get_entity_data("test_entity")
        assert result.is_failure

    def test_call_api_success(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        mock_response = MagicMock()
        mock_response.body = {"result": "ok"}
        client._client = MagicMock()
        client._client.request.return_value = FlextResult.ok(mock_response)

        result = client.call_api("test_api")
        assert result.is_success

    def test_call_api_failure(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        client = FlextOracleWmsClient(mock_config)

        client._client = MagicMock()
        client._client.request.return_value = FlextResult.fail("API error")

        result = client.call_api("test_api")
        assert result.is_failure

    def test_client_error_handling_none_config(self) -> None:
        client = FlextOracleWmsClient(None)
        assert client.config is not None
        assert isinstance(client.config, FlextOracleWmsSettings)

    def test_to_record_list_with_list_of_dicts(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        result = FlextOracleWmsClient._to_record_list(
            [{"id": 1}, {"id": 2}],
        )
        assert result == [{"id": 1}, {"id": 2}]

    def test_to_record_list_with_non_list(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        result = FlextOracleWmsClient._to_record_list("not_a_list")
        assert result == []

    def test_to_record_list_filters_non_dicts(
        self,
        mock_config: FlextOracleWmsSettings,
    ) -> None:
        result = FlextOracleWmsClient._to_record_list(
            [{"id": 1}, "invalid", 42, {"id": 2}],
        )
        assert result == [{"id": 1}, {"id": 2}]


@pytest.mark.unit
class TestGetLogger:
    """Tests for FlextLogger utility within WMS package."""

    def test_get_logger_module_name(self) -> None:
        logger = FlextLogger("test_module")
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")

        logger_empty = FlextLogger("")
        assert callable(logger_empty.info)
