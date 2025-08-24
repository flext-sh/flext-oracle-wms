"""Backward-compatibility client shim.

Historically, tests imported objects from `flext_oracle_wms.client`.
This module re-exports the modern client and exposes a simple plugin
API compatible with tests.
"""

from __future__ import annotations

from flext_api import FlextApiClient as _FlextApiClient  # for patching in tests
from flext_core import FlextResult, get_logger

from .wms_client import FlextOracleWmsClient as _Client
from .wms_exceptions import FlextOracleWmsProcessingError


class FlextOracleWmsPlugin:
    """Minimal plugin facade used by tests.

    Provides start/stop/execute lifecycle compatible with historical tests.
    """

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Init   function.

        Args:
            config (dict[str, object] | None): Description.

        """
        self.config = config or {}
        self._client: object | None = None

    async def start(self) -> FlextResult[None]:
        """Start function.

        Returns:
            FlextResult[None]: Description.

        """
        return FlextResult[None].ok(None)

    async def stop(self) -> FlextResult[None]:
        """Stop function.

        Returns:
            FlextResult[None]: Description.

        """
        return FlextResult[None].ok(None)

    async def execute(self, operation: str) -> FlextResult[object]:
        """Execute function.

        Args:
            operation (str): Description.

        Returns:
            FlextResult[object]: Description.

        """
        if self._client is None:
            return FlextResult[object].fail(
                "Plugin not initialized: client is not initialized"
            )
        try:
            return FlextResult[object].ok({"operation": operation, "status": "noop"})
        except Exception as e:  # pragma: no cover - defensive
            raise FlextOracleWmsProcessingError(str(e)) from e


# Back-compat wrapper to ensure start()/stop() can be asserted as awaited once
class FlextApiClient(_FlextApiClient):
    """FlextApiClient class."""

    async def start(self) -> FlextResult[None]:
        """Start function."""
        return await super().start()

    async def stop(self) -> FlextResult[None]:
        """Stop function."""
        return await super().stop()


# Lazy export of main client to avoid circular imports on module import time
def __getattr__(name: str) -> object:  # pragma: no cover - module-level hook
    """Getattr   function.

    Args:
      name (str): Description.

    """
    if name == "FlextOracleWmsClient":
        return _Client
    raise AttributeError(name)


# Expose imports for explicit reference in __all__
FlextOracleWmsClient = _Client

__all__ = [
    "FlextApiClient",
    "FlextOracleWmsClient",
    "FlextOracleWmsPlugin",
    "get_logger",
]
