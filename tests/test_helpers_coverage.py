"""Tests for helpers module - focusing on coverage improvement."""

from unittest.mock import Mock

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


class TestHelpersCoverage:
    """Test helper functions with comprehensive coverage."""

    def test_validate_entity_name_comprehensive(self) -> None:
      """Test entity name validation comprehensively."""
      # Test successful cases
      test_cases = [
          ("order_hdr", "order_hdr"),
          ("ORDER_HDR", "order_hdr"),
          ("  ITEM_MASTER  ", "item_master"),
          ("facility123", "facility123"),
      ]

      for input_name, expected in test_cases:
          result = flext_oracle_wms_validate_entity_name(input_name)
          assert result.success
          assert result.data == expected

      # Test failure cases
      failure_cases = [
          "",
          "   ",
          "a" * 300,  # Too long
          "invalid@name",  # Invalid characters
      ]

      for invalid_name in failure_cases:
          result = flext_oracle_wms_validate_entity_name(invalid_name)
          assert result.is_failure

    def test_normalize_url_edge_cases(self) -> None:
      """Test URL normalization edge cases."""
      # Test normal cases
      assert (
          flext_oracle_wms_normalize_url("https://api.com", "v1/orders")
          == "https://api.com/v1/orders"
      )
      assert (
          flext_oracle_wms_normalize_url("https://api.com/", "/v1/orders")
          == "https://api.com/v1/orders"
      )

      # Test empty base URL
      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_normalize_url("", "v1/orders")

      # Test whitespace only base URL
      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_normalize_url("   ", "v1/orders")

    def test_build_entity_url_comprehensive(self) -> None:
      """Test entity URL building comprehensively."""
      # Test normal case
      result = flext_oracle_wms_build_entity_url(
          "https://wms.com",
          "prod",
          "orders",
          "v2",
      )
      expected = "https://wms.com/prod/wms/lgfapi/v2/entity/orders/"
      assert result == expected

      # Test with default version
      result = flext_oracle_wms_build_entity_url("https://wms.com", "test", "items")
      expected = "https://wms.com/test/wms/lgfapi/v10/entity/items/"
      assert result == expected

      # Test with empty parameters
      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_build_entity_url("", "prod", "orders")

      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_build_entity_url("https://wms.com", "", "orders")

      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_build_entity_url("https://wms.com", "prod", "")

    def test_extract_environment_edge_cases(self) -> None:
      """Test environment extraction edge cases."""
      test_cases = [
          ("https://wms.com/production/api", "production"),
          ("https://wms.com/dev/v1", "dev"),
          ("https://wms.com", FlextOracleWmsDefaults.DEFAULT_ENVIRONMENT),
          ("https://wms.com/", FlextOracleWmsDefaults.DEFAULT_ENVIRONMENT),
      ]

      for url, expected in test_cases:
          result = flext_oracle_wms_extract_environment_from_url(url)
          assert result == expected

      # Test invalid URLs
      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_extract_environment_from_url("")

      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_extract_environment_from_url("   ")

    def test_validate_api_response_comprehensive(self) -> None:
      """Test API response validation comprehensively."""
      # Test successful responses
      good_responses = [
          {"data": [{"id": 1}]},
          {"results": []},
          {"message": "Success"},
          {"status": "OK"},
      ]

      for response in good_responses:
          result = flext_oracle_wms_validate_api_response(response)
          assert result.success

      # Test error responses
      error_responses = [
          {"error": "Not found"},
          {"error": "Invalid request", "code": 400},
          {"message": "Error: Failed to process"},
          {"message": "Internal server error occurred"},
      ]

      for response in error_responses:
          result = flext_oracle_wms_validate_api_response(response)
          assert result.is_failure
          assert "API error" in result.error

    def test_extract_pagination_info_comprehensive(self) -> None:
      """Test pagination info extraction comprehensively."""
      # Test complete pagination info
      response = {
          "page_nbr": 3,
          "page_count": 10,
          "result_count": 500,
          "next_page": "https://api.com/next",
          "previous_page": "https://api.com/prev",
      }

      result = flext_oracle_wms_extract_pagination_info(response)

      assert result["current_page"] == 3
      assert result["total_pages"] == 10
      assert result["total_results"] == 500
      assert result["has_next"] is True
      assert result["has_previous"] is True
      assert result["next_url"] == "https://api.com/next"
      assert result["previous_url"] == "https://api.com/prev"

      # Test minimal pagination info
      minimal_response = {}
      result = flext_oracle_wms_extract_pagination_info(minimal_response)

      assert result["current_page"] == 1
      assert result["total_pages"] == 1
      assert result["total_results"] == 0
      assert result["has_next"] is False
      assert result["has_previous"] is False

    def test_format_timestamp_comprehensive(self) -> None:
      """Test timestamp formatting comprehensively."""
      # Test with valid timestamp
      timestamp = "2025-01-15T10:30:00Z"
      result = flext_oracle_wms_format_timestamp(timestamp)
      assert result == timestamp

      # Test with None
      result = flext_oracle_wms_format_timestamp(None)
      assert isinstance(result, str)
      assert "T" in result

      # Test with empty string
      result = flext_oracle_wms_format_timestamp("")
      assert isinstance(result, str)
      assert "T" in result

      # Test with non-string timestamp (converts to string)
      result = flext_oracle_wms_format_timestamp(123)  # Invalid type
      assert result == "123"  # Converts to string

    def test_chunk_records_comprehensive(self) -> None:
      """Test record chunking comprehensively."""
      records = [{"id": i} for i in range(25)]

      # Test normal chunking
      chunks = flext_oracle_wms_chunk_records(records, 10)
      assert len(chunks) == 3
      assert len(chunks[0]) == 10
      assert len(chunks[1]) == 10
      assert len(chunks[2]) == 5

      # Test exact division
      chunks = flext_oracle_wms_chunk_records(records[:20], 10)
      assert len(chunks) == 2
      assert all(len(chunk) == 10 for chunk in chunks)

      # Test invalid parameters
      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_chunk_records(records, 0)

      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_chunk_records(records, -1)

      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_chunk_records(records, 10000)  # Too large

      with pytest.raises(FlextOracleWmsError):
          flext_oracle_wms_chunk_records("not a list", 10)

    def test_validation_functions_comprehensive(self) -> None:
      """Test DRY validation functions comprehensively."""
      # Test validate_records_list
      validate_records_list([{"a": 1}, {"b": 2}])  # Should pass

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Records must be a list",
      ):
          validate_records_list("not a list")

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Records must be a list",
      ):
          validate_records_list({"not": "list"})

      # Test validate_dict_parameter
      validate_dict_parameter({"key": "value"}, "config")  # Should pass

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Config must be a dictionary",
      ):
          validate_dict_parameter("not a dict", "config")

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Settings must be a dictionary",
      ):
          validate_dict_parameter(123, "settings")

      # Test validate_string_parameter
      validate_string_parameter("valid string", "name")  # Should pass
      validate_string_parameter("", "optional", allow_empty=True)  # Should pass

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Name must be a string",
      ):
          validate_string_parameter(123, "name")

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Title must be a non-empty string",
      ):
          validate_string_parameter("", "title", allow_empty=False)

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Description must be a non-empty string",
      ):
          validate_string_parameter("   ", "description", allow_empty=False)

    def test_handle_operation_exception_comprehensive(self) -> None:
      """Test operation exception handling comprehensively."""
      original_error = ValueError("Original problem")

      # Test with default logger
      with pytest.raises(FlextOracleWmsError) as exc_info:
          handle_operation_exception(original_error, "test operation")

      assert "Original problem" in str(exc_info.value)
      assert exc_info.value.__cause__ == original_error

      # Test with custom logger
      mock_logger = Mock()
      with pytest.raises(FlextOracleWmsError):
          handle_operation_exception(
              original_error,
              "custom operation",
              mock_logger,
              entity_id="test123",
              operation_type="validation",
          )

      mock_logger.error.assert_called_once()
      call_args = mock_logger.error.call_args
      assert "custom operation" in call_args[0][1]
      assert "entity_id=test123" in call_args[0][2]
      assert "operation_type=validation" in call_args[0][2]

    def test_error_message_formatting(self) -> None:
      """Test error message formatting in validation functions."""
      # Test field name capitalization in error messages
      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Test_field must be a list",
      ):
          validate_records_list("invalid", "test_field")

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="User_config must be a dictionary",
      ):
          validate_dict_parameter("invalid", "user_config")

      with pytest.raises(
          FlextOracleWmsDataValidationError,
          match="Entity_name must be a string",
      ):
          validate_string_parameter(None, "entity_name")

    def test_pagination_field_mappings(self) -> None:
      """Test pagination field mapping constants."""
      # Test that pagination extraction uses correct field constants
      response = {
          "page_nbr": 5,  # Using correct constant name
          "page_count": 20,
          "result_count": 1000,
      }

      result = flext_oracle_wms_extract_pagination_info(response)
      assert result["current_page"] == 5
      assert result["total_pages"] == 20
      assert result["total_results"] == 1000
