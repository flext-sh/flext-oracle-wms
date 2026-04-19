"""Oracle WMS exceptions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import e


class FlextOracleWmsError(e.BaseError):
    """Base Oracle WMS error."""


class FlextOracleWmsApiError(FlextOracleWmsError):
    """Oracle WMS API error."""


class FlextOracleWmsAuthenticationError(FlextOracleWmsError):
    """Oracle WMS authentication error."""


class FlextOracleWmsConfigurationError(FlextOracleWmsError):
    """Oracle WMS configuration error."""


class FlextOracleWmsConnectionError(FlextOracleWmsError):
    """Oracle WMS connection error."""


class FlextOracleWmsValidationError(FlextOracleWmsError):
    """Oracle WMS validation error."""


class FlextOracleWmsEntityNotFoundError(FlextOracleWmsValidationError):
    """Oracle WMS entity not found."""


__all__: list[str] = [
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsValidationError",
]
