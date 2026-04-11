"""Test Oracle WMS client class functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient


def test_client_class_creation() -> None:
    """Test client class creation."""
    settings = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    assert isinstance(client, FlextOracleWmsUtilitiesClient.Client)
    assert client.settings is settings


def test_client_has_http_methods() -> None:
    """Test client has get/post/put/delete methods."""
    settings = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    assert callable(client.get)
    assert callable(client.post)
    assert callable(client.put)
    assert callable(client.delete)


def test_client_has_lifecycle_methods() -> None:
    """Test client has start/stop/health_check methods."""
    settings = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    assert callable(client.start)
    assert callable(client.stop)
    assert callable(client.health_check)


def test_client_has_discovery_methods() -> None:
    """Test client has discover_entities and get_entity_data."""
    settings = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    assert callable(client.discover_entities)
    assert callable(client.get_entity_data)


def test_client_has_wms_operations() -> None:
    """Test client has WMS-specific operations."""
    settings = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    assert callable(client.update_oblpn_tracking_number)
    assert callable(client.create_lpn)
    assert callable(client.call_api)
    assert callable(client.get_apis_by_category)


def test_client_internal_state() -> None:
    """Test client internal attributes after creation."""
    settings = FlextOracleWmsSettings.testing_config()
    FlextOracleWmsUtilitiesClient.Client(settings)


def test_client_config_access() -> None:
    """Test client configuration is accessible with correct field names."""
    settings = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(settings)
    assert client.settings is not None
