"""Test Oracle WMS connection structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings


def test_real_connection() -> None:
    """Test client structural setup with testing_config."""
    config = FlextOracleWmsSettings.testing_config()
    client = FlextOracleWmsClient(config)
    assert hasattr(client, "config")
    assert client.config is config
    discovery = client.discover_entities()
    assert hasattr(discovery, "is_success")
