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

    # Why: mro-4p0t — inherit the parent's ValidationError (not the local
    # Error sibling) to satisfy the FlextExceptions override contract
    # (flext-oracle-wms-1sm3w sync fix; pattern per flext_grpc.errors).
    class ValidationError(e.ValidationError):
        """Oracle WMS validation error."""


e = FlextOracleWmsErrors

__all__: list[str] = ["FlextOracleWmsErrors", "e"]
