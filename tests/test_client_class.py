"""Test Oracle WMS client class functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings


def test_client_class_creation() -> None:
    """Test client class creation."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert isinstance(client, FlextOracleWmsClient)
    assert client.config is config


def test_client_has_http_methods() -> None:
    """Test client has get/post/put/delete methods."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert callable(client.get)
    assert callable(client.post)
    assert callable(client.put)
    assert callable(client.delete)


def test_client_has_lifecycle_methods() -> None:
    """Test client has start/stop/health_check methods."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert callable(client.start)
    assert callable(client.stop)
    assert callable(client.health_check)


def test_client_has_discovery_methods() -> None:
    """Test client has discover_entities and get_entity_data."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert callable(client.discover_entities)
    assert callable(client.get_entity_data)


def test_client_has_wms_operations() -> None:
    """Test client has WMS-specific operations."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert callable(client.update_oblpn_tracking_number)
    assert callable(client.create_lpn)
    assert callable(client.call_api)
    assert callable(client.get_apis_by_category)


def test_client_internal_state() -> None:
    """Test client internal attributes after creation."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert hasattr(client, "_client")
    assert hasattr(client, "_discovered_entities")


def test_client_config_access() -> None:
    """Test client configuration is accessible with correct field names."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert client.config is not None
    assert hasattr(client.config, "base_url")
    assert hasattr(client.config, "timeout")
    assert hasattr(client.config, "environment_from_url")
