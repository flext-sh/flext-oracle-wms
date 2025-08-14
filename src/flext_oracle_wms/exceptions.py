"""Backward-compatibility exceptions shim.

Provides `flext_oracle_wms.exceptions` import path by re-exporting the
exception classes from the consolidated exceptions module.
"""

from __future__ import annotations

from .wms_exceptions import (
    FlextOracleWmsProcessingError,
)


# Provide back-compat names expected by older tests
class FlextOracleWmsFilterError(FlextOracleWmsProcessingError):
    """Legacy alias for filter-related processing errors."""


class FlextOracleWmsRateLimitError(FlextOracleWmsProcessingError):
    """Legacy alias for rate limit errors (maps to processing error)."""


__all__ = [
    *[name for name in globals() if name.startswith("FlextOracleWms")],
    "FlextOracleWmsFilterError",
    "FlextOracleWmsRateLimitError",
]
