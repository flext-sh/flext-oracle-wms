"""FLEXT Oracle WMS Exceptions - Direct FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextLogger


# Direct FLEXT pattern implementation - no inheritance from FlextExceptions to avoid conflicts
class FlextOracleWmsExceptions:
    """Oracle WMS exceptions using direct FLEXT patterns.

    Follows FLEXT railway-oriented error handling directly.
    One class per module following SOLID principles.
    """

    logger = FlextLogger(__name__)

    # Base exception class following FLEXT patterns directly
    class BaseError(Exception):
        """Base WMS exception with FLEXT context handling."""

        def __init__(
            self, message: str, code: str = "WMS_ERROR", **context: object
        ) -> None:
            super().__init__(message)
            self.message = message
            self.code = code
            self.context = context

    # Domain-specific exceptions following FLEXT inheritance patterns
    class ValidationError(BaseError):
        """Validation error."""

        def __init__(self, message: str, **context: object) -> None:
            super().__init__(message, "WMS_VALIDATION_ERROR", **context)

    class ConfigurationError(BaseError):
        """Configuration error."""

        def __init__(self, message: str, **context: object) -> None:
            super().__init__(message, "WMS_CONFIG_ERROR", **context)

    class WmsConnectionError(BaseError):
        """Connection error."""

        def __init__(self, message: str, **context: object) -> None:
            super().__init__(message, "WMS_CONNECTION_ERROR", **context)

    class AuthenticationError(BaseError):
        """Authentication error."""

        def __init__(self, message: str, **context: object) -> None:
            super().__init__(message, "WMS_AUTH_ERROR", **context)

    class ProcessingError(BaseError):
        """Processing error."""

        def __init__(self, message: str, **context: object) -> None:
            super().__init__(message, "WMS_PROCESSING_ERROR", **context)

    # Specific domain exceptions following FLEXT inheritance
    class ApiError(BaseError):
        """API error."""

        def __init__(self, message: str, **context: object) -> None:
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


# Direct FLEXT pattern exports - no aliases, direct usage
FlextOracleWmsError = FlextOracleWmsExceptions.BaseError
FlextOracleWmsApiError = FlextOracleWmsExceptions.ApiError
FlextOracleWmsAuthenticationError = FlextOracleWmsExceptions.AuthenticationError
FlextOracleWmsConfigurationError = FlextOracleWmsExceptions.ConfigurationError
FlextOracleWmsConnectionError = FlextOracleWmsExceptions.WmsConnectionError
FlextOracleWmsDataValidationError = FlextOracleWmsExceptions.ValidationError
FlextOracleWmsEntityNotFoundError = FlextOracleWmsExceptions.EntityNotFoundError
FlextOracleWmsInventoryError = FlextOracleWmsExceptions.InventoryError
FlextOracleWmsPickingError = FlextOracleWmsExceptions.PickingError
FlextOracleWmsProcessingError = FlextOracleWmsExceptions.ProcessingError
FlextOracleWmsSchemaError = FlextOracleWmsExceptions.SchemaError
FlextOracleWmsSchemaFlatteningError = FlextOracleWmsExceptions.SchemaFlatteningError
FlextOracleWmsShipmentError = FlextOracleWmsExceptions.ShipmentError
FlextOracleWmsValidationError = FlextOracleWmsExceptions.ValidationError

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
