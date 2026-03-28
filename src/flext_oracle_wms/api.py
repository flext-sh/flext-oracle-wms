"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar, override

from flext_core import FlextService, r

from flext_oracle_wms.http_client import FlextHttpClient
from flext_oracle_wms.models import FlextOracleWmsModels as m
from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.typings import FlextOracleWmsTypes as t
from flext_oracle_wms.wms_client import FlextOracleWmsClient


class FlextOracleWmsApi(FlextService[None]):
    """Thin facade for Oracle WMS operations with complete FLEXT integration.

    Integrates:
    - FlextBus: Event emission for WMS operations
    - FlextContainer: Dependency injection for WMS services
    - FlextContext: Operation context management
    - FlextCqrs: CQRS pattern for WMS commands/queries
    - FlextDispatcher: Message routing for WMS operations
    - FlextRegistry: Component registration for WMS plugins
    - FlextLogger: Structured logging for WMS operations

    This facade provides easy access to all Oracle WMS functionality
    while maintaining clean separation between business logic and infrastructure.
    """

    FLEXT_ORACLE_WMS_APIS: ClassVar[Mapping[str, m.OracleWms.ApiEndpoint]] = {
        "test": m.OracleWms.ApiEndpoint(
            name="test",
            method="GET",
            path="/test/",
            version="v1",
            category="test",
            description="Test endpoint",
            since_version="6.1",
        ),
    }

    class OracleWmsMockServer:
        """Mock server simulating Oracle WMS Cloud API v10 responses."""

    @classmethod
    def create_mock_server(cls) -> FlextOracleWmsApi.OracleWmsMockServer:
        """Create mock server instance."""
        return cls.OracleWmsMockServer()

    def __init__(self, config: FlextOracleWmsSettings | None = None) -> None:
        """Initialize Oracle WMS facade with FLEXT integration."""
        super().__init__(
            config_type=None,
            config_overrides=None,
            initial_context=None,
        )
        resolved_config = (
            config if config is not None else FlextOracleWmsSettings.get_global()
        )
        self._client = FlextOracleWmsClient(config=resolved_config)

    @override
    def execute(self) -> r[None]:
        """Execute Oracle WMS operations."""
        return r[None].ok(None)

    @staticmethod
    def create_flext_http_client(
        base_url: str,
        timeout: float = 30.0,
        headers: t.StrMapping | None = None,
        *,
        verify_ssl: bool = True,
    ) -> FlextHttpClient:
        """Create FlextHttpClient instance."""
        return FlextHttpClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            verify_ssl=verify_ssl,
        )

    @staticmethod
    def create_oracle_wms_client(config: m.OracleWms.AuthSettings) -> r[str]:
        """Reject auth-only client construction without runtime WMS settings."""
        _ = config
        msg = (
            "Oracle WMS client creation requires runtime settings with base_url; "
            "instantiate FlextOracleWmsClient directly with FlextOracleWmsSettings."
        )
        raise NotImplementedError(
            msg,
        )


__all__ = ["FlextOracleWmsApi"]
