"""Oracle WMS Exceptions - Consolidated Exception Hierarchy.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise-grade exception hierarchy for Oracle WMS operations with explicit
class definitions for type safety. This module consolidates all Oracle WMS-specific
exceptions into a single coherent hierarchy compatible with MyPy static analysis.
"""

from __future__ import annotations

import contextlib

from flext_core import (
    FlextAuthenticationError,
    FlextError,
    FlextErrorCodes,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)

# =============================================================================
# ORACLE WMS BASE EXCEPTION HIERARCHY
# =============================================================================


class FlextOracleWmsError(FlextError):
    """Base exception for all Oracle WMS operations.

    Propagates context attributes (like entity_name) to support tests that
    access them directly on the exception instance.
    """

    def __init__(
        self,
        message: str,
        *,
        context: dict[str, object] | None = None,
        error_code: str | None = None,
    ) -> None:
        # Convert string error code to FlextErrorCodes enum
        flext_code = None
        if error_code:
            try:
                flext_code = FlextErrorCodes(error_code)
            except ValueError:
                # Fallback to generic error for unknown codes
                flext_code = FlextErrorCodes.GENERIC_ERROR
        super().__init__(message, context=context or {}, code=flext_code)
        # Attach context keys as attributes for convenient access in tests
        for key, value in (context or {}).items():
            with contextlib.suppress(Exception):
                setattr(self, key, value)


class FlextOracleWmsValidationError(FlextValidationError):
    """Oracle WMS validation error with comprehensive field context.

    Specialized validation error for Oracle WMS entity and configuration
    validation failures. Provides detailed context about validation failures
    including field names, validation rules, and error details.
    """


class FlextOracleWmsConfigurationError(FlextOracleWmsError):
    """Oracle WMS configuration error with comprehensive configuration context.

    Specialized configuration error for Oracle WMS setup and configuration
    validation failures. Provides detailed context about configuration issues.
    """

    def __init__(self, message: str = "Config error", **kwargs: object) -> None:
        super().__init__(message, error_code="FLEXT_CONFIG_ERROR", context=kwargs or {})


class FlextOracleWmsConnectionError(FlextOracleWmsError):
    """Oracle WMS connection error with comprehensive network context.

    Specialized connection error for Oracle WMS network communication failures.
    Provides detailed context about connection issues including API endpoints,
    network conditions, and error details.
    """

    def __init__(self, message: str = "Connection failed", **kwargs: object) -> None:
        # Ensure string representation uses [CONNECTION_ERROR] as tests expect
        super().__init__(
            message,
            error_code="FLEXT_CONNECTION_ERROR",
            context=kwargs or {},
        )


class FlextOracleWmsProcessingError(FlextProcessingError):
    """Oracle WMS processing error with comprehensive operation context.

    Specialized processing error for Oracle WMS business logic and data
    processing operations. Provides detailed context about processing
    failures and business rule violations.
    """


class FlextOracleWmsAuthenticationError(FlextAuthenticationError):
    """Oracle WMS authentication error with comprehensive auth context.

    Specialized authentication error for Oracle WMS authentication and
    authorization failures. Provides detailed context about auth issues.
    """


class FlextOracleWmsTimeoutError(FlextTimeoutError):
    """Oracle WMS timeout error with comprehensive deadline context.

    Specialized timeout error for Oracle WMS operation deadline violations.
    Provides detailed context about timeout conditions and API call timing.
    """


# =============================================================================
# DOMAIN-SPECIFIC EXCEPTIONS - Oracle WMS Business Logic
# =============================================================================


class FlextOracleWmsDataValidationError(FlextOracleWmsValidationError):
    """Data validation error for Oracle WMS operations."""

    def __init__(self, message: str = "Oracle WMS data validation failed") -> None:
        """Initialize data validation error."""
        super().__init__(message)


