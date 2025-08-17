"""Oracle WMS Helper Functions - Comprehensive Testing Suite.

This module provides comprehensive testing for Oracle WMS utility functions
and helper methods, including URL processing, data validation, pagination
handling, and enterprise utility operations.

Test Coverage:
    - URL construction and normalization testing for Oracle WMS endpoints
    - Data validation functions with comprehensive error scenario testing
    - Pagination information extraction and processing validation
    - Timestamp formatting and date handling utility testing
    - Record batching and chunking operations for performance optimization
    - Exception handling and error management utility testing

Test Categories:
    - Unit tests for individual helper function operations
    - Validation tests for data integrity and type checking
    - URL processing tests for Oracle WMS endpoint construction
    - Error handling tests for comprehensive exception scenarios
    - Performance tests for batch processing and optimization utilities

Helper Functions Tested:
    - flext_oracle_wms_build_entity_url: Oracle WMS entity URL construction
    - flext_oracle_wms_chunk_records: Record batching for performance
    - flext_oracle_wms_extract_environment_from_url: Environment detection
    - flext_oracle_wms_extract_pagination_info: Pagination data processing
    - flext_oracle_wms_format_timestamp: Date and time formatting utilities
    - flext_oracle_wms_normalize_url: URL standardization and validation
    - flext_oracle_wms_validate_api_response: API response validation
    - Additional specialized helper functions for Oracle WMS operations

Author: FLEXT Development Team
Version: 0.9.0
License: MIT
"""

import pytest

from flext_oracle_wms import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsDefaults,
    FlextOracleWmsError,
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
    handle_operation_exception,
    validate_dict_parameter,
    validate_records_list,
    validate_string_parameter,
)


def test_validate_entity_name() -> None:
    """Test entity name validation."""
    # Test valid entity name
    result = flext_oracle_wms_validate_entity_name("order_hdr")
    assert result.success
    assert result.data == "order_hdr"

    # Test entity name with uppercase (should be normalized)
    result = flext_oracle_wms_validate_entity_name("ORDER_HDR")
    assert result.success
    assert result.data == "order_hdr"

    # Test invalid entity name (empty)
    result = flext_oracle_wms_validate_entity_name("")
    assert result.is_failure
    assert "cannot be empty" in result.error


def test_normalize_url() -> None:
    """Test URL normalization."""
    # Test basic URL joining
    result = flext_oracle_wms_normalize_url("https://test.example.com", "api/orders")
    assert result == "https://test.example.com/api/orders"

    # Test URL with trailing slash
    result = flext_oracle_wms_normalize_url("https://test.example.com/", "/api/orders")
    assert result == "https://test.example.com/api/orders"

    # Test empty base URL
    with pytest.raises(FlextOracleWmsError):
        flext_oracle_wms_normalize_url("", "api/orders")


def test_build_entity_url() -> None:
    """Test entity URL building."""
    result = flext_oracle_wms_build_entity_url(
        "https://test.example.com",
        "prod",
        "order_hdr",
    )
    expected = "https://test.example.com/prod/wms/lgfapi/v10/entity/order_hdr/"
    assert result == expected

    # Test with custom API version
    result = flext_oracle_wms_build_entity_url(
        "https://test.example.com",
        "test",
        "item_master",
        "v2",
    )
    expected = "https://test.example.com/test/wms/lgfapi/v2/entity/item_master/"
    assert result == expected


def test_extract_environment_from_url() -> None:
    """Test environment extraction from URL."""
    # Test URL with environment
    url = "https://test.example.com/prod/wms/lgfapi/v1"
    result = flext_oracle_wms_extract_environment_from_url(url)
    assert result == "prod"

    # Test URL without environment (should return default)
    url = "https://test.example.com"
    result = flext_oracle_wms_extract_environment_from_url(url)
    assert result == FlextOracleWmsDefaults.DEFAULT_ENVIRONMENT

    # Test empty URL
    with pytest.raises(FlextOracleWmsError):
        flext_oracle_wms_extract_environment_from_url("")


