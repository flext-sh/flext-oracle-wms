"""Unit tests for FlextOracleWmsApi (api.py facade).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextService, r
from flext_tests import tm

from flext_oracle_wms.api import FlextOracleWmsApi
from flext_oracle_wms.wms_client import FlextOracleWmsClient


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
        tm.that(issubclass(FlextOracleWmsApi, FlextService), eq=True)

    def test_initialization(self) -> None:
        """Test initialization creates WMS client."""
        api = _ConcreteWmsApi()
        tm.that(hasattr(api, "_client"), eq=True)
        tm.that(isinstance(api._client, FlextOracleWmsClient), eq=True)

    def test_has_logger(self) -> None:
        """Test facade has logger from FlextService."""
        api = _ConcreteWmsApi()
        tm.that(hasattr(api, "logger"), eq=True)

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
            tm.that(
                method not in public_methods
                or not callable(getattr(api, method, None)),
                eq=True,
            )


__all__ = ["TestFlextOracleWmsApi"]