class FlextOracleWmsApiError(FlextOracleWmsError):
    """Oracle WMS API request and response errors with HTTP context."""

    def __init__(
        self,
        message: str = "Oracle WMS API error",
        *,
        status_code: int | None = None,
        response_body: str | None = None,
        entity_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize API error with HTTP context."""
        context = dict(kwargs)
        if status_code is not None:
            context["status_code"] = status_code
        if response_body is not None:
            context["response_body"] = response_body[:500]  # Truncate for safety
        if entity_name is not None:
            context["entity_name"] = entity_name

        # Preserve expected string representation code and message
        super().__init__(message, context=context, error_code="FLEXT_OPERATION_ERROR")


class FlextOracleWmsInventoryError(FlextOracleWmsProcessingError):
    """Oracle WMS inventory-specific errors with WMS context."""

    def __init__(
        self,
        message: str = "Oracle WMS inventory error",
        *,
        inventory_id: str | None = None,
        location_id: str | None = None,
        item_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize inventory error with WMS context."""
        context = dict(kwargs)
        if inventory_id is not None:
            context["inventory_id"] = inventory_id
        if location_id is not None:
            context["location_id"] = location_id
        if item_id is not None:
            context["item_id"] = item_id

        super().__init__(f"Inventory: {message}", context=context)


class FlextOracleWmsShipmentError(FlextOracleWmsProcessingError):
    """Oracle WMS shipment-specific errors with WMS context."""

    def __init__(
        self,
        message: str = "Oracle WMS shipment error",
        *,
        shipment_id: str | None = None,
        order_id: str | None = None,
        carrier_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize shipment error with WMS context."""
        context = dict(kwargs)
        if shipment_id is not None:
            context["shipment_id"] = shipment_id
        if order_id is not None:
            context["order_id"] = order_id
        if carrier_id is not None:
            context["carrier_id"] = carrier_id

        super().__init__(f"Shipment: {message}", context=context)


class FlextOracleWmsPickingError(FlextOracleWmsProcessingError):
    """Oracle WMS picking-specific errors with WMS context."""

    def __init__(
        self,
        message: str = "Oracle WMS picking error",
        *,
        pick_id: str | None = None,
        wave_id: str | None = None,
        task_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize picking error with WMS context."""
        context = dict(kwargs)
        if pick_id is not None:
            context["pick_id"] = pick_id
        if wave_id is not None:
            context["wave_id"] = wave_id
        if task_id is not None:
            context["task_id"] = task_id

        super().__init__(f"Picking: {message}", context=context)


class FlextOracleWmsEntityNotFoundError(FlextOracleWmsValidationError):
    """Oracle WMS entity not found errors with entity context."""

    def __init__(
        self,
        message: str = "Oracle WMS entity not found",
        *,
        entity_name: str | None = None,
        entity_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize entity not found error with context."""
        context = dict(kwargs)
        if entity_name is not None:
            context["entity_name"] = entity_name
        if entity_id is not None:
            context["entity_id"] = entity_id

        super().__init__(f"Entity Not Found: {message}", context=context)


class FlextOracleWmsSchemaError(FlextOracleWmsValidationError):
    """Oracle WMS schema processing errors with schema context."""

    def __init__(
        self,
        message: str = "Oracle WMS schema error",
        *,
        schema_name: str | None = None,
        field_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize schema error with context."""
        context = dict(kwargs)
        if schema_name is not None:
            context["schema_name"] = schema_name
        if field_name is not None:
            context["field_name"] = field_name

        # Tests expect "[SCHEMA_ERROR] Schema error" (no "Schema:" prefix)
        super().__init__(message, context=context)


class FlextOracleWmsSchemaFlatteningError(FlextOracleWmsSchemaError):
    """Schema flattening error for Oracle WMS nested data processing."""

    def __init__(self, message: str = "Oracle WMS schema flattening failed") -> None:
        """Initialize schema flattening error."""
        super().__init__(message)


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    # Domain-specific exceptions
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsEntityNotFoundError",
    # Factory-created base exceptions
    "FlextOracleWmsError",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsValidationError",
]
