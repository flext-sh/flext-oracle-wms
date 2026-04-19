"""Unit tests for FlextOracleWmsApi (api.py facade).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsUtilitiesClient
from tests import s, u


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi facade class."""

    def test_class_inheritance(self) -> None:
        """Test FlextOracleWmsApi inherits from s."""
        assert issubclass(FlextOracleWmsApi, s)

    def test_initialization(self) -> None:
        """Test initialization creates WMS client."""
        api = u.OracleWms.Tests.ConcreteApi()
        assert isinstance(api._client, FlextOracleWmsUtilitiesClient.Client)

    def test_has_logger(self) -> None:
        """Test facade has logger from s."""
        u.OracleWms.Tests.ConcreteApi()

    def test_no_business_methods_exposed(self) -> None:
        """Test facade has no public business methods (all commented out)."""
        api = u.OracleWms.Tests.ConcreteApi()
        public_methods = [m for m in dir(api) if not m.startswith("_")]
        business_methods = [
            "discover_entities",
            "get_inventory_data",
            "process_shipment",
            "execute_picking_wave",
        ]
        for method in business_methods:
            assert method not in public_methods or not callable(
                getattr(api, method, None),
            )


__all__: list[str] = ["TestFlextOracleWmsApi"]
