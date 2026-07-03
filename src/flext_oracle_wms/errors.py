"""Oracle WMS exceptions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import e


class FlextOracleWmsError(e.BaseError):
    """Base Oracle WMS error."""


class FlextOracleWmsValidationError(FlextOracleWmsError):
    """Oracle WMS validation error."""


__all__: list[str] = [
    "FlextOracleWmsError",
    "FlextOracleWmsValidationError",
]
