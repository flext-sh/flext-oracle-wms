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

    # flext-1wjg1.16: extend the framework's typed ValidationError (not the
    # local Error sibling) so this stays assignable to
    # FlextExceptionsTypes.ValidationError, the type flext-core's own
    # FlextExceptions.ValidationError declares.
    class ValidationError(e.ValidationError, Error):
        """Oracle WMS validation error."""


e = FlextOracleWmsErrors

__all__: list[str] = ["FlextOracleWmsErrors", "e"]
