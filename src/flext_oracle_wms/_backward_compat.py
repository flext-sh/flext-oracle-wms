"""Backward compatibility exports for flext-oracle-wms.

Exception classes and utility functions for consumers
that import from package root.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions


class FlextOracleWmsError(FlextExceptions.BaseError):
    """FlextOracleWmsError - real inheritance from BaseError."""


class FlextOracleWmsApiError(FlextExceptions.BaseError):
    """FlextOracleWmsApiError - real inheritance from BaseError."""


class FlextOracleWmsAuthenticationError(FlextExceptions.AuthenticationError):
    """FlextOracleWmsAuthenticationError - real inheritance from AuthenticationError."""


class FlextOracleWmsEntityNotFoundError(FlextExceptions.BaseError):
    """FlextOracleWmsEntityNotFoundError - real inheritance from BaseError."""


class FlextOracleWmsInventoryError(FlextExceptions.BaseError):
    """FlextOracleWmsInventoryError - real inheritance from BaseError."""


class FlextOracleWmsPickingError(FlextExceptions.BaseError):
    """FlextOracleWmsPickingError - real inheritance from BaseError."""


class FlextOracleWmsSchemaError(FlextExceptions.BaseError):
    """FlextOracleWmsSchemaError - real inheritance from BaseError."""


class FlextOracleWmsSchemaFlatteningError(FlextExceptions.BaseError):
    """FlextOracleWmsSchemaFlatteningError - real inheritance from BaseError."""


class FlextOracleWmsShipmentError(FlextExceptions.BaseError):
    """FlextOracleWmsShipmentError - real inheritance from BaseError."""


def get_mock_server(environment: str = "mock_test") -> object:
    """Get Oracle WMS mock server instance."""
    return {"environment": environment, "type": "mock_server"}
