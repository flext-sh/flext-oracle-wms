"""Oracle WMS Exceptions - Consolidated Exception Hierarchy.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

Enterprise-grade exception hierarchy for Oracle WMS operations with explicit
class definitions for type safety. This module consolidates all Oracle WMS-specific
exceptions into a single coherent hierarchy compatible with MyPy static analysis.
"""

from __future__ import annotations

import contextlib

from flext_core import FlextExceptions, FlextTypes


class FlextOracleWmsError(FlextExceptions.BaseError):
    """Base exception for all Oracle WMS operations.

    Propagates context attributes (like entity_name) to support tests that
    access them directly on the exception instance.
    """

    # Declare attributes that may be dynamically set for MyPy
    field: str | None
    entity_name: str | None
    field_name: str | None
    invalid_value: object
    retry_count: int | None
    auth_method: str | None
    retry_after_seconds: float | None
    status_code: int | None
    response_body: str | None

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        context: FlextTypes.Core.Dict | None = None,
        field: str | None = None,
        entity_name: str | None = None,
        field_name: str | None = None,
        invalid_value: object = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle WMS error with context.

        Args:
            message: Error message
            code: Optional error code
            context: Optional context dictionary
            field: Field name for validation errors
            entity_name: Entity name for entity-related errors
            field_name: Alternative field name parameter
            invalid_value: Invalid value that caused the error
            **kwargs: Additional context parameters

        """
        full_context = dict(context or {})
        full_context.update(kwargs)

        # Add specific attributes to context
        if field is not None:
            full_context["field"] = field
        if entity_name is not None:
            full_context["entity_name"] = entity_name
        if field_name is not None:
            full_context["field_name"] = field_name
        if invalid_value is not None:
            full_context["invalid_value"] = invalid_value

        super().__init__(message, code=code, context=full_context)

        # Initialize declared attributes to None
        self.field = None
        self.entity_name = None
        self.field_name = None
        self.invalid_value = None
        self.retry_count = None
        self.auth_method = None
        self.retry_after_seconds = None
        self.status_code = None
        self.response_body = None

        # Attach context keys as attributes for convenient access in tests
        for key, value in full_context.items():
            with contextlib.suppress(Exception):
                setattr(self, key, value)


class FlextOracleWmsValidationError(FlextOracleWmsError):
    """Oracle WMS validation error with comprehensive field context.

    Specialized validation error for Oracle WMS entity and configuration
    validation failures. Provides detailed context about validation failures
    including field names, validation rules, and error details.
    """

    def __init__(
        self,
        message: str = "Validation failed",
        *,
        field_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize validation error with context.

        Args:
            message: Error message
            field_name: Name of the field that failed validation
            **kwargs: Additional context parameters

        """
        context = dict(kwargs)
        if field_name is not None:
            context["field_name"] = field_name

        super().__init__(message, context=context)


class FlextOracleWmsConfigurationError(FlextOracleWmsError):
    """Oracle WMS configuration error with comprehensive configuration context.

    Specialized configuration error for Oracle WMS setup and configuration
    validation failures. Provides detailed context about configuration issues.
    """

    def __init__(self, message: str = "Config error", **kwargs: object) -> None:
        """Initialize configuration error.

        Args:
            message: Error message
            **kwargs: Additional context parameters

        """
        super().__init__(message, context=kwargs or {})
        # Extract config_key from context for backward compatibility
        context = kwargs.get("context", {})
        if isinstance(context, dict):
            self.config_key = context.get("config_key", "")
        else:
            self.config_key = kwargs.get("config_key", "")


class FlextOracleWmsConnectionError(FlextOracleWmsError):
    """Oracle WMS connection error with comprehensive network context.

    Specialized connection error for Oracle WMS network communication failures.
    Provides detailed context about connection issues including API endpoints,
    network conditions, and error details.

    Returns:
            object: Description of return value.

    """

    def __init__(
        self,
        message: str = "Connection failed",
        *,
        retry_count: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize connection error.

        Args:
            message: Error message
            retry_count: Number of retry attempts made
            **kwargs: Additional context parameters

        """
        context = dict(kwargs)
        if retry_count is not None:
            context["retry_count"] = retry_count

        # Ensure string representation uses [CONNECTION_ERROR] as tests expect
        super().__init__(message, context=context)


class FlextOracleWmsProcessingError(FlextOracleWmsError):
    """Oracle WMS processing error with comprehensive operation context.

    Specialized processing error for Oracle WMS business logic and data
    processing operations. Provides detailed context about processing
    failures and business rule violations.

    Returns:
            object: Description of return value.

    """

    def __init__(
        self,
        message: str = "Processing failed",
        *,
        retry_after_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize processing error with context.

        Args:
            message: Error message
            retry_after_seconds: Suggested retry delay in seconds
            **kwargs: Additional context parameters

        """
        context = dict(kwargs)
        if retry_after_seconds is not None:
            context["retry_after_seconds"] = retry_after_seconds

        super().__init__(message, context=context)


class FlextOracleWmsAuthenticationError(FlextOracleWmsError):
    """Oracle WMS authentication error with comprehensive auth context.

    Specialized authentication error for Oracle WMS authentication and
    authorization failures. Provides detailed context about auth issues.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        *,
        auth_method: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize authentication error with context.

        Args:
            message: Error message
            auth_method: Authentication method that failed
            **kwargs: Additional context parameters

        """
        context = dict(kwargs)
        if auth_method is not None:
            context["auth_method"] = auth_method

        super().__init__(message, context=context)


class FlextOracleWmsTimeoutError(FlextOracleWmsError):
    """Oracle WMS timeout error with comprehensive deadline context.

    Specialized timeout error for Oracle WMS operation deadline violations.
    Provides detailed context about timeout conditions and API call timing.
    """


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
        super().__init__(message, context=context)


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


__all__: FlextTypes.Core.StringList = [
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
