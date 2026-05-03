"""Tests for Oracle WMS discovery module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from tests import c, u


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