def test_extract_pagination_info() -> None:
    """Test pagination info extraction."""
    response_data = {
        "page_nbr": 2,
        "page_count": 10,
        "result_count": 250,
        "next_page": "https://api.example.com/next",
        "previous_page": "https://api.example.com/prev",
    }

    result = flext_oracle_wms_extract_pagination_info(response_data)

    assert result["current_page"] == 2
    assert result["total_pages"] == 10
    assert result["total_results"] == 250
    assert result["has_next"] is True
    assert result["has_previous"] is True
    assert result["next_url"] == "https://api.example.com/next"
    assert result["previous_url"] == "https://api.example.com/prev"


def test_validate_api_response() -> None:
    """Test API response validation."""
    # Test successful response
    good_response = {"data": [{"id": 1, "name": "test"}], "status": "success"}
    result = flext_oracle_wms_validate_api_response(good_response)
    assert result.success

    # Test response with error
    error_response = {"error": "Invalid request"}
    result = flext_oracle_wms_validate_api_response(error_response)
    assert result.is_failure
    assert "API error" in result.error

    # Test response with error message
    error_message_response = {"message": "Error occurred during processing"}
    result = flext_oracle_wms_validate_api_response(error_message_response)
    assert result.is_failure
    assert "API error" in result.error


def test_format_timestamp() -> None:
    """Test timestamp formatting."""
    # Test with provided timestamp
    result = flext_oracle_wms_format_timestamp("2025-01-01T12:00:00Z")
    assert result == "2025-01-01T12:00:00Z"

    # Test with None (should return current timestamp)
    result = flext_oracle_wms_format_timestamp(None)
    assert isinstance(result, str)
    assert "T" in result  # ISO format

    # Test with empty string
    result = flext_oracle_wms_format_timestamp("")
    assert isinstance(result, str)
    assert "T" in result  # Should fallback to current time


def test_chunk_records() -> None:
    """Test record chunking."""
    records = [{"id": i, "name": f"record_{i}"} for i in range(10)]

    # Test with default chunk size
    chunks = flext_oracle_wms_chunk_records(records, 3)
    assert len(chunks) == 4  # 10 records / 3 = 3 full chunks + 1 partial
    assert len(chunks[0]) == 3
    assert len(chunks[1]) == 3
    assert len(chunks[2]) == 3
    assert len(chunks[3]) == 1

    # Test with invalid chunk size
    with pytest.raises(FlextOracleWmsError):
        flext_oracle_wms_chunk_records(records, 0)

    # Test with non-list input
    with pytest.raises(FlextOracleWmsError):
        flext_oracle_wms_chunk_records("not a list", 3)


def test_validation_functions() -> None:
    """Test DRY validation functions."""
    # Test validate_records_list
    valid_records = [{"id": 1}, {"id": 2}]
    validate_records_list(valid_records)  # Should not raise

    with pytest.raises(FlextOracleWmsDataValidationError):
        validate_records_list("not a list")

    # Test validate_dict_parameter
    valid_dict = {"key": "value"}
    validate_dict_parameter(valid_dict, "test_param")  # Should not raise

    with pytest.raises(FlextOracleWmsDataValidationError):
        validate_dict_parameter("not a dict", "test_param")

    # Test validate_string_parameter
    validate_string_parameter("valid string", "test_param")  # Should not raise

    with pytest.raises(FlextOracleWmsDataValidationError):
        validate_string_parameter(123, "test_param")

    with pytest.raises(FlextOracleWmsDataValidationError):
        validate_string_parameter("", "test_param", allow_empty=False)


def test_handle_operation_exception() -> None:
    """Test operation exception handling."""
    original_exception = ValueError("Original error")

    with pytest.raises(FlextOracleWmsError) as exc_info:
        handle_operation_exception(original_exception, "test operation")

    assert "Original error" in str(exc_info.value)
    assert exc_info.value.__cause__ == original_exception


def test_entity_name_edge_cases() -> None:
    """Test entity name validation edge cases."""
    # Test very long name
    long_name = "a" * 200
    result = flext_oracle_wms_validate_entity_name(long_name)
    assert result.is_failure
    assert "too long" in result.error

    # Test whitespace handling
    result = flext_oracle_wms_validate_entity_name("  order_hdr  ")
    assert result.success
    assert result.data == "order_hdr"

    # Test invalid characters
    result = flext_oracle_wms_validate_entity_name("invalid@name")
    assert result.is_failure
    assert "Invalid entity name format" in result.error
