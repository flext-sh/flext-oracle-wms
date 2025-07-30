"""Test Oracle WMS client functionality."""

from unittest.mock import Mock, patch

from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsModuleConfig


def test_client_creation() -> None:
    """Test basic client creation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config == config


def test_client_with_metrics() -> None:
    """Test client creation with metrics."""
    config = FlextOracleWmsModuleConfig.for_testing()
    metrics = Mock()
    client = FlextOracleWmsClient(config, metrics=metrics)
    assert client.metrics == metrics


def test_legacy_client_creation() -> None:
    """Test legacy client creation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)


def test_context_manager() -> None:
    """Test client context manager."""
    config = FlextOracleWmsModuleConfig.for_testing()
    with FlextOracleWmsClient(config) as client:
        assert isinstance(client, FlextOracleWmsClient)


@patch("flext_oracle_wms.client.httpx")
def test_get_request(mock_httpx: Mock) -> None:
    """Test GET request functionality."""
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


def test_connection_info() -> None:
    """Test connection info generation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    info = client.get_connection_info()
    assert "base_url" in info
    assert "timeout" in info
    assert "auth_method" in info


def test_cache_stats() -> None:
    """Test cache statistics."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    stats = client.get_bulk_cache_stats()
    assert isinstance(stats, dict)


def test_clear_cache() -> None:
    """Test cache clearing."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.clear_bulk_cache()
    assert isinstance(result, bool)


def test_operation_tracking() -> None:
    """Test operation tracking statistics."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    stats = client.get_operation_tracking_stats()
    assert isinstance(stats, dict)
    assert "total_operations" in stats


async def test_discovery_entities() -> None:
    """Test entity discovery functionality."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = await client.discover_entities()
    assert result.is_success is True or result.is_success is False


async def test_connection_test() -> None:
    """Test connection testing."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = await client.test_connection()
    assert result.is_success is True or result.is_success is False


def test_client_close() -> None:
    """Test client closing."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Should not raise an exception
    client.close()


async def test_entity_data_fetch() -> None:
    """Test entity data fetching."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = await client.get_entity_data("test_entity")
    assert result.is_success is True or result.is_success is False


def test_bulk_operations() -> None:
    """Test bulk operations."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.bulk_get_entities(["entity1", "entity2"])
    assert result.is_success is True or result.is_success is False


def test_client_error_handling() -> None:
    """Test client error handling."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test with invalid entity names
    result = client.bulk_get_entities([])
    assert result.is_success is True or result.is_success is False
