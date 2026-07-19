"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_oracle_wms import (
    FlextOracleWmsSettings,
    c,
    m,
    p,
    r,
    s,
    t,
    u,
)


class FlextOracleWmsApi(s[bool]):
    """Thin facade for Oracle WMS operations with complete FLEXT integration.

    Integrates:
    - FlextBus: Event emission for WMS operations
    - FlextContainer: Dependency injection for WMS services
    - FlextContext: Operation context management
    - FlextCqrs: CQRS pattern for WMS commands/queries
    - FlextDispatcher: Message routing for WMS operations
    - FlextRegistry: Component registration for WMS plugins
    - `u.fetch_logger(...)` / `p.Logger`: Structured logging for WMS operations

    This facade provides easy access to all Oracle WMS functionality
    while maintaining clean separation between business logic and infrastructure.
    """

    def __init__(self, settings: FlextOracleWmsSettings | None = None) -> None:
        """Initialize Oracle WMS facade with FLEXT integration."""
        super().__init__()
        self._client = u.OracleWms.Client(settings=settings)

    @override
    def execute(self) -> p.Result[bool]:
        """Execute Oracle WMS operations.

        Default execute surface signals readiness; consumers call the
        domain-specific methods (``fetch_settings``, ``call_endpoint``, …)
        for real work. Returning ``r[bool].ok(True)`` matches the
        ``s[bool]`` type parameter.
        """
        return r[bool].ok(value=True)

    @staticmethod
    def api_endpoints() -> t.MappingKV[str, m.OracleWms.ApiEndpoint]:
        """Return Oracle WMS API endpoint models from canonical constants."""
        return {
            name: m.OracleWms.ApiEndpoint.model_validate(payload)
            for name, payload in c.OracleWms.API_ENDPOINTS.items()
        }

    @staticmethod
    def create_flext_http_client(
        base_url: str,
        timeout: float = 30.0,
        headers: t.StrMapping | None = None,
        *,
        verify_ssl: bool = True,
    ) -> u.OracleWms.HttpClient:
        """Create FlextHttpClient instance."""
        return u.OracleWms.HttpClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            verify_ssl=verify_ssl,
        )

    @staticmethod
    def create_oracle_wms_client(
        settings: m.OracleWms.AuthSettings,
    ) -> p.Result[u.OracleWms.Client]:
        """Create a runtime Oracle WMS client from auth settings."""
        result: p.Result[u.OracleWms.Client] = (
            u.OracleWms.Client.from_auth_settings(settings)
        )
        return result


oracle_wms = FlextOracleWmsApi

__all__: list[str] = ["FlextOracleWmsApi", "oracle_wms"]
