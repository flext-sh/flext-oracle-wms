"""Test Oracle WMS connection structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient


def test_real_connection() -> None:
    """Test client structural setup with testing_config."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsUtilitiesClient.Client(config)
    assert client.config is config
    client.discover_entities()
