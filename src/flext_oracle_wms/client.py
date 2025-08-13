"""Backward-compatibility client shim.

Historically, tests imported objects from `flext_oracle_wms.client`.
This module re-exports the modern client and exposes a simple plugin
API compatible with tests.
"""
from __future__ import annotations

from flext_core import FlextResult

from .wms_client import FlextOracleWmsClient  # re-export
from .wms_exceptions import FlextOracleWmsProcessingError


class FlextOracleWmsPlugin:
    """Minimal plugin facade used by tests.

    Provides start/stop/execute lifecycle compatible with historical tests.
    """

    def __init__(self) -> None:
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


__all__ = [
    "FlextOracleWmsClient",
    "FlextOracleWmsPlugin",
]
