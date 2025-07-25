"""Test Oracle WMS client class functionality."""

from unittest.mock import Mock, patch

import pytest

from flext_oracle_wms.client_class import (
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsClient,
    FlextOracleWmsClientError,
    FlextOracleWmsConnectionError,
)
from flext_oracle_wms.config_module import FlextOracleWmsModuleConfig


def test_client_class_creation() -> None:
    """Test client class creation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config == config


def test_client_class_with_metrics() -> None:
    """Test client class creation with metrics."""
    config = FlextOracleWmsModuleConfig.for_testing()
    metrics = Mock()
    client = FlextOracleWmsClient(config, metrics=metrics)
    assert client.metrics == metrics


def test_entity_name_validation() -> None:
    """Test entity name validation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # This should raise ValueError for invalid entity
    with pytest.raises(ValueError):
        client.validate_entity_name("invalid_entity")


def test_api_url_building() -> None:
    """Test API URL building."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Mock the validate_entity_name to return valid entity
    with patch.object(client, "validate_entity_name", return_value="order_hdr"):
        url = client.build_api_url("order_hdr")
        assert "order_hdr" in url
        assert "wms/lgfapi" in url


def test_context_manager_class() -> None:
    """Test client class context manager."""
    config = FlextOracleWmsModuleConfig.for_testing()
    with FlextOracleWmsClient(config) as client:
        assert isinstance(client, FlextOracleWmsClient)


@patch("flext_oracle_wms.client_class.httpx")
def test_get_request_class(mock_httpx) -> None:
    """Test GET request functionality in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    mock_httpx.Client.return_value.get.return_value = mock_response

    result = client.get("/test")
    assert result == {"status": "success"}


def test_discover_entities_class() -> None:
    """Test entity discovery in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.discover_entities()
    assert hasattr(result, "is_success")


def test_get_entity_data_class() -> None:
    """Test get entity data in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.get_entity_data("test_entity")
    assert hasattr(result, "is_success")


def test_test_connection_class() -> None:
    """Test connection testing in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.test_connection()
    assert hasattr(result, "is_success")


def test_bulk_get_entities_class() -> None:
    """Test bulk entity retrieval in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.bulk_get_entities(["entity1", "entity2"])
    assert hasattr(result, "is_success")


def test_bulk_post_records_class() -> None:
    """Test bulk record posting in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    records = [{"id": 1, "name": "test"}]
    result = client.bulk_post_records("test_entity", records)
    assert hasattr(result, "is_success")


def test_bulk_update_records_class() -> None:
    """Test bulk record updating in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    records = [{"id": 1, "name": "updated"}]
    result = client.bulk_update_records("test_entity", records)
    assert hasattr(result, "is_success")


def test_cache_stats_class() -> None:
    """Test cache statistics in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    stats = client.get_bulk_cache_stats()
    assert isinstance(stats, dict)


def test_clear_cache_class() -> None:
    """Test cache clearing in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.clear_bulk_cache()
    assert isinstance(result, bool)


def test_operation_tracking_class() -> None:
    """Test operation tracking in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    stats = client.get_operation_tracking_stats()
    assert isinstance(stats, dict)
    assert "total_operations" in stats


def test_connection_info_class() -> None:
    """Test connection info in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    info = client.get_connection_info()
    assert isinstance(info, dict)
    assert "base_url" in info


def test_client_close_class() -> None:
    """Test client closing in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Should not raise an exception
    client.close()


def test_exception_hierarchy() -> None:
    """Test exception hierarchy."""
    assert issubclass(FlextOracleWmsClientError, Exception)
    assert issubclass(FlextOracleWmsAuthenticationError, FlextOracleWmsClientError)
    assert issubclass(FlextOracleWmsConnectionError, FlextOracleWmsClientError)


def test_response_error_handling() -> None:
    """Test response error handling."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Mock response with 401 status
    mock_response = Mock()
    mock_response.status_code = 401

    with pytest.raises(FlextOracleWmsAuthenticationError):
        client._handle_response_errors(mock_response)

    # Mock response with 500 status
    mock_response.status_code = 500
    with pytest.raises(FlextOracleWmsConnectionError):
        client._handle_response_errors(mock_response)

    # Mock response with 400 status
    mock_response.status_code = 400
    with pytest.raises(FlextOracleWmsClientError):
        client._handle_response_errors(mock_response)
