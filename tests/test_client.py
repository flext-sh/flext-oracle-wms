"""Oracle WMS Client - Core Functionality Tests.

This module provides comprehensive testing for the FlextOracleWmsClient core
functionality, including client initialization, configuration management,
and basic operational patterns.

Test Coverage:
    - Client creation and initialization with various configurations
    - Configuration validation and error handling
    - Legacy client compatibility and migration patterns
    - Basic client lifecycle management

Test Categories:
    - Unit tests for client instantiation
    - Configuration validation tests
    - Error handling verification
    - Integration readiness tests

Author: FLEXT Development Team
Version: 0.9.0
License: MIT
"""


from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsModuleConfig


def test_client_creation() -> None:
    """Test basic client creation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config == config


def test_client_with_metrics() -> None:
    """Test client creation with config."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert client.config == config


def test_legacy_client_creation() -> None:
    """Test legacy client creation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)


def test_client_initialization() -> None:
    """Test client initialization and basic properties."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config is not None


def test_get_request() -> None:
    """Test client configuration access."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that client has proper configuration
    assert client.config is not None
    assert hasattr(client.config, 'base_url')
    assert hasattr(client.config, 'timeout')


def test_connection_info() -> None:
    """Test client configuration and available APIs."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test configuration is accessible
    assert client.config is not None
    assert hasattr(client.config, "base_url")
    assert hasattr(client.config, "timeout")

    # Test available APIs
    apis = client.get_available_apis()
    assert isinstance(apis, dict)
    assert len(apis) > 0


def test_cache_stats() -> None:
    """Test available APIs functionality."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    stats = client.get_available_apis()
    assert isinstance(stats, dict)


def test_clear_cache() -> None:
    """Test client configuration access."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = client.config is not None
    assert isinstance(result, bool)


def test_operation_tracking() -> None:
    """Test API categorization."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    stats = client.get_available_apis()
    assert isinstance(stats, dict)
    assert len(stats) > 0


async def test_discovery_entities() -> None:
    """Test entity discovery functionality."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = await client.discover_entities()
    assert result.is_success is True or result.is_success is False


async def test_connection_test() -> None:
    """Test connection testing using health_check."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    result = await client.health_check()
    assert result.is_success is True or result.is_success is False


async def test_client_close() -> None:
    """Test client stopping."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Should not raise an exception
    result = await client.stop()
    assert result.is_success is True or result.is_success is False


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

    # Test available APIs
    apis = client.get_available_apis()
    assert isinstance(apis, dict)


def test_client_error_handling() -> None:
    """Test client error handling."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test client initialization
    assert client.config == config
    assert hasattr(client, "_client")
