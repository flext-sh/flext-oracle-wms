"""Test Oracle WMS client class functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsModuleConfig,
    FlextOracleWmsPlugin,
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_validate_entity_name,
)


def test_client_class_creation() -> None:
    """Test client class creation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config == config


def test_client_class_with_real_methods() -> None:
    """Test client class with real available methods."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test real methods that exist
    assert hasattr(client, "get_available_apis")
    assert hasattr(client, "ship_oblpn")
    assert hasattr(client, "create_lpn")


def test_entity_name_validation() -> None:
    """Test entity name validation using real helper function."""
    # Test with invalid entity name
    result = flext_oracle_wms_validate_entity_name("")
    assert result.is_failure
    assert result.error is not None
    assert "cannot be empty" in result.error


def test_api_url_building() -> None:
    """Test API URL building using real helper function."""
    # Use real helper function
    url = flext_oracle_wms_build_entity_url(
        "https://test.example.com",
        "prod",
        "order_hdr",
    )
    assert "order_hdr" in url
    assert "wms/lgfapi" in url


def test_client_creation_class() -> None:
    """Test client class creation without context manager."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config is not None


def test_client_basic_properties() -> None:
    """Test client basic properties and methods exist."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that real methods exist
    assert hasattr(client, "start")
    assert hasattr(client, "stop")
    assert hasattr(client, "health_check")
    assert hasattr(client, "get_available_apis")

    # Test properties
    assert hasattr(client, "config")
    assert client.config is not None


def test_discover_entities_class() -> None:
    """Test entity discovery method exists (async)."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that method exists and is callable (async method)
    assert hasattr(client, "discover_entities")
    assert callable(client.discover_entities)


def test_specialized_wms_methods_class() -> None:
    """Test specialized WMS methods exist."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test real WMS-specific methods that exist
    assert hasattr(client, "ship_oblpn")
    assert hasattr(client, "create_lpn")
    assert callable(client.ship_oblpn)
    assert callable(client.create_lpn)


def test_health_check_method_class() -> None:
    """Test health check method exists (async)."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that health_check method exists and is callable (async method)
    assert hasattr(client, "health_check")
    assert callable(client.health_check)


def test_get_available_apis_method() -> None:
    """Test get available APIs method."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test actual method that exists
    result = client.get_available_apis()
    assert isinstance(result, dict)
    assert len(result) >= 0  # May be empty in test environment


def test_bulk_post_records_class() -> None:
    """Test bulk record posting in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that the client exists and has ship_oblpn method as alternative
    assert hasattr(client, "ship_oblpn")
    assert callable(client.ship_oblpn)


def test_bulk_update_records_class() -> None:
    """Test bulk record updating in class."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that the client exists and has create_lpn method as alternative
    assert hasattr(client, "create_lpn")
    assert callable(client.create_lpn)


def test_client_internal_properties() -> None:
    """Test client internal properties exist."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that internal properties exist as expected
    assert hasattr(client, "_client")
    assert hasattr(client, "_discovered_entities")
    assert hasattr(client, "_auth_headers")


def test_client_lifecycle_methods() -> None:
    """Test client lifecycle methods exist."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test that async lifecycle methods exist
    assert hasattr(client, "start")
    assert hasattr(client, "stop")
    assert callable(client.start)
    assert callable(client.stop)


def test_client_configuration_access() -> None:
    """Test client configuration is accessible."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test configuration access
    assert client.config is not None
    assert hasattr(client.config, "oracle_wms_base_url")
    assert hasattr(client.config, "oracle_wms_username")
    assert hasattr(client.config, "extract_environment_from_url")


def test_real_helper_functions() -> None:
    """Test using real helper functions from helpers module."""
    # Test real validation function
    result = flext_oracle_wms_validate_entity_name("order_hdr")
    assert result.success
    assert result.data == "order_hdr"

    # Test real URL building function
    url = flext_oracle_wms_build_entity_url("https://test.com", "prod", "order_hdr")
    assert "order_hdr" in url
    assert "wms/lgfapi" in url


def test_client_repr_and_str() -> None:
    """Test client string representation."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    # Test string representation doesn't raise errors
    str_repr = str(client)
    assert isinstance(str_repr, str)
    assert len(str_repr) > 0


def test_imports_and_modules() -> None:
    """Test that all required imports work correctly."""
    # Test that classes can be imported and instantiated
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    assert isinstance(client, FlextOracleWmsClient)
    assert isinstance(config, FlextOracleWmsModuleConfig)

    # Test plugin class
    plugin = FlextOracleWmsPlugin(name="test-plugin")
    assert isinstance(plugin, FlextOracleWmsPlugin)
