"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextService, r

from flext_oracle_wms import m, t
from flext_oracle_wms.http_client import FlextHttpClient
from flext_oracle_wms.wms_auth import FlextOracleWmsAuthenticator
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

    def __init__(self) -> None:
        """Initialize Oracle WMS facade with FLEXT integration."""
        super().__init__(
            config_type=None,
            config_overrides=None,
            initial_context=None,
        )
        self._client = FlextOracleWmsClient()

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
        """Create authenticated Oracle WMS client."""
        authenticator = FlextOracleWmsAuthenticator(config)
        auth_result = authenticator.authenticate()
        if auth_result.is_failure:
            return r[str].fail(f"Authentication failed: {auth_result.error}")
        return r[str].fail("Oracle WMS client creation not configured")


__all__ = ["FlextOracleWmsApi"]
