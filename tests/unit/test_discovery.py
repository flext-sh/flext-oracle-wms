"""Tests for Oracle WMS discovery module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from unittest.mock import MagicMock

from flext_oracle_wms import FlextOracleWmsUtilitiesDiscovery
from tests import c, r, u


class TestsFlextOracleWmsDiscovery:
    """Test suite for discovery constants."""

    def test_discovery_success_constant(self) -> None:
        assert u.OracleWms.DISCOVERY_SUCCESS == "discovery_success"

    def test_discovery_failure_constant(self) -> None:
        assert u.OracleWms.DISCOVERY_FAILURE == "discovery_failure"

    def test_api_based_value(self) -> None:
        assert c.OracleWms.EndpointDiscoveryStrategy.API_BASED == "api_based"

    def test_schema_based_value(self) -> None:
        assert c.OracleWms.EndpointDiscoveryStrategy.SCHEMA_BASED == "schema_based"

    def test_is_str_enum(self) -> None:
        assert isinstance(c.OracleWms.EndpointDiscoveryStrategy.API_BASED, str)

    def test_initialization_with_mock_client(self) -> None:
        mock_client = MagicMock()
        discovery = FlextOracleWmsUtilitiesDiscovery.EntityDiscovery(client=mock_client)
        assert discovery.client is mock_client

    def test_discover_entities_returns_normalized_entities(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = r[list[str]].ok([
            "inventory",
            "orders",
        ])
        discovery = FlextOracleWmsUtilitiesDiscovery.EntityDiscovery(client=mock_client)
        result = discovery.discover_entities()
        assert isinstance(result, r)
        assert result.success
        assert result.value == [
            {
                "name": "inventory",
                "path": "/entities/inventory",
                "strategy": c.OracleWms.EndpointDiscoveryStrategy.API_BASED,
            },
            {
                "name": "orders",
                "path": "/entities/orders",
                "strategy": c.OracleWms.EndpointDiscoveryStrategy.API_BASED,
            },
        ]

    def test_discover_entities_filters_empty_names(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = r[list[str]].ok([
            "inventory",
            "",
            "orders",
        ])
        discovery = FlextOracleWmsUtilitiesDiscovery.EntityDiscovery(client=mock_client)
        result = discovery.discover_entities()
        assert result.success
        assert result.value == [
            {
                "name": "inventory",
                "path": "/entities/inventory",
                "strategy": c.OracleWms.EndpointDiscoveryStrategy.API_BASED,
            },
            {
                "name": "orders",
                "path": "/entities/orders",
                "strategy": c.OracleWms.EndpointDiscoveryStrategy.API_BASED,
            },
        ]

    def test_discover_entities_propagates_client_failure(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = r[list[str]].fail("upstream error")
        discovery = FlextOracleWmsUtilitiesDiscovery.EntityDiscovery(client=mock_client)
        result = discovery.discover_entities()
        assert result.failure
        assert result.error == "upstream error"

    def test_discover_entities_result_is_list(self) -> None:
        mock_client = MagicMock()
        mock_client.discover_entities.return_value = r[list[str]].ok(list[str]())
        discovery = FlextOracleWmsUtilitiesDiscovery.EntityDiscovery(client=mock_client)
        result = discovery.discover_entities()
        assert isinstance(result.value, list)
