"""Oracle WMS exception classes using flext-core standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise-grade exception hierarchy for Oracle WMS operations.
"""

from __future__ import annotations

# Import from flext-core root namespace as required
from flext_core import (
    FlextError,
)


class FlextOracleWmsError(FlextError):
    """Base exception for Oracle WMS operations using flext-core standards."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        entity_name: str | None = None,
        details: dict[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS error with enhanced metadata.

        Args:
            message: Human-readable error message
            error_code: Oracle WMS specific error code
            entity_name: WMS entity associated with error
            details: Additional error context

        """
        super().__init__(message, error_code=error_code, context=details or {})
        self.entity_name = entity_name
        self._details = details or {}

    @property
    def details(self) -> dict[str, object]:
        """Get error details/context."""
        return self._details


class FlextOracleWmsAuthenticationError(FlextOracleWmsError):
    """Oracle WMS authentication and authorization errors."""

    def __init__(
        self,
        message: str = "Oracle WMS authentication failed",
        auth_method: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize authentication error.

        Args:
            message: Authentication error message
            auth_method: Authentication method that failed
            **kwargs: Additional error context

        """
        # Extract details from kwargs for parent class with proper typing
        details_raw = kwargs.pop("details", None)
        details = details_raw if isinstance(details_raw, dict) else None
        super().__init__(message, error_code="AUTH_ERROR", details=details)
        self.auth_method = auth_method


class FlextOracleWmsApiError(FlextOracleWmsError):
    """Oracle WMS API request and response errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize API error.

        Args:
            message: API error message
            status_code: HTTP status code
            response_body: Raw response body
            **kwargs: Additional error context

        """
        # Extract known parameters for parent class with proper typing
        entity_name_raw = kwargs.pop("entity_name", None)
        entity_name = entity_name_raw if isinstance(entity_name_raw, str) else None

        details_raw = kwargs.pop("details", None)
        details: dict[str, object] | None = None
        if isinstance(details_raw, dict):
            details = details_raw
        elif kwargs:  # Add remaining kwargs to details
            details = dict(kwargs.items())

        super().__init__(
            message,
            error_code="API_ERROR",
            entity_name=entity_name,
            details=details,
        )
        self.status_code = status_code
        self.response_body = response_body


class FlextOracleWmsConnectionError(FlextOracleWmsError):
    """Oracle WMS connection and network errors."""

    def __init__(
        self,
        message: str = "Oracle WMS connection failed",
        retry_count: int = 0,
        **kwargs: object,
    ) -> None:
        """Initialize connection error.

        Args:
            message: Connection error message
            retry_count: Number of retry attempts made
            **kwargs: Additional error context

        """
        # Extract details from kwargs for parent class with proper typing
        details_raw = kwargs.pop("details", None)
        details = details_raw if isinstance(details_raw, dict) else None
        super().__init__(message, error_code="CONNECTION_ERROR", details=details)
        self.retry_count = retry_count


class FlextOracleWmsDataValidationError(FlextOracleWmsError):
    """Oracle WMS data validation and schema errors."""

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        invalid_value: object = None,
        **kwargs: object,
    ) -> None:
        """Initialize data validation error.

        Args:
            message: Validation error message
            field_name: Field that failed validation
            invalid_value: Value that failed validation
            **kwargs: Additional error context

        """
        # Extract entity_name and details from kwargs for parent class
        entity_name_raw = kwargs.pop("entity_name", None)
        entity_name = entity_name_raw if isinstance(entity_name_raw, str) else None
        details_raw = kwargs.pop("details", None)
        details = details_raw if isinstance(details_raw, dict) else None
        super().__init__(
            message,
            error_code="VALIDATION_ERROR",
            entity_name=entity_name,
            details=details,
        )
        self.field_name = field_name
        self.invalid_value = invalid_value


class FlextOracleWmsConfigurationError(FlextOracleWmsError):
    """Oracle WMS configuration and setup errors."""

    def __init__(
        self,
        message: str,
        config_key: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize configuration error.

        Args:
            message: Configuration error message
            config_key: Configuration key that caused error
            **kwargs: Additional error context

        """
        # Extract details from kwargs for parent class with proper typing
        details_raw = kwargs.pop("details", None)
        details = details_raw if isinstance(details_raw, dict) else None
        super().__init__(message, error_code="CONFIG_ERROR", details=details)
        self.config_key = config_key


class FlextOracleWmsEntityNotFoundError(FlextOracleWmsError):
    """Oracle WMS entity not found errors."""

    def __init__(
        self,
        entity_name: str,
        message: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize entity not found error.

        Args:
            entity_name: WMS entity that was not found
            message: Custom error message
            **kwargs: Additional error context

        """
        message = message or f"Oracle WMS entity '{entity_name}' not found"
        # Extract details from kwargs for parent class with proper typing
        details_raw = kwargs.pop("details", None)
        details = details_raw if isinstance(details_raw, dict) else None
        super().__init__(
            message, error_code="NOT_FOUND", entity_name=entity_name, details=details
        )


class FlextOracleWmsRateLimitError(FlextOracleWmsError):
    """Oracle WMS rate limiting errors."""

    def __init__(
        self,
        message: str = "Oracle WMS API rate limit exceeded",
        retry_after_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Rate limit error message
            retry_after_seconds: Seconds to wait before retry
            **kwargs: Additional error context

        """
        # Extract known parameters for parent class with proper typing
        entity_name_raw = kwargs.pop("entity_name", None)
        entity_name = entity_name_raw if isinstance(entity_name_raw, str) else None

        details_raw = kwargs.pop("details", None)
        details: dict[str, object] | None = None
        if isinstance(details_raw, dict):
            details = details_raw
        elif kwargs:  # Add remaining kwargs to details
            details = dict(kwargs.items())

        super().__init__(
            message,
            error_code="RATE_LIMIT_EXCEEDED",
            entity_name=entity_name,
            details=details,
        )
        self.retry_after_seconds = retry_after_seconds


class FlextOracleWmsSchemaFlatteningError(FlextOracleWmsError):
    """Oracle WMS schema flattening/deflattening errors."""

    def __init__(
        self,
        message: str,
        schema_operation: str,
        depth_level: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize schema flattening error.

        Args:
            message: Schema operation error message
            schema_operation: Operation that failed (flatten/deflatten)
            depth_level: Schema depth where error occurred
            **kwargs: Additional error context

        """
        # Extract known parameters for parent class with proper typing
        entity_name_raw = kwargs.pop("entity_name", None)
        entity_name = entity_name_raw if isinstance(entity_name_raw, str) else None

        details_raw = kwargs.pop("details", None)
        details: dict[str, object] | None = None
        if isinstance(details_raw, dict):
            details = details_raw
        elif kwargs:  # Add remaining kwargs to details
            details = dict(kwargs.items())

        super().__init__(
            message,
            error_code="SCHEMA_PROCESSING_ERROR",
            entity_name=entity_name,
            details=details,
        )
        self.schema_operation = schema_operation
        self.depth_level = depth_level


class FlextOracleWmsFilterError(FlextOracleWmsError):
    """Oracle WMS filtering and query errors."""

    def __init__(
        self,
        message: str,
        filter_type: str | None = None,
        filter_value: object = None,
        **kwargs: object,
    ) -> None:
        """Initialize filter error.

        Args:
            message: Filter error message
            filter_type: Type of filter that failed
            filter_value: Filter value that caused error
            **kwargs: Additional error context

        """
        # Extract known parameters for parent class with proper typing
        entity_name_raw = kwargs.pop("entity_name", None)
        entity_name = entity_name_raw if isinstance(entity_name_raw, str) else None

        details_raw = kwargs.pop("details", None)
        details: dict[str, object] | None = None
        if isinstance(details_raw, dict):
            details = details_raw
        elif kwargs:  # Add remaining kwargs to details
            details = dict(kwargs.items())

        super().__init__(
            message,
            error_code="FILTER_ERROR",
            entity_name=entity_name,
            details=details,
        )
        self.filter_type = filter_type
        self.filter_value = filter_value


class FlextOracleWmsSchemaError(FlextOracleWmsError):
    """Oracle WMS schema definition and validation errors."""

    def __init__(
        self,
        message: str,
        schema_name: str | None = None,
        validation_details: dict[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize schema error.

        Args:
            message: Schema error message
            schema_name: Schema name that caused error
            validation_details: Schema validation details
            **kwargs: Additional error context

        """
        # Extract known parameters for parent class with proper typing
        entity_name_raw = kwargs.pop("entity_name", None)
        entity_name = entity_name_raw if isinstance(entity_name_raw, str) else None

        details_raw = kwargs.pop("details", None)
        details: dict[str, object] | None = None
        if isinstance(details_raw, dict):
            details = details_raw
        elif kwargs:  # Add remaining kwargs to details
            details = dict(kwargs.items())

        super().__init__(
            message,
            error_code="SCHEMA_ERROR",
            entity_name=entity_name,
            details=details,
        )
        self.schema_name = schema_name
        self.validation_details = validation_details or {}
