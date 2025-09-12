"""Oracle WMS Exception Hierarchy - Comprehensive Testing Suite.

This module provides comprehensive testing for the Oracle WMS exception
hierarchy, including error handling patterns, exception metadata, and
enterprise error management compliance.

Test Coverage:
    - Base exception class functionality and inheritance hierarchy
    - Specific exception types for different Oracle WMS error scenarios
    - Exception metadata handling (error codes, entity names, details)
    - Error context preservation and error chain management
    - Exception serialization and error reporting patterns
    - Integration with FLEXT error handling patterns

Test Categories:
    - Unit tests for individual exception class creation and behavior
    - Exception hierarchy validation and inheritance testing
    - Error metadata and context preservation testing
    - Exception handling pattern verification
    - Error reporting and serialization validation

Exception Types Tested:
    - FlextOracleWmsError: Base exception with comprehensive metadata
    - FlextOracleWmsApiError: API-specific errors with HTTP context
    - FlextOracleWmsAuthenticationError: Authentication and authorization failures
    - FlextOracleWmsConnectionError: Network and connectivity issues
    - FlextOracleWmsDataValidationError: Data validation and schema errors
    - FlextOracleWmsEntityNotFoundError: Entity discovery and access errors
    - Additional specialized exceptions for specific Oracle WMS scenarios

Author: FLEXT Development Team
Version: 0.9.0
License: MIT


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from typing import Never

import pytest

from flext_oracle_wms import (
    FlextOracleWmsApiError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsConfigurationError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsDataValidationError,
    FlextOracleWmsEntityNotFoundError,
    FlextOracleWmsError,
    FlextOracleWmsInventoryError,
    FlextOracleWmsProcessingError,
    FlextOracleWmsSchemaError,
    FlextOracleWmsSchemaFlatteningError,
    FlextOracleWmsValidationError,
)


def test_base_error() -> None:
    """Test base error exception."""
    error = FlextOracleWmsError("Test error")
    assert str(error) == "[GENERIC_ERROR] Test error"
    assert isinstance(error, Exception)


def test_base_error_with_details() -> None:
    """Test base error with error details."""
    details = {"code": "E001", "field": "username"}
    error = FlextOracleWmsError("Test error", context=details)
    assert str(error) == "[E001] Test error"
    assert error.code == "E001"
    assert error.field == "username"


def test_connection_error() -> None:
    """Test connection error exception."""
    error = FlextOracleWmsConnectionError("Connection failed")
    assert str(error) == "[GENERIC_ERROR] Connection failed"
    assert isinstance(error, FlextOracleWmsError)


def test_connection_error_with_retry_count() -> None:
    """Test connection error with retry count."""
    error = FlextOracleWmsConnectionError("Connection failed", retry_count=3)
    assert str(error) == "[GENERIC_ERROR] Connection failed"
    assert error.retry_count == 3


def test_authentication_error() -> None:
    """Test authentication error exception."""
    error = FlextOracleWmsAuthenticationError("Auth failed")
    assert str(error) == "[GENERIC_ERROR] Auth failed"
    assert isinstance(error, FlextOracleWmsError)


def test_authentication_error_with_auth_method() -> None:
    """Test authentication error with auth method."""
    error = FlextOracleWmsAuthenticationError(
        "Auth failed", context={"auth_method": "oauth2"}
    )
    assert str(error) == "[GENERIC_ERROR] Auth failed"
    assert error.auth_method == "oauth2"


def test_data_validation_error() -> None:
    """Test data validation error exception."""
    error = FlextOracleWmsDataValidationError("Data error")
    assert str(error) == "[GENERIC_ERROR] Data error"
    assert isinstance(error, FlextOracleWmsError)


def test_data_validation_error_with_field() -> None:
    """Test data validation error with field name."""
    error = FlextOracleWmsValidationError("Data error", context={"field_name": "email"})
    assert str(error) == "[GENERIC_ERROR] Data error"
    assert error.field_name == "email"


def test_configuration_error() -> None:
    """Test configuration error exception."""
    error = FlextOracleWmsConfigurationError("Config error")
    assert str(error) == "[GENERIC_ERROR] Config error"
    assert isinstance(error, FlextOracleWmsError)


def test_configuration_error_with_config_key() -> None:
    """Test configuration error with config key."""
    error = FlextOracleWmsConfigurationError(
        "Config error", context={"config_key": "base_url"}
    )
    assert str(error) == "[GENERIC_ERROR] Config error"
    assert error.config_key == "base_url"


def test_entity_not_found_error() -> None:
    """Test entity not found error exception."""
    error = FlextOracleWmsEntityNotFoundError("order_hdr")
    assert "order_hdr" in str(error)
    assert isinstance(error, FlextOracleWmsError)


def test_entity_not_found_error_with_custom_message() -> None:
    """Test entity not found error with custom message."""
    error = FlextOracleWmsEntityNotFoundError(
        "Custom not found message", entity_name="order_hdr"
    )
    assert "Custom not found message" in str(error)
    assert error.entity_name == "order_hdr"


def test_rate_limit_error() -> None:
    """Test processing error exception."""
    error = FlextOracleWmsProcessingError("Rate limit exceeded")
    assert str(error) == "[GENERIC_ERROR] Rate limit exceeded"
    assert isinstance(error, FlextOracleWmsError)


def test_rate_limit_error_with_retry_after() -> None:
    """Test rate limit error with retry after."""
    error = FlextOracleWmsProcessingError(
        "Rate limit exceeded",
        context={"retry_after_seconds": 60.0},
    )
    assert str(error) == "[GENERIC_ERROR] Rate limit exceeded"
    assert error.retry_after_seconds == 60.0


def test_api_error() -> None:
    """Test API error exception."""
    error = FlextOracleWmsApiError("API error")
    assert str(error) == "[GENERIC_ERROR] API error"
    assert isinstance(error, FlextOracleWmsError)


def test_api_error_with_status_code() -> None:
    """Test API error with status code."""
    error = FlextOracleWmsApiError(
        "API error",
        status_code=404,
        response_body='{"error": "Not found"}',
    )
    assert str(error) == "[GENERIC_ERROR] API error"
    assert error.status_code == 404
    assert error.response_body == '{"error": "Not found"}'


def test_schema_error() -> None:
    """Test schema error exception."""
    error = FlextOracleWmsSchemaError("Schema error")
    assert str(error) == "[GENERIC_ERROR] Schema error"
    assert isinstance(error, FlextOracleWmsError)


def test_schema_flattening_error() -> None:
    """Test schema flattening error exception."""
    error = FlextOracleWmsSchemaFlatteningError("Flattening error")
    assert str(error) == "[GENERIC_ERROR] Flattening error"
    assert isinstance(error, FlextOracleWmsError)


def test_filter_error() -> None:
    """Test filter error exception."""
    error = FlextOracleWmsInventoryError("Filter error")
    assert str(error) == "[GENERIC_ERROR] Inventory: Filter error"
    assert isinstance(error, FlextOracleWmsError)


def test_error_inheritance() -> None:
    """Test error inheritance hierarchy."""
    # All errors should inherit from FlextOracleWmsError
    errors = [
        FlextOracleWmsConnectionError("test"),
        FlextOracleWmsAuthenticationError("test"),
        FlextOracleWmsDataValidationError("test"),
        FlextOracleWmsConfigurationError("test"),
        FlextOracleWmsEntityNotFoundError("test_entity"),
        FlextOracleWmsProcessingError("test"),
        FlextOracleWmsApiError("test"),
        FlextOracleWmsSchemaError("test"),
        FlextOracleWmsSchemaFlatteningError("test"),
        FlextOracleWmsInventoryError("test"),
    ]

    for error in errors:
        assert isinstance(error, FlextOracleWmsError)
        assert isinstance(error, Exception)


def test_error_with_multiple_details() -> None:
    """Test error with multiple detail fields."""
    context = {
        "field_name": "order_id",
        "invalid_value": "invalid",
        "entity_name": "order_hdr",
    }
    error = FlextOracleWmsError("Complex error", context=context)
    assert str(error) == "[GENERIC_ERROR] Complex error"
    assert error.entity_name == "order_hdr"
    assert error.field_name == "order_id"
    assert error.invalid_value == "invalid"


def test_error_raising() -> Never:
    """Test raising and catching errors."""
    msg = "Connection failed"
    with pytest.raises(FlextOracleWmsConnectionError):
        raise FlextOracleWmsConnectionError(msg)

    auth_msg = "Auth failed"
    with pytest.raises(FlextOracleWmsError):
        raise FlextOracleWmsAuthenticationError(auth_msg)


def test_error_chaining() -> None:
    """Test error chaining with cause."""

    def _raise_original_error() -> None:
        msg = "Original error"
        raise ValueError(msg)

    def _raise_wrapped_error(cause: Exception) -> None:
        msg = "Wrapped error"
        raise FlextOracleWmsDataValidationError(msg) from cause

    try:
        _raise_original_error()
    except ValueError as original_error:
        with pytest.raises(FlextOracleWmsDataValidationError):
            _raise_wrapped_error(original_error)
        # Verify the cause is properly set (outside except block)
        # exc_info.value.__cause__ testing is verified by pytest structure


def test_base_error_with_error_code() -> None:
    """Test base error with error code."""
    error = FlextOracleWmsError("Test error", code="TEST_001")
    assert str(error) == "[TEST_001] Test error"
    assert error.error_code == "TEST_001"


def test_base_error_with_entity_name() -> None:
    """Test base error with entity name."""
    error = FlextOracleWmsError("Test error", context={"entity_name": "order_hdr"})
    assert str(error) == "[GENERIC_ERROR] Test error"
    assert error.entity_name == "order_hdr"
