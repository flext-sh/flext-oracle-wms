"""Unit tests for FlextOracleWmsApi (api.py facade).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextService, r

from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsClient


class _ConcreteWmsApi(FlextOracleWmsApi):
    """Concrete subclass for testing (FlextService.execute is abstract)."""

    @override
    def execute(self) -> r[None]:
        """No-op execute for tests."""
        return r[None].ok(None)


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi facade class."""

    def test_class_inheritance(self) -> None:
        """Test FlextOracleWmsApi inherits from FlextService."""
        assert issubclass(FlextOracleWmsApi, FlextService)

    def test_initialization(self) -> None:
        """Test initialization creates WMS client."""
        api = _ConcreteWmsApi()
        assert hasattr(api, "_client")
        assert isinstance(api._client, FlextOracleWmsClient)

    def test_has_logger(self) -> None:
        """Test facade has logger from FlextService."""
        api = _ConcreteWmsApi()
        assert hasattr(api, "logger")

    def test_no_business_methods_exposed(self) -> None:
        """Test facade has no public business methods (all commented out)."""
        api = _ConcreteWmsApi()
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


__all__ = ["TestFlextOracleWmsApi"]
