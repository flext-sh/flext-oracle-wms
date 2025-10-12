"""Unit tests for FlextOracleWmsApi class.

Tests the main API facade following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextCore

from flext_oracle_wms.api import FlextOracleWmsApi
from flext_oracle_wms.config import FlextOracleWmsConfig


class TestFlextOracleWmsApi:
    """Test cases for FlextOracleWmsApi class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsApi follows proper inheritance patterns."""
        # FlextOracleWmsApi should inherit from FlextCore.Service
        from flext_core import FlextCore

        assert issubclass(FlextOracleWmsApi, FlextCore.Service)

    def test_initialization_without_config(self) -> None:
        """Test initialization without explicit configuration."""
        api = FlextOracleWmsApi()

        # Should create default config
        assert hasattr(api, "_config")
        assert isinstance(api._config, FlextOracleWmsConfig)

        # Should initialize all FLEXT components
        assert isinstance(api._container, type(FlextCore.Container.get_global()))
        assert isinstance(api._context, FlextCore.Context)
        assert isinstance(api._bus, FlextCore.Bus)
        assert isinstance(api._dispatcher, FlextCore.Dispatcher)

        # Should initialize logger
        assert hasattr(api, "logger")

    def test_initialization_with_config(self) -> None:
        """Test initialization with explicit configuration."""
        config = FlextOracleWmsConfig()
        api = FlextOracleWmsApi(config=config)

        assert api._config is config

    def test_flext_integration_components(self) -> None:
        """Test that all FLEXT integration components are properly initialized."""
        api = FlextOracleWmsApi()

        # Test FLEXT ecosystem components
        assert api._container is not None
        assert api._context is not None
        assert api._bus is not None
        assert api._dispatcher is not None
        assert api._handlers is not None
        assert api._processors is not None
        assert api._registry is not None
        assert api.logger is not None

    def test_client_initialization(self) -> None:
        """Test that WMS client is properly initialized."""
        api = FlextOracleWmsApi()

        # Should have WMS client initialized
        assert hasattr(api, "_client")
        from flext_oracle_wms.wms_client import FlextOracleWmsClient

        assert isinstance(api._client, FlextOracleWmsClient)

    def test_no_business_logic_in_facade(self) -> None:
        """Test that facade contains no business logic, only delegation."""
        api = FlextOracleWmsApi()

        # Facade should not have business methods implemented
        # (they are commented out in the current implementation)
        methods = [method for method in dir(api) if not method.startswith("_")]
        business_methods = [
            "discover_entities",
            "get_inventory_data",
            "process_shipment",
            "execute_picking_wave",
        ]

        # None of the business methods should be implemented
        for method in business_methods:
            assert method not in methods or not callable(getattr(api, method, None))


__all__ = ["TestFlextOracleWmsApi"]
