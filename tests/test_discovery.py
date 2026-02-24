"""Tests for Oracle WMS discovery module.

Tests against actual wms_discovery.py source (minimal placeholder).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

from flext_core import FlextResult

from flext_oracle_wms import FlextOracleWmsEntityDiscovery
from flext_oracle_wms.wms_discovery import (
    DISCOVERY_FAILURE,
    DISCOVERY_SUCCESS,
    CacheValue,
    DiscoveryContext,
    EndpointDiscoveryStrategy,
    EntityResponseParser,
    FlextOracleWmsDefaults,
)


class TestDiscoveryConstants:
    def test_discovery_success_constant(self) -> None:
        assert DISCOVERY_SUCCESS == "discovery_success"

    def test_discovery_failure_constant(self) -> None:
        assert DISCOVERY_FAILURE == "discovery_failure"


class TestPlaceholderClasses:
    def test_cache_value_instantiates(self) -> None:
        cv = CacheValue()
        assert cv is not None

    def test_discovery_context_instantiates(self) -> None:
        ctx = DiscoveryContext()
        assert ctx is not None

    def test_entity_response_parser_instantiates(self) -> None:
        parser = EntityResponseParser()
        assert parser is not None

    def test_flext_oracle_wms_defaults_cache_ttl(self) -> None:
        assert FlextOracleWmsDefaults.CACHE_TTL == 3600


class TestEndpointDiscoveryStrategyEnum:
    def test_api_based_value(self) -> None:
        assert EndpointDiscoveryStrategy.API_BASED == "api_based"

    def test_schema_based_value(self) -> None:
        assert EndpointDiscoveryStrategy.SCHEMA_BASED == "schema_based"

    def test_is_str_enum(self) -> None:
        assert isinstance(EndpointDiscoveryStrategy.API_BASED, str)


class TestFlextOracleWmsEntityDiscovery:
    def test_initialization_with_mock_client(self) -> None:
        mock_client = MagicMock()
        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        assert discovery.client is mock_client

    def test_discover_entities_returns_ok_empty_list(self) -> None:
        mock_client = MagicMock()
        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        result = discovery.discover_entities()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.value == []

    def test_discover_entities_result_is_list(self) -> None:
        mock_client = MagicMock()
        discovery = FlextOracleWmsEntityDiscovery(client=mock_client)
        result = discovery.discover_entities()

        assert isinstance(result.value, list)
