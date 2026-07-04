"""Tests for Oracle WMS discovery module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from tests.constants import c


class TestsFlextOracleWmsDiscovery:
    """Test suite for discovery constants."""

    def test_discovery_success_constant(self) -> None:
        assert c.OracleWms.DISCOVERY_SUCCESS == "discovery_success"

    def test_discovery_failure_constant(self) -> None:
        assert c.OracleWms.DISCOVERY_FAILURE == "discovery_failure"
