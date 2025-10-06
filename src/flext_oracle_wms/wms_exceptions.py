"""FLEXT Oracle WMS Exceptions - Namespace Class Pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

Enterprise-grade exception hierarchy for Oracle WMS operations consolidated into
a single namespace class following FLEXT patterns. All exceptions are nested within
FlextOracleWmsExceptions for unified access and type safety.
"""

from __future__ import annotations

import contextlib
from typing import override

from flext_core import FlextExceptions

from flext_oracle_wms.typings import FlextOracleWmsTypes


class FlextOracleWmsExceptions(FlextExceptions):
    """Namespace class for all Oracle WMS exceptions following FLEXT patterns.

    All Oracle WMS exception types are nested within this single unified class.
    This follows the FLEXT namespace class pattern for clean imports and organization.
    """

    class BaseError(FlextExceptions.BaseError):
        """Base exception for all Oracle WMS operations.

        Propagates context attributes (like entity_name) to support tests that
        access them directly on the exception instance.
        """

        def _extract_common_kwargs(
            self, kwargs: dict[str, object]
        ) -> tuple[dict[str, object], str | None, str | None]:
            """Extract common kwargs used by all exception types.

            Args:
                kwargs: Keyword arguments passed to exception

            Returns:
                Tuple of (base_context, correlation_id, error_code)

            """
            # Extract known common parameters
            base_context = (
                kwargs.get("context", {})
                if isinstance(kwargs.get("context"), dict)
                else {}
            )
            correlation_id = kwargs.get("correlation_id")
            error_code = kwargs.get("error_code")

            # Remove extracted keys from kwargs to avoid duplication
            for key in ["context", "correlation_id", "error_code"]:
                kwargs.pop(key, None)

            return base_context, correlation_id, error_code

        def _build_context(
            self, base_context: dict[str, object], **kwargs: object
        ) -> dict[str, object]:
            """Build complete context dictionary from base context and additional fields.

            Args:
                base_context: Base context dictionary
                **kwargs: Additional context fields

            Returns:
                Complete context dictionary

            """
            context = dict(base_context)  # Copy base context
            # Add non-None kwargs to context
            context.update({
                key: value for key, value in kwargs.items() if value is not None
            })
            return context

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

    @override
    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
        entity_name: str | None = None,
        field_name: str | None = None,
        invalid_value: object = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle WMS error with context using helpers.

        Args:
            message: Error message
            field: Field name for validation errors
            entity_name: Entity name for entity-related errors
            field_name: Alternative field name parameter
            invalid_value: Invalid value that caused the error
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Store WMS-specific attributes before extracting common kwargs
        self.field = field
        self.entity_name = entity_name
        self.field_name = field_name
        self.invalid_value = invalid_value

        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with WMS-specific fields
        context = self._build_context(
            base_context,
            field=field,
            entity_name=entity_name,
            field_name=field_name,
            invalid_value=invalid_value,
        )

        # Call parent with complete error information
        super().__init__(
            message,
            code=error_code or "WMS_ERROR",
            context=context,
            correlation_id=correlation_id,
        )

        # Initialize declared attributes to None
        self.retry_count = None
        self.auth_method = None
        self.retry_after_seconds = None
        self.status_code = None
        self.response_body = None

        # Attach context keys as attributes for convenient access in tests
        for key, value in context.items():
            with contextlib.suppress(Exception):
                setattr(self, key, value)

    class ValidationError(BaseError):
        """Oracle WMS validation error with comprehensive field context.

        Specialized validation error for Oracle WMS entity and configuration
        validation failures. Provides detailed context about validation failures
        including field names, validation rules, and error details.
        """

        @override
        def __init__(
            self,
            message: str = "Validation failed",
            *,
            field_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize validation error with context using helpers.

            Args:
                message: Error message
                field_name: Name of the field that failed validation
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with validation-specific fields
            context = self._build_context(
                base_context,
                field_name=field_name,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                field_name=field_name,
                code=error_code or "WMS_VALIDATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ConfigurationError(BaseError):
        """Oracle WMS configuration error with comprehensive configuration context.

        Specialized configuration error for Oracle WMS setup and configuration
        validation failures. Provides detailed context about configuration issues.
        """

        @override
        def __init__(
            self,
            message: str = "Config error",
            *,
            config_key: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize configuration error using helpers.

            Args:
                message: Error message
                config_key: Configuration key that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with configuration-specific fields
            context = self._build_context(
                base_context,
                config_key=config_key,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WMS_CONFIG_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

            # Store config_key for backward compatibility
            self.config_key: str = str(config_key or "")

    class WmsConnectionError(BaseError):
        """Oracle WMS connection error with comprehensive network context.

        Specialized connection error for Oracle WMS network communication failures.
        Provides detailed context about connection issues including API endpoints,
        network conditions, and error details.
        """

        @override
        def __init__(
            self,
            message: str = "Connection failed",
            *,
            retry_count: int | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize connection error using helpers.

            Args:
                message: Error message
                retry_count: Number of retry attempts made
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store retry_count before extracting common kwargs
            self.retry_count = retry_count

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with connection-specific fields
            context = self._build_context(
                base_context,
                retry_count=retry_count,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WMS_CONNECTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ProcessingError(BaseError):
        """Oracle WMS processing error with comprehensive operation context.

        Specialized processing error for Oracle WMS business logic and data
        processing operations. Provides detailed context about processing
        failures and business rule violations.
        """

        @override
        def __init__(
            self,
            message: str = "Processing failed",
            *,
            retry_after_seconds: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize processing error with context using helpers.

            Args:
                message: Error message
                retry_after_seconds: Suggested retry delay in seconds
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store retry_after_seconds before extracting common kwargs
            self.retry_after_seconds = retry_after_seconds

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with processing-specific fields
            context = self._build_context(
                base_context,
                retry_after_seconds=retry_after_seconds,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WMS_PROCESSING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class AuthenticationError(BaseError):
        """Oracle WMS authentication error with comprehensive auth context.

        Specialized authentication error for Oracle WMS authentication and
        authorization failures. Provides detailed context about auth issues.
        """

        @override
        def __init__(
            self,
            message: str = "Authentication failed",
            *,
            auth_method: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize authentication error with context using helpers.

            Args:
                message: Error message
                auth_method: Authentication method that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store auth_method before extracting common kwargs
            self.auth_method = auth_method

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with authentication-specific fields
            context = self._build_context(
                base_context,
                auth_method=auth_method,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WMS_AUTH_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class WmsTimeoutError(BaseError):
        """Oracle WMS timeout error with comprehensive deadline context.

        Specialized timeout error for Oracle WMS operation deadline violations.
        Provides detailed context about timeout conditions and API call timing.
        """

    class DataValidationError(ValidationError):
        """Data validation error for Oracle WMS operations."""

        @override
        def __init__(
            self,
            message: str = "Oracle WMS data validation failed",
            **kwargs: object,
        ) -> None:
            """Initialize data validation error using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "WMS_DATA_VALIDATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )


class FlextOracleWmsApiError(FlextOracleWmsExceptions.BaseError):
    """Oracle WMS API request and response errors with HTTP context."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS API error",
        *,
        status_code: int | None = None,
        response_body: str | None = None,
        entity_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize API error with HTTP context using helpers.

        Args:
            message: Error message
            status_code: HTTP status code
            response_body: HTTP response body (truncated)
            entity_name: WMS entity name
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Store HTTP-specific attributes before extracting common kwargs
        self.status_code = status_code
        self.response_body = response_body[:500] if response_body else None
        self.entity_name = entity_name

        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with API-specific fields
        context = self._build_context(
            base_context,
            status_code=status_code,
            response_body=self.response_body,
            entity_name=entity_name,
        )

        # Call parent with complete error information
        super().__init__(
            message,
            entity_name=entity_name,
            code=error_code or "WMS_API_ERROR",
            context=context,
            correlation_id=correlation_id,
        )


class FlextOracleWmsInventoryError(FlextOracleWmsExceptions.ProcessingError):
    """Oracle WMS inventory-specific errors with WMS context."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS inventory error",
        *,
        inventory_id: str | None = None,
        location_id: str | None = None,
        item_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize inventory error with WMS context using helpers.

        Args:
            message: Error message
            inventory_id: Inventory identifier
            location_id: Location identifier
            item_id: Item identifier
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with inventory-specific fields
        context = self._build_context(
            base_context,
            inventory_id=inventory_id,
            location_id=location_id,
            item_id=item_id,
        )

        # Call parent with complete error information
        super().__init__(
            f"Inventory: {message}",
            code=error_code or "WMS_INVENTORY_ERROR",
            context=context,
            correlation_id=correlation_id,
        )


class FlextOracleWmsShipmentError(FlextOracleWmsExceptions.ProcessingError):
    """Oracle WMS shipment-specific errors with WMS context."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS shipment error",
        *,
        shipment_id: str | None = None,
        order_id: str | None = None,
        carrier_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize shipment error with WMS context using helpers.

        Args:
            message: Error message
            shipment_id: Shipment identifier
            order_id: Order identifier
            carrier_id: Carrier identifier
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with shipment-specific fields
        context = self._build_context(
            base_context,
            shipment_id=shipment_id,
            order_id=order_id,
            carrier_id=carrier_id,
        )

        # Call parent with complete error information
        super().__init__(
            f"Shipment: {message}",
            code=error_code or "WMS_SHIPMENT_ERROR",
            context=context,
            correlation_id=correlation_id,
        )


class FlextOracleWmsPickingError(FlextOracleWmsExceptions.ProcessingError):
    """Oracle WMS picking-specific errors with WMS context."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS picking error",
        *,
        pick_id: str | None = None,
        wave_id: str | None = None,
        task_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize picking error with WMS context using helpers.

        Args:
            message: Error message
            pick_id: Picking identifier
            wave_id: Wave identifier
            task_id: Task identifier
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with picking-specific fields
        context = self._build_context(
            base_context,
            pick_id=pick_id,
            wave_id=wave_id,
            task_id=task_id,
        )

        # Call parent with complete error information
        super().__init__(
            f"Picking: {message}",
            code=error_code or "WMS_PICKING_ERROR",
            context=context,
            correlation_id=correlation_id,
        )


class FlextOracleWmsEntityNotFoundError(FlextOracleWmsExceptions.ValidationError):
    """Oracle WMS entity not found errors with entity context."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS entity not found",
        *,
        entity_name: str | None = None,
        entity_id: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize entity not found error with context using helpers.

        Args:
            message: Error message
            entity_name: Entity name
            entity_id: Entity identifier
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with entity-specific fields
        context = self._build_context(
            base_context,
            entity_name=entity_name,
            entity_id=entity_id,
        )

        # Call parent with complete error information
        super().__init__(
            f"Entity Not Found: {message}",
            code=error_code or "WMS_ENTITY_NOT_FOUND",
            context=context,
            correlation_id=correlation_id,
        )


class FlextOracleWmsSchemaError(FlextOracleWmsExceptions.ValidationError):
    """Oracle WMS schema processing errors with schema context."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS schema error",
        *,
        schema_name: str | None = None,
        field_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize schema error with context using helpers.

        Args:
            message: Error message
            schema_name: Schema name
            field_name: Field name
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context with schema-specific fields
        context = self._build_context(
            base_context,
            schema_name=schema_name,
            field_name=field_name,
        )

        # Call parent with complete error information
        # Tests expect "[SCHEMA_ERROR] Schema error" (no "Schema:" prefix)
        super().__init__(
            message,
            field_name=field_name,
            code=error_code or "WMS_SCHEMA_ERROR",
            context=context,
            correlation_id=correlation_id,
        )


class FlextOracleWmsSchemaFlatteningError(FlextOracleWmsSchemaError):
    """Schema flattening error for Oracle WMS nested data processing."""

    @override
    def __init__(
        self,
        message: str = "Oracle WMS schema flattening failed",
        **kwargs: object,
    ) -> None:
        """Initialize schema flattening error using helpers.

        Args:
            message: Error message
            **kwargs: Additional context (context, correlation_id, error_code)

        """
        # Extract common parameters using helper
        base_context, correlation_id, error_code = self._extract_common_kwargs(kwargs)

        # Build context
        context = self._build_context(base_context)

        # Call parent with complete error information
        super().__init__(
            message,
            code=error_code or "WMS_SCHEMA_FLATTENING_ERROR",
            context=context,
            correlation_id=correlation_id,
        )


__all__: FlextOracleWmsTypes.Core.StringList = [
    "FlextOracleWmsApiError",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsExceptions",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
]
