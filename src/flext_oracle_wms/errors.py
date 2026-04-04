"""FLEXT Oracle WMS Exceptions - Direct FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import e

from flext_core import FlextLogger
from flext_oracle_wms import t


class FlextOracleWmsExceptions:
    """Oracle WMS exceptions using direct FLEXT patterns.

    Follows FLEXT railway-oriented error handling directly.
    One class per module following SOLID principles.
    """

    logger = FlextLogger(__name__)

    class BaseError(e.BaseError):
        """Base WMS exception with FLEXT context handling."""

        def __init__(
            self,
            message: str,
            code: str = "WMS_ERROR",
            **context: t.Scalar,
        ) -> None:
            """Initialize base WMS error with message and error code."""
            super().__init__(message)
            self.message = message
            self.code = code
            self.context = context

    class ValidationError(BaseError):
        """Validation error."""

        def __init__(self, message: str, **context: t.Scalar) -> None:
            """Initialize validation error."""
            super().__init__(message, "WMS_VALIDATION_ERROR", **context)

    class ConfigurationError(BaseError):
        """Configuration error."""

        def __init__(self, message: str, **context: t.Scalar) -> None:
            """Initialize configuration error."""
            super().__init__(message, "WMS_CONFIG_ERROR", **context)

    class WmsConnectionError(BaseError):
        """Connection error."""

        def __init__(self, message: str, **context: t.Scalar) -> None:
            """Initialize WMS connection error."""
            super().__init__(message, "WMS_CONNECTION_ERROR", **context)

    class AuthenticationError(BaseError):
        """Authentication error."""

        def __init__(self, message: str, **context: t.Scalar) -> None:
            """Initialize authentication error."""
            super().__init__(message, "WMS_AUTH_ERROR", **context)

    class ProcessingError(BaseError):
        """Processing error."""

        def __init__(self, message: str, **context: t.Scalar) -> None:
            """Initialize processing error."""
            super().__init__(message, "WMS_PROCESSING_ERROR", **context)

    class ApiError(BaseError):
        """API error."""

        def __init__(self, message: str, **context: t.Scalar) -> None:
            """Initialize API error."""
            super().__init__(message, "WMS_API_ERROR", **context)

    class InventoryError(ProcessingError):
        """Inventory error."""

    class ShipmentError(ProcessingError):
        """Shipment error."""

    class PickingError(ProcessingError):
        """Picking error."""

    class EntityNotFoundError(ValidationError):
        """Entity not found error."""

    class SchemaError(ValidationError):
        """Schema error."""

    class SchemaFlatteningError(SchemaError):
        """Schema flattening error."""


class FlextOracleWmsError(FlextOracleWmsExceptions.BaseError):
    """FlextOracleWmsError - real inheritance from BaseError."""


class FlextOracleWmsApiError(FlextOracleWmsExceptions.ApiError):
    """FlextOracleWmsApiError - real inheritance from ApiError."""


class FlextOracleWmsAuthenticationError(FlextOracleWmsExceptions.AuthenticationError):
    """FlextOracleWmsAuthenticationError - real inheritance from AuthenticationError."""


class FlextOracleWmsConfigurationError(FlextOracleWmsExceptions.ConfigurationError):
    """FlextOracleWmsConfigurationError - real inheritance from ConfigurationError."""


class FlextOracleWmsConnectionError(FlextOracleWmsExceptions.WmsConnectionError):
    """FlextOracleWmsConnectionError - real inheritance from WmsConnectionError."""


class FlextOracleWmsDataValidationError(FlextOracleWmsExceptions.ValidationError):
    """FlextOracleWmsDataValidationError - real inheritance from ValidationError."""


class FlextOracleWmsEntityNotFoundError(FlextOracleWmsExceptions.EntityNotFoundError):
    """FlextOracleWmsEntityNotFoundError - real inheritance from EntityNotFoundError."""


class FlextOracleWmsInventoryError(FlextOracleWmsExceptions.InventoryError):
    """FlextOracleWmsInventoryError - real inheritance from InventoryError."""


class FlextOracleWmsPickingError(FlextOracleWmsExceptions.PickingError):
    """FlextOracleWmsPickingError - real inheritance from PickingError."""


class FlextOracleWmsProcessingError(FlextOracleWmsExceptions.ProcessingError):
    """FlextOracleWmsProcessingError - real inheritance from ProcessingError."""


class FlextOracleWmsSchemaError(FlextOracleWmsExceptions.SchemaError):
    """FlextOracleWmsSchemaError - real inheritance from SchemaError."""


class FlextOracleWmsSchemaFlatteningError(
    FlextOracleWmsExceptions.SchemaFlatteningError,
):
    """FlextOracleWmsSchemaFlatteningError - real inheritance from SchemaFlatteningError."""


class FlextOracleWmsShipmentError(FlextOracleWmsExceptions.ShipmentError):
    """FlextOracleWmsShipmentError - real inheritance from ShipmentError."""


class FlextOracleWmsValidationError(FlextOracleWmsExceptions.ValidationError):
    """FlextOracleWmsValidationError - real inheritance from ValidationError."""


__all__ = [
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsExceptions",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsValidationError",
]
