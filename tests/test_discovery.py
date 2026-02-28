"""Tests for Oracle WMS discovery module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from unittest.mock import MagicMock

from flext_core import FlextResult
from flext_oracle_wms import FlextOracleWmsEntityDiscovery
from flext_oracle_wms.constants import FlextOracleWmsConstants as c
from flext_oracle_wms.wms_discovery import (
    DISCOVERY_FAILURE,
    DISCOVERY_SUCCESS,
)


class TestDiscoveryConstants:
    """Test suite for discovery constants."""

    def test_discovery_success_constant(self) -> None:
        assert DISCOVERY_SUCCESS == "discovery_success"

    def test_discovery_failure_constant(self) -> None:
        assert DISCOVERY_FAILURE == "discovery_failure"


class TestEndpointDiscoveryStrategyEnum:
    """Test suite for EndpointDiscoveryStrategy enum."""

    def test_api_based_value(self) -> None:
        assert c.EndpointDiscoveryStrategy.API_BASED == "api_based"

    def test_schema_based_value(self) -> None:
        assert c.EndpointDiscoveryStrategy.SCHEMA_BASED == "schema_based"

    def test_is_str_enum(self) -> None:
        assert isinstance(c.EndpointDiscoveryStrategy.API_BASED, str)


class TestFlextOracleWmsEntityDiscovery:
    """Test suite for FlextOracleWmsEntityDiscovery class."""

    def test_initialization_with_mock_client(self) -> None:
        mock_client = MagicMock()
        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        assert discovery.client is mock_client

    def test_discover_entities_returns_normalized_entities(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = FlextResult.ok(
            ["inventory", "orders"],
        )

        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        result = discovery.discover_entities()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == [
            {
                "name": "inventory",
                "path": "/entities/inventory",
                "strategy": c.EndpointDiscoveryStrategy.API_BASED,
            },
            {
                "name": "orders",
                "path": "/entities/orders",
                "strategy": c.EndpointDiscoveryStrategy.API_BASED,
            },
        ]

    def test_discover_entities_filters_empty_names(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = FlextResult.ok(
            ["inventory", "", "orders"],
        )

        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        result = discovery.discover_entities()

        assert result.is_success
        assert result.value == [
            {
                "name": "inventory",
                "path": "/entities/inventory",
                "strategy": c.EndpointDiscoveryStrategy.API_BASED,
            },
            {
                "name": "orders",
                "path": "/entities/orders",
                "strategy": c.EndpointDiscoveryStrategy.API_BASED,
            },
        ]

    def test_discover_entities_propagates_client_failure(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = FlextResult.fail("upstream error")

        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        result = discovery.discover_entities()

        assert result.is_failure
        assert result.error == "upstream error"

    def test_discover_entities_result_is_list(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = FlextResult.ok([])

        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        result = discovery.discover_entities()

        assert isinstance(result.value, list)
