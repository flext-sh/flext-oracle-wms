"""Test Oracle WMS connection structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient


class TestsFlextOracleWmsConnection:
    """Behavior contract for test_connection."""

    def test_real_connection(self) -> None:
        """Test client structural setup with testing_config."""
        settings = FlextOracleWmsSettings.testing_config()
        client = FlextOracleWmsUtilitiesClient.Client(settings)
        assert client.settings is settings
        client.discover_entities()
