"""Oracle WMS exceptions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import e


class FlextOracleWmsErrors(e):
    """Oracle WMS-specific exceptions extending the API exception facade."""

    class Error(e.BaseError):
        """Base Oracle WMS error."""

    class ValidationError(Error):
        """Oracle WMS validation error."""


e = FlextOracleWmsErrors

__all__: list[str] = ["FlextOracleWmsErrors", "e"]
