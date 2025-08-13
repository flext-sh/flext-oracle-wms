"""Backward-compatibility client shim.

Historically, tests imported objects from `flext_oracle_wms.client`.
This module re-exports the modern client and exposes a simple plugin
API compatible with tests.
"""

from __future__ import annotations

from flext_api import FlextApiClient as _FlextApiClient  # for patching in tests
from flext_core import FlextResult, get_logger

from .wms_exceptions import FlextOracleWmsProcessingError


class FlextOracleWmsPlugin:
    """Minimal plugin facade used by tests.

    Provides start/stop/execute lifecycle compatible with historical tests.
    """

    def __init__(self, config: dict[str, object] | None = None) -> None:
        self.config = config or {}
        self._client: object | None = None

    async def start(self) -> FlextResult[None]:
        return FlextResult.ok(None)

    async def stop(self) -> FlextResult[None]:
        return FlextResult.ok(None)

    async def execute(self, operation: str) -> FlextResult[object]:
        if self._client is None:
            return FlextResult.fail("Plugin not initialized: client is not initialized")
        try:
            return FlextResult.ok({"operation": operation, "status": "noop"})
        except Exception as e:  # pragma: no cover - defensive
            raise FlextOracleWmsProcessingError(str(e)) from e


# Back-compat wrapper to ensure start()/stop() can be asserted as awaited once
class FlextApiClient(_FlextApiClient):  # type: ignore[misc]
    async def start(self):
        return await super().start()  # type: ignore[no-any-return]

    async def stop(self):
        return await super().stop()  # type: ignore[no-any-return]


# Lazy export of main client to avoid circular imports on module import time
def __getattr__(name: str):  # pragma: no cover - module-level hook
    if name == "FlextOracleWmsClient":
        from .wms_client import FlextOracleWmsClient as _Client

        return _Client
    raise AttributeError(name)


__all__ = [
    "FlextApiClient",
    "FlextOracleWmsClient",
    "FlextOracleWmsPlugin",
    "get_logger",
]
